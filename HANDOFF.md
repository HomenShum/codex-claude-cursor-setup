# Current handoff

- Owner: repository maintainer
- Goal: maintain one public setup kit for Codex, Claude Code, and Cursor
- Canonical destination: `HomenShum/codex-claude-cursor-setup`
- GitHub repository identity: `1344270714`, the original two-host repository
- Current change: integrate the later kit, sanitize two original historical
  validator changesets with owner approval, and document precise Cursor scope
- Canonical instructions: `AGENTS.md`
- Canonical skills: `templates/project/.agents/skills`
- Migration and subscriber instructions: [repository migration](docs/repository-migration.md)
- Required proof: `CANONICAL-THREE-HOST-01` — original GitHub identity, clean
  advertised history, reviewed current files, public content readback, and
  Windows/macOS/Linux CI at the published SHA
- Reproduce locally:
  - `python scripts/validate_repo.py`
  - `python -m unittest discover -s tests -v`
  - `python scripts/agent_preflight.py --config templates/harness/preflight.json`
  - `python scripts/prove_preflight_mutations.py`
  - `python scripts/validate_repo.py --check-external`
  - `python scripts/check_private_history.py` in a full clone
  - `git diff --check`
- Current remote validation: [GitHub Actions](https://github.com/HomenShum/codex-claude-cursor-setup/actions)
- Proof boundary: use the run for the exact published SHA; historical handoffs
  and old test counts are not current receipts. UI proof is not applicable to
  this documentation/template migration. Actual host login, live MCP/provider
  sessions, hosted tracing, and Cloud/SSH runtime behavior remain user smoke checks.
- Privacy boundary: no private app source or runtime state is imported. Rewritten
  advertised history does not erase previous clones or hosting-provider caches.
