from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "upstreams.json"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def github_get(path: str) -> object:
    url = f"https://api.github.com{path}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "agent-skills-neutral-upstream-scanner",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def repo_head(repository: str) -> str:
    owner, name = repository.split("/", 1)
    payload = github_get(f"/repos/{owner}/{name}/commits?per_page=1")
    if not isinstance(payload, list) or not payload:
        raise RuntimeError("no commits returned")
    sha = payload[0].get("sha")
    if not isinstance(sha, str) or not SHA_RE.fullmatch(sha):
        raise RuntimeError("invalid head sha")
    return sha


def compare(repository: str, base: str, head: str) -> dict[str, object]:
    owner, name = repository.split("/", 1)
    base_q = urllib.parse.quote(base, safe="")
    head_q = urllib.parse.quote(head, safe="")
    payload = github_get(f"/repos/{owner}/{name}/compare/{base_q}...{head_q}")
    if not isinstance(payload, dict):
        raise RuntimeError("invalid compare response")

    skills: list[dict[str, str]] = []
    guidance: list[dict[str, str]] = []
    for file in payload.get("files", []):
        if not isinstance(file, dict):
            continue
        path = str(file.get("filename", ""))
        status = str(file.get("status", ""))
        lowered = path.lower()
        record = {"path": path, "status": status}
        if lowered.endswith("skill.md"):
            skills.append(record)
        elif lowered.endswith(("agents.md", "claude.md", "gemini.md", "copilot-instructions.md")):
            guidance.append(record)

    return {
        "status": payload.get("status"),
        "ahead_by": payload.get("ahead_by"),
        "behind_by": payload.get("behind_by"),
        "skill_changes": skills,
        "guidance_changes": guidance,
    }


def load_state() -> dict[str, object]:
    data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise RuntimeError("unsupported upstreams.json schema_version")
    return data


def scan(selected: set[str] | None) -> list[dict[str, object]]:
    data = load_state()
    results: list[dict[str, object]] = []

    for item in data.get("repositories", []):
        repository = item["repository"]
        if selected and repository not in selected:
            continue
        reviewed = item.get("last_reviewed_commit")
        result: dict[str, object] = {
            "repository": repository,
            "last_reviewed_commit": reviewed,
            "focus": item.get("focus", []),
        }
        try:
            head = repo_head(repository)
            result["head"] = head
            if reviewed is None:
                result["state"] = "unreviewed"
            elif reviewed == head:
                result["state"] = "current"
            else:
                result["state"] = "changed"
                result.update(compare(repository, reviewed, head))
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, RuntimeError) as exc:
            result["state"] = "error"
            result["error"] = str(exc)
        results.append(result)
    return results


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Report upstream Agent Skill deltas without modifying review state."
    )
    parser.add_argument(
        "--repo",
        action="append",
        default=[],
        help="Scan only this owner/repo. Repeat for multiple repositories.",
    )
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    selected = set(args.repo) or None
    results = scan(selected)

    if args.json:
        print(json.dumps({"repositories": results}, indent=2, ensure_ascii=False))
        return 0

    for item in results:
        state = item["state"]
        print(f"{state:10} {item['repository']}")
        if state == "changed":
            for change in item.get("skill_changes", []):
                print(f"  {change['status']:9} {change['path']}")
            if not item.get("skill_changes"):
                print("  no SKILL.md changes in compared delta")
        elif state == "unreviewed":
            print(f"  head {item['head']} — full first review required")
        elif state == "error":
            print(f"  {item['error']}")

    return 1 if any(item["state"] == "error" for item in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
