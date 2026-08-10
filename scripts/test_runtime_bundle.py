from __future__ import annotations

import json
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

from build_runtime_bundle import (
    BundleError,
    _markdown_headings,
    strip_terminal_provenance,
    validate_thinking_core,
)


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_runtime_bundle.py"
CATALOG = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
EXPECTED_SKILLS = len(CATALOG.get("skills", []))
RETIRED_ADAPTERS = {
    "build-cli",
    "build-mcp-server",
    "capture-screen",
    "create-agent-skill",
    "discover-agent-skills",
    "finish-development-branch",
    "map-security-ownership",
    "prepare-repository-for-agents",
    "produce-programmatic-video",
    "resolve-merge-conflicts",
    "test-web-app",
    "use-git-worktrees",
    "work-with-docx",
    "work-with-jupyter-notebook",
    "work-with-pdf",
    "work-with-postgresql",
    "work-with-pptx",
    "work-with-xlsx",
}
errors: list[str] = []


def source_skill_digests() -> dict[str, str]:
    return {
        path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted((ROOT / "skills").glob("*/SKILL.md"))
    }


source_digests_before = source_skill_digests()


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


if EXPECTED_SKILLS <= 0:
    errors.append("canonical catalog has no skills")

for protected_name in ("skills", "docs"):
    protected_path = ROOT / protected_name
    protected = run("build", "--output", str(protected_path), "--allow-dirty", expected={1})
    error_text = protected.stderr.lower()
    if not any(marker in error_text for marker in ("source repository", "dist/", "unsafe output")):
        errors.append(f"source-protection error did not identify unsafe output: {protected.stderr}")
    if protected_name == "skills" and not (ROOT / "skills" / "clarify-requirements" / "SKILL.md").is_file():
        errors.append("source skill disappeared during destructive-path test")

with tempfile.TemporaryDirectory(prefix="agent-skills-runtime-test-") as temp:
    bundle = Path(temp) / "runtime"
    built = run("build", "--output", str(bundle), "--allow-dirty")
    if built.returncode == 0:
        try:
            summary = json.loads(built.stdout)
        except json.JSONDecodeError as exc:
            errors.append(f"build summary is not JSON: {exc}")
            summary = {}
        if summary.get("skills") != EXPECTED_SKILLS:
            errors.append(f"unexpected runtime skill count: {summary.get('skills')}")

    verified = run("verify", "--bundle", str(bundle))
    if verified.returncode == 0:
        try:
            verify_summary = json.loads(verified.stdout)
        except json.JSONDecodeError as exc:
            errors.append(f"verify summary is not JSON: {exc}")
            verify_summary = {}
        if verify_summary.get("skills") != EXPECTED_SKILLS:
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

    try:
        validate_thinking_core(bundle / "AGENTS.md")
    except BundleError as exc:
        errors.append(str(exc))
    source_core = ROOT / "runtime" / "AGENTS.md"
    bundled_core = bundle / "AGENTS.md"
    if bundled_core.is_file() and bundled_core.read_bytes() != source_core.read_bytes():
        errors.append("runtime thinking core is not the exact source contract")

    runtime_catalog_path = bundle / "runtime-catalog.json"
    if runtime_catalog_path.is_file():
        runtime = json.loads(runtime_catalog_path.read_text(encoding="utf-8"))
        runtime_names = {item.get("name") for item in runtime.get("skills", []) if isinstance(item, dict)}
        leaked_adapters = sorted(runtime_names & RETIRED_ADAPTERS)
        if leaked_adapters:
            errors.append(f"retired adapters leaked into runtime catalog: {leaked_adapters}")

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
        if len(manifest.get("skills", [])) != EXPECTED_SKILLS:
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

    for item in CATALOG.get("skills", []):
        name = item["name"]
        source = ROOT / item["path"] / "SKILL.md"
        generated = bundle / "skills" / name / "SKILL.md"
        if not generated.is_file():
            errors.append(f"generated SKILL.md missing for exact transform test: {name}")
            continue
        expected = strip_terminal_provenance(source.read_text(encoding="utf-8")).encode("utf-8")
        actual = generated.read_bytes()
        if actual != expected:
            errors.append(f"generated SKILL.md is not the exact provenance transform: {name}")
        generated_text = actual.decode("utf-8")
        real_provenance = [
            heading
            for heading in _markdown_headings(generated_text)
            if heading[1] == 2 and heading[2] == "Provenance"
        ]
        if real_provenance:
            errors.append(f"runtime SKILL.md retains real Provenance heading: {name}")
        if "../../provenance.json" in generated_text:
            errors.append(f"runtime SKILL.md retains provenance link: {name}")

    nonterminal = "# Skill\n\n## Provenance\n\nsource info\n\n## Decision rules\n\nimportant\n"
    try:
        strip_terminal_provenance(nonterminal)
    except BundleError:
        pass
    else:
        errors.append("non-terminal Provenance section was not rejected")

    fenced = "# Example\n\n```markdown\n## Provenance\n```\n\n## Decision rules\n\nKeep this.\n"
    if strip_terminal_provenance(fenced) != fenced:
        errors.append("fenced Provenance text was treated as a real heading")

    tilde_fenced = "# Example\n\n~~~markdown\n## Provenance\n~~~\n\n## Decision rules\n\nKeep this.\n"
    if strip_terminal_provenance(tilde_fenced) != tilde_fenced:
        errors.append("tilde-fenced Provenance text was treated as a real heading")

    duplicate = "# Skill\n\n## Provenance\n\nfirst\n\n## Provenance\n\nsecond\n"
    try:
        strip_terminal_provenance(duplicate)
    except BundleError:
        pass
    else:
        errors.append("duplicate Provenance sections were not rejected")

if source_skill_digests() != source_digests_before:
    errors.append("canonical SKILL.md digest inventory changed during runtime bundle tests")

if errors:
    print("RUNTIME BUNDLE TESTS FAILED")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print(
    f"RUNTIME BUNDLE TESTS PASSED skills={EXPECTED_SKILLS} "
    "tamper_guard=pass boundary_guard=pass"
)
