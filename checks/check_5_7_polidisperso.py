"""check 5.7 — la hipótesis de polidispersión, puesta a prueba en dos datasets a la vez.

HIPÓTESIS (log 2026-09-13 e): el factor de estructura Percus–Yevick MONODISPERSO a η = φ
apantalla de más porque ignora que los poros tienen tamaños distintos. Si es así, la
aproximación de desacople —sin parámetros libres, con la P(D) medida— debería corregir A LA
VEZ los dos síntomas independientes:
  - la falla del ancla externa de Syurik 2017 (check 5.3), y
  - la sobrepredicción de la muestra 4 (check 5.2 y contraste con T).

CRITERIOS, escritos y commiteados ANTES de la primera ejecución (ver log). Deben cumplirse
los cuatro. Se declara con qué se conocía al fijarlos: con PY monodisperso, (A) da −0.12,
−0.10, −0.06; (B) da s₄ = 1.84; (C) da rms 0.105; y el η ajustado contra T (0.25) da rms 0.022.

  (A) Syurik: R_total(600) a 9, 16 y 53 µm dentro de ±0.10 de 0.57, 0.70 y 0.90.
      El mismo criterio del check 5.3, sin cambios.
  (B) Muestra 4: s₄ en rojo (600–745 nm) dentro del rango que abarcan las cinco regiones
      medidas por separado. Es la dispersión real de la muestra, no una tolerancia elegida.
  (C) Muestra 4: rms de T(λ) predicha contra la medida (tira A, 470–745 nm) < 0.05.
      Pide cerrar la mayor parte de la brecha entre 0.105 y 0.022 sin ajustar nada.
  (D) El contraste entre regímenes no se pierde: Δs rojo dentro de ×0.5–2 (criterio del 5.2).

MODELO: idéntico al del check 5.2 (y al del 5.3 para Syurik), con una sola diferencia:
factor_transporte(..., polidisperso=True). η = φ medida. Nada ajustado.

Los checks 5.2 y 5.3 NO se modifican: registran el modelo monodisperso tal como fue.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from dosregimenes import DATA, MASCARA_NM  # noqa: E402
from dosregimenes import espectros as sp  # noqa: E402
from dosregimenes import estructura as es  # noqa: E402
from dosregimenes import imagej as ij  # noqa: E402
from dosregimenes import lamina as lm  # noqa: E402
from dosregimenes import mie  # noqa: E402
from dosregimenes import montecarlo as mc  # noqa: E402
from dosregimenes.espectros import _leer_txt  # noqa: E402
from dosregimenes.nref import n_sol  # noqa: E402

N_FOT = 60000
SEED = 19

# --- nuestras muestras (mismo modelo que el check 5.2) ---
PHI = {1: 0.19, 2: 0.20, 3: 0.22, 4: 0.33}
L_NUCLEO = {1: 46.0, 2: 41.0, 3: 40.0, 4: 32.0}
ROJO = np.array([600.0, 630.0, 660.0, 700.0, 745.0])
T_GRILLA = np.array([470.0, 520.0, 570.0, 620.0, 670.0, 720.0, 745.0])

# --- Syurik 2017 (mismo modelo que el check 5.3) ---
SY_D, SY_DS, SY_PHI, SY_N, SY_VIDRIO = 0.339, 0.109, 0.39, 1.49, 1.52
SY_L, SY_R = (9.0, 16.0, 53.0), (0.57, 0.70, 0.90)

TOL_A, TOL_C = 0.10, 0.05


def _nuestra(m, lam, poros):
    D = ij.PD(m, poros=poros)
    ell, pr = mie.ell_star_diluido(D, lam, PHI[m])
    n_ef = lm.n_efectivo(n_sol(lam), PHI[m])
    g = pr["g_ef"]
    ell = ell / es.factor_transporte(D, lam, n_ef, PHI[m], g, polidisperso=True)
    rs = [mc.correr(ell[i], float(g[i]), float(n_ef[i]), L_NUCLEO[m], n_fotones=N_FOT, seed=SEED)
          for i in range(lam.size)]
    return np.array([r["R_difusa"] for r in rs]), np.array([r["T"] for r in rs])


def _s_regiones_m4():
    out = []
    for f in sorted((DATA / "reflectancia").glob("tira_A_muestra_4_*_Reflection*.txt")):
        wl, v = _leer_txt(f)
        ok = (wl >= 600) & (wl <= 745) & ~((wl >= MASCARA_NM[0]) & (wl <= MASCARA_NM[1]))
        out.append(lm.pendiente(wl[ok], v[ok] / 100.0))
    return np.array(out)


def run():
    # (A) Syurik
    s2 = np.log(1 + (SY_DS / SY_D) ** 2)
    Dsy = np.random.default_rng(3).lognormal(np.log(SY_D) - s2 / 2, np.sqrt(s2), 40000)
    lam6 = np.array([600.0])
    ell, pr = mie.ell_star_diluido(Dsy, lam6, SY_PHI, n_matriz=SY_N)
    n_ef = lm.n_efectivo(np.full(1, SY_N), SY_PHI)
    fS = es.factor_transporte(Dsy, lam6, n_ef, SY_PHI, pr["g_ef"], polidisperso=True)
    ell = ell / fS
    R_sy = [mc.correr(float(ell[0]), float(pr["g_ef"][0]), float(n_ef[0]), L, n_fotones=N_FOT,
                      seed=SEED, n_abajo=SY_VIDRIO)["R_total"] for L in SY_L]
    ok_A = all(abs(a - b) <= TOL_A for a, b in zip(R_sy, SY_R))

    # nuestras muestras
    poros = ij.cargar_poros()
    s_rojo = {}
    for m in (1, 2, 3, 4):
        Rd, _ = _nuestra(m, ROJO, poros)
        s_rojo[m] = lm.pendiente(ROJO, Rd)

    # (B) s4 dentro del rango de las cinco regiones
    reg = _s_regiones_m4()
    ok_B = reg.min() <= s_rojo[4] <= reg.max()

    # (C) rms de T de m4
    _, T4 = _nuestra(4, T_GRILLA, poros)
    TA = sp.cargar_transmitancia("A")[4]
    rms = float(np.sqrt(np.mean((T4 - np.interp(T_GRILLA, TA.lam, TA.R)) ** 2)))
    ok_C = rms < TOL_C

    # (D) Δs rojo
    R = sp.cargar_reflectancia()

    def s_med(m):
        e = R[m]
        ok = (e.lam >= 600) & (e.lam <= 745) & ~((e.lam >= MASCARA_NM[0]) & (e.lam <= MASCARA_NM[1]))
        return lm.pendiente(e.lam[ok], e.R[ok])

    ds_p = s_rojo[4] - np.mean([s_rojo[m] for m in (1, 2, 3)])
    ds_m = s_med(4) - np.mean([s_med(m) for m in (1, 2, 3)])
    razon = ds_p / ds_m
    ok_D = 0.5 <= razon <= 2.0

    ev = (f"(A) Syurik R(600): " + ", ".join(f"{L:.0f} µm {a:.2f} vs {b:.2f}" for L, a, b in zip(SY_L, R_sy, SY_R)) +
          f", factor {float(fS[0]):.2f} → {ok_A} | (B) s₄ rojo {s_rojo[4]:.2f} en [{reg.min():.2f}, {reg.max():.2f}] → {ok_B} | "
          f"(C) rms T m4 {rms:.3f} (<{TOL_C}) → {ok_C} | (D) Δs rojo {ds_p:.2f} vs {ds_m:.2f} (×{razon:.2f}) → {ok_D}")
    return "check 5.7 — hipótesis de polidispersión (Syurik + muestra 4)", bool(ok_A and ok_B and ok_C and ok_D), ev


if __name__ == "__main__":
    print(run())
