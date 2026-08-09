from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
errors: list[str] = []
names: set[str] = set()
name_pattern = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
repo_pattern = re.compile(r"^[^/\s]+/[^/\s]+$")
sha_pattern = re.compile(r"^[0-9a-f]{40}$")
markdown_link_pattern = re.compile(r"\]\(([^)#]+\.md)(?:#[^)]+)?\)")


def real_h1_h2_headings(text: str) -> list[tuple[int, int, str]]:
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


def check_local_markdown_links(root: Path) -> None:
    for markdown_path in root.rglob("*.md"):
        text = markdown_path.read_text(encoding="utf-8")
        for target in markdown_link_pattern.findall(text):
            if "://" in target or target.startswith(("mailto:", "#")):
                continue
            resolved = (markdown_path.parent / target).resolve()
            if not resolved.is_file():
                errors.append(
                    f"missing markdown link: {markdown_path.relative_to(ROOT)} -> {target}"
                )


for item in catalog.get("skills", []):
    name = item.get("name", "")
    if name in names:
        errors.append(f"duplicate catalog name: {name}")
    names.add(name)
    if not name_pattern.fullmatch(name):
        errors.append(f"invalid name: {name}")
    if item.get("reference_level") not in {"S", "A"}:
        errors.append(f"unsupported reference level: {name} -> {item.get('reference_level')}")

    skill_dir = ROOT / item.get("path", "")
    skill_md = skill_dir / "SKILL.md"
    if skill_dir.name != name:
        errors.append(f"directory/name mismatch: {name} -> {skill_dir}")
    if not skill_md.is_file():
        errors.append(f"missing SKILL.md: {name}")
        continue

    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        errors.append(f"invalid frontmatter delimiters: {name}")
        continue
    frontmatter, body = text[4:].split("\n---\n", 1)
    fields = [
        line.split(":", 1)[0].strip()
        for line in frontmatter.splitlines()
        if ":" in line
    ]
    if fields != ["name", "description"]:
        errors.append(f"frontmatter fields must be name,description: {name} -> {fields}")
    if f"name: {name}" not in frontmatter:
        errors.append(f"frontmatter name mismatch: {name}")
    description_line = next(
        (line for line in frontmatter.splitlines() if line.startswith("description:")),
        "",
    )
    frontmatter_description = description_line.removeprefix("description:").strip()
    if (
        len(frontmatter_description) >= 2
        and frontmatter_description[0] == frontmatter_description[-1]
        and frontmatter_description[0] in {'"', "'"}
    ):
        frontmatter_description = frontmatter_description[1:-1]
    if frontmatter_description != item.get("description"):
        errors.append(f"frontmatter/catalog description mismatch: {name}")
    if not body.strip() or "TODO" in text or "Insert instructions" in text:
        errors.append(f"empty or placeholder body: {name}")

    headings = real_h1_h2_headings(text)
    provenance_headings = [
        heading
        for heading in headings
        if heading[1] == 2 and heading[2] == "Provenance"
    ]
    if len(provenance_headings) > 1:
        errors.append(f"multiple real top-level Provenance sections: {name}")
    elif provenance_headings:
        provenance_index = provenance_headings[0][0]
        if any(index > provenance_index for index, _level, _title in headings):
            errors.append(f"Provenance section must be terminal: {name}")

    agent_metadata = skill_dir / "agents" / "openai.yaml"
    if not agent_metadata.is_file():
        errors.append(f"missing agent metadata: {name}")
    elif "display_name:" not in agent_metadata.read_text(encoding="utf-8"):
        errors.append(f"invalid agent metadata: {name}")

    for related in item.get("related", []):
        if related not in {
            entry.get("name") for entry in catalog.get("skills", [])
        }:
            errors.append(f"unknown related skill: {name} -> {related}")

    if item.get("has_variants_reference") and not (
        skill_dir / "references" / "variants.md"
    ).is_file():
        errors.append(f"missing variants reference: {name}")

    check_local_markdown_links(skill_dir)


disk_names = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
if disk_names != names:
    errors.append(
        f"catalog/disk mismatch: catalog_only={sorted(names-disk_names)} "
        f"disk_only={sorted(disk_names-names)}"
    )

provenance_path = ROOT / "provenance.json"
source_repositories: set[str] = set()
mechanism_repositories: set[str] = set()
if not provenance_path.is_file():
    errors.append("missing provenance.json")
else:
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    source_snapshots = provenance.get("source_snapshots")
    mechanism_snapshots = provenance.get("mechanism_snapshots")
    if not isinstance(source_snapshots, dict):
        errors.append("provenance source_snapshots must be an object")
        source_snapshots = {}
    if not isinstance(mechanism_snapshots, dict):
        errors.append("provenance mechanism_snapshots must be an object")
        mechanism_snapshots = {}
    source_repositories = set(source_snapshots)
    mechanism_repositories = set(mechanism_snapshots)
    overlap = sorted(source_repositories & mechanism_repositories)
    if overlap:
        errors.append(f"provenance snapshot role overlap: {overlap}")
    provenance_skills = provenance.get("skills", {})
    if not isinstance(provenance_skills, dict):
        errors.append("provenance skills must be an object")
        provenance_skills = {}
    if set(provenance_skills) != names:
        errors.append(
            f"provenance/catalog mismatch: catalog_only={sorted(names-set(provenance_skills))} "
            f"provenance_only={sorted(set(provenance_skills)-names)}"
        )

    for snapshot_role, snapshots in (
        ("source", source_snapshots),
        ("mechanism", mechanism_snapshots),
    ):
        for repository, commit in snapshots.items():
            if not repo_pattern.fullmatch(repository):
                errors.append(f"invalid {snapshot_role} provenance repository: {repository}")
            if not sha_pattern.fullmatch(commit or ""):
                errors.append(
                    f"invalid {snapshot_role} provenance snapshot: {repository}@{commit}"
                )

    for skill_name, sources in provenance_skills.items():
        if not isinstance(sources, list) or not sources:
            errors.append(f"empty provenance sources: {skill_name}")
            continue
        for source in sources:
            if not isinstance(source, dict):
                errors.append(f"invalid provenance entry: {skill_name}")
                continue
            repository = source.get("repository")
            commit = source.get("commit")
            source_kind = source.get("source_kind", "direct")
            if source_kind == "direct":
                if repository not in source_snapshots:
                    errors.append(
                        f"provenance source repository missing from source_snapshots: "
                        f"{skill_name} -> {repository}"
                    )
            elif source_kind == "mechanism":
                if repository not in mechanism_snapshots:
                    errors.append(
                        f"provenance mechanism repository missing from mechanism_snapshots: "
                        f"{skill_name} -> {repository}"
                    )
                if repository in source_snapshots:
                    errors.append(
                        f"mechanism provenance repository also in source_snapshots: "
                        f"{skill_name} -> {repository}"
                    )
                adaptation_note = source.get("adaptation_note")
                if not isinstance(adaptation_note, str) or not adaptation_note.strip():
                    errors.append(
                        f"mechanism provenance missing adaptation note: {skill_name} -> {repository}"
                    )
            else:
                errors.append(
                    f"unknown provenance source_kind: {skill_name} -> {source_kind}"
                )
            if not sha_pattern.fullmatch(commit or ""):
                errors.append(f"invalid provenance commit: {skill_name} -> {commit}")
            url = source.get("url", "")
            if not isinstance(commit, str) or not isinstance(url, str) or commit not in url:
                errors.append(
                    f"unpinned provenance URL: {skill_name} -> {url}"
                )
            if source.get("license") and not source.get("license_url"):
                errors.append(
                    f"licensed adaptation missing license URL: {skill_name} -> {repository}"
                )
            if source.get("license") and not source.get("adaptation_note"):
                errors.append(
                    f"licensed adaptation missing change note: {skill_name} -> {repository}"
                )

upstreams_path = ROOT / "upstreams.json"
tracked_repositories: set[str] = set()
if not upstreams_path.is_file():
    errors.append("missing upstream review state: upstreams.json")
else:
    upstreams = json.loads(upstreams_path.read_text(encoding="utf-8"))
    if upstreams.get("schema_version") != 1:
        errors.append("unsupported upstreams.json schema_version")
    for item in upstreams.get("repositories", []):
        repository = item.get("repository", "")
        if not repo_pattern.fullmatch(repository):
            errors.append(f"invalid upstream repository: {repository}")
        if repository in tracked_repositories:
            errors.append(f"duplicate upstream repository: {repository}")
        tracked_repositories.add(repository)
        reviewed = item.get("last_reviewed_commit")
        if reviewed is not None and not sha_pattern.fullmatch(reviewed):
            errors.append(
                f"invalid upstream reviewed commit: {repository}@{reviewed}"
            )
        focus = item.get("focus")
        if not isinstance(focus, list) or not all(
            isinstance(value, str) and value for value in focus
        ):
            errors.append(f"invalid upstream focus list: {repository}")

    missing_tracked_sources = sorted(source_repositories - tracked_repositories)
    if missing_tracked_sources:
        errors.append(
            f"provenance sources missing from upstream tracking: {missing_tracked_sources}"
        )

evidence_schema_path = ROOT / "schemas" / "evolution-evidence.schema.json"
if not evidence_schema_path.is_file():
    errors.append("missing evolution evidence schema: schemas/evolution-evidence.schema.json")
else:
    try:
        evidence_schema = json.loads(evidence_schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid evolution evidence schema JSON: {exc}")
    else:
        if not isinstance(evidence_schema, dict) or evidence_schema.get("type") != "object":
            errors.append("evolution evidence schema top level must be an object schema")
        schema_properties = (
            evidence_schema.get("properties", {})
            if isinstance(evidence_schema, dict)
            else {}
        )
        schema_version = (
            schema_properties.get("schema_version", {})
            if isinstance(schema_properties, dict)
            else {}
        )
        if not isinstance(schema_version, dict) or schema_version.get("const") != 1:
            errors.append("evolution evidence schema_version must have const=1")
        required = evidence_schema.get("required", []) if isinstance(evidence_schema, dict) else []
        required_fields = {
            "schema_version",
            "candidate_id",
            "target",
            "claim",
            "proposal_evidence",
            "candidate_change",
            "acceptance_evidence",
            "decision",
        }
        if not isinstance(required, list) or not required_fields.issubset(required):
            errors.append(
                "evolution evidence schema required fields are incomplete"
            )

run_schema_path = ROOT / "schemas" / "evolution-run.schema.json"
if not run_schema_path.is_file():
    errors.append("missing evolution run schema: schemas/evolution-run.schema.json")
else:
    try:
        run_schema = json.loads(run_schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid evolution run schema JSON: {exc}")
    else:
        if not isinstance(run_schema, dict) or run_schema.get("type") != "object":
            errors.append("evolution run schema top level must be an object schema")
        run_properties = run_schema.get("properties", {}) if isinstance(run_schema, dict) else {}
        run_version = run_properties.get("schema_version", {}) if isinstance(run_properties, dict) else {}
        if not isinstance(run_version, dict) or run_version.get("const") != 1:
            errors.append("evolution run schema_version must have const=1")
        run_required = run_schema.get("required", []) if isinstance(run_schema, dict) else []
        run_required_fields = {
            "schema_version",
            "candidate_id",
            "contract",
            "phase",
            "promotion_authority",
            "evidence_packet",
            "experiments",
            "history",
        }
        if not isinstance(run_required, list) or not run_required_fields.issubset(run_required):
            errors.append("evolution run schema required fields are incomplete")
        authority = run_properties.get("promotion_authority", {}) if isinstance(run_properties, dict) else {}
        if not isinstance(authority, dict) or authority.get("const") != "explicit-curator":
            errors.append("evolution run promotion_authority must have const=explicit-curator")
        expected_contracts = {"satisfaction", "optimization", "discovery", "judgment"}
        contract = run_properties.get("contract", {}) if isinstance(run_properties, dict) else {}
        if not isinstance(contract, dict) or set(contract.get("enum", [])) != expected_contracts:
            errors.append("evolution run contract enum is unexpected")
        experiments = run_properties.get("experiments", {}) if isinstance(run_properties, dict) else {}
        experiment_properties = experiments.get("items", {}).get("properties", {}) if isinstance(experiments, dict) else {}
        expected_variants = {"baseline", "candidate", "reference"}
        expected_phases = {"proposal", "held-out", "regression", "transfer"}
        variant = experiment_properties.get("variant", {}) if isinstance(experiment_properties, dict) else {}
        phase = experiment_properties.get("phase", {}) if isinstance(experiment_properties, dict) else {}
        if not isinstance(variant, dict) or set(variant.get("enum", [])) != expected_variants:
            errors.append("evolution run experiment variant enum is unexpected")
        if not isinstance(phase, dict) or set(phase.get("enum", [])) != expected_phases:
            errors.append("evolution run experiment phase enum is unexpected")

runtime_manifest_schema_path = ROOT / "schemas" / "runtime-manifest.schema.json"
if not runtime_manifest_schema_path.is_file():
    errors.append("missing runtime manifest schema: schemas/runtime-manifest.schema.json")
else:
    try:
        runtime_manifest_schema = json.loads(
            runtime_manifest_schema_path.read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid runtime manifest schema JSON: {exc}")
    else:
        if not isinstance(runtime_manifest_schema, dict) or runtime_manifest_schema.get("type") != "object":
            errors.append("runtime manifest schema top level must be an object schema")
        runtime_properties = (
            runtime_manifest_schema.get("properties", {})
            if isinstance(runtime_manifest_schema, dict)
            else {}
        )
        runtime_version = (
            runtime_properties.get("schema_version", {})
            if isinstance(runtime_properties, dict)
            else {}
        )
        if not isinstance(runtime_version, dict) or runtime_version.get("const") != 1:
            errors.append("runtime manifest schema_version must have const=1")
        runtime_authority = (
            runtime_properties.get("routing_authority", {})
            if isinstance(runtime_properties, dict)
            else {}
        )
        if not isinstance(runtime_authority, dict) or runtime_authority.get("const") != "model-native-semantic":
            errors.append("runtime manifest routing_authority must have const=model-native-semantic")
        runtime_required_fields = {
            "schema_version",
            "source_repository",
            "source_commit",
            "source_dirty",
            "routing_authority",
            "catalog_digest",
            "runtime_catalog_digest",
            "skills",
            "files",
        }
        runtime_required = (
            runtime_manifest_schema.get("required", [])
            if isinstance(runtime_manifest_schema, dict)
            else []
        )
        if not isinstance(runtime_required, list) or not runtime_required_fields.issubset(runtime_required):
            errors.append("runtime manifest schema required fields are incomplete")
        runtime_skills = (
            runtime_properties.get("skills", {})
            if isinstance(runtime_properties, dict)
            else {}
        )
        runtime_files = (
            runtime_properties.get("files", {})
            if isinstance(runtime_properties, dict)
            else {}
        )
        if not isinstance(runtime_skills, dict) or runtime_skills.get("type") != "array":
            errors.append("runtime manifest skills property must be an array")
        if not isinstance(runtime_files, dict) or runtime_files.get("type") != "array":
            errors.append("runtime manifest files property must be an array")
        skill_items = runtime_skills.get("items", {}) if isinstance(runtime_skills, dict) else {}
        skill_required = skill_items.get("required", []) if isinstance(skill_items, dict) else []
        if not isinstance(skill_required, list) or not {"name", "location", "digest"}.issubset(skill_required):
            errors.append("runtime manifest skill required fields are incomplete")

attribution_schema_path = ROOT / "schemas" / "execution-attribution.schema.json"
if not attribution_schema_path.is_file():
    errors.append(
        "missing execution attribution schema: schemas/execution-attribution.schema.json"
    )
else:
    try:
        attribution_schema = json.loads(
            attribution_schema_path.read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid execution attribution schema JSON: {exc}")
    else:
        if not isinstance(attribution_schema, dict) or attribution_schema.get("type") != "object":
            errors.append("execution attribution schema top level must be an object schema")
        attribution_properties = (
            attribution_schema.get("properties", {})
            if isinstance(attribution_schema, dict)
            else {}
        )
        attribution_version = (
            attribution_properties.get("schema_version", {})
            if isinstance(attribution_properties, dict)
            else {}
        )
        if not isinstance(attribution_version, dict) or attribution_version.get("const") != 1:
            errors.append("execution attribution schema_version must have const=1")
        attribution_required_fields = {
            "schema_version",
            "record_type",
            "receipt_id",
            "recorded_at",
            "producer",
            "session",
            "runtime",
            "serving",
            "activation",
            "privacy",
            "integrity",
        }
        attribution_required = (
            attribution_schema.get("required", [])
            if isinstance(attribution_schema, dict)
            else []
        )
        if not isinstance(attribution_required, list) or set(attribution_required) != attribution_required_fields:
            errors.append("execution attribution schema required fields are incomplete or unexpected")
        privacy = (
            attribution_properties.get("privacy", {})
            if isinstance(attribution_properties, dict)
            else {}
        )
        privacy_properties = privacy.get("properties", {}) if isinstance(privacy, dict) else {}
        if not isinstance(privacy_properties, dict) or not privacy_properties or not all(
            isinstance(value, dict) and value.get("const") is False
            for value in privacy_properties.values()
        ):
            errors.append("execution attribution privacy properties must all have const=false")

behavior_schema_path = ROOT / "schemas" / "behavior-evidence.schema.json"
if not behavior_schema_path.is_file():
    errors.append("missing behavior evidence schema: schemas/behavior-evidence.schema.json")
else:
    try:
        behavior_schema = json.loads(behavior_schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid behavior evidence schema JSON: {exc}")
    else:
        behavior_properties = behavior_schema.get("properties", {})
        if (
            behavior_schema.get("type") != "object"
            or not isinstance(behavior_properties, dict)
            or behavior_properties.get("record_type", {}).get("const")
            != "behavior-evidence"
        ):
            errors.append("behavior evidence schema identity is invalid")

for required_path in (
    "runtime/AGENTS.md",
    "scripts/build_runtime_bundle.py",
    "scripts/test_runtime_bundle.py",
    "docs/RUNTIME_BUNDLE.md",
    "scripts/execution_attribution.py",
    "scripts/test_execution_attribution.py",
    "docs/EXECUTION_ATTRIBUTION.md",
    "schemas/behavior-evidence.schema.json",
):
    path = ROOT / required_path
    if not path.is_file() or not path.read_text(encoding="utf-8").strip():
        errors.append(f"runtime authoring surface file is missing or empty: {required_path}")

gitignore_path = ROOT / ".gitignore"
if not gitignore_path.is_file() or "dist/" not in gitignore_path.read_text(encoding="utf-8").splitlines():
    errors.append(".gitignore must contain an independent dist/ entry")

levels = Counter(
    item.get("reference_level") for item in catalog.get("skills", [])
)

index_path = ROOT / "index.json"
routed_names: list[str] = []
indexed_categories: set[str] = set()
runtime_catalog_path = ROOT / "runtime-catalog.json"
if not index_path.is_file():
    errors.append("missing compact routing index: index.json")
else:
    index = json.loads(index_path.read_text(encoding="utf-8"))
    if index.get("routing_authority") != "model-native-semantic":
        errors.append("index routing_authority is missing or unexpected")
    runtime_catalog_reference = index.get("runtime_catalog")
    if not isinstance(runtime_catalog_reference, str) or not runtime_catalog_reference:
        errors.append("index runtime_catalog is missing or invalid")
    else:
        indexed_runtime_path = ROOT / runtime_catalog_reference
        if not indexed_runtime_path.is_file():
            errors.append(f"missing indexed runtime catalog: {indexed_runtime_path}")
        elif indexed_runtime_path != runtime_catalog_path:
            errors.append(
                f"index runtime_catalog must point to runtime-catalog.json: {runtime_catalog_reference}"
            )
    if index.get("advisory_router") != "python scripts/select_skills.py <task> --json":
        errors.append("index advisory_router is missing or unexpected")

    categories = index.get("categories", [])
    for category in categories:
        category_name = category.get("name", "")
        if category_name in indexed_categories:
            errors.append(f"duplicate route category: {category_name}")
        indexed_categories.add(category_name)
        route_path = ROOT / category.get("route_file", "")
        if not route_path.is_file():
            errors.append(f"missing route file: {route_path}")
            continue
        route = json.loads(route_path.read_text(encoding="utf-8"))
        if route.get("category") != category_name:
            errors.append(f"route category mismatch: {route_path}")
        route_skills = route.get("skills", [])
        if category.get("skill_count") != len(route_skills):
            errors.append(f"route count mismatch: {route_path}")
        for rule in route_skills:
            routed_names.append(rule.get("name", ""))
            required = {
                "name",
                "path",
                "level",
                "kind",
                "maturity",
                "choose_when",
                "avoid_when",
                "triggers",
                "negative_triggers",
                "explicit_only",
            }
            missing = required - set(rule)
            if missing:
                errors.append(
                    f"route fields missing: {rule.get('name')} -> {sorted(missing)}"
                )

    catalog_categories = {
        item.get("category", "") for item in catalog.get("skills", [])
    }
    if indexed_categories != catalog_categories:
        errors.append(
            f"index/catalog category mismatch: "
            f"catalog_only={sorted(catalog_categories-indexed_categories)} "
            f"index_only={sorted(indexed_categories-catalog_categories)}"
        )

    duplicate_routes = sorted(
        name for name, count in Counter(routed_names).items() if count > 1
    )
    if duplicate_routes:
        errors.append(f"duplicate routed skills: {duplicate_routes}")
    if set(routed_names) != names:
        errors.append(
            f"route/catalog mismatch: catalog_only={sorted(names-set(routed_names))} "
            f"route_only={sorted(set(routed_names)-names)}"
        )

    route_files = {
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "routes").glob("*.json")
    }
    indexed_route_files = {
        category.get("route_file", "") for category in categories
    }
    if route_files != indexed_route_files:
        errors.append(
            f"stale or missing route files: "
            f"disk_only={sorted(route_files-indexed_route_files)} "
            f"index_only={sorted(indexed_route_files-route_files)}"
        )

    profile_map = index.get("profiles", {})
    for profile_name, relative_path in profile_map.items():
        profile_path = ROOT / relative_path
        if not profile_path.is_file():
            errors.append(f"missing indexed profile: {profile_name} -> {relative_path}")

if not runtime_catalog_path.is_file():
    errors.append("missing runtime catalog: runtime-catalog.json")
else:
    runtime_catalog = json.loads(runtime_catalog_path.read_text(encoding="utf-8"))
    runtime_entries = runtime_catalog.get("skills", [])
    if not isinstance(runtime_entries, list):
        errors.append("runtime catalog skills must be a list")
        runtime_entries = []
    runtime_names: list[str] = []
    for entry in runtime_entries:
        if not isinstance(entry, dict):
            errors.append("runtime catalog skill entry must be an object")
            continue
        name = entry.get("name", "")
        description = entry.get("description", "")
        location = entry.get("location", "")
        runtime_names.append(name)
        if name in runtime_names[:-1]:
            errors.append(f"duplicate runtime catalog name: {name}")
        if name not in names:
            errors.append(f"runtime catalog skill not in catalog: {name}")
            continue
        expected_location = f"skills/{name}/SKILL.md"
        if location != expected_location:
            errors.append(
                f"runtime catalog location mismatch: {name} -> {location}"
            )
        if not (ROOT / location).is_file():
            errors.append(f"missing runtime catalog location: {name} -> {location}")
        catalog_item = next(item for item in catalog["skills"] if item["name"] == name)
        if description != catalog_item.get("description"):
            errors.append(f"runtime catalog description mismatch: {name}")
    if len(runtime_entries) != len(names):
        errors.append(
            f"runtime catalog count mismatch: catalog={len(names)} runtime={len(runtime_entries)}"
        )
    if set(runtime_names) != names:
        errors.append(
            f"runtime catalog/catalog mismatch: catalog_only={sorted(names-set(runtime_names))} "
            f"runtime_only={sorted(set(runtime_names)-names)}"
        )

expected_default = [
    "clarify-requirements",
    "plan-implementation",
    "execute-plan",
    "diagnose-software",
    "review-code",
    "verify-completion",
]
profile_paths = sorted((ROOT / "profiles").glob("*.txt"))
for profile_path in profile_paths:
    profile_names = [
        line.removeprefix("skills/").strip()
        for line in profile_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    unknown = sorted(set(profile_names) - names)
    if unknown:
        errors.append(f"unknown skills in profile {profile_path.name}: {unknown}")
    if profile_path.name == "default.txt":
        if profile_names != expected_default:
            errors.append(f"unexpected default profile: {profile_names}")
        non_s_names = {
            item["name"]
            for item in catalog["skills"]
            if item.get("reference_level") != "S"
        }
        if set(profile_names) & non_s_names:
            errors.append("default profile contains non-S skills")

if index_path.is_file():
    index = json.loads(index_path.read_text(encoding="utf-8"))
    indexed_profiles = {
        (ROOT / relative_path).resolve()
        for relative_path in index.get("profiles", {}).values()
    }
    disk_profiles = {path.resolve() for path in profile_paths}
    if indexed_profiles != disk_profiles:
        errors.append(
            "index/profile mismatch: "
            f"disk_only={sorted(str(path.relative_to(ROOT.resolve())) for path in disk_profiles-indexed_profiles)} "
            f"index_only={sorted(str(path.relative_to(ROOT.resolve())) for path in indexed_profiles-disk_profiles)}"
        )

review_path = ROOT / "docs" / "SKILL_REVIEW.md"
if not review_path.is_file():
    errors.append("missing complete skill review: docs/SKILL_REVIEW.md")
else:
    review_text = review_path.read_text(encoding="utf-8")
    missing_review = sorted(name for name in names if f"`{name}`" not in review_text)
    if missing_review:
        errors.append(
            f"skills missing from implementation review: {missing_review}"
        )

zh_review_path = ROOT / "docs" / "SKILL_REVIEW.zh-CN.md"
if not zh_review_path.is_file():
    errors.append("missing Chinese skill review: docs/SKILL_REVIEW.zh-CN.md")
else:
    zh_review_text = zh_review_path.read_text(encoding="utf-8")
    missing_zh_review = sorted(
        name for name in names if f"`{name}`" not in zh_review_text
    )
    if missing_zh_review:
        errors.append(
            f"skills missing from Chinese implementation review: {missing_zh_review}"
        )

if errors:
    print("INVALID")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print(
    f"VALID skills={len(names)} levels={dict(levels)} "
    f"routes={len(routed_names)} profiles={len(profile_paths)} "
    f"upstreams={len(tracked_repositories)}"
)
