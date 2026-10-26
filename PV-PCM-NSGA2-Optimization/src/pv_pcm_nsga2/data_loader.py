"""
File: data_loader.py
Author: Fatemehsadat Mortazavi
Date: Aug 2026
Description: Data loader for NASA POWER hourly weather data.
             - Converts raw embedded arrays to pandas DataFrames
             - Computes minimum nighttime temperature (00:00-05:00) per city
             - Computes maximum ambient temperature per city
"""

import numpy as np
import pandas as pd

from . import config as cfg


def load_city_dataframe(raw_data):
    """
    Convert a raw NASA POWER array into a pandas DataFrame.

    Parameters
    ----------
    raw_data : list of list
        Each row: [Hour, G (W/m^2), T2M (°C), WS10M (m/s)].

    Returns
    -------
    pd.DataFrame
        DataFrame with columns HR, G, T2M, WS10M.
    """
    return pd.DataFrame(raw_data, columns=['HR', 'G', 'T2M', 'WS10M'])


def compute_city_metadata(df):
    """
    Compute T_min_night and T_max_amb for a city DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with columns HR, G, T2M, WS10M.

    Returns
    -------
    dict
        Keys: T_min_night (°C), T_max_amb (°C).
    """
    return {
        'T_min_night': float(df['T2M'].iloc[0:6].min()),
        'T_max_amb': float(df['T2M'].max()),
    }


def load_all_cities():
    """
    Load and preprocess all cities defined in config.

    Returns
    -------
    dict
        Nested dict: cities[name] = {'df': DataFrame, 'T_min_night': float, 'T_max_amb': float}.
    """
    cities = {}
    for name, raw in cfg.NASA_DATA_RAW.items():
        df = load_city_dataframe(raw)
        meta = compute_city_metadata(df)
        cities[name] = {'df': df, **meta}
    return cities