# Execution Attribution

Execution attribution records which capability artifact a real Agent session was assigned and what activation evidence is actually observable. It does not decide why an Agent failed.

The design keeps telemetry in the serving, launcher, hook, and trace plane:

```text
canonical source
      |
      v
deterministic Runtime Bundle + MANIFEST.json
      |
      v
host/session adapter ----> execution attribution receipt
                               |
session trace -----------------+
                               |
                               v
                    failure-mining attribution facts
```

No receipt field is added to `runtime/AGENTS.md`, `runtime-catalog.json`, or a Skill body. The Agent does not need to emit bookkeeping text.

## Responsibilities and dependency direction

The vendor-neutral core consists of:

- `schemas/execution-attribution.schema.json` — the stable, privacy-minimal receipt contract;
- `schemas/behavior-evidence.schema.json` — a separate receipt-bound contract required before activation can become a compliance conclusion;
- bundle identity derived from the existing `MANIFEST.json` rather than a second version registry;
- receipt integrity validation and evidence-bounded failure classification;
- explicit `unknown` states when serving or activation cannot be established.

The Codex adapter in `scripts/execution_attribution.py` owns only Codex-specific facts:

- `SessionStart` and `SessionEnd` hook input;
- `codex debug prompt-input` preflight;
- Codex JSONL `session_meta`, `turn_context`, and tool-call evidence;
- Codex JSONL `world_state.agents_md` linkage for the exact directory and instruction bytes actually assigned to the session;
- Codex runtime and model identifiers.

Evolution Runner and trajectory mining remain consumers. They may reference a receipt from `trajectory_reference` or `evidence`; they do not duplicate receipt fields inside the evolution evidence packet.

## Evidence levels

These claims are intentionally separate:

| Fact | Strongest first-version evidence | What it does not prove |
|---|---|---|
| Artifact assigned to a session | Actual Codex trace `world_state.agents_md` matches the exact bundle directory and `AGENTS.md` digest; the artifact is reverified before trace linkage | That every artifact file entered model context |
| Equivalent setup before launch | Matching, self-digested `codex debug prompt-input` preflight predates the session and contains the exact verified `AGENTS.md` bytes after newline normalization | That the later session used it; cwd and preflight alone leave serving `unknown` until actual-session evidence arrives |
| Runtime catalog available | Verified manifest and file digest | That catalog content was prompt-visible or read |
| Skill available | Skill name/location/digest in the verified manifest | That it was activated |
| Skill body delivered | A traced tool call names `skills/<name>/SKILL.md`, its model-visible output has a recognized zero-exit success envelope with no failure status, and one output text block contains the complete normalized body whose manifest digest belongs to the unchanged served bundle | That the model adopted or followed the guidance, or which filesystem object produced equivalent bytes |
| Skill body not observed | Verified served bundle plus a parse-clean trace whose final parsed record is Codex `task_complete`, with no successful full-body delivery | That a different host could not inject equivalent guidance through another surface |
| Compliance failure | Observed Skill-body delivery plus a self-digested behavior record bound to this exact receipt/session/Skill | That the Skill caused the behavior or that an unsigned local record is externally authentic |

The receipt always keeps `adoption_claim=unknown`. Full Skill content in model-visible tool output is activation evidence, not proof of semantic adoption. A definite activation or absence state is emitted only after the same receipt has verified the actual-session bundle assignment; otherwise activation remains `unknown`, even when the scanner found matching output or a complete no-read trace.

## Receipt privacy and integrity

Receipts contain UUIDs or opaque digests, bounded metadata tokens, runtime/model metadata, Skill names, and trace line references. They do not copy:

- prompts or responses;
- source code or Skill bodies;
- tool inputs or outputs;
- full traces;
- absolute local paths.

The trace pointer and unsafe host identifiers are opaque digests. Cwd and bundle locations are stored as normalized path digests. Source/runtime metadata keeps only a narrow plain-token alphabet; relative markers, colon-bearing URI-like values, drive-relative Windows forms, separators, and other free-form values are digested rather than copied. Surface names and evidence are closed code lists, and Skill identifiers use the canonical lowercase-hyphen grammar, so those fields cannot carry paths, prompts, source text, or tool payloads. The canonical source repository is constrained to a non-relative `owner/repository` identity.

Each receipt, preflight, and behavior-evidence record has a deterministic self-digest. This detects accidental or unsynchronized edits; it is not a signature and does not defend against an actor who can rewrite both a record and its digest. Stronger authenticity would require an external trusted signer or append-only evidence store and is outside this first version.

The JSON Schema validates portable shape, privacy allowlists, trace-state requirements, and state-local constraints. Trust decisions must also run `execution_attribution.py validate`, which enforces relational invariants that portable JSON Schema cannot express, including that every observed Skill name exists in the served manifest-derived Skill map. Verified serving requires a parse-clean linked terminal trace plus the exact `world_state_assignments_match` evidence code and matching AGENTS surface; an incomplete snapshot remains unknown, and `none_observed` additionally requires complete absence evidence. Mismatch evidence codes are state-exclusive: a mismatch must name at least one concrete mismatch, while verified or unknown serving cannot retain one. The receipt stores the Skill map once as `skill_digests`; it does not duplicate a separate Skill-name list, location, or observation digest that could drift.

Raw sessions and receipts should remain under `.evolution/` or another local access-controlled evidence directory. Do not commit private trajectory data.

## Codex setup

Codex 0.146 exposes host-native lifecycle hooks. `SessionStart` includes `session_id`, `transcript_path`, `cwd`, `model`, and start source. `SessionEnd` exposes the same session linkage and lets the adapter scan the final local transcript without copying it.

First create a serving preflight for the exact bundle and Codex executable:

```bash
python scripts/execution_attribution.py codex-probe \
  --bundle /absolute/path/to/runtime \
  --codex-command /absolute/path/to/codex \
  --output /private/evidence/serving-probe.json
```

The probe invokes `codex debug prompt-input --disable hooks` with a fixed non-sensitive marker. It stores only digests, time, runtime identity, visibility booleans, and a self-digest. The expected runtime `AGENTS.md` must appear as the isolated exact Codex project-instruction block; a bundle nested below an authoring repository whose ancestor `AGENTS.md` is composed into the same block is rejected. Linkage rejects a probe created after the session starts. Probe/cwd evidence alone does not set `serving=verified`.

Configure trusted project hooks adjacent to the deployment environment, not inside the verified Runtime Bundle. The command must use absolute paths. A minimal `hooks.json` shape is:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "python /opt/agent-skills-neutral/scripts/execution_attribution.py codex-hook --bundle /srv/agent-runtime --receipt-dir /private/evidence/receipts --probe /private/evidence/serving-probe.json",
            "commandWindows": "C:\\Python\\python.exe C:\\agent-skills-neutral\\scripts\\execution_attribution.py codex-hook --bundle C:\\agent-runtime --receipt-dir C:\\private\\evidence\\receipts --probe C:\\private\\evidence\\serving-probe.json"
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python /opt/agent-skills-neutral/scripts/execution_attribution.py codex-hook --bundle /srv/agent-runtime --receipt-dir /private/evidence/receipts --probe /private/evidence/serving-probe.json",
            "commandWindows": "C:\\Python\\python.exe C:\\agent-skills-neutral\\scripts\\execution_attribution.py codex-hook --bundle C:\\agent-runtime --receipt-dir C:\\private\\evidence\\receipts --probe C:\\private\\evidence\\serving-probe.json"
          }
        ]
      }
    ]
  }
}
```

The hook writes no stdout, so it adds no developer context and changes no normal Agent response. Codex still requires the normal hook trust review; one-off controlled automation may use Codex's explicit hook-trust bypass flag.

`SessionStart` records the candidate artifact without claiming actual-session serving. Before a resume or finalization performs any fallible probe/transcript read, the hook atomically clears the prior serving/activation proof; a failed lifecycle event therefore leaves a conservative pending receipt instead of stale verified state. A repeated startup/resume replaces stale serving surfaces and clears prior activation conclusions until `SessionEnd` rescans the whole session. A same-session bundle switch is a monotonic mismatch: later startups and a trace matching only the replacement bundle cannot erase evidence that the session crossed artifact identities. Repeated or corrected finalization otherwise recomputes trace-derived states instead of retaining stale trace conclusions. A `SessionEnd` without a transcript clears prior serving/activation proof. Exactly one valid `session_meta` record, including a parseable timestamp, must be the first parsed record so the preflight must strictly predate the session; a concatenated, reordered, or multi-session JSONL cannot contribute serving or activation evidence. Every `world_state` must expose a parseable `agents_md`, and every assignment must match the same bundle; a missing assignment blocks verification while any definite changed assignment remains `mismatch` even if another record is malformed. A trace with an unsupported top-level or nested response/output block, a parse error, a dangling/duplicate/out-of-order tool call ID, or any parsed record after the first `task_complete` cannot verify serving or establish activation absence. The adapter reads one immutable byte snapshot per linkage and computes the trace digest and byte count from those exact scanned bytes, so concurrent file growth cannot detach a conclusion from its recorded snapshot.

Commands that write a probe or receipt first replace the requested output with a minimal pending marker. Hook events with a usable session identity also replace the target before rejecting an unsupported lifecycle event. If bundle, probe, or trace reading then fails, the old file cannot remain a stale verified result; successful completion atomically replaces the marker with the sealed record. The marker contains no source path, prompt, response, or error body.

If project hooks are unavailable or intentionally disabled, run the same preflight before the task and explicitly link the completed Codex JSONL trace afterward:

```bash
python scripts/execution_attribution.py codex-link \
  --session /private/codex/session.jsonl \
  --bundle /absolute/path/to/runtime \
  --probe /private/evidence/serving-probe.json \
  --output /private/evidence/receipts/<session-id>.json
```

This fallback does not claim that a hook ran. It requires a matching pre-session probe, verifies the bundle again, and checks every trace `world_state` binding. A late/changed probe, manifest, path, or assigned `AGENTS.md` produces `mismatch`. The receipt accepts activation only when one explicit model-visible output text block contains the complete expected Skill body; path text, arbitrary structured metadata, or strings assembled across fields are insufficient.

## Retrospective backfill

Create a privacy-minimal receipt from an existing Codex JSONL session:

```bash
python scripts/execution_attribution.py backfill-codex \
  --session /private/codex/session.jsonl \
  --output .evolution/attribution/legacy-session.json
```

A pre-instrumentation session can establish an opaque session identity, Codex version, model, and trace digest. Without a contemporaneous verified bundle it cannot validate Skill-body bytes or establish serving, so both remain `unknown`.

## Failure-mining interface

Validate a receipt:

```bash
python scripts/execution_attribution.py validate --receipt /private/evidence/receipts/<session-id>.json
```

Attach one failure unit to an evidence-bounded attribution state:

```bash
python scripts/execution_attribution.py classify \
  --receipt /private/evidence/receipts/<session-id>.json \
  --skill verify-completion \
  --current-bundle /absolute/path/to/current/runtime \
  --failure-domain agent
```

To emit `activated_but_not_followed` or `activated_and_followed`, add `--behavior-evidence-record /private/evidence/behavior.json`. The record must conform to `schemas/behavior-evidence.schema.json` and bind its evaluator/content digest to this receipt digest, session, and Skill. A bare caller assertion is not accepted.

The classifier can return:

- `requested_skill_artifact_absent` — the verified served artifact and supplied current reference both lack that exact Skill artifact; this is not a semantic claim that equivalent capability is absent everywhere;
- `served_skill_artifact_absent` — no current reference was supplied, so only absence of the exact artifact from the served bundle is asserted;
- `not_served` — the current reference has the Skill, but the session bundle lacked it or used a different relevant Skill digest;
- `not_activated` — the Skill was exposed and a parse-clean trace whose final parsed record is `task_complete` has no successful full-body delivery;
- `activation_observed` — full-body delivery is observed but compliance is unknown;
- `activated_but_not_followed` — activation plus a receipt-bound contradictory behavior record;
- `unknown_attribution` — serving or activation evidence is insufficient;
- separate environment, tool, and evaluator failure classes.

Classification supplies facts for root-cause analysis. Every result sets `root_cause_claimed=false`.

## Limitations

- The Codex JSONL transcript is useful evidence but is not documented as a stable hook interface. The adapter therefore parses conservatively and fails to `unknown`.
- Absence claims use an allowlist of currently observed Codex record/subtype shapes. A future unknown shape disables `not_activated` until the adapter is reviewed for that trace version.
- `debug prompt-input` is a preflight under equivalent cwd/config with hooks disabled, not a cryptographic record of the later model request. Actual serving stays unknown until `world_state` matches.
- Explicit trace linking depends on the preflight being created before execution. Records are self-digested but unsigned, so a malicious local actor able to rewrite all artifacts remains outside the trust model.
- Trace linkage without the exact bundle path may retain only session metadata; it cannot reverify Skill bodies or emit activation absence.
- `world_state` proves the actual `AGENTS.md` bytes and directory, not every on-demand file. Exact Skill-body output matching supplies the additional activation evidence for an observed Skill.
- The first version is session-level across resume. It accepts the session only when every observed assignment uses the same bundle; it does not claim per-turn bundle attribution.
- Hosts that inject Skill bodies internally need their own adapter event. The Codex trace adapter only records activation when successful model-visible tool output contains the complete expected Skill body.
- The first version has one real Codex adapter. Vendor-neutrality lives in the evidence contract and classification semantics, not in pretending all hosts expose the same events.

## Deterministic verification

```bash
python scripts/test_execution_attribution.py
```

The tests cover manifest/hash identity, stale/late preflights, tampered artifacts, malformed/partial/multi-session traces, altered receipts, closed evidence codes, schema state invariants, opaque metadata, session linkage, complete-body activation matching, false absence prevention, receipt-bound behavior evidence, relevant Skill digest drift, and environment/tool/evaluator separation.
