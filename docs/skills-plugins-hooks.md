# Skills, plugins, and hooks

These extension types solve different problems. Mixing them creates duplicate
instructions and surprising execution.

| Extension | Human situation | Technical boundary |
|---|---|---|
| Skill | A repeatable job needs a reusable playbook. | Instructions and supporting resources loaded on demand. |
| Plugin | A maintained package should distribute skills or integrations. | Vendor-specific bundle with its own manifest and trust boundary. |
| Hook | A lifecycle event must always run a deterministic action. | Executable automation with the user's permissions. |
| MCP server | The agent must call a tool or remote system. | Process or service protocol, authentication, and data boundary. |

## Keep one canonical skill source

Codex discovers repository skills in `.agents/skills/<name>/SKILL.md` and
personal skills in `~/.agents/skills`. Claude Code discovers repository skills
in `.claude/skills/<name>/SKILL.md` and personal skills in
`~/.claude/skills`.

When both agents need the same skill, maintain one reviewed source and install
or link it into both discovery paths. On Windows, copying through a small
script is often more portable than relying on privileged symlinks. Record the
source URL and revision, and validate that both installed copies match it.

Start a local skill from `templates/skill/SKILL.md`. Keep the description
specific enough that an agent can decide when the skill applies. Put long
references and scripts beside it rather than inflating every prompt.

Official references: [Codex skills](https://learn.chatgpt.com/docs/build-skills)
and [Claude Code skills](https://code.claude.com/docs/en/skills).

## Plugins are installable supply-chain inputs

Before installing a plugin:

1. verify its publisher and canonical repository;
2. read its manifest, permissions, MCP servers, hooks, and update behavior;
3. pin or record the reviewed release when the host supports it;
4. test it in a disposable repository;
5. document removal and state-cleanup steps.

OpenAI and Anthropic publish example or official plugin directories, but a
directory listing does not transfer trust to every third-party integration.
The repositories used in this setup's history are recorded in
[External projects](external-projects.md).

## Hooks are code, not prose

Claude Code hooks can run commands, prompts, agents, HTTP requests, or MCP
tools at lifecycle events. A malicious or careless project hook executes with
the user's authority. This repository therefore ships no enabled hook.

For any hook proposal, document:

- trigger and matcher;
- exact input schema and untrusted fields;
- command or endpoint and working directory;
- timeout, exit-code meaning, and output cap;
- side effects and rollback;
- Windows and POSIX behavior;
- adversarial filename, prompt-injection, and concurrent-event scenarios.

Use `claude /hooks` to inspect what is active and consult the official
[hooks guide](https://code.claude.com/docs/en/hooks-guide) before enabling one.

## Promotion proof

A reusable extension is ready only when a realistic user can invoke it from
both intended hosts, its refusal and degraded paths are visible, its source is
attributed, no secret is stored in config, and uninstalling it returns the
host to the prior state.
