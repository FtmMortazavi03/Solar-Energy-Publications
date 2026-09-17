"""
File: simulation.py
Author: Fatemehsadat Mortazavi
Date: Jun 2026
Description: Transient thermal-electrical simulation engine.
             - Generates 24-hour weather profiles (temperature and irradiance)
             - Implements lumped capacitance thermal model for PV panel
             - Two scenarios: simple PCM and finned aluminum enclosure
             - Two conditions: clean and dusty panel
             - Returns time, PV temperature, and power output arrays
"""

import numpy as np
from . import config as cfg
from .pcm_model import enthalpy_to_temperature, update_pcm_enthalpy


def generate_weather(city_name):
    """
    Generate 24-hour profiles for ambient temperature and solar irradiance.

    Parameters
    ----------
    city_name : str
        One of: 'Yazd', 'Ahvaz', 'Bandar Abbas'.

    Returns
    -------
    time_hours : np.ndarray
        Time array (0 to 24 h) with 1-minute resolution.
    T_amb : np.ndarray
        Ambient temperature profile (°C).
    G : np.ndarray
        Solar irradiance profile (W/m^2).
    """
    city = cfg.CITIES[city_name]
    time_hours = np.linspace(0, 24, cfg.TIME_STEPS)

    # Ambient temperature: sinusoidal, peaking at 15:00
    T_amb = city['T_amb_avg'] + city['T_amp'] * np.sin(2 * np.pi * (time_hours - 9) / 24)

    # Solar irradiance: half-sine wave from 6:00 to 18:00
    G = np.zeros_like(time_hours)
    daylight = (time_hours >= 6) & (time_hours <= 18)
    G_peak = (city['G_daily_wh'] * np.pi) / 12.0
    G[daylight] = G_peak * np.sin(np.pi * (time_hours[daylight] - 6) / 12)

    return time_hours, T_amb, G


def simulate_pv(city_name, pcm_name=None, dusty=False, finned=False):
    """
    Simulate PV panel temperature and power output over 24 hours.

    Parameters
    ----------
    city_name : str
        City name ('Yazd', 'Ahvaz', 'Bandar Abbas').
    pcm_name : str or None
        PCM type ('RT42', 'RT44HC', 'RT45HC', 'RT47', 'RT50') or None.
    dusty : bool
        If True, apply dusty panel transmissivity.
    finned : bool
        If True, use finned aluminum enclosure (only if PCM present).

    Returns
    -------
    time_hours : np.ndarray
    T_pv : np.ndarray
        PV panel temperature (°C).
    P_out : np.ndarray
        Power output per unit area (W/m^2).
    """
    time_hours, T_amb_arr, G_arr = generate_weather(city_name)
    dt = (time_hours[1] - time_hours[0]) * 3600.0
    n_steps = len(time_hours)

    # Glass transmissivity
    tau = cfg.DUSTY_TAU if dusty else cfg.CLEAN_TAU

    # Initialize arrays
    T_pv = np.zeros(n_steps)
    P_out = np.zeros(n_steps)
    T_pv[0] = T_amb_arr[0]

    # PCM setup
    if pcm_name is not None:
        pcm = cfg.PCM_PROPERTIES[pcm_name]
        m_pcm = pcm['rho'] * cfg.THICKNESS_PCM
        H_pcm = np.zeros(n_steps)
        H_pcm[0] = pcm['cp'] * T_amb_arr[0]
        T_pcm = np.zeros(n_steps)
        T_pcm[0] = T_amb_arr[0]

    # Main simulation loop
    for t in range(1, n_steps):
        G = G_arr[t]
        T_a = T_amb_arr[t]

        # Electrical efficiency and power output
        eta = cfg.EFF_REF * (1.0 - cfg.BETA * (T_pv[t-1] - cfg.T_REF))
        eta = max(0.0, eta)
        P_out[t-1] = G * tau * cfg.ABSORPTIVITY * eta

        # Solar heat absorbed (after electrical conversion)
        Q_solar = G * tau * cfg.ABSORPTIVITY * (1.0 - eta)

        # Heat loss from PV front surface
        Q_conv_rad_front = (
            cfg.H_CONV_FRONT * (T_pv[t-1] - T_a)
            + cfg.SIGMA * cfg.EMISSIVITY
            * ((T_pv[t-1] + 273.15) ** 4 - (T_a + 273.15) ** 4)
        )

        if pcm_name is None:
            # Scenario: no PCM
            Q_conv_rad_back = (
                cfg.H_CONV_BACK * (T_pv[t-1] - T_a)
                + cfg.SIGMA * cfg.EMISSIVITY
                * ((T_pv[t-1] + 273.15) ** 4 - (T_a + 273.15) ** 4)
            )
            dT_pv = (Q_solar - Q_conv_rad_front - Q_conv_rad_back) / (cfg.M_PV * cfg.CP_PV) * dt
            T_pv[t] = T_pv[t-1] + dT_pv
        else:
            # Scenario: with PCM
            k_contact = cfg.K_CONTACT if finned else 50.0
            Q_pv_to_pcm = k_contact * (T_pv[t-1] - T_pcm[t-1])

            # Update PV temperature
            dT_pv = (Q_solar - Q_conv_rad_front - Q_pv_to_pcm) / (cfg.M_PV * cfg.CP_PV) * dt
            T_pv[t] = T_pv[t-1] + dT_pv

            # Heat loss from PCM to ambient
            if finned:
                Q_pcm_to_amb = (
                    cfg.H_CONV_PCM * cfg.ENCLOSURE_AREA_FACTOR * (T_pcm[t-1] - T_a)
                    + cfg.SIGMA * cfg.EMISSIVITY
                    * ((T_pcm[t-1] + 273.15) ** 4 - (T_a + 273.15) ** 4)
                )
            else:
                Q_pcm_to_amb = (
                    cfg.H_CONV_FRONT * (T_pcm[t-1] - T_a)
                    + cfg.SIGMA * cfg.EMISSIVITY
                    * ((T_pcm[t-1] + 273.15) ** 4 - (T_a + 273.15) ** 4)
                )

            # Update PCM enthalpy
            H_pcm[t] = update_pcm_enthalpy(H_pcm[t-1], Q_pv_to_pcm, Q_pcm_to_amb, m_pcm, dt)

            # Convert enthalpy to temperature
            T_pcm[t], _ = enthalpy_to_temperature(H_pcm[t], pcm)

    # Final power value
    eta_final = max(0.0, cfg.EFF_REF * (1.0 - cfg.BETA * (T_pv[-1] - cfg.T_REF)))
    P_out[-1] = G_arr[-1] * tau * cfg.ABSORPTIVITY * eta_final

    return time_hours, T_pv, P_out