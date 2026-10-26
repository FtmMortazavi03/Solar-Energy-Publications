"""
File: config.py
Author: Fatemehsadat Mortazavi
Date: Aug 2026
Description: Configuration file for PV-PCM NSGA-II optimization.
             - Physical constants (Stefan-Boltzmann, reference temperature)
             - PV panel properties (mass, heat capacity, absorptivity, emissivity)
             - PCM thermal properties (RT42, RT44HC, RT45HC, RT47, RT50)
             - NASA POWER hourly weather data for Ahvaz, Kerman, Zahedan
             - NSGA-II parameters and optimization bounds
"""

# ==========================================
# 1. PHYSICAL CONSTANTS
# ==========================================
SIGMA = 5.67e-8          # Stefan-Boltzmann constant (W/m^2.K^4)
T_REF = 25.0             # Reference temperature for PV efficiency (°C)
EFF_REF = 0.20           # Reference electrical efficiency (20%)
BETA = 0.0045            # Temperature coefficient of efficiency (1/K)
AREA = 1.0               # Panel area per unit (m^2)

# ==========================================
# 2. PV PANEL PROPERTIES (per m^2)
# ==========================================
M_PV = 12.0              # Mass of PV panel per unit area (kg/m^2)
CP_PV = 900.0            # Specific heat capacity of PV panel (J/kg.K)
ABSORPTIVITY = 0.90      # Absorptivity of PV cells
EMISSIVITY = 0.85        # Emissivity of PV glass/backsheet

# ==========================================
# 3. GLASS TRANSMISSIVITY (clean vs dusty)
# ==========================================
TAU_CLEAN = 0.95         # Clean glass transmissivity
TAU_DUSTY = 0.75         # Dusty glass transmissivity

# ==========================================
# 4. HEAT TRANSFER COEFFICIENTS (PCM side)
# ==========================================
K_CONTACT = 200.0        # Thermal contact PV-PCM with paste (W/m^2.K)
H_CONV_PCM = 25.0        # Back convection with finned enclosure (W/m^2.K)
FIN_FACTOR = 1.5         # Effective area enhancement due to fins

# ==========================================
# 5. PCM PROPERTIES (Rubitherm datasheets)
# ==========================================
PCM_PROPERTIES = {
    'RT42':   {'T_m': 41.0, 'L': 165e3, 'rho': 880.0, 'cp': 2000.0},
    'RT44HC': {'T_m': 43.0, 'L': 250e3, 'rho': 800.0, 'cp': 2000.0},
    'RT45HC': {'T_m': 47.0, 'L': 230e3, 'rho': 900.0, 'cp': 2000.0},
    'RT47':   {'T_m': 46.0, 'L': 160e3, 'rho': 880.0, 'cp': 2000.0},
    'RT50':   {'T_m': 49.0, 'L': 160e3, 'rho': 880.0, 'cp': 2000.0},
}
PCM_NAMES = list(PCM_PROPERTIES.keys())

# ==========================================
# 6. NASA POWER HOURLY DATA (15 July 2025)
# ==========================================
# Columns: [Hour, G (W/m^2), T2M (°C), WS10M (m/s)]
NASA_DATA_RAW = {
    'Ahvaz': [
        [0, 0, 38.49, 3.38], [1, 0, 37.88, 4.24], [2, 0, 37.37, 5.44],
        [3, 0, 36.80, 5.89], [4, 0, 36.20, 5.51], [5, 38.92, 36.41, 5.57],
        [6, 154.85, 38.18, 5.56], [7, 321.27, 41.25, 5.76], [8, 519.45, 43.90, 5.47],
        [9, 679.9, 45.81, 4.57], [10, 807.97, 47.42, 3.70], [11, 660.92, 48.56, 3.07],
        [12, 812.3, 49.33, 2.74], [13, 709.97, 49.76, 2.64], [14, 609.7, 49.76, 2.77],
        [15, 434.6, 49.43, 3.07], [16, 253.6, 48.71, 3.25], [17, 112.53, 47.29, 2.30],
        [18, 17.5, 44.75, 1.77], [19, 0, 43.33, 1.37], [20, 0, 42.34, 0.81],
        [21, 0, 41.49, 0.21], [22, 0, 41.29, 1.71], [23, 0, 39.72, 3.34],
    ],
    'Kerman': [
        [0, 0, 19.83, 1.35], [1, 0, 19.49, 1.25], [2, 0, 19.20, 1.21],
        [3, 0, 18.87, 1.13], [4, 0, 18.59, 1.02], [5, 14.2, 18.53, 0.90],
        [6, 149.5, 20.66, 1.10], [7, 358.5, 23.99, 2.96], [8, 581.78, 26.31, 3.46],
        [9, 773.78, 28.21, 3.95], [10, 917.83, 29.79, 4.40], [11, 1002.7, 31.04, 4.80],
        [12, 1028.53, 31.93, 5.20], [13, 978.78, 32.37, 5.50], [14, 868.62, 32.35, 5.73],
        [15, 700.67, 31.85, 5.90], [16, 494.6, 30.90, 5.94], [17, 273.67, 29.46, 5.86],
        [18, 77.9, 27.37, 5.11], [19, 0, 23.82, 3.18], [20, 0, 22.47, 2.82],
        [21, 0, 21.72, 2.20], [22, 0, 21.38, 1.54], [23, 0, 21.07, 0.97],
    ],
    'Zahedan': [
        [0, 0, 21.05, 4.02], [1, 0, 20.51, 3.97], [2, 0, 20.00, 3.79],
        [3, 0, 19.59, 3.67], [4, 0, 19.25, 3.57], [5, 24.55, 20.28, 3.28],
        [6, 177.35, 24.54, 5.10], [7, 396.0, 27.38, 7.00], [8, 612.08, 29.39, 7.46],
        [9, 799.45, 31.08, 7.98], [10, 935.35, 32.45, 8.52], [11, 1005.92, 33.46, 8.97],
        [12, 1007.45, 34.11, 9.26], [13, 935.25, 34.34, 9.37], [14, 798.05, 34.21, 9.39],
        [15, 609.38, 33.65, 9.33], [16, 397.08, 32.64, 9.08], [17, 208.12, 31.27, 8.49],
        [18, 37.38, 29.03, 6.17], [19, 0, 26.20, 4.07], [20, 0, 24.86, 3.70],
        [21, 0, 23.76, 3.53], [22, 0, 22.86, 3.51], [23, 0, 22.12, 3.60],
    ],
}

# ==========================================
# 7. NSGA-II PARAMETERS & BOUNDS
# ==========================================
POP_SIZE = 100
N_GENERATIONS = 50
SBX_PROB = 0.9
SBX_ETA = 15
PM_PROB = 0.1
PM_ETA = 20
SEED = 42

MASS_MIN = 5.0            # Minimum PCM mass (kg/m^2)
MASS_MAX = 20.0           # Maximum PCM mass (kg/m^2)
T_MAX_LIMIT = 85.0        # Maximum allowed panel temperature (°C)

CITIES = ['Ahvaz', 'Kerman', 'Zahedan']
SCENARIOS = [('Clean', TAU_CLEAN), ('Dusty', TAU_DUSTY)]