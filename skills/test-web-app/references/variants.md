# Implementation variants

## Command or isolated-session adapter

Start a fresh browser/context for reproducible automation, capture logs and requests, and tear down all owned processes.

## Managed-server adapter

Wrap one or more local servers with readiness checks and guaranteed cleanup before running the browser flow.

Do not put client-specific REPL commands in the portable core. A runtime adapter may add persistent handles when that client supports them.
