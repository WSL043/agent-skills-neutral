from __future__ import annotations

import tempfile
from pathlib import Path

import sync_codex_skills as sync


def state_for(rows: list[dict[str, str]], name: str) -> str:
    return next(row["state"] for row in rows if row["name"] == name)


def main() -> int:
    name = "clarify-requirements"
    source_before = (sync.SOURCE_ROOT / name / "SKILL.md").read_bytes()

    with tempfile.TemporaryDirectory() as temporary:
        target = Path(temporary) / "skills"
        result = sync.install(target, [name], replace=False)
        if result != [{"name": name, "state": "installed"}]:
            raise AssertionError(f"unexpected install result: {result}")

        installed = (target / name / "SKILL.md").read_text(encoding="utf-8")
        if "## Provenance" in installed or "../../provenance.json" in installed:
            raise AssertionError("Codex install retained maintainer-only provenance content")

        rows = sync.inventory(target, sync.canonical_names())
        if state_for(rows, name) != "current":
            raise AssertionError(f"fresh runtime install is not current: {rows}")

        (target / name / "SKILL.md").write_text(installed + "\nTAMPERED\n", encoding="utf-8")
        rows = sync.inventory(target, sync.canonical_names())
        if state_for(rows, name) != "drifted":
            raise AssertionError("tampered runtime install was not reported as drifted")

        result = sync.install(target, [name], replace=True)
        if result != [{"name": name, "state": "installed"}]:
            raise AssertionError(f"unexpected replacement result: {result}")
        rows = sync.inventory(target, sync.canonical_names())
        if state_for(rows, name) != "current":
            raise AssertionError("replacement did not restore the runtime install")

    if (sync.SOURCE_ROOT / name / "SKILL.md").read_bytes() != source_before:
        raise AssertionError("sync test modified canonical source")

    print("CODEX SKILL SYNC TESTS PASSED runtime_transform=pass drift_guard=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
