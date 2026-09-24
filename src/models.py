# Electricity price / SDE simulation
import numpy as np

def harmonic_seasonality(t, a0, a1, b1, a2, b2, period=365.0):
    """
    Deterministic harmonic seasonality for electricity price.

    Model:
        mu(t) = a0 
            + a1 * cos(2*pi*t / period)
            + b1 * sin(2*pi*t / period)
            + a2 * cos(4*pi*t / period)
            + b2 * sin(4*pi*t / period)
    
    Parameters
        t : float or ndarray
        Time measured in the same units as period.

        a0 : float
            Baseline price level.

        a1, b1 : float
            Annual harmonic coefficients.

        a2, b2 : float
            Semiannual harmonic coefficients.

        period : float, optional
            Length of one seasonal cycle.
            Default is 365 days.

        Returns
        -------
        mu : float or ndarray
            Seasonal electricity-price level.
    """
    return (
        a0 +
        a1 * np.cos(2 * np.pi * t / period) +
        b1 * np.sin(2 * np.pi * t / period) +
        a2 * np.cos(4 * np.pi * t / period) +
        b2 * np.sin(4 * np.pi * t / period)        
    )

def simulate_ou_paths(N, Y0, kappa, sigma, T, M, rng=None, Z=None):
    """
    Simulate the deseasonalized mean-reverting price component
        dY_t = -kappa * Y_t dt
    
    Parameters
        N : int
            Number of simulated paths.

        Y0 : float
            Initial value of the deseasonalized price component.

        kappa : float
            Mean-reversion speed.

        sigma : float
            Diffusion volatility.

        T : float
            Simulation horizon.

        M : int
            Number of time steps.

        rng : np.random.Generator, optional
            Random number generator.

        Z : ndarray, optional, shape (N, M)
            Pre-generated independent standard normal random variables.
            Supplying these allows the same random numbers to be reused.
    Returns
        Y_paths : ndarray, shape (N, M + 1)
            Simulated OU paths.
    """
    if rng is None:
        rng = np.random.default_rng()

    dt = T / M

    if Z is None:
        Z = rng.standard_normal(size=(N, M))

    Y_paths = np.empty((N, M + 1))
    Y_paths[:, 0] = Y0

    decay = np.exp(-kappa * dt)

    ou_std = sigma * np.sqrt(
        (1 - np.exp(-2 * kappa * dt)) / (2 * kappa)
    )

    for m in range(M):
        Y_paths[:, m + 1] = (
            decay * Y_paths[:, m] + ou_std * Z[:, m]
        )

    return Y_paths

def simulate_mean_reverting_jump_price_paths(
        N,
        Y0,
        Z0,
        kappa,
        sigma,
        T,
        M,
        seasonal_mean,
        jump_intensity,
        jump_scale,
        jump_reversion,
        rng=None,
        normal_draws=None,
        jump_increments=None
):
    """
    Simulate a seasonal mean-reverting electricity-price model
    with temporary positive price spikes.

    Model:
        S_t = mu(t) + Y_t + Z_t
    where,
        dY_t = -kappa * Y_t dt + sigma dW_t
        dZ_t = -jump_reversion * Z_t dt + dJ_t
    and J_t is a compouond_Poisson process with intensity 
    jump_intensity and exponentially distributed positive
    jump size.

    The OU component is simulated using its exact transition (using 
    the analytical solution of the OU SDE derived by applying Ito's 
    product rule).
    The spile component decays exponentially between jumps.

    Parameters:
        N: int 
            number of simulated paths
        Y0: float
            initial value of the ordinary mean-reverting component
        Z0: float
            initial value of the temporary spike component
        kappa: float
            mean-reversion speed of the ordinary price component
        sigma: float
            diffusion volatility
        T: float 
            time horizon
        M: int
            number of time steps
        seasonal_mean: callable
            function mu(t) returning the deterministic seasonal 
            electricity-price model
        jump_intensity: float
            expected number of jumps per unit time
        jump_scale: float
            mean size of individual exponential jumps.
        jump_reversion: float
            mean-reversion speed
        rng: np.random.Generator, optional
            random number generator
        normal_draws: ndarray, optional, shape (N, M)
            pre-generated independent standard normal random variables
        jump_increments: ndarray, optional, shape (N, M)
            pre-generated compound-Poisson jump increments 
    Returns:
        S_paths: ndarray, shape (N, M+1)
            simulated electricity-price paths.
    """
    if rng is None:
        rng = np.random.default_rng()

    dt = T / M

    # --- Gaussian innovations
    if normal_draws is None:
        normal_draws = rng.standard_normal(size=(N, M))

    # --- Compound-Poisson jump increments
    if jump_increments is None:
        jump_counts = rng.poisson(jump_intensity * dt, size=(N, M))

        jump_increments = np.zeros((N, M))

        mask = jump_counts > 0

        # Sum of n Exp(scale) variables is Gamma(n, scale)
        jump_increments[mask] = rng.gamma(shape=jump_counts[mask], scale=jump_scale)

    # --- State variables
    Y_paths = np.empty((N, M+1))
    Z_paths = np.empty((N, M+1))

    Y_paths[:, 0] = Y0
    Z_paths[:, 0] = Z0

    S_paths = np.empty((N, M+1))
    S_paths[:, 0] = seasonal_mean(0.0) + Y0 + Z0

    # --- Exact Ohrnstein-Uhlenbeck transition coefficients (using analytical solution of OU SDE derived by Ito product rule)
    ou_decay = np.exp(-kappa * dt)
    ou_std = sigma * np.sqrt( (1 - np.exp(-2 * kappa * dt)) / (2 * kappa))

    # --- jump/spike decay factor
    jump_decay = np.exp(-jump_reversion * dt)

    # --- simulation
    for m in range(M):
        t_next = (m+1) * dt

        # Update Y_paths (mean-reverting model component)
        Y_paths[:, m+1] = ou_decay * Z_paths[:, m] + ou_std * normal_draws[:,m] 

        # Update Z_paths (temporary spike component)
        Z_paths[:, m+1] = jump_decay * Z_paths[:, m] + jump_increments[:, m]

        # Observed electricity price
        S_paths[:, m+1] = seasonal_mean(t_next) + Y_paths[:, m+1] + Z_paths[:, m+1]

    return S_paths

