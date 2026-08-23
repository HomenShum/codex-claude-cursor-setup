# Security and publication checklist

The main risk is not that a template fails to parse. It is that a working
local setup quietly contains credentials, session data, private paths, or
executable trust decisions that become public with it.

## Threat model

| Asset | Common failure | Control |
|---|---|---|
| API and OAuth credentials | Token committed in config, URL, shell argument, or log | Environment-variable name only; secret manager; pre-push scan; rotate on exposure |
| Private source and history | Whole worktree or home directory copied into a public repo | Fresh allowlisted repository and fresh Git history |
| Agent sessions and memory | Cache/database/transcript copied as setup | Exclude session stores entirely |
| Workstation identity | Absolute paths, usernames, tenant names, hostnames | Portable placeholders and path scan |
| Tool authority | Broad MCP or hook silently enabled | Narrow scope, explicit approval, disabled-by-default examples |
| Supply chain | Unpinned or unattributed skill/plugin changes | Canonical source, revision, license, and access date ledger |
| False completion | CLI says success but public artifact is absent or stale | Fetch the public repository and inspect exact content signals |

## Before the first commit

- Build the public repository from an explicit file allowlist.
- Never recursively copy `.codex`, `.claude`, `.env`, browser state, worktrees,
  caches, databases, terminal captures, or ignored files.
- Search content and filenames for secret patterns and personal absolute paths.
- Keep this documentation repository text-only: every regular publication file
  must be UTF-8, no larger than 1 MiB, and within the validator's 2,000-file
  cap. Link to large or binary evidence instead of hiding it from the scan.
- Parse every JSON and TOML template.
- Resolve every relative Markdown link.
- Ensure every cited GitHub repository appears in the attribution ledger.
- Review the Git author identity and commit message before publishing.

Run:

```bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
git diff --check
```

## Before every push

- Inspect `git status`, the staged diff, and the exact files that will leave
  the machine.
- Confirm examples contain variable names, never values.
- Treat tool listings and screenshots as sensitive until sanitized.
- Re-run the offline checks.
- Run `python scripts/validate_repo.py --check-external` when links changed or
  on a scheduled trusted runner.

## After publishing

Fetch raw public content rather than trusting a push exit code. Verify the
default branch contains at least `README.md`, `SECURITY.md`, the machine-readable
source ledgers, and the validator. Confirm the repository's declared visibility
through the hosting API.

## If a credential is exposed

1. Revoke or rotate it immediately at its issuer.
2. Check access logs and reduce the replacement credential's scope.
3. Remove it from all reachable history and artifacts using the host's
   documented incident process.
4. Invalidate caches and rebuild affected artifacts.
5. Record the incident without reproducing the secret.

Deleting the latest line is not containment: earlier commits, terminal logs,
CI output, screenshots, and indexing systems may retain it.
