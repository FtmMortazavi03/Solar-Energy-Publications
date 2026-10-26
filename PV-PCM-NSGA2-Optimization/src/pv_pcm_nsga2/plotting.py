"""
File: plotting.py
Author: Fatemehsadat Mortazavi
Date: Aug 2026
Description: Visualization module for NSGA-II results.
             - Combined Pareto front for all cities and scenarios
             - Bar chart comparison of optimal T_max and E_daily
             - Saves high-resolution figures (300 dpi) to outputs/figures
"""

import os
import matplotlib.pyplot as plt
import numpy as np

from . import config as cfg


# Color palette (per city and scenario)
COLORS = {
    'Ahvaz':   {'Clean': 'red',   'Dusty': 'darkred'},
    'Kerman':  {'Clean': 'blue',  'Dusty': 'darkblue'},
    'Zahedan': {'Clean': 'green', 'Dusty': 'darkgreen'},
}
MARKERS = {
    'Ahvaz':   {'Clean': 'o', 'Dusty': 's'},
    'Kerman':  {'Clean': '^', 'Dusty': 'v'},
    'Zahedan': {'Clean': 'D', 'Dusty': 'p'},
}


def plot_pareto_fronts(all_results, output_path):
    """
    Plot combined Pareto fronts for all cities and scenarios.

    Parameters
    ----------
    all_results : dict
        Nested dict: results[city][scenario] = pymoo Result.
    output_path : str
        Path to save the figure.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    for city in cfg.CITIES:
        for label, _ in cfg.SCENARIOS:
            res = all_results[city][label]
            ax.scatter(
                res.F[:, 0], -res.F[:, 1],
                c=COLORS[city][label],
                marker=MARKERS[city][label],
                s=20, alpha=0.6,
                edgecolors='black', linewidth=0.3,
                label=f'{city} - {label}',
            )

    ax.set_xlabel('Maximum PV Temperature (°C)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Daily Energy Output (kWh)', fontsize=12, fontweight='bold')
    ax.set_title(
        'Pareto Fronts: PV-PCM Multi-Objective Optimization\n'
        '(NSGA-II, T_init = T_min_night)',
        fontsize=13, fontweight='bold',
    )
    ax.legend(fontsize=9, loc='lower left', ncol=2, framealpha=0.9)
    ax.grid(True, linestyle=':', alpha=0.4)
    ax.set_xlim(40, 100)
    ax.set_ylim(0.4, 1.6)
    plt.tight_layout()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  -> Figure saved: {output_path}")


def plot_bar_comparison(best_designs, output_path):
    """
    Bar chart of optimal T_max and E_daily for all six scenarios.

    Parameters
    ----------
    best_designs : dict
        Nested dict: best_designs[city][scenario] = dict.
    output_path : str
        Path to save the figure.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    x_labels, T_vals, E_vals, colors = [], [], [], []
    for city in cfg.CITIES:
        for label, _ in cfg.SCENARIOS:
            x_labels.append(f'{city}\n{label}')
            T_vals.append(best_designs[city][label]['T_max'])
            E_vals.append(best_designs[city][label]['E_daily'])
            colors.append(COLORS[city][label])

    x_pos = np.arange(len(x_labels))

    bars1 = ax1.bar(x_pos, T_vals, color=colors, edgecolor='black', linewidth=0.5)
    ax1.set_ylabel('Maximum PV Temperature (°C)', fontsize=11, fontweight='bold')
    ax1.set_title('Optimal Maximum Temperature by City and Scenario',
                  fontsize=12, fontweight='bold')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(x_labels, fontsize=9)
    ax1.grid(axis='y', linestyle=':', alpha=0.4)
    ax1.set_ylim(0, 80)
    for bar, val in zip(bars1, T_vals):
        ax1.text(bar.get_x() + bar.get_width() / 2., bar.get_height() + 1,
                 f'{val:.1f}', ha='center', va='bottom', fontsize=8, fontweight='bold')

    bars2 = ax2.bar(x_pos, E_vals, color=colors, edgecolor='black', linewidth=0.5)
    ax2.set_ylabel('Daily Energy Output (kWh)', fontsize=11, fontweight='bold')
    ax2.set_title('Optimal Daily Energy by City and Scenario',
                  fontsize=12, fontweight='bold')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(x_labels, fontsize=9)
    ax2.grid(axis='y', linestyle=':', alpha=0.4)
    ax2.set_ylim(0, 1.8)
    for bar, val in zip(bars2, E_vals):
        ax2.text(bar.get_x() + bar.get_width() / 2., bar.get_height() + 0.02,
                 f'{val:.3f}', ha='center', va='bottom', fontsize=8, fontweight='bold')

    plt.tight_layout()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  -> Figure saved: {output_path}")