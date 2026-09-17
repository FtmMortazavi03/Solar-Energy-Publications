"""
File: main.py
Author: Fatemehsadat Mortazavi
Date: Jun 2026
Description: Main execution script for PV-PCM-Iran simulation.
             - Loads climate data for three cities
             - Runs all scenarios (no PCM, simple PCM, finned PCM)
             - Compares five PCM types in clean and dusty conditions
             - Generates figures and summary tables
"""

import os
import numpy as np
import pandas as pd
from . import config as cfg
from .simulation import simulate_pv
from .plotting import plot_city_results


def compute_energy(P_out, time_hours):
    """Integrate power over time to get daily energy (kWh/m^2)."""
    return np.trapezoid(P_out, time_hours) / 1000.0


def run_city(city_name, output_dir):
    """
    Run all scenarios for a single city and save results.

    Parameters
    ----------
    city_name : str
    output_dir : str
        Directory to save figures.

    Returns
    -------
    tuple
        (rows, best_pcm_name, best_energy, e_no_pcm)
    """
    print(f"\nProcessing {city_name}...")
    rows = []

    # Scenario 1: No PCM, clean
    t, T_no_pcm, P_no_pcm = simulate_pv(city_name)
    e_no_pcm = compute_energy(P_no_pcm, t)
    rows.append([city_name, 'No PCM (Clean)', max(T_no_pcm), e_no_pcm])

    # Scenario 2: No PCM, dusty
    _, T_dusty, P_dusty = simulate_pv(city_name, dusty=True)
    e_dusty = compute_energy(P_dusty, t)
    rows.append([city_name, 'No PCM (Dusty)', max(T_dusty), e_dusty])

    # ==========================================
    # Scenario 3A: SIMPLE PCM (no fins)
    # ==========================================
    best_simple_pcm = None
    best_simple_energy = -1.0
    best_simple_T = None
    best_simple_P = None

    for pcm_name in cfg.PCM_PROPERTIES.keys():
        _, T_pcm, P_pcm = simulate_pv(city_name, pcm_name=pcm_name, finned=False)
        e_pcm = compute_energy(P_pcm, t)
        rows.append([city_name, f'{pcm_name} Simple (Clean)', max(T_pcm), e_pcm])

        if e_pcm > best_simple_energy:
            best_simple_energy = e_pcm
            best_simple_pcm = pcm_name
            best_simple_T = T_pcm
            best_simple_P = P_pcm

    # Plot simple PCM results
    fig_path_simple = os.path.join(
        output_dir, f'{city_name.replace(" ", "_")}_Simple_PCM_No_Fins.png'
    )
    plot_city_results(
        city_name, t,
        T_no_pcm, P_no_pcm,
        T_dusty, P_dusty,
        best_simple_T, best_simple_P,
        best_simple_pcm, fig_path_simple,
        scenario_label="Simple PCM (No Fins) Performance"
    )

    # ==========================================
    # Scenario 3B: FINNED PCM
    # ==========================================
    best_pcm_name = None
    best_energy = -1.0
    best_T = None
    best_P = None

    for pcm_name in cfg.PCM_PROPERTIES.keys():
        _, T_pcm, P_pcm = simulate_pv(city_name, pcm_name=pcm_name, finned=True)
        e_pcm = compute_energy(P_pcm, t)
        rows.append([city_name, f'{pcm_name} Finned (Clean)', max(T_pcm), e_pcm])

        if e_pcm > best_energy:
            best_energy = e_pcm
            best_pcm_name = pcm_name
            best_T = T_pcm
            best_P = P_pcm

    # Plot finned PCM results
    fig_path_finned = os.path.join(
        output_dir, f'{city_name.replace(" ", "_")}_PCM_Analysis.png'
    )
    plot_city_results(
        city_name, t,
        T_no_pcm, P_no_pcm,
        T_dusty, P_dusty,
        best_T, best_P,
        best_pcm_name, fig_path_finned,
        scenario_label="PCM with Finned Enclosure Performance"
    )

    return rows, best_pcm_name, best_energy, e_no_pcm


def main():
    """Main entry point."""
    # Paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    figures_dir = os.path.join(base_dir, 'outputs', 'figures')
    tables_dir = os.path.join(base_dir, 'outputs', 'tables')

    os.makedirs(figures_dir, exist_ok=True)
    os.makedirs(tables_dir, exist_ok=True)

    # Run simulations for each city
    all_rows = []
    improvements = []

    for city_name in cfg.CITIES.keys():
        rows, best_pcm, e_best, e_base = run_city(city_name, figures_dir)
        all_rows.extend(rows)

        delta_E = (e_best - e_base) / e_base * 100.0
        improvements.append([city_name, best_pcm, e_base, e_best, delta_E])

    # Summary table
    df_summary = pd.DataFrame(
        all_rows,
        columns=['City', 'Scenario', 'Max Temp (°C)', 'Daily Yield (kWh/m²)']
    )
    summary_path = os.path.join(tables_dir, 'summary_results.csv')
    df_summary.to_csv(summary_path, index=False)
    print(f"\nSummary table saved: {summary_path}")

    # Improvement table
    df_imp = pd.DataFrame(
        improvements,
        columns=['City', 'Best PCM', 'Base Energy', 'Best Energy', 'Improvement (%)']
    )
    imp_path = os.path.join(tables_dir, 'improvement_summary.csv')
    df_imp.to_csv(imp_path, index=False)
    print(f"Improvement table saved: {imp_path}")

    # Print summary to console
    print("\n" + "=" * 75)
    print("PERFORMANCE IMPROVEMENT SUMMARY")
    print("=" * 75)
    for row in improvements:
        print(f"{row[0]:<15} | Best PCM: {row[1]:<10} | Energy Gain: {row[4]:+.2f}%")
    print("=" * 75)
    print("\nAll simulations completed successfully.")


if __name__ == "__main__":
    main()