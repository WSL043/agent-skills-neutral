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

if errors:
    print("INVALID")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print(f"VALID skills={len(names)} levels={dict(levels)}")
