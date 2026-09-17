"""
File: data_loader.py
Author: Fatemehsadat Mortazavi
Date: Jun 2026
Description: Data loader for NASA POWER CSV files.
             - Reads daily meteorological data (2010-2026)
             - Filters July data for each city
             - Computes average ambient temperature, maximum temperature,
               and daily solar irradiance
             - Saves processed summary to data/processed/climate_summary.csv
"""

import os
import pandas as pd


def load_nasa_csv(filepath):
    """
    Load a NASA POWER CSV file, skipping the header lines.

    Parameters
    ----------
    filepath : str
        Path to the CSV file.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: YEAR, MO, DY, T2M, T2M_MAX, ALLSKY_SFC_SW_DWN
    """
    df = pd.read_csv(
        filepath,
        skiprows=10,
        usecols=['YEAR', 'MO', 'DY', 'T2M', 'T2M_MAX', 'ALLSKY_SFC_SW_DWN']
    )
    return df


def compute_july_summary(df):
    """
    Compute average values for July (MO == 7) from a NASA POWER dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with columns YEAR, MO, T2M, T2M_MAX, ALLSKY_SFC_SW_DWN.

    Returns
    -------
    dict
        Dictionary with keys:
        - T_amb_avg : mean daily temperature (°C)
        - T_max_avg : mean daily maximum temperature (°C)
        - G_daily_wh : mean daily solar irradiance (Wh/m^2)
    """
    july = df[df['MO'] == 7]
    summary = {
        'T_amb_avg': round(july['T2M'].mean(), 2),
        'T_max_avg': round(july['T2M_MAX'].mean(), 2),
        'G_daily_wh': round(july['ALLSKY_SFC_SW_DWN'].mean() * 1000.0, 1)
    }
    return summary


def load_all_cities(raw_dir):
    """
    Load and process NASA POWER CSV files for all three cities.

    Parameters
    ----------
    raw_dir : str
        Directory containing the raw CSV files.

    Returns
    -------
    dict
        Dictionary keyed by city name, each containing the July summary.
    """
    files = {
        'Yazd': 'POWER_Point_Daily_YAZD_LST.csv',
        'Ahvaz': 'POWER_Point_Daily_AHVAZ_LST.csv',
        'Bandar Abbas': 'POWER_Point_Daily_BANDARABBAS_LST.csv'
    }

    results = {}
    for city, filename in files.items():
        filepath = os.path.join(raw_dir, filename)
        df = load_nasa_csv(filepath)
        results[city] = compute_july_summary(df)
    return results


def save_summary(results, output_path):
    """
    Save the climate summary dictionary to a CSV file.

    Parameters
    ----------
    results : dict
        Dictionary with city summaries.
    output_path : str
        Path to the output CSV file.
    """
    df = pd.DataFrame(results).T
    df.index.name = 'City'
    df.to_csv(output_path)
    print(f"Climate summary saved to: {output_path}")


if __name__ == "__main__":
    # Example usage
    RAW_DIR = os.path.join('..', '..', 'data', 'raw')
    OUTPUT_PATH = os.path.join('..', '..', 'data', 'processed', 'climate_summary.csv')

    results = load_all_cities(RAW_DIR)
    for city, summary in results.items():
        print(f"{city}: {summary}")

    save_summary(results, OUTPUT_PATH)