from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def tokens(value: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9]+", value.casefold()) if len(token) > 1}


ALIASES = {
    "debug": {"diagnose", "bug", "failure"},
    "diagnose": {"debug", "bug", "failure"},
    "flaky": {"intermittent", "nondeterministic"},
    "powerpoint": {"pptx", "slides", "presentation"},
    "word": {"docx", "document"},
    "excel": {"xlsx", "spreadsheet"},
    "browser": {"web", "ui", "playwright"},
    "architecture": {"codebase", "design"},
    "security": {"secure", "threat", "vulnerability"},
}


def expand_query(value: str) -> set[str]:
    result = tokens(value)
    for token in tuple(result):
        result.update(ALIASES.get(token, set()))
    return result


parser = argparse.ArgumentParser(description="Select likely skills from catalog.json")
parser.add_argument("query", help="Natural-language task or capability query")
parser.add_argument("--limit", type=int, default=5)
parser.add_argument("--json", action="store_true", dest="as_json")
args = parser.parse_args()

catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
query_tokens = expand_query(args.query)
ranked = []
for item in catalog["skills"]:
    name_tokens = tokens(item["name"])
    category_tokens = tokens(item["category"])
    description_tokens = tokens(item["description"])
    related_tokens = set().union(*(tokens(value) for value in item.get("related", []))) if item.get("related") else set()
    score = (
        5 * len(query_tokens & name_tokens)
        + 2 * len(query_tokens & category_tokens)
        + len(query_tokens & description_tokens)
        + 0.5 * len(query_tokens & related_tokens)
    )
    phrase = item["name"].replace("-", " ")
    if phrase in args.query.casefold():
        score += 10
    if score:
        ranked.append((score, item))

ranked.sort(key=lambda pair: (-pair[0], {"S": 0, "A": 1, "B": 2}[pair[1]["reference_level"]], pair[1]["name"]))
selected = [dict(item, score=score) for score, item in ranked[: max(args.limit, 0)]]

if args.as_json:
    print(json.dumps(selected, ensure_ascii=False, indent=2))
else:
    for item in selected:
        print(f"{item['score']:>4}  [{item['reference_level']}] {item['name']}  {item['path']}/SKILL.md")
        print(f"      {item['description']}")
