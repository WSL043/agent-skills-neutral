from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "evolution_runner.py"
errors: list[str] = []


def invoke(*args: str, expected: set[int] | None = None) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        [sys.executable, str(RUNNER), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    allowed = expected or {0}
    if completed.returncode not in allowed:
        errors.append(
            f"command failed rc={completed.returncode}: {' '.join(args)}\n"
            f"stdout={completed.stdout}\nstderr={completed.stderr}"
        )
    return completed


def init_candidate(home: Path, candidate: str, contract: str, falsifier: str | None = None) -> Path:
    args = [
        "init",
        "--candidate-id", candidate,
        "--contract", contract,
        "--target-kind", "shared-kernel",
        "--owner", "AGENTS.md",
        "--condition", "the tested decision boundary is active",
        "--behavior-change", "the candidate should improve the claimed decision",
        "--evidence-signal", "acceptance evidence distinguishes baseline from candidate",
        "--transfer-scope", "test scope",
        "--operation", "replace",
        "--change-reference", "AGENTS.md",
        "--rationale", "runner regression fixture",
        "--baseline-ref", "baseline",
        "--candidate-ref", "candidate",
        "--home", str(home),
    ]
    if falsifier:
        args.extend(["--falsifier", falsifier])
    completed = invoke(*args)
    return Path(completed.stdout.strip())


with tempfile.TemporaryDirectory(prefix="agent-skills-neutral-evo-") as tmp:
    home = Path(tmp)

    optimization = init_candidate(home, "optimization-case", "optimization")
    gate = invoke("gate", "--run", str(optimization), expected={2})
    initial = json.loads(gate.stdout)
    if initial.get("decision_ready") is not False:
        errors.append("optimization gate became ready before held-out evidence")

    invoke(
        "record-execution", "--run", str(optimization),
        "--phase", "held-out", "--case-id", "held-1", "--variant", "baseline",
        "--role", "failure", "--result", "failure", "--evidence", "baseline failed",
    )
    invoke(
        "record-execution", "--run", str(optimization),
        "--phase", "held-out", "--case-id", "held-1", "--variant", "candidate",
        "--role", "success", "--result", "success", "--evidence", "candidate passed",
    )
    invoke(
        "set-holdout-integrity", "--run", str(optimization), "--status", "clean",
        "--evidence", "held-out cases were not used for proposal generation",
    )
    invoke(
        "set-model-role", "--run", str(optimization),
        "--role", "curator", "--model", "independent-curator",
    )
    ready = json.loads(invoke("gate", "--run", str(optimization)).stdout)
    if ready.get("promotion_ready") is not True:
        errors.append(f"paired optimization case did not become promotion-ready: {ready}")
    if ready.get("paired_held_out_cases") != ["held-1"]:
        errors.append(f"paired held-out detection mismatch: {ready.get('paired_held_out_cases')}")

    invoke(
        "record-execution", "--run", str(optimization),
        "--phase", "regression", "--case-id", "protected-behavior", "--variant", "candidate",
        "--role", "failure", "--result", "failure", "--evidence", "candidate regressed protected behavior",
    )
    candidate_failure = json.loads(invoke("gate", "--run", str(optimization)).stdout)
    if candidate_failure.get("promotion_ready") is not False:
        errors.append("candidate acceptance failure did not block promotion")
    if not any(
        "candidate failed or was blocked on acceptance cases" in blocker
        for blocker in candidate_failure.get("promotion_blockers", [])
    ):
        errors.append(f"candidate acceptance failure blocker missing: {candidate_failure}")

    invoke(
        "record-check", "--run", str(optimization),
        "--check", "protected-behavior", "--result", "fail", "--evidence", "regression observed",
    )
    blocked = json.loads(invoke("gate", "--run", str(optimization)).stdout)
    if blocked.get("promotion_ready") is not False:
        errors.append("failed deterministic check did not block promotion")
    retain = invoke(
        "decide", "--run", str(optimization), "--status", "retain",
        "--scope", "test scope", "--reason", "should be refused",
        expected={1},
    )
    if "promotion decision refused" not in retain.stderr:
        errors.append("runner did not explain refused retain decision")
    invoke(
        "decide", "--run", str(optimization), "--status", "narrow",
        "--scope", "narrowed test scope", "--reason", "broad claim regressed protected behavior",
        "--negative-lesson", "do not generalize beyond the surviving condition",
    )

    judgment = init_candidate(home, "judgment-case", "judgment")
    invoke("gate", "--run", str(judgment), expected={2})
    invoke(
        "set-model-role", "--run", str(judgment),
        "--role", "curator", "--model", "independent-curator",
    )
    invoke(
        "record-judgment", "--run", str(judgment), "--dimension", "quality",
        "--result", "supports", "--judge", "independent-curator",
        "--independence-note", "candidate author did not judge this case",
        "--evidence", "pairwise review",
    )
    judgment_gate = json.loads(invoke("gate", "--run", str(judgment)).stdout)
    if judgment_gate.get("decision_ready") is not True:
        errors.append("judgment contract did not become ready after semantic evidence")

    discovery = init_candidate(home, "discovery-case", "discovery", falsifier="held-out counterexample")
    invoke(
        "record-execution", "--run", str(discovery),
        "--phase", "transfer", "--case-id", "transfer-1", "--variant", "candidate",
        "--role", "counterexample", "--result", "success", "--evidence", "transfer evidence",
    )
    invoke(
        "set-holdout-integrity", "--run", str(discovery), "--status", "clean",
        "--evidence", "held-out cases were not used for proposal generation",
    )
    invoke(
        "set-model-role", "--run", str(discovery),
        "--role", "curator", "--model", "independent-curator",
    )
    invoke(
        "record-judgment", "--run", str(discovery), "--dimension", "novelty-scope",
        "--result", "supports", "--judge", "independent-curator",
        "--independence-note", "candidate author did not judge this case",
        "--evidence", "bounded claim review",
    )
    discovery_gate = json.loads(invoke("gate", "--run", str(discovery)).stdout)
    if discovery_gate.get("decision_ready") is not True:
        errors.append(f"discovery contract remained incomplete: {discovery_gate}")

    satisfaction = init_candidate(home, "satisfaction-case", "satisfaction")
    invoke(
        "set-model-role", "--run", str(satisfaction),
        "--role", "curator", "--model", "independent-curator",
    )
    check = invoke(
        "run-check", "--run", str(satisfaction), "--check", "stdlib-smoke", "--",
        sys.executable, "-c", "print('pass')",
    )
    check_payload = json.loads(check.stdout)
    if check_payload.get("result") != "pass":
        errors.append(f"run-check did not record pass: {check_payload}")
    artifacts = satisfaction / "artifacts"
    if not artifacts.is_dir() or not list(artifacts.glob("*.stdout.txt")):
        errors.append("run-check did not persist local artifacts")
    history = json.loads((satisfaction / "run.json").read_text(encoding="utf-8")).get("history", [])
    if any(
        isinstance(item, dict)
        and isinstance(item.get("detail"), dict)
        and "command" in item["detail"]
        for item in history
    ):
        errors.append("run-check history retained a complete command")
    satisfaction_gate = json.loads(invoke("gate", "--run", str(satisfaction)).stdout)
    if satisfaction_gate.get("decision_ready") is not True:
        errors.append("satisfaction contract did not accept deterministic evidence")

if errors:
    print("EVOLUTION RUNNER TESTS FAILED")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("EVOLUTION RUNNER TESTS PASSED contracts=4 promotion_gate=1 run_check=1")
