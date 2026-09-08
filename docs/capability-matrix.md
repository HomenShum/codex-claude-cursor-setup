# Host capability matrix

One project contract can guide all three hosts, but their configuration files
are not interchangeable. Unless a row says otherwise, these paths describe
local desktop, IDE, and CLI sessions. This matrix was rechecked against the
vendors' primary documentation on 2026-09-04.

Cursor permission precedence, sandbox controls, and local/remote skill scope
were rechecked on 2026-09-08. That source check does not retest other host paths
or prove native runtime behavior.

| Capability | Codex | Claude Code | Cursor |
|---|---|---|---|
| Project instructions | Root and nested `AGENTS.md` | Import-only `.claude/CLAUDE.md` plus Claude-only `.claude/rules/` | Root and nested `AGENTS.md` |
| Project skills | `.agents/skills` | `.claude/skills` | `.agents/skills` or `.cursor/skills` |
| Project subagents | `.codex/agents/*.toml` | `.claude/agents/*.md` | `.cursor/agents/*.md` |
| Project MCP | `.codex/config.toml` | `.mcp.json` | `.cursor/mcp.json` |
| Project hooks | `.codex/hooks.json` in a trusted project | `hooks` in `.claude/settings.json` | `.cursor/hooks.json` |
| Permission policy | policy keys in `.codex/config.toml` | shared `permissions` in `.claude/settings.json` | `.cursor/permissions.json` (desktop/local Agent); `.cursor/cli.json` (Agent CLI) |
| Sandbox policy | Codex sandbox settings | Claude permission and sandbox controls | `.cursor/sandbox.json` (desktop/local Agent); `/sandbox` or `--sandbox` (Agent CLI) |
| Parallel workers | Supported; bounded by Codex agent settings | Supported through subagents | Supported through foreground/background tasks |

For reusable agents, omit Codex's TOML `model` key so the parent setting is
inherited; Claude Code and Cursor Markdown frontmatter may use
`model: inherit`. A requested worker or judge model can be unavailable or
replaced by account or administrator policy, so verification must depend on
receipts and observed checks rather than a model name.

Claude Code does not natively load `AGENTS.md`, and its built-in Explore and
Plan agents omit `CLAUDE.md`. The templates therefore use an import-only
`.claude/CLAUDE.md`, put Claude-only guidance in `.claude/rules/`, and give
custom worker/judge definitions the critical filesystem and evidence rules
directly. Cursor loads the root `AGENTS.md`; omitting root `CLAUDE.md` prevents
the same shared contract from entering Cursor's context twice.

The Codex and Cursor worker templates are filesystem-read-only defaults, not a
complete tool boundary. Codex can inherit parent MCP configuration and live
permission overrides; Cursor subagents inherit all parent MCP tools. Inspect and
narrow the effective parent tools before delegating proof work. Cursor Cloud
subagents are a different surface: they use team MCP configuration at
`cursor.com/agents`, not the local session's `.cursor/mcp.json`; see
[Cursor cloud subagents](https://cursor.com/docs/subagents#cloud-subagents).

Cursor and Codex read the canonical `.agents/skills` tree directly. Claude
Code uses `.claude/skills`; run `scripts/sync_skills.py` to copy and verify a
project mirror. Tracked whole-directory symlinks are intentionally avoided so
the same kit works on native Windows and restricted filesystems.

Cursor does not copy local `~/.agents/skills` or unsynced personal skills to
Cloud Agents, Agents Window remote SSH sessions, or self-hosted workers.
Personal Cloud sync uses `~/.cursor/skills`; self-hosted workers can use project
skills from the repository. See [Cursor skill scope](https://cursor.com/docs/skills#skill-directories).

Cursor's desktop/local Agent permission lists combine across user and project
scope when Run Mode is not admin-controlled; file-defined allowlists replace
the corresponding IDE lists. Team-managed Run Mode controls prevent local
allowlist additions, and a team Auto-review configuration causes both local
permissions files to be ignored. The permission file applies only with a Run
Mode enabled; `autoRun` guidance applies only in Auto-review. Allowlists and
Auto-review guidance are not a security boundary. See the
[permissions reference](https://cursor.com/docs/reference/permissions) and
[Run Modes](https://cursor.com/docs/agent/security/run-modes).

Sandboxing separately applies OS filesystem and network restrictions to
supported commands. Project sandbox values have higher priority, but extra
paths are unioned and restrictive values win; team and built-in restrictions
remain stronger. The effective network mode can add default domains or allow
all network access; inspect it alongside the file. The Agent CLI uses separate
controls: `/sandbox` or `agent --sandbox enabled`; the flag accepts `enabled`
or `disabled`, and settings persist across sessions. See
[sandbox configuration](https://cursor.com/docs/reference/sandbox) and
[CLI sandbox controls](https://cursor.com/docs/cli/overview#sandbox-controls).

Primary references: [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents),
[Codex hooks](https://learn.chatgpt.com/docs/hooks),
[Claude Code subagents](https://code.claude.com/docs/en/sub-agents),
[Claude Code skills](https://code.claude.com/docs/en/skills),
[Claude Code hooks](https://code.claude.com/docs/en/hooks),
[Cursor rules](https://cursor.com/docs/rules),
[Cursor `CLAUDE.md` compatibility](https://cursor.com/help/customization/rules),
[Cursor skills](https://cursor.com/docs/skills),
[Cursor subagents](https://cursor.com/docs/subagents),
[Cursor hooks](https://cursor.com/docs/hooks),
[Cursor desktop/local Agent permissions](https://cursor.com/docs/reference/permissions),
[Cursor sandbox configuration](https://cursor.com/docs/reference/sandbox),
[Cursor CLI configuration](https://cursor.com/docs/cli/reference/configuration),
[Cursor CLI permissions](https://cursor.com/docs/cli/reference/permissions), and
[Cursor MCP](https://cursor.com/docs/mcp).
