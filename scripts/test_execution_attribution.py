from __future__ import annotations

import copy
import hashlib
import json
import tempfile
from argparse import Namespace
from pathlib import Path

from build_runtime_bundle import BundleError, build_bundle
from execution_attribution import (
    AttributionError,
    MISMATCH_EVIDENCE_CODES,
    SERVING_EVIDENCE_CODES,
    SURFACE_EVIDENCE_CODES,
    SURFACE_NAMES,
    attach_trace,
    bundle_identity,
    classify_failure,
    cmd_backfill,
    cmd_codex_link,
    cmd_probe,
    handle_codex_event,
    load_receipt,
    make_backfill_receipt,
    make_codex_linked_receipt,
    path_digest,
    safe_metadata_token,
    seal_behavior_evidence,
    seal_probe,
    seal_receipt,
    validate_probe,
    validate_receipt,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "execution-attribution.schema.json"
BEHAVIOR_SCHEMA = ROOT / "schemas" / "behavior-evidence.schema.json"
errors: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def write_trace(
    path: Path,
    *,
    session_id: str,
    include_read: bool,
    bundle: Path | None = None,
    include_false_positives: bool = True,
    include_terminal: bool = True,
    include_world_state: bool = True,
) -> None:
    rows: list[dict[str, object]] = [
        {
            "type": "session_meta",
            "payload": {
                "id": session_id,
                "timestamp": "2026-08-09T00:00:00Z",
                "cwd": str(bundle) if bundle is not None else "C:/private/project",
                "cli_version": "0.146.0",
                "source": "exec",
            },
        },
        {
            "type": "turn_context",
            "payload": {"model": "test-model"},
        },
    ]
    if bundle is not None and include_world_state:
        rows.append(
            {
                "type": "world_state",
                "payload": {
                    "full": True,
                    "state": {
                        "agents_md": {
                            "directory": str(bundle),
                            "text": (bundle / "AGENTS.md").read_text(encoding="utf-8"),
                        }
                    },
                },
            }
        )
    if include_read:
        rows.extend(
            [
                {
                    "type": "response_item",
                    "payload": {
                        "type": "custom_tool_call",
                        "call_id": "call-good",
                        "name": "exec",
                        "input": (
                            "const r = await tools.shell_command({command: "
                            "\"Get-Content -Raw skills/verify-completion/SKILL.md\"});"
                        ),
                    },
                },
                {
                    "type": "response_item",
                    "payload": {
                        "type": "custom_tool_call_output",
                        "call_id": "call-good",
                        "output": [
                            {
                                "type": "input_text",
                                "text": (
                                    "Script completed\nExit code: 0\nOutput:\n"
                                    + (
                                        (
                                            bundle
                                            / "skills"
                                            / "verify-completion"
                                            / "SKILL.md"
                                        ).read_text(encoding="utf-8")
                                        if bundle is not None
                                        else "# Verify Completion"
                                    )
                                ),
                            }
                        ],
                    },
                },
            ]
        )
    if include_false_positives:
        rows.extend(
            [
                {
                    "type": "response_item",
                    "payload": {
                        "type": "custom_tool_call",
                        "call_id": "call-patch",
                        "name": "apply_patch",
                        "input": "*** Begin Patch\n*** Update File: skills/review-code/SKILL.md",
                    },
                },
                {
                    "type": "response_item",
                    "payload": {
                        "type": "custom_tool_call_output",
                        "call_id": "call-patch",
                        "output": [
                            {"type": "input_text", "text": "Script completed\nExit code: 0"}
                        ],
                    },
                },
                {
                    "type": "response_item",
                    "payload": {
                        "type": "custom_tool_call",
                        "call_id": "call-failed-read",
                        "name": "exec",
                        "input": "Get-Content skills/review-code/SKILL.md",
                    },
                },
                {
                    "type": "response_item",
                    "payload": {
                        "type": "custom_tool_call_output",
                        "call_id": "call-failed-read",
                        "output": [
                            {
                                "type": "input_text",
                                "text": "Script failed\nExit code: 1\nCannot find path",
                            }
                        ],
                    },
                },
                {
                    "type": "response_item",
                    "payload": {
                        "type": "custom_tool_call",
                        "call_id": "call-other-nonzero",
                        "name": "exec",
                        "input": "Get-Content skills/build-cli/SKILL.md",
                    },
                },
                {
                    "type": "response_item",
                    "payload": {
                        "type": "custom_tool_call_output",
                        "call_id": "call-other-nonzero",
                        "output": [
                            {"type": "input_text", "text": "Exit code: 7\nOutput unavailable"}
                        ],
                    },
                },
            ]
        )
    if include_terminal:
        rows.append(
            {
                "type": "event_msg",
                "payload": {"type": "task_complete", "turn_id": "test-turn"},
            }
        )
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
required_root = {
    "schema_version",
    "record_type",
    "receipt_id",
    "recorded_at",
    "producer",
    "session",
    "runtime",
    "serving",
    "activation",
    "privacy",
    "integrity",
}
check(set(schema.get("required", [])) == required_root, "receipt schema required fields drifted")
check(
    schema.get("properties", {}).get("receipt_id", {}).get("$ref") == "#/$defs/opaqueId",
    "receipt schema accepts non-opaque receipt ids",
)
privacy_properties = schema.get("properties", {}).get("privacy", {}).get("properties", {})
check(
    privacy_properties
    and all(value.get("const") is False for value in privacy_properties.values()),
    "receipt schema privacy fields must all be false",
)
schema_defs = schema.get("$defs", {})
serving_schema = schema.get("properties", {}).get("serving", {}).get("properties", {})
surface_schema = serving_schema.get("surfaces", {}).get("items", {}).get("properties", {})
check(
    set(surface_schema.get("name", {}).get("enum", [])) == SURFACE_NAMES,
    "receipt schema surface-name privacy allowlist drifted",
)
check(
    set(schema_defs.get("surfaceEvidenceCode", {}).get("enum", []))
    == SURFACE_EVIDENCE_CODES,
    "receipt schema surface-evidence privacy allowlist drifted",
)
check(
    set(schema_defs.get("servingEvidenceCode", {}).get("enum", []))
    == SERVING_EVIDENCE_CODES,
    "receipt schema serving-evidence privacy allowlist drifted",
)
check(
    set(schema_defs.get("mismatchEvidenceCode", {}).get("enum", []))
    == MISMATCH_EVIDENCE_CODES,
    "receipt schema mismatch-evidence state contract drifted",
)
schema_conditions = json.dumps(schema.get("allOf", []), sort_keys=True)
for required_invariant in (
    "observed_prompt_visible",
    "complete_trace_snapshot",
    "minItems",
    "maxItems",
):
    check(
        required_invariant in schema_conditions,
        f"receipt schema omitted state invariant: {required_invariant}",
    )
bundle_schema = schema.get("$defs", {}).get("bundleIdentity", {})
check(
    "skill_names" not in bundle_schema.get("required", [])
    and "skill_names" not in bundle_schema.get("properties", {}),
    "receipt schema retained a duplicate Skill-name registry",
)
check(
    bundle_schema.get("properties", {})
    .get("skill_digests", {})
    .get("propertyNames", {})
    .get("$ref")
    == "#/$defs/skillName",
    "receipt schema does not privacy-bound Skill map keys",
)
activation_item_required = (
    schema.get("properties", {})
    .get("activation", {})
    .get("properties", {})
    .get("observed_skills", {})
    .get("items", {})
    .get("required", [])
)
check(
    "location" not in activation_item_required and "digest" not in activation_item_required,
    "receipt schema retained redundant activation identity fields",
)
check(
    safe_metadata_token("C:private-project").startswith("sha256:"),
    "Windows drive-relative metadata was copied",
)
check(
    safe_metadata_token("https://private.example/path").startswith("sha256:"),
    "URI-like metadata was copied",
)
for unsafe_token in (".", "..", "file:private", "urn:private:value"):
    check(
        safe_metadata_token(unsafe_token).startswith("sha256:"),
        f"path/URI-like metadata token was copied: {unsafe_token}",
    )
behavior_schema = json.loads(BEHAVIOR_SCHEMA.read_text(encoding="utf-8"))
check(
    behavior_schema.get("properties", {}).get("record_type", {}).get("const")
    == "behavior-evidence",
    "behavior evidence schema identity drifted",
)
check(
    behavior_schema.get("properties", {}).get("skill", {}).get("$ref")
    == "#/$defs/skillName",
    "behavior evidence schema does not privacy-bound Skill names",
)

with tempfile.TemporaryDirectory(prefix="execution-attribution-test-") as temporary:
    temp = Path(temporary)
    bundle = temp / "runtime"
    build_bundle(bundle, allow_dirty=True)
    identity = bundle_identity(bundle)
    check(identity["source_repository"] == "WSL043/agent-skills-neutral", "bundle source identity lost")
    check(identity["agents_digest"].startswith("sha256:"), "AGENTS digest missing")
    check("verify-completion" in identity["skill_digests"], "bundle skill index missing")

    probe = {
        "schema_version": 1,
        "record_type": "codex-serving-preflight",
        "probe_id": "019fe3d4-0000-7000-8000-000000000001",
        "recorded_at": "2026-08-08T23:59:59Z",
        "runtime": {
            "vendor": "openai",
            "name": "codex",
            "version": "0.146.0",
            "command_digest": "sha256:" + "1" * 64,
        },
        "bundle": {
            "manifest_digest": identity["manifest_digest"],
            "path_digest": identity["path_digest"],
            "agents_digest": identity["agents_digest"],
            "runtime_catalog_digest": identity["runtime_catalog_digest"],
        },
        "prompt_input_digest": "sha256:" + "2" * 64,
        "agents_prompt_visible": True,
        "runtime_catalog_prompt_visible": False,
        "privacy": {
            "prompt_content_stored": False,
            "response_content_stored": False,
            "source_content_stored": False,
        },
        "integrity": {"algorithm": "sha256", "record_digest": None},
    }
    seal_probe(probe)
    probe_path = temp / "probe.json"
    probe_path.write_text(json.dumps(probe), encoding="utf-8")
    receipts = temp / "receipts"
    session_id = "019fe3d6-f66e-7873-9b80-91bc17d7b3c5"
    start = {
        "session_id": session_id,
        "transcript_path": None,
        "cwd": str(bundle),
        "hook_event_name": "SessionStart",
        "model": "test-model",
        "source": "startup",
    }
    receipt_file = handle_codex_event(
        start,
        bundle_path=bundle,
        receipt_dir=receipts,
        probe_path=probe_path,
    )
    receipt = load_receipt(receipt_file)
    check(receipt["session"]["id"] == session_id, "SessionStart did not link session id")
    check(receipt["runtime"]["version"] == "0.146.0", "probe runtime version was not retained")
    check(receipt["serving"]["status"] == "unknown", "startup artifact was overclaimed as served")
    check(receipt["serving"]["evidence_strength"] == "strong", "matching preflight was not strong evidence")
    surface = {item["name"]: item for item in receipt["serving"]["surfaces"]}
    check(surface["AGENTS.md"]["status"] == "preflight_prompt_visible", "preflight boundary missing")
    check(
        surface["runtime-catalog.json"]["status"] == "available_on_demand",
        "catalog availability was confused with prompt visibility",
    )
    check(receipt["activation"]["status"] == "unknown", "start receipt guessed activation")

    trace = temp / "session.jsonl"
    write_trace(trace, session_id=session_id, include_read=True, bundle=bundle)
    end = {
        "session_id": session_id,
        "transcript_path": str(trace),
        "cwd": str(bundle),
        "hook_event_name": "SessionEnd",
        "model": "test-model",
        "reason": "other",
    }
    handle_codex_event(
        end,
        bundle_path=bundle,
        receipt_dir=receipts,
        probe_path=probe_path,
    )
    receipt = load_receipt(receipt_file)
    observed_names = [item["name"] for item in receipt["activation"]["observed_skills"]]
    check(observed_names == ["verify-completion"], "activation scanner accepted a false read")
    check(receipt["serving"]["status"] == "verified", "actual world_state did not verify serving")
    check(receipt["activation"]["status"] == "observed_skill_content", "Skill body delivery was not observed")
    check(receipt["serving"]["evidence_strength"] == "direct", "world_state did not upgrade serving evidence")
    check(receipt["activation"]["adoption_claim"] == "unknown", "file read was confused with adoption")
    check(receipt["session"]["trace"]["pointer"] == path_digest(trace), "trace pointer is not opaque")
    check(not receipt["privacy"]["absolute_paths_stored"], "privacy contract changed")
    serialized = json.dumps(receipt, ensure_ascii=False)
    for forbidden in ("C:/private/project", "# Verify Completion", "Get-Content -Raw"):
        check(forbidden not in serialized, f"receipt copied private trace content: {forbidden}")

    handle_codex_event(
        start,
        bundle_path=bundle,
        receipt_dir=receipts,
        probe_path=probe_path,
    )
    resumed_pending = load_receipt(receipt_file)
    check(resumed_pending["serving"]["status"] == "unknown", "resume retained stale serving proof")
    check(resumed_pending["activation"]["status"] == "unknown", "resume retained stale activation")
    check(
        not any(
            item["status"] == "observed_prompt_visible"
            for item in resumed_pending["serving"]["surfaces"]
        ),
        "resume retained stale actual-session surface evidence",
    )
    handle_codex_event(
        end,
        bundle_path=bundle,
        receipt_dir=receipts,
        probe_path=probe_path,
    )
    receipt = load_receipt(receipt_file)
    check(receipt["serving"]["status"] == "verified", "same-bundle resume did not reverify")

    missing_transcript_end = copy.deepcopy(end)
    missing_transcript_end["transcript_path"] = None
    handle_codex_event(
        missing_transcript_end,
        bundle_path=bundle,
        receipt_dir=receipts,
        probe_path=probe_path,
    )
    missing_transcript_receipt = load_receipt(receipt_file)
    check(
        missing_transcript_receipt["serving"]["status"] == "unknown",
        "transcript-less SessionEnd retained serving proof",
    )
    check(
        missing_transcript_receipt["activation"]["status"] == "unknown",
        "transcript-less SessionEnd retained activation",
    )
    handle_codex_event(
        end,
        bundle_path=bundle,
        receipt_dir=receipts,
        probe_path=probe_path,
    )
    receipt = load_receipt(receipt_file)
    check(receipt["serving"]["status"] == "verified", "corrected SessionEnd did not recover")

    linked = make_codex_linked_receipt(
        trace,
        bundle_path=bundle,
        probe_path=probe_path,
    )
    check(linked["serving"]["status"] == "verified", "explicit Codex trace link lost serving")
    check(linked["serving"]["evidence_strength"] == "direct", "trace world_state was not direct")
    check(
        [item["name"] for item in linked["activation"]["observed_skills"]]
        == ["verify-completion"],
        "explicit Codex trace link lost activation evidence",
    )

    failure_receipts = temp / "failure-receipts"
    failure_session = "019fe3d6-f66e-7873-9b80-91bc17d7b3d0"
    failure_start = copy.deepcopy(start)
    failure_start["session_id"] = failure_session
    failure_file = handle_codex_event(
        failure_start,
        bundle_path=bundle,
        receipt_dir=failure_receipts,
        probe_path=probe_path,
    )
    failure_trace = temp / "failure-session.jsonl"
    write_trace(
        failure_trace,
        session_id=failure_session,
        include_read=False,
        bundle=bundle,
    )
    failure_end = {
        "session_id": failure_session,
        "transcript_path": str(failure_trace),
        "cwd": str(bundle),
        "hook_event_name": "SessionEnd",
        "model": "test-model",
        "reason": "other",
    }
    handle_codex_event(
        failure_end,
        bundle_path=bundle,
        receipt_dir=failure_receipts,
        probe_path=probe_path,
    )
    check(
        load_receipt(failure_file)["serving"]["status"] == "verified",
        "failed-event fixture did not reach verified state",
    )
    try:
        handle_codex_event(
            failure_start,
            bundle_path=bundle,
            receipt_dir=failure_receipts,
            probe_path=temp / "missing-probe.json",
        )
    except (AttributionError, BundleError, OSError):
        pass
    else:
        errors.append("missing resume probe unexpectedly succeeded")
    failed_resume_receipt = load_receipt(failure_file)
    check(
        failed_resume_receipt["serving"]["status"] == "unknown"
        and failed_resume_receipt["activation"]["status"] == "unknown",
        "failed resume probe retained stale verified receipt",
    )
    handle_codex_event(
        failure_start,
        bundle_path=bundle,
        receipt_dir=failure_receipts,
        probe_path=probe_path,
    )
    handle_codex_event(
        failure_end,
        bundle_path=bundle,
        receipt_dir=failure_receipts,
        probe_path=probe_path,
    )
    missing_file_end = copy.deepcopy(failure_end)
    missing_file_end["transcript_path"] = str(temp / "missing-transcript.jsonl")
    try:
        handle_codex_event(
            missing_file_end,
            bundle_path=bundle,
            receipt_dir=failure_receipts,
            probe_path=probe_path,
        )
    except AttributionError:
        pass
    else:
        errors.append("missing SessionEnd transcript unexpectedly succeeded")
    failed_end_receipt = load_receipt(failure_file)
    check(
        failed_end_receipt["serving"]["status"] == "unknown"
        and failed_end_receipt["activation"]["status"] == "unknown",
        "failed SessionEnd linkage retained stale verified receipt",
    )

    no_world_state_trace = temp / "no-world-state.jsonl"
    write_trace(
        no_world_state_trace,
        session_id=session_id,
        include_read=True,
        bundle=bundle,
        include_world_state=False,
    )
    no_world_state_link = make_codex_linked_receipt(
        no_world_state_trace,
        bundle_path=bundle,
        probe_path=probe_path,
    )
    check(
        no_world_state_link["serving"]["status"] == "unknown",
        "preflight/cwd alone was overclaimed as actual-session serving",
    )
    check(
        no_world_state_link["activation"]["status"] == "unknown",
        "activation was asserted without actual-session serving assignment",
    )
    stale_rescan = copy.deepcopy(receipt)
    attach_trace(
        stale_rescan,
        no_world_state_trace,
        bundle_path=bundle,
        complete=True,
    )
    check(stale_rescan["serving"]["status"] == "unknown", "rescan retained stale serving")
    check(
        not any(
            item["status"] == "observed_prompt_visible"
            for item in stale_rescan["serving"]["surfaces"]
        ),
        "rescan retained stale actual-session surface",
    )

    stale_probe = copy.deepcopy(probe)
    stale_probe["bundle"]["manifest_digest"] = "sha256:" + "0" * 64
    seal_probe(stale_probe)
    stale_probe_path = temp / "stale-probe.json"
    stale_probe_path.write_text(json.dumps(stale_probe), encoding="utf-8")
    stale_link = make_codex_linked_receipt(
        trace,
        bundle_path=bundle,
        probe_path=stale_probe_path,
    )
    check(stale_link["serving"]["status"] == "mismatch", "stale preflight was accepted")

    late_probe = copy.deepcopy(probe)
    late_probe["recorded_at"] = "2026-08-09T00:00:01Z"
    seal_probe(late_probe)
    late_probe_path = temp / "late-probe.json"
    late_probe_path.write_text(json.dumps(late_probe), encoding="utf-8")
    late_link = make_codex_linked_receipt(
        trace,
        bundle_path=bundle,
        probe_path=late_probe_path,
    )
    check(late_link["serving"]["status"] == "mismatch", "post-session preflight was accepted")

    equal_probe = copy.deepcopy(probe)
    equal_probe["recorded_at"] = "2026-08-09T00:00:00Z"
    seal_probe(equal_probe)
    equal_probe_path = temp / "equal-time-probe.json"
    equal_probe_path.write_text(json.dumps(equal_probe), encoding="utf-8")
    equal_link = make_codex_linked_receipt(
        trace,
        bundle_path=bundle,
        probe_path=equal_probe_path,
    )
    check(
        equal_link["serving"]["status"] == "mismatch",
        "preflight did not strictly predate the session",
    )

    malformed_preflight_time = copy.deepcopy(receipt)
    malformed_preflight_time["serving"]["preflight"]["recorded_at"] = "not-a-timestamp"
    seal_receipt(malformed_preflight_time)
    try:
        validate_receipt(malformed_preflight_time)
    except AttributionError:
        pass
    else:
        errors.append("malformed preflight timestamp was accepted")

    postdated_preflight = copy.deepcopy(receipt)
    postdated_preflight["serving"]["preflight"]["recorded_at"] = "9999-01-01T00:00:00Z"
    seal_receipt(postdated_preflight)
    try:
        validate_receipt(postdated_preflight)
    except AttributionError:
        pass
    else:
        errors.append("preflight timestamp after receipt was accepted")

    missing_observed_scope = copy.deepcopy(receipt)
    missing_observed_scope["activation"]["evidence_scope"] = "none"
    seal_receipt(missing_observed_scope)
    try:
        validate_receipt(missing_observed_scope)
    except AttributionError:
        pass
    else:
        errors.append("observed activation without trace evidence scope was accepted")

    observed = classify_failure(
        receipt,
        skill="verify-completion",
        current_bundle=identity,
        failure_domain="agent",
        behavior_evidence=None,
    )
    check(observed["classification"] == "activation_observed", "observed activation classification failed")
    behavior_record = {
        "schema_version": 1,
        "record_type": "behavior-evidence",
        "session_id": receipt["session"]["id"],
        "skill": "verify-completion",
        "assessment": "contradicted",
        "evaluator": {"kind": "deterministic", "id_digest": "sha256:" + "3" * 64},
        "evidence": {
            "attribution_receipt_digest": receipt["integrity"]["receipt_digest"],
            "content_digest": "sha256:" + "4" * 64,
            "recorded_at": receipt["recorded_at"],
        },
        "integrity": {"algorithm": "sha256", "record_digest": None},
    }
    seal_behavior_evidence(behavior_record)
    contradicted = classify_failure(
        receipt,
        skill="verify-completion",
        current_bundle=identity,
        failure_domain="agent",
        behavior_evidence=behavior_record,
    )
    check(
        contradicted["classification"] == "activated_but_not_followed",
        "separate contradiction evidence did not produce compliance classification",
    )
    wrong_behavior_record = copy.deepcopy(behavior_record)
    wrong_behavior_record["evidence"]["attribution_receipt_digest"] = "sha256:" + "5" * 64
    seal_behavior_evidence(wrong_behavior_record)
    try:
        classify_failure(
            receipt,
            skill="verify-completion",
            current_bundle=identity,
            failure_domain="agent",
            behavior_evidence=wrong_behavior_record,
        )
    except AttributionError:
        pass
    else:
        errors.append("behavior evidence bound to another receipt was accepted")
    future_behavior_record = copy.deepcopy(behavior_record)
    future_behavior_record["evidence"]["recorded_at"] = "9999-01-01T00:00:00Z"
    seal_behavior_evidence(future_behavior_record)
    try:
        classify_failure(
            receipt,
            skill="verify-completion",
            current_bundle=identity,
            failure_domain="agent",
            behavior_evidence=future_behavior_record,
        )
    except AttributionError:
        pass
    else:
        errors.append("future behavior evidence timestamp was accepted")
    environment = classify_failure(
        receipt,
        skill="verify-completion",
        current_bundle=identity,
        failure_domain="environment",
        behavior_evidence=None,
    )
    check(environment["classification"] == "environment_failure", "environment failure was conflated")

    no_read_trace = temp / "no-read.jsonl"
    write_trace(no_read_trace, session_id=session_id, include_read=False, bundle=bundle)
    no_read_receipt = copy.deepcopy(receipt)
    attach_trace(no_read_receipt, no_read_trace, bundle_path=bundle, complete=True)
    not_activated = classify_failure(
        no_read_receipt,
        skill="verify-completion",
        current_bundle=identity,
        failure_domain="agent",
        behavior_evidence=None,
    )
    check(
        not_activated["classification"] == "not_activated",
        f"complete no-read trace was not classified: {not_activated}",
    )

    missing_bundle_path_receipt = copy.deepcopy(receipt)
    attach_trace(
        missing_bundle_path_receipt,
        no_read_trace,
        bundle_path=None,
        complete=True,
    )
    check(
        missing_bundle_path_receipt["activation"]["status"] == "unknown",
        "missing bundle path produced activation absence",
    )
    missing_bundle_path_result = classify_failure(
        missing_bundle_path_receipt,
        skill="verify-completion",
        current_bundle=identity,
        failure_domain="agent",
        behavior_evidence=None,
    )
    check(
        missing_bundle_path_result["classification"] == "unknown_attribution",
        "missing bundle path produced not_activated",
    )

    recovered_mismatch_receipt = copy.deepcopy(receipt)
    recovered_mismatch_receipt["serving"]["status"] = "mismatch"
    recovered_mismatch_receipt["serving"]["evidence"].append(
        "world_state_assignment_mismatch"
    )
    seal_receipt(recovered_mismatch_receipt)
    attach_trace(
        recovered_mismatch_receipt,
        trace,
        bundle_path=bundle,
        complete=True,
    )
    check(
        recovered_mismatch_receipt["serving"]["status"] == "verified",
        "corrected trace could not replace stale mismatch",
    )

    partial_trace = temp / "partial-no-read.jsonl"
    write_trace(
        partial_trace,
        session_id=session_id,
        include_read=False,
        bundle=bundle,
        include_terminal=False,
    )
    partial_receipt = copy.deepcopy(receipt)
    attach_trace(partial_receipt, partial_trace, bundle_path=bundle, complete=True)
    check(partial_receipt["session"]["trace"]["status"] == "snapshot", "partial trace was linked")
    check(partial_receipt["serving"]["status"] == "unknown", "partial trace verified serving")
    check(partial_receipt["activation"]["status"] == "unknown", "partial trace invented absence")
    partial_result = classify_failure(
        partial_receipt,
        skill="verify-completion",
        current_bundle=identity,
        failure_domain="agent",
        behavior_evidence=None,
    )
    check(partial_result["classification"] == "unknown_attribution", "partial trace became not_activated")

    activity_after_terminal = temp / "activity-after-terminal.jsonl"
    write_trace(
        activity_after_terminal,
        session_id=session_id,
        include_read=False,
        bundle=bundle,
    )
    activity_after_terminal.write_text(
        activity_after_terminal.read_text(encoding="utf-8")
        + json.dumps(
            {
                "type": "response_item",
                "payload": {"type": "reasoning", "summary": []},
            }
        )
        + "\n",
        encoding="utf-8",
    )
    after_terminal_receipt = copy.deepcopy(receipt)
    attach_trace(
        after_terminal_receipt,
        activity_after_terminal,
        bundle_path=bundle,
        complete=True,
    )
    check(
        after_terminal_receipt["activation"]["status"] == "unknown",
        "activity after task_complete was ignored",
    )

    repeated_terminal_trace = temp / "repeated-terminal.jsonl"
    repeated_terminal_rows = [
        json.loads(line) for line in no_read_trace.read_text(encoding="utf-8").splitlines()
    ]
    repeated_terminal_rows.extend(
        [
            {"type": "event_msg", "payload": {"type": "token_count", "total": 1}},
            {"type": "event_msg", "payload": {"type": "task_complete"}},
        ]
    )
    repeated_terminal_trace.write_text(
        "".join(json.dumps(row) + "\n" for row in repeated_terminal_rows),
        encoding="utf-8",
    )
    repeated_terminal_receipt = copy.deepcopy(receipt)
    attach_trace(
        repeated_terminal_receipt,
        repeated_terminal_trace,
        bundle_path=bundle,
        complete=True,
    )
    check(
        repeated_terminal_receipt["activation"]["status"] == "unknown",
        "a later task_complete erased records after the first terminal",
    )
    check(
        repeated_terminal_receipt["serving"]["status"] == "unknown",
        "a repeated terminal trace verified serving",
    )

    premetadata_trace = temp / "evidence-before-session-meta.jsonl"
    premetadata_rows = [
        json.loads(line) for line in no_read_trace.read_text(encoding="utf-8").splitlines()
    ]
    premetadata_rows[0], premetadata_rows[2] = premetadata_rows[2], premetadata_rows[0]
    premetadata_trace.write_text(
        "".join(json.dumps(row) + "\n" for row in premetadata_rows),
        encoding="utf-8",
    )
    premetadata_receipt = copy.deepcopy(receipt)
    attach_trace(
        premetadata_receipt,
        premetadata_trace,
        bundle_path=bundle,
        complete=True,
    )
    check(
        premetadata_receipt["serving"]["status"] == "unknown"
        and premetadata_receipt["activation"]["status"] == "unknown",
        "evidence before session_meta was attributed to the later session",
    )

    duplicate_call_trace = temp / "duplicate-call-id.jsonl"
    duplicate_rows = [
        json.loads(line) for line in no_read_trace.read_text(encoding="utf-8").splitlines()
    ]
    duplicate_rows[-1:-1] = [
        {
            "type": "response_item",
            "payload": {
                "type": "custom_tool_call",
                "call_id": "duplicate-call",
                "name": "exec",
                "input": "Write-Output harmless",
            },
        },
        {
            "type": "response_item",
            "payload": {
                "type": "custom_tool_call_output",
                "call_id": "duplicate-call",
                "output": (
                    "Script completed\nExit code: 0\nOutput:\n"
                    + (bundle / "skills" / "verify-completion" / "SKILL.md").read_text(
                        encoding="utf-8"
                    )
                ),
            },
        },
        {
            "type": "response_item",
            "payload": {
                "type": "custom_tool_call",
                "call_id": "duplicate-call",
                "name": "exec",
                "input": "Get-Content -Raw skills/verify-completion/SKILL.md",
            },
        },
    ]
    duplicate_call_trace.write_text(
        "".join(json.dumps(row) + "\n" for row in duplicate_rows),
        encoding="utf-8",
    )
    duplicate_call_receipt = copy.deepcopy(receipt)
    attach_trace(
        duplicate_call_receipt,
        duplicate_call_trace,
        bundle_path=bundle,
        complete=True,
    )
    check(
        duplicate_call_receipt["activation"]["status"] == "unknown",
        "duplicate call ID cross-paired unrelated output with a Skill read",
    )

    unknown_record_trace = temp / "unknown-record.jsonl"
    unknown_rows = [
        json.loads(line)
        for line in no_read_trace.read_text(encoding="utf-8").splitlines()
    ]
    unknown_rows.insert(
        -1,
        {
            "type": "future_model_output",
            "payload": {"type": "future_text", "text": "unparsed model-visible output"},
        },
    )
    unknown_record_trace.write_text(
        "".join(json.dumps(row) + "\n" for row in unknown_rows),
        encoding="utf-8",
    )
    unknown_record_receipt = copy.deepcopy(receipt)
    attach_trace(
        unknown_record_receipt,
        unknown_record_trace,
        bundle_path=bundle,
        complete=True,
    )
    check(
        unknown_record_receipt["activation"]["status"] == "unknown",
        "unrecognized trace record was ignored for absence",
    )

    future_message_trace = temp / "future-message-block.jsonl"
    future_message_rows = [
        json.loads(line) for line in no_read_trace.read_text(encoding="utf-8").splitlines()
    ]
    future_message_rows.insert(
        -1,
        {
            "type": "response_item",
            "payload": {
                "type": "message",
                "role": "assistant",
                "content": [{"type": "future_text", "text": "unparsed model output"}],
            },
        },
    )
    future_message_trace.write_text(
        "".join(json.dumps(row) + "\n" for row in future_message_rows),
        encoding="utf-8",
    )
    future_message_receipt = copy.deepcopy(receipt)
    attach_trace(
        future_message_receipt,
        future_message_trace,
        bundle_path=bundle,
        complete=True,
    )
    check(
        future_message_receipt["serving"]["status"] == "unknown"
        and future_message_receipt["activation"]["status"] == "unknown",
        "future nested message block produced definite absence",
    )

    dangling_call_trace = temp / "dangling-read-call.jsonl"
    dangling_call_rows = [
        json.loads(line) for line in no_read_trace.read_text(encoding="utf-8").splitlines()
    ]
    dangling_call_rows.insert(
        -1,
        {
            "type": "response_item",
            "payload": {
                "type": "custom_tool_call",
                "call_id": "dangling-read",
                "name": "exec",
                "input": "Get-Content -Raw skills/verify-completion/SKILL.md",
            },
        },
    )
    dangling_call_trace.write_text(
        "".join(json.dumps(row) + "\n" for row in dangling_call_rows),
        encoding="utf-8",
    )
    dangling_call_receipt = copy.deepcopy(receipt)
    attach_trace(
        dangling_call_receipt,
        dangling_call_trace,
        bundle_path=bundle,
        complete=True,
    )
    check(
        dangling_call_receipt["serving"]["status"] == "unknown"
        and dangling_call_receipt["activation"]["status"] == "unknown",
        "dangling read call produced definite absence",
    )

    missing_timestamp_trace = temp / "missing-session-timestamp.jsonl"
    missing_timestamp_rows = [
        json.loads(line) for line in no_read_trace.read_text(encoding="utf-8").splitlines()
    ]
    missing_timestamp_rows[0]["payload"].pop("timestamp")
    missing_timestamp_trace.write_text(
        "".join(json.dumps(row) + "\n" for row in missing_timestamp_rows),
        encoding="utf-8",
    )
    missing_timestamp_receipt = copy.deepcopy(receipt)
    attach_trace(
        missing_timestamp_receipt,
        missing_timestamp_trace,
        bundle_path=bundle,
        complete=True,
    )
    check(
        missing_timestamp_receipt["serving"]["status"] == "unknown"
        and missing_timestamp_receipt["activation"]["status"] == "unknown",
        "missing session timestamp bypassed preflight chronology",
    )

    future_timestamp_trace = temp / "future-session-timestamp.jsonl"
    future_timestamp_rows = [
        json.loads(line) for line in no_read_trace.read_text(encoding="utf-8").splitlines()
    ]
    future_timestamp_rows[0]["payload"]["timestamp"] = "9999-01-01T00:00:00Z"
    future_timestamp_trace.write_text(
        "".join(json.dumps(row) + "\n" for row in future_timestamp_rows),
        encoding="utf-8",
    )
    future_timestamp_receipt = copy.deepcopy(receipt)
    attach_trace(
        future_timestamp_receipt,
        future_timestamp_trace,
        bundle_path=bundle,
        complete=True,
    )
    check(
        future_timestamp_receipt["serving"]["status"] == "unknown"
        and future_timestamp_receipt["activation"]["status"] == "unknown",
        "future session timestamp produced attribution evidence",
    )

    malformed_trace = temp / "malformed-no-read.jsonl"
    write_trace(malformed_trace, session_id=session_id, include_read=False, bundle=bundle)
    malformed_trace.write_text(
        malformed_trace.read_text(encoding="utf-8") + "{not-json\n",
        encoding="utf-8",
    )
    malformed_trace_receipt = copy.deepcopy(receipt)
    attach_trace(
        malformed_trace_receipt,
        malformed_trace,
        bundle_path=bundle,
        complete=True,
    )
    check(
        malformed_trace_receipt["activation"]["status"] == "unknown",
        "parse-error trace invented activation absence",
    )

    structured_metadata_trace = temp / "structured-metadata.jsonl"
    metadata_rows = [json.loads(line) for line in trace.read_text(encoding="utf-8").splitlines()]
    skill_body = (bundle / "skills" / "verify-completion" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    for row in metadata_rows:
        payload = row.get("payload", {})
        if payload.get("type") == "custom_tool_call_output" and payload.get("call_id") == "call-good":
            payload["output"] = {"metadata": skill_body, "status": "completed"}
    structured_metadata_trace.write_text(
        "".join(json.dumps(row) + "\n" for row in metadata_rows),
        encoding="utf-8",
    )
    structured_metadata_receipt = copy.deepcopy(receipt)
    attach_trace(
        structured_metadata_receipt,
        structured_metadata_trace,
        bundle_path=bundle,
        complete=True,
    )
    check(
        structured_metadata_receipt["activation"]["status"] == "unknown",
        "unknown structured-output shape produced definite activation absence",
    )

    future_output_trace = temp / "future-output-shape.jsonl"
    future_output_rows = [
        json.loads(line) for line in trace.read_text(encoding="utf-8").splitlines()
    ]
    for row in future_output_rows:
        payload = row.get("payload", {})
        if payload.get("type") == "custom_tool_call_output" and payload.get("call_id") == "call-good":
            payload["output"] = [{"type": "future_output_text", "text": skill_body}]
    future_output_trace.write_text(
        "".join(json.dumps(row) + "\n" for row in future_output_rows),
        encoding="utf-8",
    )
    future_output_receipt = copy.deepcopy(receipt)
    attach_trace(
        future_output_receipt,
        future_output_trace,
        bundle_path=bundle,
        complete=True,
    )
    check(
        future_output_receipt["serving"]["status"] == "unknown"
        and future_output_receipt["activation"]["status"] == "unknown",
        "future tool-output block shape produced definite absence",
    )

    for label, unsupported_output in (
        ("scalar", "Script completed\nExit code: 0\n" + skill_body),
        (
            "output-text",
            [{"type": "output_text", "text": "Exit code: 0\n" + skill_body}],
        ),
        ("text", [{"type": "text", "text": "Exit code: 0\n" + skill_body}]),
    ):
        unsupported_output_trace = temp / f"unsupported-{label}-output.jsonl"
        unsupported_output_rows = [
            json.loads(line) for line in trace.read_text(encoding="utf-8").splitlines()
        ]
        for row in unsupported_output_rows:
            payload = row.get("payload", {})
            if (
                payload.get("type") == "custom_tool_call_output"
                and payload.get("call_id") == "call-good"
            ):
                payload["output"] = unsupported_output
        unsupported_output_trace.write_text(
            "".join(json.dumps(row) + "\n" for row in unsupported_output_rows),
            encoding="utf-8",
        )
        unsupported_output_receipt = copy.deepcopy(receipt)
        attach_trace(
            unsupported_output_receipt,
            unsupported_output_trace,
            bundle_path=bundle,
            complete=True,
        )
        check(
            unsupported_output_receipt["serving"]["status"] == "unknown"
            and unsupported_output_receipt["activation"]["status"] == "unknown",
            f"unsupported {label} output shape produced attribution evidence",
        )

    for field, value in (("status", "failed"), ("error", "permission denied")):
        structured_failure_trace = temp / f"structured-{field}-failure.jsonl"
        structured_failure_rows = [
            json.loads(line) for line in trace.read_text(encoding="utf-8").splitlines()
        ]
        for row in structured_failure_rows:
            payload = row.get("payload", {})
            if (
                payload.get("type") == "custom_tool_call_output"
                and payload.get("call_id") == "call-good"
            ):
                payload[field] = value
        structured_failure_trace.write_text(
            "".join(json.dumps(row) + "\n" for row in structured_failure_rows),
            encoding="utf-8",
        )
        structured_failure_receipt = copy.deepcopy(receipt)
        attach_trace(
            structured_failure_receipt,
            structured_failure_trace,
            bundle_path=bundle,
            complete=True,
        )
        check(
            structured_failure_receipt["serving"]["status"] == "unknown"
            and structured_failure_receipt["activation"]["status"] == "unknown",
            f"structured {field} failure metadata produced attribution evidence",
        )

    input_text_output_trace = temp / "input-text-output-shape.jsonl"
    input_text_output_rows = [
        json.loads(line) for line in trace.read_text(encoding="utf-8").splitlines()
    ]
    for row in input_text_output_rows:
        payload = row.get("payload", {})
        if payload.get("type") == "custom_tool_call_output" and payload.get("call_id") == "call-good":
            payload["output"] = [{"type": "input_text", "text": skill_body}]
    input_text_output_trace.write_text(
        "".join(json.dumps(row) + "\n" for row in input_text_output_rows),
        encoding="utf-8",
    )
    input_text_output_receipt = copy.deepcopy(receipt)
    attach_trace(
        input_text_output_receipt,
        input_text_output_trace,
        bundle_path=bundle,
        complete=True,
    )
    check(
        input_text_output_receipt["activation"]["status"] == "none_observed",
        "unframed input_text tool output produced activation evidence",
    )

    framed_input_text_trace = temp / "framed-input-text-output.jsonl"
    framed_input_text_rows = [
        json.loads(line) for line in trace.read_text(encoding="utf-8").splitlines()
    ]
    for row in framed_input_text_rows:
        payload = row.get("payload", {})
        if payload.get("type") == "custom_tool_call_output" and payload.get("call_id") == "call-good":
            payload["output"] = [
                {"type": "input_text", "text": "Script completed\nOutput:\n"},
                {"type": "input_text", "text": "Exit code: 0\nOutput:\n" + skill_body},
            ]
    framed_input_text_trace.write_text(
        "".join(json.dumps(row) + "\n" for row in framed_input_text_rows),
        encoding="utf-8",
    )
    framed_input_text_receipt = copy.deepcopy(receipt)
    attach_trace(
        framed_input_text_receipt,
        framed_input_text_trace,
        bundle_path=bundle,
        complete=True,
    )
    check(
        framed_input_text_receipt["activation"]["status"] == "observed_skill_content",
        "recognized Codex input_text output envelope lost activation evidence",
    )

    explicit_failure_trace = temp / "explicit-failure-after-body.jsonl"
    explicit_failure_rows = [
        json.loads(line) for line in trace.read_text(encoding="utf-8").splitlines()
    ]
    for row in explicit_failure_rows:
        payload = row.get("payload", {})
        if payload.get("type") == "custom_tool_call_output" and payload.get("call_id") == "call-good":
            payload["output"] = [
                {
                    "type": "input_text",
                    "text": (
                        "Script completed\nExit code: 0\nOutput:\n"
                        + skill_body
                        + "\nERROR: failed to read file"
                    ),
                }
            ]
    explicit_failure_trace.write_text(
        "".join(json.dumps(row) + "\n" for row in explicit_failure_rows),
        encoding="utf-8",
    )
    explicit_failure_receipt = copy.deepcopy(receipt)
    attach_trace(
        explicit_failure_receipt,
        explicit_failure_trace,
        bundle_path=bundle,
        complete=True,
    )
    check(
        explicit_failure_receipt["activation"]["status"] == "none_observed",
        "explicit failed tool output produced activation evidence",
    )

    nonzero_exit_trace = temp / "nonzero-exit-after-body.jsonl"
    nonzero_exit_rows = [
        json.loads(line) for line in trace.read_text(encoding="utf-8").splitlines()
    ]
    for row in nonzero_exit_rows:
        payload = row.get("payload", {})
        if payload.get("type") == "custom_tool_call_output" and payload.get("call_id") == "call-good":
            payload["output"] = [
                {
                    "type": "input_text",
                    "text": (
                        "Script completed\nExit code: 0\nOutput:\n"
                        + skill_body
                        + "\nProcess exited with code 7"
                    ),
                }
            ]
    nonzero_exit_trace.write_text(
        "".join(json.dumps(row) + "\n" for row in nonzero_exit_rows),
        encoding="utf-8",
    )
    nonzero_exit_receipt = copy.deepcopy(receipt)
    attach_trace(
        nonzero_exit_receipt,
        nonzero_exit_trace,
        bundle_path=bundle,
        complete=True,
    )
    check(
        nonzero_exit_receipt["activation"]["status"] == "none_observed",
        "nonzero tool exit produced activation evidence",
    )

    for label, failure_text in (
        ("missing-path", "The path does not exist"),
        ("permission-error", "PermissionError: denied"),
        ("compact-exit-code", "ExitCode=7"),
        ("inline-error-field", "Output: ERROR: read failed"),
        ("access-denied", "Output: access denied"),
        ("file-not-found", "Output: file not found"),
        ("path-missing", "Output: path missing"),
        ("process-exit", "Output: process-exit=7"),
        ("bare-status", "Output: status 7"),
        ("nonzero-field", "Output: nonzero=7"),
        ("return-code-field", "Output: rc=7"),
        ("return-status-field", "Output: return_status=7"),
    ):
        failed_variant_trace = temp / f"{label}-after-body.jsonl"
        failed_variant_rows = [
            json.loads(line) for line in trace.read_text(encoding="utf-8").splitlines()
        ]
        for row in failed_variant_rows:
            payload = row.get("payload", {})
            if (
                payload.get("type") == "custom_tool_call_output"
                and payload.get("call_id") == "call-good"
            ):
                payload["output"] = [
                    {
                        "type": "input_text",
                        "text": (
                            "Script completed\nExit code: 0\nOutput:\n"
                            + skill_body
                            + "\n"
                            + failure_text
                        ),
                    }
                ]
        failed_variant_trace.write_text(
            "".join(json.dumps(row) + "\n" for row in failed_variant_rows),
            encoding="utf-8",
        )
        failed_variant_receipt = copy.deepcopy(receipt)
        attach_trace(
            failed_variant_receipt,
            failed_variant_trace,
            bundle_path=bundle,
            complete=True,
        )
        check(
            failed_variant_receipt["activation"]["status"] == "none_observed",
            f"{label} tool failure produced activation evidence",
        )

    split_status_trace = temp / "split-status-after-body.jsonl"
    split_status_rows = [
        json.loads(line) for line in trace.read_text(encoding="utf-8").splitlines()
    ]
    for row in split_status_rows:
        payload = row.get("payload", {})
        if payload.get("type") == "custom_tool_call_output" and payload.get("call_id") == "call-good":
            payload["output"] = [
                {
                    "type": "input_text",
                    "text": "Script completed\nExit code: 0\nOutput:\n" + skill_body,
                },
                {"type": "input_text", "text": "r"},
                {"type": "input_text", "text": "c=7"},
            ]
    split_status_trace.write_text(
        "".join(json.dumps(row) + "\n" for row in split_status_rows),
        encoding="utf-8",
    )
    split_status_receipt = copy.deepcopy(receipt)
    attach_trace(
        split_status_receipt,
        split_status_trace,
        bundle_path=bundle,
        complete=True,
    )
    check(
        split_status_receipt["activation"]["status"] == "none_observed",
        "split nonzero return code produced activation evidence",
    )

    future_call_trace = temp / "future-call-shape.jsonl"
    future_call_rows = [
        json.loads(line) for line in no_read_trace.read_text(encoding="utf-8").splitlines()
    ]
    future_call_rows[-1:-1] = [
        {
            "type": "response_item",
            "payload": {
                "type": "custom_tool_call",
                "call_id": "future-call",
                "name": "exec",
                "future_input": "Get-Content skills/verify-completion/SKILL.md",
            },
        },
        {
            "type": "response_item",
            "payload": {
                "type": "custom_tool_call_output",
                "call_id": "future-call",
                "output": "Script completed\nExit code: 0",
            },
        },
    ]
    future_call_trace.write_text(
        "".join(json.dumps(row) + "\n" for row in future_call_rows),
        encoding="utf-8",
    )
    future_call_receipt = copy.deepcopy(receipt)
    attach_trace(
        future_call_receipt,
        future_call_trace,
        bundle_path=bundle,
        complete=True,
    )
    check(
        future_call_receipt["serving"]["status"] == "unknown"
        and future_call_receipt["activation"]["status"] == "unknown",
        "future tool-call input shape produced definite absence",
    )

    stable_snapshot_trace = temp / "stable-snapshot.jsonl"
    stable_snapshot_trace.write_bytes(no_read_trace.read_bytes())
    stable_snapshot = stable_snapshot_trace.read_bytes()
    stable_snapshot_trace.write_text(
        stable_snapshot_trace.read_text(encoding="utf-8")
        + json.dumps({"type": "response_item", "payload": {"type": "reasoning", "summary": []}})
        + "\n",
        encoding="utf-8",
    )
    stable_snapshot_receipt = copy.deepcopy(receipt)
    attach_trace(
        stable_snapshot_receipt,
        stable_snapshot_trace,
        bundle_path=bundle,
        complete=True,
        trace_bytes=stable_snapshot,
    )
    check(
        stable_snapshot_receipt["session"]["trace"]["content_digest"]
        == "sha256:" + hashlib.sha256(stable_snapshot).hexdigest(),
        "trace receipt digest was not bound to the scanned snapshot bytes",
    )
    check(
        stable_snapshot_receipt["session"]["trace"]["content_digest"]
        != "sha256:" + hashlib.sha256(stable_snapshot_trace.read_bytes()).hexdigest(),
        "stable snapshot test did not distinguish later file mutation",
    )

    stale = copy.deepcopy(receipt)
    stale["serving"]["bundle"]["skill_digests"]["verify-completion"] = "sha256:" + "0" * 64
    seal_receipt(stale)
    validate_receipt(stale)
    stale_result = classify_failure(
        stale,
        skill="verify-completion",
        current_bundle=identity,
        failure_domain="agent",
        behavior_evidence=None,
    )
    check(stale_result["classification"] == "not_served", "stale relevant Skill digest was not detected")

    absent_from_served = copy.deepcopy(receipt)
    absent_from_served["serving"]["bundle"]["skill_digests"].pop("verify-completion")
    absent_from_served["activation"]["observed_skills"] = []
    absent_from_served["activation"]["status"] = "none_observed"
    absent_from_served["activation"]["evidence_scope"] = "complete_trace_snapshot"
    seal_receipt(absent_from_served)
    validate_receipt(absent_from_served)
    missing_result = classify_failure(
        absent_from_served,
        skill="verify-completion",
        current_bundle=identity,
        failure_domain="agent",
        behavior_evidence=None,
    )
    check(missing_result["classification"] == "not_served", "missing current Skill was not detected")

    never_exists = classify_failure(
        receipt,
        skill="does-not-exist",
        current_bundle=identity,
        failure_domain="agent",
        behavior_evidence=None,
    )
    check(
        never_exists["classification"] == "requested_skill_artifact_absent",
        "artifact absence was overclaimed as semantic capability absence",
    )
    served_only_absent = classify_failure(
        receipt,
        skill="does-not-exist",
        current_bundle=None,
        failure_domain="agent",
        behavior_evidence=None,
    )
    check(
        served_only_absent["classification"] == "served_skill_artifact_absent",
        "missing current reference produced a two-bundle absence claim",
    )

    other_commit = copy.deepcopy(receipt)
    other_commit["serving"]["bundle"]["source_commit"] = "0" * 40
    seal_receipt(other_commit)
    validate_receipt(other_commit)
    same_skill_result = classify_failure(
        other_commit,
        skill="verify-completion",
        current_bundle=identity,
        failure_domain="agent",
        behavior_evidence=None,
    )
    check(
        same_skill_result["classification"] == "activation_observed",
        "unrelated source commit drift overrode identical relevant Skill digest",
    )

    backfill = make_backfill_receipt(trace)
    check(backfill["serving"]["status"] == "unknown", "legacy backfill invented serving")
    backfill_result = classify_failure(
        backfill,
        skill="verify-completion",
        current_bundle=identity,
        failure_domain="agent",
        behavior_evidence=None,
    )
    check(backfill_result["classification"] == "unknown_attribution", "unknown serving was over-attributed")

    unsafe_trace = temp / "unsafe-session.jsonl"
    write_trace(
        unsafe_trace,
        session_id="private project name with spaces",
        include_read=False,
        bundle=None,
    )
    unsafe_backfill = make_backfill_receipt(unsafe_trace)
    check(
        unsafe_backfill["session"]["id"].startswith("sha256:"),
        "unsafe session identifier was copied",
    )
    check(
        unsafe_backfill["session"]["trace"]["pointer"].startswith("sha256:"),
        "trace path was not made opaque",
    )

    malformed = copy.deepcopy(receipt)
    malformed.pop("privacy")
    try:
        validate_receipt(malformed)
    except AttributionError:
        pass
    else:
        errors.append("missing receipt field was accepted")

    future_receipt = copy.deepcopy(receipt)
    future_receipt["recorded_at"] = "9999-01-01T00:00:00Z"
    seal_receipt(future_receipt)
    try:
        validate_receipt(future_receipt)
    except AttributionError:
        pass
    else:
        errors.append("future receipt timestamp was accepted")

    future_probe = copy.deepcopy(probe)
    future_probe["recorded_at"] = "9999-01-01T00:00:00Z"
    seal_probe(future_probe)
    try:
        validate_probe(future_probe)
    except AttributionError:
        pass
    else:
        errors.append("future serving preflight timestamp was accepted")

    tampered_receipt = copy.deepcopy(receipt)
    tampered_receipt["runtime"]["model"] = "tampered"
    try:
        validate_receipt(tampered_receipt)
    except AttributionError as exc:
        check("integrity" in str(exc), "tampered receipt failed for the wrong reason")
    else:
        errors.append("tampered receipt integrity was accepted")

    private_repository_receipt = copy.deepcopy(receipt)
    private_repository_receipt["serving"]["bundle"]["source_repository"] = "file:///C:/private"
    seal_receipt(private_repository_receipt)
    try:
        validate_receipt(private_repository_receipt)
    except AttributionError:
        pass
    else:
        errors.append("path-like repository identity was accepted")

    private_skill_map_receipt = copy.deepcopy(receipt)
    private_digest = private_skill_map_receipt["serving"]["bundle"]["skill_digests"].pop(
        "verify-completion"
    )
    private_skill_map_receipt["serving"]["bundle"]["skill_digests"][
        "C:/private/Skill"
    ] = private_digest
    private_skill_map_receipt["activation"]["observed_skills"] = []
    private_skill_map_receipt["activation"]["status"] = "none_observed"
    private_skill_map_receipt["activation"]["evidence_scope"] = "complete_trace_snapshot"
    seal_receipt(private_skill_map_receipt)
    try:
        validate_receipt(private_skill_map_receipt)
    except AttributionError:
        pass
    else:
        errors.append("path-like private Skill map key was accepted")

    private_activation_receipt = copy.deepcopy(receipt)
    private_activation_receipt["activation"]["observed_skills"][0]["name"] = (
        "secret-acme-project"
    )
    seal_receipt(private_activation_receipt)
    try:
        validate_receipt(private_activation_receipt)
    except AttributionError:
        pass
    else:
        errors.append("noncanonical private activation Skill name was accepted")

    impossible_absence_receipt = copy.deepcopy(receipt)
    impossible_absence_receipt["session"]["trace"] = {
        "status": "unknown",
        "pointer": None,
        "content_digest": None,
        "bytes": None,
    }
    impossible_absence_receipt["serving"]["evidence"] = [
        "bundle_at_session_cwd_assignment_pending"
    ]
    for serving_surface in impossible_absence_receipt["serving"]["surfaces"]:
        if serving_surface["name"] == "AGENTS.md":
            serving_surface["evidence"] = "manifest_agents_artifact_verified"
    impossible_absence_receipt["activation"] = {
        "status": "none_observed",
        "evidence_scope": "complete_trace_snapshot",
        "observed_skills": [],
        "adoption_claim": "unknown",
    }
    seal_receipt(impossible_absence_receipt)
    try:
        validate_receipt(impossible_absence_receipt)
    except AttributionError:
        pass
    else:
        errors.append("verified absence without world_state and linked trace was accepted")

    snapshot_verified_receipt = copy.deepcopy(receipt)
    snapshot_verified_receipt["session"]["trace"]["status"] = "snapshot"
    snapshot_verified_receipt["serving"]["evidence"].append("trace_incomplete")
    seal_receipt(snapshot_verified_receipt)
    try:
        validate_receipt(snapshot_verified_receipt)
    except AttributionError:
        pass
    else:
        errors.append("verified serving accepted an incomplete trace snapshot")

    contradictory_receipt = copy.deepcopy(receipt)
    contradictory_receipt["serving"]["evidence"].append(
        "world_state_assignment_mismatch"
    )
    seal_receipt(contradictory_receipt)
    try:
        validate_receipt(contradictory_receipt)
    except AttributionError:
        pass
    else:
        errors.append("verified serving retained contradictory mismatch evidence")

    for field, mutate in (
        (
            "serving evidence",
            lambda value: value["serving"].update({"evidence": ["C:/private/prompt.txt"]}),
        ),
        (
            "surface evidence",
            lambda value: value["serving"]["surfaces"][0].update(
                {"evidence": "private prompt or tool payload"}
            ),
        ),
        (
            "surface name",
            lambda value: value["serving"]["surfaces"][0].update(
                {"name": "C:/private/AGENTS.md"}
            ),
        ),
    ):
        private_text_receipt = copy.deepcopy(receipt)
        mutate(private_text_receipt)
        seal_receipt(private_text_receipt)
        try:
            validate_receipt(private_text_receipt)
        except AttributionError:
            pass
        else:
            errors.append(f"free-form private {field} was accepted")

    mismatched_trace = temp / "mismatched.jsonl"
    write_trace(mismatched_trace, session_id="different-session", include_read=False)
    try:
        attach_trace(copy.deepcopy(receipt), mismatched_trace, bundle_path=bundle, complete=True)
    except AttributionError:
        pass
    else:
        errors.append("mismatched transcript session id was accepted")

    multi_session_trace = temp / "multi-session.jsonl"
    multi_session_rows = [
        json.loads(line) for line in trace.read_text(encoding="utf-8").splitlines()
    ]
    multi_session_rows.insert(
        1,
        {
            "type": "session_meta",
            "payload": {
                "id": "019fe3d6-f66e-7873-9b80-91bc17d7b3ff",
                "timestamp": "2026-08-09T00:00:01Z",
                "cwd": "C:/private/foreign",
                "cli_version": "0.146.0",
                "source": "exec",
            },
        },
    )
    multi_session_trace.write_text(
        "".join(json.dumps(row) + "\n" for row in multi_session_rows),
        encoding="utf-8",
    )
    multi_session_receipt = make_codex_linked_receipt(
        multi_session_trace,
        bundle_path=bundle,
        probe_path=probe_path,
    )
    check(
        multi_session_receipt["serving"]["status"] == "unknown",
        "multi-session trace attributed serving evidence across sessions",
    )
    check(
        multi_session_receipt["activation"]["status"] == "unknown",
        "multi-session trace attributed Skill evidence across sessions",
    )

    tampered_bundle = temp / "tampered-runtime"
    build_bundle(tampered_bundle, allow_dirty=True)
    skill_file = tampered_bundle / "skills" / "verify-completion" / "SKILL.md"
    skill_file.write_bytes(skill_file.read_bytes() + b"\nTAMPERED\n")
    tampered_start = copy.deepcopy(start)
    tampered_start["session_id"] = "019fe3d6-f66e-7873-9b80-91bc17d7b3c6"
    tampered_start["cwd"] = str(tampered_bundle)
    tampered_receipt_file = handle_codex_event(
        tampered_start,
        bundle_path=tampered_bundle,
        receipt_dir=temp / "tampered-receipts",
        probe_path=probe_path,
    )
    tampered_serving_receipt = load_receipt(tampered_receipt_file)
    check(
        tampered_serving_receipt["serving"]["status"] == "mismatch",
        "bundle verification failure did not produce a mismatch receipt",
    )
    tampered_link = make_codex_linked_receipt(
        trace,
        bundle_path=tampered_bundle,
        probe_path=probe_path,
    )
    check(
        tampered_link["serving"]["status"] == "mismatch",
        "explicit link crashed or accepted an unverifiable bundle",
    )
    try:
        bundle_identity(tampered_bundle)
    except BundleError:
        pass
    else:
        errors.append("tampered bundle was accepted for serving attribution")

    catalog_mismatch = temp / "catalog-mismatch"
    build_bundle(catalog_mismatch, allow_dirty=True)
    catalog_file = catalog_mismatch / "runtime-catalog.json"
    catalog_file.write_bytes(catalog_file.read_bytes() + b"\n")
    try:
        bundle_identity(catalog_mismatch)
    except BundleError:
        pass
    else:
        errors.append("runtime catalog digest mismatch was accepted")

    other_runtime = temp / "other-runtime-path"
    build_bundle(other_runtime, allow_dirty=True)
    other_identity = bundle_identity(other_runtime)
    other_probe = copy.deepcopy(probe)
    other_probe["probe_id"] = "019fe3d4-0000-7000-8000-000000000002"
    other_probe["bundle"]["manifest_digest"] = other_identity["manifest_digest"]
    other_probe["bundle"]["path_digest"] = other_identity["path_digest"]
    other_probe["bundle"]["agents_digest"] = other_identity["agents_digest"]
    other_probe["bundle"]["runtime_catalog_digest"] = other_identity[
        "runtime_catalog_digest"
    ]
    seal_probe(other_probe)
    other_probe_path = temp / "other-probe.json"
    other_probe_path.write_text(json.dumps(other_probe), encoding="utf-8")

    switch_receipts = temp / "switch-receipts"
    switch_session = "019fe3d6-f66e-7873-9b80-91bc17d7b3e0"
    switch_a_start = copy.deepcopy(start)
    switch_a_start["session_id"] = switch_session
    switch_file = handle_codex_event(
        switch_a_start,
        bundle_path=bundle,
        receipt_dir=switch_receipts,
        probe_path=probe_path,
    )
    switch_b_start = copy.deepcopy(switch_a_start)
    switch_b_start["cwd"] = str(other_runtime)
    handle_codex_event(
        switch_b_start,
        bundle_path=other_runtime,
        receipt_dir=switch_receipts,
        probe_path=other_probe_path,
    )
    check(
        load_receipt(switch_file)["serving"]["status"] == "mismatch",
        "same-session bundle switch was not recorded as mismatch",
    )
    handle_codex_event(
        switch_b_start,
        bundle_path=other_runtime,
        receipt_dir=switch_receipts,
        probe_path=other_probe_path,
    )
    check(
        load_receipt(switch_file)["serving"]["status"] == "mismatch",
        "repeated replacement startup erased the prior bundle switch",
    )
    switch_b_trace = temp / "switch-b-session.jsonl"
    write_trace(
        switch_b_trace,
        session_id=switch_session,
        include_read=False,
        bundle=other_runtime,
    )
    switch_b_end = {
        "session_id": switch_session,
        "transcript_path": str(switch_b_trace),
        "cwd": str(other_runtime),
        "hook_event_name": "SessionEnd",
        "model": "test-model",
        "reason": "other",
    }
    handle_codex_event(
        switch_b_end,
        bundle_path=other_runtime,
        receipt_dir=switch_receipts,
        probe_path=other_probe_path,
    )
    check(
        load_receipt(switch_file)["serving"]["status"] == "mismatch",
        "final B trace erased the prior A-to-B same-session mismatch",
    )

    changed_resume = copy.deepcopy(start)
    changed_resume["cwd"] = str(other_runtime)
    handle_codex_event(
        changed_resume,
        bundle_path=other_runtime,
        receipt_dir=receipts,
        probe_path=probe_path,
    )
    changed_resume_receipt = load_receipt(receipt_file)
    check(
        changed_resume_receipt["serving"]["status"] == "mismatch",
        "resume with another bundle overwrote prior session evidence",
    )
    mixed_assignment_trace = temp / "mixed-assignment.jsonl"
    mixed_rows = [
        json.loads(line)
        for line in trace.read_text(encoding="utf-8").splitlines()
    ]
    mixed_rows.insert(
        -1,
        {
            "type": "world_state",
            "payload": {
                "state": {
                    "agents_md": {
                        "directory": str(other_runtime),
                        "text": (other_runtime / "AGENTS.md").read_text(encoding="utf-8"),
                    }
                }
            },
        },
    )
    mixed_assignment_trace.write_text(
        "".join(json.dumps(row) + "\n" for row in mixed_rows),
        encoding="utf-8",
    )
    mixed_assignment_receipt = make_codex_linked_receipt(
        mixed_assignment_trace,
        bundle_path=bundle,
        probe_path=probe_path,
    )
    check(
        mixed_assignment_receipt["serving"]["status"] == "mismatch",
        "multiple world_state assignments were collapsed to the last one",
    )
    check(
        mixed_assignment_receipt["activation"]["status"] == "unknown",
        "Skill-body output was attributed to a mismatched serving bundle",
    )
    malformed_mismatch_trace = temp / "malformed-and-mismatched-world-state.jsonl"
    malformed_mismatch_rows = copy.deepcopy(mixed_rows)
    malformed_mismatch_rows.insert(-1, {"type": "world_state", "payload": {"state": {}}})
    malformed_mismatch_trace.write_text(
        "".join(json.dumps(row) + "\n" for row in malformed_mismatch_rows),
        encoding="utf-8",
    )
    malformed_mismatch_receipt = make_codex_linked_receipt(
        malformed_mismatch_trace,
        bundle_path=bundle,
        probe_path=probe_path,
    )
    check(
        malformed_mismatch_receipt["serving"]["status"] == "mismatch",
        "malformed world_state downgraded a definite assignment mismatch",
    )
    check(
        malformed_mismatch_receipt["activation"]["status"] != "none_observed",
        "malformed world_state allowed activation absence",
    )
    invalid_world_trace = temp / "invalid-world-state.jsonl"
    invalid_world_rows = [
        json.loads(line)
        for line in no_read_trace.read_text(encoding="utf-8").splitlines()
    ]
    invalid_world_rows.insert(-1, {"type": "world_state", "payload": {"state": {}}})
    invalid_world_trace.write_text(
        "".join(json.dumps(row) + "\n" for row in invalid_world_rows),
        encoding="utf-8",
    )
    invalid_world_receipt = make_codex_linked_receipt(
        invalid_world_trace,
        bundle_path=bundle,
        probe_path=probe_path,
    )
    check(
        invalid_world_receipt["serving"]["status"] == "unknown",
        "malformed world_state was ignored while serving became verified",
    )
    check(
        invalid_world_receipt["activation"]["status"] == "unknown",
        "malformed world_state allowed activation absence",
    )
    invalid_payload_trace = temp / "invalid-world-payload.jsonl"
    invalid_payload_rows = [
        json.loads(line)
        for line in no_read_trace.read_text(encoding="utf-8").splitlines()
    ]
    invalid_payload_rows.insert(-1, {"type": "world_state", "payload": None})
    invalid_payload_trace.write_text(
        "".join(json.dumps(row) + "\n" for row in invalid_payload_rows),
        encoding="utf-8",
    )
    invalid_payload_receipt = make_codex_linked_receipt(
        invalid_payload_trace,
        bundle_path=bundle,
        probe_path=probe_path,
    )
    check(
        invalid_payload_receipt["serving"]["status"] == "unknown",
        "non-object world_state payload was ignored",
    )
    check(
        invalid_payload_receipt["activation"]["status"] == "unknown",
        "non-object world_state payload allowed activation absence",
    )

    stale_output = temp / "stale-command-output.json"
    stale_output.write_text(json.dumps(receipt), encoding="utf-8")
    try:
        cmd_codex_link(
            Namespace(
                session=str(temp / "missing-link-trace.jsonl"),
                bundle=str(bundle),
                probe=str(probe_path),
                output=str(stale_output),
            )
        )
    except AttributionError:
        pass
    else:
        errors.append("missing codex-link trace unexpectedly succeeded")
    stale_marker = json.loads(stale_output.read_text(encoding="utf-8"))
    check(
        stale_marker.get("record_type") == "execution-attribution-pending"
        and stale_marker.get("operation") == "codex-link"
        and "serving" not in stale_marker,
        "failed codex-link retained a stale verified output",
    )

    stale_output.write_text(json.dumps(receipt), encoding="utf-8")
    try:
        cmd_backfill(
            Namespace(
                session=str(temp / "missing-backfill-trace.jsonl"),
                output=str(stale_output),
            )
        )
    except OSError:
        pass
    else:
        errors.append("missing backfill trace unexpectedly succeeded")
    stale_marker = json.loads(stale_output.read_text(encoding="utf-8"))
    check(
        stale_marker.get("record_type") == "execution-attribution-pending"
        and stale_marker.get("operation") == "backfill"
        and "serving" not in stale_marker,
        "failed backfill retained a stale verified output",
    )

    stale_output.write_text(json.dumps(probe), encoding="utf-8")
    try:
        cmd_probe(
            Namespace(
                bundle=str(bundle),
                codex_command=str(temp / "missing-codex.exe"),
                output=str(stale_output),
            )
        )
    except OSError:
        pass
    else:
        errors.append("missing Codex command unexpectedly produced a probe")
    stale_marker = json.loads(stale_output.read_text(encoding="utf-8"))
    check(
        stale_marker.get("record_type") == "execution-attribution-pending"
        and stale_marker.get("operation") == "codex-probe"
        and "bundle" not in stale_marker,
        "failed codex-probe retained a stale serving preflight",
    )

    unsupported_hook_receipts = temp / "unsupported-hook-receipts"
    unsupported_hook_session = "019fe3d6-f66e-7873-9b80-91bc17d7b3e4"
    unsupported_hook_start = copy.deepcopy(start)
    unsupported_hook_start["session_id"] = unsupported_hook_session
    unsupported_hook_file = handle_codex_event(
        unsupported_hook_start,
        bundle_path=bundle,
        receipt_dir=unsupported_hook_receipts,
        probe_path=probe_path,
    )
    unsupported_hook_trace = temp / "unsupported-hook-session.jsonl"
    write_trace(
        unsupported_hook_trace,
        session_id=unsupported_hook_session,
        include_read=True,
        bundle=bundle,
    )
    handle_codex_event(
        {
            "session_id": unsupported_hook_session,
            "transcript_path": str(unsupported_hook_trace),
            "cwd": str(bundle),
            "hook_event_name": "SessionEnd",
            "model": "test-model",
            "reason": "other",
        },
        bundle_path=bundle,
        receipt_dir=unsupported_hook_receipts,
        probe_path=probe_path,
    )
    check(
        load_receipt(unsupported_hook_file)["serving"]["status"] == "verified",
        "unsupported-hook fixture did not reach verified state",
    )
    try:
        handle_codex_event(
            {
                "session_id": unsupported_hook_session,
                "hook_event_name": "UnsupportedFutureEvent",
            },
            bundle_path=bundle,
            receipt_dir=unsupported_hook_receipts,
            probe_path=probe_path,
        )
    except AttributionError:
        pass
    else:
        errors.append("unsupported hook event unexpectedly succeeded")
    unsupported_hook_marker = json.loads(
        unsupported_hook_file.read_text(encoding="utf-8")
    )
    check(
        unsupported_hook_marker.get("record_type") == "execution-attribution-pending"
        and unsupported_hook_marker.get("operation") == "codex-hook"
        and "serving" not in unsupported_hook_marker,
        "unsupported hook event retained stale verified serving",
    )

    for index, lifecycle_event in enumerate(("SessionStart", "SessionEnd"), 5):
        corrupt_session = f"019fe3d6-f66e-7873-9b80-91bc17d7b3e{index}"
        corrupt_receipts = temp / f"corrupt-{lifecycle_event.lower()}-receipts"
        corrupt_start = copy.deepcopy(start)
        corrupt_start["session_id"] = corrupt_session
        corrupt_file = handle_codex_event(
            corrupt_start,
            bundle_path=bundle,
            receipt_dir=corrupt_receipts,
            probe_path=probe_path,
        )
        corrupt_trace = temp / f"corrupt-{lifecycle_event.lower()}-session.jsonl"
        write_trace(
            corrupt_trace,
            session_id=corrupt_session,
            include_read=True,
            bundle=bundle,
        )
        corrupt_end = {
            "session_id": corrupt_session,
            "transcript_path": str(corrupt_trace),
            "cwd": str(bundle),
            "hook_event_name": "SessionEnd",
            "model": "test-model",
            "reason": "other",
        }
        handle_codex_event(
            corrupt_end,
            bundle_path=bundle,
            receipt_dir=corrupt_receipts,
            probe_path=probe_path,
        )
        corrupt_record = json.loads(corrupt_file.read_text(encoding="utf-8"))
        check(
            corrupt_record["serving"]["status"] == "verified",
            f"corrupt {lifecycle_event} fixture did not reach verified state",
        )
        corrupt_record["integrity"]["receipt_digest"] = "sha256:" + "0" * 64
        corrupt_file.write_text(json.dumps(corrupt_record), encoding="utf-8")
        failed_event = corrupt_start if lifecycle_event == "SessionStart" else corrupt_end
        try:
            handle_codex_event(
                failed_event,
                bundle_path=bundle,
                receipt_dir=corrupt_receipts,
                probe_path=probe_path,
            )
        except AttributionError:
            pass
        else:
            errors.append(f"corrupt receipt {lifecycle_event} unexpectedly succeeded")
        corrupt_marker = json.loads(corrupt_file.read_text(encoding="utf-8"))
        check(
            corrupt_marker.get("record_type") == "execution-attribution-pending"
            and corrupt_marker.get("operation") == "codex-hook"
            and "serving" not in corrupt_marker,
            f"corrupt receipt {lifecycle_event} retained stale verified serving",
        )

if errors:
    for error in errors:
        print(f"ERROR: {error}")
    raise SystemExit(1)

print(
    "EXECUTION ATTRIBUTION TESTS PASSED "
    "serving=verified activation=observed unknown=preserved privacy=minimal"
)
