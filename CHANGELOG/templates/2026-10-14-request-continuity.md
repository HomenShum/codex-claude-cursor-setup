## 2026-10-14 — Carry request IDs into project handoffs

- Commit: candidate
- User outcome: A new host receives the original ask, remaining failures, attempt budget and evidence references.
- Source: Cross-host continuity and append-only decisions request.
- Before: The handoff named one outcome without request IDs or the outcome ledger head.
- After: Project guidance and templates retain request scope, expected head, failures and before/after/review records; an inert request event seeds intake.
- Files: templates/project/AGENTS.md, DECISIONS.md, HANDOFF.md and templates/harness/request-event.json.
- Verification: Existing setup materialization copies these paths; target adoption and offline suite remain required for this candidate.
- Caveats: Existing project files are never overwritten automatically. Copied templates do not prove a target application or enable hooks.

### Verification checkpoint — 2026-10-14

- Repository scenario suite passed, including additive setup materialization, missing/conflicting destinations, stale plans and competing writers. Offline template/link validation passed. Existing host configurations and credentials remain unchanged.
