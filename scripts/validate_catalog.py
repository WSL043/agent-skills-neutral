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

for item in catalog.get("skills", []):
    name = item.get("name", "")
    if name in names:
        errors.append(f"duplicate catalog name: {name}")
    names.add(name)
    if not name_pattern.fullmatch(name):
        errors.append(f"invalid name: {name}")
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
    fields = [line.split(":", 1)[0].strip() for line in frontmatter.splitlines() if ":" in line]
    if fields != ["name", "description"]:
        errors.append(f"frontmatter fields must be name,description: {name} -> {fields}")
    if f"name: {name}" not in frontmatter:
        errors.append(f"frontmatter name mismatch: {name}")
    if not body.strip() or "TODO" in text or "Insert instructions" in text:
        errors.append(f"empty or placeholder body: {name}")
    if len(text.splitlines()) >= 500:
        errors.append(f"SKILL.md is 500+ lines: {name}")
    for related in item.get("related", []):
        if related not in {entry.get("name") for entry in catalog.get("skills", [])}:
            errors.append(f"unknown related skill: {name} -> {related}")
    if item.get("has_variants_reference") and not (skill_dir / "references" / "variants.md").is_file():
        errors.append(f"missing variants reference: {name}")

disk_names = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
if disk_names != names:
    errors.append(f"catalog/disk mismatch: catalog_only={sorted(names-disk_names)} disk_only={sorted(disk_names-names)}")

levels = Counter(item.get("reference_level") for item in catalog.get("skills", []))
expected = {"S": 9, "A": 24, "B": 12}
if dict(levels) != expected:
    errors.append(f"unexpected level counts: {dict(levels)} != {expected}")

index_path = ROOT / "index.json"
routed_names: list[str] = []
if not index_path.is_file():
    errors.append("missing compact routing index: index.json")
else:
    index = json.loads(index_path.read_text(encoding="utf-8"))
    if index.get("preferred_router") != "python scripts/select_skills.py <task> --json":
        errors.append("index preferred_router is missing or unexpected")
    categories = index.get("categories", [])
    if len(categories) != 14:
        errors.append(f"unexpected route category count: {len(categories)} != 14")
    for category in categories:
        route_path = ROOT / category.get("route_file", "")
        if not route_path.is_file():
            errors.append(f"missing route file: {route_path}")
            continue
        route = json.loads(route_path.read_text(encoding="utf-8"))
        route_skills = route.get("skills", [])
        if category.get("skill_count") != len(route_skills):
            errors.append(f"route count mismatch: {route_path}")
        for rule in route_skills:
            routed_names.append(rule.get("name", ""))
            required = {
                "name", "path", "level", "kind", "maturity", "choose_when",
                "avoid_when", "triggers", "negative_triggers", "explicit_only",
            }
            missing = required - set(rule)
            if missing:
                errors.append(f"route fields missing: {rule.get('name')} -> {sorted(missing)}")
            if rule.get("level") == "B" and rule.get("maturity") == "stable":
                errors.append(f"B-level route must be conditional or experimental: {rule.get('name')}")

    duplicate_routes = sorted(name for name, count in Counter(routed_names).items() if count > 1)
    if duplicate_routes:
        errors.append(f"duplicate routed skills: {duplicate_routes}")
    if set(routed_names) != names:
        errors.append(
            f"route/catalog mismatch: catalog_only={sorted(names-set(routed_names))} "
            f"route_only={sorted(set(routed_names)-names)}"
        )
    if index_path.stat().st_size > 6000:
        errors.append(f"compact routing index exceeds 6 KB: {index_path.stat().st_size}")
    oversized_routes = [
        path.name for path in (ROOT / "routes").glob("*.json") if path.stat().st_size > 8000
    ]
    if oversized_routes:
        errors.append(f"route files exceed 8 KB: {sorted(oversized_routes)}")

expected_default = [
    "clarify-requirements",
    "plan-implementation",
    "execute-plan",
    "diagnose-software",
    "review-code",
    "verify-completion",
]
profile_paths = sorted((ROOT / "profiles").glob("*.txt"))
if len(profile_paths) != 6:
    errors.append(f"unexpected profile count: {len(profile_paths)} != 6")
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
        b_names = {item["name"] for item in catalog["skills"] if item.get("reference_level") == "B"}
        if set(profile_names) & b_names:
            errors.append("default profile contains B-level skills")

review_path = ROOT / "docs" / "SKILL_REVIEW.md"
if not review_path.is_file():
    errors.append("missing complete skill review: docs/SKILL_REVIEW.md")
else:
    review_text = review_path.read_text(encoding="utf-8")
    missing_review = sorted(name for name in names if f"`{name}`" not in review_text)
    if missing_review:
        errors.append(f"skills missing from implementation review: {missing_review}")

zh_review_path = ROOT / "docs" / "SKILL_REVIEW.zh-CN.md"
if not zh_review_path.is_file():
    errors.append("missing Chinese skill review: docs/SKILL_REVIEW.zh-CN.md")
else:
    zh_review_text = zh_review_path.read_text(encoding="utf-8")
    missing_zh_review = sorted(name for name in names if f"`{name}`" not in zh_review_text)
    if missing_zh_review:
        errors.append(f"skills missing from Chinese implementation review: {missing_zh_review}")

if errors:
    print("INVALID")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print(
    f"VALID skills={len(names)} levels={dict(levels)} "
    f"routes={len(routed_names)} profiles={len(profile_paths)}"
)
