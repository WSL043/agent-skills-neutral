# Runtime Bundle Boundary

The source repository is the single authoring and evolution authority. Task agents should consume a generated runtime bundle rather than the repository root.

## Why the boundary exists

Maintainers need discovery state, provenance, rejected candidates, evaluators, Evolution Runner state, schemas, tests, and source policy. A task agent normally needs none of that context. Exposing the full control plane can waste attention, create irrelevant routing choices, and blur the distinction between validated capabilities and the machinery used to produce them.

The runtime boundary therefore separates **authoring authority** from **task-time consumption** without creating a second hand-maintained source tree.

## Source of truth

Editable canonical source remains here:

```text
skills/
catalog.json
runtime-catalog.json
runtime/AGENTS.md
```

Evolution, evaluation, and maintenance may change those sources only through the normal evidence and validation contracts.

Generated runtime output is not canonical source and must never be edited as the way to change a skill.

Canonical `SKILL.md` files may contain a terminal maintainer-only `## Provenance` section. Runtime compilation deterministically removes that terminal section from generated `SKILL.md` files because attribution/review lineage belongs to the authoring/control plane and `provenance.json` is intentionally absent from task-time artifacts. This is a build transform, not a second canonical skill representation.

## Build

Production build from a clean commit:

```bash
python scripts/build_runtime_bundle.py build --output dist/runtime
python scripts/build_runtime_bundle.py verify --bundle dist/runtime
```

During an uncommitted local change, pre-validation is explicit:

```bash
python scripts/build_runtime_bundle.py build --output dist/runtime --allow-dirty
```

A dirty build records `source_dirty=true` in `MANIFEST.json` and is not a publication-quality artifact.

`dist/` is generated and ignored by Git.

## Runtime surface

The generated bundle contains only:

```text
AGENTS.md
runtime-catalog.json
MANIFEST.json
skills/
```

The skill directories contain the canonical skill-owned files required at task time, including their `SKILL.md` bodies and conditionally loaded references/resources.

The bundle intentionally excludes repository-level control-plane material such as:

```text
provenance.json
upstreams.json
catalog.json
index.json
routes/
profiles/
docs/
scripts/
tests/
schemas/
.github/
.evolution/
```

The runtime `AGENTS.md` is deliberately smaller than the maintainer `AGENTS.md`.

## Manifest

`MANIFEST.json` binds the artifact to its source commit and records:

- source repository and exact commit;
- whether the build came from a dirty tree;
- routing authority;
- canonical-catalog and runtime-catalog digests;
- every runtime file's SHA-256 and byte size;
- one deterministic digest for each skill directory.

The manifest is a reproducibility and integrity record. It is not proof that a skill is semantically correct; semantic promotion still belongs to the evolution/evaluation layer.

## Verification

`verify` rejects:

- changed or missing runtime files relative to the manifest;
- unexpected top-level files or directories;
- control-plane leakage;
- runtime catalog/manifest skill disagreement;
- missing skill locations;
- corrupted per-skill digests.

The compiler never executes skill scripts while packaging them.

## Future standalone runtime repository

If a separately consumable repository becomes useful, do not fork the canonical source into another hand-maintained library.

Use this flow instead:

```text
source main
    |
    v
validate canonical + runner
    |
    v
build runtime bundle
    |
    v
verify manifest
    |
    v
automatically mirror exact generated output
    |
    v
runtime-only repository/package/release
```

The generated destination should reject manual edits or treat them as disposable. A runtime repository is a distribution channel, not a second source of truth.

## Scaling into packs

The initial bundle contains all canonical skills because the current metadata surface is small. If specialist breadth grows enough to create context competition, the compiler may later emit deterministic packs such as `core`, `reasoning`, and specialist groups.

Pack generation must remain an artifact concern. It must not turn a deterministic classifier into the semantic task-time authority: the agent still chooses among exposed candidates by meaning and task outcome.
