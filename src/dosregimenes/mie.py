"""Dispersión de Mie: Q_sca(x, m), g(x, m), y promedio sobre P(D).  [Etapa 5]

Marco teórico: notas/fichas.md (Bohren & Huffman; Borgmann §2.2.1).
El scatterer es aire en el sólido -> m = n_aire / n_sol(λ) < 1 (usar dosregimenes.nref).

check 5.1 (límites):
    x -> 0   : Q_sca ∝ x^4               (Rayleigh)
    x -> inf : Q_sca -> 2                (paradoja de extinción)

TODO Etapa 5:
  - qsca_g(x, m): envolver miepython (mie_S1_S2 / mie_cross_sections).
  - promediar_PD(P_D, lam, m): <Q_sca> y <g> pesados por P(D) y por el área geométrica.
  - polidispersión: discutir sesgo de la aproximación esférica (poros no esféricos).
"""
from __future__ import annotations

import numpy as np


def qsca_g(x, m):
    """Eficiencia de dispersión y anisotropía para parámetro de tamaño x, contraste m."""
    raise NotImplementedError("Etapa 5 — envolver miepython y verificar check 5.1")


def promediar_PD(P_D_um, pesos, lam_nm, m):
    """<Q_sca>(λ) y <g>(λ) sobre la distribución de tamaño P(D)."""
    raise NotImplementedError("Etapa 5")
