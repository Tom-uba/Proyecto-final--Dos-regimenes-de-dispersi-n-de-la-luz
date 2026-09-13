"""Cadena directa morfología → espectro, compartida por la Etapa 6.

Es la cadena de los checks 5.2 (`polidisperso=False`) y 5.7 (`polidisperso=True`):

    P(D) → Mie promediado → ℓ* diluido a porosidad φ → factor de estructura (η = φ)
         → Monte Carlo de una lámina de espesor L

Se extrajo acá para no copiarla en cada control. Los checks 5.x no se modificaron: siguen
registrando exactamente lo que corrió entonces. Con los mismos argumentos, `cadena` da los
mismos números que el check 5.2 (misma semilla por λ).

Opciones que agrega la Etapa 6:
  congelar_nm  la dispersión (ℓ*, g, n_ef) se evalúa en esa λ para TODAS las λ pedidas: un
               medio espectralmente plano (hipótesis alternativa del control de absorción).
  mu_a_sol     absorción del SÓLIDO en µm⁻¹, array (nμ, nλ). En el medio efectivo se usa
               μ_a = (1−φ)·μ_a,sol, sin concentración de campo (supuesto declarado).
"""
from __future__ import annotations

import numpy as np

from . import estructura as es
from . import lamina as lm
from . import mie
from . import montecarlo as mc
from .nref import n_sol

ROJO = np.array([600.0, 630.0, 660.0, 700.0, 745.0])
PHI = {1: 0.19, 2: 0.20, 3: 0.22, 4: 0.33}
L_NUCLEO = {1: 46.0, 2: 41.0, 3: 40.0, 4: 32.0}
N_FOT = 60000
SEED = 13


def cadena(D_um, lam_nm, phi: float, L_um: float, polidisperso: bool = False,
           n_fotones: int = N_FOT, seed: int = SEED, congelar_nm: float | None = None,
           mu_a_sol=None) -> dict:
    """R_especular, R_difusa, R_total, T por λ (y *_abs con absorción)."""
    lam = np.atleast_1d(np.asarray(lam_nm, float))
    lam_d = np.full(lam.shape, float(congelar_nm)) if congelar_nm is not None else lam
    ell, pr = mie.ell_star_diluido(D_um, lam_d, phi)
    n_ef = lm.n_efectivo(n_sol(lam_d), phi)
    g = pr["g_ef"]
    fS = es.factor_transporte(D_um, lam_d, n_ef, phi, g, polidisperso=polidisperso)
    ell = ell / fS

    mu = None if mu_a_sol is None else (1.0 - phi) * np.atleast_2d(np.asarray(mu_a_sol, float))
    claves = ("R_especular", "R_difusa", "R_total", "T")
    out = {k: np.empty(lam.size) for k in claves}
    if mu is not None:
        out["R_total_abs"] = np.empty((mu.shape[0], lam.size))
        out["T_abs"] = np.empty((mu.shape[0], lam.size))
    for i in range(lam.size):
        r = mc.correr(float(ell[i]), float(g[i]), float(n_ef[i]), float(L_um),
                      n_fotones=n_fotones, seed=seed, mu_a=None if mu is None else mu[:, i])
        for k in claves:
            out[k][i] = r[k]
        if mu is not None:
            out["R_total_abs"][:, i] = r["R_total_abs"]
            out["T_abs"][:, i] = r["T_abs"]
    out.update(lam=lam, ell=ell, g=g, n_ef=n_ef, factor_S=fS)
    return out


def s_medida(esp, lo: float = 600.0, hi: float = 745.0) -> float:
    """s de un espectro medido en [lo, hi], sin la máscara instrumental."""
    ok = (esp.lam >= lo) & (esp.lam <= hi) & esp.mascara_valida
    return lm.pendiente(esp.lam[ok], esp.R[ok])
