"""Factor de estructura S(q) y dispersión dependiente.  [Etapa 5]

Marco: informe/teoria.md §4. Las ecuaciones de Mie suponen scatterers DILUIDOS. Acá
φ ≈ 0.20 (muestras 1–3) y 0.33 (muestra 4): los poros están correlacionados y sumar sus
secciones eficaces sin más sobreestima la dispersión.

Se usa el cierre de **Percus–Yevick para esferas duras**, cuya función de correlación
directa en el espacio real es exacta y corta:

    c(r) = −λ₁ − 6η λ₂ (r/σ) − (η λ₁/2)(r/σ)³      r < σ
    c(r) = 0                                        r > σ
    λ₁ = (1+2η)²/(1−η)⁴        λ₂ = −(1+η/2)²/(1−η)⁴

y de ahí  C(q) = 4π ∫₀^σ c(r) sinc(qr) r² dr  y  S(q) = 1/(1 − ρ C(q)).

**Por qué numérico y no la forma cerrada de Ashcroft–Lekner:** la transformada analítica
es larga y fácil de transcribir mal. La integral se hace numéricamente y se valida contra
los dos límites que sí se conocen exactamente (`check_5_4_estructura.py`):

    S(0) = (1−η)⁴ / (1+2η)²        (compresibilidad, exacta en PY)
    S(q) → 1  cuando q → ∞

Efecto sobre el transporte: la corrección pesa la dispersión angular por S(q), con
q = 2k sin(θ/2). Suprime el ángulo pequeño (donde S<1), que es justo el que menos aporta
al transporte, y por eso el efecto neto sobre ℓ* es moderado — pero se calcula, no se
supone. Todo el proyecto reporta ℓ* CON y SIN esta corrección.
"""
from __future__ import annotations

import numpy as np


def S_py(q_sigma, eta: float, n_r: int = 800):
    """Factor de estructura de Percus–Yevick. `q_sigma` = q·σ, adimensional."""
    k = np.atleast_1d(np.asarray(q_sigma, float))
    lam1 = (1 + 2 * eta) ** 2 / (1 - eta) ** 4
    lam2 = -((1 + eta / 2) ** 2) / (1 - eta) ** 4

    s = np.linspace(1e-9, 1.0, n_r)            # r/σ
    c = -lam1 - 6 * eta * lam2 * s - (eta * lam1 / 2) * s ** 3

    # C(q)/σ³ = 4π ∫ c(s) sinc(k s) s² ds     con sinc(u) = sin(u)/u
    ks = k[:, None] * s[None, :]
    sinc = np.where(ks < 1e-8, 1.0 - ks ** 2 / 6.0, np.sin(ks) / np.where(ks == 0, 1, ks))
    Cq = 4 * np.pi * np.trapezoid(c[None, :] * sinc * s[None, :] ** 2, s, axis=1)

    rho_sigma3 = 6 * eta / np.pi           # ρσ³
    return 1.0 / (1.0 - rho_sigma3 * Cq)


def S_py_cero(eta: float) -> float:
    """Límite exacto S(q→0) del cierre de Percus–Yevick."""
    return (1 - eta) ** 4 / (1 + 2 * eta) ** 2


def factor_transporte(D_um, lam_nm, n_ef, eta: float, g_ef, n_theta: int = 400):
    """Factor por el que la dispersión dependiente corrige la sección de TRANSPORTE.

    ℓ* = 1/(ρ σ_tr) con  σ_tr = ∫ (dσ/dΩ)(1 − cos θ) dΩ.  Con correlaciones:

        σ_tr,S / σ_tr,libre  =  ∫ p(θ) S(q) (1−cos θ) dΩ  /  ∫ p(θ) (1−cos θ) dΩ

    con q = 2k sin(θ/2), k = 2π n_ef/λ₀, y p(θ) Henyey–Greenstein con la g efectiva de Mie.

    Corrección (2026-09-13): una versión anterior devolvía sólo el cociente de (1−g)
    NORMALIZADO, [(1−⟨μ⟩_S)/(1−⟨μ⟩_libre)], que omite que S(q)<1 también reduce la
    dispersión total. Eso no es el factor de ℓ*. Ahora se integra la sección de transporte
    completa.

    Devuelve el cociente por λ; ℓ*_corregido = ℓ*_libre / factor.
    """
    lam = np.atleast_1d(np.asarray(lam_nm, float))
    g = np.broadcast_to(np.atleast_1d(np.asarray(g_ef, float)), lam.shape)
    sigma = float(np.mean(D_um))                       # escala de correlación ≈ ⟨D⟩
    th = np.linspace(1e-6, np.pi, n_theta)
    mu = np.cos(th)

    out = np.empty_like(lam)
    for i, (l, gi) in enumerate(zip(lam, g)):
        k = 2 * np.pi * float(np.atleast_1d(n_ef)[min(i, np.size(n_ef) - 1)]) / (l * 1e-3)  # 1/µm
        q = 2 * k * np.sin(th / 2)
        S = S_py(q * sigma, eta)
        # Henyey-Greenstein normalizada
        p = (1 - gi ** 2) / (4 * np.pi * (1 + gi ** 2 - 2 * gi * mu) ** 1.5)
        w = 2 * np.pi * np.sin(th)
        tr_libre = np.trapezoid(p * (1 - mu) * w, th)
        tr_S = np.trapezoid(p * S * (1 - mu) * w, th)
        out[i] = tr_S / tr_libre
    return out
