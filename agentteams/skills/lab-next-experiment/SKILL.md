---
name: lab-next-experiment
description: Propose the next high-information experiment for a ranked candidate set, with hypothesis, measurements, controls, success gates, and uncertainty-reduction rationale. Use after candidate ranking and before any physical action.
---

# Lab Next Experiment

Choose a test that resolves the most decision-relevant uncertainty.

## Workflow

1. Identify the uncertainty most likely to change the decision.
2. Select a candidate and state a falsifiable hypothesis.
3. Specify measurements, controls, declared protocol conditions, and required provenance.
4. Define success, failure, and inconclusive gates before execution.
5. Explain how each possible outcome updates the ranking.
6. Send the proposal to `lab-approval-gate`; do not execute it.

## Failure and safety

- Do not propose an experiment without a measurable decision consequence.
- Do not fabricate equipment, protocols, material availability, or expected results.
- Mark missing laboratory expertise and safety review as blockers.
- Preserve negative and inconclusive outcomes in the evidence ledger.
