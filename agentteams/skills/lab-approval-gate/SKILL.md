---
name: lab-approval-gate
description: Risk-classify proposed R&D actions and enforce human approval, least privilege, rollback, audit, and execution boundaries. Use before physical experiments, external writes, spending, credential use, regulated work, or irreversible actions.
---

# Lab Approval Gate

Fail closed when authority, evidence, or recovery is inadequate.

## Workflow

1. Classify the action as low, medium, or high risk.
2. Identify data, money, credentials, equipment, people, and external systems affected.
3. Verify the actor has explicit authority and least-privilege access.
4. Require a named human role for medium or high-risk approval.
5. Record preconditions, rollback, audit evidence, and expiration.
6. Return `approved`, `rejected`, or `blocked_pending_human_approval`.

## Non-negotiable boundaries

- An Agent cannot approve its own high-risk action.
- Missing approver, rollback, or safety evidence means blocked.
- Approval never expands beyond the exact action and time window.
- Physical laboratory execution requires a qualified laboratory owner.
