from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LEVEL_ORDER = {"S": 0, "A": 1}
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
    "openapi": {"api", "contract", "schema"},
    "observability": {"logs", "metrics", "traces", "telemetry"},
    "migration": {"backfill", "cutover", "compatibility"},
    "handoff": {"context", "resume", "transfer"},
}

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.casefold()).strip()


def tokens(value: str) -> set[str]:
    return {
        token
        for token in re.findall(
            r"[a-z0-9][a-z0-9.+#-]*|[\u3400-\u9fff]+", normalize(value)
        )
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
        route = json.loads(
            (root / category["route_file"]).read_text(encoding="utf-8")
        )
        for item in route["skills"]:
            rules.append(dict(item, category=route["category"]))
    return rules


def match_rule(query: str, rule: dict[str, Any]) -> dict[str, Any] | None:
    normalized_query = normalize(query)
    query_tokens = expanded_tokens(query)

    for phrase in rule["negative_triggers"]:
        normalized_phrase = normalize(phrase)
        if normalized_phrase and normalized_phrase in normalized_query:
            return None

    name_phrase = rule["name"].replace("-", " ")
    name_hit = name_phrase in normalized_query or rule["name"] in normalized_query

    trigger_hits = [
        phrase
        for phrase in rule["triggers"]
        if normalize(phrase) and normalize(phrase) in normalized_query
    ]

    route_text = " ".join(
        [rule["name"], rule["category"], rule["choose_when"], *rule["triggers"]]
    )
    overlap = sorted(query_tokens & expanded_tokens(route_text))
    explicit = name_hit or bool(trigger_hits)

    if rule["maturity"] in {"conditional", "experimental"} and not explicit:
        return None
    if rule.get("explicit_only") and not explicit:
        return None
    if not explicit and not overlap:
        return None

    if name_hit:
        match_class = "name"
        class_order = 0
    elif trigger_hits:
        match_class = "trigger"
        class_order = 1
    else:
        match_class = "terms"
        class_order = 2

    # Ranking evidence is derived only from the text that actually matched:
    # explicit name > explicit trigger > shared terms. Within the same class,
    # more matched triggers/terms and a more specific trigger phrase provide
    # stronger evidence. Project S/A priority and the skill name are stable
    # tie-breakers rather than invented numeric weights.
    longest_trigger_terms = max(
        (len(tokens(phrase)) for phrase in trigger_hits),
        default=0,
    )
    sort_key = (
        class_order,
        -len(trigger_hits),
        -longest_trigger_terms,
        -len(overlap),
        LEVEL_ORDER[rule["level"]],
        rule["name"],
    )

    return {
        "name": rule["name"],
        "path": rule["path"],
        "category": rule["category"],
        "level": rule["level"],
        "kind": rule["kind"],
        "maturity": rule["maturity"],
        "match_class": match_class,
        "matched": {
            "name": name_hit,
            "triggers": trigger_hits,
            "terms": overlap,
        },
        "choose_when": rule["choose_when"],
        "avoid_when": rule["avoid_when"],
        "explicit": explicit,
        "_sort_key": sort_key,
    }


def public_result(item: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in item.items() if key != "_sort_key"}


def route_query(
    query: str,
    root: Path = ROOT,
    alternative_limit: int | None = None,
) -> dict[str, Any]:
    candidates = [
        result
        for rule in load_rules(root)
        if (result := match_rule(query, rule))
    ]
    candidates.sort(key=lambda item: item["_sort_key"])

    primary_pool = [
        item
        for item in candidates
        if item["kind"] != "support" or item["explicit"]
    ]
    primary = (
        primary_pool[0]
        if primary_pool
        else (candidates[0] if candidates else None)
    )

    # AGENTS.md explicitly authorizes at most one support skill for a distinct
    # second phase, so this is project policy rather than an inferred cap.
    supports = [
        item
        for item in candidates
        if item["kind"] == "support" and item is not primary
    ][:1]

    excluded_names = {item["name"] for item in supports}
    if primary:
        excluded_names.add(primary["name"])
    alternatives = [
        item for item in candidates if item["name"] not in excluded_names
    ]
    if alternative_limit is not None:
        alternatives = alternatives[: max(0, alternative_limit)]

    warnings: list[str] = []
    if not primary:
        warnings.append(
            "No confident route. Inspect index.json and one likely category route file; "
            "do not load every skill."
        )

    return {
        "query": query,
        "primary": public_result(primary) if primary else None,
        "support": [public_result(item) for item in supports],
        "alternatives": [public_result(item) for item in alternatives],
        "warnings": warnings,
    }


def print_text(result: dict[str, Any]) -> None:
    primary = result["primary"]
    if primary:
        print(
            f"PRIMARY  [{primary['level']}] {primary['name']}  "
            f"match={primary['match_class']}"
        )
        print(f"         {primary['path']}")
        matched = primary["matched"]
        evidence: list[str] = []
        if matched["name"]:
            evidence.append("name")
        if matched["triggers"]:
            evidence.append("triggers=" + ",".join(matched["triggers"]))
        if matched["terms"]:
            evidence.append("terms=" + ",".join(matched["terms"]))
        print(f"         matched: {'; '.join(evidence)}")
    else:
        print("PRIMARY  none")

    for item in result["support"]:
        print(
            f"SUPPORT  [{item['level']}] {item['name']}  "
            f"match={item['match_class']}"
        )
        print(f"         {item['path']}")
    for item in result["alternatives"]:
        print(
            f"ALT      [{item['level']}] {item['name']}  "
            f"match={item['match_class']}"
        )
    for warning in result["warnings"]:
        print(f"WARNING  {warning}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Route a task to the smallest matching Agent Skill set"
    )
    parser.add_argument(
        "query",
        help="Natural-language task or capability query (English or Chinese)",
    )
    parser.add_argument(
        "--alternatives",
        type=int,
        default=None,
        help="Optional user-selected cap for displayed fallback routes.",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    result = route_query(args.query, alternative_limit=args.alternatives)
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_text(result)


if __name__ == "__main__":
    main()
