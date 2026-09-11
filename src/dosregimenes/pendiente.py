"""Pendiente espectral  s = -d ln R / d ln λ  y curvatura.  [Etapa 2]

Observable central del proyecto. Se mide por dos métodos redundantes y en dos sub-bandas
(check 2.1). La firma esperada:
    régimen de Mie (muestras 1–3): s pequeña, casi constante.
    transición Rayleigh (muestra 4): s grande.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.interpolate import UnivariateSpline

SUBBANDAS_NM = ((450.0, 600.0), (600.0, 750.0))


@dataclass
class Pendiente:
    muestra: int
    metodo: str
    subbanda: tuple[float, float]
    s: float                 # -d ln R / d ln λ  (media en la sub-banda)
    s_err: float             # incertidumbre (del ajuste o de la banda de dispersión)
    curvatura: float         # d² ln R / d(ln λ)²  (media en la sub-banda)


def _sel(lam, sub, valida=None):
    lo, hi = sub
    s = (lam >= lo) & (lam <= hi)
    if valida is not None:
        s &= valida
    return s


def por_regresion(lam, R, sub, sigma=None, valida=None) -> Pendiente:
    """Ajuste lineal de ln R vs ln λ en la sub-banda. s = -pendiente."""
    s = _sel(lam, sub, valida)
    x, y = np.log(lam[s]), np.log(R[s])
    w = None if sigma is None else 1.0 / np.clip(sigma[s] / R[s], 1e-6, None) ** 2
    p, cov = np.polyfit(x, y, 2, w=w, cov=True)
    a2, a1, _ = p
    lnl0 = np.log(np.sqrt(sub[0] * sub[1]))
    s_val = -(2 * a2 * lnl0 + a1)
    s_err = float(np.sqrt(cov[1, 1] + (2 * lnl0) ** 2 * cov[0, 0]))
    return Pendiente(muestra=-1, metodo="regresion", subbanda=sub,
                     s=float(s_val), s_err=s_err, curvatura=float(2 * a2))


def por_spline(lam, R, sub, valida=None, k_smooth=None) -> Pendiente:
    """Derivada de un spline suavizado de ln R(ln λ), promediada en la sub-banda."""
    ok = np.ones_like(lam, bool) if valida is None else valida.copy()
    x, y = np.log(lam[ok]), np.log(R[ok])
    o = np.argsort(x)
    x, y = x[o], y[o]
    sp = UnivariateSpline(x, y, k=3, s=(k_smooth if k_smooth is not None else len(x) * 1e-5))
    s = _sel(lam, sub, valida)
    xs = np.log(lam[s])
    d1 = sp.derivative(1)(xs)
    d2 = sp.derivative(2)(xs)
    return Pendiente(muestra=-1, metodo="spline", subbanda=sub,
                     s=float(-d1.mean()), s_err=float(d1.std()), curvatura=float(d2.mean()))


def medir(espectro, subbandas=SUBBANDAS_NM) -> list[Pendiente]:
    """Todas las combinaciones método × sub-banda para un Espectro."""
    out = []
    for sub in subbandas:
        for fn in (por_regresion, por_spline):
            kw = dict(sigma=espectro.sigma) if fn is por_regresion else {}
            p = fn(espectro.lam, espectro.R, sub, valida=espectro.mascara_valida, **kw)
            p.muestra = espectro.muestra
            out.append(p)
    return out
