# Adjacent Routes

SkillConverge studies neighboring systems as architecture evidence, not just as sources of `SKILL.md` prose. The purpose of this ledger is to keep transferable mechanisms and non-transferable assumptions visible without turning every adjacent project into a runtime dependency.

This is a living comparison. Entries are not endorsements or rankings.

## SkillCompass — lifecycle and quality management

**Useful mechanisms**

- evaluate → improve → verify as a closed loop rather than prompt tweaking by intuition;
- compare uniqueness and overlap, not only syntax and trigger quality;
- keep recoverable snapshots so an attempted improvement can be rolled back;
- use real usage/correction signals to decide what deserves attention;
- intercept skill edits at a pre-accept boundary instead of trusting the editing tool.

**Do not generalize blindly**

- fixed dimension weights and PASS/CAUTION/FAIL score cutoffs are a product policy, not universal evidence;
- fixed improvement-round defaults and model/version requirements should not become SkillConverge gates;
- local hooks and one host's lifecycle are useful adapters, not the vendor-neutral core.

**Current lesson**

Skill quality needs lifecycle evidence and rollback, but the acceptance contract should be capability-specific rather than one global score.

## skillgrade — executable skill evaluation

**Useful mechanisms**

- evaluate the skill in an actual agent run rather than grading the text alone;
- combine deterministic graders with qualitative/model graders when each settles a different claim;
- support a custom command agent so the evaluator is not tied to one host;
- compare reproducible workspace state and task outcomes, not just the agent's explanation;
- CI should fail only on an explicitly authorized evaluation contract.

**Do not generalize blindly**

- preset trial counts, timeouts, weights, and pass thresholds are tool defaults, not portable truths;
- LLM graders inherit model variance and should not be treated as deterministic evidence;
- installing an external evaluation stack is optional infrastructure, not a requirement for every canonical skill.

**Current lesson**

SkillConverge should make baseline-versus-candidate evaluation pluggable, with deterministic assertions preferred whenever the capability permits them.

## SkillAnything — target-to-skill generation pipeline

**Useful mechanisms**

- analyze a target before writing instructions;
- separate capability extraction, skill design, implementation, test generation, evaluation, optimization, and packaging;
- keep platform-specific packaging as an adapter around a portable skill;
- generate evaluation cases from the target contract rather than only from the authored prompt.

**Do not generalize blindly**

- a fixed phase count is a pipeline design, not a universal requirement;
- automatically generating one skill per tool/API can create a large local library without global semantic deduplication;
- automatic inspection of executable targets or network services crosses a trust boundary and cannot be inherited by discovery automation;
- optimization iteration counts and benchmark percentages are local evidence, not project-wide gates.

**Current lesson**

Target analysis is a strong source of baseline skills for uncovered domains, but generated capabilities must still enter the global canonical competition instead of bypassing deduplication.

## RepoSkillOpt — canonical convergence plus specialization

**Useful mechanisms**

- separate a generic canonical base from target-specific specialization;
- let specialization learn local quirks without writing them back into the shared canonical skill;
- use deterministic grounding checks against real files as acceptance evidence;
- reject edits when the baseline is already at ceiling instead of forcing an optimization round to produce change;
- validate shared/canonical improvements against held-out targets so one repository does not contaminate the base.

**Do not generalize blindly**

- repository-understanding artifacts, fixed section counts, symbol-coverage targets, and citation metrics are specific to that product contract;
- a metric that works for repository specifications cannot automatically grade design, security, writing, or scientific skills;
- per-repo optimization and ecosystem-wide canonical distillation are different layers and should stay separate.

**Current lesson**

This is the strongest neighboring evidence for SkillConverge's contamination boundary: global canonical evolution and local specialization should be separate optimization problems.

## SkillEvolver — deployment-grounded skill evolution

**Useful mechanisms**

- test candidate guidance through a fresh downstream agent instead of asking the authoring agent whether its own patch is good;
- contrast successful and failed trajectories to identify the missing decision rule;
- keep exploration and validation separate where the task supports a held-out split;
- evaluate deployed behavior, including silent skill bypass and misleading guidance, rather than only the skill text;
- an independent auditor can reduce anchoring on the author's own reasoning.

**Do not generalize blindly**

- fixed strategy counts, round counts, specific models, Harbor infrastructure, and benchmark cost are experiment choices;
- validation on the same problem for some continuous-reward tasks is weaker evidence of cross-task generalization;
- spawning many expensive trials is not automatically justified for low-risk deterministic skills.

**Current lesson**

Fresh-session deployment evaluation should become the preferred evidence for behavior-sensitive skill improvements when deterministic evaluation cannot settle the claim.

## SkillWeaver — practice-to-skill distillation

**Useful mechanisms**

- let an agent explore a domain, practice tasks, observe failures, and distill recurring successful procedures into reusable actions;
- compare performance with and without the learned library;
- recover and refine generated actions when real execution exposes a gap;
- treat interaction experience as evidence that can create a reusable capability.

**Do not generalize blindly**

- web-agent APIs and exploration schedules are domain-specific;
- continually synthesizing APIs can grow a local action space without a global one-trigger-per-capability policy;
- practice-generated artifacts require the same trust, compatibility, and dedup review as human-authored skills.

**Current lesson**

A future SkillConverge feedback layer may learn from task trajectories, but learned behavior still has to compete for canonical ownership rather than accumulate indefinitely.

## Cisco Skill Scanner — skill supply-chain security

**Useful mechanisms**

- layer static signatures, behavioral/data-flow analysis, semantic analysis, and false-positive filtering instead of trusting one scanner;
- scan a repository or skill package before installation/execution;
- distinguish detection from certification and preserve human review for material findings;
- emit machine-readable security evidence suitable for CI.

**Do not generalize blindly**

- scanner policies, severity cutoffs, consensus run counts, and cloud analyzers are configurable product choices;
- "no findings" cannot become proof that an upstream is safe;
- an LLM security analyzer is still probabilistic and cannot authorize execution by itself.

**Current lesson**

Promotion should support dedicated supply-chain scanner evidence, but security remains a gate of unresolved material risk rather than a single numeric score.

## Agent Skills specification — interoperability

**Useful mechanisms**

- preserve a portable core format and keep host-specific metadata in adapters;
- validate the standard structure independently of any one vendor runtime.

**Do not generalize blindly**

- format compliance proves interoperability structure, not skill quality or safety.

## Transitive sources currently worth inspecting

- `HKUDS/CLI-Anything` — surfaced through SkillAnything's stated methodology lineage; inspect capability extraction and tool-interface generation directly rather than through SkillAnything's interpretation.
- `DazhuangJammy/DazhuangSkill-Creator` — surfaced through SkillAnything's project-structure lineage; inspect whether any authoring structure survives comparison with current `create-agent-skill`.

The discovery action also emits one-hop GitHub references from every tracked README. Those references are leads only. Mirrors, dependencies, benchmarks, papers, and unrelated links should be filtered during review rather than automatically copied into `upstreams.json`.

## Cross-project synthesis already adopted

The current project architecture already reflects several mechanisms reinforced by the adjacent routes above:

- untrusted discovery is separated from canonical routing;
- the current canonical implementation is a baseline to beat, not permanent authority;
- candidate claims are tested against explicit evidence rather than accepted for recency or reputation;
- specialization and provider-specific behavior are scoped rather than promoted into universal core rules;
- failed or rejected implementations may produce a compact architectural lesson without preserving their source prose;
- deterministic checks are preferred when they can directly prove the claim;
- judgment-heavy skills should be evaluated on contrasting cases and, when possible, fresh downstream sessions.

Future adjacent-route reviews should update this ledger only when they change a real project decision. It is not a catalog of every project encountered.
