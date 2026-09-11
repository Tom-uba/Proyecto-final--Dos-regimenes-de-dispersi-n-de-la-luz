"""Parámetro de tamaño  x = π D / λ  y el mapa de regímenes.  [Etapa 4]

Toma la distribución de Feret P(D) (de `imagej.py`) y la lleva al eje x sobre la banda
donde efectivamente se midió la reflectancia. Para cada muestra queda una nube P(x) — no
un valor — porque los poros son polidispersos y λ recorre un rango.

La frontera primaria es x = 1 (definición F1 de informe/teoria.md §6). Lo que decide el
resultado no es dónde se ponga exactamente la línea, sino que las nubes de las muestras
micrométricas y la de la nanométrica no se solapen.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from . import BANDA_NM

FRONTERA = 1.0          # F1, definición primaria (teoria.md §6)


def x_de(D_um, lam_nm):
    """x = π D / λ, con D en µm y λ en nm. Hace broadcasting D × λ."""
    D = np.asarray(D_um, float)[..., None] * 1e-6
    lam = np.asarray(lam_nm, float) * 1e-9
    return np.pi * D / lam


def nube_x(D_um, banda_nm: tuple[float, float] = BANDA_NM, n_lam: int = 61) -> np.ndarray:
    """Muestra de P(x): todos los pares (D, λ) con λ recorriendo la banda uniformemente."""
    lam = np.linspace(banda_nm[0], banda_nm[1], n_lam)
    return x_de(np.asarray(D_um, float), lam).ravel()


@dataclass
class BandaX:
    muestra: int
    n: int
    x_p5: float
    x_p25: float
    x_mediana: float
    x_p75: float
    x_p95: float
    frac_sobre_frontera: float   # fracción de P(x) con x > FRONTERA

    @property
    def intervalo(self) -> tuple[float, float]:
        """Intervalo central del 90 % de P(x)."""
        return (self.x_p5, self.x_p95)


def banda_x(muestra: int, D_um, banda_nm: tuple[float, float] = BANDA_NM,
            frontera: float = FRONTERA) -> BandaX:
    """Resumen de la nube P(x) de una muestra."""
    x = nube_x(D_um, banda_nm)
    p5, p25, med, p75, p95 = np.percentile(x, [5, 25, 50, 75, 95])
    return BandaX(muestra=muestra, n=len(x), x_p5=float(p5), x_p25=float(p25),
                  x_mediana=float(med), x_p75=float(p75), x_p95=float(p95),
                  frac_sobre_frontera=float(np.mean(x > frontera)))


def solape(xa: np.ndarray, xb: np.ndarray, n_grilla: int = 800) -> float:
    """Coeficiente de solape entre dos nubes P(x): ∫ min(f_a, f_b) dx, en [0, 1].

    Se calcula sobre log10(x) —que es como se grafica y como se comparan escalas— con
    densidades por KDE. 0 = distribuciones disjuntas, 1 = idénticas.
    """
    from scipy.stats import gaussian_kde

    la, lb = np.log10(xa), np.log10(xb)
    lo = min(la.min(), lb.min())
    hi = max(la.max(), lb.max())
    g = np.linspace(lo, hi, n_grilla)
    fa = gaussian_kde(la)(g)
    fb = gaussian_kde(lb)(g)
    return float(np.trapezoid(np.minimum(fa, fb), g))
