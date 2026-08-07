# Continuous Evolution

The library is a distillation layer, not an archive. Upstream coverage may grow without bound; the canonical skill set should grow only when a genuinely distinct reusable capability survives comparison with what already exists.

## State

`upstreams.json` records the last commit whose delta was fully reviewed for each tracked repository. `provenance.json` records only sources that actually contributed to retained canonical skills. Upstream files are not copied merely to preserve history.

Run:

```bash
python scripts/scan_upstreams.py
python scripts/scan_upstreams.py --json
python scripts/scan_upstreams.py --repo owner/repo
```

The scanner is read-only. A changed or unreviewed repository remains pending until an agent or maintainer inspects it.

## Ingestion loop

1. Scan only the delta after `last_reviewed_commit` when one exists.
2. Inspect each changed candidate's complete instructions, references needed to understand its behavior, bundled scripts, dependencies, license, and trust boundary before using it.
3. Translate the candidate into capability, trigger, decision logic, evidence, and failure modes. Ignore naming differences.
4. Compare it against existing canonical skills before proposing a new one.
5. Classify the candidate as one of:
   - **strengthen** — same outcome, but it contains a better rule, test, safety boundary, or implementation branch;
   - **replace** — it demonstrably dominates an existing implementation while preserving the existing contract;
   - **new capability** — the outcome and trigger are materially distinct and cannot be expressed cleanly by an existing skill;
   - **reject** — redundant, provider-bound without reusable logic, weakly implemented, stale, unsafe, unlicensed for adaptation, or unable to beat the current baseline.
6. For a retained change, absorb only the smallest behavior that improves the canonical implementation. Do not vendor upstream prose, scripts, assets, or process history unless the artifact itself is necessary and its license permits it.
7. Evaluate the candidate against explicit assertions before and after the change. A new canonical skill must also pass positive and negative routing tests. Do not keep a change merely because it is newer or more detailed.
8. Advance `last_reviewed_commit` only after the whole relevant delta has been classified. The reviewed commit is also the rejection memory: rejected source text does not need a local archive.
9. Update provenance only for sources that materially contributed to a retained implementation.

## Replacement pressure

Existing skills are candidates too. A canonical skill should be simplified, merged, replaced, or removed when current evidence shows another implementation covers its useful behavior with less overlap or stronger proof. Historical status is not authority.

## Design evolution

Design guidance has two different kinds of knowledge and they must not be mixed:

- **durable judgment** — hierarchy, proportion, rhythm, contrast, optical balance, typography, material coherence, content-form fit, interaction quality, restraint, and intentional tension;
- **dated generator fingerprints** — recurring combinations that a model family or design-generator era overproduces across unrelated briefs.

Durable judgment belongs in the core design protocol. Dated fingerprints belong in `skills/design-frontend/references/aesthetic-signals.md` and are evidence, not bans. Update or remove them when the pattern landscape changes.

A design rule is not accepted because a respected designer prefers it. Compare multiple independent design sources, separate shared principles from author taste, and test the result across deliberately different briefs. If different briefs still collapse to the same composition, palette logic, typography role, or motion vocabulary, the guidance is not teaching taste; it is teaching another template.

## Stop condition

Stop an ingestion pass when every changed candidate in the reviewed delta is classified and every retained change is proven against its actual contract. Do not search for extra work merely to make the pass feel comprehensive.
