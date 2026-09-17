"""
File: test_data_loader.py
Author: Fatemehsadat Mortazavi
Date: Jun 2026
Description: Unit tests for data_loader module.
             - Tests July filtering
             - Tests climate summary calculation
"""

import os
import sys
import pandas as pd
import pytest

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from pv_pcm.data_loader import compute_july_summary, load_all_cities


def test_compute_july_summary():
    """Test July average calculation on a small synthetic dataframe."""
    df = pd.DataFrame({
        'YEAR': [2020, 2020, 2020, 2020],
        'MO':   [6, 7, 7, 8],
        'DY':   [1, 1, 2, 1],
        'T2M':  [30.0, 40.0, 42.0, 35.0],
        'T2M_MAX': [35.0, 45.0, 47.0, 40.0],
        'ALLSKY_SFC_SW_DWN': [7.0, 8.0, 8.5, 7.5]
    })

    summary = compute_july_summary(df)

    assert summary['T_amb_avg'] == 41.0
    assert summary['T_max_avg'] == 46.0
    assert summary['G_daily_wh'] == 8250.0


def test_load_all_cities_missing_file():
    """Test that missing files raise an error."""
    with pytest.raises(FileNotFoundError):
        load_all_cities('/non/existent/path')