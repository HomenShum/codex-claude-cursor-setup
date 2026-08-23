# Codex + Claude Code setup

A public, copy-safe setup for running OpenAI Codex and Anthropic Claude Code on
the same repositories without duplicating instructions or leaking local state.

The core decision is simple: keep one checked-in `AGENTS.md` as the shared
project contract, then let a thin `CLAUDE.md` import it with `@AGENTS.md`.
Configuration stays client-native because Codex uses TOML while Claude Code
uses JSON.

## What is included

- current install paths for Windows, macOS, Linux, and WSL;
- global and project instruction templates;
- safe Codex and Claude Code settings examples;
- project-scoped and user-scoped MCP examples;
- optional Codex-to-Claude and Claude-to-Codex MCP bridges;
- skills, plugins, hooks, and permission guidance;
- a complete ledger of directly used external repositories;
- offline validation, secret scanning, link checks, and scenario tests.

## Five-minute setup

### 1. Install the agents

Windows PowerShell:

```powershell
irm https://chatgpt.com/codex/install.ps1 | iex
irm https://claude.ai/install.ps1 | iex
```

macOS, Linux, or WSL:

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
curl -fsSL https://claude.ai/install.sh | bash
```

Then launch each once and complete its supported sign-in flow:

```bash
codex
claude
```

Verify the local installation instead of assuming it succeeded:

```bash
codex --version
claude --version
claude doctor
```

See the current [Codex CLI guide](https://learn.chatgpt.com/docs/codex/cli) and
[Claude Code setup guide](https://code.claude.com/docs/en/setup) before using
these commands in managed or automated environments.

### 2. Add personal working agreements

Review `templates/global/WORKING_AGREEMENTS.md`. If you do not already have
global instruction files, copy the reviewed content to:

| Agent | Personal instructions |
|---|---|
| Codex | `~/.codex/AGENTS.md` |
| Claude Code | `~/.claude/CLAUDE.md` |

Do not overwrite an existing file blindly. Merge the parts you want and keep
personal identifiers, private paths, and credentials out of shared repositories.

### 3. Add project instructions

Copy the project templates into a repository and replace every bracketed field:

```text
your-project/
├── AGENTS.md                  # canonical team instructions
├── CLAUDE.md                  # imports @AGENTS.md
├── .codex/config.toml         # optional Codex project settings
├── .claude/settings.json      # optional shared Claude settings
└── .mcp.json                  # optional Claude project MCP servers
```

Codex reads `AGENTS.md` directly. Claude Code composes `CLAUDE.md` files and
supports importing `AGENTS.md`; it does not treat `AGENTS.md` as an automatic
instruction source by itself. See the official
[Codex AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
and [Claude Code memory guide](https://code.claude.com/docs/en/memory).

### 4. Add tools only when a workflow needs them

Start with no MCP servers. Add one server for one concrete job, keep project
servers team-safe, and pass credentials by environment-variable name. The full
examples are in [MCP and agent bridges](docs/mcp-and-agent-bridges.md).

### 5. Validate before publishing

```bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
python scripts/validate_repo.py --check-external
```

The first two commands are offline. The last command verifies current official
pages and repository endpoints.

## Repository map

| Path | Purpose |
|---|---|
| [`docs/setup.md`](docs/setup.md) | installation, scope, settings, and migration |
| [`docs/mcp-and-agent-bridges.md`](docs/mcp-and-agent-bridges.md) | MCP and bounded cross-agent review |
| [`docs/proof-workflow.md`](docs/proof-workflow.md) | evidence loop, browser proof, and independent judgment |
| [`docs/skills-plugins-hooks.md`](docs/skills-plugins-hooks.md) | reusable workflows and executable extension boundaries |
| [`docs/security.md`](docs/security.md) | credential, permission, hook, and publication checks |
| [`docs/external-projects.md`](docs/external-projects.md) | human-readable attribution ledger |
| [`docs/provenance.md`](docs/provenance.md) | what was observed, generalized, or excluded |
| [`docs/troubleshooting.md`](docs/troubleshooting.md) | discovery, MCP, skill, and publication diagnosis |
| [`THIRD_PARTY.md`](THIRD_PARTY.md) | root attribution entry point |
| [`templates/`](templates/) | copy-and-adapt examples |
| [`sources/`](sources/) | machine-readable citations |
| [`scripts/validate_repo.py`](scripts/validate_repo.py) | deterministic validator and optional live link check |

## Design boundary

This repository documents a working setup; it is not an export of a home
directory. Authentication files, session transcripts, memories, caches, local
project registries, private repositories, and machine-specific paths are never
publication inputs. Publicly viewable third-party repositories also retain
their own licenses; citation does not relicense their content.

## License

Original documentation, templates, and validation code in this repository are
available under the [MIT License](LICENSE). External projects remain under the
licenses recorded in the attribution ledger.
