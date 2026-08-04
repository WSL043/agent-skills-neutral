# Implementation variants

## Strict cycle

Use an uncompromising red-green-refactor gate when premature implementation is the dominant failure mode. Record the red failure before editing production code.

## Domain-quality layer

Name tests in the problem vocabulary, prefer observable behavior over collaboration details, and select the test boundary based on the actual risk.
