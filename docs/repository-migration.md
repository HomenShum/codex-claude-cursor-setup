# Canonical repository and subscriber upgrade

A developer following the original two-host kit should receive the same
maintained project, not have to discover a second repository. The canonical
destination is [codex-claude-cursor-setup](https://github.com/HomenShum/codex-claude-cursor-setup),
renamed in place from `HomenShum/codex-claude-code-setup`. Its GitHub repository
ID is **1344270714**. The separate
[coding-agent-setup](https://github.com/HomenShum/coding-agent-setup) was an
intermediate publication, not the original repository under another name.

## What existing subscribers gain

The original-to-intermediate comparison contained **181 changed files**
(17,593 insertions and 692 deletions), before the canonical-destination and
Cursor corrections in this release. This is not merely a seven-file update.
The intermediate source is retained through commit `1f50906`.

| Surface | Original two-host baseline | Integrated kit and exact entry point |
|---|---|---|
| Host setup | Codex and Claude Code | Cursor desktop and optional Agent CLI; platform and remote-session distinctions in [setup](setup.md) and [capability matrix](capability-matrix.md) |
| Instructions and extensions | Shared instructions and starter examples | One canonical `.agents/skills` tree, 18 portable skills, verified Claude mirror, native three-host MCP/hooks/subagents under [templates](../templates/) |
| Delegation | Proof-workflow guidance | Bounded planner, workers, and independent judge with receipts in [agent stack](agent-stack.md) |
| Continuity and verification | Publication validator | Seven-layer preflight, deliberate failure mutations, handoff/state validation, and claim reconciliation in [preflight and continuity](preflight-and-continuity.md) |
| Evidence application bootstrap | No equivalent end-to-end starter contract | Scope-authorized context discovery and reuse, data sourcing/curation, tracing, assistant-style UI proof, and acceptance criteria in [one-prompt bootstrap](one-prompt-bootstrap.md) |
| Evaluation and improvement | No equivalent executable comparison kit | Descriptive Boolean gates, 1–5 grades with rationale, split-bound comparison and guarded promotion in [learning templates](../templates/learning/README.md) |
| Durable outcomes and deployment | No equivalent profile/ledger kit | Append-only outcomes and explicit deployment profiles in [outcome lifecycle](outcome-lifecycle.md) and [enterprise deployment](enterprise-deployment.md) |
| Existing-project adoption | Manual setup copying | Read-only missing/conflict plan plus explicit missing-file apply through `scripts/setup_project.py`; existing files are not silently overwritten |
| Attribution and privacy | 111 external repositories and 19 vendor references | All original references retained; current source relationships, digest-only privacy policy, and full reachable-history CI added |

Cursor-specific corrections in this release distinguish administrative policy
from local configuration, Auto-review/allowlists from OS sandbox enforcement,
and CLI sandbox controls from desktop policy. Native examples remain inert.
See [Cursor scope corrections](../CHANGELOG/docs/2026-09-08-cursor-scope.md).

## Why the original commit hashes changed

The owner approved sanitizing two original commits because the old privacy
validator embedded an excluded source identifier in its own constants. Only
that historical validator file was changed; the check now uses a digest rather
than a literal identifier. Original changeset metadata and other file contents
were retained. The later kit's history is merged without rewriting its commits.
The cleaned original changesets are `e61ced4` and `7edb7ae`.

Renaming preserves the GitHub repository identity and redirects ordinary old
repository URLs, but do not reuse the old name. History rewriting changes Git
ancestry and does not erase previous clones or cached objects. These are
different operations. [GitHub rename guidance](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository),
[GitHub history-removal guidance](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository).

## Upgrade safely

1. In your existing clone, run `git status --short` and preserve any local work
   privately. Do not merge the old original history into the rewritten main.
2. Clone into a **new directory**. Keep the old clone private until you have
   reviewed and moved only the changes you need; do not delete local work.

   ```bash
   git clone https://github.com/HomenShum/codex-claude-cursor-setup.git
   cd codex-claude-cursor-setup
   python scripts/validate_repo.py
   python -m unittest discover -s tests -v
   python scripts/check_private_history.py
   ```

3. If your project already copied kit files, use the [adoption sequence](setup.md)
   to inventory missing files and conflicts. A repository rename does not
   update project copies, personal settings, installed skills, or credentials.
4. Review root `CLAUDE.md` manually: this kit now uses import-only
   `.claude/CLAUDE.md` and separate `.claude/rules/`. Preserve your project-specific
   instructions before removing an obsolete duplicate. Canonical project
   skills stay in `.agents/skills`; synchronize the Claude mirror after review.
5. Review effective host permissions, approve each desired MCP integration,
   and perform the harmless host-native smoke checks in the setup guide.
   Offline CI cannot prove account login, team policy, Cloud/SSH propagation,
   live Langfuse/provider access, or a finished product's UI.

If you follow the intermediate repository, its history is an ancestor of this
kit, but a fresh clone is still the simplest unambiguous migration. Do not use
`--allow-unrelated-histories` to combine an old original checkout with the new
main; that can reintroduce the excluded history.

## Maintainer publication checklist

Before any push, name the intended repository and check its identity:

```bash
git remote get-url origin
gh api repos/HomenShum/codex-claude-cursor-setup --jq '{id,full_name,default_branch}'
git ls-remote origin refs/heads/main
```

Require ID `1344270714`, canonical name, and the expected remote head. Stop on
any mismatch. A successful push or `HEAD == origin/main` alone cannot identify
the intended repository. This is an explicit maintainer check, not an automatic
property of the source validator.

Run all commands in [AGENTS.md](../AGENTS.md), plus the full-history gate.
After a push, confirm the remote SHA, inspect anonymous raw README, Cursor
templates, and this guide, and check the latest three-platform CI results.
Use a full fresh clone for history proof; never use shallow or replacement-ref
views as evidence. Only the authorized migration uses an explicit
`--force-with-lease=refs/heads/main:<expected-old-sha>`; routine updates use
normal pushes. [Git lease semantics](https://git-scm.com/docs/git-push).

For recovery, preserve private backups and apply a new corrective commit.
Do not restore contaminated public refs as a shortcut. GitHub may retain
unreachable old objects; a clean advertised-ref scan is not a claim that every
previous copy has disappeared.
