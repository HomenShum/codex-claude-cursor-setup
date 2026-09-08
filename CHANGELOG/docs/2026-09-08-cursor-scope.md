## 2026-09-08 — Clarify Cursor authority and execution scope

- Commit: candidate.
- Touches: `CHANGELOG/docs/setup-guide.md`, `CHANGELOG/scripts/validator.md`.
- User outcome: a setup reader can distinguish team-controlled permissions,
  local Auto-review guidance, supported command sandbox restrictions, and the
  optional Agent CLI controls; existing users can find the repository migration
  guide and use the canonical clone name in setup commands.
- Source: Cursor's [permissions reference](https://cursor.com/docs/reference/permissions),
  [Run Modes](https://cursor.com/docs/agent/security/run-modes),
  [sandbox reference](https://cursor.com/docs/reference/sandbox),
  [CLI overview](https://cursor.com/docs/cli/overview), and
  [skills reference](https://cursor.com/docs/skills), accessed 2026-09-08.
- Files: `README.md`, `docs/setup.md`, `docs/capability-matrix.md`.
- Changes: document team precedence, separate guidance from OS sandbox
  restrictions, name effective network modes and persistent CLI sandbox
  controls, and explain which local skills are unavailable to remote workers.
- Verification: compare the edited passages with the cited primary sources;
  the publication workflow runs repository validation and scenario gates.
- Caveats: this is a scoped Cursor documentation check, not a fresh verification
  of every host path or a native host-runtime smoke test.
