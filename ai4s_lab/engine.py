from __future__ import annotations

import csv
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List


METRICS = (
    "specific_capacity",
    "voltage",
    "cycle_retention",
    "safety",
    "cost",
)


@dataclass(frozen=True)
class DesignTarget:
    objective: str
    minimums: Dict[str, float]
    weights: Dict[str, float]

    def normalized_weights(self) -> Dict[str, float]:
        cleaned = {metric: max(0.0, float(self.weights.get(metric, 0.0))) for metric in METRICS}
        total = sum(cleaned.values())
        if total <= 0:
            return {metric: 1.0 / len(METRICS) for metric in METRICS}
        return {metric: value / total for metric, value in cleaned.items()}


@dataclass(frozen=True)
class Material:
    material_id: str
    name: str
    formula: str
    family: str
    specific_capacity: float
    voltage: float
    cycle_retention: float
    safety: float
    cost: float
    evidence_level: float


class MaterialEngine:
    """Deterministic multi-objective screener.

    The bundled records are product-demo inputs rather than research-grade
    measurements. Replacing this loader with validated experimental and DFT
    data is the first scientific milestone.
    """

    def __init__(self, data_path: Path):
        self.materials = list(self._load(data_path))
        if not self.materials:
            raise ValueError("materials dataset is empty")
        self._ranges = self._metric_ranges(self.materials)

    @staticmethod
    def _load(data_path: Path) -> Iterable[Material]:
        with data_path.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                yield Material(
                    material_id=row["material_id"],
                    name=row["name"],
                    formula=row["formula"],
                    family=row["family"],
                    specific_capacity=float(row["specific_capacity"]),
                    voltage=float(row["voltage"]),
                    cycle_retention=float(row["cycle_retention"]),
                    safety=float(row["safety"]),
                    cost=float(row["cost"]),
                    evidence_level=float(row["evidence_level"]),
                )

    @staticmethod
    def _metric_ranges(materials: List[Material]) -> Dict[str, tuple]:
        ranges = {}
        for metric in METRICS:
            values = [float(getattr(material, metric)) for material in materials]
            ranges[metric] = (min(values), max(values))
        return ranges

    def _normalize(self, metric: str, value: float) -> float:
        low, high = self._ranges[metric]
        if math.isclose(low, high):
            return 1.0
        return (value - low) / (high - low)

    def screen(self, target: DesignTarget, limit: int = 6) -> Dict[str, object]:
        weights = target.normalized_weights()
        ranked = []
        for material in self.materials:
            violations = []
            score = 0.0
            for metric in METRICS:
                value = float(getattr(material, metric))
                minimum = target.minimums.get(metric)
                if minimum is not None and value < float(minimum):
                    violations.append(
                        {
                            "metric": metric,
                            "actual": round(value, 3),
                            "required": round(float(minimum), 3),
                        }
                    )
                score += weights[metric] * self._normalize(metric, value)

            feasibility_penalty = 0.12 * len(violations)
            evidence_bonus = 0.08 * material.evidence_level
            final_score = max(0.0, min(1.0, score - feasibility_penalty + evidence_bonus))
            uncertainty = max(0.04, min(0.45, 0.38 - 0.28 * material.evidence_level))
            ranked.append(
                {
                    **asdict(material),
                    "score": round(final_score * 100, 1),
                    "uncertainty": round(uncertainty * 100, 1),
                    "feasible": not violations,
                    "violations": violations,
                }
            )

        ranked.sort(key=lambda item: (item["feasible"], item["score"]), reverse=True)
        selected = ranked[: max(1, min(limit, len(ranked)))]
        next_experiment = self._next_experiment(selected)
        return {
            "objective": target.objective,
            "weights": weights,
            "candidates": selected,
            "next_experiment": next_experiment,
            "disclaimer": (
                "Prototype ranking based on illustrative demo data. Validate against "
                "traceable experimental or first-principles data before scientific use."
            ),
        }

    @staticmethod
    def _next_experiment(candidates: List[Dict[str, object]]) -> Dict[str, object]:
        if not candidates:
            return {"hypothesis": "No candidate available", "measurements": []}
        candidate = max(candidates, key=lambda item: float(item["uncertainty"]))
        return {
            "candidate_id": candidate["material_id"],
            "hypothesis": (
                f"{candidate['name']} offers the highest information gain among the shortlisted "
                "candidates because its current evidence confidence is weakest."
            ),
            "measurements": [
                "Confirm composition and phase purity",
                "Measure initial specific capacity at a declared C-rate",
                "Run a controlled cycle-retention protocol",
                "Record thermal behavior under the same protocol as the benchmark set",
            ],
            "success_gate": "Update the ranking only after measurements have provenance and uncertainty bounds.",
        }

