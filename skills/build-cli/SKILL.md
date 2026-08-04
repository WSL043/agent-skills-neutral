---
name: build-cli
description: "Design and implement command-line interfaces with coherent commands, arguments, configuration precedence, structured output, exit codes, and automated tests. Use for new CLIs or substantial command-surface changes."
---

# Build CLI

## Goal

Deliver a scriptable CLI that is discoverable for humans and stable for automation.

## Workflow

1. Map user jobs to a small command hierarchy and define examples before implementation.
2. Specify positional arguments, options, defaults, environment variables, config files, and their precedence.
3. Separate parsing, domain logic, I/O adapters, and presentation.
4. Implement consistent help, diagnostics, progress behavior, output formats, and exit codes.
5. Test happy paths, invalid input, missing dependencies, interrupted execution, and machine-readable output.
6. Package and run the installed entry point from a clean environment.

## Decision rules

- Use subcommands when operations have distinct arguments or side effects.
- Send data to stdout and diagnostics to stderr; offer JSON for machine consumers.
- Prefer non-interactive defaults when stdin is not a terminal.

## Guardrails

- Do not print secrets or include them in process arguments when safer channels exist.
- Do not return exit code zero after partial or failed work.
- Do not change existing command semantics without migration guidance.

## Completion evidence

- Help output, installed invocation, exit codes, and representative shell pipelines behave as documented.
- Tests cover parsing separately from domain behavior.

## Related skills

- `verify-completion`

## Provenance

This is an original vendor-neutral synthesis. Source implementation pointers and snapshot commits are recorded in [`../../provenance.json`](../../provenance.json); upstream text, scripts, and assets are not bundled here.
