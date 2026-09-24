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


# Current preliminary SE3 parameter estimates.
#
# Seasonality and OU parameters are taken from the current
# estimation pipeline. Jump-process parameters are temporary
# toy values until the jump estimation has been inspected.

PRELIMINARY_SE3_MODEL = {
    # Simulation
    "N": 500,
    "T": 1.0,              # years
    "M": 365,              # daily time steps
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
    "kappa": 62.35,        # 1/year
    "sigma": 536.76,       # EUR/MWh / sqrt(year)

    # Temporary toy jump parameters
    "jump_intensity": 7.0,  # jumps/year
    "jump_scale": 40.0,     # EUR/MWh
    "jump_reversion": 80.0, # 1/year

    "random_seed": 123,
}
