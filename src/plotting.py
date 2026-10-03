import numpy as np
import matplotlib.pyplot as plt


def plot_price_paths(
    S_paths,
    T,
    max_paths=20,
    title="Simulated Electricity-Price Paths",
):
    """
    Plot a selection of simulated electricity-price paths.
    """
    N, n_times = S_paths.shape

    n_plot = min(N, max_paths)

    t_grid = np.linspace(
        0.0,
        T,
        n_times,
    )

    plt.figure(figsize=(9, 5))

    for i in range(n_plot):
        plt.plot(
            t_grid,
            S_paths[i],
            linewidth=1.0,
            alpha=0.7,
        )

    plt.xlabel("Time (years)")
    plt.ylabel("Price (EUR/MWh)")
    plt.title(title)
    plt.grid(
        True,
        linestyle=":",
        linewidth=0.8,
    )
    plt.tight_layout()
    plt.show()


def plot_price_distribution(
    values,
    bins=50,
    title="Electricity-Price Distribution",
):
    """
    Plot the empirical distribution of electricity-price observations.
    """
    values = np.asarray(values, dtype=float)

    plt.figure(figsize=(8.5, 4.8))

    plt.hist(
        values,
        bins=bins,
        density=True,
        alpha=0.7,
    )

    plt.xlabel("Price (EUR/MWh)")
    plt.ylabel("Density")
    plt.title(title)
    plt.grid(
        True,
        linestyle=":",
        linewidth=0.8,
    )
    plt.tight_layout()
    plt.show()


def plot_acf(
    values,
    max_lag=30,
    title="Electricity-Price Autocorrelation",
):
    """
    Plot the sample autocorrelation function up to max_lag.
    """
    values = np.asarray(values, dtype=float)

    lags = np.arange(1, max_lag + 1)

    acf = np.array([
        np.corrcoef(
            values[:-lag],
            values[lag:],
        )[0, 1]
        for lag in lags
    ])

    plt.figure(figsize=(8.5, 4.8))

    plt.stem(
        lags,
        acf,
    )

    plt.axhline(
        0.0,
        linewidth=0.8,
    )

    plt.xlabel("Lag (days)")
    plt.ylabel("Autocorrelation")
    plt.title(title)
    plt.grid(
        True,
        linestyle=":",
        linewidth=0.8,
    )
    plt.tight_layout()
    plt.show()


def plot_statistic_distribution(
    simulated_statistics,
    observed_value=None,
    statistic_name="Statistic",
    bins=40,
):
    """
    Plot the distribution of a statistic across simulated paths.

    Optionally add the corresponding statistic from historical data.
    """
    simulated_statistics = np.asarray(
        simulated_statistics,
        dtype=float,
    )

    plt.figure(figsize=(8.5, 4.8))

    plt.hist(
        simulated_statistics,
        bins=bins,
        alpha=0.7,
    )

    if observed_value is not None:
        plt.axvline(
            observed_value,
            linestyle="--",
            linewidth=1.5,
            label="Historical data",
        )
        plt.legend()

    plt.xlabel(statistic_name)
    plt.ylabel("Number of simulated paths")
    plt.title(
        f"Simulated Distribution of {statistic_name}"
    )
    plt.grid(
        True,
        linestyle=":",
        linewidth=0.8,
    )
    plt.tight_layout()
    plt.show()