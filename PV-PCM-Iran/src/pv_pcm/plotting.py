"""
File: plotting.py
Author: Fatemehsadat Mortazavi
Date: Jun 2026
Description: Visualization module for simulation results.
             - Plots PV panel temperature vs time
             - Plots power output vs time
             - Saves high-resolution figures (300 dpi) for each city
"""

import os
import matplotlib.pyplot as plt


def plot_city_results(city, time_hours,
                      T_no_pcm, P_no_pcm,
                      T_dusty, P_dusty,
                      T_best_pcm, P_best_pcm,
                      best_pcm_name, output_path,
                      scenario_label="PCM Cooling Performance"):
    """
    Create a two-panel figure (temperature and power) for one city.

    Parameters
    ----------
    city : str
        City name.
    time_hours : np.ndarray
    T_no_pcm, P_no_pcm : np.ndarray
        Temperature and power for clean panel without PCM.
    T_dusty, P_dusty : np.ndarray
        Temperature and power for dusty panel without PCM.
    T_best_pcm, P_best_pcm : np.ndarray
        Temperature and power for the best PCM scenario.
    best_pcm_name : str
        Name of the best PCM type.
    output_path : str
        Path to save the figure.
    scenario_label : str
        Title label for the figure.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # Temperature subplot
    ax1.plot(time_hours, T_no_pcm, 'r--', label='No PCM (Clean)', linewidth=1.5)
    ax1.plot(time_hours, T_dusty, 'brown', linestyle=':', label='No PCM (Dusty)', linewidth=1.5)
    ax1.plot(time_hours, T_best_pcm, 'g-', label=f'With PCM ({best_pcm_name})', linewidth=2)
    ax1.set_ylabel('PV Panel Temperature (°C)', fontsize=11)
    ax1.set_title(f'{city} - {scenario_label}', fontsize=14, fontweight='bold')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper left')

    # Power subplot
    ax2.plot(time_hours, P_no_pcm, 'r--', label='No PCM (Clean)', linewidth=1.5)
    ax2.plot(time_hours, P_dusty, 'brown', linestyle=':', label='No PCM (Dusty)', linewidth=1.5)
    ax2.plot(time_hours, P_best_pcm, 'g-', label=f'With PCM ({best_pcm_name})', linewidth=2)
    ax2.set_xlabel('Time of Day (Hours)', fontsize=11)
    ax2.set_ylabel('Power Output (W/m²)', fontsize=11)
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='upper right')

    plt.xlim(0, 24)
    plt.xticks(range(0, 25, 2))
    plt.tight_layout()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"  -> Figure saved: {output_path}")