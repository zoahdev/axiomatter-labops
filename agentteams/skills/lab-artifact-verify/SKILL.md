---
name: lab-artifact-verify
description: Audit an Agent run for complete traces, claim-to-evidence links, approvals, deterministic replay inputs, disclosures, and reproducibility. Use before results are shown, submitted, published, or used for a downstream decision.
---

# Lab Artifact Verify

Issue a verdict from recorded evidence only.

## Required checks

1. Verify every step has agent, role, skill, status, input digest, output digest, and evidence references.
2. Verify every material claim links to evidence with a permitted use.
3. Verify risky actions were approved or blocked.
4. Verify algorithm, configuration, data, and dependency versions are recorded.
5. Verify demo or synthetic data is visibly disclosed.
6. Compute a replay key and report missing artifacts.

## Output contract

Return `pass`, `fail`, or `incomplete`, plus check results, unverified claims, missing artifacts, replay key, and remediation steps.

## Failure and safety

- Do not infer missing evidence.
- A polished screenshot is not execution evidence.
- Any fabricated metric, partnership, result, user, star, or experiment forces `fail`.
