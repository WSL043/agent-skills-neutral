from __future__ import annotations

import json
import sys
from pathlib import Path

from select_skills import load_rules, route_query


ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / "tests" / "routing_cases.json").read_text(encoding="utf-8"))
errors: list[str] = []
reachable = 0

for rule in load_rules():
    for trigger in rule["triggers"]:
        result = route_query(trigger)
        if result["primary"] and result["primary"]["name"] == rule["name"]:
            reachable += 1
            break
    else:
        errors.append(f"unreachable route: {rule['name']}")

for case in CASES["positive"]:
    result = route_query(case["query"])
    actual = result["primary"]["name"] if result["primary"] else None
    if actual != case["primary"]:
        errors.append(f"positive route {case['query']!r}: {actual!r} != {case['primary']!r}")

for case in CASES["guardrails"]:
    result = route_query(case["query"])
    candidates = [item for item in [result["primary"], *result["support"], *result["alternatives"]] if item]
    names = {item["name"] for item in candidates}
    forbidden = set(case.get("forbid", [])) & names
    if forbidden:
        errors.append(f"guardrail route {case['query']!r} included {sorted(forbidden)}")
    forbidden_level = case.get("forbid_level")
    if forbidden_level and any(item["level"] == forbidden_level for item in candidates):
        errors.append(f"guardrail route {case['query']!r} included level {forbidden_level}")

if errors:
    print("ROUTING TESTS FAILED")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print(
    f"ROUTING TESTS PASSED reachable={reachable} positive={len(CASES['positive'])} "
    f"guardrails={len(CASES['guardrails'])}"
)
