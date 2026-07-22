---
name: lab-brief-to-spec
description: Convert a natural-language R&D request into an explicit objective, constraints, preferences, assumptions, and approval-ready specification. Use for scientific or engineering briefs before candidate ranking, retrieval, simulation, or experiment planning.
---

# Lab Brief to Spec

Convert intent into a bounded specification without inventing requirements.

## Workflow

1. Restate the objective in one falsifiable sentence.
2. Extract only explicit hard constraints. Preserve units and comparators.
3. Convert qualitative preferences into nonnegative weights and normalize them.
4. List missing information as questions or assumptions; never silently fill it.
5. Mark safety, legal, cost, data, and authorization constraints.
6. Emit the contract below and attach the original brief as evidence.

## Output contract

Return `objective`, `minimums`, `maximums`, `weights`, `assumptions`, `unknowns`, `risk_flags`, and `source_ref`. Use `null` for absent values. Keep invented constraints empty.

## Failure and safety

- Fail closed on ambiguous units or contradictory hard constraints.
- Do not convert a preference into a hard threshold.
- Do not claim scientific validity; this skill structures a request only.
- Route physical execution, hazardous materials, or regulated work to `lab-approval-gate`.
