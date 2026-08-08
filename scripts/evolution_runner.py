from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HOME = ROOT / ".evolution"

CONTRACTS = ("satisfaction", "optimization", "discovery", "judgment")
PHASES = ("proposal", "held-out", "regression", "transfer")
VARIANTS = ("baseline", "candidate", "reference")
EXECUTION_ROLES = ("success", "failure", "boundary", "counterexample", "transfer")
EXECUTION_RESULTS = ("success", "partial", "failure", "blocked", "indeterminate")
CHECK_RESULTS = ("pass", "fail", "blocked", "not-applicable")
JUDGMENT_RESULTS = ("supports", "contradicts", "mixed", "indeterminate")
DECISIONS = ("pending", "retain", "narrow", "specialize", "merge", "reject", "evaluator-fix")
PROMOTION_DECISIONS = {"retain", "merge"}
TARGET_KINDS = (
    "skill",
    "shared-kernel",
    "routing",
    "memory-retrieval",
    "evaluator",
    "discovery",
    "architecture",
)
CHANGE_OPERATIONS = (
    "add",
    "delete",
    "replace",
    "move",
    "merge",
    "split",
    "new-owner",
    "architecture-change",
    "evaluator-change",
    "retrieval-change",
)


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def safe_candidate_id(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", value):
        raise ValueError("candidate id must match [A-Za-z0-9][A-Za-z0-9._-]*")
    return value


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def resolve_run_dir(value: str | Path) -> Path:
    path = Path(value).expanduser().resolve()
    if not path.is_dir():
        raise FileNotFoundError(f"run directory does not exist: {path}")
    return path


def evidence_path(run_dir: Path, state: dict[str, Any]) -> Path:
    rel = state.get("evidence_packet", "evidence.json")
    if not isinstance(rel, str) or not rel:
        raise ValueError("run state has invalid evidence_packet")
    path = (run_dir / rel).resolve()
    if run_dir not in path.parents and path != run_dir:
        raise ValueError("evidence_packet escapes the run directory")
    return path


def load_run(run_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    state = load_json(run_dir / "run.json")
    evidence = load_json(evidence_path(run_dir, state))
    if state.get("candidate_id") != evidence.get("candidate_id"):
        raise ValueError("run state and evidence packet candidate_id differ")
    return state, evidence


def save_run(run_dir: Path, state: dict[str, Any], evidence: dict[str, Any]) -> None:
    atomic_write_json(evidence_path(run_dir, state), evidence)
    atomic_write_json(run_dir / "run.json", state)


def add_history(state: dict[str, Any], event: str, detail: dict[str, Any] | None = None) -> None:
    item: dict[str, Any] = {"at": utc_now(), "event": event}
    if detail:
        item["detail"] = detail
    state.setdefault("history", []).append(item)


def make_evidence(args: argparse.Namespace) -> dict[str, Any]:
    protected = list(dict.fromkeys(args.protected or []))
    return {
        "schema_version": 1,
        "candidate_id": args.candidate_id,
        "created_at": utc_now(),
        "target": {
            "kind": args.target_kind,
            "owner": args.owner,
            "current_version": args.current_version,
        },
        "claim": {
            "condition": args.condition,
            "behavior_change": args.behavior_change,
            "evidence_signal": args.evidence_signal,
            "transfer_scope": args.transfer_scope,
            "protected_behavior": protected,
            "non_transferable_assumptions": list(dict.fromkeys(args.non_transferable or [])),
            "falsifier": args.falsifier,
        },
        "source_evidence": [],
        "proposal_evidence": [],
        "local_lessons": [],
        "candidate_change": {
            "operation": args.operation,
            "reference": args.change_reference,
            "rationale": args.rationale,
            "bounded_to_claim": not args.unbounded_change,
        },
        "acceptance_evidence": {
            "held_out": [],
            "regressions": [],
            "transfer_cases": [],
            "deterministic_checks": [],
            "semantic_judgments": [],
            "holdout_integrity": "unknown",
        },
        "decision": {
            "status": "pending",
            "scope": args.transfer_scope,
            "reason": "Awaiting acceptance evidence.",
            "negative_lesson": None,
            "reconsider_if": None,
        },
        "model_roles": {},
    }


def cmd_init(args: argparse.Namespace) -> int:
    candidate_id = safe_candidate_id(args.candidate_id)
    base = Path(args.home).expanduser().resolve() if args.home else DEFAULT_HOME
    run_dir = base / candidate_id
    if run_dir.exists():
        raise FileExistsError(f"candidate already exists: {run_dir}")
    args.candidate_id = candidate_id
    evidence = make_evidence(args)
    state: dict[str, Any] = {
        "schema_version": 1,
        "candidate_id": candidate_id,
        "contract": args.contract,
        "phase": "evaluating",
        "promotion_authority": "explicit-curator",
        "evidence_packet": "evidence.json",
        "baseline_ref": args.baseline_ref,
        "candidate_ref": args.candidate_ref,
        "rollback_ref": args.rollback_ref or args.baseline_ref,
        "experiments": [],
        "history": [],
    }
    add_history(
        state,
        "initialized",
        {
            "contract": args.contract,
            "baseline_ref": args.baseline_ref,
            "candidate_ref": args.candidate_ref,
        },
    )
    save_run(run_dir, state, evidence)
    print(run_dir)
    return 0


def evidence_bucket(evidence: dict[str, Any], phase: str) -> list[dict[str, Any]]:
    if phase == "proposal":
        return evidence.setdefault("proposal_evidence", [])
    acceptance = evidence.setdefault("acceptance_evidence", {})
    key = {
        "held-out": "held_out",
        "regression": "regressions",
        "transfer": "transfer_cases",
    }[phase]
    return acceptance.setdefault(key, [])


def cmd_record_execution(args: argparse.Namespace) -> int:
    run_dir = resolve_run_dir(args.run)
    state, evidence = load_run(run_dir)
    item = {
        "case_id": args.case_id,
        "role": args.role,
        "result": args.result,
        "trajectory_reference": args.trajectory_reference,
        "evidence": args.evidence,
        "model_runtime": args.model_runtime,
        "notes": args.notes,
    }
    evidence_bucket(evidence, args.phase).append(item)
    state.setdefault("experiments", []).append(
        {
            "recorded_at": utc_now(),
            "phase": args.phase,
            "case_id": args.case_id,
            "variant": args.variant,
            "role": args.role,
            "result": args.result,
            "evidence": args.evidence,
            "model_runtime": args.model_runtime,
        }
    )
    add_history(
        state,
        "execution-recorded",
        {"phase": args.phase, "case_id": args.case_id, "variant": args.variant, "result": args.result},
    )
    save_run(run_dir, state, evidence)
    return 0


def cmd_record_check(args: argparse.Namespace) -> int:
    run_dir = resolve_run_dir(args.run)
    state, evidence = load_run(run_dir)
    evidence.setdefault("acceptance_evidence", {}).setdefault("deterministic_checks", []).append(
        {"check": args.check, "result": args.result, "evidence": args.evidence}
    )
    add_history(state, "deterministic-check-recorded", {"check": args.check, "result": args.result})
    save_run(run_dir, state, evidence)
    return 0


def artifact_stem(check: str, index: int) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", check.strip()).strip("-") or "check"
    return f"{index:03d}-{slug}"


def cmd_run_check(args: argparse.Namespace) -> int:
    run_dir = resolve_run_dir(args.run)
    state, evidence = load_run(run_dir)
    command = list(args.command)
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        raise ValueError("run-check requires a command after --")
    cwd = Path(args.cwd).expanduser().resolve() if args.cwd else ROOT
    artifacts = run_dir / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    checks = evidence.setdefault("acceptance_evidence", {}).setdefault("deterministic_checks", [])
    stem = artifact_stem(args.check, len(checks) + 1)
    stdout_path = artifacts / f"{stem}.stdout.txt"
    stderr_path = artifacts / f"{stem}.stderr.txt"
    with stdout_path.open("w", encoding="utf-8") as stdout, stderr_path.open("w", encoding="utf-8") as stderr:
        completed = subprocess.run(command, cwd=cwd, stdout=stdout, stderr=stderr, text=True, check=False)
    result = "pass" if completed.returncode == 0 else "fail"
    evidence_ref = (
        f"exit={completed.returncode}; stdout={stdout_path.relative_to(run_dir)}; "
        f"stderr={stderr_path.relative_to(run_dir)}"
    )
    checks.append({"check": args.check, "result": result, "evidence": evidence_ref})
    add_history(
        state,
        "deterministic-check-executed",
        {"check": args.check, "result": result, "exit_code": completed.returncode},
    )
    save_run(run_dir, state, evidence)
    print(json.dumps({"check": args.check, "result": result, "exit_code": completed.returncode}))
    return 0 if completed.returncode == 0 else 1


def cmd_record_judgment(args: argparse.Namespace) -> int:
    run_dir = resolve_run_dir(args.run)
    state, evidence = load_run(run_dir)
    evidence.setdefault("acceptance_evidence", {}).setdefault("semantic_judgments", []).append(
        {
            "claim_dimension": args.dimension,
            "result": args.result,
            "judge": args.judge,
            "independence_note": args.independence_note,
            "evidence": args.evidence,
        }
    )
    add_history(
        state,
        "semantic-judgment-recorded",
        {"dimension": args.dimension, "result": args.result, "judge": args.judge},
    )
    save_run(run_dir, state, evidence)
    return 0


def cmd_set_holdout(args: argparse.Namespace) -> int:
    run_dir = resolve_run_dir(args.run)
    state, evidence = load_run(run_dir)
    evidence.setdefault("acceptance_evidence", {})["holdout_integrity"] = args.status
    detail = {"status": args.status}
    if args.evidence:
        detail["evidence"] = args.evidence
    add_history(state, "holdout-integrity-set", detail)
    save_run(run_dir, state, evidence)
    return 0


def cmd_set_model_role(args: argparse.Namespace) -> int:
    run_dir = resolve_run_dir(args.run)
    state, evidence = load_run(run_dir)
    evidence.setdefault("model_roles", {})[args.role] = args.model
    add_history(state, "model-role-set", {"role": args.role, "model": args.model})
    save_run(run_dir, state, evidence)
    return 0


def paired_optimization_cases(state: dict[str, Any]) -> list[str]:
    variants: dict[str, set[str]] = {}
    for item in state.get("experiments", []):
        if not isinstance(item, dict) or item.get("phase") != "held-out":
            continue
        case_id = item.get("case_id")
        variant = item.get("variant")
        if isinstance(case_id, str) and variant in {"baseline", "candidate"}:
            variants.setdefault(case_id, set()).add(variant)
    return sorted(case_id for case_id, seen in variants.items() if {"baseline", "candidate"} <= seen)


def gate_result(state: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    contract = state.get("contract")
    acceptance = evidence.get("acceptance_evidence", {})
    if not isinstance(acceptance, dict):
        acceptance = {}
    held_out = acceptance.get("held_out", [])
    regressions = acceptance.get("regressions", [])
    transfer_cases = acceptance.get("transfer_cases", [])
    checks = acceptance.get("deterministic_checks", [])
    judgments = acceptance.get("semantic_judgments", [])
    holdout_integrity = acceptance.get("holdout_integrity", "unknown")

    coverage_gaps: list[str] = []
    promotion_blockers: list[str] = []
    warnings: list[str] = []

    if evidence.get("candidate_change", {}).get("bounded_to_claim") is not True:
        promotion_blockers.append("candidate change is not explicitly bounded to the claim")

    model_roles = evidence.get("model_roles", {})
    if not isinstance(model_roles, dict) or not model_roles.get("curator"):
        promotion_blockers.append("no explicit curator identity/runtime is recorded")

    failed_checks = [
        item.get("check", "unnamed")
        for item in checks
        if isinstance(item, dict) and item.get("result") == "fail"
    ]
    blocked_checks = [
        item.get("check", "unnamed")
        for item in checks
        if isinstance(item, dict) and item.get("result") == "blocked"
    ]
    if failed_checks:
        promotion_blockers.append(f"deterministic checks failed: {', '.join(map(str, failed_checks))}")
    if blocked_checks:
        promotion_blockers.append(f"deterministic checks blocked: {', '.join(map(str, blocked_checks))}")

    contradictions = [
        item.get("claim_dimension", "unnamed")
        for item in judgments
        if isinstance(item, dict) and item.get("result") == "contradicts"
    ]
    if contradictions:
        promotion_blockers.append(f"semantic judgments contradict the claim: {', '.join(map(str, contradictions))}")

    if holdout_integrity == "leaked":
        promotion_blockers.append("hold-out integrity is leaked")
    elif holdout_integrity == "unknown" and contract in {"optimization", "discovery"}:
        coverage_gaps.append("hold-out integrity has not been established")

    acceptance_failures: list[str] = []
    acceptance_indeterminate: list[str] = []
    for item in state.get("experiments", []):
        if not isinstance(item, dict):
            continue
        phase = item.get("phase")
        if item.get("variant") != "candidate" or phase not in {"held-out", "regression"}:
            continue
        label = f"{phase}:{item.get('case_id', 'unnamed')}"
        result = item.get("result")
        if result in {"failure", "blocked"}:
            acceptance_failures.append(label)
        elif result == "indeterminate":
            acceptance_indeterminate.append(label)
    if acceptance_failures:
        promotion_blockers.append(
            "candidate failed or was blocked on acceptance cases: "
            + ", ".join(acceptance_failures)
        )
    if acceptance_indeterminate:
        promotion_blockers.append(
            "candidate acceptance evidence is indeterminate: "
            + ", ".join(acceptance_indeterminate)
        )

    complete_judgments = [
        item
        for item in judgments
        if isinstance(item, dict)
        and item.get("judge")
        and item.get("independence_note")
    ]

    if contract == "satisfaction":
        if not held_out and not checks and not judgments:
            coverage_gaps.append("no acceptance evidence recorded")
    elif contract == "optimization":
        pairs = paired_optimization_cases(state)
        if not pairs:
            coverage_gaps.append("no held-out case has both baseline and candidate evidence")
        if not regressions:
            warnings.append("no regression case is recorded; curator must justify whether none is applicable")
    elif contract == "discovery":
        claim = evidence.get("claim", {})
        if not isinstance(claim, dict) or not claim.get("falsifier"):
            coverage_gaps.append("discovery contract requires an explicit falsifier")
        if not held_out and not transfer_cases:
            coverage_gaps.append("discovery contract requires held-out or transfer/counterexample evidence")
        if not complete_judgments:
            coverage_gaps.append(
                "discovery contract requires semantic adjudication with judge identity and independence note"
            )
    elif contract == "judgment":
        if not complete_judgments:
            coverage_gaps.append(
                "judgment contract requires semantic adjudication with judge identity and independence note"
            )
    else:
        coverage_gaps.append(f"unknown contract: {contract!r}")

    if any(
        isinstance(item, dict) and item.get("result") in {"mixed", "indeterminate"}
        for item in judgments
    ):
        warnings.append("semantic judgment contains mixed or indeterminate evidence")

    decision_ready = not coverage_gaps
    promotion_ready = decision_ready and not promotion_blockers
    return {
        "candidate_id": state.get("candidate_id"),
        "contract": contract,
        "decision_ready": decision_ready,
        "promotion_ready": promotion_ready,
        "coverage_gaps": coverage_gaps,
        "promotion_blockers": promotion_blockers,
        "warnings": warnings,
        "paired_held_out_cases": paired_optimization_cases(state) if contract == "optimization" else [],
        "holdout_integrity": holdout_integrity,
    }


def cmd_gate(args: argparse.Namespace) -> int:
    run_dir = resolve_run_dir(args.run)
    state, evidence = load_run(run_dir)
    result = gate_result(state, evidence)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["decision_ready"] else 2


def cmd_decide(args: argparse.Namespace) -> int:
    run_dir = resolve_run_dir(args.run)
    state, evidence = load_run(run_dir)
    gate = gate_result(state, evidence)
    if args.status in PROMOTION_DECISIONS and not gate["promotion_ready"]:
        raise RuntimeError(
            "promotion decision refused; resolve gate blockers first: "
            + "; ".join([*gate["coverage_gaps"], *gate["promotion_blockers"]])
        )
    if args.status in {"narrow", "specialize"} and not gate["decision_ready"]:
        raise RuntimeError(
            "scope-reduction decision refused; complete the evidence contract first: "
            + "; ".join(gate["coverage_gaps"])
        )
    evidence["decision"] = {
        "status": args.status,
        "scope": args.scope,
        "reason": args.reason,
        "negative_lesson": args.negative_lesson,
        "reconsider_if": args.reconsider_if,
    }
    state["phase"] = "closed" if args.status != "pending" else "evaluating"
    add_history(state, "decision-recorded", {"status": args.status, "scope": args.scope})
    save_run(run_dir, state, evidence)
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    run_dir = resolve_run_dir(args.run)
    state, evidence = load_run(run_dir)
    gate = gate_result(state, evidence)
    payload = {
        "candidate_id": state.get("candidate_id"),
        "contract": state.get("contract"),
        "phase": state.get("phase"),
        "promotion_authority": state.get("promotion_authority"),
        "baseline_ref": state.get("baseline_ref"),
        "candidate_ref": state.get("candidate_ref"),
        "rollback_ref": state.get("rollback_ref"),
        "decision": evidence.get("decision"),
        "evidence_counts": {
            "proposal": len(evidence.get("proposal_evidence", [])),
            "held_out": len(evidence.get("acceptance_evidence", {}).get("held_out", [])),
            "regressions": len(evidence.get("acceptance_evidence", {}).get("regressions", [])),
            "transfer": len(evidence.get("acceptance_evidence", {}).get("transfer_cases", [])),
            "checks": len(evidence.get("acceptance_evidence", {}).get("deterministic_checks", [])),
            "judgments": len(evidence.get("acceptance_evidence", {}).get("semantic_judgments", [])),
        },
        "gate": gate,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Deterministic evolution state machine. It records candidate evidence and "
            "enforces evidence coverage; it never generates or promotes a candidate by itself."
        )
    )
    sub = parser.add_subparsers(dest="command_name", required=True)

    init = sub.add_parser("init", help="Initialize one candidate experiment.")
    init.add_argument("--candidate-id", required=True)
    init.add_argument("--contract", choices=CONTRACTS, required=True)
    init.add_argument("--target-kind", choices=TARGET_KINDS, required=True)
    init.add_argument("--owner", required=True)
    init.add_argument("--current-version")
    init.add_argument("--condition", required=True)
    init.add_argument("--behavior-change", required=True)
    init.add_argument("--evidence-signal", required=True)
    init.add_argument("--transfer-scope", required=True)
    init.add_argument("--protected", action="append", default=[])
    init.add_argument("--non-transferable", action="append", default=[])
    init.add_argument("--falsifier")
    init.add_argument("--operation", choices=CHANGE_OPERATIONS, required=True)
    init.add_argument("--change-reference", required=True)
    init.add_argument("--rationale", required=True)
    init.add_argument("--unbounded-change", action="store_true")
    init.add_argument("--baseline-ref")
    init.add_argument("--candidate-ref")
    init.add_argument("--rollback-ref")
    init.add_argument("--home")
    init.set_defaults(func=cmd_init)

    record = sub.add_parser("record-execution", help="Record proposal or acceptance execution evidence.")
    record.add_argument("--run", required=True)
    record.add_argument("--phase", choices=PHASES, required=True)
    record.add_argument("--case-id", required=True)
    record.add_argument("--variant", choices=VARIANTS, required=True)
    record.add_argument("--role", choices=EXECUTION_ROLES, required=True)
    record.add_argument("--result", choices=EXECUTION_RESULTS, required=True)
    record.add_argument("--trajectory-reference")
    record.add_argument("--evidence")
    record.add_argument("--model-runtime")
    record.add_argument("--notes")
    record.set_defaults(func=cmd_record_execution)

    check = sub.add_parser("record-check", help="Record an already-run deterministic check.")
    check.add_argument("--run", required=True)
    check.add_argument("--check", required=True)
    check.add_argument("--result", choices=CHECK_RESULTS, required=True)
    check.add_argument("--evidence")
    check.set_defaults(func=cmd_record_check)

    run_check = sub.add_parser("run-check", help="Execute an explicitly supplied deterministic command and record it.")
    run_check.add_argument("--run", required=True)
    run_check.add_argument("--check", required=True)
    run_check.add_argument("--cwd")
    run_check.add_argument("command", nargs=argparse.REMAINDER)
    run_check.set_defaults(func=cmd_run_check)

    judgment = sub.add_parser("record-judgment", help="Record semantic curator/judge evidence.")
    judgment.add_argument("--run", required=True)
    judgment.add_argument("--dimension", required=True)
    judgment.add_argument("--result", choices=JUDGMENT_RESULTS, required=True)
    judgment.add_argument("--judge")
    judgment.add_argument("--independence-note")
    judgment.add_argument("--evidence")
    judgment.set_defaults(func=cmd_record_judgment)

    holdout = sub.add_parser("set-holdout-integrity", help="Record hold-out separation state.")
    holdout.add_argument("--run", required=True)
    holdout.add_argument("--status", choices=("clean", "leaked", "unknown"), required=True)
    holdout.add_argument("--evidence")
    holdout.set_defaults(func=cmd_set_holdout)

    role = sub.add_parser("set-model-role", help="Record a worker/analyst/curator/judge model/runtime.")
    role.add_argument("--run", required=True)
    role.add_argument("--role", choices=("worker", "analyst", "curator", "judge"), required=True)
    role.add_argument("--model", required=True)
    role.set_defaults(func=cmd_set_model_role)

    gate = sub.add_parser("gate", help="Evaluate evidence coverage and promotion blockers.")
    gate.add_argument("--run", required=True)
    gate.set_defaults(func=cmd_gate)

    decide = sub.add_parser("decide", help="Record an explicit curator decision.")
    decide.add_argument("--run", required=True)
    decide.add_argument("--status", choices=DECISIONS, required=True)
    decide.add_argument("--scope", required=True)
    decide.add_argument("--reason", required=True)
    decide.add_argument("--negative-lesson")
    decide.add_argument("--reconsider-if")
    decide.set_defaults(func=cmd_decide)

    status = sub.add_parser("status", help="Show current candidate/evidence state.")
    status.add_argument("--run", required=True)
    status.set_defaults(func=cmd_status)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except (FileNotFoundError, FileExistsError, ValueError, RuntimeError) as exc:
        print(f"EVOLUTION RUNNER ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
