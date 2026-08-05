# Handoff schema

Use JSON so a new agent can validate the snapshot deterministically.

```json
{
  "schema_version": "1.0.0",
  "generated_at": "ISO-8601 UTC timestamp",
  "workspace": {
    "root": "absolute path when useful",
    "repository": "owner/name or null",
    "branch": "branch or null",
    "base_revision": "commit or null"
  },
  "task": {
    "goal": "one sentence",
    "acceptance_criteria": ["testable outcome"],
    "non_goals": ["explicit exclusion"]
  },
  "current_state": "short factual summary",
  "completed": [
    {
      "claim": "past-tense result",
      "evidence": ["command, artifact, commit, or safe source reference"]
    }
  ],
  "pending": [
    {
      "action": "imperative next step",
      "prerequisites": ["condition that must still hold"],
      "verification": ["how to prove completion"]
    }
  ],
  "constraints": ["non-negotiable rule"],
  "decisions": [
    {
      "decision": "chosen approach",
      "rationale": "why it was chosen",
      "alternatives": ["rejected option"],
      "reopen_if": ["evidence that invalidates the decision"]
    }
  ],
  "open_risks": [
    {
      "risk": "known issue or uncertainty",
      "status": "unverified | confirmed | blocked",
      "evidence": ["safe reference"]
    }
  ],
  "files": [
    {
      "path": "repo-relative path",
      "status": "created | modified | deleted | read-only",
      "note": "what matters to continuation"
    }
  ],
  "artifacts": [
    {
      "path_or_url": "safe reference",
      "purpose": "why the next agent may need it"
    }
  ],
  "next_action": "first valid pending action",
  "resume_prompt": "compact, ready-to-use instruction naming this handoff"
}
```

Rules:

- Keep completed claims evidence-backed; an unrun check belongs in `pending` or `open_risks`.
- Preserve exact paths, symbols, error text, and commit IDs when they matter.
- Use empty arrays instead of omitting required collections.
- Point to large logs, screenshots, plans, and research artifacts rather than copying them.
- Never store tokens, cookies, passwords, private keys, QR payloads, or other raw credentials.
