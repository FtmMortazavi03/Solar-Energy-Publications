# PV-PCM-NSGA2-Optimization

Multi-objective optimization of PV-PCM systems using NSGA-II for hot and dusty climates in Iran.

## Author

Fatemehsadat Mortazavi

## Description

This project presents a multi-objective optimization framework, based on the NSGA-II algorithm, for designing a photovoltaic-phase change material (PV-PCM) thermal management system. Three cities in Iran are studied as representatives of hot climates:

- **Ahvaz** (hot and semi-humid, ~50 °C)
- **Kerman** (hot and dry, high elevation)
- **Zahedan** (hot and dry, dusty)

Five commercial PCMs from Rubitherm are compared:

- RT42
- RT44HC
- RT45HC
- RT47
- RT50

Two design variables are optimized simultaneously:

1. **PCM type** (discrete, 5 options)
2. **PCM mass** (continuous, 5–20 kg/m²)

Two conflicting objective functions are considered:

- Minimize maximum daily panel temperature
- Maximize daily electrical energy output

A constraint ensures the panel temperature does not exceed 85 °C. Two dust scenarios (clean: τ = 0.95, dusty: τ = 0.75) are evaluated for each city. Unlike previous studies, the initial PCM temperature is set to the **minimum nighttime temperature** (00:00–05:00), giving a more realistic estimate of PCM performance.

## Requirements

- Python 3.9 or higher
- numpy
- pandas
- matplotlib
- scipy
- pymoo

## Installation

```bash
pip install -e .
```

## Data

Hourly weather data (ambient temperature, solar irradiance, wind speed) for July 15, 2025 were obtained from the NASA POWER database. These data are embedded directly in `src/pv_pcm_nsga2/config.py` under `NASA_DATA_RAW` for full reproducibility.

## Usage

```bash
python -m pv_pcm_nsga2.main
```

Outputs:

- Figures saved to `outputs/figures/`
- Summary tables saved to `outputs/tables/`

## Results

| City    | Scenario | Optimal PCM | Mass (kg/m²) | T_max (°C) | E_daily (kWh) |
|---------|----------|-------------|--------------|------------|----------------|
| Ahvaz   | Clean    | RT45HC      | 20.0         | 59.1       | 0.920          |
| Ahvaz   | Dusty    | RT45HC      | 20.0         | 56.8       | 0.732          |
| Kerman  | Clean    | RT50        | 7.6          | 62.3       | 1.322          |
| Kerman  | Dusty    | RT50        | 7.6          | 62.3       | 1.053          |
| Zahedan | Clean    | RT50        | 7.8          | 64.8       | 1.273          |
| Zahedan | Dusty    | RT50        | 7.8          | 64.9       | 1.012          |

## License

This project is for academic use.