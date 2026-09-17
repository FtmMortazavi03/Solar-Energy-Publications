"""
File: test_simulation.py
Author: Fatemehsadat Mortazavi
Date: Jun 2026
Description: Unit tests for simulation module.
             - Tests weather profile generation
             - Tests simulation output dimensions
             - Tests PCM enthalpy calculation
"""

import os
import sys
import numpy as np
import pytest

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from pv_pcm.simulation import generate_weather, simulate_pv
from pv_pcm.pcm_model import enthalpy_to_temperature
from pv_pcm import config as cfg


def test_generate_weather_shapes():
    """Test that weather arrays have the correct length."""
    t, T_amb, G = generate_weather('Yazd')
    assert len(t) == cfg.TIME_STEPS
    assert len(T_amb) == cfg.TIME_STEPS
    assert len(G) == cfg.TIME_STEPS


def test_irradiance_zero_at_night():
    """Test that irradiance is zero before 6:00 and after 18:00."""
    t, _, G = generate_weather('Yazd')
    # Before 6:00
    assert np.all(G[t < 6] == 0)
    # After 18:00
    assert np.all(G[t > 18] == 0)


def test_simulation_no_pcm():
    """Test simulation without PCM returns expected shapes."""
    t, T_pv, P_out = simulate_pv('Yazd')
    assert len(t) == cfg.TIME_STEPS
    assert len(T_pv) == cfg.TIME_STEPS
    assert len(P_out) == cfg.TIME_STEPS
    # Temperature should be above ambient during the day
    assert T_pv.max() > cfg.CITIES['Yazd']['T_amb_avg']


def test_simulation_with_pcm():
    """Test simulation with PCM reduces peak temperature."""
    _, T_no_pcm, _ = simulate_pv('Yazd')
    _, T_pcm, _ = simulate_pv('Yazd', pcm_name='RT45HC', finned=True)
    # With finned PCM, peak temperature should be lower
    assert T_pcm.max() < T_no_pcm.max()


def test_enthalpy_solid_phase():
    """Test enthalpy-to-temperature conversion in solid phase."""
    pcm = cfg.PCM_PROPERTIES['RT42']
    H_low = pcm['cp'] * 20.0  # at 20°C, solid
    T, lf = enthalpy_to_temperature(H_low, pcm)
    assert T == 20.0
    assert lf == 0.0


def test_enthalpy_liquid_phase():
    """Test enthalpy-to-temperature conversion in liquid phase."""
    pcm = cfg.PCM_PROPERTIES['RT42']
    H_high = pcm['cp'] * pcm['T_m'] + pcm['L'] + pcm['cp'] * 10.0
    T, lf = enthalpy_to_temperature(H_high, pcm)
    assert T > pcm['T_m']
    assert lf == 1.0


def test_enthalpy_mushy_phase():
    """Test enthalpy-to-temperature conversion in phase change zone."""
    pcm = cfg.PCM_PROPERTIES['RT42']
    H_mid = pcm['cp'] * pcm['T_m'] + 0.5 * pcm['L']
    T, lf = enthalpy_to_temperature(H_mid, pcm)
    assert T == pcm['T_m']
    assert 0.0 < lf < 1.0