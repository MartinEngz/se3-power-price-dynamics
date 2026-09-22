import glob
import pandas as pd


def load_and_clean_data(path_pattern="entso_se3/*EnergyPrices*.csv"):
  # hämtar alla filer
  files = sorted(glob.glob(path_pattern))
  print(f"Hittade {len(files)} filer.")

  dfs = []
  for f in files:
    df = pd.read_csv(f)
    dfs.append(df)

  #dagsmedelvärden
  combined = pd.concat(dfs, ignore_index=True)
  combined["DateTime(UTC)"] = pd.to_datetime(combined["DateTime(UTC)"])
  combined["Date"] = combined["DateTime(UTC)"].dt.date
  combined["EUR/MWh"] = pd.to_numeric(combined["EUR/MWh"], errors="coerce")

  daily_avg = combined.groupby("Date")["EUR/MWh"].mean().reset_index()
  daily_avg = daily_avg.sort_values("Date").reset_index(drop=True)

  return daily_avg