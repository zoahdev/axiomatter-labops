# Axiomatter LabOps

Evidence-first multi-agent execution infrastructure for auditable industrial R&D.

> Competition status: GOAI 2026 Agent Infra working prototype. The name is a working codename and has not been cleared for trademark use.

## Why this exists

AI can suggest candidates and experiments, but enterprise R&D needs a defensible answer to five harder questions: who made each decision, which evidence supported it, what failed, who approved risky work, and whether the result can be replayed.

Axiomatter LabOps turns one R&D brief into a six-agent evidence chain:

1. Requirement Agent - explicit objective, constraints, preferences, and unknowns.
2. Evidence Agent - record-level provenance and permitted-use boundaries.
3. Candidate Agent - deterministic ranking with visible violations and uncertainty.
4. Experiment Agent - the next high-information experiment and outcome gates.
5. Safety Agent - human approval, least privilege, rollback, and audit boundary.
6. Reproducibility Agent - claim-to-evidence audit and deterministic replay key.

The included cathode screen is a flagship demo, not the product boundary. The reusable layer is the Agent Identity, Skill, Trace, approval, and evidence-pack contract.

## Run locally for free

Requirements: Python 3.8 or newer. There are no third-party runtime dependencies.

```powershell
cd C:\Users\zoah\Documents\1\goai-axiomatter-labops
python app.py
```

Open `http://127.0.0.1:8765` and click **启动证据闭环**.

The app is offline by default and makes no paid model calls. To opt in to an OpenAI-compatible enhancement after setting a valid key:

```powershell
$env:AXIOMATTER_OFFLINE='0'
$env:OPENAI_MODEL='gpt-5.6'
python app.py
```

Never commit credentials. `.env` and `.env.*` are ignored.

## Verify

```powershell
python -m unittest discover -s tests -v
```

The tests cover deterministic ranking, weight normalization, experiment proposal, the six-agent audit loop, approval blocking, and replay-key stability.

## AgentTeams package

- `agentteams/team.yaml` defines the Manager and six Worker identities using the official `agentteams.io/v1beta1` Team resource.
- `agentteams/skills/` contains six validated, reusable Skill packages with explicit inputs, outputs, failure handling, and safety boundaries.
- The local deterministic orchestrator mirrors the same contracts so reviewers can run the demo without Docker or an API key.

AgentTeams runtime execution is the next integration milestone. It requires Docker Desktop or a Kubernetes environment; neither is required to review the current offline evidence path.

## API

`POST /api/run`

```json
{"brief": "specific capacity at least 170 mAh/g; prioritize safety"}
```

The response includes candidates, the next experiment, six Agent identities, a step-level Trace, approval status, audit checks, metrics, evidence pack, and a deterministic `run_id`.

## Scientific and integrity boundary

This repository is an engineering prototype, not a validated scientific system. Every bundled material identifier begins with `demo-`; the provenance agent classifies all bundled records as `illustrative-demo` and blocks scientific-use claims. Do not use the ranking for laboratory, engineering, safety, financial, or investment decisions.

We do not claim experiments, discoveries, users, customers, partnerships, benchmarks, stars, financing, patents, or domain credentials that do not exist.

## Competition materials

- `competition/PROJECT_BRIEF_CN.md` - 500-character entry draft and judging map.
- `competition/PRIZE_CAPTURE_CN.md` - prize, subsidy, gift, tax, and travel checklist.
- `competition/ORGANIZER_INQUIRY_CN.md` - written questions on multi-track entry and stacking awards.

## License

Apache-2.0. Third-party dependencies, datasets, and future partner materials must retain their own licenses and authorization boundaries.
