"""Factor de estructura S(q) y dispersión dependiente.  [Etapa 5]

Marco: informe/teoria.md §4. Las ecuaciones de Mie suponen scatterers DILUIDOS. Acá
φ ≈ 0.20 (muestras 1–3) y 0.33 (muestra 4): los poros están correlacionados y sumar sus
secciones eficaces sin más sobreestima la dispersión.

## Percus–Yevick monodisperso

Cierre de Percus–Yevick para esferas duras, cuya función de correlación directa en el
espacio real es exacta y corta:

    c(r) = −λ₁ − 6η λ₂ (r/σ) − (η λ₁/2)(r/σ)³      r < σ
    c(r) = 0                                        r > σ
    λ₁ = (1+2η)²/(1−η)⁴        λ₂ = −(1+η/2)²/(1−η)⁴

de ahí  C(q) = 4π ∫₀^σ c(r) sinc(qr) r² dr  y  S(q) = 1/(1 − ρ C(q)).

Se integra numéricamente (la forma cerrada de Ashcroft–Lekner es fácil de transcribir mal)
y se valida contra sus límites exactos en `check_5_4_estructura.py`:
    S(0) = (1−η)⁴ / (1+2η)²        S(q) → 1 cuando q → ∞

## Polidispersión: aproximación de desacople (Kotlarchyk & Chen 1983)

Agregado el 2026-09-13 tras la falla del check 5.3. PY monodisperso supone poros todos
iguales. Con tamaños distintos la interferencia entre vecinos se cancela peor, porque poros
de distinto tamaño dispersan con distinta amplitud. La aproximación de desacople separa la
parte coherente:

    S_ef(q) = 1 + β(q) [S(q) − 1]
    β(q)    = |⟨F(q)⟩|² / ⟨|F(q)|²⟩  ≤ 1

con F(q, D) ∝ D³ · 3(sin u − u cos u)/u³, u = qD/2 (amplitud de una esfera homogénea; el
contraste es común a todos los poros y se cancela en β). Los promedios son sobre la P(D)
medida. Sin parámetros libres. β = 1 para poros iguales (recupera PY monodisperso) y
β(0) = ⟨D³⟩²/⟨D⁶⟩. Validado en `check_5_6_desacople.py`. La escala de correlación de S(q)
sigue siendo σ = ⟨D⟩, igual que antes: el único cambio respecto del monodisperso es β.

Supuestos de la aproximación, a declarar: el tamaño de un poro no está correlacionado con su
posición; los poros son esferas. Ninguno es exacto en una espuma, menos en la red de m4.

## Efecto sobre el transporte

La corrección pesa la dispersión angular por S(q) (o S_ef), con q = 2k sin(θ/2). ℓ* depende
de la sección de transporte completa ∫ p(θ) S(q) (1−cos θ) dΩ.
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


def _forma_esfera(u):
    """3(sin u − u cos u)/u³, con su serie 1 − u²/10 cerca de 0."""
    u = np.asarray(u, float)
    chico = np.abs(u) < 1e-3
    uu = np.where(chico, 1.0, u)
    f = 3.0 * (np.sin(uu) - uu * np.cos(uu)) / uu ** 3
    return np.where(chico, 1.0 - u ** 2 / 10.0, f)


def _histograma_D(D_um, n_bines: int = 160):
    """P(D) discretizada: centros y pesos. Con poros todos iguales devuelve un solo bin."""
    D = np.asarray(D_um, float).ravel()
    lo, hi = float(D.min()), float(np.percentile(D, 99.9))
    if hi - lo < 1e-9 * max(hi, 1e-12):
        return np.array([float(np.mean(D))]), np.array([1.0])
    bordes = np.linspace(lo, hi, n_bines + 1)
    w, _ = np.histogram(D, bins=bordes)
    c = 0.5 * (bordes[:-1] + bordes[1:])
    ok = w > 0
    return c[ok], w[ok] / w[ok].sum()


def beta_desacople(D_um, q_inv_um):
    """β(q) = |⟨F⟩|²/⟨F²⟩ sobre P(D). `q_inv_um` en µm⁻¹."""
    Dc, w = _histograma_D(D_um)
    q = np.atleast_1d(np.asarray(q_inv_um, float))
    F = (Dc ** 3)[None, :] * _forma_esfera(q[:, None] * Dc[None, :] / 2.0)
    num = (F @ w) ** 2
    den = (F ** 2) @ w
    return num / np.where(den > 0, den, 1.0)


def S_desacople(q_inv_um, D_um, eta: float):
    """S_ef(q) = 1 + β(q)[S_PY(q⟨D⟩) − 1]. `q_inv_um` en µm⁻¹."""
    q = np.atleast_1d(np.asarray(q_inv_um, float))
    sigma = float(np.mean(D_um))
    return 1.0 + beta_desacople(D_um, q) * (S_py(q * sigma, eta) - 1.0)


def factor_transporte(D_um, lam_nm, n_ef, eta: float, g_ef, n_theta: int = 400,
                      polidisperso: bool = False):
    """Factor por el que la dispersión dependiente corrige la sección de TRANSPORTE.

    ℓ* = 1/(ρ σ_tr) con  σ_tr = ∫ (dσ/dΩ)(1 − cos θ) dΩ.  Con correlaciones:

        σ_tr,S / σ_tr,libre  =  ∫ p(θ) S(q) (1−cos θ) dΩ  /  ∫ p(θ) (1−cos θ) dΩ

    con q = 2k sin(θ/2), k = 2π n_ef/λ₀, y p(θ) Henyey–Greenstein con la g efectiva de Mie.
    `polidisperso=True` usa S_ef del desacople en lugar de PY monodisperso.

    Corrección (2026-09-13): una versión anterior devolvía sólo el cociente de (1−g)
    NORMALIZADO, que omite que S(q)<1 también reduce la dispersión total.

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
        S = S_desacople(q, D_um, eta) if polidisperso else S_py(q * sigma, eta)
        p = (1 - gi ** 2) / (4 * np.pi * (1 + gi ** 2 - 2 * gi * mu) ** 1.5)
        w = 2 * np.pi * np.sin(th)
        tr_libre = np.trapezoid(p * (1 - mu) * w, th)
        tr_S = np.trapezoid(p * S * (1 - mu) * w, th)
        out[i] = tr_S / tr_libre
    return out
