# Setup guide changelog

## 2026-08-23 — Publish one cross-client setup path

- Commit: `79508f0`
- User outcome: a newcomer can configure Codex and Claude Code around one
  shared project contract without copying private machine state.
- Source: current OpenAI and Anthropic installation, settings, instruction,
  MCP, skills, plugins, and hooks documentation.
- Files: `README.md`, `docs/`, `AGENTS.md`, `CLAUDE.md`, and source ledgers.
- Verification: offline validator, 11-scenario suite, and 129 bounded external
  links passed. After the initial push, GitHub reported `PUBLIC` with `main` as
  default; anonymous raw fetches returned HTTP 200 for the README title signal
  and a 111-project machine ledger at remote commit `79508f0`.
- Caveats: vendor documentation is mutable; access dates are recorded.
