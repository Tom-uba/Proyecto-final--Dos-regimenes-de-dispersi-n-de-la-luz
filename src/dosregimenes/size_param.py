"""Parámetro de tamaño  x = π D / λ  y distribución P(x, λ) por muestra.  [Etapa 4]

Toma la distribución de Feret P(D) (de feret.py) y la lleva al eje x sobre la banda
visible. Salida: para cada muestra, la banda de x que ocupa y la fracción que cae de cada
lado de la frontera candidata (check 4.1: 1–3 se solapan entre sí, 4 disjunta).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def x_de(D_um, lam_nm):
    """x = π D / λ.  Acepta escalares o arrays (broadcasting D × λ)."""
    D = np.asarray(D_um, float)[..., None] * 1e-6
    lam = np.asarray(lam_nm, float) * 1e-9
    return np.pi * D / lam


@dataclass
class BandaX:
    muestra: int
    x_med: float             # x en <D> a 550 nm
    x_q1: float              # cuartiles de x sobre P(D) × banda visible
    x_q3: float
    x_min: float
    x_max: float
    frac_bajo_frontera: float  # fracción de la masa P(x) con x < x_frontera


def banda_x(muestra: int, D_muestras_um, pesos=None,
            lam_nm=(400.0, 700.0), x_frontera: float = 1.0) -> BandaX:
    """Resume la nube P(x) de una muestra sobre la banda [lam_min, lam_max]."""
    D = np.asarray(D_muestras_um, float)
    w = np.ones_like(D) if pesos is None else np.asarray(pesos, float)
    w = w / w.sum()
    lam = np.linspace(lam_nm[0], lam_nm[1], 61)
    X = x_de(D, lam)                       # (nD, nlam)
    W = np.broadcast_to(w[:, None], X.shape).ravel()
    xf = X.ravel()
    orden = np.argsort(xf)
    xf, W = xf[orden], W[orden]
    cdf = np.cumsum(W) / W.sum()
    q1, med, q3 = np.interp([0.25, 0.5, 0.75], cdf, xf)
    frac = float(np.interp(x_frontera, xf, cdf))
    return BandaX(muestra=muestra, x_med=float(np.interp(np.median(D), np.sort(D),
                  x_de(np.sort(D), 550.0).ravel())),
                  x_q1=float(q1), x_q3=float(q3),
                  x_min=float(xf[0]), x_max=float(xf[-1]),
                  frac_bajo_frontera=frac)
