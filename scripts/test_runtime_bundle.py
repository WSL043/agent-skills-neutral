from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_runtime_bundle.py"
errors: list[str] = []


def run(*args: str, expected: set[int] = {0}) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if completed.returncode not in expected:
        errors.append(
            f"command failed ({completed.returncode}): {' '.join(args)}\n"
            f"stdout={completed.stdout}\nstderr={completed.stderr}"
        )
    return completed


with tempfile.TemporaryDirectory(prefix="agent-skills-runtime-test-") as temp:
    bundle = Path(temp) / "runtime"
    built = run("build", "--output", str(bundle), "--allow-dirty")
    if built.returncode == 0:
        try:
            summary = json.loads(built.stdout)
        except json.JSONDecodeError as exc:
            errors.append(f"build summary is not JSON: {exc}")
            summary = {}
        if summary.get("skills") != 45:
            errors.append(f"unexpected runtime skill count: {summary.get('skills')}")

    verified = run("verify", "--bundle", str(bundle))
    if verified.returncode == 0:
        try:
            verify_summary = json.loads(verified.stdout)
        except json.JSONDecodeError as exc:
            errors.append(f"verify summary is not JSON: {exc}")
            verify_summary = {}
        if verify_summary.get("skills") != 45:
            errors.append(f"verified runtime skill count mismatch: {verify_summary.get('skills')}")

    required = {
        "AGENTS.md",
        "runtime-catalog.json",
        "MANIFEST.json",
        "skills",
    }
    actual = {path.name for path in bundle.iterdir()} if bundle.is_dir() else set()
    if actual != required:
        errors.append(f"runtime top-level surface mismatch: {sorted(actual)}")

    forbidden = {
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
    leaked = sorted(name for name in forbidden if (bundle / name).exists())
    if leaked:
        errors.append(f"maintainer content leaked into runtime bundle: {leaked}")

    manifest_path = bundle / "MANIFEST.json"
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("routing_authority") != "model-native-semantic":
            errors.append("manifest routing authority mismatch")
        if manifest.get("source_repository") != "WSL043/agent-skills-neutral":
            errors.append("manifest source repository mismatch")
        if len(manifest.get("skills", [])) != 45:
            errors.append("manifest skill count mismatch")

    target = bundle / "skills" / "clarify-requirements" / "SKILL.md"
    if target.is_file():
        original = target.read_bytes()
        target.write_bytes(original + b"\nTAMPERED\n")
        tampered = run("verify", "--bundle", str(bundle), expected={1})
        if tampered.returncode != 1 or "digest/size mismatch" not in tampered.stderr:
            errors.append("runtime verifier did not reject a tampered skill file")
        target.write_bytes(original)
        run("verify", "--bundle", str(bundle))

    leaked_file = bundle / "provenance.json"
    leaked_file.write_text("{}\n", encoding="utf-8")
    leakage = run("verify", "--bundle", str(bundle), expected={1})
    if leakage.returncode != 1 or "unexpected runtime top-level content" not in leakage.stderr:
        errors.append("runtime verifier did not reject leaked control-plane content")

if errors:
    print("RUNTIME BUNDLE TESTS FAILED")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("RUNTIME BUNDLE TESTS PASSED skills=45 tamper_guard=pass boundary_guard=pass")
