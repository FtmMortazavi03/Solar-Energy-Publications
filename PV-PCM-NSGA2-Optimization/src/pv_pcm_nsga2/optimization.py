"""
File: optimization.py
Author: Fatemehsadat Mortazavi
Date: Aug 2026
Description: NSGA-II multi-objective optimization for PV-PCM design.
             - Decision variables: PCM type (discrete), PCM mass (continuous)
             - Objectives: minimize T_max, maximize E_daily
             - Constraint: T_max <= 85 °C
"""

import numpy as np
from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.termination import get_termination
from pymoo.optimize import minimize

from . import config as cfg
from .simulation import simulate_daily


class PVPCMOptimizer(Problem):
    """Two-objective NSGA-II problem for PV-PCM design."""

    def __init__(self, weather_df, tau, T_initial):
        self.weather_df = weather_df
        self.tau = tau
        self.T_initial = T_initial
        super().__init__(
            n_var=2,
            n_obj=2,
            n_constr=1,
            xl=np.array([0, cfg.MASS_MIN]),
            xu=np.array([len(cfg.PCM_NAMES) - 1, cfg.MASS_MAX]),
        )

    def _evaluate(self, X, out, *args, **kwargs):
        n_pop = X.shape[0]
        f1 = np.zeros(n_pop)
        f2 = np.zeros(n_pop)
        g1 = np.zeros(n_pop)

        for i in range(n_pop):
            pcm_idx = int(round(X[i, 0]))
            mass = X[i, 1]
            res = simulate_daily(pcm_idx, mass, self.weather_df, self.tau, self.T_initial)
            f1[i] = res['T_max']
            f2[i] = -res['E_daily']
            g1[i] = res['T_max'] - cfg.T_MAX_LIMIT

        out['F'] = np.column_stack([f1, f2])
        out['G'] = g1.reshape(-1, 1)


def run_nsga2(weather_df, tau, T_initial):
    """
    Run NSGA-II for a single scenario.

    Parameters
    ----------
    weather_df : pd.DataFrame
        Hourly weather data.
    tau : float
        Glass transmissivity.
    T_initial : float
        Initial temperature (°C).

    Returns
    -------
    pymoo.core.result.Result
        Optimization result containing Pareto front and design variables.
    """
    problem = PVPCMOptimizer(weather_df, tau, T_initial)
    algorithm = NSGA2(
        pop_size=cfg.POP_SIZE,
        sampling=FloatRandomSampling(),
        crossover=SBX(prob=cfg.SBX_PROB, eta=cfg.SBX_ETA),
        mutation=PM(prob=cfg.PM_PROB, eta=cfg.PM_ETA),
        eliminate_duplicates=True,
    )
    termination = get_termination('n_gen', cfg.N_GENERATIONS)
    return minimize(problem, algorithm, termination, seed=cfg.SEED, verbose=False)


def extract_best_design(res):
    """
    Select the Pareto-optimal point with maximum daily energy.

    Parameters
    ----------
    res : pymoo.core.result.Result

    Returns
    -------
    dict
        Keys: PCM, Mass, T_max, E_daily.
    """
    idx = int(np.argmin(res.F[:, 1]))
    pcm_idx = int(round(res.X[idx, 0]))
    return {
        'PCM': cfg.PCM_NAMES[pcm_idx],
        'Mass': float(res.X[idx, 1]),
        'T_max': float(res.F[idx, 0]),
        'E_daily': float(-res.F[idx, 1]),
    }