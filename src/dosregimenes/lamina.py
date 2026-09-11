"""Reflectancia difusa de una lámina de espesor d dado ℓ*(λ).  [Etapa 5]

Difusión con condiciones de borde extrapoladas: R crece con d/ℓ*. Se compara con el
Monte Carlo (montecarlo.py) en su régimen de validez.

De acá sale la PENDIENTE PREDICHA  s = -d ln R / d ln λ  por muestra, sin parámetros de
ajuste, que se contrasta con la medida (check 5.2: signo correcto, factor < 2).

d (espesor de la capa porosa): data/PROCEDENCIA.md §4 — 46/41/40/32 µm (m1–m4), a remedir
en Etapa 3.

TODO Etapa 5:
  - R_difusion(d, ell_star, mu_a=0, n_ef=1.0): fórmula de lámina.
  - s_predicha(muestra): arma ℓ*(λ) (estructura.py) y devuelve la pendiente.
"""
from __future__ import annotations

import numpy as np


def R_difusion(d_um, ell_star_um, mu_a_um=0.0, n_ef: float = 1.0):
    """Reflectancia difusa de una lámina (aprox. de difusión, borde extrapolado)."""
    raise NotImplementedError("Etapa 5")


def s_predicha(muestra: int, lam_nm=None):
    """Pendiente espectral predicha para una muestra, sin parámetros de ajuste."""
    raise NotImplementedError("Etapa 5")
