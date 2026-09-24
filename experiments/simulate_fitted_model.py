import numpy as np

from experiments.config import (
    STYLIZED_SE3_MODEL,
    PRELIMINARY_SE3_MODEL,
)

from src.models import (
    harmonic_seasonality,
    simulate_mean_reverting_jump_price_paths,
)

from src.statistics import (
    path_statistics,
    simulated_path_statistics,
)

from src.plotting import (
    plot_price_paths,
    plot_price_distribution,
    plot_acf,
    plot_statistic_distribution,
)


def run_fitted_model_simulation():
    """
    Test the electricity-price simulation and validation pipeline
    using stylized parameters.

    The parameters used here are not fitted to SE3 data.
    """
    cfg = STYLIZED_SE3_MODEL
    # cfg = PRELIMINARY_SE3_MODEL

    rng = np.random.default_rng(
        cfg["random_seed"]
    )

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
        N=cfg["N"],
        Y0=cfg["Y0"],
        Z0=cfg["Z0"],
        kappa=cfg["kappa"],
        sigma=cfg["sigma"],
        T=cfg["T"],
        M=cfg["M"],
        seasonal_mean=seasonal_mean,
        jump_intensity=cfg["jump_intensity"],
        jump_scale=cfg["jump_scale"],
        jump_reversion=cfg["jump_reversion"],
        rng=rng,
    )

    # --- Validation statistics

    stats = simulated_path_statistics(
        S_paths,
        acf_lags=(1, 7, 30),
        upper_threshold=100.0,
        lower_threshold=0.0,
    )

    first_path_stats = path_statistics(
        S_paths[0],
        acf_lags=(1, 7, 30),
        upper_threshold=100.0,
        lower_threshold=0.0,
    )

    # --- Simple diagnostics

    print("\n--- Stylized fitted-model simulation ---")
    print(f"Number of paths: {cfg['N']:,}")
    print(f"Time steps:      {cfg['M']:,}")
    print(f"Horizon:         {cfg['T']:.2f} years")

    print("\nFirst simulated path:")
    for name, value in first_path_stats.items():
        print(f"{name:>12}: {value:.4f}")

    print("\nAcross simulated paths:")
    print(
        f"Mean price: "
        f"{np.mean(stats['mean']):.2f} EUR/MWh"
    )
    print(
        f"Mean std:   "
        f"{np.mean(stats['std']):.2f} EUR/MWh"
    )
    print(
        f"Mean ACF(1): "
        f"{np.mean(stats['acf_1']):.3f}"
    )

    # --- Simple plotting experiment

    plot_price_paths(
        S_paths=S_paths,
        T=cfg["T"],
        max_paths=20,
        title="Seasonal Mean-Reverting Jump Model -- Stylized Parameters",
    )

    plot_price_distribution(
        values=S_paths.ravel(),
        title="Distribution of Simulated Electricity Prices",
    )

    plot_acf(
        values=S_paths[0],
        max_lag=30,
        title="ACF of One Simulated Electricity-Price Path",
    )

    plot_statistic_distribution(
        simulated_statistics=stats["std"],
        statistic_name="Annual Path Standard Deviation",
    )

    return {
        "paths": S_paths,
        "statistics": stats,
    }


if __name__ == "__main__":
    run_fitted_model_simulation()