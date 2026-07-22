---
name: lab-provenance-check
description: Classify research records by provenance, authorization, evidence strength, and permitted use. Use before an Agent cites, ranks, trains on, or exports scientific, industrial, personal, or partner data.
---

# Lab Provenance Check

Create a record-level evidence boundary that later agents cannot silently weaken.

## Workflow

1. Inventory every record and stable identifier.
2. Capture source, owner, license or authorization, acquisition method, version, and uncertainty.
3. Classify each record as `traceable`, `partner-restricted`, `illustrative-demo`, or `unknown`.
4. Assign permitted uses: `display`, `ranking`, `training`, `publication`, or `scientific-decision`.
5. Block uses not supported by authorization or evidence strength.
6. Return counts, missing fields, blocked uses, and record references.

## Failure and safety

- Treat missing provenance as `unknown`, never as public.
- Treat demo data as ineligible for scientific conclusions.
- Do not expose personal, partner, or enterprise data outside its stated boundary.
- Preserve the original license and dependency notices in every export.
