"""
File: plotting_poster.py
Author: Fatemehsadat Mortazavi
Date: Sep 2026
Description: Poster-specific plotting module.
             - Generates clean temperature-only plots for Yazd and Ahvaz
             - Three lines: No PCM (Clean), No PCM (Dusty), With PCM (RT45HC)
             - High resolution (300 DPI) for conference poster printing
"""

import os
import matplotlib.pyplot as plt
from .simulation import simulate_pv


# Color palette
COLOR_NO_PCM = '#E53935'      # Red
COLOR_NO_PCM_DUSTY = '#EF9A9A'  # Light red
COLOR_PCM = '#43A047'          # Green


def plot_poster_temperature(city_name, output_path, y_limits):
    """
    Generate a temperature-only plot for the conference poster.

    Parameters
    ----------
    city_name : str
        City name ('Yazd' or 'Ahvaz').
    output_path : str
        Path to save the PNG file.
    y_limits : tuple
        (y_min, y_max) for the Y axis.
    """
    # Run the three scenarios using the same simulation engine as the paper
    t, T_no_pcm, _ = simulate_pv(city_name)
    _, T_dusty, _ = simulate_pv(city_name, dusty=True)
    _, T_pcm, _ = simulate_pv(city_name, pcm_name='RT45HC', finned=True)

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)

    ax.plot(t, T_no_pcm, '--', color=COLOR_NO_PCM, linewidth=2,
            label='No PCM (Clean)')
    ax.plot(t, T_dusty, ':', color=COLOR_NO_PCM_DUSTY, linewidth=2,
            label='No PCM (Dusty)')
    ax.plot(t, T_pcm, '-', color=COLOR_PCM, linewidth=2,
            label='With PCM (RT45HC)')

    ax.set_xlabel('Time of Day (Hours)', fontsize=12)
    ax.set_ylabel('PV Panel Temperature (°C)', fontsize=12)
    ax.set_title(f'{city_name} — PCM Cooling Performance',
                 fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 24)
    ax.set_ylim(y_limits)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

    print(f"  -> Poster figure saved: {output_path}")


def generate_all_poster_figures(output_dir):
    """
    Generate all poster figures (Yazd and Ahvaz).

    Parameters
    ----------
    output_dir : str
        Directory to save the figures.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Yazd
    plot_poster_temperature(
        'Yazd',
        os.path.join(output_dir, 'fig_yazd_temp.png'),
        y_limits=(30, 90)
    )

    # Ahvaz
    plot_poster_temperature(
        'Ahvaz',
        os.path.join(output_dir, 'fig_ahvaz_temp.png'),
        y_limits=(40, 100)
    )


if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    output_dir = os.path.join(base_dir, 'outputs', 'poster')
    generate_all_poster_figures(output_dir)