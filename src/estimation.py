import numpy as np
import statsmodels.api as sm


def run_seasonality_and_ou(daily_avg):
  #säsongskomponenter och kör OLS
  daily_avg["t"] = np.arange(len(daily_avg))
  daily_avg["cos1"] = np.cos(2 * np.pi * daily_avg["t"] / 365)
  daily_avg["sin1"] = np.sin(2 * np.pi * daily_avg["t"] / 365)
  daily_avg["cos2"] = np.cos(4 * np.pi * daily_avg["t"] / 365)
  daily_avg["sin2"] = np.sin(4 * np.pi * daily_avg["t"] / 365)

  X = daily_avg[["cos1", "sin1", "cos2", "sin2"]]
  X = sm.add_constant(X)
  y = daily_avg["EUR/MWh"]

  model = sm.OLS(y, X).fit()
  print(model.summary())

  daily_avg["mu_hat"] = model.predict(X)
  daily_avg["X_t"] = daily_avg["EUR/MWh"] - daily_avg["mu_hat"]

  #(kappa och sigma)
  X_t_series = daily_avg["X_t"].dropna().values
  y_ar = X_t_series[1:]
  x_ar = X_t_series[:-1]

  ar_model = sm.OLS(y_ar, x_ar).fit()
  phi = ar_model.params[0]

  delta_t = 1 / 365
  kappa = -np.log(phi) / delta_t

  epsilon_var = np.var(ar_model.resid)
  sigma = np.sqrt(
      (epsilon_var * 2 * kappa) / (1 - np.exp(-2 * kappa * delta_t))
  )

  print("\nornstein-uhlenbeck Parametrar")
  print(f"Phi: {phi:.4f}")
  print(f"Kappa: {kappa:.2f}")
  print(f"Sigma: {sigma:.2f}")

  #prisspikar
  std_X = daily_avg["X_t"].std()
  threshold = 3 * std_X
  spikes = daily_avg[np.abs(daily_avg["X_t"]) > threshold].copy()

  print(f"\n Spikar")
  print(f"Tröskelvärde: +/- {threshold:.2f} EUR/MWh")
  print(f"{len(spikes)} spikar")

  #kappa_J (AR(1) på dagarna efter varje spik)
  n_after = 3
  spike_pos = np.where(np.abs(X_t_series) > threshold)[0]
  x_now, x_next = [], []
  for i in spike_pos:
    for k in range(n_after):
      if i + k + 1 < len(X_t_series):
        x_now.append(X_t_series[i + k])
        x_next.append(X_t_series[i + k + 1])
  phi_J = sm.OLS(np.array(x_next), np.array(x_now)).fit().params[0]
  kappa_J = -np.log(phi_J) / delta_t if phi_J > 0 else np.nan
  print(f"Phi_J: {phi_J:.4f}")
  print(f"Kappa_J: {kappa_J:.2f}")

  return daily_avg, spikes