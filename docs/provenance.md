# Provenance and exclusions

This repository is a clean, public synthesis created on 2026-08-23 from three
evidence classes:

1. current OpenAI and Anthropic documentation;
2. public repositories and skills directly used or cited during prior agentic
   development work;
3. observed configuration patterns from a private working environment.

## What was generalized

- the shared `AGENTS.md` plus thin `CLAUDE.md` import pattern;
- separation of personal, project, and local scope;
- MCP setup for local servers and bounded agent-to-agent review;
- skill discovery and canonical-source guidance;
- proof-oriented handoff, scenario testing, and public-content verification;
- attribution and security checks that can run without vendor credentials.

The text and templates here were written anew. They do not copy private
application source or session transcripts.

## What was deliberately excluded

- live or expired secret values and any credential-bearing command lines;
- authentication stores, chats, memories, local databases, caches, browser
  profiles, generated worktrees, and ignored runtime directories;
- personal absolute paths, private repository URLs, deployment identifiers,
  and account metadata;
- private application implementation, fixtures, evidence captures, and Git
  history;
- stale instructions that referenced deleted code paths;
- historical commands that pushed directly to a protected branch, destructively
  restored files, or launched unsupported platform entry points;
- installed tools whose canonical source or license could not be established.

## Attribution method

`sources/external-projects.json` records external repositories with their role,
relationship, revision evidence when available, license status, and access
date. `docs/external-projects.md` renders the same decision context for humans.
`sources/official-docs.json` records mutable vendor documentation separately.

“Used” means direct installation, copied/inspired workflow authority, runtime
dependency, or an explicitly recorded historical design influence. These
labels are not equivalent, so the ledger preserves the relationship instead
of presenting every project as a dependency.

License labels are discovery aids, not legal advice. A public repository is
not automatically open source, and this repository's MIT license applies only
to original material here.
