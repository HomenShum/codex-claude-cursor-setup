# Current handoff

Before: the kit already compared saved learning runs and kept outcome events, but a consumer had no integrated per-case review page or explicit scoped upstream viewer recipe.

Fix: add learning_review.py around the existing comparator and agent_flow_outcome.py around the existing outcome ledger parser. The latter serves only the exact reviewed Agent Flow assets, binds every receipt to the one byte snapshot parsed, and preserves prior record prefixes. Both retain existing human authority boundaries.

After: the [observable learning proof](docs/observable-learning-proof.md) records the synthetic comparison, actual ledger arrival, clean pinned viewer build, dirty-asset refusal and repository gates. No model improvement or activation is claimed. The [recipe](docs/observable-learning.md) contains runnable commands.

Prevention: scenario tests cover source/policy drift, one-case regression, private-field exclusion, source rewrite, modified generated assets, malformed inputs, unsafe paths and HTTP refusals. Current checks belong to this change; older handoff test counts are historical.

Remaining: independently verify production source authenticity, heldout isolation, judge calibration and human acceptance in the target project. Cross-platform CI and public content readback must be checked at the published SHA. The upstream mobile toolbar remains wider than a narrow viewport; only the scope notice was verified there. No dispatcher, host hook or scheduler was installed.

Handoff: the repository maintainer owns review and publication. Canonical destination is HomenShum/codex-claude-cursor-setup, repository ID 1344270714. Preserve existing subscriber configurations and the inactive-by-default host examples. Do not treat numerical eligibility or a ledger actor string as approval.

Reproduce from the root:

```bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
python scripts/agent_preflight.py --config templates/harness/preflight.json
python scripts/prove_preflight_mutations.py
python scripts/validate_repo.py --check-external
python scripts/check_private_history.py
git diff --check
```
