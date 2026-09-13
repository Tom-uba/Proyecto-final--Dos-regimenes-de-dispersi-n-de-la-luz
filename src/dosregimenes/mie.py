"""Dispersión de Mie: Q_sca, g, y sus promedios sobre P(D).  [Etapa 5]

Marco teórico: informe/teoria.md §2. El scatterer es un poro de AIRE dentro del sólido,
así que el índice relativo es m = n_aire / n_sol ≈ 0.68 < 1.

## Las dos convenciones de "parámetro de tamaño" — leer antes de tocar nada

Este proyecto define, desde `teoria.md` §1 y en toda la Etapa 4:

    x  =  π D / λ₀          (λ₀ = longitud de onda EN VACÍO)

La teoría de Mie, en cambio, usa la longitud de onda EN EL MEDIO que rodea al scatterer:

    x_Mie  =  π D n_sol / λ₀  =  n_sol · x       (≈ 1.47 · x)

No son lo mismo y confundirlas mete un factor 1.47. `miepython` documenta explícitamente
que su `x` es el del medio. Acá:

  - `x` (a secas) siempre significa el de vacío, el del eje de la Etapa 4;
  - toda función que hable con miepython convierte internamente y lo dice en su firma.

Que la frontera "x = 1" dependa de la convención NO afecta la conclusión del proyecto: los
dos grupos escalan por el mismo factor, así que el solape (0.000) y el hueco (×5.1) no
cambian. Lo que cambia es dónde cae la línea, y por eso F2/F3 —que se calculan con Mie y
no dependen de ninguna convención— son el desempate. Ver `teoria.md` §6.

## Índice de la matriz

Por defecto la matriz es acetato de celulosa, n_sol(λ) de `nref.py`. El argumento
`n_matriz` (un número) reemplaza esa curva por un índice constante; se agregó para el ancla
externa del check 5.3, que usa la morfología publicada de películas de PMMA (n = 1.49).
Con `n_matriz=None` todo da exactamente lo mismo que antes.

## Verificación

`checks/check_5_1_mie.py` comprueba los dos límites analíticos de `teoria.md`:
    x → 0    Q_sca = (8/3) x⁴ |(m²−1)/(m²+2)|²     [ec. (3)]
    x → ∞    Q_sca → 2                              [ec. (5)]
"""
from __future__ import annotations

import numpy as np

from .nref import n_sol

# Los cálculos se hacen sobre un histograma de P(D) en vez de poro por poro: con ~9000
# poros y ~60 longitudes de onda serían medio millón de evaluaciones de la serie de Mie.
# Con 160 bines el error relativo en los promedios es <0.1 % y el costo baja 60×.
N_BINES_D = 160


def _indice(lam_nm, bias: float = 0.0, n_matriz: float | None = None) -> np.ndarray:
    """Índice de la matriz en cada λ: curva de nref.py, o constante si se da n_matriz."""
    lam = np.atleast_1d(np.asarray(lam_nm, float))
    if n_matriz is None:
        return np.atleast_1d(n_sol(lam, bias=bias))
    return np.full(lam.shape, float(n_matriz))


def qsca_g_mie(x_mie, m_rel):
    """Q_sca y g crudos de la serie de Mie. `x_mie` ya debe estar en el medio."""
    import miepython as mp

    x_mie = np.atleast_1d(np.asarray(x_mie, float))
    m_rel = np.broadcast_to(np.asarray(m_rel, float), x_mie.shape)
    _, qsca, _, g = mp.efficiencies_mx(m_rel, x_mie)
    return np.asarray(qsca, float), np.asarray(g, float)


def x_mie_de(D_um, lam_nm, bias: float = 0.0, n_matriz: float | None = None):
    """x_Mie = π D n_matriz(λ) / λ₀, a partir de cantidades físicas."""
    D = np.asarray(D_um, float)[..., None] * 1e-6
    lam = np.atleast_1d(np.asarray(lam_nm, float)) * 1e-9
    return np.pi * D * _indice(lam_nm, bias, n_matriz) / lam


def qsca_g_de(D_um, lam_nm, bias: float = 0.0, n_matriz: float | None = None):
    """Q_sca(D, λ) y g(D, λ) para poros de aire en la matriz. Devuelve arrays (nD, nλ)."""
    xm = x_mie_de(D_um, lam_nm, bias=bias, n_matriz=n_matriz)
    m = np.broadcast_to(1.0 / _indice(lam_nm, bias, n_matriz), xm.shape)
    q, g = qsca_g_mie(xm.ravel(), m.ravel())
    return q.reshape(xm.shape), g.reshape(xm.shape)


def _histograma(D_um, n_bines: int = N_BINES_D):
    """P(D) discretizada: centros de bin y pesos normalizados."""
    D = np.asarray(D_um, float)
    bordes = np.linspace(D.min(), np.percentile(D, 99.9), n_bines + 1)
    w, _ = np.histogram(D, bins=bordes)
    centros = 0.5 * (bordes[:-1] + bordes[1:])
    ok = w > 0
    w = w[ok].astype(float)
    return centros[ok], w / w.sum()


def promedios_PD(D_um, lam_nm, bias: float = 0.0, n_bines: int = N_BINES_D,
                 n_matriz: float | None = None):
    """Promedios sobre P(D) que hacen falta para ℓ*.

    Devuelve un dict con, para cada λ:
        sigma_sca   ⟨Q_sca · πD²/4⟩        sección eficaz media por poro [µm²]
        sigma_tr    ⟨Q_sca (1−g) · πD²/4⟩  sección de transporte media   [µm²]
        g_ef        ⟨Q_sca g D²⟩ / ⟨Q_sca D²⟩   anisotropía efectiva
        qsca_ef     ⟨Q_sca D²⟩ / ⟨D²⟩       eficiencia media pesada por área
    y, independientes de λ:
        D3          ⟨D³⟩ [µm³]   (fija la densidad numérica a porosidad dada)
    """
    Dc, w = _histograma(D_um, n_bines)
    q, g = qsca_g_de(Dc, lam_nm, bias=bias, n_matriz=n_matriz)   # (nD, nλ)
    area = np.pi * Dc**2 / 4.0                                    # µm²
    wa = (w * 1.0)[:, None]

    sigma_sca = np.sum(wa * q * area[:, None], axis=0)
    sigma_tr = np.sum(wa * q * (1.0 - g) * area[:, None], axis=0)
    qd2 = np.sum(wa * q * (Dc**2)[:, None], axis=0)
    g_ef = np.sum(wa * q * g * (Dc**2)[:, None], axis=0) / qd2
    qsca_ef = qd2 / np.sum(w * Dc**2)

    return dict(lam_nm=np.atleast_1d(np.asarray(lam_nm, float)),
                sigma_sca=sigma_sca, sigma_tr=sigma_tr,
                g_ef=g_ef, qsca_ef=qsca_ef,
                D3=float(np.sum(w * Dc**3)), D2=float(np.sum(w * Dc**2)))


def ell_star_diluido(D_um, lam_nm, phi: float, bias: float = 0.0,
                     n_matriz: float | None = None):
    """ℓ*(λ) en µm suponiendo poros independientes (sin factor de estructura).

        ρ = φ / ⟨πD³/6⟩          (densidad numérica a porosidad φ)
        ℓ* = 1 / (ρ ⟨σ_tr⟩)

    La corrección por dispersión dependiente va en `estructura.py`.
    """
    pr = promedios_PD(D_um, lam_nm, bias=bias, n_matriz=n_matriz)
    rho = phi / (np.pi * pr["D3"] / 6.0)      # poros por µm³
    return 1.0 / (rho * pr["sigma_tr"]), pr
