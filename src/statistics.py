import numpy as np
import pandas as pd

def summary_statistics(values):
    """
    Compute basic distributional statistics for a one-dimensional
    electricity-price series.

    Parameters
    ----------
    values : array_like
        Electricity-price observations.

    Returns
    -------
    stats : dict
        Mean, standard deviation, selected quantiles, minimum
        and maximum.
    """
    values = np.asarray(values, dtype=float)

    return {
        "mean": np.mean(values),
        "std": np.std(values, ddof=1),
        "q05": np.quantile(values, 0.05),
        "q50": np.quantile(values, 0.50),
        "q95": np.quantile(values, 0.95),
        "q99": np.quantile(values, 0.99),
        "min": np.min(values),
        "max": np.max(values),
    }


def autocorrelation(values, lag):
    """
    Compute the sample autocorrelation at a given lag.

    Parameters
    ----------
    values : array_like
        One-dimensional time series.

    lag : int
        Lag measured in observations.

    Returns
    -------
    acf : float
        Sample autocorrelation at the requested lag.
    """
    values = np.asarray(values, dtype=float)

    if lag < 1 or lag >= len(values):
        raise ValueError(
            "lag must satisfy 1 <= lag < len(values)"
        )

    return np.corrcoef(
        values[:-lag],
        values[lag:],
    )[0, 1]


def autocorrelations(values, lags):
    """
    Compute sample autocorrelations for several lags.

    Returns
    -------
    acf : dict
        Dictionary mapping each lag to its autocorrelation.
    """
    return {
        lag: autocorrelation(values, lag)
        for lag in lags
    }


def extreme_frequency(
    values,
    upper_threshold=None,
    lower_threshold=None,
):
    """
    Compute the fraction of observations exceeding specified
    upper or lower price thresholds.

    Parameters
    ----------
    values : array_like
        Electricity-price observations.

    upper_threshold : float, optional
        Upper extreme-price threshold.

    lower_threshold : float, optional
        Lower extreme-price threshold.

    Returns
    -------
    frequencies : dict
        Fractions of observations above/below the thresholds.
    """
    values = np.asarray(values, dtype=float)

    frequencies = {}

    if upper_threshold is not None:
        frequencies["above_upper"] = np.mean(
            values > upper_threshold
        )

    if lower_threshold is not None:
        frequencies["below_lower"] = np.mean(
            values < lower_threshold
        )

    return frequencies


def path_statistics(
    values,
    acf_lags=(1, 7, 30),
    upper_threshold=None,
    lower_threshold=None,
):
    """
    Compute the main validation statistics for one electricity-price
    time series.

    This function can be applied both to historical data and to an
    individual simulated path.

    Returns
    -------
    stats : dict
        Distributional, dependence and extreme-price statistics.
    """
    stats = summary_statistics(values)

    acf = autocorrelations(
        values,
        lags=acf_lags,
    )

    for lag, value in acf.items():
        stats[f"acf_{lag}"] = value

    extremes = extreme_frequency(
        values,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold,
    )

    stats.update(extremes)

    return stats


def simulated_path_statistics(
    S_paths,
    acf_lags=(1, 7, 30),
    upper_threshold=None,
    lower_threshold=None,
):
    """
    Compute validation statistics separately for every simulated path.

    Parameters
    ----------
    S_paths : ndarray, shape (N, M + 1)
        Simulated electricity-price paths.

    Returns
    -------
    results : dict
        Each key corresponds to a validation statistic and contains
        one value per simulated path.
    """
    S_paths = np.asarray(S_paths, dtype=float)

    path_results = [
        path_statistics(
            path,
            acf_lags=acf_lags,
            upper_threshold=upper_threshold,
            lower_threshold=lower_threshold,
        )
        for path in S_paths
    ]

    keys = path_results[0].keys()

    return {
        key: np.array([
            result[key]
            for result in path_results
        ])
        for key in keys
    }

def validation_summary(
        historical_values,
        S_paths,
        acf_lags=(1, 7, 30),
        upper_threshold=100.0,
        lower_threshold=0.0,
        interval=(0.05, 0.95),
):
    """
    Compare historical statistics with their distribution across
    simulated paths.
    """
    historical_values = np.asarray(historical_values, dtype=float)
    historical_values = historical_values[np.isfinite(historical_values)]

    paths = np.asarray(S_paths, dtype=float)

    if paths.ndim != 2:
        raise ValueError("S_paths must have shape (N, M + 1)")

    # Remove the common initial value at time zero.
    paths = paths[:, 1:]

    lower_q, upper_q = interval
    historical = path_statistics(
        historical_values,
        acf_lags=acf_lags,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold,
    )

    simulated = simulated_path_statistics(
        paths,
        acf_lags=acf_lags,
        upper_threshold=upper_threshold,
        lower_threshold=lower_threshold,
    )

    rows = []

    for name, historical_value in historical.items():
        simulated_values = simulated[name]

        rows.append({
            "statistic": name,
            "historical": historical_value,
            "simulated_median": np.median(simulated_values),
            "simulated_q05": np.quantile(simulated_values, lower_q),
            "simulated_q95": np.quantile(simulated_values, upper_q),
        })

    return pd.DataFrame(rows).set_index("statistic")