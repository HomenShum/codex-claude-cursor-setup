# Current handoff

- Owner: repository maintainer
- Goal: maintain a public, product-neutral setup for Codex, Claude Code, and Cursor
- Current state: three-host executable harness implementation is locally complete; the named proof below passes, but publication is blocked by reachable-history proof
- Canonical instructions: `AGENTS.md`
- Canonical skills: `templates/project/.agents/skills`
- Named proof receipts:
  - `python scripts/validate_repo.py` -> PASS
  - `python -m unittest discover -s tests -v` -> 184 tests passed; 2 platform-inapplicable FIFO scenarios skipped on Windows
  - `python scripts/agent_preflight.py --config templates/harness/preflight.json` -> all seven layers passed
  - `python scripts/prove_preflight_mutations.py` -> 30 tests, 0 failures, 0 errors, 1 platform-inapplicable skip
  - `python scripts/validate_repo.py --check-external` -> 183 bounded external URL checks passed
  - `python -m compileall -q scripts tests`, `git diff --check`, and `python scripts/check_claim_language.py HANDOFF.md handoffs/0001/HANDOFF.md` -> PASS
  - Visual proof -> N/A; this change has no user-interface surface
- Privacy boundary: current publishable files pass the private-marker scan; `python scripts/check_private_history.py` exits 1 against the existing reachable history and reports only a redacted object identifier
- Recommendation: create a fresh reviewed history for publication; use an explicitly authorized history rewrite only if preserving the existing public repository identity is mandatory
- External action: none; no commit, push, history rewrite, or publication was performed
- Remote observation: `origin/main` remained at `03fd1b8040846b77a07dbcc40a634d9829029cfb` during the final local audit
- Next reader: inspect the complete working-tree inventory, preserve the passing receipts, resolve the reachable-history blocker, rerun every named proof, and publish only after explicit authorization
