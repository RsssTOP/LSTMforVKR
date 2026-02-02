from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Iterable

import pandas as pd

REQUIRED_COLUMNS = [
    "dataset",
    "entity_id",
    "timestamp",
    "cpu_usage",
    "mem_usage",
    "disk_io",
    "net_io",
    "label",
    "source_fields",
]


@dataclass(frozen=True)
class MappingConfig:
    timestamp: str
    entity_id: str
    cpu_usage: str | None = None
    mem_usage: str | None = None
    disk_io: str | None = None
    net_io: str | None = None
    label: str | None = None


def apply_column_mapping(
    df: pd.DataFrame,
    mapping: MappingConfig,
    dataset: str,
) -> pd.DataFrame:
    selected: dict[str, pd.Series] = {
        "timestamp": df[mapping.timestamp],
        "entity_id": df[mapping.entity_id],
    }
    for key in ["cpu_usage", "mem_usage", "disk_io", "net_io", "label"]:
        source = getattr(mapping, key)
        if source is None or source not in df.columns:
            selected[key] = pd.Series([pd.NA] * len(df))
        else:
            selected[key] = df[source]
    mapped = pd.DataFrame(selected)
    mapped["dataset"] = dataset
    mapped["source_fields"] = json.dumps(mapping.__dict__)
    return mapped


def ensure_columns(df: pd.DataFrame) -> pd.DataFrame:
    for column in REQUIRED_COLUMNS:
        if column not in df.columns:
            df[column] = pd.NA
    return df[REQUIRED_COLUMNS]


def to_datetime_index(
    series: pd.Series,
    unit: str,
) -> pd.Series:
    return pd.to_datetime(series, unit=unit, utc=True, errors="coerce")


def aggregate_time_series(
    df: pd.DataFrame,
    window: str,
    timestamp_unit: str,
    label_strategy: str = "first",
) -> pd.DataFrame:
    df = df.copy()
    df["timestamp"] = to_datetime_index(df["timestamp"], unit=timestamp_unit)
    df["timestamp"] = df["timestamp"].dt.floor(window)

    numeric_columns = ["cpu_usage", "mem_usage", "disk_io", "net_io"]
    agg_spec: dict[str, Any] = {col: "mean" for col in numeric_columns}
    if label_strategy == "first":
        agg_spec["label"] = "first"
    else:
        agg_spec["label"] = "last"

    grouped = (
        df.groupby(["dataset", "entity_id", "timestamp"], dropna=False)
        .agg(agg_spec)
        .reset_index()
    )

    grouped["source_fields"] = df["source_fields"].iloc[0]
    return ensure_columns(grouped)


def concat_frames(frames: Iterable[pd.DataFrame]) -> pd.DataFrame:
    frames_list = list(frames)
    if not frames_list:
        return pd.DataFrame(columns=REQUIRED_COLUMNS)
    combined = pd.concat(frames_list, ignore_index=True)
    return ensure_columns(combined)
