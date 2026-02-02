from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def validate_dataset(df: pd.DataFrame) -> dict:
    missing = df.isna().sum().to_dict()
    negatives = {
        "cpu_usage": int((df["cpu_usage"] < 0).sum()),
        "mem_usage": int((df["mem_usage"] < 0).sum()),
        "disk_io": int((df["disk_io"] < 0).sum()),
        "net_io": int((df["net_io"] < 0).sum()),
    }

    monotonic_violations = 0
    for _, group in df.sort_values("timestamp").groupby("entity_id"):
        if not group["timestamp"].is_monotonic_increasing:
            monotonic_violations += 1

    return {
        "missing_values": missing,
        "negative_values": negatives,
        "non_monotonic_entities": monotonic_violations,
    }


def save_report(report: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
