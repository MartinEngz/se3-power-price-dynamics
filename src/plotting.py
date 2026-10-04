import numpy as np
import pandas as pd
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

def historical_year_data(
        data,
        year,
        date_column="Date",
        price_column="EUR/MWh",
):
    """Select and clean one calendar year of historical prices."""
    dates = pd.to_datetime(data[date_column], errors="coerce")
    prices = pd.to_numeric(data[price_column], errors="coerce")

    yearly = pd.DataFrame({
        date_column: dates,
        price_column: prices
    })

    yearly = yearly.loc[dates.dt.year == int(year)]
    yearly = yearly.dropna()
    yearly = yearly.sort_values(date_column).reset_index(drop=True)

    if yearly.empty:
        available = sorted(dates.dropna().dt.year.unique())
        raise ValueError(
            f"No observations found for {year}. "
            f"Available years: {available}"
        )

    return yearly

def plot_historical_year(
    data,
    year,
    date_column="Date",
    price_column="EUR/MWh",
    save_path=None,
    show=True,
):
    """Plot historical daily-average SE3 prices for one year."""
    yearly = historical_year_data(
        data,
        year,
        date_column=date_column,
        price_column=price_column
    )
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        yearly[date_column],
        yearly[price_column],
        color="black",
        linewidth=1.1,
        label="Historical SE3 prices",
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Price (EUR/MWh)")
    ax.set_title(f"Historical SE3 Day-Ahead Prices, {year}")
    ax.grid(True, linestyle=":", linewidth=0.8)
    ax.legend()

    fig.autofmt_xdate()
    fig.tight_layout()

    if save_path is not None:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    if show:
        plt.show()

    return fig, ax