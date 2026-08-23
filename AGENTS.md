# Repository instructions

This repository is a public, vendor-neutral setup kit for OpenAI Codex and
Anthropic Claude Code. It contains documentation, safe configuration examples,
and validation code. It does not contain credentials, copied session history,
private project source, or machine-specific configuration.

## Sources of truth

- `README.md` is the shortest supported path for a new user.
- `docs/setup.md` owns installation, file placement, and configuration scope.
- `docs/mcp-and-agent-bridges.md` owns MCP and cross-agent setup.
- `docs/skills-plugins-hooks.md` owns reusable workflow extensions.
- `sources/external-projects.json` is the machine-readable third-party ledger.
- `sources/official-docs.json` is the machine-readable vendor-document ledger.
- `templates/` contains examples only. No example may contain a working token,
  private hostname, personal absolute path, or destructive default.

## Change rules

- Check current OpenAI and Anthropic documentation before changing a product
  command or configuration key. Record the access date.
- Add every deliberately used or recommended GitHub repository to
  `sources/external-projects.json` and `docs/external-projects.md`.
- Keep `AGENTS.md` canonical. Root `CLAUDE.md` imports it and may add only
  Claude Code-specific guidance.
- Put credentials in environment variables or an external secret store. Never
  place them in command arguments, MCP URLs, committed JSON, or TOML.
- Hooks execute code with the user's authority. Examples must be disabled by
  default and must explain their trigger, inputs, side effects, and rollback.
- Preserve the distinction between guidance and enforcement: instruction files
  guide a model; permissions, hooks, CI, and server-side authorization enforce
  policy.
- Update the relevant append-only `CHANGELOG/` lane for substantive changes.

## Verification

Run from the repository root:

```bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
python scripts/validate_repo.py --check-external
git diff --check
```

The external check requires network access. Offline validation and scenario
tests must pass without credentials or network access.

## Completion bar

A change is complete only when a new user can identify where each file belongs,
the templates parse, every local link resolves, all external projects are
attributed, the secret scan is clean, and the scenario suite passes. A green
command is evidence for that command only; do not call remote content published
until the public repository is fetched and the promised files are observed.
