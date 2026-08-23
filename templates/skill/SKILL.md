---
name: example-proof
description: Verify a completed change against raw artifacts and one named user outcome. Use after substantive implementation or when another agent claims completion.
---

# Example proof skill

## Inputs

- the user's requested outcome;
- the exact files or remote surface in scope;
- the claimed verification commands;
- one named observable proof.

## Workflow

1. Restate the claim in falsifiable terms.
2. Inspect the raw diff or artifact rather than relying on a summary.
3. Re-run the narrow verification from a clean state.
4. Exercise one realistic failure or degraded path.
5. Compare the observation with the named proof.
6. Return `VERIFIED`, `VERIFIED WITH CAVEATS`, or `NOT VERIFIED`, followed by
   the evidence and the smallest next repair.

## Boundaries

- Do not edit while judging.
- Do not expose credentials or private identifiers in evidence.
- A lower-layer check cannot prove a higher-layer claim.
- Stop when the named proof is observed or concretely falsified.
