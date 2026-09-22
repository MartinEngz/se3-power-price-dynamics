# Statistical Modelling of Nordic Electricity Prices

This SA2001 group project uses historical day-ahead electricity prices from the Swedish bidding zone SE3 to estimate and validate an interpretable stochastic price model. The model separates prices into deterministic seasonality, ordinary mean-reverting variation, and temporary extreme spikes.

The objective is not to develop the best possible forecasting system. Instead, the project connects real electricity-market data to transparent mathematical modelling and evaluates whether a deliberately compact model can reproduce important properties of the observed market.

## Research question

> What can historical Nordic electricity-price data tell us about price variability, seasonality, and extreme events, and why are these dynamics relevant for maintaining a reliable and flexible electricity system with increasing shares of variable renewable energy?

The project characterizes observed price dynamics; it **does not establish that renewable generation causes price spikes, volatility, or any other observed price feature**. Such a claim would require additional explanatory variables and a causal research design, both of which are outside the project scope.

## SA2001 context: 3.3 Energy Modes

The SA2001 project framework combines three components:

1. sustainability questions;
2. mathematical modelling; and
3. approaches and solutions.

Topic 3.3, **Energy Modes**, considers energy in forms ranging from conventional to renewable sources and emphasizes mathematical modelling as a way to navigate environmental, social, and economic considerations in energy-system configurations. Its keywords include renewable energy sources, energy-transition technologies, and sustainable energy systems, with application areas such as electric vehicles and smart grids.

This project approaches that broad theme through the operation of the Nordic electricity market. It uses observed SE3 prices to study statistical behaviour relevant to flexibility, reliability, and uncertainty in an increasingly low-carbon power system.

## Sustainability motivation

A power system with substantial weather-dependent wind and solar generation must continuously balance supply and demand. This makes flexibility increasingly important, including hydro flexibility, storage, demand response, reserves, dispatchable capacity, transmission, and interconnection.

Electricity prices are economic signals of market conditions, so their statistical properties matter to consumers, generators, storage operators, traders, investors, and system planners:

- **Seasonality** reflects recurring changes in supply and demand.
- **Mean reversion** describes how unusually high or low prices tend to move back toward more typical levels.
- **Volatility** measures ordinary price uncertainty.
- **Extreme spikes** can accompany unusually tight market conditions or scarcity, although their causes are not identified here.
- **Very low or negative prices** can occur when supply is abundant relative to demand and available flexibility.

The stochastic model is not itself a solution to renewable integration. Its contribution is to quantify price dynamics that inform discussions of risk, flexibility, and investment incentives. The strongest connection is to **SDG 7: Affordable and Clean Energy**, with additional links to **SDG 9: Industry, Innovation and Infrastructure** and **SDG 13: Climate Action**.

## Data

The project uses **day-ahead electricity prices for Swedish bidding zone SE3** from the [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/). ENTSO-E provides public, standardized, and reproducible European electricity-system and market data. Restricting the analysis to one bidding zone gives a single coherent time series and keeps the work manageable.

Available market-interval observations are aggregated to **daily average prices in EUR/MWh**. Daily aggregation is a deliberate modelling choice because it:

- reduces intraday complexity;
- makes estimation and interpretation more accessible;
- retains medium-term seasonality, mean reversion, and major extreme-price episodes; and
- keeps simulation and validation within the scope of the course project.

The data preparation must document the observation period, units, timestamps and time conventions, missing and duplicate observations, aggregation procedure, and treatment of anomalous or missing days. The cleaned dataset should be stored in a reproducible format with a short data dictionary or accompanying description.

## Mathematical model

The observed electricity price is modelled as

$$
S_t = \mu(t) + Y_t + Z_t,
$$

where:

- $\mu(t)$ is a deterministic seasonal component;
- $Y_t$ represents ordinary mean-reverting stochastic fluctuations; and
- $Z_t$ represents temporary price spikes.

Prices are modelled directly rather than logarithmically because electricity prices can be zero or negative.

### Harmonic seasonality

The seasonal component is represented by a two-harmonic regression:

$$ \mu(t) = a_0 + a_1\cos\left(\frac{2\pi t}{365}\right) + b_1\sin\left(\frac{2\pi t}{365}\right) + a_2\cos\left(\frac{4\pi t}{365}\right) + b_2\sin\left(\frac{4\pi t}{365}\right). $$

Here, $a_0$ is the baseline level, the first sine-cosine pair represents an annual cycle, and the second pair represents semiannual structure. The coefficients are estimated by ordinary least squares (OLS). Extra harmonics, weekday effects, or splines should be added only if clearly justified.

### Ordinary mean-reverting component

Ordinary deviations from the seasonal level follow an Ornstein-Uhlenbeck (OU) process:

$$
dY_t = -\kappa Y_t\,dt + \sigma\,dW_t.
$$

- $\kappa>0$ is the mean-reversion speed. Larger values imply a faster return toward the seasonal level. Its associated half-life is $t_{1/2} = log(2) / \kappa$.
- $\sigma>0$ controls the magnitude of ordinary stochastic price variation.
- $W_t$ is standard Brownian motion, representing many small unresolved influences on price.

After estimating seasonality, define the deseasonalized series

$$
X_t = S_t-\widehat{\mu}(t).
$$

Under the complete model, $X_t=Y_t+Z_t$, so it still contains spikes. The practical approach is therefore to fit a preliminary AR(1) model, detect extreme residuals, and re-estimate the ordinary dynamics after excluding or appropriately treating spike periods.

For observations separated by $\Delta$, the exact OU transition has the AR(1) form

$$
Y_{t+\Delta}=\phi Y_t+\varepsilon_{t+\Delta},
\qquad
\phi=e^{-\kappa\Delta}.
$$

An AR(1)/OLS estimate $\widehat{\phi}$ gives

$$
\widehat{\kappa}=-\frac{\log(\widehat{\phi})}{\Delta}.
$$

Because

$$
\text{Var}(\varepsilon)
=\frac{\sigma^2}{2\kappa}\left(1-e^{-2\kappa\Delta}\right),
$$

the diffusion volatility is estimated as

$$
\widehat{\sigma}
=\sqrt{
\widehat{\sigma}_{\varepsilon}^{2}
\frac{2\widehat{\kappa}}
{1-e^{-2\widehat{\kappa}\Delta}}
}.
$$

The baseline convention is $\Delta=1$ day. Accordingly, $\kappa$ is measured in day $^{-1}$, $\lambda$ in spikes per day, and $\sigma$ in compatible daily-time units.

### Temporary compound-Poisson spike component

Temporary spikes are represented by

$$
dZ_t=-\kappa_J Z_t\,dt+dJ_t,
$$

where $J_t$ is a compound-Poisson process,

$$
J_t=\sum_{i=1}^{N_t}\xi_i.
$$

- $N_t$ is a Poisson process with intensity $\lambda$, the expected number of spike arrivals per unit time.
- $\xi_i$ is the magnitude of jump $i$.
- $\kappa_J>0$ is the spike-decay speed. Its half-life is $t_{1/2,J}=\frac{\ln 2}{\kappa_J}$.

Economically, a jump represents an unusually large price movement that is not adequately described by ordinary Gaussian OU fluctuations. Its contribution then decays toward zero.

#### Spike detection

Candidate positive spikes are identified from residuals after fitting seasonality and a preliminary OU model. The baseline analysis should select and report one transparent rule in advance, such as:

- residual above the empirical 99th percentile; or
- residual above approximately three residual standard deviations.

One alternative threshold may be used for a small sensitivity check. Extensive threshold optimization is outside scope.

#### Jump intensity

If $n_J$ spike arrivals are detected during an observation period of length $T$, the homogeneous Poisson maximum-likelihood estimate is

$$
\hat{\lambda}=\frac{n_J}{T}.
$$

#### Jump-size distribution

The baseline positive-spike model assumes

$$
\xi\sim\text{Exp}(\beta),
$$

with maximum-likelihood estimate

$$
\hat{\beta}=\frac{1}{\overline{\xi}}.
$$

Thus $1/\beta$ is the mean spike magnitude, and a larger $\beta$ implies smaller typical jumps. Comparing this fit with another simple positive distribution, such as a lognormal distribution, is optional and should only be attempted if time permits.

#### Spike decay

The spike-decay parameter is estimated using one manageable, explainable method:

1. **Post-spike AR(1):** if $Z_{t+\Delta}\approx\phi_J Z_t$, then 

$$
\hat{\kappa}_J = -\frac{\text{log}(\hat{\phi}_J)}{\Delta}.
$$ 

2. **Empirical half-life:** estimate the typical number of days $t_{1/2,J}$ for a spike effect to halve, then set

 $$
 \hat{\kappa}_J = \frac{\text{log}(2)}{t_{1/2,J}}.
 $$

A complicated latent-state procedure is intentionally avoided.

## Estimation pipeline

1. Retrieve and clean SE3 day-ahead price data.
2. Aggregate observations to daily average EUR/MWh.
3. Inspect the complete time series and empirical distribution.
4. Estimate $\mu(t)$ by harmonic regression.
5. Compute $X_t=S_t-\hat{\mu}(t)$.
6. Fit a preliminary AR(1)/OU model.
7. Detect candidate spikes from the residuals using the chosen rule.
8. Re-estimate $\kappa$ and $\sigma$ from observations representing ordinary dynamics.
9. Estimate $\lambda$ from detected spike arrivals.
10. Estimate the jump-size distribution from detected spike magnitudes.
11. Estimate $\kappa_J$ using a post-spike decay or empirical half-life method.
12. Combine the fitted parameters and simulate synthetic price paths.
13. Validate simulated behaviour against the empirical SE3 series.
14. Interpret model successes and shortcomings in relation to the sustainability question.

This is a pragmatic two-stage procedure, not full joint maximum-likelihood estimation of a latent jump-diffusion model. That limitation is accepted to keep the methods transparent and appropriate for SA2001.

## Simulation

Simulation uses the same daily grid as the empirical dataset. For the ordinary component, the exact OU transition is preferred over an Euler approximation:

$$
Y_{t+\Delta}
=e^{-\kappa\Delta}Y_t
+\sigma\sqrt{\frac{1-e^{-2\kappa\Delta}}{2\kappa}}\,\varepsilon_t,
\qquad
\varepsilon_t\sim\mathcal{N}(0,1).
$$

For each interval, the simulation:

1. decays the existing spike component by $e^{-\kappa_J\Delta}$;
2. draws the number of arrivals from the fitted Poisson process;
3. draws their magnitudes from the fitted jump-size distribution;
4. adds the new jumps to $Z_t$; and
5. combines $\mu(t)$, $Y_t$, and $Z_t$ to obtain $S_t$.

Validation should use many simulated paths rather than relying on a single visually convenient realization.

## Model validation

The central validation question is:

> Does the fitted stochastic model reproduce important statistical characteristics of the observed SE3 electricity prices?

Validation includes:

- **Visual behaviour:** empirical prices, representative simulated paths, empirical and simulated distributions or ECDFs, and seasonal average patterns.
- **Summary statistics:** mean, variance or standard deviation, selected quantiles such as 5%, 50%, 95%, and 99%, extreme upper-tail behaviour, and detected-spike frequency.
- **Dependence:** short- and medium-lag autocorrelation functions and mean-reversion behaviour.
- **Seasonality:** broad annual and semiannual patterns generated by $\hat{\mu}(t)$.
- **Spikes:** frequency, magnitude distribution, and approximate duration or decay.

The preferred implementation simulates many paths with the same length as the historical sample, calculates each statistic for every path, and compares the observed statistic with its simulated distribution. Model mismatches are valid findings and should be discussed rather than hidden by adding unnecessary complexity.

## Scope and limitations

The project is a descriptive, interpretable stochastic analysis of one bidding zone. Unless the core work is completed early, it excludes:

- causal estimation of renewable generation's effect on prices;
- wind or solar generation as explanatory variables;
- forecasting competitions and machine-learning models;
- multiple bidding zones;
- battery optimization or trading strategies;
- regime-switching models;
- full joint likelihood or Bayesian estimation of the latent jump model;
- hourly or intraday structural modelling; and
- detailed power-flow or grid simulation.

These are possible future extensions, not requirements. In particular, observed price spikes must not be presented as effects caused by renewable generation.

## Group responsibilities

| Member(s) | Primary responsibility |
| --- | --- |
| **Albin & Antoine** | Sustainability relevance, SA2001 Energy Modes framing, research motivation, links to flexibility and SDGs, and careful non-causal interpretation. |
| **John** | ENTSO-E data acquisition and cleaning, daily aggregation, documentation, and basic descriptive outputs. |
| **Martin** | Mathematical model specification and implementation, consistent parameter conventions, exact-transition simulation, and contribution to validation. |
| **Toomany** | Seasonal, OU, and jump-parameter estimation; transparent spike detection; units and parameter interpretation. |
| **Martin & Toomany** | Integration of fitted parameters, empirical-versus-simulated validation, assessment of model strengths and limitations, and mathematical/results material. |
| **All members** | Consistency review, final report editing, sustainability interpretation, and preparation for the 15-20 minute presentation and discussion. |

## Repository workflow

The intended workflow is linear and reproducible:

$$
\text{ENTSO-E data}
\longrightarrow
\text{clean daily SE3 series}
\longrightarrow
\text{parameter estimates}
\longrightarrow
\text{simulated paths}
\longrightarrow
\text{validation and interpretation}.
$$

Contributions should keep data transformations reproducible, report parameter units and assumptions explicitly, and separate empirical findings from sustainability background. No repository structure is prescribed here; code, data documentation, figures, and results should be organized consistently as the implementation develops.

## Intended project narrative

The final report and presentation should tell one coherent story: introduce the sustainability context; ask what is observed in historical SE3 prices; model seasonality, ordinary mean-reverting fluctuations, and temporary jumps; estimate parameters from real ENTSO-E data; validate simulated against empirical behaviour; and discuss what the model captures, what it misses, and why those dynamics matter for flexibility and risk management.

The conclusion should preserve the core limitation: **the project characterizes electricity-price dynamics but does not identify the causal effect of renewable generation on prices.**
