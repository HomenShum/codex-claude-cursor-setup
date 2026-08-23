# Validator changelog

## 2026-08-23 — Add bounded publication checks

- Commit: `candidate`
- User outcome: a maintainer can detect secrets, private paths, broken local
  links, invalid templates, missing attribution—including non-URL GitHub
  Actions references—and stale external sources.
- Source: observed publication and agent-tool failure modes.
- Files: `scripts/validate_repo.py`, `tests/test_setup_scenarios.py`, and CI.
- Verification: scenario tests cover normal, adversarial, degraded, concurrent,
  burst, and sustained-use behavior. Every regular publication file is scanned
  as bounded UTF-8 input, including uncommon credential-file extensions.
- Caveats: pattern scans supplement review; they cannot prove no secret exists.
