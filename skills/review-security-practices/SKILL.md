---
name: review-security-practices
description: "Review code and configuration for language- and framework-appropriate security practices using evidence from the actual data flow and deployment model. Use for secure-coding assessment, hardening review, or security-focused implementation guidance."
---

# Review Security Practices

## Goal

Identify concrete security weaknesses and prioritized hardening actions without producing generic checklist noise.

## Workflow

1. Define scope, assets, trust boundaries, attacker capabilities, deployment model, and applicable framework versions.
2. Trace authentication, authorization, input parsing, secrets, storage, cryptography, logging, network calls, and dependency use.
3. Compare implementation against current official framework and language guidance.
4. Validate candidate issues through reachable paths, existing controls, and realistic impact.
5. Prioritize fixes by exploitability, impact, exposure, and change risk; include a verification method.
6. Recheck the final code or configuration after hardening changes.

## Decision rules

- Use a threat model first when scope or attacker goals are unclear.
- Treat defense-in-depth gaps separately from directly exploitable vulnerabilities.

## Guardrails

- Do not run destructive proof-of-concept attacks against live systems without explicit authorization.
- Do not report a vulnerability from a dangerous-looking function name alone.
- Do not recommend obsolete controls or custom cryptography.

## Completion evidence

- Findings include location, mechanism, preconditions, impact, confidence, fix, and verification.
- Non-findings and blocked checks are distinguishable from reviewed-safe areas.

## Related skills

- `threat-model-system`
- `review-code`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
