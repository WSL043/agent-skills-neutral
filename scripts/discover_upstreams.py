from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "upstreams.json"
SELF_REPOSITORY = "WSL043/agent-skills-neutral"
API_ROOT = "https://api.github.com"

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


def skill_paths(repository: str, default_branch: str) -> tuple[list[str], bool]:
    owner, name = repository.split("/", 1)
    ref = urllib.parse.quote(default_branch, safe="")
    payload, _ = github_get(
        f"/repos/{owner}/{name}/git/trees/{ref}?recursive=1"
    )
    if not isinstance(payload, dict):
        raise RuntimeError("invalid git tree response")
    paths = []
    for item in payload.get("tree", []):
        if not isinstance(item, dict) or item.get("type") != "blob":
            continue
        path = item.get("path")
        if isinstance(path, str) and Path(path).name.casefold() == "skill.md":
            paths.append(path)
    return sorted(set(paths)), bool(payload.get("truncated"))


def license_id(item: dict[str, Any]) -> str | None:
    license_data = item.get("license")
    if not isinstance(license_data, dict):
        return None
    value = license_data.get("spdx_id")
    if not isinstance(value, str) or value in {"NOASSERTION", "OTHER"}:
        return None
    return value


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
        try:
            paths, tree_truncated = skill_paths(repository, default_branch)
        except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError) as exc:
            errors.append({"repository": repository, "error": str(exc)})
            continue
        if not paths:
            continue
        candidates.append(
            {
                "repository": repository,
                "url": item.get("html_url"),
                "default_branch": default_branch,
                "license": license_id(item),
                "skill_paths": paths,
                "tree_truncated": tree_truncated,
                "matched_queries": sorted(raw[repository]["queries"]),
                "review_state": "untrusted-candidate",
            }
        )

    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "queries": queries,
        "tracked_count": len(tracked),
        "candidates": candidates,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Discover untracked GitHub repositories that contain SKILL.md files. "
            "The command reads metadata and file paths only; it does not execute or "
            "promote candidate content."
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
