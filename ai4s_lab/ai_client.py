from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Dict

from .engine import DesignTarget, METRICS


DEFAULT_WEIGHTS = {
    "specific_capacity": 0.28,
    "voltage": 0.16,
    "cycle_retention": 0.24,
    "safety": 0.20,
    "cost": 0.12,
}


def load_local_env(project_root: Path) -> None:
    """Load env values without logging them.

    The workspace-level .env.local is supported so the existing key can be
    reused without copying it into this project.
    """

    for candidate in (project_root / ".env.local", project_root.parent / ".env.local"):
        if not candidate.exists():
            continue
        for raw_line in candidate.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            name, value = line.split("=", 1)
            name = name.strip()
            if name and name not in os.environ:
                os.environ[name] = value.strip().strip('"').strip("'")


def parse_design_brief(brief: str, project_root: Path) -> DesignTarget:
    load_local_env(project_root)
    if os.environ.get("AXIOMATTER_OFFLINE", "1").strip().lower() not in {"0", "false", "no"}:
        return fallback_target(brief)
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return fallback_target(brief)

    prompt = f"""You translate a battery-cathode material design brief into a screening target.
Return only one JSON object with this exact shape:
{{
  "objective": "short restatement",
  "minimums": {{
    "specific_capacity": number_or_null,
    "voltage": number_or_null,
    "cycle_retention": number_or_null,
    "safety": number_or_null,
    "cost": number_or_null
  }},
  "weights": {{
    "specific_capacity": nonnegative_number,
    "voltage": nonnegative_number,
    "cycle_retention": nonnegative_number,
    "safety": nonnegative_number,
    "cost": nonnegative_number
  }}
}}
Metric units: specific_capacity=mAh/g; voltage=V; cycle_retention=percent; safety and cost are 0-10 normalized demo scores.
Do not invent a hard minimum unless the user explicitly gives it. Use weights to represent qualitative preferences.
User brief: {brief}
"""
    request_body = json.dumps(
        {
            "model": os.environ.get("OPENAI_MODEL", "gpt-5.6"),
            "input": prompt,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=request_body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            payload = json.loads(response.read().decode("utf-8"))
        parsed = json.loads(_response_text(payload))
        return _coerce_target(parsed, brief)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError, KeyError, json.JSONDecodeError):
        return fallback_target(brief)


def _response_text(payload: Dict[str, object]) -> str:
    if isinstance(payload.get("output_text"), str):
        return payload["output_text"]
    for output in payload.get("output", []):
        for content in output.get("content", []):
            if content.get("type") == "output_text" and content.get("text"):
                return content["text"]
    raise ValueError("Responses API returned no text")


def _coerce_target(payload: Dict[str, object], brief: str) -> DesignTarget:
    minimums = {}
    raw_minimums = payload.get("minimums") or {}
    for metric in METRICS:
        value = raw_minimums.get(metric)
        if value is not None:
            minimums[metric] = float(value)
    raw_weights = payload.get("weights") or {}
    weights = {metric: float(raw_weights.get(metric, DEFAULT_WEIGHTS[metric])) for metric in METRICS}
    return DesignTarget(
        objective=str(payload.get("objective") or brief)[:280],
        minimums=minimums,
        weights=weights,
    )


def fallback_target(brief: str) -> DesignTarget:
    minimums = {}
    patterns = {
        "specific_capacity": r"(?:比容量|capacity)[^0-9]{0,12}(\d+(?:\.\d+)?)",
        "voltage": r"(?:电压|voltage)[^0-9]{0,12}(\d+(?:\.\d+)?)",
        "cycle_retention": r"(?:循环保持率|retention)[^0-9]{0,12}(\d+(?:\.\d+)?)",
        "safety": r"(?:安全|safety)[^0-9]{0,12}(\d+(?:\.\d+)?)",
        "cost": r"(?:成本|cost)[^0-9]{0,12}(\d+(?:\.\d+)?)",
    }
    for metric, pattern in patterns.items():
        match = re.search(pattern, brief, flags=re.IGNORECASE)
        if match:
            minimums[metric] = float(match.group(1))
    return DesignTarget(objective=brief[:280], minimums=minimums, weights=DEFAULT_WEIGHTS)

