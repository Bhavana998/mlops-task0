#!/usr/bin/env python3
"""MLOps batch job: rolling mean signal from OHLCV data."""

import argparse
import json
import logging
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import yaml


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to data.csv")
    parser.add_argument("--config", required=True, help="Path to config.yaml")
    parser.add_argument("--output", required=True, help="Path to metrics.json")
    parser.add_argument("--log-file", required=True, help="Path to run.log")
    return parser.parse_args()


def setup_logging(log_file: Path) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)],
    )


def load_config(config_path: Path) -> dict:
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    required = ["seed", "window", "version"]
    for field in required:
        if field not in config:
            raise ValueError(f"Missing required config field: {field}")

    if not isinstance(config["seed"], int):
        raise ValueError("seed must be an integer")
    if not isinstance(config["window"], int) or config["window"] <= 0:
        raise ValueError("window must be a positive integer")
    if not isinstance(config["version"], str):
        raise ValueError("version must be a string")

    return config


def load_data(csv_path: Path) -> pd.DataFrame:
    """Load CSV where every line (header and data) is enclosed in double quotes."""
    if not csv_path.exists():
        raise FileNotFoundError(f"Data file not found: {csv_path}")
    if csv_path.stat().st_size == 0:
        raise ValueError("Data file is empty")

    # Read the header line and extract column names
    with open(csv_path, "r") as f:
        header_line = f.readline().strip()
        if header_line.startswith('"') and header_line.endswith('"'):
            header_line = header_line[1:-1]
        column_names = header_line.split(",")

    # Read data rows, strip quotes, split by comma
    data_rows = []
    with open(csv_path, "r") as f:
        next(f)  # skip header line
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('"') and line.endswith('"'):
                line = line[1:-1]
            row = line.split(",")
            data_rows.append(row)

    # Create DataFrame and convert numeric columns
    df = pd.DataFrame(data_rows, columns=column_names)
    numeric_cols = ["open", "high", "low", "close", "volume_btc", "volume_usd"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "close" not in df.columns:
        raise ValueError("Column 'close' not found in CSV")
    if df["close"].isna().all():
        raise ValueError("No valid numeric values in 'close' column")

    return df


def compute_signal(df: pd.DataFrame, window: int):
    rolling_mean = df["close"].rolling(window=window).mean()
    signal = (df["close"] > rolling_mean).astype(int)
    valid_mask = rolling_mean.notna()
    valid_signal = signal[valid_mask]
    rows_processed = len(valid_signal)
    return valid_signal, rows_processed


def run_pipeline(args):
    start_time = time.perf_counter()
    log_path = Path(args.log_file)
    setup_logging(log_path)
    logging.info("=== Job started ===")

    status = "success"
    error_message = None
    metrics = {}
    config = {}

    try:
        logging.info(f"Loading config from {args.config}")
        config = load_config(Path(args.config))
        seed = config["seed"]
        window = config["window"]
        version = config["version"]
        logging.info(f"Config loaded: seed={seed}, window={window}, version={version}")

        np.random.seed(seed)

        logging.info(f"Loading data from {args.input}")
        df = load_data(Path(args.input))
        total_rows = len(df)
        logging.info(f"Loaded {total_rows} rows")

        logging.info(f"Computing rolling mean with window={window}")
        valid_signal, rows_processed = compute_signal(df, window)

        if rows_processed == 0:
            raise RuntimeError(
                f"No valid rows after rolling mean (window={window} larger than dataset?)"
            )

        signal_rate = float(valid_signal.mean())
        logging.info(
            f"Processed {rows_processed} valid rows (first {window-1} rows excluded)"
        )
        logging.info(f"Signal rate: {signal_rate:.4f}")

        latency_ms = int((time.perf_counter() - start_time) * 1000)

        metrics = {
            "version": version,
            "rows_processed": rows_processed,
            "metric": "signal_rate",
            "value": round(signal_rate, 4),
            "latency_ms": latency_ms,
            "seed": seed,
            "status": "success",
        }
        logging.info(f"Metrics: {json.dumps(metrics, indent=2)}")

    except Exception as e:
        status = "error"
        error_message = str(e)
        metrics = {
            "version": config.get("version", "unknown") if config else "unknown",
            "status": "error",
            "error_message": error_message,
        }
        logging.error(f"Job failed: {error_message}")

    finally:
        output_path = Path(args.output)
        logging.info(f"Writing metrics to {output_path}")
        with open(output_path, "w") as f:
            json.dump(metrics, f, indent=2)

        print(json.dumps(metrics, indent=2))
        logging.info(f"=== Job ended with status: {status} ===")
        sys.exit(0 if status == "success" else 1)


if __name__ == "__main__":
    args = parse_args()
    run_pipeline(args)
