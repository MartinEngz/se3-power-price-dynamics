"""Compare the fitted model with one historical SE3 year."""

import argparse
from pathlib import Path

import numpy as np

from src.data import load_and_clean_data

from src.plotting import (
    historical_year_data,
    plot_historical_year
)

def run_validation(
    year,
    n_paths=1000,
    random_seed=123,
    output_dir="figures/validation"
):
    data = load_and_clean_data(
        "entso_se3/*EnergyPrices*.csv"
    )

    historical = historical_year_data(data, year)
    historical_prices = historical["EUR/MWh"].to_numpy()
    n_days = len(historical)

    # Convert the string to a Path and ensure the directory exists.
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    plot_historical_year(
        data,
        year,
        save_path=output_dir / f"historical_prices_{year}.png",
    )

    return {
        "historical": historical,
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2025)
    parser.add_argument("--paths", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=123)
    parser.add_argument("--output-dir", default="figures/validation")
    args = parser.parse_args()

    run_validation(
        year=args.year,
        n_paths=args.paths,
        random_seed=args.seed,
        output_dir=args.output_dir,
    )