"""
File: main.py
Author: Fatemehsadat Mortazavi
Date: Aug 2026
Description: Main execution script for PV-PCM NSGA-II optimization.
             - Loads NASA POWER hourly data for three Iranian cities
             - Runs NSGA-II for clean and dusty scenarios
             - Extracts optimal designs and saves summary tables
             - Generates Pareto front and bar chart figures
"""

import os
import pandas as pd

from . import config as cfg
from .data_loader import load_all_cities
from .optimization import run_nsga2, extract_best_design
from .plotting import plot_pareto_fronts, plot_bar_comparison


def main():
    """Run full optimization pipeline and save all outputs."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    figures_dir = os.path.join(base_dir, 'outputs', 'figures')
    tables_dir = os.path.join(base_dir, 'outputs', 'tables')
    os.makedirs(figures_dir, exist_ok=True)
    os.makedirs(tables_dir, exist_ok=True)

    cities = load_all_cities()

    all_results = {}
    best_designs = {}
    rows = []

    for city in cfg.CITIES:
        all_results[city] = {}
        best_designs[city] = {}

        for label, tau in cfg.SCENARIOS:
            print(f"\n{'=' * 60}")
            print(f"  {city} - {label}")
            print(f"  T_init = {cities[city]['T_min_night']:.2f} °C")
            print(f"{'=' * 60}")

            res = run_nsga2(cities[city]['df'], tau, cities[city]['T_min_night'])
            best = extract_best_design(res)

            all_results[city][label] = res
            best_designs[city][label] = best

            print(f"  Best Design: PCM = {best['PCM']}, "
                  f"Mass = {best['Mass']:.1f} kg/m², "
                  f"T_max = {best['T_max']:.1f} °C, "
                  f"E_daily = {best['E_daily']:.3f} kWh")

            rows.append({
                'City': city,
                'Scenario': label,
                'T_min_night': cities[city]['T_min_night'],
                'PCM': best['PCM'],
                'Mass(kg/m²)': best['Mass'],
                'T_max(°C)': best['T_max'],
                'E_daily(kWh)': best['E_daily'],
            })

    # Summary table
    df = pd.DataFrame(rows)
    table_path = os.path.join(tables_dir, 'optimal_designs.csv')
    df.to_csv(table_path, index=False)
    print(f"\nSummary table saved: {table_path}")

    # Figures
    plot_pareto_fronts(all_results, os.path.join(figures_dir, 'fig1_pareto_fronts.png'))
    plot_bar_comparison(best_designs, os.path.join(figures_dir, 'fig2_bar_comparison.png'))

    print("\n" + "=" * 80)
    print("OPTIMIZATION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()