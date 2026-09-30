# Toy parameters for testing the simulation pipeline.
# These are not fitted to SE3 data.

STYLIZED_SE3_MODEL = {
    # Simulation
    "N": 5,
    "T": 1.0,              # years
    "M": 365,              # daily steps
    "Y0": 0.0,
    "Z0": 0.0,

    # Seasonal component, EUR/MWh
    "a0": 50.0,
    "a1": 10.0,
    "b1": -5.0,
    "a2": 3.0,
    "b2": 1.0,

    # OU component
    "kappa": 8.0,          # 1/year
    "sigma": 40.0,         # EUR/MWh / sqrt(year)

    # Temporary positive spikes
    "jump_intensity": 8.0, # expected jumps/year
    "jump_scale": 30.0,    # mean jump size, EUR/MWh
    "jump_reversion": 25.0,# 1/year

    "random_seed": 123,
}


# Preliminary estimates from the current full-sample estimation pipeline.
# jump_reversion is still a placeholder and has not yet been estimated.
ESTIMATED_SE3_MODEL = {
    # Simulation
    "N": 3,
    "T": 1.0,                  # years
    "M": 365,                  # daily time steps
    "Y0": 0.0,
    "Z0": 0.0,

    # Estimated harmonic seasonality, EUR/MWh
    "a0": 48.4350,
    "a1": 9.7719,
    "b1": -4.4011,
    "a2": 3.1526,
    "b2": 1.1118,

    # Estimated OU component
    "phi": 0.8430,
    "kappa": 62.35,            # 1/year
    "sigma": 536.76,           # EUR/MWh / sqrt(year)

    # Estimated positive-spike process
    "spike_threshold": 144.2334,   # EUR/MWh
    "n_spikes": 85,
    "jump_intensity": 7.2539,      # jumps/year
    "jump_scale": 241.1772,        # mean detected spike magnitude, EUR/MWh

    # Not yet estimated
    "jump_reversion": 80.0,        # 1/year, temporary placeholder

    "random_seed": 123,
}