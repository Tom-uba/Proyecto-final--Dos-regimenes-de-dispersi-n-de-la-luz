"""Transporte radiativo de una lámina por Monte Carlo (tipo MCML).  [Etapa 5, opcional]

Lanza fotones, paso ~ Exp(mu_s), dispersión con Henyey–Greenstein (g), absorción mu_a,
Fresnel en las caras con n_ef; cuenta R, T, A.

check MC: |R + T + A − 1| < 1e-3  y acuerdo con lamina.R_difusion en el régimen grueso.
Correrlo headless, con dos modelos / dos niveles de esfuerzo, y comparar qué verifica cada
uno (ejercicio "modelo y esfuerzo" del curso).

TODO Etapa 5:
  - correr(mu_s, mu_a, g, n_ef, d, n_fotones, rng): devuelve (R, T, A).
"""
from __future__ import annotations

import numpy as np


def correr(mu_s_um, mu_a_um, g, n_ef, d_um, n_fotones=100_000, seed=0):
    """Devuelve (R, T, A) difusas de la lámina. Verifica R+T+A≈1."""
    raise NotImplementedError("Etapa 5")
