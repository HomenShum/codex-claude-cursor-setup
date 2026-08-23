# MCP and agent bridges

MCP lets an agent call a bounded external capability. Add a server because a
real workflow requires it, not because a long tool list looks capable.

## Choose the narrowest scope

| Scope | Appropriate use |
|---|---|
| Project | A reviewed server the whole repository needs; commit only safe configuration. |
| Local | A project-specific server or credential mapping for one workstation. |
| User | A trusted server intentionally available across repositories. |

Prefer remote HTTP when the provider operates the server. Use stdio for a
local executable you control. In either case, authenticate with environment
variables or an OAuth flow—never embed a bearer token in a URL, command
argument, JSON file, or TOML file.

Official references: [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)
and [Claude Code MCP](https://code.claude.com/docs/en/mcp).

## One local server, two clients

Assume a reviewed project server runs as:

```bash
python -m example_mcp_server
```

Codex user configuration:

```bash
codex mcp add example -- python -m example_mcp_server
codex mcp list
```

Equivalent TOML is shown in `templates/codex/config.toml`.
For a Codex stdio server, `env_vars = ["NAME"]` forwards a named variable
without committing its value. Keep the server disabled until the command and
variable scope have been reviewed.

Claude Code local configuration:

```bash
claude mcp add --scope local example -- python -m example_mcp_server
claude mcp list
```

For a reviewed, team-shared Claude server, adapt
`templates/project/.mcp.json`, commit it, and let each user approve it. Keep
secret values in the environment; `.mcp.json` supports `${VARIABLE}`
expansion.

## Remote HTTP example

For Codex, keep the secret in an environment variable named by the config:

```bash
codex mcp add example-remote \
  --url https://mcp.example.invalid/mcp \
  --bearer-token-env-var EXAMPLE_MCP_TOKEN
```

For Claude Code, follow the provider's OAuth flow when available. If a custom
header is required, add the server locally and avoid committing its value.
Legacy SSE transport is not a good default for new Claude Code configuration.

## Optional cross-agent review

Both CLIs can expose an MCP stdio server:

```bash
# Allow Claude Code to ask Codex for a bounded review.
claude mcp add --scope user codex-review -- codex mcp-server

# Allow Codex to ask Claude Code for a bounded review.
codex mcp add claude-review -- claude mcp serve
```

Enable only one direction in a workflow unless you have an explicit recursion
guard. The caller must define a bounded task, treat the response as a claim,
and verify the underlying diff, logs, tests, or rendered output itself. Never
let two agents recursively delegate completion to each other.

## Server admission checklist

Before enabling a server, record:

- owner, source, version or commit, and license;
- exact user job and tools required;
- data sent off-machine and retention implications;
- authentication and least-privilege scope;
- timeouts, response-size limits, and error semantics;
- whether URLs are validated before server-side fetches;
- uninstall or disable command;
- one happy, denied, timeout, malformed-response, and sustained-use scenario.

For a tool endpoint, a failure must be visible as a failure. Do not translate
timeouts or upstream errors into a successful status or invented score.

## Diagnostics

```bash
codex mcp list
claude mcp list
claude doctor
```

Treat command output as potentially secret-bearing. Some tools display
configured arguments or headers, so sanitize captures before sharing them.
