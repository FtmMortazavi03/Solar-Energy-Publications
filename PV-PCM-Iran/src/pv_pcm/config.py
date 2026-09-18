"""
File: config.py
Author: Fatemehsadat Mortazavi
Date: Jun 2026
Description: Configuration file for PV-PCM-Iran simulation.
             - Physical constants (Stefan-Boltzmann, reference temperature)
             - PV panel properties (mass, heat capacity, absorptivity, emissivity)
             - PCM layer properties (thickness, heat transfer coefficients)
             - City data (Yazd, Ahvaz, Bandar Abbas)
             - PCM properties (RT42, RT44HC, RT45HC, RT47, RT50 from Rubitherm)
"""

# ==========================================
# 1. PHYSICAL CONSTANTS
# ==========================================
SIGMA = 5.67e-8       # Stefan-Boltzmann constant (W/m^2.K^4)
T_REF = 25.0          # Reference temperature for PV efficiency (°C)
EFF_REF = 0.20        # Reference electrical efficiency (20%)
BETA = 0.0045         # Temperature coefficient of efficiency (1/K)

# ==========================================
# 2. PV PANEL PROPERTIES (per m^2)
# ==========================================
M_PV = 12.0           # Mass of PV panel per unit area (kg/m^2)
CP_PV = 900.0         # Specific heat capacity of PV panel (J/kg.K)
ABSORPTIVITY = 0.90   # Absorptivity of PV cells
EMISSIVITY = 0.85     # Emissivity of PV glass/backsheet

# ==========================================
# 3. PCM LAYER PROPERTIES
# ==========================================
THICKNESS_PCM = 0.03  # PCM layer thickness (m)

# Heat transfer coefficients (W/m^2.K)
H_CONV_FRONT = 15.0   # Front surface (natural convection)
H_CONV_BACK = 5.0     # Back surface without PCM
H_CONV_PCM = 25.0     # Back surface with finned aluminum enclosure

# Thermal contact between PV and PCM
K_CONTACT = 200.0     # With thermal paste (W/m^2.K)

# Finned enclosure
ENCLOSURE_AREA_FACTOR = 1.5  # Effective area enhancement due to fins

# ==========================================
# 4. CITIES (July averages from NASA POWER)
# ==========================================
CITIES = {
    'Yazd': {
        'T_amb_avg': 37.7,
        'T_amp': 7.0,
        'G_daily_wh': 7770
    },
    'Ahvaz': {
        'T_amb_avg': 49.2,
        'T_amp': 8.0,
        'G_daily_wh': 7630
    },
    'Bandar Abbas': {
        'T_amb_avg': 38.3,
        'T_amp': 5.0,
        'G_daily_wh': 6850
    }
}

# ==========================================
# 5. PCM PROPERTIES (Rubitherm datasheets)
# ==========================================
PCM_PROPERTIES = {
    'RT42': {
        'T_m': 41.0,      # Melting temperature (°C)
        'L': 165e3,       # Latent heat (J/kg)
        'rho': 880.0,     # Density (kg/m^3)
        'cp': 2000.0,     # Specific heat (J/kg.K)
        'k': 0.2          # Thermal conductivity (W/m.K)
    },
    'RT44HC': {
        'T_m': 43.0,
        'L': 250e3,
        'rho': 800.0,
        'cp': 2000.0,
        'k': 0.2
    },
    'RT45HC': {
        'T_m': 47.0,
        'L': 230e3,
        'rho': 900.0,
        'cp': 2000.0,
        'k': 0.2
    },
    'RT47': {
        'T_m': 46.0,
        'L': 160e3,
        'rho': 880.0,
        'cp': 2000.0,
        'k': 0.2
    },
    'RT50': {
        'T_m': 49.0,
        'L': 160e3,
        'rho': 880.0,
        'cp': 2000.0,
        'k': 0.2
    }
}

# ==========================================
# 6. SIMULATION PARAMETERS
# ==========================================
TIME_STEPS = 1440     # Number of timesteps (1-minute intervals for 24 hours)
DUSTY_TAU = 0.75      # Glass transmissivity for dusty panel
CLEAN_TAU = 0.95      # Glass transmissivity for clean panel