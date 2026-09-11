"""Factor de estructura S(q) y camino libre de transporte ℓ*(λ).  [Etapa 5]

Los poros no son diluidos (φ ~ 0.3–0.7): las correlaciones de corto alcance suprimen la
dispersión hacia adelante y modifican ℓ*. Se calcula ℓ*(λ) CON y SIN la corrección para
acotar cuánto pesa.

    ℓ*  = 1 / [ ρ · σ_sca · (1 − g) ]          (independiente / diluido)
    ℓ*_S se corrige con S(q) integrado (Percus–Yevick, esferas duras a fracción φ).

Marco: notas/fichas.md (Wilts 2018; Syurik 2017). Referencia de φ: Etapa 3 (feret.py) /
espesores (data/PROCEDENCIA.md §4).

TODO Etapa 5:
  - S_py(q, phi): Percus–Yevick analítico.
  - ell_star(lam, P_D, phi, m, con_estructura=bool).
"""
from __future__ import annotations

import numpy as np


def S_py(q, phi):
    """Factor de estructura de Percus–Yevick para esferas duras a fracción φ."""
    raise NotImplementedError("Etapa 5")


def ell_star(lam_nm, P_D_um, pesos, phi, m, con_estructura: bool = True):
    """Camino libre medio de transporte ℓ*(λ) en µm."""
    raise NotImplementedError("Etapa 5")
