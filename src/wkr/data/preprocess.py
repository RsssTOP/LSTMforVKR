from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import pandas as pd
import yaml

from wkr.data.common import (
    MappingConfig,
    aggregate_time_series,
    apply_column_mapping,
    concat_frames,
)


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _iter_csv_chunks(path: Path, chunksize: int = 200_000) -> Iterable[pd.DataFrame]:
    return pd.read_csv(path, chunksize=chunksize)


def _build_mapping(mapping_dict: dict, level_override: str | None = None) -> MappingConfig:
    mapping = mapping_dict.copy()
    if level_override is not None:
        mapping["entity_id"] = mapping.get("entity_id", "entity_id")
    return MappingConfig(**mapping)


def preprocess_google(raw_path: Path, config: dict) -> pd.DataFrame:
    mapping = _build_mapping(config["google"]["mapping"])
    window = config["aggregation"]["window"]
    unit = config["aggregation"]["timestamp_unit"]

    frames = []
    for chunk in _iter_csv_chunks(raw_path):
        mapped = apply_column_mapping(chunk, mapping, dataset="google")
        aggregated = aggregate_time_series(mapped, window=window, timestamp_unit=unit)
        frames.append(aggregated)
    return concat_frames(frames)


def preprocess_alibaba(raw_path: Path, config: dict) -> pd.DataFrame:
    level = config["alibaba"]["level"]
    mapping = _build_mapping(config["alibaba"]["mapping"], level_override=level)
    window = config["aggregation"]["window"]
    unit = config["aggregation"]["timestamp_unit"]

    frames = []
    for chunk in _iter_csv_chunks(raw_path):
        mapped = apply_column_mapping(chunk, mapping, dataset="alibaba")
        mapped["label"] = level
        aggregated = aggregate_time_series(mapped, window=window, timestamp_unit=unit)
        frames.append(aggregated)
    return concat_frames(frames)


def preprocess_bitbrains(raw_path: Path, config: dict) -> pd.DataFrame:
    mapping = _build_mapping(config["bitbrains"]["mapping"])
    window = config["aggregation"]["window"]
    unit = config["aggregation"]["timestamp_unit"]

    frames = []
    for chunk in _iter_csv_chunks(raw_path):
        mapped = apply_column_mapping(chunk, mapping, dataset="bitbrains")
        aggregated = aggregate_time_series(mapped, window=window, timestamp_unit=unit)
        frames.append(aggregated)
    return concat_frames(frames)


def save_processed(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)


def run_preprocessing(dataset: str, config_path: Path) -> Path:
    config = load_config(config_path)
    raw_dir = Path(config["paths"]["raw"])
    processed_dir = Path(config["paths"]["processed"])

    dataset = dataset.lower()
    if dataset == "google":
        raw_path = raw_dir / "google" / "trace.csv"
        processed = preprocess_google(raw_path, config)
    elif dataset == "alibaba":
        raw_path = raw_dir / "alibaba" / "trace.csv"
        processed = preprocess_alibaba(raw_path, config)
    elif dataset == "bitbrains":
        raw_path = raw_dir / "bitbrains" / "trace.csv"
        processed = preprocess_bitbrains(raw_path, config)
    else:
        raise ValueError(f"Unsupported dataset: {dataset}")

    output_path = processed_dir / f"{dataset}.parquet"
    save_processed(processed, output_path)
    return output_path


def write_metadata(df: pd.DataFrame, output_path: Path) -> None:
    metadata = {
        "rows": int(df.shape[0]),
        "columns": df.columns.tolist(),
    }
    output_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
