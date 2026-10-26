"""
File: simulation.py
Author: Fatemehsadat Mortazavi
Date: Aug 2026
Description: Transient thermal-electrical simulation engine.
             - Integrates PV panel and PCM energy equations at 60-second timestep
             - Uses T_min_night as initial condition (novelty vs. previous work)
             - Returns max temperature, daily energy, and full histories
"""

import numpy as np
from scipy.integrate import trapezoid

from . import config as cfg
from .pcm_model import enthalpy_to_temperature, update_pcm_enthalpy


def simulate_daily(pcm_idx, mass_pcm, weather_df, tau, T_initial):
    """
    Simulate 24 hours with 60-second timestep.

    Parameters
    ----------
    pcm_idx : int
        Index into cfg.PCM_NAMES. Negative value means no PCM.
    mass_pcm : float
        PCM mass per unit area (kg/m^2). Ignored if pcm_idx < 0.
    weather_df : pd.DataFrame
        Hourly weather data with columns HR, G, T2M, WS10M.
    tau : float
        Glass transmissivity (0.95 clean, 0.75 dusty).
    T_initial : float
        Initial temperature of PV and PCM (°C), typically T_min_night.

    Returns
    -------
    dict
        Keys: T_max (°C), E_daily (kWh), T_pv_hist, power_hist.
    """
    dt = 60.0
    n_steps = int(24 * 3600 / dt)

    use_pcm = (pcm_idx >= 0) and (mass_pcm >= 0.001)

    if use_pcm:
        pcm = cfg.PCM_PROPERTIES[cfg.PCM_NAMES[int(pcm_idx)]]
        T_m = pcm['T_m']
        L = pcm['L']
        cp_pcm = pcm['cp']
        H_solid_max = cp_pcm * T_m
        H_liquid_min = H_solid_max + L
    else:
        T_m = 0.0
        L = 0.0
        cp_pcm = 1.0
        H_solid_max = 0.0
        H_liquid_min = 0.0
        mass_pcm = 1e-6

    T_pv = T_initial
    T_pcm = T_initial
    H_pcm = cp_pcm * T_initial

    T_pv_hist = np.zeros(n_steps)
    power_hist = np.zeros(n_steps)

    time_hours = np.linspace(0, 24, n_steps)
    G_interp = np.interp(time_hours, weather_df['HR'], weather_df['G'])
    Ta_interp = np.interp(time_hours, weather_df['HR'], weather_df['T2M'])
    Vw_interp = np.interp(time_hours, weather_df['HR'], weather_df['WS10M'])

    for i in range(n_steps):
        G = max(0.0, G_interp[i])
        Ta = Ta_interp[i]
        Vw = Vw_interp[i]

        h_front = np.clip(5.7 + 3.8 * Vw, 5.0, 50.0)

        eta = np.clip(cfg.EFF_REF * (1.0 - cfg.BETA * (T_pv - cfg.T_REF)), 0.05, 0.25)
        power_hist[i] = G * tau * cfg.ABSORPTIVITY * eta * cfg.AREA

        Q_solar = G * tau * cfg.ABSORPTIVITY * (1.0 - eta)
        Q_loss_front = (
            h_front * (T_pv - Ta)
            + cfg.EMISSIVITY * cfg.SIGMA
            * ((T_pv + 273.15) ** 4 - (Ta + 273.15) ** 4)
        )

        if use_pcm:
            Q_pv_to_pcm = cfg.K_CONTACT * (T_pv - T_pcm)
            Q_pcm_to_amb = (
                cfg.H_CONV_PCM * cfg.FIN_FACTOR * (T_pcm - Ta)
                + cfg.EMISSIVITY * cfg.SIGMA
                * ((T_pcm + 273.15) ** 4 - (Ta + 273.15) ** 4)
            )
            H_pcm = update_pcm_enthalpy(H_pcm, Q_pv_to_pcm, Q_pcm_to_amb, mass_pcm, dt)
            T_pcm, _ = enthalpy_to_temperature(H_pcm, {'T_m': T_m, 'L': L, 'cp': cp_pcm})
            T_pcm = np.clip(T_pcm, -20.0, 100.0)
        else:
            Q_pv_to_pcm = 0.0

        dT_pv = (Q_solar - Q_loss_front - Q_pv_to_pcm) / (cfg.M_PV * cfg.CP_PV) * dt
        T_pv = np.clip(T_pv + dT_pv, -20.0, 100.0)
        T_pv_hist[i] = T_pv

    time_seconds = np.arange(0, 24 * 3600, dt)
    E_daily = trapezoid(power_hist, time_seconds) / 3_600_000

    return {
        'T_max': float(np.max(T_pv_hist)),
        'E_daily': float(E_daily),
        'T_pv_hist': T_pv_hist,
        'power_hist': power_hist,
    }