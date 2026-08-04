---
name: build-mcp-server
description: "Design and implement Model Context Protocol servers with well-scoped tools, resources, schemas, error handling, and evaluation. Use when exposing an API, datastore, or local capability to MCP-compatible agents."
---

# Build MCP Server

## Goal

Deliver an MCP server whose tools are predictable, safe, discoverable, and easy for agents to call correctly.

## Workflow

1. Inventory target operations, authentication, data sensitivity, latency, pagination, and destructive effects.
2. Choose tools for actions, resources for readable context, and prompts only for reusable interaction templates.
3. Design narrow verb-led tool names and explicit input/output schemas with bounded defaults.
4. Implement transport-independent domain logic, then attach the chosen MCP SDK and transport adapter.
5. Return structured errors that distinguish invalid input, authorization, upstream failure, timeout, and partial completion.
6. Exercise discovery, successful calls, malformed inputs, permission failures, pagination, and cancellation with an MCP client.

## Decision rules

- Split a tool when one schema contains unrelated modes or mutually exclusive parameter families.
- Require explicit confirmation fields for irreversible actions when the host cannot provide an approval gate.
- Use resources instead of giant tool responses for stable or browsable context.

## Guardrails

- Never place credentials in tool descriptions, logs, examples, or returned errors.
- Do not expose broad shell, SQL, or filesystem execution when a constrained operation is possible.
- Document read, write, and destructive semantics in descriptions.

## Completion evidence

- Schema validation and MCP discovery succeed from a clean client.
- Representative success and failure calls return stable structured results.
- Authentication and destructive-action boundaries are tested.

## Related skills

- `threat-model-system`
- `verify-completion`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
