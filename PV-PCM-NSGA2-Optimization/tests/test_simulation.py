"""
File: test_simulation.py
Author: Fatemehsadat Mortazavi
Date: Aug 2026
Description: Unit tests for the thermal simulation engine.
             - Verifies no-PCM simulation runs and returns finite values
             - Verifies PCM simulation reduces peak temperature
             - Verifies dust reduces daily energy
"""

from pv_pcm_nsga2 import config as cfg
from pv_pcm_nsga2.data_loader import load_all_cities
from pv_pcm_nsga2.simulation import simulate_daily


def test_no_pcm_runs():
    cities = load_all_cities()
    res = simulate_daily(-1, 0.0, cities['Ahvaz']['df'], cfg.TAU_CLEAN,
                         cities['Ahvaz']['T_min_night'])
    assert res['T_max'] > 0
    assert res['E_daily'] > 0


def test_pcm_reduces_peak_temperature():
    cities = load_all_cities()
    base = simulate_daily(-1, 0.0, cities['Ahvaz']['df'], cfg.TAU_CLEAN,
                          cities['Ahvaz']['T_min_night'])
    cooled = simulate_daily(4, 15.0, cities['Ahvaz']['df'], cfg.TAU_CLEAN,
                            cities['Ahvaz']['T_min_night'])
    assert cooled['T_max'] < base['T_max']


def test_dust_reduces_energy():
    cities = load_all_cities()
    clean = simulate_daily(-1, 0.0, cities['Kerman']['df'], cfg.TAU_CLEAN,
                           cities['Kerman']['T_min_night'])
    dusty = simulate_daily(-1, 0.0, cities['Kerman']['df'], cfg.TAU_DUSTY,
                           cities['Kerman']['T_min_night'])
    assert dusty['E_daily'] < clean['E_daily']