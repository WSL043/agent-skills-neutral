#!/usr/bin/env python3
"""Audit or install canonical skills without deleting local-only skills."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "skills"


class SyncError(RuntimeError):
    pass


def default_target() -> Path:
    profile = os.environ.get("USERPROFILE") or os.environ.get("HOME")
    if not profile:
        raise SyncError("USERPROFILE or HOME is required when --target is omitted")
    return Path(profile) / ".codex" / "skills"


def canonical_names() -> list[str]:
    catalog = json.loads((ROOT / "runtime-catalog.json").read_text(encoding="utf-8"))
    names = [item["name"] for item in catalog["skills"]]
    if names != sorted(names) or len(names) != len(set(names)):
        raise SyncError("runtime-catalog skill names must be unique and sorted")
    for name in names:
        if not (SOURCE_ROOT / name / "SKILL.md").is_file():
            raise SyncError(f"canonical skill is missing SKILL.md: {name}")
    return names


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        if path.is_symlink():
            raise SyncError(f"skill tree contains unsupported symlink: {path}")
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        data = path.read_bytes()
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest()


def resolve_target(value: str | None) -> Path:
    target = Path(value).expanduser() if value else default_target()
    target = target.resolve()
    if target == target.parent or target.name.lower() != "skills":
        raise SyncError("target must be an exact directory named 'skills'")
    return target


def inventory(target: Path, names: list[str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    canonical = set(names)
    for name in names:
        source = SOURCE_ROOT / name
        destination = target / name
        if not destination.exists():
            state = "missing"
        elif not destination.is_dir() or not (destination / "SKILL.md").is_file():
            state = "conflict"
        else:
            state = "current" if tree_digest(source) == tree_digest(destination) else "drifted"
        rows.append({"name": name, "state": state})

    if target.is_dir():
        for destination in sorted(target.iterdir(), key=lambda item: item.name.lower()):
            if (
                destination.is_dir()
                and destination.name not in canonical
                and (destination / "SKILL.md").is_file()
            ):
                rows.append({"name": destination.name, "state": "local_only"})
    return rows


def checked_destination(target: Path, name: str) -> Path:
    destination = target / name
    if destination.parent.resolve() != target:
        raise SyncError(f"destination escaped target root: {destination}")
    return destination


def install(target: Path, selected: list[str], replace: bool) -> list[dict[str, str]]:
    known = set(canonical_names())
    unknown = sorted(set(selected) - known)
    if unknown:
        raise SyncError(f"unknown canonical skills: {', '.join(unknown)}")
    if not selected:
        raise SyncError("install requires at least one explicit skill name")

    target.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, str]] = []
    for name in dict.fromkeys(selected):
        source = SOURCE_ROOT / name
        destination = checked_destination(target, name)
        if destination.exists():
            if destination.is_dir() and tree_digest(source) == tree_digest(destination):
                results.append({"name": name, "state": "current"})
                continue
            if not replace:
                results.append({"name": name, "state": "drifted"})
                continue
            if destination.is_symlink() or destination.is_file():
                destination.unlink()
            else:
                shutil.rmtree(destination)
        shutil.copytree(source, destination)
        results.append({"name": name, "state": "installed"})
    return results


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Audit or install canonical skills into an exact Codex skills directory."
    )
    result.add_argument("--target", help="Target directory; defaults to ~/.codex/skills")
    subparsers = result.add_subparsers(dest="command", required=True)
    subparsers.add_parser("audit", help="Report canonical and local-only skill state")
    install_parser = subparsers.add_parser("install", help="Install explicit canonical skills")
    install_parser.add_argument("names", nargs="+")
    install_parser.add_argument(
        "--replace",
        action="store_true",
        help="Replace an existing conflicting skill directory",
    )
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        target = resolve_target(args.target)
        if args.command == "audit":
            rows = inventory(target, canonical_names())
        else:
            rows = install(target, args.names, args.replace)
        print(json.dumps({"target": str(target), "skills": rows}, indent=2))
        return 0
    except (OSError, ValueError, SyncError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
