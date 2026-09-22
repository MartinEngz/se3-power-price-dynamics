from src.data import load_and_clean_data
from src.estimation import run_seasonality_and_ou

if __name__ == "__main__":
  #hämta data
  daily_avg = load_and_clean_data("entso_se3/*EnergyPrices*.csv")

  # hittar spikar
  daily_avg, spikes = run_seasonality_and_ou(daily_avg)

  #sparar resultatet
  daily_avg.to_csv("SE3_deseasonalized_output.csv", index=False)
  print("\n Resultatet sparat i 'SE3_deseasonalized_output.csv'.")