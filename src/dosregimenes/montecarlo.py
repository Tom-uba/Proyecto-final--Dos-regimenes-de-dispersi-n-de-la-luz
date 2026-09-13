"""Transporte radiativo en una lámina por Monte Carlo.  [Etapa 5]

Pasó de opcional a NECESARIO: la aproximación de difusión (`lamina.py`) requiere L ≫ ℓ*, y
para las muestras 1–3 da L/ℓ* ≈ 1.3–2.0. Ahí manda este módulo.

## Modelo

Lámina infinita lateralmente, espesor L, NO absorbente, índice efectivo n_ef. Arriba hay
aire; abajo, un medio de índice `n_abajo` (aire por defecto; vidrio en el ancla externa del
check 5.3). Incidencia normal desde arriba.

- Entrada: reflexión especular de Fresnel a incidencia normal, R₀ = ((n_ef−1)/(n_ef+1))².
- Paso libre: exponencial con coeficiente de dispersión μ_s = 1/[ℓ*(1−g)].
  (ℓ* = 1/[μ_s(1−g)] es el camino de transporte de mie.py; se despeja μ_s.)
- Fase: Henyey–Greenstein con la g efectiva de Mie.
- Bordes: reflexión de Fresnel no polarizada hacia el medio de afuera correspondiente, en el
  ángulo real de incidencia, con reflexión total interna; se decide por sorteo. Lo que sale
  por abajo cuenta como T y no vuelve.

Al llegar a un borde el fotón se detiene ahí y se re-sortea el siguiente paso. Es
insesgado porque la distribución exponencial no tiene memoria.

Sin absorción, todo fotón termina en R o en T: R_especular + R_difusa + T = 1 por conteo.

## Verificación (`checks/check_5_5_montecarlo.py`)

  (a) límite balístico, ℓ* → ∞:  R = 2R₀/(1+R₀),  T = (1−R₀)/(1+R₀)   (exacto)
  (b) régimen grueso, L ≫ ℓ*:    T coincide con difusión de `lamina.py`

`n_abajo` se agregó para el check 5.3 (2026-09-13). Con su valor por defecto (1.0) el
generador consume los mismos números aleatorios que antes, así que los checks 5.2 y 5.5 dan
exactamente lo mismo.

## Absorción (Etapa 6, control de absorción)

`mu_a` (µm⁻¹, un número o un array) activa la absorción por PESO DE CAMINO: se registra el
camino total recorrido dentro de la lámina por cada fotón que sale, y la fracción que
escapa con absorción μ_a es  Σ exp(−μ_a · camino) / N.  Es exacto para un medio de absorción
homogénea (Beer–Lambert microscópico) y una sola corrida sirve para muchos μ_a. No consume
números aleatorios: con o sin `mu_a` las fracciones sin absorción son idénticas.
Validado en `checks/check_6_0_mc_absorcion.py` contra el límite balístico con absorción.
"""
from __future__ import annotations

import numpy as np


def _fresnel(cos_i, n1: float, n2: float = 1.0):
    """Reflectancia no polarizada desde el medio n1 hacia el medio n2."""
    cos_i = np.clip(np.abs(cos_i), 0.0, 1.0)
    sin_t = (n1 / n2) * np.sqrt(1.0 - cos_i**2)
    R = np.ones_like(cos_i)                    # reflexión total interna por defecto
    ok = sin_t < 1.0
    ci, ct = cos_i[ok], np.sqrt(1.0 - sin_t[ok] ** 2)
    rs = (n1 * ci - n2 * ct) / (n1 * ci + n2 * ct)
    rp = (n2 * ci - n1 * ct) / (n2 * ci + n1 * ct)
    R[ok] = 0.5 * (rs**2 + rp**2)
    return R


def _hg(g: float, xi):
    """Coseno del ángulo de dispersión muestreado de Henyey–Greenstein."""
    if abs(g) < 1e-6:
        return 2.0 * xi - 1.0
    frac = (1.0 - g * g) / (1.0 - g + 2.0 * g * xi)
    return np.clip((1.0 + g * g - frac * frac) / (2.0 * g), -1.0, 1.0)


def correr(ell_star_um: float, g: float, n_ef: float, d_um: float,
           n_fotones: int = 20000, seed: int = 0, max_pasos: int = 200000,
           n_abajo: float = 1.0, mu_a=None) -> dict:
    """Devuelve fracciones R_especular, R_difusa, R_total, T y sin_escapar.

    Con `mu_a` agrega R_total_abs y T_abs: arrays del largo de `mu_a`.
    """
    rng = np.random.default_rng(seed)
    L = float(d_um)
    mus = 1.0 / (float(ell_star_um) * (1.0 - g))
    R0 = ((n_ef - 1.0) / (n_ef + 1.0)) ** 2

    entra = rng.random(n_fotones) >= R0
    n_esp = int(n_fotones - entra.sum())
    n = int(entra.sum())
    z = np.zeros(n)
    ux, uy, uz = np.zeros(n), np.zeros(n), np.ones(n)
    vivo = np.ones(n, bool)
    nR = nT = 0
    camino = np.zeros(n)
    caminos_R, caminos_T = [], []

    for _ in range(max_pasos):
        idx = np.flatnonzero(vivo)
        if idx.size == 0:
            break
        paso = -np.log(rng.random(idx.size)) / mus
        zn = z[idx] + paso * uz[idx]
        arriba, abajo = zn < 0.0, zn > L
        borde = arriba | abajo

        # --- los que llegan a un borde: Fresnel hacia el medio de afuera ---
        if borde.any():
            b = idx[borde]
            es_arriba = arriba[borde]
            camino[b] += np.where(es_arriba, -z[b], L - z[b]) / uz[b]
            z[b] = np.where(es_arriba, 0.0, L)
            Rf = np.where(es_arriba, _fresnel(uz[b], n_ef, 1.0), _fresnel(uz[b], n_ef, n_abajo))
            refleja = rng.random(b.size) < Rf
            uz[b[refleja]] *= -1.0
            sale = b[~refleja]
            sale_arriba = z[sale] == 0.0
            nR += int(sale_arriba.sum())
            nT += int((~sale_arriba).sum())
            if mu_a is not None:
                caminos_R.append(camino[sale[sale_arriba]])
                caminos_T.append(camino[sale[~sale_arriba]])
            vivo[sale] = False

        # --- los que siguen adentro: mover y dispersar ---
        interior = idx[~borde]
        if interior.size:
            z[interior] = zn[~borde]
            camino[interior] += paso[~borde]
            ct = _hg(g, rng.random(interior.size))
            st = np.sqrt(1.0 - ct**2)
            phi = 2.0 * np.pi * rng.random(interior.size)
            cp, sp = np.cos(phi), np.sin(phi)
            x, y, w = ux[interior], uy[interior], uz[interior]
            vertical = np.abs(w) > 0.99999
            tmp = np.sqrt(np.where(vertical, 1.0, 1.0 - w**2))
            nx = np.where(vertical, st * cp, st * (x * w * cp - y * sp) / tmp + x * ct)
            ny = np.where(vertical, st * sp, st * (y * w * cp + x * sp) / tmp + y * ct)
            nz = np.where(vertical, np.sign(w) * ct, -st * cp * tmp + w * ct)
            ux[interior], uy[interior], uz[interior] = nx, ny, nz

    sin_escapar = int(vivo.sum())
    N = float(n_fotones)
    out = dict(R_especular=n_esp / N, R_difusa=nR / N, R_total=(n_esp + nR) / N,
               T=nT / N, sin_escapar=sin_escapar / N, R0=R0)
    if mu_a is not None:
        mu = np.atleast_1d(np.asarray(mu_a, float))
        cR = np.concatenate(caminos_R) if caminos_R else np.zeros(0)
        cT = np.concatenate(caminos_T) if caminos_T else np.zeros(0)
        out["R_total_abs"] = np.array([n_esp + np.exp(-u * cR).sum() for u in mu]) / N
        out["T_abs"] = np.array([np.exp(-u * cT).sum() for u in mu]) / N
    return out
