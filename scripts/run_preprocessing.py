from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from wkr.data.preprocess import load_config, run_preprocessing
from wkr.data.validate import save_report, validate_dataset


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run dataset preprocessing.")
    parser.add_argument(
        "--dataset",
        required=True,
        choices=["google", "alibaba", "bitbrains"],
        help="Dataset to preprocess.",
    )
    parser.add_argument(
        "--config",
        default="src/wkr/config/default.yaml",
        help="Path to YAML config.",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Run data validation after preprocessing.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = run_preprocessing(args.dataset, Path(args.config))
    print(f"Saved processed data to {output_path}")

    if args.validate:
        df = pd.read_parquet(output_path)
        report = validate_dataset(df)
        config = load_config(Path(args.config))
        interim_dir = Path(config["paths"]["interim"])
        report_path = interim_dir / f"validation_report_{args.dataset}.json"
        save_report(report, report_path)
        print(f"Saved validation report to {report_path}")


if __name__ == "__main__":
    main()
