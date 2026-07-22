---
name: lab-candidate-rank
description: Rank scientific or engineering candidates under explicit multi-objective constraints while exposing uncertainty, evidence level, violations, and scoring logic. Use after a specification and provenance report exist.
---

# Lab Candidate Rank

Produce an inspectable shortlist, not a discovery claim.

## Preconditions

Require a specification from `lab-brief-to-spec` and a provenance report from `lab-provenance-check`. Stop if units conflict or the requested use is blocked.

## Workflow

1. Normalize comparable metrics with a declared method.
2. Apply hard-constraint violations before preferences.
3. Apply normalized weights and a declared evidence or uncertainty adjustment.
4. Sort deterministically and retain stable candidate identifiers.
5. Report raw metrics, normalized score, uncertainty, violations, and evidence class.
6. Emit the algorithm version and replay inputs.

## Failure and safety

- Never hide infeasibility behind a high aggregate score.
- Never compare incompatible units or protocols.
- Never label the top-ranked item as experimentally validated unless evidence proves it.
- Return an empty result with reasons when no candidate is supportable.
