"""Synthetic demonstration cases for the first vertical slice."""

from __future__ import annotations

import json
from pathlib import Path

from .models import DemoCase

DEMO_CASES_PATH = Path(__file__).resolve().parents[1] / "data" / "demo_cases" / "demo_cases.json"


def load_demo_cases(path: Path = DEMO_CASES_PATH) -> list[DemoCase]:
    with path.open(encoding="utf-8") as file:
        payload = json.load(file)
    return [DemoCase.model_validate(item) for item in payload]
