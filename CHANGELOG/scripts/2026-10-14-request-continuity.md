## 2026-10-14 — Bind completion to requests and current evidence

- Commit: candidate
- User outcome: Competing hosts cannot silently lose a request or complete it against another request's baseline or an obsolete review.
- Source: Original-request traceability and append-only before/after change-log requirement.
- Before: Generic events preserved prose and failures without typed request, change or completion references.
- After: The existing hash-linked ledger validates request, decision, baseline, change, independent review and completion links during append and replay.
- Files: scripts/outcome_review.py and tests/test_outcome_review.py.
- Verification: New request scenarios fail before implementation and seven outcome scenarios pass after implementation, including eight concurrent writers and the real 500-record cap.
- Caveats: Actor identities and evidence references are assertions; replay remains necessary. Hashes do not create a WORM store or deployment authority.

### Verification checkpoint — 2026-10-14

- Before: Independent review found that very long change IDs could prevent a full review from fitting the event cap, and rendered handoffs hid PASS/REVISE details.
- After: Canonical encoded change IDs are capped at 64 bytes; request/actor/record hashes, verdicts, covered changes and current/accepted review references are rendered explicitly.
- Verification: 12 outcome scenarios pass, including 101 changes, oversized Unicode/ASCII IDs, append and rehashed replay, competing writers and sustained history. The repository suite passed 231 scenarios with three platform skips before the final targeted additions; all final additions passed in the targeted run. Independent Codex code review and simplification both APPROVED the final script snapshot.
- Reliability: collections derive from at most 500 records; reads/events retain existing byte caps; malformed state is NO_GATE; canonical sorted-key hashing is retained. No network route, external fetch, score calculation or async backend was added. Wall-clock execution remains the runner's responsibility.
