from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ai4s_lab.engine import DesignTarget, MaterialEngine  # noqa: E402
from ai4s_lab.orchestrator import LabOpsOrchestrator  # noqa: E402


SCENARIOS = (
    DesignTarget("balanced cathode", {}, {}),
    DesignTarget("high capacity", {"specific_capacity": 170}, {"specific_capacity": 1}),
    DesignTarget("safety first", {"safety": 8}, {"safety": 3, "cost": 1}),
    DesignTarget("intentionally infeasible", {"specific_capacity": 300}, {"specific_capacity": 1}),
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the deterministic LabOps competition evaluation.")
    parser.add_argument("--output", type=Path, help="Optional JSON result path.")
    args = parser.parse_args()

    data_path = ROOT / "data" / "demo_cathodes.csv"
    engine = MaterialEngine(data_path)
    orchestrator = LabOpsOrchestrator(engine)
    runs = []
    replay_matches = []

    for scenario in SCENARIOS:
        first = orchestrator.run(scenario.objective, scenario)
        second = orchestrator.run(scenario.objective, scenario)
        replay_matches.append(first["run_id"] == second["run_id"])
        runs.append(
            {
                "objective": scenario.objective,
                "run_id": first["run_id"],
                "audit": first["audit"]["status"],
                "trace_coverage": first["metrics"]["trace_coverage"],
                "verified_steps": first["metrics"]["verified_steps"],
                "unverified_claims": first["metrics"]["unverified_claims"],
                "approval": first["approval"]["status"],
                "feasible_candidates": sum(1 for item in first["candidates"] if item["feasible"]),
            }
        )

    count = len(runs)
    report = {
        "evaluation": "axiomatter-labops-deterministic-v1",
        "scientific_claim": False,
        "dataset_class": "illustrative-demo",
        "dataset_sha256": hashlib.sha256(data_path.read_bytes()).hexdigest(),
        "scenario_count": count,
        "metrics": {
            "audit_pass_rate": sum(run["audit"] == "pass" for run in runs) / count,
            "trace_coverage": sum(run["trace_coverage"] for run in runs) / count,
            "high_risk_block_rate": sum(
                run["approval"] == "blocked_pending_human_approval" for run in runs
            )
            / count,
            "zero_unverified_claim_rate": sum(run["unverified_claims"] == 0 for run in runs) / count,
            "deterministic_replay_rate": sum(replay_matches) / count,
        },
        "runs": runs,
        "limitations": [
            "Measures engineering invariants, not scientific accuracy.",
            "Uses illustrative demo records with no claim of experimental provenance.",
            "AgentTeams container execution is not included in this local reference evaluation.",
        ],
    }

    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
