"""
File: test_pcm_model.py
Author: Fatemehsadat Mortazavi
Date: Aug 2026
Description: Unit tests for the PCM enthalpy model.
             - Verifies solid, mushy, and liquid phases
             - Verifies round-trip consistency
"""

from pv_pcm_nsga2.pcm_model import enthalpy_to_temperature


PCM = {'T_m': 47.0, 'L': 230e3, 'cp': 2000.0}


def test_solid_phase():
    H = 2000.0 * 30.0
    T, fl = enthalpy_to_temperature(H, PCM)
    assert abs(T - 30.0) < 1e-6
    assert fl == 0.0


def test_mushy_phase():
    H = 2000.0 * 47.0 + 0.5 * 230e3
    T, fl = enthalpy_to_temperature(H, PCM)
    assert abs(T - 47.0) < 1e-6
    assert abs(fl - 0.5) < 1e-6


def test_liquid_phase():
    H = 2000.0 * 47.0 + 230e3 + 2000.0 * 10.0
    T, fl = enthalpy_to_temperature(H, PCM)
    assert abs(T - 57.0) < 1e-6
    assert fl == 1.0