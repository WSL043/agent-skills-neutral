# Agent Capability Learning Loop

The repository should improve from experience without turning every failure into permanent prompt text. Learning is a controlled evidence loop over externalized behavior, not uncontrolled self-rewriting.

## Objective

Convert execution experience, user corrections, upstream mechanisms, and evaluation failures into the smallest transferable improvement that measurably increases agent capability.

The loop optimizes shared behavior while the underlying model may remain frozen.

## 1. Collect experience

For behavior-sensitive evolution, preserve enough structured evidence to reconstruct what happened:

- task contract and relevant constraints;
- model/runtime/harness when material;
- skills made available and skills actually loaded;
- an execution-attribution receipt when the host can provide one, keeping serving, activation, and compliance evidence separate;
- important tool/environment state;
- execution trajectory or a bounded diagnostic representation;
- deterministic outcomes;
- semantic grader evidence where required;
- user correction or observed failure;
- whether the task succeeded despite an inefficient or fragile path.

Do not retain secrets or unnecessary private content merely to make future analysis convenient.

The receipt is referenced evidence, not a second copy of trajectory or Evolution Runner state. Pre-instrumentation sessions without a contemporaneous receipt remain unknown for serving even if their model/runtime can be recovered.

## 2. Attribute the failure before editing

A bad outcome does not automatically mean a skill needs another rule.

Classify the evidence among possibilities such as:

- routing failure;
- ambiguous description;
- missing or incorrect workflow rule;
- sufficient rule not followed by the model;
- tool failure;
- environment or dependency failure;
- evaluator error;
- task outside the claimed capability;
- local specialization mistaken for a shared requirement.

An edit is justified only when the attributed failure is actually addressable by that edit.

## 3. Extract trajectory-local lessons

Analyze successful and failed trajectories independently before trying to write a universal rule.

A local lesson should state:

- what decision point mattered;
- what evidence was available at that point;
- which action helped or failed;
- what boundary or alternative explains the outcome;
- how certain the lesson is;
- what additional contrasting trajectory could falsify it.

Do not force local lessons into canonical prose yet.

## 4. Consolidate across experience

Pool diverse local lessons and cluster them by semantic mechanism rather than wording.

During consolidation:

- merge duplicate lessons;
- retain material counterexamples;
- separate compatible branches from true contradictions;
- distinguish source-specific facts from transferable decision policies;
- identify whether a repeated failure is actually one upstream root cause;
- preserve exceptions that determine scope;
- prefer one rule that explains several failures over several symptom rules.

A broad rule requires broader evidence than a local patch.

## 5. Form the smallest improvement claim

Before editing, state one falsifiable behavior claim, for example:

```text
When condition C is observable, rule R should cause the agent to choose action A
more reliably than the current canonical behavior without regressing cases B and D.
```

The claim defines what evidence matters. Avoid vague objectives such as "make the skill smarter" or "improve robustness" without observable behavior.

Run the deletion test on the proposed rule: if removing it would leave the demonstrated gap closed, the rule is not necessary.

## 6. Produce a bounded candidate edit

Prefer localized `add`, `delete`, `replace`, `move`, or branch/reference changes over full rewrites.

Use a broad rewrite only when evidence shows that the existing structure itself prevents correct behavior.

Keep candidate changes small enough that a regression can be attributed to the changed mechanism.

When the candidate is a new skill, first test whether the behavior can be expressed as:

- a stronger existing rule;
- a conditional branch;
- a reference loaded only for one mode;
- a specialist extension;
- an architecture mechanism that does not need a user-facing skill.

## 7. Separate proposal data from acceptance data

The experience used to discover a rule may not also be the sole proof that the rule generalizes.

Use:

- proposal/training trajectories to generate the candidate;
- held-out or deliberately contrasting tasks to test transfer;
- previous regression cases to protect retained behavior;
- an external domain or execution setting when the claim is cross-domain or cross-runtime.

If no independent acceptance evidence exists yet, keep the candidate pending or explicitly local.

## 8. Run an evaluation cascade

Use the cheapest reliable evidence first:

1. structural and schema validation;
2. deterministic task checks;
3. fresh agent baseline versus candidate executions;
4. qualitative judge only for irreducibly semantic dimensions;
5. transfer/held-out checks proportional to the claimed scope.

Stop the cascade when a decisive regression already invalidates the candidate. Do not spend model judgment to argue against failed deterministic evidence.

## 9. Accept, narrow, specialize, or reject

Possible outcomes:

- **retain** — demonstrated improvement at the claimed scope;
- **narrow** — improvement exists only under a tighter condition;
- **specialize** — useful behavior does not generalize enough for the shared owner;
- **merge** — several candidates reduce to one stronger mechanism;
- **reject** — no reliable improvement or material regression;
- **evaluator-fix** — the candidate exposed a broken acceptance test rather than a skill defect.

Do not hide a severe local regression inside an improved aggregate score.

## 10. Keep negative learning without prompt bloat

A rejected edit can be valuable memory.

Retain a concise negative lesson when it prevents repeated rediscovery, such as:

- the failed mechanism;
- why it failed;
- the scope tested;
- the evidence that would justify reconsideration.

Do not preserve full rejected source prose or every failed prompt attempt.

Negative memory belongs in evolution evidence, not automatically inside runtime skill instructions.

## 11. Slow consolidation

Fast local improvements and slow library cleanup are different loops.

Periodically review accumulated retained and rejected lessons for:

- duplicate rules;
- rules that no longer change behavior;
- contradictions created by local patches;
- over-specific examples that can be replaced by a decision policy;
- specialist knowledge leaking into meta capabilities;
- repeated patterns that justify a shared mechanism;
- rules whose source assumptions are obsolete.

Compression must preserve proven behavior. Shorter is not automatically better.

## 12. Learn retrieval and memory policy too

Do not assume that only skill prose can evolve. Failures may arise from how experience is stored, retrieved, or presented.

Treat **memory content** and **retrieval policy** as different objects. What the system remembers may be correct while the policy that decides when, how, and how much to retrieve is wrong. Diagnose those failure classes separately before changing either one.

Treat these as learnable objects when evidence supports it:

- what experience is worth retaining;
- how observations are compressed into memory units;
- provenance, time, scope, confidence, and supersession metadata attached to those units;
- which memories are retrieved for a new task;
- whether retrieval should happen at all;
- how exact state-matching evidence is separated from analogy or merely similar prior experience;
- how retrieved evidence is ranked, filtered, decomposed, or fused;
- how much retrieved context is exposed to the agent;
- when low-confidence retrieval needs verification or a second retrieval path;
- when old memory should be merged, superseded, quarantined, or ignored;
- how routing metadata is structured for model-native selection.

When optimizing retrieval behavior, expose a **bounded, inspectable policy state** rather than asking an optimizer to rewrite the whole memory system. A candidate may change one or a small coherent set of retrieval dimensions, but the accepted state is still the best evidence-backed incumbent until a candidate beats it.

Use a closed loop analogous to other capability evolution:

```text
held-out retrieval tasks
        |
        v
 evaluate failures
        |
        v
 diagnose retrieval cause
        |
        v
 propose bounded policy change
        |
        v
 run candidate + regression/transfer checks
        |
    +---+---+
    |       |
 improve  regress
    |       |
    v       v
 retain   revert
```

A failure diagnosis is allowed to propose a previously absent retrieval dimension, such as query decomposition or an additional verification step, but a new dimension is still only a candidate. Require evidence that it improves the underlying task contract and test transfer before promoting it into shared policy.

Keep best-known recoverable state so memory-policy experimentation can revert cleanly. Do not let exploratory policy mutation overwrite the incumbent before acceptance evidence exists.

Changes to memory/retrieval policy pass the same baseline, held-out, evaluator, transfer, and regression gates as skill edits.

Do not turn benchmark-specific retrieval knobs, fixed fusion weights, context sizes, iteration counts, or stopping thresholds into universal runtime policy.

## 13. Learn the learning procedure cautiously

The evolution mechanism itself can be improved from evidence: analyst prompts, consolidation strategy, candidate mutation format, judge rubrics, retrieval structure, and acceptance sequencing are all replaceable.

However, a self-improvement procedure must never be able to silently weaken its own acceptance contract merely because doing so increases its score.

The stable outer constraints are:

- explicit task contract;
- independent evidence where possible;
- no hidden material regression;
- authorization and trust boundaries;
- provenance of retained behavior;
- ability to revert a bad shared change.

## Experience-to-skill pipeline

```text
real executions / user corrections / source mechanisms
                      |
                      v
              bounded experience pool
                      |
                      v
             trajectory-local lessons
                      |
                      v
        hierarchical semantic consolidation
                      |
                      v
           smallest improvement claim
                      |
                      v
               bounded candidate edit
                      |
             +--------+--------+
             |                 |
             v                 v
        held-out tasks     regression suite
             |                 |
             +--------+--------+
                      v
             deterministic evidence
                      |
                      v
          independent semantic judgment
               when necessary
                      |
                      v
       retain / narrow / specialize / reject
                      |
                      v
             slow library consolidation
```

## Success criterion

The learning loop succeeds when future agents perform better because past experience was converted into transferable decision structure, while the runtime library remains smaller and more reliable than the raw experience that produced it.
