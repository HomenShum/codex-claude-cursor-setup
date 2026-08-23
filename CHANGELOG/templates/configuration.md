# Configuration template changelog

## 2026-08-23 — Add copy-safe configuration examples

- Commit: `79508f0`
- User outcome: a team can start from parsed, permission-gated examples and
  supply credentials by environment-variable name. Codex MCP examples are
  disabled; Claude project MCP remains subject to each user's approval.
- Source: current vendor configuration, MCP, skills, and memory documentation.
- Files: `templates/`.
- Verification: JSON/TOML parsing and repository secret scan.
- Caveats: every project must choose its own permission policy.
