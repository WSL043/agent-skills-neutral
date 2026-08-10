from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "upstreams.json"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def git(*args: str, cwd: Path | None = None) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def repo_url(repository: str) -> str:
    return f"https://github.com/{repository}.git"


def repo_head(repository: str) -> str:
    output = git("ls-remote", repo_url(repository), "HEAD")
    if not output:
        raise RuntimeError("remote HEAD not found")
    sha = output.split()[0]
    if not SHA_RE.fullmatch(sha):
        raise RuntimeError("remote HEAD is not a full commit SHA")
    return sha


def compare(repository: str, base: str, head: str) -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="agent-skills-upstream-") as temp:
        work = Path(temp)
        git("init", "-q", cwd=work)
        git("remote", "add", "origin", repo_url(repository), cwd=work)
        git("fetch", "-q", "--no-tags", "--depth=1", "origin", base, cwd=work)
        git("fetch", "-q", "--no-tags", "--depth=1", "origin", head, cwd=work)
        output = git("diff", "--name-status", base, head, "--", cwd=work)

    skill_changes: list[dict[str, str]] = []
    guidance_changes: list[dict[str, str]] = []
    for line in output.splitlines():
        if not line.strip():
            continue
        fields = line.split("\t")
        status = fields[0]
        path = fields[-1]
        record = {"path": path, "status": status}
        lowered = path.lower()
        if lowered.endswith("skill.md"):
            skill_changes.append(record)
        elif lowered.endswith(("agents.md", "claude.md", "gemini.md", "copilot-instructions.md")):
            guidance_changes.append(record)

    return {
        "skill_changes": skill_changes,
        "guidance_changes": guidance_changes,
    }


def load_state() -> dict[str, object]:
    data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise RuntimeError("unsupported upstreams.json schema_version")
    return data


def scan(selected: set[str] | None) -> list[dict[str, object]]:
    if shutil.which("git") is None:
        raise RuntimeError("git is required to scan upstream repositories")

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
        except (subprocess.CalledProcessError, RuntimeError) as exc:
            result["state"] = "error"
            if isinstance(exc, subprocess.CalledProcessError):
                result["error"] = (exc.stderr or str(exc)).strip()
            else:
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
