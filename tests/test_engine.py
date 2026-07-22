import unittest
from pathlib import Path

from ai4s_lab.engine import DesignTarget, MaterialEngine
from ai4s_lab.orchestrator import LabOpsOrchestrator


ROOT = Path(__file__).resolve().parents[1]


class MaterialEngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = MaterialEngine(ROOT / "data" / "demo_cathodes.csv")

    def test_returns_ranked_candidates(self):
        target = DesignTarget(
            objective="high capacity and safety",
            minimums={"specific_capacity": 170, "safety": 5},
            weights={"specific_capacity": 0.4, "voltage": 0.1, "cycle_retention": 0.2, "safety": 0.25, "cost": 0.05},
        )
        result = self.engine.screen(target)
        self.assertEqual(6, len(result["candidates"]))
        self.assertTrue(result["candidates"][0]["feasible"])
        self.assertGreaterEqual(result["candidates"][0]["specific_capacity"], 170)

    def test_weights_are_normalized(self):
        target = DesignTarget("balanced", {}, {"safety": 2, "cost": 2})
        weights = target.normalized_weights()
        self.assertAlmostEqual(1.0, sum(weights.values()))
        self.assertAlmostEqual(0.5, weights["safety"])

    def test_next_experiment_is_proposed(self):
        target = DesignTarget("balanced", {}, {})
        result = self.engine.screen(target)
        self.assertIn("candidate_id", result["next_experiment"])
        self.assertGreater(len(result["next_experiment"]["measurements"]), 2)

    def test_agent_team_emits_auditable_closed_loop(self):
        target = DesignTarget("safe high-capacity cathode", {"specific_capacity": 170}, {})
        result = LabOpsOrchestrator(self.engine).run("capacity >= 170", target)

        self.assertEqual("pass", result["audit"]["status"])
        self.assertEqual(6, len(result["trace"]))
        self.assertEqual(1.0, result["metrics"]["trace_coverage"])
        self.assertEqual(0, result["metrics"]["unverified_claims"])
        self.assertEqual("blocked_pending_human_approval", result["approval"]["status"])
        self.assertTrue(result["run_id"].startswith("axm-"))

    def test_replay_key_is_deterministic(self):
        target = DesignTarget("balanced", {}, {})
        orchestrator = LabOpsOrchestrator(self.engine)
        first = orchestrator.run("balanced", target)
        second = orchestrator.run("balanced", target)
        self.assertEqual(first["run_id"], second["run_id"])


if __name__ == "__main__":
    unittest.main()

