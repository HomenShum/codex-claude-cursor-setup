# Decision ledger

Append decisions. Corrections add a new row with `SUPERSEDES`; they do not
rewrite history.

| ID | Date | Owner | Decision | Evidence | Status | Supersedes |
|---|---|---|---|---|---|---|
| D001 | [YYYY-MM-DD] | [ROLE] | [ONE DECISION] | [RECEIPT] | ACTIVE | — |

For long-running work, the outcome JSONL ledger is authoritative. Append a
`DECISION_RECORDED` event with `request_id`, `decision_id`, `supersedes` (null
for the first decision), `before`, `after` and evidence. Link its record hash
here. Preserve both the original request and corrected decision. A change
uses `CHANGE_RECORDED` with a preceding baseline record and after evidence;
an explanation alone is not a completed change.
