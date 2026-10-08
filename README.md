# Statistical Modelling of Nordic Electricity Prices

## Objective

Estimate and validate a compact stochastic model for SE3 day-ahead electricity prices using ENTSO-E data. The model separates deterministic seasonality, ordinary mean-reverting fluctuations, and temporary price spikes.

## Data

- Market: **SE3**
- Source: **[ENTSO-E Transparency Platform](https://transparency.entsoe.eu/)**
- Estimation sample: **1 Jan 2023 – 16 Sep 2026**
- Frequency: daily averages of day-ahead prices
- Observations: **1,355 daily prices**

## Model

$$
S_t = \mu(t) + Y_t + Z_t
$$

with

$$
dY_t = -\kappa Y_t\,dt + \sigma\,dW_t
$$

and

$$
dZ_t = -\kappa_J Z_t\,dt + dJ_t.
$$

The seasonal component uses annual and semiannual harmonics:

$$
\mu(t)=
a_0
+a_1\cos\left(\frac{2\pi t}{365}\right)
+b_1\sin\left(\frac{2\pi t}{365}\right)
+a_2\cos\left(\frac{4\pi t}{365}\right)
+b_2\sin\left(\frac{4\pi t}{365}\right).
$$

The jump process is compound Poisson with exponentially distributed positive jump sizes.

## Estimation

- Seasonality: **OLS harmonic regression**
- Ordinary dynamics: **AR(1)** on deseasonalized prices
- Spike detection: residuals exceeding **3 residual standard deviations**
- Mean reversion:
  $$
  \hat{\kappa}=-\frac{\log \hat{\phi}}{\Delta}
  $$
- OU volatility: recovered from the exact OU transition variance
- Jump intensity:
  $$
  \hat{\lambda}=\frac{n_J}{T}
  $$
- Jump sizes: exponential MLE,
  $$
  \hat{\beta}=\frac{1}{\bar{\xi}}
  $$
- Spike decay: post-spike AR(1)

## Estimated parameters

| Parameter | Estimate |
|---|---:|
| $$a_0$$ | 49.67 EUR/MWh |
| $$a_1$$ | 17.76 EUR/MWh |
| $$b_1$$ | 7.73 EUR/MWh |
| $$a_2$$ | 4.67 EUR/MWh |
| $$b_2$$ | 1.32 EUR/MWh |
| $$\phi$$ | 0.6881 |
| $$\kappa$$ | 136.43 year$$^{-1}$$ |
| $$\sigma$$ | 560.50 EUR/MWh/$$\sqrt{\text{year}}$$ |
| $$\phi_J$$ | 0.5587 |
| $$\kappa_J$$ | 212.45 year$$^{-1}$$ |
| Detected spikes | 10 |
| $$\lambda$$ | 2.69 spikes/year |
| Mean jump size | 121.42 EUR/MWh |

## Simulation

The OU component is simulated using its **exact conditional transition**. Jump counts are Poisson and summed exponential jumps are sampled through the equivalent Gamma distribution.

<p align="center">
  <img src="figures/historical_simulated_paths.png" width="800">
</p>

<p align="center">
  <em>Historical SE3 daily-average prices in 2025 and three representative paths simulated from the fitted model.</em>
</p>

## Validation

Against 2025 SE3 prices, the model reproduced the upper tail reasonably well:

- historical mean, 95th percentile, 99th percentile, maximum, and share above 100 EUR/MWh all fell within the central 90% simulation ranges;
- short-term dependence was captured approximately.


<p align="center">
  <img src="figures/historical_simulated_distributions.png" width="800">
</p>

<p align="center">
  <em>Historical 2025 SE3 price distribution compared with pooled prices from 1,000 simulated one-year paths.</em>
</p>

Main mismatch:

- simulated prices were too dispersed on the downside;
- simulated negative-price frequency was **8.5%** versus **0.3%** historically;
- simulated standard deviation was somewhat too high.

This suggests that the Gaussian OU component and sequential spike-estimation procedure do not fully capture the asymmetry of observed electricity prices.

## Limitations

- sequential rather than joint estimation;
- only positive jumps are modelled;
- spike estimates depend on the chosen threshold;
- the estimation window contains only a few complete years;
- validation is descriptive and in-sample rather than out-of-sample forecasting.

## Sustainability relevance

The model provides an interpretable statistical description of electricity-price variability, persistence, and extreme events relevant to flexibility, storage, transmission, and risk management in a power system with increasing renewable penetration.

Relevant SDGs: **7, 9, and 13**.

## Relation to derivative pricing

The fitted parameters describe historical dynamics under the **physical measure**. A market-consistent electricity-derivative model would additionally require a **risk-neutral specification** and calibration to traded forwards, futures, and potentially options.

This makes the project a natural empirical complement to the earlier optimal importance sampling work: this project estimates and validates the electricity-price process, while the importance-sampling project studies efficient Monte Carlo pricing of rare energy-derivative payoffs.
