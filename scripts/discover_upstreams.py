from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "upstreams.json"
SELF_REPOSITORY = "WSL043/agent-skills-neutral"
API_ROOT = "https://api.github.com"
GITHUB_REPO_URL_RE = re.compile(
    r"https?://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)"
)

# These are discovery lenses, not quality gates. Add or revise lenses as the
# ecosystem vocabulary changes; acceptance happens later in the ingestion loop.
DEFAULT_QUERIES = [
    '"agent skills" in:name,description',
    '"agent skill" in:name,description',
    "topic:agent-skills",
    '"SKILL.md" "Agent Skills" in:readme',
]


def github_get(path: str) -> tuple[Any, dict[str, str]]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "skillconverge-discovery",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(f"{API_ROOT}{path}", headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
        return payload, {key.casefold(): value for key, value in response.headers.items()}


def has_next(link_header: str | None) -> bool:
    if not link_header:
        return False
    return any('rel="next"' in part for part in link_header.split(","))


def tracked_repositories() -> set[str]:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return {
        item["repository"]
        for item in state.get("repositories", [])
        if isinstance(item, dict) and isinstance(item.get("repository"), str)
    }


def search_repositories(query: str) -> list[dict[str, Any]]:
    page = 1
    found: list[dict[str, Any]] = []
    while True:
        encoded = urllib.parse.quote(query, safe="")
        # GitHub's repository-search API allows at most 100 results per page.
        payload, headers = github_get(
            f"/search/repositories?q={encoded}&per_page=100&page={page}"
        )
        if not isinstance(payload, dict):
            raise RuntimeError("invalid repository search response")
        items = payload.get("items", [])
        if not isinstance(items, list):
            raise RuntimeError("repository search response has no item list")
        found.extend(item for item in items if isinstance(item, dict))
        if not has_next(headers.get("link")):
            break
        page += 1
    return found


def license_id(item: dict[str, Any]) -> str | None:
    license_data = item.get("license")
    if not isinstance(license_data, dict):
        return None
    value = license_data.get("spdx_id")
    if not isinstance(value, str) or value in {"NOASSERTION", "OTHER"}:
        return None
    return value


def readme_text(repository: str) -> str | None:
    owner, name = repository.split("/", 1)
    payload, _ = github_get(f"/repos/{owner}/{name}/readme")
    if not isinstance(payload, dict):
        return None
    content = payload.get("content")
    encoding = payload.get("encoding")
    if not isinstance(content, str) or encoding != "base64":
        return None
    try:
        return base64.b64decode(content).decode("utf-8", errors="replace")
    except (ValueError, UnicodeError):
        return None


def normalize_repo_reference(owner: str, name: str) -> str:
    cleaned = name.rstrip(".,);]}>\"").removesuffix(".git")
    return f"{owner}/{cleaned}"


def referenced_repositories(
    repositories: set[str],
    errors: list[dict[str, str]],
) -> list[dict[str, Any]]:
    tracked_folded = {repository.casefold() for repository in repositories}
    references: dict[str, set[str]] = defaultdict(set)

    # This is intentionally a one-hop metadata crawl. It reads README text only
    # to extract GitHub repository URLs; it never treats the README as agent
    # instructions and never executes referenced content.
    for source in sorted(repositories, key=str.casefold):
        try:
            text = readme_text(source)
        except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError) as exc:
            errors.append({"repository": source, "readme_error": str(exc)})
            continue
        if not text:
            continue
        for owner, name in GITHUB_REPO_URL_RE.findall(text):
            target = normalize_repo_reference(owner, name)
            if target.casefold() == SELF_REPOSITORY.casefold():
                continue
            if target.casefold() in tracked_folded:
                continue
            references[target].add(source)

    return [
        {
            "repository": repository,
            "referenced_by": sorted(sources, key=str.casefold),
            "review_state": "untrusted-transitive-reference",
        }
        for repository, sources in sorted(
            references.items(), key=lambda item: item[0].casefold()
        )
    ]


def discover(queries: list[str]) -> dict[str, Any]:
    tracked = tracked_repositories()
    raw: dict[str, dict[str, Any]] = {}
    errors: list[dict[str, str]] = []

    for query in queries:
        try:
            items = search_repositories(query)
        except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError) as exc:
            errors.append({"query": query, "error": str(exc)})
            continue
        for item in items:
            full_name = item.get("full_name")
            if not isinstance(full_name, str):
                continue
            if full_name.casefold() == SELF_REPOSITORY.casefold():
                continue
            if item.get("fork") or item.get("archived"):
                continue
            entry = raw.setdefault(full_name, {"repository": item, "queries": set()})
            entry["queries"].add(query)

    candidates: list[dict[str, Any]] = []
    for repository in sorted(raw, key=str.casefold):
        if repository in tracked:
            continue
        item = raw[repository]["repository"]
        default_branch = item.get("default_branch")
        if not isinstance(default_branch, str) or not default_branch:
            continue
        candidates.append(
            {
                "repository": repository,
                "url": item.get("html_url"),
                "default_branch": default_branch,
                "license": license_id(item),
                "matched_queries": sorted(raw[repository]["queries"]),
                "review_state": "untrusted-search-candidate",
                "note": "File-level skill verification is deferred to review to keep discovery metadata-only.",
            }
        )

    transitive = referenced_repositories(tracked, errors)

    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "queries": queries,
        "tracked_count": len(tracked),
        "candidates": candidates,
        "transitive_references": transitive,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Discover untracked Agent Skill repositories and one-hop GitHub sources "
            "referenced by tracked upstreams. The command reads repository metadata "
            "and README URLs only; file-level inspection is deferred to review and no "
            "candidate content is executed or promoted."
        )
    )
    parser.add_argument(
        "--query",
        action="append",
        default=[],
        help="Additional/replacement GitHub repository search lens. Repeat as needed.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Write JSON to this path instead of stdout.",
    )
    args = parser.parse_args()

    queries = args.query or DEFAULT_QUERIES
    result = discover(queries)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)

    return 1 if result["errors"] and not result["candidates"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
