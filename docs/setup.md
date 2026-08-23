# Setup and configuration

This guide gives one repository to both agents without pretending their
configuration formats are interchangeable. The team contract lives in
`AGENTS.md`; Claude Code receives it through `CLAUDE.md` and `@AGENTS.md`.

All vendor documentation was rechecked on 2026-08-23. Recheck it before
automating an installer or adopting a new configuration key.

## 1. Choose the operating environment

| Environment | Recommendation |
|---|---|
| macOS or Linux | Use the native installers and your normal shell. |
| Windows, native | Use PowerShell. Git for Windows is useful for Claude Code. |
| Windows, Linux-first toolchain | Use WSL2 and keep the repository in the Linux filesystem. |
| Managed workstation | Ask the administrator which install and authentication methods are allowed. |

Codex documents both native Windows and WSL2. Anthropic documents native
Windows and WSL2, but its native Windows sandbox behavior differs from WSL2.
Read the vendor platform notes before granting broad permissions.

## 2. Install and authenticate

Preferred standalone installers:

```powershell
# Windows PowerShell
irm https://chatgpt.com/codex/install.ps1 | iex
irm https://claude.ai/install.ps1 | iex
```

```bash
# macOS, Linux, or WSL
curl -fsSL https://chatgpt.com/codex/install.sh | sh
curl -fsSL https://claude.ai/install.sh | bash
```

Launch each program interactively and use the sign-in method appropriate for
your account:

```bash
codex
claude
```

Verify what is actually installed:

```bash
codex --version
claude --version
claude doctor
```

Do not pin this repository to the versions seen on one workstation. Codex and
Claude Code change frequently; compatibility belongs in an explicit project
lock or CI matrix when a project truly requires it.

Official references: [Codex CLI](https://learn.chatgpt.com/docs/codex/cli),
[Codex on Windows](https://learn.chatgpt.com/docs/windows/windows-app),
[Codex with WSL](https://learn.chatgpt.com/docs/windows/wsl), and
[Claude Code setup](https://code.claude.com/docs/en/setup).

## 3. Separate personal and project scope

| Purpose | Codex | Claude Code |
|---|---|---|
| Personal instructions | `~/.codex/AGENTS.md` | `~/.claude/CLAUDE.md` |
| Project instructions | `AGENTS.md` and nearer nested files | `CLAUDE.md` or `.claude/CLAUDE.md` |
| Personal settings | `~/.codex/config.toml` | `~/.claude/settings.json` |
| Shared project settings | `.codex/config.toml` in a trusted project | `.claude/settings.json` |
| Private project override | keep outside version control | `.claude/settings.local.json` |
| Shared project MCP | `.codex/config.toml` | `.mcp.json` |

Copy and edit; do not overwrite an existing personal file blindly:

- `templates/global/WORKING_AGREEMENTS.md` is a compact personal contract.
- `templates/project/AGENTS.md` is the canonical project contract.
- `templates/project/CLAUDE.md` imports the project contract.
- `templates/codex/config.toml` and `templates/claude/settings.json` are safe
  starting points, not universal policies.

Instruction files provide context to a model. They do not replace OS
permissions, sandbox rules, server authorization, code review, or CI.

Official references: [Codex configuration](https://learn.chatgpt.com/docs/config-file/config-basic),
[Codex `AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
[Claude Code settings](https://code.claude.com/docs/en/settings), and
[Claude Code memory](https://code.claude.com/docs/en/memory).

## 4. Bootstrap a repository

Create only the surfaces the project needs:

```text
project/
├── AGENTS.md
├── CLAUDE.md
├── .codex/
│   └── config.toml       # optional
├── .claude/
│   └── settings.json     # optional
└── .mcp.json             # optional
```

Replace every `[BRACKETED_FIELD]`. Keep commands runnable from the repository
root, describe the true test command, and record platform-specific launchers.
Nested `AGENTS.md` or `CLAUDE.md` files should add only instructions owned by
that subtree.

## 5. Migrate an existing split setup

1. Inventory every instruction, settings, MCP, hook, skill, plugin, and ignored
   local-state location.
2. Exclude authentication stores, transcripts, caches, databases, generated
   worktrees, screenshots containing secrets, and private path registries.
3. Merge shared team rules into `AGENTS.md`.
4. Replace the duplicated root `CLAUDE.md` with `@AGENTS.md` plus Claude-only
   guidance.
5. Keep native settings separate; their schemas and precedence differ.
6. Move credentials to environment variables or a secret manager.
7. Reinstall skills from their canonical source instead of copying generated
   or cached directories.
8. Run the offline validator and scenario suite before publishing.

## 6. Definition of done

A newcomer can clone the repository, identify every file's destination, parse
all templates, run offline validation without credentials, and understand what
must be reviewed before enabling network tools or executable hooks.
