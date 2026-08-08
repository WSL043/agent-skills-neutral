from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "dist" / "runtime"
SOURCE_REPOSITORY = "WSL043/agent-skills-neutral"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
ALLOWED_TOP_LEVEL_FILES = {"AGENTS.md", "runtime-catalog.json", "MANIFEST.json"}
ALLOWED_TOP_LEVEL_DIRS = {"skills"}
IGNORED_FILE_NAMES = {".DS_Store"}
IGNORED_DIR_NAMES = {"__pycache__"}


class BundleError(RuntimeError):
    pass


def _markdown_headings(text: str) -> list[tuple[int, int, str]]:
    """Return real H1/H2 headings, ignoring fenced Markdown blocks."""
    headings: list[tuple[int, int, str]] = []
    in_fence = False
    fence_char = ""
    fence_length = 0
    for index, line in enumerate(text.splitlines(keepends=True)):
        stripped = line.lstrip(" \t")
        fence = re.match(r"(`{3,}|~{3,})(?:[^`~]*)?(?:\r?\n)?$", stripped)
        if fence:
            marker = fence.group(1)
            if not in_fence:
                in_fence = True
                fence_char = marker[0]
                fence_length = len(marker)
            elif marker[0] == fence_char and len(marker) >= fence_length:
                in_fence = False
                fence_char = ""
                fence_length = 0
            continue
        if in_fence:
            continue
        heading = re.match(r"^(#{1,2})[ \t]+([^\r\n]*?)[ \t]*(?:\r?\n)?$", line)
        if heading:
            headings.append((index, len(heading.group(1)), heading.group(2).strip()))
    return headings


def strip_terminal_provenance(text: str) -> str:
    """Remove one terminal, real top-level ``## Provenance`` section."""
    lines = text.splitlines(keepends=True)
    headings = _markdown_headings(text)
    provenance = [
        heading
        for heading in headings
        if heading[1] == 2 and heading[2] == "Provenance"
    ]
    if len(provenance) > 1:
        raise BundleError("multiple real top-level Provenance sections")
    if not provenance:
        return text

    start = provenance[0][0]
    if any(index > start for index, _level, _title in headings):
        raise BundleError("Provenance section must be terminal")

    prefix = "".join(lines[:start])
    prefix = re.sub(r"(?:\r?\n)+$", "", prefix)
    return prefix + "\n"


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BundleError(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise BundleError(f"JSON root must be an object: {path}")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def prefixed_digest(path: Path) -> str:
    return f"sha256:{sha256_file(path)}"


def git_output(*args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise BundleError(
            f"git {' '.join(args)} failed: {completed.stderr.strip() or completed.stdout.strip()}"
        )
    return completed.stdout.strip()


def git_state() -> tuple[str, bool]:
    commit = git_output("rev-parse", "HEAD")
    if not SHA_RE.fullmatch(commit):
        raise BundleError(f"unexpected git HEAD: {commit!r}")
    dirty = bool(git_output("status", "--porcelain", "--untracked-files=all"))
    return commit, dirty


def validate_source_catalogs() -> tuple[dict[str, Any], dict[str, Any]]:
    catalog_path = ROOT / "catalog.json"
    runtime_path = ROOT / "runtime-catalog.json"
    catalog = read_json(catalog_path)
    runtime = read_json(runtime_path)

    catalog_items = catalog.get("skills")
    runtime_items = runtime.get("skills")
    if not isinstance(catalog_items, list) or not isinstance(runtime_items, list):
        raise BundleError("catalog and runtime catalog must contain skill lists")
    if runtime.get("routing_authority") != "model-native-semantic":
        raise BundleError("runtime catalog routing authority must be model-native-semantic")

    canonical: dict[str, dict[str, Any]] = {}
    for item in catalog_items:
        if not isinstance(item, dict):
            raise BundleError("catalog skill entry must be an object")
        name = item.get("name")
        path = item.get("path")
        if not isinstance(name, str) or not name:
            raise BundleError("catalog skill has invalid name")
        if name in canonical:
            raise BundleError(f"duplicate catalog skill: {name}")
        if path != f"skills/{name}":
            raise BundleError(f"catalog path is not canonical for {name}: {path!r}")
        canonical[name] = item

    runtime_names: set[str] = set()
    for item in runtime_items:
        if not isinstance(item, dict):
            raise BundleError("runtime catalog skill entry must be an object")
        if set(item) != {"name", "description", "location"}:
            raise BundleError(
                f"runtime catalog entry must expose only name/description/location: {item.get('name')!r}"
            )
        name = item.get("name")
        if not isinstance(name, str) or name not in canonical:
            raise BundleError(f"runtime catalog contains unknown skill: {name!r}")
        if name in runtime_names:
            raise BundleError(f"duplicate runtime catalog skill: {name}")
        runtime_names.add(name)
        if item.get("description") != canonical[name].get("description"):
            raise BundleError(f"runtime/catalog description mismatch: {name}")
        if item.get("location") != f"skills/{name}/SKILL.md":
            raise BundleError(f"runtime location mismatch: {name}")

    if runtime_names != set(canonical):
        raise BundleError(
            "runtime catalog does not exactly match canonical catalog: "
            f"missing={sorted(set(canonical) - runtime_names)} "
            f"extra={sorted(runtime_names - set(canonical))}"
        )
    return catalog, runtime


def should_ignore(relative: Path) -> bool:
    if any(part in IGNORED_DIR_NAMES for part in relative.parts[:-1]):
        return True
    if relative.name in IGNORED_FILE_NAMES or relative.suffix == ".pyc":
        return True
    return False


def copy_skill_tree(source: Path, destination: Path) -> None:
    if not source.is_dir():
        raise BundleError(f"missing canonical skill directory: {source}")
    for path in sorted(source.rglob("*"), key=lambda item: item.as_posix()):
        relative = path.relative_to(source)
        if should_ignore(relative):
            continue
        if path.is_symlink():
            raise BundleError(f"runtime skill contains a symlink: {path}")
        if any(part.startswith(".") for part in relative.parts):
            raise BundleError(f"runtime skill contains hidden content: {path}")
        target = destination / relative
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif path.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            if path == source / "SKILL.md":
                target.write_bytes(strip_terminal_provenance(path.read_text(encoding="utf-8")).encode("utf-8"))
                shutil.copystat(path, target)
            else:
                shutil.copy2(path, target)
        else:
            raise BundleError(f"unsupported filesystem entry in skill: {path}")


def bundle_files(bundle: Path) -> list[Path]:
    return sorted(
        (
            path
            for path in bundle.rglob("*")
            if path.is_file() and path.name != "MANIFEST.json"
        ),
        key=lambda item: item.relative_to(bundle).as_posix(),
    )


def skill_digest(bundle: Path, name: str, file_entries: list[dict[str, Any]]) -> str:
    prefix = f"skills/{name}/"
    matching = [entry for entry in file_entries if str(entry["path"]).startswith(prefix)]
    if not matching:
        raise BundleError(f"runtime skill has no files: {name}")
    digest = hashlib.sha256()
    for entry in matching:
        digest.update(str(entry["path"]).encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(entry["sha256"]).encode("ascii"))
        digest.update(b"\0")
        digest.update(str(entry["bytes"]).encode("ascii"))
        digest.update(b"\n")
    return f"sha256:{digest.hexdigest()}"


def build_manifest(
    bundle: Path,
    *,
    source_commit: str,
    source_dirty: bool,
    catalog: dict[str, Any],
    runtime_catalog: dict[str, Any],
) -> dict[str, Any]:
    files: list[dict[str, Any]] = []
    for path in bundle_files(bundle):
        relative = path.relative_to(bundle).as_posix()
        data = path.read_bytes()
        files.append(
            {
                "path": relative,
                "sha256": sha256_bytes(data),
                "bytes": len(data),
            }
        )

    skills: list[dict[str, Any]] = []
    runtime_items = runtime_catalog.get("skills", [])
    for item in runtime_items:
        name = item["name"]
        skills.append(
            {
                "name": name,
                "location": item["location"],
                "digest": skill_digest(bundle, name, files),
            }
        )

    return {
        "schema_version": 1,
        "source_repository": SOURCE_REPOSITORY,
        "source_commit": source_commit,
        "source_dirty": source_dirty,
        "routing_authority": "model-native-semantic",
        "catalog_digest": f"sha256:{sha256_file(ROOT / 'catalog.json')}",
        "runtime_catalog_digest": f"sha256:{sha256_file(bundle / 'runtime-catalog.json')}",
        "skills": skills,
        "files": files,
    }


def prepare_output(output: Path) -> Path:
    output = output.expanduser().resolve()
    dist_root = (ROOT / "dist").resolve()
    if output == ROOT or ROOT.is_relative_to(output):
        raise BundleError(
            f"refusing unsafe output path at or above source repository: {output}"
        )
    if output.is_relative_to(ROOT) and not output.is_relative_to(dist_root):
        raise BundleError(
            f"output inside source repository must be under dist/: {output}"
        )
    if output.exists():
        if output.is_symlink():
            raise BundleError(f"refusing to replace symlink output: {output}")
        if not output.is_dir():
            raise BundleError(f"output exists and is not a directory: {output}")
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=False)
    return output


def build_bundle(output: Path, allow_dirty: bool) -> dict[str, Any]:
    catalog, runtime_catalog = validate_source_catalogs()
    source_commit, source_dirty = git_state()
    if source_dirty and not allow_dirty:
        raise BundleError(
            "source tree is dirty; commit or revert changes before a production build, "
            "or use --allow-dirty for local pre-validation"
        )

    bundle = prepare_output(output)
    shutil.copy2(ROOT / "runtime" / "AGENTS.md", bundle / "AGENTS.md")
    shutil.copy2(ROOT / "runtime-catalog.json", bundle / "runtime-catalog.json")

    for item in catalog["skills"]:
        name = item["name"]
        copy_skill_tree(ROOT / item["path"], bundle / "skills" / name)

    manifest = build_manifest(
        bundle,
        source_commit=source_commit,
        source_dirty=source_dirty,
        catalog=catalog,
        runtime_catalog=runtime_catalog,
    )
    write_json(bundle / "MANIFEST.json", manifest)
    verify_bundle(bundle)
    return manifest


def validate_manifest_shape(manifest: dict[str, Any]) -> None:
    if manifest.get("schema_version") != 1:
        raise BundleError("unsupported runtime manifest schema version")
    if manifest.get("source_repository") != SOURCE_REPOSITORY:
        raise BundleError("runtime manifest source repository mismatch")
    if not SHA_RE.fullmatch(str(manifest.get("source_commit", ""))):
        raise BundleError("runtime manifest source commit is invalid")
    if not isinstance(manifest.get("source_dirty"), bool):
        raise BundleError("runtime manifest source_dirty must be boolean")
    if manifest.get("routing_authority") != "model-native-semantic":
        raise BundleError("runtime manifest routing authority mismatch")
    for field in ("catalog_digest", "runtime_catalog_digest"):
        value = manifest.get(field)
        if not isinstance(value, str) or not value.startswith("sha256:") or not DIGEST_RE.fullmatch(value[7:]):
            raise BundleError(f"runtime manifest {field} is invalid")
    if not isinstance(manifest.get("skills"), list) or not isinstance(manifest.get("files"), list):
        raise BundleError("runtime manifest skills/files must be lists")


def verify_bundle(bundle: Path) -> dict[str, Any]:
    bundle = bundle.expanduser().resolve()
    if not bundle.is_dir():
        raise BundleError(f"runtime bundle does not exist: {bundle}")

    manifest_path = bundle / "MANIFEST.json"
    manifest = read_json(manifest_path)
    validate_manifest_shape(manifest)

    top_names = {path.name for path in bundle.iterdir()}
    unexpected = top_names - ALLOWED_TOP_LEVEL_FILES - ALLOWED_TOP_LEVEL_DIRS
    missing = {"AGENTS.md", "runtime-catalog.json", "MANIFEST.json", "skills"} - top_names
    if unexpected:
        raise BundleError(f"unexpected runtime top-level content: {sorted(unexpected)}")
    if missing:
        raise BundleError(f"missing runtime top-level content: {sorted(missing)}")

    runtime_catalog = read_json(bundle / "runtime-catalog.json")
    if runtime_catalog.get("routing_authority") != "model-native-semantic":
        raise BundleError("runtime bundle catalog is not model-native-semantic")
    runtime_items = runtime_catalog.get("skills")
    if not isinstance(runtime_items, list):
        raise BundleError("runtime bundle catalog skills must be a list")

    actual_files = bundle_files(bundle)
    actual_paths = [path.relative_to(bundle).as_posix() for path in actual_files]
    file_entries = manifest["files"]
    if not all(isinstance(item, dict) for item in file_entries):
        raise BundleError("runtime manifest file entry must be an object")
    manifest_paths = [str(item.get("path", "")) for item in file_entries]
    if manifest_paths != sorted(manifest_paths) or manifest_paths != actual_paths:
        raise BundleError("runtime manifest file inventory does not exactly match bundle files")

    for entry, path in zip(file_entries, actual_files, strict=True):
        data = path.read_bytes()
        digest = sha256_bytes(data)
        if entry.get("sha256") != digest or entry.get("bytes") != len(data):
            raise BundleError(f"runtime file digest/size mismatch: {entry.get('path')}")

    runtime_digest = f"sha256:{sha256_file(bundle / 'runtime-catalog.json')}"
    if manifest.get("runtime_catalog_digest") != runtime_digest:
        raise BundleError("runtime catalog digest does not match manifest")

    runtime_names: list[str] = []
    runtime_locations: dict[str, str] = {}
    for item in runtime_items:
        if not isinstance(item, dict) or set(item) != {"name", "description", "location"}:
            raise BundleError("runtime catalog exposes unsupported metadata")
        name = item.get("name")
        location = item.get("location")
        if not isinstance(name, str) or not isinstance(location, str):
            raise BundleError("runtime catalog entry has invalid name/location")
        if name in runtime_locations:
            raise BundleError(f"duplicate runtime skill: {name}")
        if location != f"skills/{name}/SKILL.md":
            raise BundleError(f"runtime skill location mismatch: {name}")
        if not (bundle / location).is_file():
            raise BundleError(f"runtime skill location missing: {name}")
        runtime_names.append(name)
        runtime_locations[name] = location

    manifest_skills = manifest["skills"]
    if not all(isinstance(item, dict) for item in manifest_skills):
        raise BundleError("runtime manifest skill entry must be an object")
    manifest_names = [str(item.get("name", "")) for item in manifest_skills]
    if manifest_names != runtime_names:
        raise BundleError("runtime manifest skill ordering/set does not match runtime catalog")
    for entry in manifest_skills:
        name = str(entry["name"])
        if entry.get("location") != runtime_locations[name]:
            raise BundleError(f"runtime manifest skill location mismatch: {name}")
        expected = skill_digest(bundle, name, file_entries)
        if entry.get("digest") != expected:
            raise BundleError(f"runtime skill digest mismatch: {name}")

    forbidden_names = {
        "provenance.json",
        "upstreams.json",
        "catalog.json",
        "index.json",
        "routes",
        "profiles",
        "docs",
        "scripts",
        "tests",
        "schemas",
        ".github",
        ".evolution",
    }
    leaked = sorted(name for name in forbidden_names if (bundle / name).exists())
    if leaked:
        raise BundleError(f"maintainer/control-plane content leaked into runtime bundle: {leaked}")

    return {
        "bundle": str(bundle),
        "source_commit": manifest["source_commit"],
        "source_dirty": manifest["source_dirty"],
        "skills": len(runtime_names),
        "files": len(file_entries),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build or verify the generated runtime-only Agent Skills bundle. "
            "The bundle excludes evolution, provenance, discovery, tests, and maintainer infrastructure."
        )
    )
    sub = parser.add_subparsers(dest="command", required=True)

    build = sub.add_parser("build", help="Build a runtime bundle from canonical source.")
    build.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    build.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Allow local pre-validation from a dirty tree; manifest will record source_dirty=true.",
    )

    verify = sub.add_parser("verify", help="Verify an existing runtime bundle and manifest.")
    verify.add_argument("--bundle", type=Path, default=DEFAULT_OUTPUT)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.command == "build":
            result = build_bundle(args.output, args.allow_dirty)
            summary = {
                "bundle": str(args.output.expanduser().resolve()),
                "source_commit": result["source_commit"],
                "source_dirty": result["source_dirty"],
                "skills": len(result["skills"]),
                "files": len(result["files"]),
            }
        else:
            summary = verify_bundle(args.bundle)
    except (BundleError, OSError, ValueError) as exc:
        print(f"RUNTIME BUNDLE ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
