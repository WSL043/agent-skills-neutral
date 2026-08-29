---
name: threat-model-system
description: "Threat-model a system by identifying assets, actors, trust boundaries, attack surfaces, abuse cases, and mitigations grounded in the actual architecture. Use before security-sensitive design, during major architecture change, or to scope a security review."
---

# Threat Model System

## Goal

Produce a prioritized threat model that connects realistic attacker goals to system controls and verification work.

## Workflow

1. Define scope, deployment, data classification, critical assets, users, administrators, and external actors.
2. Draw data flows, entry points, trust boundaries, privileged components, dependencies, and operational control planes.
3. Enumerate attacker goals and abuse cases per boundary, including identity, data, availability, supply chain, and tenant isolation.
4. Trace attack paths from reachable entry to impact and record required preconditions.
5. Map preventive, detective, and recovery controls; identify gaps and control owners.
6. Prioritize threats by likelihood, impact, exposure, and evidence, then define validation and residual risk.

## Decision rules

- Use diagrams only at the granularity needed to expose trust transitions.
- Separate assumed controls from verified controls and planned controls.
- Revisit the model when architecture, identity, data, or deployment changes.

## Guardrails

- Do not produce a generic threat list disconnected from components and flows.
- Do not include exploit steps that exceed the authorized defensive purpose.
- Do not assign risk without naming impact and preconditions.

## Completion evidence

- Assets, boundaries, threats, controls, owners, and residual risks are linked.
- High-priority threats have concrete validation or mitigation tasks.

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
