from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LEVEL_ORDER = {"S": 0, "A": 1, "B": 2}
ALIASES = {
    "debug": {"diagnose", "bug", "failure"},
    "diagnose": {"debug", "bug", "failure"},
    "flaky": {"intermittent", "failure"},
    "powerpoint": {"pptx", "slides", "presentation"},
    "ppt": {"pptx", "slides", "presentation"},
    "word": {"docx", "document"},
    "excel": {"xlsx", "spreadsheet", "workbook"},
    "browser": {"web", "ui", "playwright"},
    "architecture": {"codebase", "design", "modules"},
    "security": {"secure", "threat", "vulnerability"},
    "review": {"inspect", "audit"},
}

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.casefold()).strip()


def tokens(value: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9][a-z0-9.+#-]*|[\u3400-\u9fff]+", normalize(value))
        if len(token) > 1
    }


def expanded_tokens(value: str) -> set[str]:
    result = tokens(value)
    for token in tuple(result):
        result.update(ALIASES.get(token, set()))
    return result


def load_rules(root: Path = ROOT) -> list[dict[str, Any]]:
    rules: list[dict[str, Any]] = []
    index = json.loads((root / "index.json").read_text(encoding="utf-8"))
    for category in index["categories"]:
        route = json.loads((root / category["route_file"]).read_text(encoding="utf-8"))
        for item in route["skills"]:
            rules.append(dict(item, category=route["category"]))
    return rules


def score_rule(query: str, rule: dict[str, Any]) -> dict[str, Any] | None:
    normalized_query = normalize(query)
    query_tokens = expanded_tokens(query)
    name_phrase = rule["name"].replace("-", " ")
    score = 0.0
    reasons: list[str] = []
    explicit_hits = 0

    if name_phrase in normalized_query or rule["name"] in normalized_query:
        score += 24
        explicit_hits += 1
        reasons.append(f"name:{rule['name']}")

    for phrase in rule["triggers"]:
        normalized_phrase = normalize(phrase)
        if normalized_phrase and normalized_phrase in normalized_query:
            score += 12 + min(4, len(normalized_phrase.split()))
            explicit_hits += 1
            reasons.append(f"trigger:{phrase}")

    for phrase in rule["negative_triggers"]:
        normalized_phrase = normalize(phrase)
        if normalized_phrase and normalized_phrase in normalized_query:
            score -= 24
            reasons.append(f"negative:{phrase}")

    route_text = " ".join(
        [rule["name"], rule["category"], rule["choose_when"], *rule["triggers"]]
    )
    overlap = query_tokens & expanded_tokens(route_text)
    score += 1.5 * len(overlap)
    if overlap:
        reasons.append("terms:" + ",".join(sorted(overlap)))

    if rule["maturity"] in {"conditional", "experimental"} and explicit_hits == 0:
        return None
    if rule.get("explicit_only") and explicit_hits == 0:
        return None
    if score < 3:
        return None

    return {
        "name": rule["name"],
        "path": rule["path"],
        "category": rule["category"],
        "level": rule["level"],
        "kind": rule["kind"],
        "maturity": rule["maturity"],
        "score": round(score, 1),
        "matched": reasons,
        "choose_when": rule["choose_when"],
        "avoid_when": rule["avoid_when"],
        "explicit": explicit_hits > 0,
    }


def route_query(query: str, root: Path = ROOT, alternative_limit: int = 3) -> dict[str, Any]:
    candidates = [result for rule in load_rules(root) if (result := score_rule(query, rule))]
    candidates.sort(key=lambda item: (-item["score"], LEVEL_ORDER[item["level"]], item["name"]))

    primary_pool = [
        item for item in candidates if item["kind"] != "support" or item["explicit"]
    ]
    primary = primary_pool[0] if primary_pool else (candidates[0] if candidates else None)

    supports = [
        item
        for item in candidates
        if item["kind"] == "support" and item is not primary and item["score"] >= 4
    ][:1]
    excluded_names = {item["name"] for item in supports}
    if primary:
        excluded_names.add(primary["name"])
    alternatives = [item for item in candidates if item["name"] not in excluded_names][
        : max(0, alternative_limit)
    ]

    warnings: list[str] = []
    if primary and primary["level"] == "B":
        warnings.append("Primary route is B-level and must remain explicit/on-demand.")
    if primary and primary["maturity"] == "experimental":
        warnings.append("Primary route is experimental; treat it as a checklist, not a bundled implementation.")
    if not primary:
        warnings.append("No confident route. Inspect index.json and one likely category route file; do not load every skill.")

    return {
        "query": query,
        "primary": primary,
        "support": supports,
        "alternatives": alternatives,
        "warnings": warnings,
    }


def print_text(result: dict[str, Any]) -> None:
    primary = result["primary"]
    if primary:
        print(f"PRIMARY  [{primary['level']}] {primary['name']}  score={primary['score']}")
        print(f"         {primary['path']}")
        print(f"         matched: {'; '.join(primary['matched'])}")
    else:
        print("PRIMARY  none")

    for item in result["support"]:
        print(f"SUPPORT  [{item['level']}] {item['name']}  score={item['score']}")
        print(f"         {item['path']}")
    for item in result["alternatives"]:
        print(f"ALT      [{item['level']}] {item['name']}  score={item['score']}")
    for warning in result["warnings"]:
        print(f"WARNING  {warning}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Route a task to the smallest matching Agent Skill set")
    parser.add_argument("query", help="Natural-language task or capability query (English or Chinese)")
    parser.add_argument("--alternatives", type=int, default=3)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    result = route_query(args.query, alternative_limit=args.alternatives)
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_text(result)


if __name__ == "__main__":
    main()
