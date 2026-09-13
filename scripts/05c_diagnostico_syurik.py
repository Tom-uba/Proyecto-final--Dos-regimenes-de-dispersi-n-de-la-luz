"""Diagnóstico de la falla del check 5.3 (ancla externa Syurik 2017).  [Etapa 5]

RESULTADO:   tabla impresa: R_total(600) contra espesor y l_t extraído, para tres variantes
             del factor de estructura. Registrada en notas/log.md (2026-09-13, entrada e).
ENTRADA:     morfología publicada por Syurik et al. 2017 (ver checks/check_5_3_syurik.py y
             notas/fichas.md): poros 339 ± 109 nm, fracción 39 %, PMMA n = 1.49, sobre vidrio.
CÁLCULO:     dosregimenes.mie.ell_star_diluido → estructura.factor_transporte →
             montecarlo.correr(n_abajo=1.52)
DERIVADO vs LIBRERÍA:  todo propio salvo la serie de Mie (miepython).
ELECCIONES:  - variantes del factor de estructura: ninguno, η = 0.25, η = φ = 0.39;
             - l_t "como en el paper": pendiente de T = 1 − R contra 1/L sobre espesores de
               9 a 79 µm, por el origen y con ordenada libre (el paper no dice cuál);
             - 80 000 fotones, semilla fija (números aleatorios comunes entre espesores).
CHECK:       este script NO es un check y no cambia el 5.3: el 5.3 falla tal como se registró.
             Sirve para localizar qué pieza del modelo falla.
INCERTIDUMBRE:  ruido de Monte Carlo ~±0.01 en R con 80 000 fotones.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from dosregimenes import estructura as es  # noqa: E402
from dosregimenes import lamina as lm  # noqa: E402
from dosregimenes import mie  # noqa: E402
from dosregimenes import montecarlo as mc  # noqa: E402

D_M, D_S, PHI, N_PMMA, N_VIDRIO = 0.339, 0.109, 0.39, 1.49, 1.52
PUB = {9: 0.57, 16: 0.70, 53: 0.90}
LS = [9, 16, 25, 35, 53, 79]


def main() -> None:
    s2 = np.log(1 + (D_S / D_M) ** 2)
    D = np.random.default_rng(3).lognormal(np.log(D_M) - s2 / 2, np.sqrt(s2), 40000)
    lam = np.array([600.0])
    ell0, pr = mie.ell_star_diluido(D, lam, PHI, n_matriz=N_PMMA)
    n_ef = lm.n_efectivo(np.full(1, N_PMMA), PHI)
    g = pr["g_ef"]
    print(f"n_ef = {n_ef[0]:.3f}   g = {g[0]:.3f}   l* sin S = {ell0[0]:.2f} um")
    for eta in (None, 0.25, PHI):
        f = np.ones(1) if eta is None else es.factor_transporte(D, lam, n_ef, eta, g)
        ell = ell0 / f
        R = np.array([mc.correr(float(ell[0]), float(g[0]), float(n_ef[0]), float(L),
                                n_fotones=80000, seed=17, n_abajo=N_VIDRIO)["R_total"] for L in LS])
        invL = 1.0 / np.array(LS, float)
        T = 1.0 - R
        pend_origen = float(np.sum(T * invL) / np.sum(invL ** 2))
        pend, ordenada = np.polyfit(invL, T, 1)
        nombre = "sin S" if eta is None else f"eta={eta:.2f}"
        filas = ", ".join(f"{L} um {R[i]:.2f}" + (f" (pub {PUB[L]:.2f})" if L in PUB else "")
                          for i, L in enumerate(LS))
        print(f"{nombre:9s} factor {f[0]:.2f}  l* {ell[0]:.2f} um | R(600): {filas}")
        print(f"          l_t como en el paper: por el origen {pend_origen:.2f} um, "
              f"con ordenada {pend:.2f} um   [publicado 3.5-4 um]")


if __name__ == "__main__":
    main()
