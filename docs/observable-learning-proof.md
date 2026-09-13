# Observable learning proof

[View the architecture map](observable-learning-map.html). Screenshots and source-scoped browser receipts remain in the maintainer review packet; the public repository keeps its text-only artifact convention.

MEASURED on macOS arm64, Python 3.14.7: all 238 repository scenarios ran; 230 passed and eight platform-specific scenarios were skipped. Repository validation, native preflight, preflight mutation proof, external-source checks, full reachable private-history checks and `git diff --check` exited 0. Linux and Windows execution of this change still requires CI at the published revision.

The standalone example created two explicitly synthetic cases. The new command reused the existing comparator, reported NUMERICALLY_ELIGIBLE, preserved the input hashes and left activation false. A real one-case score regression changed the CLI exit to 1/REJECT; restoring the same candidate bytes returned 0/NUMERICALLY_ELIGIBLE. No model was called or measured as improved.



The upstream viewer was rebuilt in a second clean detached checkout at `84cd2fb8c704cefe52e6dd41a375c4069442e206`. Node 22.22.2, pnpm 11.19.0 and the frozen lockfile reproduced both accepted asset hashes exactly. See the [build receipt](../sources/observable-learning-build.json). Changing the generated JavaScript while preserving Git HEAD caused the real adapter CLI to refuse with exit 2; restoring its bytes passed the asset check.

The actual browser displayed three existing synthetic records, then a real append advanced it to four. The new GATE_FAILED event's exact digest matched both the validated source ledger and the visible transcript. Layout checks ran before each screenshot. The desktop transcript showed all four complete record hashes and the source-count banner. The narrow-width check established that the scope notice fits; the unchanged upstream toolbar still extends horizontally, so this is not a claim of a complete mobile viewer experience.



The viewer's CLAUDE badge is a compatibility label from upstream, not a claim that these records came from that host. Its transcript contains projected ledger metadata, not a raw conversation. The graph uses recorded ledger timestamp offsets; these are not measured host tool durations. Token and cost totals remain unmeasured regardless of the upstream display defaults.

## Boundaries and reproduction

Follow the [recipe](observable-learning.md). Keep actual case data and local receipts within their authorized audience. The new scripts were authored in this MIT repository and reuse only its comparator, ledger parser and path guards. The only upstream runtime integration is the separately licensed Agent Flow browser protocol/build. No private application files, transcripts, credential values, absolute workstation paths or global hook configurations enter this public change.

A valid comparison is not independent acceptance. A source hash is not a signature. A watched outcome ledger does not execute the workflow or authenticate its actor. Source authenticity, heldout isolation, judge calibration, human acceptance and production improvement remain separate requirements.
