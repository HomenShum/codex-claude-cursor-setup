# Troubleshooting

Start by asking which layer is failing: installation, instruction discovery,
settings precedence, skill discovery, MCP process startup, tool authorization,
or the application the tool calls. Changing prompts cannot repair a dead
process or denied credential.

## The agent does not follow project instructions

- Confirm the terminal's current directory is inside the intended repository.
- For Codex, check the `AGENTS.md` chain from repository root to the current
  directory. Nearer files override earlier guidance.
- For Claude Code, confirm a root `CLAUDE.md` imports `@AGENTS.md`; Claude Code
  does not automatically treat `AGENTS.md` as its project memory.
- Keep the combined instructions short enough to load and move detailed
  workflows into skills.
- Remember that instructions guide behavior; use permissions or CI when a rule
  must be enforced.

## A skill works in one client only

Codex and Claude Code use different discovery roots. Verify the canonical
skill was installed to `.agents/skills/<name>/SKILL.md` for Codex and
`.claude/skills/<name>/SKILL.md` for Claude Code. Compare the installed copies
with their recorded source revision; do not assume two files with the same
name are the same implementation.

## An MCP server is missing or fails to start

```bash
codex mcp list
claude mcp list
claude doctor
```

Then run the server command directly from the same working directory. Check
the executable path, arguments, environment-variable names, startup timeout,
and whether the project configuration has been trusted or approved. On
Windows, prefer a documented module launcher when a framework's default event
loop is incompatible with a database driver.

Do not paste raw MCP listings into an issue: command arguments and headers may
contain credentials.

## Cross-agent review loops or hangs

Disable one bridge direction. A Codex server called by Claude should not call
the Claude server again. Give the reviewer a bounded artifact and require the
caller to verify the report against raw evidence.

## Claude Code customizations make startup fail

Use the vendor's safe-mode troubleshooting option to isolate custom skills,
plugins, hooks, MCP servers, and instruction files, then restore one reviewed
layer at a time. Do not use a permission-bypass mode as a diagnostic shortcut.

## Configuration appears valid but is ignored

Parsing proves syntax only. Confirm the installed client version recognizes
the key, the project is trusted, and a higher-precedence user, local, managed,
profile, or CLI setting is not overriding it. Recheck the current
[Codex configuration guide](https://learn.chatgpt.com/docs/config-file/config-basic)
or [Claude Code settings guide](https://code.claude.com/docs/en/settings).

## A push succeeded but the public repository is stale

Inspect repository visibility and the default branch through the hosting API,
then fetch raw `README.md` and one exact source-ledger signal. A successful Git
push establishes transport, not the content a public reader receives.
