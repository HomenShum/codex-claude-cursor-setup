# Inspect learning results and outcome steps

A saved-output comparison can be numerically eligible while still awaiting
source verification and human acceptance. This recipe makes those distinctions
visible using the existing comparator and outcome ledger.

Use Python 3.11 or newer. The example needs no credentials, network, model calls
or installed Python packages. From the setup-kit root, choose a new directory
whose parent already exists:

```bash
python examples/observable-learning/demo.py --out learning-example
python scripts/learning_review.py --policy learning-example/policy.json --baseline learning-example/baseline.json --candidate learning-example/candidate.json
```

Open `learning-example/review.html` in your browser. It shows every case's
baseline and candidate values, the explicit synthetic flag and exact input
hashes. These are fabricated test values used to prove the comparison path;
they are not an evaluated model or evidence of self-improvement.

For real work, provide your separately reviewed version-2 policy and saved
baseline/candidate files. See the [learning contract](../templates/learning/README.md)
for identity, grouping and heldout boundaries. This command reuses
`bootstrap_learning.compare`; it does not loosen that comparator's rules.

`--format html` writes an escaped, offline inspection page to stdout.
`--format event` writes an existing `EVAL_COMPLETED` event for explicit append
with [`outcome_review.py`](outcome-lifecycle.md). The event includes the three
input hashes and any comparison failure. Generating an event does not append it.
Exit 0 means a valid comparison, including a tie; exit 1 means rejected; exit 2
means no valid verdict. The command never authorizes activation. Do not share
real case identifiers or heldout evidence beyond their approved audience.

## Watch the existing ledger with Agent Flow

The optional viewer uses the unchanged upstream Agent Flow UI. This adapter
projects existing outcome records into its message view. It does not represent
tool calls, agent delegation, host execution or an application pipeline graph.
The avatar is a compatibility presentation. The graph clock uses relative
recorded ledger timestamps; these are not observed tool durations. Token and
cost totals are unmeasured.

Build the reviewed upstream revision in a separate checkout. Git, Node.js 22.22.2
and pnpm 11.19.0 were used to reproduce the currently pinned assets. Other
runtime versions have not been verified against these hashes. These exact build steps were used
for the pinned UI:

```bash
git clone https://github.com/patoles/agent-flow.git agent-flow-viewer
git -C agent-flow-viewer checkout --detach 84cd2fb8c704cefe52e6dd41a375c4069442e206
cd agent-flow-viewer
AGENT_FLOW_TELEMETRY=false DO_NOT_TRACK=1 pnpm install --frozen-lockfile --ignore-scripts
AGENT_FLOW_TELEMETRY=false DO_NOT_TRACK=1 pnpm run build:app
cd ..
```

From the setup-kit root, pass the actual relative path to that checkout and
the one approved ledger. No default searches a home directory or transcript
store. The adapter has no telemetry transport, denies external browser
connections with Content Security Policy, and does not run upstream setup,
hooks or the upstream directory-scanning relay.

```bash
python scripts/agent_flow_outcome.py --ledger learning-example/events.jsonl --upstream agent-flow-viewer --port 8769
```

Open `http://127.0.0.1:8769`. Choose the Outcome ledger metadata session. The
banner identifies the projection and links its exact source receipt. Only
event type, sequence, record digest, failed-gate count and recorded timestamps
leave the source reader. Actor names, summaries, goals, evidence references and local paths are
withheld. Source hashes and bytes are recomputed on refresh; a rewritten prior
record, malformed tail or oversized source is refused. A temporary incomplete
append may reconnect after the writer finishes. It never clears a prior failure.

In a second terminal at the setup-kit root, append an explicitly synthetic
failure to this example:

```bash
python examples/observable-learning/demo.py --append-to learning-example/events.jsonl
```

The displayed count advances from two to three records. `GATE_FAILED` and its
record hash appear in the UI's transcript view. This proves an actual local
ledger arrival; the failure content remains an expressly synthetic fixture.
Real hosts continue to use their existing explicit [planner/worker/judge
protocol](agent-stack.md) and [outcome routes](outcome-lifecycle.md). This viewer
does not add a scheduler, change a host configuration or invoke a model.

The server accepts only the fixed GET routes and at most four event streams.
All listeners bind `127.0.0.1`; there is no remote-host option. Quit with Ctrl-C.
Keep your inputs and recorded receipts if needed; remove the explicitly created
example directory and isolated upstream checkout when finished. No global
configuration rollback is needed because these commands do not change it.

The adapter requires both the pinned upstream Git revision and the exact
reviewed JavaScript/CSS build hashes in `ASSET_HASHES`. Modified generated
assets are refused even when Git HEAD is unchanged. Different build outputs
need an explicit source/build review and a new hash pin; they are not silently
accepted. The receipt includes the actual served hashes. Keep it with the
build command and walkthrough receipt.

## Provenance and limits

The two adapters and synthetic example were authored for this MIT setup kit.
They reuse this repository's `bootstrap_learning`, `outcome_review` and
`path_safety` modules. No application runtime, private transcript or company
configuration was imported. Agent Flow is a separate Apache-2.0 project at the
pinned revision; its UI assets are built locally and are not redistributed here.
Its message protocol is documented in the pinned
[bridge types](https://github.com/patoles/agent-flow/blob/84cd2fb8c704cefe52e6dd41a375c4069442e206/web/lib/bridge-types.ts).
The [external project ledger](external-projects.md) records that dependency.

The source digest detects a changed local record. It does not authenticate the
actor, establish that a trace is real, isolate a heldout set, calibrate a judge
or grant human approval. A watched ledger and a numerical comparison each prove
their own behavior; neither alone proves an improved production system.

Measured examples and limits: [observable learning proof](observable-learning-proof.md).
