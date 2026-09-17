"""
File: pcm_model.py
Author: Fatemehsadat Mortazavi
Date: Jun 2026
Description: Phase Change Material (PCM) thermal model.
             - Implements the enthalpy method for phase change simulation
             - Handles solid, mushy, and liquid phases
             - Computes PCM temperature from enthalpy at each timestep
"""


def enthalpy_to_temperature(H, pcm):
    """
    Convert PCM enthalpy to temperature using the enthalpy method.

    Parameters
    ----------
    H : float
        Current enthalpy of the PCM layer (J/kg).
    pcm : dict
        PCM properties with keys: T_m (melting temperature, °C),
        L (latent heat, J/kg), cp (specific heat, J/kg.K).

    Returns
    -------
    T : float
        PCM temperature (°C).
    liquid_fraction : float
        Fraction of PCM in liquid phase (0 = solid, 1 = liquid).
    """
    H_solid_max = pcm['cp'] * pcm['T_m']
    H_liquid_min = H_solid_max + pcm['L']

    if H <= H_solid_max:
        # Completely solid
        T = H / pcm['cp']
        liquid_fraction = 0.0
    elif H >= H_liquid_min:
        # Completely liquid
        T = pcm['T_m'] + (H - H_liquid_min) / pcm['cp']
        liquid_fraction = 1.0
    else:
        # Mushy zone (phase change in progress)
        T = pcm['T_m']
        liquid_fraction = (H - H_solid_max) / pcm['L']

    return T, liquid_fraction


def update_pcm_enthalpy(H_prev, Q_pv_to_pcm, Q_pcm_to_amb, m_pcm, dt):
    """
    Update PCM enthalpy based on heat fluxes.

    Parameters
    ----------
    H_prev : float
        Previous enthalpy (J/kg).
    Q_pv_to_pcm : float
        Heat flux from PV panel to PCM (W/m^2).
    Q_pcm_to_amb : float
        Heat flux from PCM to ambient (W/m^2).
    m_pcm : float
        PCM mass per unit area (kg/m^2).
    dt : float
        Timestep (s).

    Returns
    -------
    H_new : float
        Updated enthalpy (J/kg).
    """
    dH = (Q_pv_to_pcm - Q_pcm_to_amb) / m_pcm * dt
    return H_prev + dH