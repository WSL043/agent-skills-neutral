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
if not provenance_path.is_file():
    errors.append("missing provenance.json")
else:
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    snapshots = provenance.get("source_snapshots", {})
    source_repositories = set(snapshots)
    provenance_skills = provenance.get("skills", {})
    if set(provenance_skills) != names:
        errors.append(
            f"provenance/catalog mismatch: catalog_only={sorted(names-set(provenance_skills))} "
            f"provenance_only={sorted(set(provenance_skills)-names)}"
        )
    for repository, commit in snapshots.items():
        if not repo_pattern.fullmatch(repository):
            errors.append(f"invalid provenance repository: {repository}")
        if not sha_pattern.fullmatch(commit or ""):
            errors.append(f"invalid provenance snapshot: {repository}@{commit}")
    for skill_name, sources in provenance_skills.items():
        if not sources:
            errors.append(f"empty provenance sources: {skill_name}")
        for source in sources:
            repository = source.get("repository")
            commit = source.get("commit")
            if snapshots.get(repository) != commit:
                errors.append(
                    f"provenance snapshot mismatch: {skill_name} -> {repository}@{commit}"
                )
            if not sha_pattern.fullmatch(commit or ""):
                errors.append(f"invalid provenance commit: {skill_name} -> {commit}")
            if commit and commit not in source.get("url", ""):
                errors.append(
                    f"unpinned provenance URL: {skill_name} -> {source.get('url')}"
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

levels = Counter(
    item.get("reference_level") for item in catalog.get("skills", [])
)

index_path = ROOT / "index.json"
routed_names: list[str] = []
indexed_categories: set[str] = set()
if not index_path.is_file():
    errors.append("missing compact routing index: index.json")
else:
    index = json.loads(index_path.read_text(encoding="utf-8"))
    if index.get("preferred_router") != "python scripts/select_skills.py <task> --json":
        errors.append("index preferred_router is missing or unexpected")

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
