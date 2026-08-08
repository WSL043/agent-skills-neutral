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

# These are discovery lenses, not quality gates. Acceptance happens later in
# the ingestion loop. Direct-skill search stays compact for low-cost local use.
DEFAULT_QUERIES = [
    '"agent skills" in:name,description',
    '"agent skill" in:name,description',
    "topic:agent-skills",
    '"SKILL.md" "Agent Skills" in:readme',
]

# Mechanism discovery deliberately looks outside repositories that call
# themselves Agent Skills. It is intended to surface implementations that may
# improve shared agent behavior: evaluation, reasoning, memory/context,
# self-correction, routing/tool choice, and learning from experience. The
# scheduled authenticated scan enables this lane; local callers can opt in.
DEFAULT_MECHANISM_QUERIES = [
    '"agent evaluation" in:name,description,readme',
    '"agent reasoning" in:name,description,readme',
    '"agent memory" in:name,description,readme',
    '"agent self improvement" in:name,description,readme',
    '"context engineering" in:name,description,readme',
    '"agent routing" in:name,description,readme',
    '"skill evolution" in:name,description,readme',
    '"self evolving agent" in:name,description,readme',
    '"self-evolving agent" in:name,description,readme',
    '"trajectory distillation" in:name,description,readme',
    '"agent experience learning" in:name,description,readme',
    '"memory optimization" in:name,description,readme',
    '"memory evolution" in:name,description,readme',
    '"context evolution" in:name,description,readme',
    '"agent harness optimization" in:name,description,readme',
    '"semantic skill routing" in:name,description,readme',
    '"skill retrieval" in:name,description,readme',
]

# Metadata-only review signals. They only affect review order; they never grant
# trust, acceptance, or promotion. Keep these semantic families broad and avoid
# numeric scores that would pretend discovery metadata measures quality.
CAPABILITY_LIFT_SIGNAL_PATTERNS: dict[str, tuple[str, ...]] = {
    "evaluation-verification": (
        "evaluation",
        "evaluator",
        "evals",
        "verification",
        "verifier",
        "grader",
        "benchmark",
        "held out",
        "held-out",
        "holdout",
        "validation gate",
        "evaluation gate",
        "judge calibration",
        "evaluator overfitting",
        "reward hacking",
        "reward gaming",
    ),
    "reasoning-planning": (
        "reasoning",
        "planner",
        "planning",
        "decomposition",
        "hypothesis",
        "decision making",
    ),
    "memory-context": (
        "agent memory",
        "memory system",
        "context engineering",
        "context management",
        "context compression",
        "memory optimization",
        "memory evolution",
        "memory consolidation",
        "memory retrieval",
        "context evolution",
        "context curation",
        "meta context",
        "context optimizer",
    ),
    "learning-self-correction": (
        "self improvement",
        "self-improvement",
        "self correction",
        "self-correction",
        "reflection",
        "reflexion",
        "learning agent",
    ),
    "routing-tool-selection": (
        "agent routing",
        "router",
        "tool selection",
        "tool routing",
        "tool use",
        "orchestration",
        "retrieval policy",
        "semantic routing",
        "semantic retrieval",
        "skill graph",
        "capability tree",
        "skill dependency",
        "hierarchical routing",
    ),
    "feedback-trajectory-distillation": (
        "trajectory",
        "distillation",
        "feedback loop",
        "experience replay",
        "skill learning",
        "skill evolution",
        "skill optimizer",
        "skill optimization",
        "skill distillation",
        "experience distillation",
        "trajectory analysis",
        "trajectory consolidation",
    ),
    "uncertainty-calibration": (
        "uncertainty",
        "calibration",
        "confidence calibration",
        "abstention",
    ),
}


def github_get(path: str) -> tuple[Any, dict[str, str]]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "agent-skills-neutral-discovery",
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


def repository_metadata_text(item: dict[str, Any]) -> str:
    values: list[str] = []
    for key in ("name", "full_name", "description"):
        value = item.get(key)
        if isinstance(value, str):
            values.append(value)
    topics = item.get("topics")
    if isinstance(topics, list):
        values.extend(topic for topic in topics if isinstance(topic, str))
    return " ".join(values).casefold()


def capability_lift_signals(item: dict[str, Any]) -> list[str]:
    text = repository_metadata_text(item)
    signals: list[str] = []
    for label, patterns in CAPABILITY_LIFT_SIGNAL_PATTERNS.items():
        if any(pattern.casefold() in text for pattern in patterns):
            signals.append(label)
    return signals


def discover(
    skill_queries: list[str],
    mechanism_queries: list[str],
) -> dict[str, Any]:
    tracked = tracked_repositories()
    raw: dict[str, dict[str, Any]] = {}
    errors: list[dict[str, str]] = []

    query_plan = [
        *(('skill', query) for query in skill_queries),
        *(('mechanism', query) for query in mechanism_queries),
    ]

    for lane, query in query_plan:
        try:
            items = search_repositories(query)
        except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError) as exc:
            errors.append({"lane": lane, "query": query, "error": str(exc)})
            continue
        for item in items:
            full_name = item.get("full_name")
            if not isinstance(full_name, str):
                continue
            if full_name.casefold() == SELF_REPOSITORY.casefold():
                continue
            if item.get("fork") or item.get("archived"):
                continue
            entry = raw.setdefault(
                full_name,
                {"repository": item, "queries": set(), "lanes": set()},
            )
            entry["queries"].add(query)
            entry["lanes"].add(lane)

    candidates: list[dict[str, Any]] = []
    for repository in raw:
        if repository in tracked:
            continue
        item = raw[repository]["repository"]
        default_branch = item.get("default_branch")
        if not isinstance(default_branch, str) or not default_branch:
            continue
        signals = capability_lift_signals(item)
        candidates.append(
            {
                "repository": repository,
                "url": item.get("html_url"),
                "default_branch": default_branch,
                "license": license_id(item),
                "candidate_lanes": sorted(raw[repository]["lanes"]),
                "capability_lift_signals": signals,
                "review_priority": "capability-lift-first" if signals else "normal",
                "matched_queries": sorted(raw[repository]["queries"]),
                "review_state": "untrusted-search-candidate",
                "note": (
                    "File-level verification is deferred to review. Metadata signals only "
                    "prioritize inspection and never imply trust, quality, or promotion."
                ),
            }
        )

    candidates.sort(
        key=lambda item: (
            item["review_priority"] != "capability-lift-first",
            item["repository"].casefold(),
        )
    )

    transitive = referenced_repositories(tracked, errors)

    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "skill_queries": skill_queries,
        "mechanism_queries": mechanism_queries,
        "tracked_count": len(tracked),
        "capability_lift_candidate_count": sum(
            1 for item in candidates if item["review_priority"] == "capability-lift-first"
        ),
        "candidates": candidates,
        "transitive_references": transitive,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Discover untracked Agent Skill repositories, optional high-value agent "
            "mechanism repositories, and one-hop GitHub sources referenced by tracked "
            "upstreams. Discovery is metadata-only; candidate content is never executed "
            "or promoted."
        )
    )
    parser.add_argument(
        "--query",
        action="append",
        default=[],
        help=(
            "Replacement direct-skill GitHub repository search lens. Repeat as needed. "
            "If omitted, the built-in direct-skill lenses are used."
        ),
    )
    parser.add_argument(
        "--include-mechanisms",
        action="store_true",
        help=(
            "Also search for evaluator/reasoning/memory/self-correction/routing/context "
            "implementations that may contain transferable agent-capability mechanisms."
        ),
    )
    parser.add_argument(
        "--mechanism-query",
        action="append",
        default=[],
        help=(
            "Replacement mechanism-discovery GitHub repository search lens. Repeat as "
            "needed; implies --include-mechanisms."
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Write JSON to this path instead of stdout.",
    )
    args = parser.parse_args()

    skill_queries = args.query or DEFAULT_QUERIES
    include_mechanisms = args.include_mechanisms or bool(args.mechanism_query)
    mechanism_queries = (
        (args.mechanism_query or DEFAULT_MECHANISM_QUERIES)
        if include_mechanisms
        else []
    )
    result = discover(skill_queries, mechanism_queries)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)

    return 1 if result["errors"] and not result["candidates"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
