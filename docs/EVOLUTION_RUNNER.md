# Evolution Runner

The Evolution Runner is the deterministic spine of the capability-evolution layer. It turns a proposed behavioral change into an auditable experiment without letting the worker that produced the change silently promote itself.

It is intentionally **not** an autonomous prompt rewriter, model API client, source-ingestion agent, or semantic judge.

Its responsibilities are narrower:

- create one candidate run with an explicit behavioral claim;
- bind that run to a baseline, candidate, and rollback reference when available;
- record proposal, held-out, regression, transfer, deterministic, and semantic evidence;
- distinguish evidence coverage from evidence quality;
- refuse promotion while hard evidence blockers remain;
- require an explicit curator decision for every retained change;
- keep run artifacts local by default rather than turning raw trajectories into runtime instructions.

The runner writes `.evolution/<candidate-id>/run.json` plus an `evidence.json` packet conforming to `schemas/evolution-evidence.schema.json`. The runner state itself follows `schemas/evolution-run.schema.json`.

## Why a runner exists

A governance document can describe good evolution while still leaving every maintenance session to improvise the experiment. The runner makes the outer loop executable and repeatable.

The separation is deliberate:

```text
experience / source mechanism
          |
          v
analyst or optimizer proposes a bounded candidate
          |
          v
Evolution Runner records baseline/candidate experiment state
          |
          +--> deterministic checks
          +--> fresh executions / held-out cases
          +--> regression cases
          +--> transfer cases
          +--> independent semantic judgment when necessary
          |
          v
runner computes evidence coverage + hard blockers
          |
          v
explicit curator decision
          |
          +--> retain / narrow / specialize / merge
          +--> reject / evaluator-fix
```

The runner never changes `pending` to `retain` by itself.

When execution attribution is available, `trajectory_reference` or an evidence pointer may identify the corresponding local receipt. The Runner does not copy receipt fields into `evidence.json`: serving and activation are independent evidence-plane facts, while candidate acceptance remains governed by the existing experiment contract. See [`EXECUTION_ATTRIBUTION.md`](EXECUTION_ATTRIBUTION.md).

## Evidence contracts

The contract selects **what evidence must exist before a decision can be considered ready**. It is not a skill router and it does not define a universal score.

### Satisfaction

Use when the question is absolute:

> Does the candidate satisfy the stated task or system contract?

The runner requires actual acceptance evidence such as a deterministic check, a held-out execution, or a semantic judgment. A configuration or implementation claim without observed evidence is not enough.

### Optimization

Use when the question is comparative:

> Is the candidate better than the current baseline under the same relevant conditions?

At least one held-out `case_id` must contain both a `baseline` and `candidate` record. Hold-out integrity must be established before promotion. Regression evidence should be recorded for previously protected behavior; when none is applicable, the curator must justify that rather than the runner inventing a fake regression case.

The runner does not decide that a candidate is better merely because both variants ran. The paired evidence becomes input to deterministic graders or an independent semantic judge.

### Discovery

Use for a candidate claiming a new rule, mechanism, or finding rather than merely satisfying an existing contract.

The claim needs an explicit falsifier, held-out or transfer/counterexample evidence, and semantic adjudication. This contract intentionally makes broad novelty claims harder to promote than ordinary implementation improvements.

The runner can establish that a bounded discovery claim was tested. It cannot prove global novelty across all possible prior work.

### Judgment

Use when the material outcome cannot be reduced to a deterministic ground truth: design quality, writing quality, trade-off judgment, preference-sensitive choices, or similar semantic decisions.

An explicit semantic judgment is required. Deterministic evidence may still verify structure, constraints, rendering, or factual properties, but it does not substitute for the irreducibly judgment-based dimension.

## Two readiness states

`gate` reports two different results:

- `decision_ready` — the contract has enough evidence coverage for a curator to make a decision;
- `promotion_ready` — evidence coverage is present **and** no hard promotion blocker is currently recorded.

Examples of hard promotion blockers:

- a deterministic acceptance check failed;
- a required deterministic check is blocked;
- hold-out integrity leaked;
- a semantic judgment contradicts the promoted claim;
- the candidate change is not explicitly bounded to the claim.

A failed candidate can therefore be decision-ready for rejection while remaining impossible to retain.

## Local state

By default, candidate runs live under:

```text
.evolution/<candidate-id>/
  run.json
  evidence.json
  artifacts/
```

`run.json` stores experiment orchestration state such as contract kind, baseline/candidate/rollback references, structured baseline-vs-candidate case pairing, and an append-only event history.

`evidence.json` stores the portable evidence packet used by the repository's evolution protocol.

Command output captured by `run-check` is written under `artifacts/`. The command is executed only because the maintainer explicitly supplied it; the runner never executes discovered upstream candidate code automatically.

## Basic flow

Initialize a candidate:

```bash
python scripts/evolution_runner.py init \
  --candidate-id tool-policy-v1 \
  --contract optimization \
  --target-kind shared-kernel \
  --owner AGENTS.md \
  --condition "the agent must decide whether and when a tool is necessary" \
  --behavior-change "separate tool need, selection, composition, timing, and stop decisions" \
  --evidence-signal "held-out tasks show fewer unnecessary or mistimed calls without losing task success" \
  --transfer-scope "shared execution kernel" \
  --protected "tasks that already choose the correct direct tool remain correct" \
  --operation replace \
  --change-reference AGENTS.md \
  --rationale "test the strengthened tool-decision policy" \
  --baseline-ref <baseline-ref> \
  --candidate-ref <candidate-ref>
```

Record paired held-out executions:

```bash
python scripts/evolution_runner.py record-execution \
  --run .evolution/tool-policy-v1 \
  --phase held-out \
  --case-id hidden-task-1 \
  --variant baseline \
  --role failure \
  --result failure \
  --evidence <reference>

python scripts/evolution_runner.py record-execution \
  --run .evolution/tool-policy-v1 \
  --phase held-out \
  --case-id hidden-task-1 \
  --variant candidate \
  --role success \
  --result success \
  --evidence <reference>
```

Establish hold-out separation:

```bash
python scripts/evolution_runner.py set-holdout-integrity \
  --run .evolution/tool-policy-v1 \
  --status clean
```

Run an explicit deterministic check and preserve its stdout/stderr locally:

```bash
python scripts/evolution_runner.py run-check \
  --run .evolution/tool-policy-v1 \
  --check repository-regressions \
  -- python scripts/test_routing.py
```

Record a semantic judgment when the contract requires one:

```bash
python scripts/evolution_runner.py record-judgment \
  --run .evolution/tool-policy-v1 \
  --dimension transfer-quality \
  --result supports \
  --judge <model-or-human-runtime> \
  --independence-note "judge did not author the candidate" \
  --evidence <reference>
```

Inspect the gate:

```bash
python scripts/evolution_runner.py gate --run .evolution/tool-policy-v1
```

A retained decision must be explicit:

```bash
python scripts/evolution_runner.py decide \
  --run .evolution/tool-policy-v1 \
  --status retain \
  --scope "shared execution kernel" \
  --reason "held-out evidence supports the claim and protected behavior did not regress"
```

The runner refuses retain or merge while promotion blockers remain. Narrow or specialize require decision-ready evidence and an explicit reduced scope. `reject` and `evaluator-fix` remain available because a decisive failure should be recordable without pretending the candidate was promotable.

## Model roles

Model/runtime identity is experimental metadata rather than authority.

The evidence packet can record:

- `worker` — executes mechanical tasks or agent trials;
- `analyst` — extracts local lessons or proposes candidate hypotheses;
- `curator` — makes high-impact abstraction and promotion decisions;
- `judge` — evaluates irreducibly semantic evidence.

Record them with:

```bash
python scripts/evolution_runner.py set-model-role \
  --run <run-dir> \
  --role curator \
  --model <runtime-description>
```

A stronger model may be appropriate for curator/judge roles, but model size does not override missing evidence or a failing deterministic gate.

## Exploration and local mutation

The runner deliberately does not generate candidates. Candidate generation is a separate replaceable layer.

Two future-compatible proposal lanes can feed the same runner:

- **local mutation** — a bounded add/delete/replace/move against current behavior;
- **exploration** — a materially different strategy, decomposition, retrieval policy, tool policy, or architecture hypothesis.

Both must enter the same acceptance pipeline. Exploration does not gain permission to bypass held-out evidence, regressions, trust boundaries, or rollback simply because it is more novel.

## Rollback

`rollback_ref` records the state to return to if a retained shared change later proves harmful. v0 records this reference but does not execute repository rollback automatically.

Automatic mutation and automatic rollback should only be added after the repository has evidence that the runner can identify the correct state boundary across the supported runtimes. A recorded rollback target is safer than an incorrect automatic revert.

## What v0 intentionally does not do

- call a model provider directly;
- invent a candidate;
- decide a semantic score;
- auto-promote a candidate;
- execute untrusted discovered source code;
- install candidate dependencies;
- create Git branches or worktrees;
- infer that missing evidence is a pass;
- manufacture numeric thresholds, retry counts, or evaluation budgets;
- claim that one held-out benchmark establishes universal capability lift.

Those omissions are deliberate boundaries, not unfinished convenience features.

## Success criterion

The Runner is useful when different optimizers, models, runtimes, and human maintainers can all propose changes through the same outer experimental contract, while the repository retains only changes whose evidence survives that contract.
