from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Any

from build_runtime_bundle import BundleError, read_json, verify_bundle


ROOT = Path(__file__).resolve().parents[1]
PRODUCER = "agent-skills-neutral/execution-attribution"
MAX_FUTURE_CLOCK_SKEW = dt.timedelta(minutes=5)
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)
SAFE_TOKEN_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]{0,199}$")
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
READ_VERB_RE = re.compile(
    r"(?i)(?:get-content|select-string|\bcat\b|\btype\b|\bmore\b|"
    r"\.read_text\s*\(|\.read_bytes\s*\(|\bopen\s*\(|\brg\b)"
)
SKILL_PATH_RE = re.compile(
    r"(?i)(?:[A-Za-z]:)?[^\"'\r\n|;]{0,320}?skills[\\/]+"
    r"(?P<name>[A-Za-z0-9_.:-]+)[\\/]+SKILL\.md"
)
FAILURE_MARKERS = (
    "script failed",
    "script error",
    "exit code: 1",
    "exit code: 2",
    "no such file",
    "cannot find path",
    "指定されたファイルが見つかりません",
)
EXPLICIT_FAILURE_LINE_RE = re.compile(
    r"(?im)^\s*(?:(?:[A-Za-z]+)?error|(?:[A-Za-z]+)?exception|fatal|failed|failure)"
    r"(?:\s*[:=]|\b)"
)
INLINE_FAILURE_FIELD_RE = re.compile(
    r"(?i)(?:\b(?:(?:[A-Za-z]+)?error|(?:[A-Za-z]+)?exception|fatal|failed|failure)\b\s*[:=]|"
    r"\boutput\s*:\s*[^\r\n]{0,100}\b(?:error|exception|fatal|failed|failure)\b)"
)
PATH_PERMISSION_FAILURE_RE = re.compile(
    r"(?i)(?:\b(?:the\s+)?path\b[^\r\n]{0,100}\b(?:does not exist|not found|cannot be found)\b|"
    r"\b(?:file|path)\b[^\r\n]{0,60}\b(?:missing|not found)\b|"
    r"\bmissing\s+(?:file|path)\b|\bpermission(?:error| denied)\b|"
    r"\baccess(?:\s+is)?\s+denied\b|\baccessdenied\b|\bfilenotfounderror\b)"
)
NONZERO_EXIT_RE_LIST = (
    re.compile(r"(?i)\bexit\s+(?:code|status)\s*[:=]?\s*(-?\d+)\b"),
    re.compile(r"(?i)\b(?:process|command)\s+exited\s+with\s+(?:code|status)\s+(-?\d+)\b"),
    re.compile(r"(?i)\breturn(?:ed)?\s*(?:code)?\s*[:=]\s*(-?\d+)\b"),
    re.compile(r"(?i)\bstatus\s*[:=]\s*(-?\d+)\b"),
    re.compile(r"(?i)\bexitcode\s*[:=]\s*(-?\d+)\b"),
    re.compile(
        r"(?i)\b(?:process|command)[ -]?exit(?:ed)?(?:\s+with)?"
        r"(?:\s+(?:code|status))?\s*[:=]?\s*(-?\d+)\b"
    ),
    re.compile(r"(?i)\bstatus\s+(-?\d+)\b"),
    re.compile(r"(?i)\b(?:nonzero|rc|return[_ -]?status)\s*[:=]\s*(-?\d+)\b"),
)
SUCCESS_EXIT_RE_LIST = (
    re.compile(r"(?i)\bexit\s+(?:code|status)\s*[:=]?\s*0\b"),
    re.compile(r"(?i)\b(?:process|command)\s+exited\s+with\s+(?:code|status)\s+0\b"),
    re.compile(r"(?i)\breturn(?:ed)?\s*(?:code)?\s*[:=]\s*0\b"),
    re.compile(r"(?i)\bstatus\s*[:=]\s*0\b"),
    re.compile(r"(?i)\bexitcode\s*[:=]\s*0\b"),
)
SURFACE_NAMES = {"AGENTS.md", "runtime-catalog.json", "skills/*/SKILL.md"}
SURFACE_EVIDENCE_CODES = {
    "manifest_agents_artifact_verified",
    "manifest_runtime_catalog_available",
    "manifest_skill_bodies_available",
    "preflight_agents_prompt_visible",
    "preflight_runtime_catalog_prompt_visible",
    "actual_session_assignment_pending",
    "actual_session_agents_exact_match",
}
SERVING_EVIDENCE_CODES = {
    "legacy_trace_without_contemporaneous_bundle",
    "bundle_verification_failed",
    "bundle_at_session_cwd_assignment_pending",
    "preflight_matches_bundle",
    "preflight_bundle_mismatch",
    "session_cwd_bundle_path_mismatch",
    "bundle_reverification_failed",
    "bundle_path_omitted",
    "preflight_after_session_start",
    "world_state_agents_invalid",
    "world_state_assignment_mismatch",
    "trace_structure_unsupported",
    "world_state_assignments_match",
    "trace_incomplete",
    "explicit_trace_link_without_sessionstart",
    "resume_bundle_mismatch",
    "resume_requires_reverification",
    "sessionend_trace_missing",
}
MISMATCH_EVIDENCE_CODES = {
    "bundle_verification_failed",
    "preflight_bundle_mismatch",
    "session_cwd_bundle_path_mismatch",
    "bundle_reverification_failed",
    "preflight_after_session_start",
    "world_state_assignment_mismatch",
    "resume_bundle_mismatch",
}


class AttributionError(RuntimeError):
    pass


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def path_digest(path: str | Path) -> str:
    normalized = os.path.normcase(str(Path(path).expanduser().resolve())).replace("\\", "/")
    return f"sha256:{sha256_bytes(normalized.encode('utf-8'))}"


def opaque_identifier(value: str | None) -> str | None:
    if value is None:
        return None
    if UUID_RE.fullmatch(value):
        return value.lower()
    return f"sha256:{sha256_bytes(value.encode('utf-8'))}"


def safe_metadata_token(value: str | None) -> str | None:
    if value is None:
        return None
    if DIGEST_RE.fullmatch(value):
        return value
    if (
        SAFE_TOKEN_RE.fullmatch(value)
        and value not in {".", ".."}
        and not value.startswith(('/', '\\'))
        and not re.match(r"^[A-Za-z]:", value)
        and "\\" not in value
    ):
        return value
    return f"sha256:{sha256_bytes(value.encode('utf-8'))}"


def _require_opaque_identifier(value: Any, label: str, *, nullable: bool = False) -> None:
    if nullable and value is None:
        return
    if not isinstance(value, str) or not (UUID_RE.fullmatch(value) or DIGEST_RE.fullmatch(value)):
        raise AttributionError(f"{label} must be a UUID or opaque sha256 digest")


def _require_safe_metadata(value: Any, label: str, *, nullable: bool = False) -> None:
    if nullable and value is None:
        return
    if not isinstance(value, str) or safe_metadata_token(value) != value:
        raise AttributionError(f"{label} must be a bounded non-path token or sha256 digest")


def _require_repository_identity(value: Any, label: str) -> None:
    if not isinstance(value, str) or not re.fullmatch(
        r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", value
    ):
        raise AttributionError(f"{label} must be an owner/repository identity")
    if any(part in {".", ".."} for part in value.split("/")):
        raise AttributionError(f"{label} must not contain relative path components")


def _require_skill_name(value: Any, label: str) -> None:
    if not isinstance(value, str) or not SKILL_NAME_RE.fullmatch(value):
        raise AttributionError(f"{label} must be a canonical lowercase hyphenated Skill name")


def atomic_write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def mark_output_pending(path: Path, operation: str) -> None:
    if operation not in {"codex-probe", "codex-link", "codex-hook", "backfill"}:
        raise AttributionError("unsupported pending-output operation")
    atomic_write_json(
        path.expanduser().resolve(),
        {
            "schema_version": 1,
            "record_type": "execution-attribution-pending",
            "recorded_at": utc_now(),
            "producer": {"name": PRODUCER, "version": 1},
            "operation": operation,
            "status": "pending",
        },
    )


def load_receipt_for_lifecycle_update(path: Path) -> dict[str, Any]:
    resolved = path.expanduser().resolve()
    try:
        snapshot = resolved.read_bytes()
    except OSError:
        mark_output_pending(resolved, "codex-hook")
        raise
    mark_output_pending(resolved, "codex-hook")
    return load_receipt_bytes(snapshot)


def canonical_receipt_bytes(receipt: dict[str, Any]) -> bytes:
    value = copy.deepcopy(receipt)
    value.setdefault("integrity", {})["receipt_digest"] = None
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def seal_receipt(receipt: dict[str, Any]) -> dict[str, Any]:
    receipt.setdefault("integrity", {})["algorithm"] = "sha256"
    receipt["integrity"]["receipt_digest"] = (
        f"sha256:{sha256_bytes(canonical_receipt_bytes(receipt))}"
    )
    return receipt


def _require_exact_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    if actual != expected:
        raise AttributionError(
            f"{label} fields mismatch: missing={sorted(expected - actual)} "
            f"unexpected={sorted(actual - expected)}"
        )


def _require_digest(value: Any, label: str, *, nullable: bool = False) -> None:
    if nullable and value is None:
        return
    if not isinstance(value, str) or not DIGEST_RE.fullmatch(value):
        raise AttributionError(f"{label} must be a sha256 digest")


def validate_receipt(receipt: dict[str, Any], *, verify_integrity: bool = True) -> None:
    _require_exact_keys(
        receipt,
        {
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
        },
        "receipt",
    )
    if receipt.get("schema_version") != 1:
        raise AttributionError("unsupported receipt schema_version")
    if receipt.get("record_type") != "execution-attribution":
        raise AttributionError("unexpected receipt record_type")
    _require_opaque_identifier(receipt.get("receipt_id"), "receipt_id")
    if not isinstance(receipt.get("recorded_at"), str) or not receipt["recorded_at"]:
        raise AttributionError("recorded_at must be non-empty")
    receipt_timestamp = require_not_future(receipt["recorded_at"], "receipt recorded_at")

    producer = receipt.get("producer")
    if not isinstance(producer, dict):
        raise AttributionError("producer must be an object")
    _require_exact_keys(producer, {"name", "version"}, "producer")
    if producer.get("name") != PRODUCER or producer.get("version") != 1:
        raise AttributionError("producer identity/version mismatch")

    session = receipt.get("session")
    if not isinstance(session, dict):
        raise AttributionError("session must be an object")
    _require_exact_keys(
        session,
        {"id", "run_id", "source", "start_source", "cwd_digest", "trace"},
        "session",
    )
    _require_opaque_identifier(session.get("id"), "session.id", nullable=True)
    _require_opaque_identifier(session.get("run_id"), "session.run_id")
    _require_safe_metadata(session.get("source"), "session.source", nullable=True)
    _require_safe_metadata(session.get("start_source"), "session.start_source", nullable=True)
    _require_digest(session.get("cwd_digest"), "session.cwd_digest", nullable=True)
    trace = session.get("trace")
    if not isinstance(trace, dict):
        raise AttributionError("session.trace must be an object")
    _require_exact_keys(
        trace,
        {"status", "pointer", "content_digest", "bytes"},
        "session.trace",
    )
    if trace.get("status") not in {"unknown", "linked", "snapshot"}:
        raise AttributionError("session.trace.status is invalid")
    _require_digest(trace.get("pointer"), "session.trace.pointer", nullable=True)
    _require_digest(trace.get("content_digest"), "session.trace.content_digest", nullable=True)
    if trace.get("bytes") is not None and (
        not isinstance(trace.get("bytes"), int) or trace["bytes"] < 0
    ):
        raise AttributionError("session.trace.bytes must be a non-negative integer or null")

    runtime = receipt.get("runtime")
    if not isinstance(runtime, dict):
        raise AttributionError("runtime must be an object")
    _require_exact_keys(runtime, {"vendor", "name", "version", "model"}, "runtime")
    _require_safe_metadata(runtime.get("vendor"), "runtime.vendor")
    _require_safe_metadata(runtime.get("name"), "runtime.name")
    _require_safe_metadata(runtime.get("version"), "runtime.version", nullable=True)
    _require_safe_metadata(runtime.get("model"), "runtime.model", nullable=True)

    serving = receipt.get("serving")
    if not isinstance(serving, dict):
        raise AttributionError("serving must be an object")
    _require_exact_keys(
        serving,
        {"status", "evidence_strength", "bundle", "preflight", "surfaces", "evidence"},
        "serving",
    )
    if serving.get("status") not in {"verified", "unknown", "mismatch"}:
        raise AttributionError("serving.status is invalid")
    if serving.get("evidence_strength") not in {"direct", "strong", "limited", "unknown"}:
        raise AttributionError("serving.evidence_strength is invalid")
    bundle = serving.get("bundle")
    if bundle is not None:
        validate_bundle_identity(bundle)
    preflight = serving.get("preflight")
    if preflight is not None:
        if not isinstance(preflight, dict):
            raise AttributionError("serving.preflight must be an object or null")
        _require_exact_keys(
            preflight,
            {"status", "recorded_at", "record_digest"},
            "serving.preflight",
        )
        if preflight.get("status") not in {"matched", "mismatch"}:
            raise AttributionError("serving.preflight.status is invalid")
        if not isinstance(preflight.get("recorded_at"), str) or not preflight["recorded_at"]:
            raise AttributionError("serving.preflight.recorded_at must be non-empty")
        preflight_timestamp = parse_timestamp(
            preflight["recorded_at"], "serving.preflight.recorded_at"
        )
        if preflight_timestamp > receipt_timestamp:
            raise AttributionError("serving preflight cannot postdate the receipt")
        _require_digest(preflight.get("record_digest"), "serving.preflight.record_digest")
    if not isinstance(serving.get("surfaces"), list) or not all(
        isinstance(item, dict) for item in serving["surfaces"]
    ):
        raise AttributionError("serving.surfaces must be an object array")
    for item in serving["surfaces"]:
        _require_exact_keys(item, {"name", "status", "digest", "evidence"}, "serving surface")
        if item.get("name") not in SURFACE_NAMES:
            raise AttributionError("serving surface name is not allowlisted")
        if item.get("status") not in {
            "observed_prompt_visible",
            "preflight_prompt_visible",
            "artifact_verified",
            "available_on_demand",
            "unknown",
        }:
            raise AttributionError("serving surface status is invalid")
        _require_digest(item.get("digest"), "serving surface digest", nullable=True)
        if item.get("evidence") not in SURFACE_EVIDENCE_CODES:
            raise AttributionError("serving surface evidence is not allowlisted")
    if not isinstance(serving.get("evidence"), list) or not serving["evidence"] or not all(
        item in SERVING_EVIDENCE_CODES for item in serving["evidence"]
    ):
        raise AttributionError("serving.evidence must contain only allowlisted codes")
    if len(serving["evidence"]) != len(set(serving["evidence"])):
        raise AttributionError("serving.evidence must not contain duplicates")
    mismatch_evidence = set(serving["evidence"]) & MISMATCH_EVIDENCE_CODES
    if serving.get("status") == "mismatch" and not mismatch_evidence:
        raise AttributionError("mismatch serving requires a concrete mismatch evidence code")
    if serving.get("status") != "mismatch" and mismatch_evidence:
        raise AttributionError("non-mismatch serving cannot retain mismatch evidence codes")
    if serving.get("status") == "verified":
        if not isinstance(bundle, dict) or serving.get("evidence_strength") != "direct":
            raise AttributionError("verified serving requires a bundle and direct evidence")
        if "world_state_assignments_match" not in serving["evidence"]:
            raise AttributionError("verified serving requires exact world_state evidence")
        agents_surfaces = [
            item
            for item in serving["surfaces"]
            if item.get("name") == "AGENTS.md"
            and item.get("status") == "observed_prompt_visible"
            and item.get("evidence") == "actual_session_agents_exact_match"
            and item.get("digest") == bundle.get("agents_digest")
        ]
        if not agents_surfaces:
            raise AttributionError("verified serving requires actual-session AGENTS.md evidence")
        if trace.get("status") != "linked":
            raise AttributionError("verified serving requires a linked terminal trace")
        _require_digest(trace.get("pointer"), "verified serving trace.pointer")
        _require_digest(trace.get("content_digest"), "verified serving trace.content_digest")
        if not isinstance(trace.get("bytes"), int) or trace["bytes"] <= 0:
            raise AttributionError("verified serving requires a non-empty trace snapshot")
        if {"trace_incomplete", "trace_structure_unsupported"} & set(serving["evidence"]):
            raise AttributionError("verified serving cannot retain incomplete trace evidence")

    activation = receipt.get("activation")
    if not isinstance(activation, dict):
        raise AttributionError("activation must be an object")
    _require_exact_keys(
        activation,
        {"status", "evidence_scope", "observed_skills", "adoption_claim"},
        "activation",
    )
    if activation.get("status") not in {"observed_skill_content", "none_observed", "unknown"}:
        raise AttributionError("activation.status is invalid")
    if activation.get("evidence_scope") not in {
        "complete_trace_snapshot",
        "partial_trace_snapshot",
        "none",
    }:
        raise AttributionError("activation.evidence_scope is invalid")
    if activation.get("adoption_claim") != "unknown":
        raise AttributionError("activation.adoption_claim must remain unknown")
    if not isinstance(activation.get("observed_skills"), list):
        raise AttributionError("activation.observed_skills must be an array")
    for item in activation["observed_skills"]:
        validate_activation_item(item)
    observed_names = [item["name"] for item in activation["observed_skills"]]
    if len(observed_names) != len(set(observed_names)):
        raise AttributionError("activation observed_skills contains duplicates")
    if bool(observed_names) != (activation.get("status") == "observed_skill_content"):
        raise AttributionError("activation status and observed_skills disagree")
    if activation.get("status") == "observed_skill_content" and (
        activation.get("evidence_scope")
        not in {"partial_trace_snapshot", "complete_trace_snapshot"}
    ):
        raise AttributionError("observed Skill content requires trace snapshot evidence")
    if activation.get("status") == "none_observed" and (
        activation.get("evidence_scope") != "complete_trace_snapshot"
    ):
        raise AttributionError("none_observed requires a complete trace snapshot")
    if activation.get("status") == "none_observed" and trace.get("status") != "linked":
        raise AttributionError("none_observed requires a linked terminal trace")
    if activation.get("status") != "unknown" and serving.get("status") != "verified":
        raise AttributionError("definite activation evidence requires verified serving")
    if activation.get("status") == "observed_skill_content" and not isinstance(bundle, dict):
        raise AttributionError("observed Skill content requires a served bundle identity")
    if isinstance(bundle, dict):
        for item in activation["observed_skills"]:
            name = item["name"]
            if name not in bundle["skill_digests"]:
                raise AttributionError("observed Skill is absent from the served bundle")

    privacy = receipt.get("privacy")
    if not isinstance(privacy, dict):
        raise AttributionError("privacy must be an object")
    _require_exact_keys(
        privacy,
        {
            "prompts_copied",
            "responses_copied",
            "source_content_copied",
            "tool_payloads_copied",
            "trace_content_copied",
            "absolute_paths_stored",
        },
        "privacy",
    )
    if any(privacy.get(field) is not False for field in privacy):
        raise AttributionError("receipt violates the minimal privacy contract")

    integrity = receipt.get("integrity")
    if not isinstance(integrity, dict):
        raise AttributionError("integrity must be an object")
    _require_exact_keys(integrity, {"algorithm", "receipt_digest"}, "integrity")
    if integrity.get("algorithm") != "sha256":
        raise AttributionError("integrity algorithm mismatch")
    _require_digest(integrity.get("receipt_digest"), "integrity.receipt_digest")
    if verify_integrity:
        expected = f"sha256:{sha256_bytes(canonical_receipt_bytes(receipt))}"
        if integrity.get("receipt_digest") != expected:
            raise AttributionError("receipt integrity digest mismatch")


def validate_bundle_identity(bundle: dict[str, Any]) -> None:
    _require_exact_keys(
        bundle,
        {
            "source_repository",
            "source_commit",
            "source_dirty",
            "manifest_digest",
            "catalog_digest",
            "runtime_catalog_digest",
            "agents_digest",
            "path_digest",
            "skill_digests",
        },
        "serving.bundle",
    )
    _require_repository_identity(bundle.get("source_repository"), "bundle.source_repository")
    if not isinstance(bundle.get("source_commit"), str) or not re.fullmatch(
        r"[0-9a-f]{40}", bundle["source_commit"]
    ):
        raise AttributionError("bundle source_commit is invalid")
    if not isinstance(bundle.get("source_dirty"), bool):
        raise AttributionError("bundle source_dirty must be boolean")
    for field in (
        "manifest_digest",
        "catalog_digest",
        "runtime_catalog_digest",
        "agents_digest",
        "path_digest",
    ):
        _require_digest(bundle.get(field), f"bundle.{field}")
    digests = bundle.get("skill_digests")
    if not isinstance(digests, dict) or not digests:
        raise AttributionError("bundle.skill_digests must be a non-empty object")
    for name, digest in digests.items():
        _require_skill_name(name, "bundle Skill name")
        _require_digest(digest, f"bundle.skill_digests[{name}]")


def validate_activation_item(item: Any) -> None:
    if not isinstance(item, dict):
        raise AttributionError("activation item must be an object")
    _require_exact_keys(
        item,
        {"name", "evidence_kind", "trace_line", "tool", "call_id_digest", "successful_output", "adoption"},
        "activation item",
    )
    _require_skill_name(item.get("name"), "activation item name")
    if item.get("evidence_kind") != "successful_tool_content_match":
        raise AttributionError("activation evidence_kind is invalid")
    if not isinstance(item.get("trace_line"), int) or item["trace_line"] <= 0:
        raise AttributionError("activation trace_line must be positive")
    _require_safe_metadata(item.get("tool"), "activation item tool")
    _require_digest(item.get("call_id_digest"), "activation call_id_digest")
    if item.get("successful_output") is not True or item.get("adoption") != "unknown":
        raise AttributionError("activation evidence may prove read, never adoption")


def load_receipt(path: Path) -> dict[str, Any]:
    value = read_json(path)
    validate_receipt(value)
    return value


def load_receipt_bytes(data: bytes) -> dict[str, Any]:
    try:
        value = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AttributionError("receipt snapshot is not valid UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise AttributionError("receipt snapshot must be an object")
    validate_receipt(value)
    return value


def manifest_file_entry(manifest: dict[str, Any], relative: str) -> dict[str, Any]:
    for item in manifest.get("files", []):
        if isinstance(item, dict) and item.get("path") == relative:
            return item
    raise AttributionError(f"manifest does not contain {relative}")


def bundle_identity(bundle_path: Path) -> dict[str, Any]:
    bundle_path = bundle_path.expanduser().resolve()
    verify_bundle(bundle_path)
    manifest_path = bundle_path / "MANIFEST.json"
    manifest = read_json(manifest_path)
    agents_entry = manifest_file_entry(manifest, "AGENTS.md")
    skill_items = manifest.get("skills", [])
    names = sorted(str(item["name"]) for item in skill_items)
    skill_digests = {str(item["name"]): str(item["digest"]) for item in skill_items}
    return {
        "source_repository": manifest["source_repository"],
        "source_commit": manifest["source_commit"],
        "source_dirty": manifest["source_dirty"],
        "manifest_digest": f"sha256:{sha256_file(manifest_path)}",
        "catalog_digest": manifest["catalog_digest"],
        "runtime_catalog_digest": manifest["runtime_catalog_digest"],
        "agents_digest": f"sha256:{agents_entry['sha256']}",
        "path_digest": path_digest(bundle_path),
        "skill_digests": {name: skill_digests[name] for name in names},
    }


def empty_trace() -> dict[str, Any]:
    return {"status": "unknown", "pointer": None, "content_digest": None, "bytes": None}


def privacy_contract() -> dict[str, bool]:
    return {
        "prompts_copied": False,
        "responses_copied": False,
        "source_content_copied": False,
        "tool_payloads_copied": False,
        "trace_content_copied": False,
        "absolute_paths_stored": False,
    }


def new_receipt(
    *,
    session_id: str | None,
    run_id: str,
    source: str | None,
    start_source: str | None,
    cwd: str | None,
    runtime_vendor: str,
    runtime_name: str,
    runtime_version: str | None,
    model: str | None,
    serving: dict[str, Any],
) -> dict[str, Any]:
    receipt = {
        "schema_version": 1,
        "record_type": "execution-attribution",
        "receipt_id": str(uuid.uuid4()),
        "recorded_at": utc_now(),
        "producer": {"name": PRODUCER, "version": 1},
        "session": {
            "id": opaque_identifier(session_id),
            "run_id": opaque_identifier(run_id),
            "source": safe_metadata_token(source),
            "start_source": safe_metadata_token(start_source),
            "cwd_digest": path_digest(cwd) if cwd else None,
            "trace": empty_trace(),
        },
        "runtime": {
            "vendor": safe_metadata_token(runtime_vendor),
            "name": safe_metadata_token(runtime_name),
            "version": safe_metadata_token(runtime_version),
            "model": safe_metadata_token(model),
        },
        "serving": serving,
        "activation": {
            "status": "unknown",
            "evidence_scope": "none",
            "observed_skills": [],
            "adoption_claim": "unknown",
        },
        "privacy": privacy_contract(),
        "integrity": {"algorithm": "sha256", "receipt_digest": None},
    }
    seal_receipt(receipt)
    validate_receipt(receipt)
    return receipt


def unknown_serving(reason: str) -> dict[str, Any]:
    if reason not in SERVING_EVIDENCE_CODES:
        raise AttributionError("unknown serving reason is not allowlisted")
    return {
        "status": "unknown",
        "evidence_strength": "unknown",
        "bundle": None,
        "preflight": None,
        "surfaces": [],
        "evidence": [reason],
    }


def serving_from_bundle(
    bundle_path: Path,
    *,
    cwd: str | None,
    probe: dict[str, Any] | None,
) -> dict[str, Any]:
    try:
        identity = bundle_identity(bundle_path)
    except (AttributionError, BundleError, OSError, ValueError):
        return {
            "status": "mismatch",
            "evidence_strength": "limited",
            "bundle": None,
            "preflight": None,
            "surfaces": [],
            "evidence": ["bundle_verification_failed"],
        }

    cwd_matches = cwd is not None and path_digest(cwd) == identity["path_digest"]
    surfaces = [
        {
            "name": "AGENTS.md",
            "status": "artifact_verified",
            "digest": identity["agents_digest"],
            "evidence": "manifest_agents_artifact_verified",
        },
        {
            "name": "runtime-catalog.json",
            "status": "available_on_demand",
            "digest": identity["runtime_catalog_digest"],
            "evidence": "manifest_runtime_catalog_available",
        },
        {
            "name": "skills/*/SKILL.md",
            "status": "available_on_demand",
            "digest": None,
            "evidence": "manifest_skill_bodies_available",
        },
    ]
    evidence = ["bundle_at_session_cwd_assignment_pending"]
    strength = "limited"
    preflight_mismatch = False
    preflight_evidence: dict[str, Any] | None = None
    if probe is not None:
        probe_valid = (
            probe.get("schema_version") == 1
            and probe.get("record_type") == "codex-serving-preflight"
            and probe.get("bundle", {}).get("manifest_digest") == identity["manifest_digest"]
            and probe.get("bundle", {}).get("path_digest") == identity["path_digest"]
            and probe.get("agents_prompt_visible") is True
            and probe.get("privacy", {}).get("prompt_content_stored") is False
        )
        if probe_valid:
            surfaces[0]["status"] = "preflight_prompt_visible"
            surfaces[0]["evidence"] = "preflight_agents_prompt_visible"
            if probe.get("runtime_catalog_prompt_visible") is True:
                surfaces[1]["status"] = "preflight_prompt_visible"
                surfaces[1]["evidence"] = "preflight_runtime_catalog_prompt_visible"
            evidence.append("preflight_matches_bundle")
            strength = "strong"
            preflight_evidence = {
                "status": "matched",
                "recorded_at": probe["recorded_at"],
                "record_digest": probe["integrity"]["record_digest"],
            }
        else:
            evidence.append("preflight_bundle_mismatch")
            preflight_mismatch = True
            preflight_evidence = {
                "status": "mismatch",
                "recorded_at": probe["recorded_at"],
                "record_digest": probe["integrity"]["record_digest"],
            }

    return {
        "status": "unknown" if cwd_matches and not preflight_mismatch else "mismatch",
        "evidence_strength": strength if cwd_matches else "limited",
        "bundle": identity,
        "preflight": preflight_evidence,
        "surfaces": surfaces,
        "evidence": evidence
        if cwd_matches
        else evidence
        + (
            ["session_cwd_bundle_path_mismatch"]
            if not cwd_matches
            else []
        ),
    }


def load_probe(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    value = read_json(path.expanduser().resolve())
    validate_probe(value)
    return value


def canonical_probe_bytes(probe: dict[str, Any]) -> bytes:
    value = copy.deepcopy(probe)
    value.setdefault("integrity", {})["record_digest"] = None
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def seal_probe(probe: dict[str, Any]) -> dict[str, Any]:
    probe.setdefault("integrity", {})["algorithm"] = "sha256"
    probe["integrity"]["record_digest"] = (
        f"sha256:{sha256_bytes(canonical_probe_bytes(probe))}"
    )
    return probe


def parse_timestamp(value: str, label: str) -> dt.datetime:
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise AttributionError(f"{label} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise AttributionError(f"{label} must include a timezone")
    return parsed


def require_not_future(value: str, label: str) -> dt.datetime:
    parsed = parse_timestamp(value, label)
    if parsed > dt.datetime.now(dt.timezone.utc) + MAX_FUTURE_CLOCK_SKEW:
        raise AttributionError(f"{label} cannot be in the future")
    return parsed


def validate_probe(probe: dict[str, Any]) -> None:
    _require_exact_keys(
        probe,
        {
            "schema_version",
            "record_type",
            "probe_id",
            "recorded_at",
            "runtime",
            "bundle",
            "prompt_input_digest",
            "agents_prompt_visible",
            "runtime_catalog_prompt_visible",
            "privacy",
            "integrity",
        },
        "Codex serving preflight",
    )
    if probe.get("schema_version") != 1 or probe.get("record_type") != "codex-serving-preflight":
        raise AttributionError("serving preflight identity/version mismatch")
    _require_opaque_identifier(probe.get("probe_id"), "serving preflight probe_id")
    if not isinstance(probe.get("recorded_at"), str):
        raise AttributionError("serving preflight recorded_at must be a string")
    require_not_future(probe["recorded_at"], "serving preflight recorded_at")
    runtime = probe.get("runtime")
    if not isinstance(runtime, dict):
        raise AttributionError("serving preflight runtime must be an object")
    _require_exact_keys(runtime, {"vendor", "name", "version", "command_digest"}, "preflight runtime")
    _require_safe_metadata(runtime.get("vendor"), "preflight runtime.vendor")
    _require_safe_metadata(runtime.get("name"), "preflight runtime.name")
    _require_safe_metadata(runtime.get("version"), "preflight runtime.version", nullable=True)
    _require_digest(runtime.get("command_digest"), "preflight runtime.command_digest")
    bundle = probe.get("bundle")
    if not isinstance(bundle, dict):
        raise AttributionError("serving preflight bundle must be an object")
    _require_exact_keys(
        bundle,
        {"manifest_digest", "path_digest", "agents_digest", "runtime_catalog_digest"},
        "preflight bundle",
    )
    for field in bundle:
        _require_digest(bundle[field], f"preflight bundle.{field}")
    _require_digest(probe.get("prompt_input_digest"), "preflight prompt_input_digest")
    if probe.get("agents_prompt_visible") is not True:
        raise AttributionError(
            "serving preflight must observe an isolated exact runtime AGENTS.md block"
        )
    if not isinstance(probe.get("runtime_catalog_prompt_visible"), bool):
        raise AttributionError("serving preflight runtime_catalog_prompt_visible must be boolean")
    privacy = probe.get("privacy")
    if not isinstance(privacy, dict):
        raise AttributionError("serving preflight privacy must be an object")
    _require_exact_keys(
        privacy,
        {"prompt_content_stored", "response_content_stored", "source_content_stored"},
        "preflight privacy",
    )
    if any(value is not False for value in privacy.values()):
        raise AttributionError("serving preflight violates privacy contract")
    integrity = probe.get("integrity")
    if not isinstance(integrity, dict):
        raise AttributionError("serving preflight integrity must be an object")
    _require_exact_keys(integrity, {"algorithm", "record_digest"}, "preflight integrity")
    if integrity.get("algorithm") != "sha256":
        raise AttributionError("serving preflight integrity algorithm mismatch")
    _require_digest(integrity.get("record_digest"), "preflight integrity.record_digest")
    expected = f"sha256:{sha256_bytes(canonical_probe_bytes(probe))}"
    if integrity.get("record_digest") != expected:
        raise AttributionError("serving preflight integrity digest mismatch")


def safe_receipt_filename(session_id: str) -> str:
    opaque = opaque_identifier(session_id)
    if opaque is None:
        raise AttributionError("session id is required")
    return f"{opaque.replace(':', '-')}.json"


def receipt_path(receipt_dir: Path, session_id: str) -> Path:
    return receipt_dir.expanduser().resolve() / safe_receipt_filename(session_id)


def _payload_text(payload: dict[str, Any]) -> str:
    values: list[str] = []
    for key in ("arguments", "input", "command"):
        value = payload.get(key)
        if isinstance(value, str):
            values.append(value)
    return "\n".join(values)


def _output_segments(payload: dict[str, Any]) -> tuple[list[str], bool]:
    value = payload.get("output")
    if not isinstance(value, list):
        return [], False
    segments: list[str] = []
    for item in value:
        if (
            not isinstance(item, dict)
            or item.get("type") != "input_text"
            or not isinstance(item.get("text"), str)
        ):
            return [], False
        segments.append(item["text"])
    return segments, True


def _supported_event_message(payload: dict[str, Any]) -> bool:
    event_type = payload.get("type")
    if event_type == "mcp_tool_call_end":
        return (
            set(payload) == {"type", "call_id", "invocation", "duration", "result"}
            and isinstance(payload.get("call_id"), str)
            and isinstance(payload.get("invocation"), dict)
            and isinstance(payload.get("duration"), dict)
            and isinstance(payload.get("result"), dict)
        )
    if event_type == "web_search_end":
        return (
            set(payload) == {"type", "call_id", "query", "action", "results"}
            and isinstance(payload.get("call_id"), str)
            and isinstance(payload.get("query"), str)
            and isinstance(payload.get("action"), dict)
            and isinstance(payload.get("results"), list)
        )
    return True


def _supported_non_tool_response(payload: dict[str, Any]) -> bool:
    response_type = payload.get("type")
    if response_type == "message":
        content = payload.get("content")
        return isinstance(content, list) and all(
            isinstance(item, dict)
            and item.get("type") in {"input_text", "output_text"}
            and isinstance(item.get("text"), str)
            for item in content
        )
    if response_type == "reasoning":
        summary = payload.get("summary")
        return isinstance(summary, list) and all(
            isinstance(item, dict)
            and item.get("type") == "summary_text"
            and isinstance(item.get("text"), str)
            for item in summary
        )
    return True


def _supported_tool_response(payload: dict[str, Any]) -> bool:
    response_type = payload.get("type")
    metadata = payload.get("internal_chat_message_metadata_passthrough")
    if metadata is not None and (
        not isinstance(metadata, dict)
        or set(metadata) != {"turn_id"}
        or not isinstance(metadata.get("turn_id"), str)
    ):
        return False
    if "id" in payload and not isinstance(payload.get("id"), str):
        return False
    common_optional = {"id", "internal_chat_message_metadata_passthrough"}
    if response_type == "custom_tool_call":
        allowed = {"type", "call_id", "name", "input", "status"} | common_optional
        return (
            set(payload) <= allowed
            and {"type", "call_id", "name", "input"} <= set(payload)
            and payload.get("status") in {None, "completed"}
        )
    if response_type == "function_call":
        allowed = {"type", "call_id", "name", "arguments", "status"} | common_optional
        return (
            set(payload) <= allowed
            and {"type", "call_id", "name", "arguments"} <= set(payload)
            and payload.get("status") in {None, "completed"}
        )
    if response_type in {"custom_tool_call_output", "function_call_output"}:
        allowed = {"type", "call_id", "output"} | common_optional
        return set(payload) <= allowed and {"type", "call_id", "output"} <= set(payload)
    return True


def _successful_output(text: str) -> bool:
    lowered = text.lower()
    if not text or any(marker in lowered for marker in FAILURE_MARKERS):
        return False
    if any(marker in lowered for marker in ("permission denied", "access is denied")):
        return False
    if EXPLICIT_FAILURE_LINE_RE.search(text):
        return False
    if INLINE_FAILURE_FIELD_RE.search(text):
        return False
    if PATH_PERMISSION_FAILURE_RE.search(text):
        return False
    for pattern in NONZERO_EXIT_RE_LIST:
        if any(int(code) != 0 for code in pattern.findall(text)):
            return False
    compact = re.sub(r"\s+", "", text)
    compact_codes = re.findall(
        r"(?i)(?:nonzero|rc|return[_-]?status|process-?exit)[:=](-?\d+)\b",
        compact,
    )
    if any(int(code) != 0 for code in compact_codes):
        return False
    return any(pattern.search(text) for pattern in SUCCESS_EXIT_RE_LIST)


def _is_read_call(text: str) -> bool:
    lowered = text.lower()
    if "*** begin patch" in lowered or "apply_patch" in lowered:
        return False
    if "rg --files" in lowered and not re.search(r"(?i)\brg\b(?!\s+--files)", text):
        return False
    return READ_VERB_RE.search(text) is not None


def scan_codex_trace(
    trace_path: Path,
    *,
    bundle: dict[str, Any] | None,
    bundle_path: Path | None = None,
    complete: bool,
    trace_bytes: bytes | None = None,
) -> dict[str, Any]:
    calls: dict[str, dict[str, Any]] = {}
    outputs: dict[str, list[str]] = {}
    invalid_call_ids: set[str] = set()
    metadata: dict[str, Any] = {}
    models: set[str] = set()
    agents_observations: list[dict[str, Any]] = []
    session_meta_records = 0
    session_timestamp_valid = False
    line_count = 0
    parse_errors = 0
    terminal_task_complete_line: int | None = None
    last_relevant_line: int | None = None
    last_record_line: int | None = None
    invalid_world_state_records = 0
    unsupported_records = 0
    allowed_record_types = {
        "session_meta",
        "turn_context",
        "world_state",
        "response_item",
        "event_msg",
    }
    allowed_event_types = {
        "user_message",
        "agent_message",
        "task_started",
        "token_count",
        "task_complete",
        "mcp_tool_call_end",
        "web_search_end",
    }
    allowed_response_types = {
        "message",
        "reasoning",
        "function_call",
        "function_call_output",
        "custom_tool_call",
        "custom_tool_call_output",
    }
    snapshot = trace_bytes if trace_bytes is not None else trace_path.read_bytes()
    try:
        trace_text = snapshot.decode("utf-8")
    except UnicodeDecodeError:
        trace_text = ""
        parse_errors += 1
    for line_count, line in enumerate(trace_text.splitlines(), 1):
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                parse_errors += 1
                continue
            if not isinstance(item, dict):
                parse_errors += 1
                continue
            last_record_line = line_count
            record_type = item.get("type")
            payload = item.get("payload")
            if record_type == "world_state" and not isinstance(payload, dict):
                invalid_world_state_records += 1
                unsupported_records += 1
                continue
            if not isinstance(payload, dict):
                unsupported_records += 1
                continue
            if record_type not in allowed_record_types:
                unsupported_records += 1
                continue
            if record_type == "event_msg" and payload.get("type") not in allowed_event_types:
                unsupported_records += 1
                continue
            if record_type == "event_msg" and not _supported_event_message(payload):
                unsupported_records += 1
                continue
            if record_type == "response_item" and payload.get("type") not in allowed_response_types:
                unsupported_records += 1
                continue
            if record_type == "response_item" and not _supported_non_tool_response(payload):
                unsupported_records += 1
                continue
            if record_type == "response_item" and not _supported_tool_response(payload):
                unsupported_records += 1
                continue
            if terminal_task_complete_line is not None:
                unsupported_records += 1
                continue
            if record_type != "session_meta" and session_meta_records == 0:
                unsupported_records += 1
                continue
            if record_type == "session_meta":
                session_meta_records += 1
                if session_meta_records == 1 and isinstance(payload.get("id"), str):
                    metadata = {
                        key: payload.get(key)
                        for key in ("id", "timestamp", "cwd", "cli_version", "source", "originator")
                    }
                    timestamp = metadata.get("timestamp")
                    if isinstance(timestamp, str):
                        try:
                            require_not_future(timestamp, "Codex session timestamp")
                        except AttributionError:
                            unsupported_records += 1
                        else:
                            session_timestamp_valid = True
                    else:
                        unsupported_records += 1
                else:
                    unsupported_records += 1
            elif record_type == "turn_context":
                last_relevant_line = line_count
                raw_model = payload.get("model")
                if isinstance(raw_model, str):
                    models.add(raw_model)
            elif record_type == "world_state":
                last_relevant_line = line_count
                state = payload.get("state")
                agents_md = state.get("agents_md") if isinstance(state, dict) else None
                if isinstance(agents_md, dict):
                    directory = agents_md.get("directory")
                    text = agents_md.get("text")
                    if isinstance(directory, str) and isinstance(text, str):
                        agents_observations.append({
                            "directory_digest": path_digest(directory),
                            "text_digest": f"sha256:{sha256_bytes(text.encode('utf-8'))}",
                        })
                    else:
                        invalid_world_state_records += 1
                        unsupported_records += 1
                else:
                    invalid_world_state_records += 1
                    unsupported_records += 1
            elif record_type == "event_msg" and payload.get("type") == "task_complete":
                terminal_task_complete_line = line_count
                last_relevant_line = line_count
            elif record_type == "event_msg" and payload.get("type") in {
                "user_message",
                "agent_message",
            }:
                last_relevant_line = line_count
            elif record_type == "response_item":
                last_relevant_line = line_count
                response_type = payload.get("type")
                call_id = payload.get("call_id")
                if response_type in {"function_call", "custom_tool_call"}:
                    call_text = _payload_text(payload)
                    if (
                        not isinstance(call_id, str)
                        or not call_text
                        or call_id in calls
                        or call_id in outputs
                        or call_id in invalid_call_ids
                    ):
                        unsupported_records += 1
                        if isinstance(call_id, str):
                            invalid_call_ids.add(call_id)
                            calls.pop(call_id, None)
                            outputs.pop(call_id, None)
                    else:
                        calls[call_id] = {
                            "line": line_count,
                            "tool": str(payload.get("name") or response_type),
                            "text": call_text,
                        }
                elif response_type in {"function_call_output", "custom_tool_call_output"}:
                    if (
                        not isinstance(call_id, str)
                        or call_id not in calls
                        or call_id in outputs
                        or call_id in invalid_call_ids
                    ):
                        unsupported_records += 1
                        if isinstance(call_id, str):
                            invalid_call_ids.add(call_id)
                            calls.pop(call_id, None)
                            outputs.pop(call_id, None)
                    else:
                        output_segments, supported_output = _output_segments(payload)
                        if not supported_output:
                            unsupported_records += 1
                            invalid_call_ids.add(call_id)
                            calls.pop(call_id, None)
                            outputs.pop(call_id, None)
                        else:
                            outputs[call_id] = output_segments

    dangling_call_ids = set(calls) - set(outputs)
    if dangling_call_ids:
        unsupported_records += len(dangling_call_ids)
        invalid_call_ids.update(dangling_call_ids)
    session_identity_valid = bool(
        session_meta_records == 1
        and isinstance(metadata.get("id"), str)
        and session_timestamp_valid
    )
    if not session_identity_valid:
        calls = {}
        outputs = {}
        agents_observations = []
    model = next(iter(models)) if session_identity_valid and len(models) == 1 else None
    effective_complete = bool(
        complete
        and parse_errors == 0
        and unsupported_records == 0
        and session_identity_valid
        and terminal_task_complete_line is not None
        and terminal_task_complete_line == last_relevant_line
        and terminal_task_complete_line == last_record_line
    )
    bundle_names = set(bundle.get("skill_digests", {})) if bundle else set()
    observed: dict[str, dict[str, Any]] = {}
    for call_id, call in calls.items():
        if call_id in invalid_call_ids:
            continue
        text = call["text"]
        if not _is_read_call(text):
            continue
        output_segments = outputs.get(call_id, [])
        for match in SKILL_PATH_RE.finditer(text):
            name = match.group("name")
            if bundle is not None and name not in bundle_names:
                continue
            if bundle_path is None:
                continue
            skill_path = bundle_path / "skills" / name / "SKILL.md"
            try:
                skill_body = normalize_text(skill_path.read_text(encoding="utf-8")).strip()
            except OSError:
                continue
            normalized_segments = [normalize_text(segment) for segment in output_segments]
            if not skill_body or not any(skill_body in segment for segment in normalized_segments):
                continue
            envelope_segments: list[str] = []
            body_removed = False
            for segment in normalized_segments:
                if not body_removed and skill_body in segment:
                    segment = segment.replace(skill_body, "", 1)
                    body_removed = True
                envelope_segments.append(segment)
            if not _successful_output("\n".join(envelope_segments)):
                continue
            observed.setdefault(
                name,
                {
                    "name": name,
                    "evidence_kind": "successful_tool_content_match",
                    "trace_line": call["line"],
                    "tool": safe_metadata_token(call["tool"]),
                    "call_id_digest": f"sha256:{sha256_bytes(call_id.encode('utf-8'))}",
                    "successful_output": True,
                    "adoption": "unknown",
                },
            )

    if observed:
        status = "observed_skill_content"
    elif effective_complete and bundle is not None:
        status = "none_observed"
    else:
        status = "unknown"
    return {
        "metadata": metadata,
        "model": model,
        "agents_observations": agents_observations,
        "session_meta_records": session_meta_records,
        "invalid_world_state_records": invalid_world_state_records,
        "unsupported_records": unsupported_records,
        "line_count": line_count,
        "parse_errors": parse_errors,
        "terminal_task_complete": terminal_task_complete_line is not None,
        "complete": effective_complete,
        "activation": {
            "status": status,
            "evidence_scope": (
                "complete_trace_snapshot" if effective_complete else "partial_trace_snapshot"
            ),
            "observed_skills": [observed[name] for name in sorted(observed)],
            "adoption_claim": "unknown",
        },
    }


TRACE_EVIDENCE_CODES = {
    "bundle_reverification_failed",
    "bundle_path_omitted",
    "preflight_after_session_start",
    "world_state_agents_invalid",
    "world_state_assignment_mismatch",
    "trace_structure_unsupported",
    "world_state_assignments_match",
    "trace_incomplete",
    "sessionend_trace_missing",
    "session_cwd_bundle_path_mismatch",
}


def reset_trace_derived_state(receipt: dict[str, Any]) -> None:
    serving = receipt["serving"]
    preflight = serving.get("preflight")
    persistent_resume_mismatch = "resume_bundle_mismatch" in serving.get("evidence", [])
    if isinstance(serving.get("bundle"), dict):
        serving["status"] = (
            "mismatch"
            if persistent_resume_mismatch
            or (isinstance(preflight, dict) and preflight.get("status") == "mismatch")
            else "unknown"
        )
        serving["evidence_strength"] = (
            "direct"
            if persistent_resume_mismatch
            else (
                "strong"
                if isinstance(preflight, dict) and preflight.get("status") == "matched"
                else "limited"
            )
        )
    serving["evidence"] = [
        evidence
        for evidence in serving["evidence"]
        if evidence not in TRACE_EVIDENCE_CODES
    ]
    for surface in serving["surfaces"]:
        if surface.get("name") == "AGENTS.md":
            if isinstance(preflight, dict) and preflight.get("status") == "matched":
                surface["status"] = "preflight_prompt_visible"
                surface["evidence"] = "actual_session_assignment_pending"
            else:
                surface["status"] = "artifact_verified"
                surface["evidence"] = "actual_session_assignment_pending"
    receipt["activation"] = {
        "status": "unknown",
        "evidence_scope": "none",
        "observed_skills": [],
        "adoption_claim": "unknown",
    }
    receipt["session"]["trace"] = empty_trace()


def attach_trace(
    receipt: dict[str, Any],
    trace_path: Path,
    *,
    bundle_path: Path | None = None,
    complete: bool,
    trace_bytes: bytes | None = None,
) -> dict[str, Any]:
    trace_path = trace_path.expanduser().resolve()
    if not trace_path.is_file():
        raise AttributionError("Codex transcript path is missing")
    snapshot = trace_bytes if trace_bytes is not None else trace_path.read_bytes()
    bundle = receipt.get("serving", {}).get("bundle")
    preflight = receipt["serving"].get("preflight")
    reset_trace_derived_state(receipt)
    scan_bundle: dict[str, Any] | None = None
    resolved_bundle_path: Path | None = None
    bundle_identity_matches = False
    if isinstance(bundle, dict) and bundle_path is not None:
        resolved_bundle_path = bundle_path.expanduser().resolve()
        try:
            current_identity = bundle_identity(resolved_bundle_path)
        except (AttributionError, BundleError, OSError, ValueError):
            current_identity = None
        if current_identity == bundle:
            bundle_identity_matches = True
            scan_bundle = bundle
            if receipt["serving"]["status"] != "mismatch":
                receipt["serving"]["status"] = (
                    "mismatch"
                    if isinstance(preflight, dict) and preflight.get("status") == "mismatch"
                    else "unknown"
                )
        else:
            receipt["serving"]["status"] = "mismatch"
            receipt["serving"]["evidence_strength"] = "direct"
            receipt["serving"]["evidence"].append("bundle_reverification_failed")
            resolved_bundle_path = None
    elif isinstance(bundle, dict):
        receipt["serving"]["status"] = "unknown"
        receipt["serving"]["evidence_strength"] = "unknown"
        receipt["serving"]["evidence"].append("bundle_path_omitted")
    scan = scan_codex_trace(
        trace_path,
        bundle=scan_bundle,
        bundle_path=resolved_bundle_path,
        complete=complete,
        trace_bytes=snapshot,
    )
    metadata = scan["metadata"]
    session_id = receipt["session"].get("id")
    trace_session_id = metadata.get("id")
    if session_id and trace_session_id and session_id != opaque_identifier(trace_session_id):
        raise AttributionError("receipt session id does not match transcript")
    if trace_session_id:
        receipt["session"]["id"] = opaque_identifier(trace_session_id)
    receipt["session"]["source"] = safe_metadata_token(
        metadata.get("source") or receipt["session"].get("source")
    )
    receipt["session"]["trace"] = {
        "status": "linked" if scan["complete"] else "snapshot",
        "pointer": path_digest(trace_path),
        "content_digest": f"sha256:{sha256_bytes(snapshot)}",
        "bytes": len(snapshot),
    }
    if metadata.get("cli_version"):
        receipt["runtime"]["version"] = safe_metadata_token(str(metadata["cli_version"]))
    if scan.get("model"):
        receipt["runtime"]["model"] = safe_metadata_token(scan["model"])
    session_timestamp = metadata.get("timestamp")
    if isinstance(preflight, dict) and isinstance(session_timestamp, str):
        if parse_timestamp(preflight["recorded_at"], "serving preflight recorded_at") >= parse_timestamp(
            session_timestamp, "Codex session timestamp"
        ):
            receipt["serving"]["status"] = "mismatch"
            receipt["serving"]["evidence_strength"] = "direct"
            receipt["serving"]["evidence"].append("preflight_after_session_start")
    agents_observations = scan.get("agents_observations")
    invalid_world_states = scan.get("invalid_world_state_records", 0)
    trace_structure_unknown = bool(
        scan.get("parse_errors", 0) or scan.get("unsupported_records", 0)
    )
    all_assignments_match: bool | None = None
    if (
        bundle_identity_matches
        and isinstance(bundle, dict)
        and isinstance(agents_observations, list)
        and agents_observations
    ):
        all_assignments_match = all(
            observation.get("text_digest") == bundle.get("agents_digest")
            and observation.get("directory_digest") == bundle.get("path_digest")
            for observation in agents_observations
            if isinstance(observation, dict)
        ) and all(isinstance(observation, dict) for observation in agents_observations)
    if all_assignments_match is False:
        receipt["serving"]["status"] = "mismatch"
        receipt["serving"]["evidence_strength"] = "direct"
        receipt["serving"]["evidence"].append("world_state_assignment_mismatch")
    elif isinstance(invalid_world_states, int) and invalid_world_states > 0:
        if receipt["serving"]["status"] != "mismatch":
            receipt["serving"]["status"] = "unknown"
        receipt["serving"]["evidence_strength"] = "limited"
        receipt["serving"]["evidence"].append("world_state_agents_invalid")
    elif trace_structure_unknown:
        if receipt["serving"]["status"] != "mismatch":
            receipt["serving"]["status"] = "unknown"
        receipt["serving"]["evidence_strength"] = "limited"
        receipt["serving"]["evidence"].append("trace_structure_unsupported")
    elif all_assignments_match is True and scan["complete"]:
        for surface in receipt["serving"]["surfaces"]:
            if surface.get("name") == "AGENTS.md":
                surface["status"] = "observed_prompt_visible"
                surface["evidence"] = "actual_session_agents_exact_match"
        if receipt["serving"]["status"] != "mismatch":
            receipt["serving"]["status"] = "verified"
        receipt["serving"]["evidence_strength"] = "direct"
        receipt["serving"]["evidence"].append("world_state_assignments_match")
    elif all_assignments_match is True:
        if receipt["serving"]["status"] != "mismatch":
            receipt["serving"]["status"] = "unknown"
        receipt["serving"]["evidence_strength"] = "limited"
    if receipt["serving"]["status"] == "verified":
        receipt["activation"] = scan["activation"]
    else:
        receipt["activation"] = {
            "status": "unknown",
            "evidence_scope": "partial_trace_snapshot",
            "observed_skills": [],
            "adoption_claim": "unknown",
        }
    if not scan["complete"]:
        receipt["serving"]["evidence"].append("trace_incomplete")
    receipt["recorded_at"] = utc_now()
    seal_receipt(receipt)
    validate_receipt(receipt)
    return receipt


def make_backfill_receipt(trace_path: Path) -> dict[str, Any]:
    snapshot = trace_path.read_bytes()
    scan = scan_codex_trace(
        trace_path,
        bundle=None,
        complete=False,
        trace_bytes=snapshot,
    )
    metadata = scan["metadata"]
    session_id = metadata.get("id") if isinstance(metadata.get("id"), str) else None
    receipt = new_receipt(
        session_id=session_id,
        run_id=f"backfill:{session_id or sha256_bytes(snapshot)[:16]}",
        source=metadata.get("source") if isinstance(metadata.get("source"), str) else None,
        start_source="retrospective-backfill",
        cwd=metadata.get("cwd") if isinstance(metadata.get("cwd"), str) else None,
        runtime_vendor="openai",
        runtime_name="codex",
        runtime_version=metadata.get("cli_version")
        if isinstance(metadata.get("cli_version"), str)
        else None,
        model=scan.get("model"),
        serving=unknown_serving("legacy_trace_without_contemporaneous_bundle"),
    )
    receipt["activation"] = scan["activation"]
    receipt["session"]["trace"] = {
        "status": "snapshot",
        "pointer": path_digest(trace_path),
        "content_digest": f"sha256:{sha256_bytes(snapshot)}",
        "bytes": len(snapshot),
    }
    seal_receipt(receipt)
    validate_receipt(receipt)
    return receipt


def make_codex_linked_receipt(
    trace_path: Path,
    *,
    bundle_path: Path,
    probe_path: Path,
) -> dict[str, Any]:
    """Link a completed Codex trace to a pre-session serving preflight.

    This is the explicit adapter for environments where project hooks are not
    enabled. The preflight binds the bundle before execution; world_state in the
    trace independently binds the exact AGENTS.md text and directory observed by
    the session. Neither source is treated as Skill adoption evidence.
    """
    trace_path = trace_path.expanduser().resolve()
    if not trace_path.is_file():
        raise AttributionError("Codex transcript path is missing")
    snapshot = trace_path.read_bytes()
    probe = load_probe(probe_path)
    if probe is None:
        raise AttributionError("Codex trace linkage requires a serving preflight")
    scan = scan_codex_trace(
        trace_path,
        bundle=None,
        complete=True,
        trace_bytes=snapshot,
    )
    metadata = scan["metadata"]
    session_id = metadata.get("id") if isinstance(metadata.get("id"), str) else None
    if not session_id:
        raise AttributionError("Codex transcript lacks a session id")
    cwd = metadata.get("cwd") if isinstance(metadata.get("cwd"), str) else None
    receipt = new_receipt(
        session_id=session_id,
        run_id=f"codex:{session_id}",
        source=metadata.get("source") if isinstance(metadata.get("source"), str) else None,
        start_source="codex-preflight-trace-link",
        cwd=cwd,
        runtime_vendor="openai",
        runtime_name="codex",
        runtime_version=metadata.get("cli_version")
        if isinstance(metadata.get("cli_version"), str)
        else None,
        model=scan.get("model"),
        serving=serving_from_bundle(bundle_path, cwd=cwd, probe=probe),
    )
    receipt["serving"]["evidence"].append("explicit_trace_link_without_sessionstart")
    attach_trace(
        receipt,
        trace_path,
        bundle_path=bundle_path,
        complete=True,
        trace_bytes=snapshot,
    )
    return receipt


def handle_codex_event(
    event: dict[str, Any],
    *,
    bundle_path: Path,
    receipt_dir: Path,
    probe_path: Path | None,
) -> Path:
    event_name = event.get("hook_event_name")
    session_id = event.get("session_id")
    if not isinstance(session_id, str) or not session_id:
        raise AttributionError("Codex hook event lacks session_id")
    output = receipt_path(receipt_dir, session_id)
    if event_name not in {"SessionStart", "SessionEnd"}:
        mark_output_pending(output, "codex-hook")
        raise AttributionError(f"unsupported Codex hook event: {event_name}")
    if event_name == "SessionStart":
        receipt: dict[str, Any] | None = None
        existing_bundle: dict[str, Any] | None = None
        persistent_bundle_switch = False
        if output.is_file():
            receipt = load_receipt_for_lifecycle_update(output)
            prior_bundle = receipt["serving"].get("bundle")
            existing_bundle = prior_bundle if isinstance(prior_bundle, dict) else None
            persistent_bundle_switch = (
                "resume_bundle_mismatch" in receipt["serving"].get("evidence", [])
            )
            reset_trace_derived_state(receipt)
            if "resume_requires_reverification" not in receipt["serving"]["evidence"]:
                receipt["serving"]["evidence"].append("resume_requires_reverification")
            receipt["recorded_at"] = utc_now()
            seal_receipt(receipt)
            validate_receipt(receipt)
            atomic_write_json(output, receipt)
        probe = load_probe(probe_path)
        serving = serving_from_bundle(
            bundle_path,
            cwd=event.get("cwd") if isinstance(event.get("cwd"), str) else None,
            probe=probe,
        )
        if receipt is not None:
            resumed_bundle = serving.get("bundle")
            receipt["serving"] = serving
            if (
                persistent_bundle_switch
                or serving.get("status") == "mismatch"
                or not isinstance(existing_bundle, dict)
                or existing_bundle != resumed_bundle
            ):
                receipt["serving"]["status"] = "mismatch"
                receipt["serving"]["evidence"].append("resume_bundle_mismatch")
            else:
                receipt["serving"]["evidence"].append("resume_requires_reverification")
            receipt["activation"] = {
                "status": "unknown",
                "evidence_scope": "none",
                "observed_skills": [],
                "adoption_claim": "unknown",
            }
            receipt["session"]["trace"] = empty_trace()
            receipt["recorded_at"] = utc_now()
            seal_receipt(receipt)
            validate_receipt(receipt)
            atomic_write_json(output, receipt)
            return output
        runtime_version = None
        if probe is not None:
            value = probe.get("runtime", {}).get("version")
            runtime_version = value if isinstance(value, str) else None
        receipt = new_receipt(
            session_id=session_id,
            run_id=f"codex:{session_id}",
            source="codex-hook",
            start_source=event.get("source") if isinstance(event.get("source"), str) else None,
            cwd=event.get("cwd") if isinstance(event.get("cwd"), str) else None,
            runtime_vendor="openai",
            runtime_name="codex",
            runtime_version=runtime_version,
            model=event.get("model") if isinstance(event.get("model"), str) else None,
            serving=serving,
        )
        atomic_write_json(output, receipt)
        return output
    if event_name == "SessionEnd":
        receipt = load_receipt_for_lifecycle_update(output)
        reset_trace_derived_state(receipt)
        if "trace_incomplete" not in receipt["serving"]["evidence"]:
            receipt["serving"]["evidence"].append("trace_incomplete")
        receipt["recorded_at"] = utc_now()
        seal_receipt(receipt)
        validate_receipt(receipt)
        atomic_write_json(output, receipt)
        transcript = event.get("transcript_path")
        if not isinstance(transcript, str) or not transcript:
            receipt["serving"]["evidence"] = [
                evidence
                for evidence in receipt["serving"]["evidence"]
                if evidence != "trace_incomplete"
            ]
            receipt["serving"]["evidence"].append("sessionend_trace_missing")
            receipt["recorded_at"] = utc_now()
            seal_receipt(receipt)
            validate_receipt(receipt)
        else:
            attach_trace(
                receipt,
                Path(transcript),
                bundle_path=bundle_path,
                complete=True,
            )
        atomic_write_json(output, receipt)
        return output
    raise AttributionError(f"unsupported Codex hook event: {event_name}")


def normalize_text(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\r", "\n")


def prompt_input_texts(value: Any) -> list[str]:
    texts: list[str] = []
    if isinstance(value, dict):
        if value.get("type") in {"input_text", "output_text"} and isinstance(value.get("text"), str):
            texts.append(value["text"])
        for child in value.values():
            texts.extend(prompt_input_texts(child))
    elif isinstance(value, list):
        for child in value:
            texts.extend(prompt_input_texts(child))
    return texts


def _codex_agents_prompt_isolated(
    texts: list[str], bundle_path: Path, agents: str
) -> bool:
    expected = (
        f"# AGENTS.md instructions for {bundle_path}\n\n"
        f"<INSTRUCTIONS>\n{normalize_text(agents).strip()}\n\n</INSTRUCTIONS>"
    )
    return any(normalize_text(text).strip() == expected for text in texts)


def run_codex_version(command: Path) -> str | None:
    completed = subprocess.run(
        [str(command), "--version"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
        check=False,
    )
    if completed.returncode != 0:
        return None
    text = completed.stdout.strip()
    match = re.search(r"([0-9]+(?:\.[0-9A-Za-z-]+)+)", text)
    return match.group(1) if match else text or None


def create_codex_probe(bundle_path: Path, codex_command: Path) -> dict[str, Any]:
    bundle_path = bundle_path.expanduser().resolve()
    codex_command = codex_command.expanduser().resolve()
    identity = bundle_identity(bundle_path)
    command = [
        str(codex_command),
        "debug",
        "prompt-input",
        "--disable",
        "hooks",
        "execution-attribution-preflight",
    ]
    completed = subprocess.run(
        command,
        cwd=bundle_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
        check=False,
    )
    if completed.returncode != 0:
        raise AttributionError(
            f"Codex prompt-input preflight failed with exit {completed.returncode}"
        )
    try:
        prompt_input = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise AttributionError("Codex prompt-input output is not JSON") from exc
    texts = [normalize_text(text) for text in prompt_input_texts(prompt_input)]
    agents = normalize_text((bundle_path / "AGENTS.md").read_text(encoding="utf-8")).strip()
    catalog = normalize_text((bundle_path / "runtime-catalog.json").read_text(encoding="utf-8")).strip()
    probe = {
        "schema_version": 1,
        "record_type": "codex-serving-preflight",
        "probe_id": str(uuid.uuid4()),
        "recorded_at": utc_now(),
        "runtime": {
            "vendor": "openai",
            "name": "codex",
            "version": run_codex_version(codex_command),
            "command_digest": f"sha256:{sha256_file(codex_command)}",
        },
        "bundle": {
            "manifest_digest": identity["manifest_digest"],
            "path_digest": identity["path_digest"],
            "agents_digest": identity["agents_digest"],
            "runtime_catalog_digest": identity["runtime_catalog_digest"],
        },
        "prompt_input_digest": f"sha256:{sha256_bytes(completed.stdout.encode('utf-8'))}",
        "agents_prompt_visible": _codex_agents_prompt_isolated(
            texts, bundle_path, agents
        ),
        "runtime_catalog_prompt_visible": any(catalog in text for text in texts),
        "privacy": {
            "prompt_content_stored": False,
            "response_content_stored": False,
            "source_content_stored": False,
        },
        "integrity": {"algorithm": "sha256", "record_digest": None},
    }
    seal_probe(probe)
    validate_probe(probe)
    return probe


def canonical_behavior_evidence_bytes(record: dict[str, Any]) -> bytes:
    value = copy.deepcopy(record)
    value.setdefault("integrity", {})["record_digest"] = None
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def seal_behavior_evidence(record: dict[str, Any]) -> dict[str, Any]:
    record.setdefault("integrity", {})["algorithm"] = "sha256"
    record["integrity"]["record_digest"] = (
        f"sha256:{sha256_bytes(canonical_behavior_evidence_bytes(record))}"
    )
    return record


def validate_behavior_evidence(
    record: dict[str, Any],
    *,
    receipt: dict[str, Any],
    skill: str,
) -> None:
    _require_exact_keys(
        record,
        {
            "schema_version",
            "record_type",
            "session_id",
            "skill",
            "assessment",
            "evaluator",
            "evidence",
            "integrity",
        },
        "behavior evidence",
    )
    if record.get("schema_version") != 1 or record.get("record_type") != "behavior-evidence":
        raise AttributionError("behavior evidence identity/version mismatch")
    _require_opaque_identifier(record.get("session_id"), "behavior evidence session_id")
    if record.get("session_id") != receipt["session"]["id"]:
        raise AttributionError("behavior evidence session does not match receipt")
    _require_skill_name(record.get("skill"), "behavior evidence Skill")
    if record.get("skill") != skill:
        raise AttributionError("behavior evidence Skill does not match classification target")
    if record.get("assessment") not in {"contradicted", "followed"}:
        raise AttributionError("behavior evidence assessment is invalid")
    evaluator = record.get("evaluator")
    if not isinstance(evaluator, dict):
        raise AttributionError("behavior evidence evaluator must be an object")
    _require_exact_keys(evaluator, {"kind", "id_digest"}, "behavior evidence evaluator")
    if evaluator.get("kind") not in {"human", "deterministic", "model"}:
        raise AttributionError("behavior evidence evaluator kind is invalid")
    _require_digest(evaluator.get("id_digest"), "behavior evidence evaluator.id_digest")
    evidence = record.get("evidence")
    if not isinstance(evidence, dict):
        raise AttributionError("behavior evidence evidence must be an object")
    _require_exact_keys(
        evidence,
        {"attribution_receipt_digest", "content_digest", "recorded_at"},
        "behavior evidence evidence",
    )
    _require_digest(
        evidence.get("attribution_receipt_digest"),
        "behavior evidence attribution_receipt_digest",
    )
    if evidence.get("attribution_receipt_digest") != receipt["integrity"]["receipt_digest"]:
        raise AttributionError("behavior evidence is not bound to this receipt version")
    _require_digest(evidence.get("content_digest"), "behavior evidence content_digest")
    if not isinstance(evidence.get("recorded_at"), str):
        raise AttributionError("behavior evidence recorded_at must be a string")
    behavior_timestamp = require_not_future(
        evidence["recorded_at"], "behavior evidence recorded_at"
    )
    receipt_timestamp = parse_timestamp(receipt["recorded_at"], "receipt recorded_at")
    if behavior_timestamp < receipt_timestamp:
        raise AttributionError("behavior evidence cannot predate its bound receipt")
    integrity = record.get("integrity")
    if not isinstance(integrity, dict):
        raise AttributionError("behavior evidence integrity must be an object")
    _require_exact_keys(integrity, {"algorithm", "record_digest"}, "behavior evidence integrity")
    if integrity.get("algorithm") != "sha256":
        raise AttributionError("behavior evidence integrity algorithm mismatch")
    _require_digest(integrity.get("record_digest"), "behavior evidence integrity.record_digest")
    expected = f"sha256:{sha256_bytes(canonical_behavior_evidence_bytes(record))}"
    if integrity.get("record_digest") != expected:
        raise AttributionError("behavior evidence integrity digest mismatch")


def classify_failure(
    receipt: dict[str, Any],
    *,
    skill: str,
    current_bundle: dict[str, Any] | None,
    failure_domain: str,
    behavior_evidence: dict[str, Any] | None,
) -> dict[str, Any]:
    validate_receipt(receipt)
    _require_skill_name(skill, "classification Skill")
    if failure_domain != "agent":
        mapping = {
            "environment": "environment_failure",
            "tool": "tool_failure",
            "evaluator": "evaluator_failure",
            "unknown": "unknown_attribution",
        }
        return {
            "classification": mapping[failure_domain],
            "skill": skill,
            "root_cause_claimed": False,
            "reason": "failure domain was supplied independently of capability attribution",
        }
    if behavior_evidence is not None:
        validate_behavior_evidence(
            behavior_evidence,
            receipt=receipt,
            skill=skill,
        )
    serving = receipt["serving"]
    served_bundle = serving.get("bundle")
    if serving.get("status") != "verified" or not isinstance(served_bundle, dict):
        return {
            "classification": "unknown_attribution",
            "skill": skill,
            "root_cause_claimed": False,
            "reason": "session is not linked to a verified serving bundle",
        }
    served_digests = served_bundle["skill_digests"]
    served_has = skill in served_digests
    current_has = current_bundle is not None and skill in current_bundle["skill_digests"]
    if not served_has:
        if current_bundle is None:
            return {
                "classification": "served_skill_artifact_absent",
                "skill": skill,
                "root_cause_claimed": False,
                "reason": "the exact Skill artifact is absent from the verified served bundle; no current reference was supplied",
            }
        return {
            "classification": (
                "not_served" if current_has else "requested_skill_artifact_absent"
            ),
            "skill": skill,
            "root_cause_claimed": False,
            "reason": (
                "current reference bundle contains the exact Skill artifact but the session bundle did not"
                if current_has
                else "the exact Skill artifact is absent from both verified served and current reference bundles"
            ),
        }
    if current_has and served_digests[skill] != current_bundle["skill_digests"][skill]:
        return {
            "classification": "not_served",
            "skill": skill,
            "root_cause_claimed": False,
            "reason": "session used a different digest for the relevant skill",
        }
    observed = {
        item["name"]: item for item in receipt["activation"]["observed_skills"]
    }
    if skill in observed:
        assessment = behavior_evidence.get("assessment") if behavior_evidence else None
        if assessment == "contradicted":
            classification = "activated_but_not_followed"
            reason = (
                "Skill content delivery is observed and a receipt-bound behavior record contradicts it"
            )
        elif assessment == "followed":
            classification = "activated_and_followed"
            reason = (
                "Skill content delivery and a receipt-bound following record are both present"
            )
        else:
            classification = "activation_observed"
            reason = "Skill body delivery is observed; adoption/compliance remains unknown"
        result = {
            "classification": classification,
            "skill": skill,
            "root_cause_claimed": False,
            "reason": reason,
        }
        if behavior_evidence is not None:
            result["behavior_evidence_digest"] = behavior_evidence["integrity"]["record_digest"]
        return result
    activation = receipt["activation"]
    if (
        activation.get("status") == "none_observed"
        and activation.get("evidence_scope") == "complete_trace_snapshot"
    ):
        return {
            "classification": "not_activated",
            "skill": skill,
            "root_cause_claimed": False,
            "reason": (
                "verified bundle exposed the Skill and the parse-clean terminal trace has no "
                "successful full-body content delivery"
            ),
        }
    return {
        "classification": "unknown_attribution",
        "skill": skill,
        "root_cause_claimed": False,
        "reason": "serving is known but activation evidence is incomplete",
    }


def cmd_probe(args: argparse.Namespace) -> int:
    output = Path(args.output).expanduser().resolve() if args.output else None
    if output is not None:
        mark_output_pending(output, "codex-probe")
    probe = create_codex_probe(Path(args.bundle), Path(args.codex_command))
    if output is not None:
        atomic_write_json(output, probe)
    print(json.dumps(probe, ensure_ascii=False, sort_keys=True))
    return 0


def cmd_codex_hook(args: argparse.Namespace) -> int:
    event = json.load(sys.stdin)
    if not isinstance(event, dict):
        raise AttributionError("Codex hook input must be an object")
    handle_codex_event(
        event,
        bundle_path=Path(args.bundle),
        receipt_dir=Path(args.receipt_dir),
        probe_path=Path(args.probe) if args.probe else None,
    )
    return 0


def cmd_backfill(args: argparse.Namespace) -> int:
    output = Path(args.output).expanduser().resolve() if args.output else None
    if output is not None:
        mark_output_pending(output, "backfill")
    trace_path = Path(args.session).expanduser().resolve()
    receipt = make_backfill_receipt(trace_path)
    if output is not None:
        atomic_write_json(output, receipt)
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0


def cmd_codex_link(args: argparse.Namespace) -> int:
    output = Path(args.output).expanduser().resolve()
    mark_output_pending(output, "codex-link")
    receipt = make_codex_linked_receipt(
        Path(args.session),
        bundle_path=Path(args.bundle),
        probe_path=Path(args.probe),
    )
    atomic_write_json(output, receipt)
    print(
        json.dumps(
            {
                "receipt": str(output),
                "session_id": receipt["session"]["id"],
                "serving": receipt["serving"]["status"],
                "activation": receipt["activation"]["status"],
            },
            sort_keys=True,
        )
    )
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    receipt = load_receipt(Path(args.receipt).expanduser().resolve())
    print(
        json.dumps(
            {
                "receipt": str(Path(args.receipt).expanduser().resolve()),
                "status": "valid",
                "session_id": receipt["session"]["id"],
                "serving": receipt["serving"]["status"],
                "activation": receipt["activation"]["status"],
            },
            sort_keys=True,
        )
    )
    return 0


def cmd_classify(args: argparse.Namespace) -> int:
    receipt = load_receipt(Path(args.receipt).expanduser().resolve())
    current = bundle_identity(Path(args.current_bundle)) if args.current_bundle else None
    behavior_evidence = (
        read_json(Path(args.behavior_evidence_record).expanduser().resolve())
        if args.behavior_evidence_record
        else None
    )
    result = classify_failure(
        receipt,
        skill=args.skill,
        current_bundle=current,
        failure_domain=args.failure_domain,
        behavior_evidence=behavior_evidence,
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Create and analyze privacy-minimal execution attribution receipts. "
            "Receipts record serving and activation evidence; they do not infer root cause."
        )
    )
    sub = parser.add_subparsers(dest="command", required=True)

    probe = sub.add_parser("codex-probe", help="Verify Codex model-visible serving preflight.")
    probe.add_argument("--bundle", required=True)
    probe.add_argument("--codex-command", required=True)
    probe.add_argument("--output")
    probe.set_defaults(func=cmd_probe)

    hook = sub.add_parser("codex-hook", help="Consume a Codex SessionStart or SessionEnd hook event.")
    hook.add_argument("--bundle", required=True)
    hook.add_argument("--receipt-dir", required=True)
    hook.add_argument("--probe")
    hook.set_defaults(func=cmd_codex_hook)

    backfill = sub.add_parser("backfill-codex", help="Create an unknown-serving receipt from a legacy JSONL session.")
    backfill.add_argument("--session", required=True)
    backfill.add_argument("--output")
    backfill.set_defaults(func=cmd_backfill)

    link = sub.add_parser(
        "codex-link",
        help="Link a completed Codex JSONL session to its pre-session serving probe.",
    )
    link.add_argument("--session", required=True)
    link.add_argument("--bundle", required=True)
    link.add_argument("--probe", required=True)
    link.add_argument("--output", required=True)
    link.set_defaults(func=cmd_codex_link)

    validate = sub.add_parser("validate", help="Validate a receipt and its integrity digest.")
    validate.add_argument("--receipt", required=True)
    validate.set_defaults(func=cmd_validate)

    classify = sub.add_parser("classify", help="Map one failure to an evidence-bounded attribution state.")
    classify.add_argument("--receipt", required=True)
    classify.add_argument("--skill", required=True)
    classify.add_argument("--current-bundle")
    classify.add_argument(
        "--failure-domain",
        choices=("agent", "environment", "tool", "evaluator", "unknown"),
        default="agent",
    )
    classify.add_argument(
        "--behavior-evidence-record",
        help=(
            "Receipt-bound behavior evidence JSON. Without it, activation never becomes a "
            "compliance conclusion."
        ),
    )
    classify.set_defaults(func=cmd_classify)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except (AttributionError, BundleError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
