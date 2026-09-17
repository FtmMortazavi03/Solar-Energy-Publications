# PV-PCM-Iran

Simulation of photovoltaic panel cooling using Phase Change Materials (PCM) in hot climates of Iran.

## Author

Fatemehsadat Mortazavi

## Description

This project simulates the thermal and electrical performance of a photovoltaic (PV) panel with a Phase Change Material (PCM) layer attached to its back surface. The simulation covers three cities in Iran with distinct climates:

- **Yazd** (hot-arid)
- **Ahvaz** (hot-semi-humid with heavy dust)
- **Bandar Abbas** (hot-humid)

Five commercial PCMs from Rubitherm are compared:

- RT42
- RT44HC
- RT45HC
- RT47
- RT50

Two design scenarios are considered:

1. **Simple PCM** (no enclosure)
2. **Finned aluminum enclosure** (enhanced heat dissipation)

Two panel conditions are simulated:

1. **Clean panel** (glass transmissivity = 0.95)
2. **Dusty panel** (glass transmissivity = 0.75)

## Requirements

- Python 3.9 or higher
- numpy
- pandas
- matplotlib
- scipy

## Installation

```bash
pip install -e .
