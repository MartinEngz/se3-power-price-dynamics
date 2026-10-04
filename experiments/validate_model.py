"""Compare the fitted model with one historical SE3 year."""

import argparse
from pathlib import Path

import numpy as np

from experiments.config import ESTIMATED_SE3_MODEL
from src.data import load_and_clean_data
from src.models import (
    harmonic_seasonality,
    simulate_mean_reverting_jump_price_paths
)
from src.plotting import (
    historical_year_data,
    plot_historical_year,
    plot_historical_vs_simulated_distribution,
    plot_historical_vs_simulated_year,
)
from src.statistics import validation_summary

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

    cfg = ESTIMATED_SE3_MODEL
    rng = np.random.default_rng(random_seed)

    seasonal_mean = lambda t: harmonic_seasonality(
        t=t,
        a0=cfg["a0"],
        a1=cfg["a1"],
        b1=cfg["b1"],
        a2=cfg["a2"],
        b2=cfg["b2"],
        period=1.0,
    )

    S_paths = simulate_mean_reverting_jump_price_paths(
        N=n_paths,
        Y0=cfg["Y0"],
        Z0=cfg["Z0"],
        kappa=cfg["kappa"],
        sigma=cfg["sigma"],
        T=n_days / 365.0,
        M=n_days,
        seasonal_mean=seasonal_mean,
        jump_intensity=cfg["jump_intensity"],
        jump_scale=cfg["jump_scale"],
        jump_reversion=cfg["jump_reversion"],
        rng=rng,
    )

    table = validation_summary(
        historical_prices,
        S_paths,
        acf_lags=(1, 7, 30),
        upper_threshold=100.0,
        lower_threshold=0.0
    )

    # Convert the string to a Path and ensure the directory exists.
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    table_path = output_dir / f"validation_summary_{year}.csv"
    table.to_csv(table_path)

    plot_historical_year(
        data,
        year,
        save_path=output_dir / f"historical_prices_{year}.png",
    )

    plot_historical_vs_simulated_year(
        data,
        S_paths,
        year,
        max_paths=3,
        save_path=output_dir / f"historical_vs_simulated_{year}.png"
    )

    plot_historical_vs_simulated_distribution(
        historical_prices,
        S_paths,
        save_path=output_dir / f"historical_vs_simulated_distribution_{year}.png"
    )

    print("\nHistorical-versus-simulated validation")
    print(table.round(3).to_string())
    print(f"\nSaved validation table to {table_path}")

    return {
        "historical": historical,
        "simulated_paths": S_paths,
        "summary": table
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