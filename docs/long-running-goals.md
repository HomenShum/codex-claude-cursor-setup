# Keep a user's job intact across agents and sessions

A builder asks Claude to improve the interface and Codex to improve the agent
inside it. If the next session remembers only the latest bug, earlier requests
disappear; if it accepts an old review, an unreviewed change can look finished.
Record each request and its proof in the existing outcome ledger. A long-running
goal is complete only when its current work can be traced back to the request
and independently checked.

## Register the work before executing it

Initialize one [outcome contract](../templates/harness/outcome-contract.json)
per bounded experiment with the existing [outcome commands](outcome-lifecycle.md).
Append a [request event](../templates/harness/request-event.json) for every
accepted ask, including later steering. Use a sanitized paraphrase and a local
source reference; keep private prompts and transcripts in the target's ignored
`.agent-local/` directory. Separate experiments when their failure gates or
attempt budgets should be independent. A campaign register links those ledgers.

```bash
python scripts/outcome_review.py init --input outcome.json --ledger .agent-local/events.jsonl
python scripts/outcome_review.py append --input request.json --ledger .agent-local/events.jsonl --expected-head PREVIOUS_SHA256
python scripts/outcome_review.py render --ledger .agent-local/events.jsonl --format ascii
```

The parent directory must exist. Each append returns the next SHA. After a
stale-head or lock failure, re-read and reconcile; do not delete another writer's
lock or silently replace the log. A request's owner and acceptance are frozen.
A different scope or owner needs a new request ID referencing the prior request,
plus an explanatory decision; retain the old request and its disposition.

All events keep the existing `type`, `actor`, `summary`, `next_action`,
`failed_gates` and `evidence` fields. Add these fields for request-bound work:

| Event | Required additions and meaning |
|---|---|
| `REQUEST_RECORDED` | Unique `request_id`, `source_ref`, `owner`, nonempty `scope` and `acceptance` lists. Summary preserves the accepted ask. |
| `DECISION_RECORDED` | `request_id`, unique `decision_id`, `supersedes` (null or an earlier decision in this request), `before`, `after`, nonempty supporting evidence. Corrections append; they never edit an old row. |
| `BASELINE_CAPTURED` | `request_id` and nonempty evidence of the actual prior behavior. Save this record's SHA. |
| `CHANGE_RECORDED` | `request_id`, unique `change_id` (at most 64 bytes in canonical JSON, including quotes/escapes), `before` containing that request's earlier baseline SHA, and `after: {summary, evidence}` with nonempty evidence. |
| `REVIEW_RECORDED` | `request_id`, exact `change_ids` for all current changes, `verdict` of `PASS` or `REVISE`, and nonempty review evidence. The actor must differ from the request owner and change authors. |
| `REQUEST_COMPLETED` | `request_id`, `review_sha256` identifying the latest passing review. No unresolved ledger-wide gates or intervening baseline, decision or change may remain. |

Example change after a real cancellation repair:

```json
{
  "type": "CHANGE_RECORDED",
  "actor": "runtime-worker",
  "summary": "Stop no longer schedules the next stage.",
  "next_action": "Ask an independent reviewer to replay the cancellation case.",
  "failed_gates": [],
  "evidence": ["changes/candidate.diff"],
  "request_id": "agent-cancellation",
  "change_id": "cancel-v1",
  "before": "REPLACE_WITH_BASELINE_RECORD_SHA256",
  "after": {"summary": "No later stage or graph write; completed output retained.", "evidence": ["proof/after-cancel.json", "proof/after-cancel.png"]}
}
```

Rendering derives open/completion-recorded requests and before/after references
from the same bounded history. Older v1 contracts and generic events still work;
older binaries cannot read these new event types. Completion records are
immutable; regressions need linked follow-up requests. A missing review or
unknown reference returns `NO_GATE`, not success.

## Run one bounded cycle, then reconcile

1. Read all open requests, the latest steering, owner scopes, branch state,
   unresolved failures, last head and remaining budget. Do not duplicate work
   already held by another active agent.
2. Pick one authorized user journey. Observe its actual failure before editing;
   record a baseline, exact code/model/data/judge identities and a named proof.
3. Repair the earliest owned cause in an isolated branch. Preserve adjacent
   work, completed artifacts and the user's ability to cancel or recover.
4. Re-run the same case, including rejected/degraded/adversarial paths and
   representative burst and sustained use. Record output, state changes,
   traces, latency/cost and screenshots where user-visible behavior changed.
5. Append the change and independently review the current revision. Failed
   checks stay open across host switches. A new change invalidates the review.
6. Use existing review/CI/merge gates; verify the real target after publication.
   Append completion only for the request actually proved. Then choose the
   next open request, or hand off the exact blocker and an independent next item.

The host scheduler owns wakeups, mutual exclusion, wall-clock timeout and
cancellation. This kit records outcomes; it does not start a daemon, enable
hooks, execute evidence references or spend provider money. Configure a reviewed
host-native recurring task explicitly, using the same campaign and ledger.
An active loop has a finite budget for each attempt: at most three candidate
attempts per contract and at most four hours per declared run. The runner must
enforce time, cost and permissions; the ledger enforces candidate count. A host
switch does not reset them. Three failed repairs, unchanged external blockers,
missing authority, or exhausted cost/time stop that item. Evidence of success
stops the slice; it does not trigger an unrequested refactor.

At 500 records or 4 MB the ledger refuses more writes. Preserve the sealed
ledger and its final hash, and create an explicitly linked continuation with
carried open requests, failed gates, approvals and consumed attempts. Never
rotate by dropping failures or granting a fresh retry budget. This transfer is
a reviewed operator action, not an automatic capability of the current tool.

## Improve the harness without teaching it the answer

Start with the app's existing runtime and [learning comparison](../templates/learning/README.md).
Use [the research candidates](portfolio-agent-campaign.md#framework-candidates)
only for a measured shortcoming. Current-task recovery and future harness
evolution are separate experiments. Freeze the policy, evaluator, tool
permissions and final holdout outside the candidate's editable workspace.
Generated code and proposed harnesses receive the same isolation and review as
ordinary code. Recursion never grants authority to change its own acceptance
rules, approvals, permissions, budgets or hidden tests.

Synthetic cases begin with a realistic persona, goal, starting data/state,
allowed actions, source provenance, expected final state, forbidden side
effects and a failure mode. Include cancellation between stages, provider
timeouts, denied permissions, duplicate submissions, stale/conflicting data,
untrusted instructions, concurrent actors and state accumulation. Split by
source and scenario family before generating variants; paraphrases stay in
the same split. Record generator/version/seed/license and label every generated
trace synthetic. Validate source constraints, have an independent reviewer
check expected outcomes, and preserve real failures as regression cases.

Compare incumbent and candidate on the same frozen cases and resource budget.
Report task completion, critical invariant violations, recovery success,
latency, provider cost, missing traces and per-case regressions. The existing
comparison requires all hard gates and no case-score decrease; numerical
eligibility does not activate a harness. Final unseen cases must remain outside
optimizer access, with real UI/state inspection before adoption. Do not call
offline fixture success a measured model improvement or production proof.

## What these records prove

Hash chaining, bounded reads, exclusive append locking and expected-head checks
detect inconsistent history and competing writers. Filesystem owners can
rewrite and rehash it. Actor names assert independence; they do not authenticate
people. A reference is not proof that an artifact exists or predates the edit.
Independent reviewers must inspect and replay the evidence; deployments and
spending retain their existing authorization boundaries. The ledger's
`COMPLETION_RECORDED` label means that required record links are present, not that
this tool observed the user's app or authorized activation.
