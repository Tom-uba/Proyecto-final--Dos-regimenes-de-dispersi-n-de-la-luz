"""Reflectancia difusa de una lámina dado ℓ*(λ).  [Etapa 5]

Marco: informe/teoria.md §3.2. Cierra la cadena

    P(D) → σ_tr(λ) [mie.py] → ℓ*(λ) [+ estructura.py] → R(λ) → s = −d ln R/d ln λ

y de acá sale la PENDIENTE PREDICHA, sin ningún parámetro ajustado a los espectros.

## La fórmula, y por qué ésta

Para una lámina NO absorbente de espesor L, difusión con bordes extrapolados da

    T = (z₀ + z_e) / (L + 2 z_e),      R = 1 − T
    z₀ ≈ ℓ*        (profundidad de la primera dispersión)
    z_e = (2/3) ℓ* (1 + R_ef)/(1 − R_ef)     (longitud de extrapolación)

Es el resultado estándar de óptica mesoscópica. `R_ef` es la reflectancia interna efectiva
por el salto de índice entre el medio poroso y el aire, con la aproximación usual

    R_ef ≈ −1.440/n² + 0.710/n + 0.668 + 0.0636 n

No absorbente es una hipótesis, no un hecho: se contrasta contra T(λ) medida en la Etapa 6.

## Validez

La difusión vale para L ≫ ℓ*. Cuando eso no se cumple la fórmula deja de ser confiable y
manda el Monte Carlo (`montecarlo.py`). `espesor_optico()` devuelve L/ℓ* para poder decir
en qué régimen está cada muestra en vez de suponerlo.
"""
from __future__ import annotations

import numpy as np


def n_efectivo(n_sol_lam, phi: float, regla: str = "eps") -> np.ndarray:
    """Índice efectivo del medio poroso (fracción φ de aire en el sólido).

    regla="eps"       promedio volumétrico de ε  (el que se usa por defecto)
    regla="bruggeman" cierre simétrico de Bruggeman
    Las dos difieren <1 % en este rango de φ; se ofrece la segunda como sensibilidad.
    """
    ns = np.asarray(n_sol_lam, float)
    if regla == "eps":
        return np.sqrt(phi * 1.0 + (1 - phi) * ns**2)
    if regla == "bruggeman":
        # φ(1−ε)/(1+2ε) + (1−φ)(ns²−ε)/(ns²+2ε) = 0, resuelta para ε
        e1, e2 = 1.0, ns**2
        b = (3 * phi - 1) * e1 + (3 * (1 - phi) - 1) * e2
        eps = (b + np.sqrt(b**2 + 8 * e1 * e2)) / 4.0
        return np.sqrt(eps)
    raise ValueError(regla)


def R_ef_interna(n) -> np.ndarray:
    """Reflectancia interna efectiva para el borde medio-poroso / aire."""
    n = np.asarray(n, float)
    return -1.440 / n**2 + 0.710 / n + 0.668 + 0.0636 * n


def R_difusion(d_um, ell_um, n_ef) -> np.ndarray:
    """Reflectancia difusa de una lámina no absorbente de espesor d_um."""
    ell = np.asarray(ell_um, float)
    Ref = R_ef_interna(n_ef)
    z_e = (2.0 / 3.0) * ell * (1 + Ref) / (1 - Ref)
    T = (ell + z_e) / (float(d_um) + 2 * z_e)
    return 1.0 - np.clip(T, 0.0, 1.0)


def espesor_optico(d_um, ell_um) -> np.ndarray:
    """L/ℓ*. Por debajo de ~5 la aproximación de difusión empieza a flaquear."""
    return float(d_um) / np.asarray(ell_um, float)


def pendiente(lam_nm, R) -> float:
    """s = −d ln R / d ln λ por regresión lineal en log–log."""
    lam = np.asarray(lam_nm, float)
    return float(-np.polyfit(np.log(lam), np.log(np.asarray(R, float)), 1)[0])
