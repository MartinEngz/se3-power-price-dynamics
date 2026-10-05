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
    "a0": 49.6667,
    "a1": 17.7604,
    "b1": 7.7254,
    "a2": 4.6718,
    "b2": 1.3214,

    # Estimated OU component
    "phi": 0.6881,
    "kappa": 136.43,            # OU reversion speed [1/year]
    "sigma": 560.50,           # EUR/MWh / sqrt(year)

    # Estimated positive-spike process
    "spike_threshold": 101.96,   # EUR/MWh
    "n_spikes": 10,
    "jump_intensity": 2.6937,      # jumps/year
    "jump_scale": 121.4195,        # mean detected spike magnitude, EUR/MWh
    "jump_reversion": 212.45,       # kappa_J
    "random_seed": 123,
}