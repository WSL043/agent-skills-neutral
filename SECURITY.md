# Security Policy

SkillConverge continuously inspects third-party Agent Skills. Discovery is therefore a supply-chain boundary, not a trust signal.

## Report a security issue

Do not publish exploit details, credentials, or sensitive reproduction material in a public issue. Use GitHub's private vulnerability reporting for this repository when available. If private reporting is unavailable, contact the repository owner privately through the contact method exposed on their GitHub profile and include only the minimum information needed to establish contact.

## Untrusted upstream rule

Everything discovered outside the canonical `skills/` tree is untrusted until reviewed.

An entry in `upstreams.json` means only that a repository is worth watching. It does not authorize execution, installation, network access, secret access, or adaptation.

Discovery and scheduled automation may inspect repository metadata, commit identifiers, file paths, and other non-executable structure. They must not execute upstream scripts or import upstream instructions into the canonical runtime automatically.

## Promotion security gate

Before upstream behavior is retained, inspect the relevant instructions and executable artifacts for:

- prompt injection or instructions that attempt to override the host/user contract;
- credential, token, environment-variable, browser-session, or local-file access unrelated to the stated capability;
- data exfiltration or unexplained network destinations;
- destructive commands, persistence, privilege escalation, or opaque installers;
- dependency or binary provenance that cannot be reasonably inspected;
- hidden provider coupling or external side effects that the canonical skill would fail to disclose.

Security findings are claims and still require evidence, but a source with unresolved material risk is not eligible for automatic promotion.

## Canonical skills are not a security certification

The canonical library is filtered and reviewed, but inclusion does not prove absence of every malicious pattern or vulnerability. Runtime authorization, repository policy, sandboxing, and current security guidance remain authoritative.

For third-party skill scanning, dedicated tools such as static, behavioral, and semantic scanners may be used as evidence, but no scanner result replaces review of the actual trust boundary.
