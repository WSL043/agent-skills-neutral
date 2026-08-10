from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LEVEL_ORDER = {"S": 0, "A": 1}
STOP_WORDS = frozenset(
    {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "been",
        "being",
        "by",
        "can",
        "could",
        "did",
        "do",
        "does",
        "for",
        "from",
        "had",
        "has",
        "have",
        "if",
        "in",
        "into",
        "is",
        "it",
        "its",
        "may",
        "might",
        "must",
        "no",
        "not",
        "of",
        "on",
        "or",
        "our",
        "should",
        "that",
        "the",
        "their",
        "there",
        "these",
        "they",
        "this",
        "those",
        "to",
        "was",
        "were",
        "will",
        "with",
        "without",
        "would",
        "you",
        "your",
        "task",
    }
)
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


def contains_phrase(normalized_query: str, phrase: str) -> bool:
    """Match Latin trigger phrases at token boundaries and CJK phrases by substring."""
    normalized_phrase = normalize(phrase)
    if not normalized_phrase:
        return False
    if re.fullmatch(r"[a-z0-9][a-z0-9 .+#-]*", normalized_phrase):
        return bool(
            re.search(
                rf"(?<![a-z0-9]){re.escape(normalized_phrase)}(?![a-z0-9])",
                normalized_query,
            )
        )
    return normalized_phrase in normalized_query


def tokens(value: str) -> set[str]:
    return {
        token
        for token in re.findall(
            r"[a-z0-9][a-z0-9.+#-]*|[\u3400-\u9fff]+", normalize(value)
        )
        if len(token) > 1 and token not in STOP_WORDS
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
    """Return deterministic lexical evidence for one route.

    This function deliberately remains simple and inspectable. It is used to
    test routing metadata and provide fallback suggestions; it is not intended
    to reproduce a capable model's semantic routing judgment.
    """
    normalized_query = normalize(query)
    query_tokens = expanded_tokens(query)

    for phrase in rule["negative_triggers"]:
        if contains_phrase(normalized_query, phrase):
            return None

    name_phrase = rule["name"].replace("-", " ")
    name_hit = contains_phrase(normalized_query, name_phrase) or contains_phrase(
        normalized_query, rule["name"]
    )

    trigger_hits = [
        phrase
        for phrase in rule["triggers"]
        if contains_phrase(normalized_query, phrase)
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
    # One shared term is too weak to justify loading a workflow. High-signal
    # single phrases belong in explicit trigger metadata; free-term fallback
    # requires corroborating lexical evidence.
    if not explicit and len(overlap) < 2:
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

    # Ranking evidence is derived only from text that actually matched. These
    # rules keep the fallback deterministic; they are not a claim that lexical
    # rank is semantically optimal for an agent.
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

    # AGENTS.md authorizes at most one support skill for a distinct second
    # phase. This remains useful for fallback output but does not constrain a
    # host that implements its own model-native progressive-disclosure policy.
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

    warnings: list[str] = [
        "Advisory lexical result only. A capable agent should select from skill "
        "name/description metadata semantically and may override this suggestion."
    ]
    if not primary:
        warnings.append(
            "No lexical suggestion. Model-native semantic selection may still find a "
            "useful skill; no route is also a valid result."
        )

    return {
        "query": query,
        "authority": "advisory-lexical-fallback",
        "primary": public_result(primary) if primary else None,
        "support": [public_result(item) for item in supports],
        "alternatives": [public_result(item) for item in alternatives],
        "warnings": warnings,
    }


def print_text(result: dict[str, Any]) -> None:
    primary = result["primary"]
    if primary:
        print(
            f"SUGGESTED_PRIMARY  [{primary['level']}] {primary['name']}  "
            f"match={primary['match_class']}"
        )
        print(f"                   {primary['path']}")
        matched = primary["matched"]
        evidence: list[str] = []
        if matched["name"]:
            evidence.append("name")
        if matched["triggers"]:
            evidence.append("triggers=" + ",".join(matched["triggers"]))
        if matched["terms"]:
            evidence.append("terms=" + ",".join(matched["terms"]))
        print(f"                   matched: {'; '.join(evidence)}")
    else:
        print("SUGGESTED_PRIMARY  none")

    for item in result["support"]:
        print(
            f"SUGGESTED_SUPPORT  [{item['level']}] {item['name']}  "
            f"match={item['match_class']}"
        )
        print(f"                   {item['path']}")
    for item in result["alternatives"]:
        print(
            f"ALT                [{item['level']}] {item['name']}  "
            f"match={item['match_class']}"
        )
    for warning in result["warnings"]:
        print(f"WARNING            {warning}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Advisory lexical Agent Skill router for regression tests, diagnostics, "
            "and clients without model-native semantic activation"
        )
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
