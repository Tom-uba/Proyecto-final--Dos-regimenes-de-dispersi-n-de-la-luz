"""check 5.2 — la predicción SIN parámetros ajustados reproduce el contraste entre regímenes.

Es el check que responde la pregunta del proyecto, y por eso su diseño se fija antes de
mirar el resultado (plan de trabajo, §J):

  OBSERVABLE PRIMARIO: Δs = s₄ − s̄₁₂₃ en la banda ROJA (600–745 nm).
    - Δs y no s absoluta: un error de calibración multiplicativo del patrón blanco suma el
      mismo término a la s de todas las muestras y se cancela en la diferencia.
    - Rojo y no azul: en el azul las muestras 1–3 cargan un exceso de pendiente que no es
      común a las cuatro (anomalía A3 y quizá el patrón amarillento), así que ahí Δs deja
      de ser inmune. Ver notas/log.md, 2026-09-13.

  CRITERIO (registrado en el plan): signo correcto y  1/2 ≤ Δs_pred / Δs_med ≤ 2.

  MODELO, sin ningún número tomado de los espectros:
    P(D) de ImageJ → Mie promediado → ℓ* con φ por muestra (0.19 / 0.20 / 0.22 / 0.33)
    → factor de estructura Percus–Yevick con η = φ MEDIDA (no ajustada) → Monte Carlo de
    lámina con el espesor de núcleo de la slide 13 (46 / 41 / 40 / 32 µm).

Se reporta sin gatear: Δs azul, y s absolutas. NO entra el refinamiento con η ajustado
contra la transmitancia (η ≈ 0.25): eso sería usar datos para fijar un parámetro.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from dosregimenes import MASCARA_NM  # noqa: E402
from dosregimenes import espectros as sp  # noqa: E402
from dosregimenes import estructura as es  # noqa: E402
from dosregimenes import imagej as ij  # noqa: E402
from dosregimenes import lamina as lm  # noqa: E402
from dosregimenes import mie  # noqa: E402
from dosregimenes import montecarlo as mc  # noqa: E402
from dosregimenes.nref import n_sol  # noqa: E402

PHI = {1: 0.19, 2: 0.20, 3: 0.22, 4: 0.33}
L_NUCLEO = {1: 46.0, 2: 41.0, 3: 40.0, 4: 32.0}
BANDAS = {"rojo": np.array([600.0, 630.0, 660.0, 700.0, 745.0]),
          "azul": np.array([470.0, 500.0, 530.0, 555.0, 590.0])}
N_FOT = 60000
SEED = 13


def _s_medida(esp, lo, hi):
    ok = (esp.lam >= lo) & (esp.lam <= hi) & ~((esp.lam >= MASCARA_NM[0]) & (esp.lam <= MASCARA_NM[1]))
    return lm.pendiente(esp.lam[ok], esp.R[ok])


def run():
    poros = ij.cargar_poros()
    R = sp.cargar_reflectancia()
    pred, med, fmin13 = {}, {}, 1.0
    for banda, lam in BANDAS.items():
        pred[banda], med[banda] = {}, {}
        for m in (1, 2, 3, 4):
            D = ij.PD(m, poros=poros)
            ell, pr = mie.ell_star_diluido(D, lam, PHI[m])
            n_ef = lm.n_efectivo(n_sol(lam), PHI[m])
            g = pr["g_ef"]
            fS = es.factor_transporte(D, lam, n_ef, PHI[m], g)
            if m != 4:
                fmin13 = min(fmin13, float(fS.min()))
            ell = ell / fS
            Rd = np.array([mc.correr(ell[i], float(g[i]), float(n_ef[i]), L_NUCLEO[m],
                                     n_fotones=N_FOT, seed=SEED)["R_difusa"]
                           for i in range(lam.size)])
            pred[banda][m] = lm.pendiente(lam, Rd)
            med[banda][m] = _s_medida(R[m], lam.min(), lam.max())

    def ds(d):
        return d[4] - np.mean([d[1], d[2], d[3]])

    ds_p, ds_m = ds(pred["rojo"]), ds(med["rojo"])
    razon = ds_p / ds_m if ds_m != 0 else np.inf
    ok = (np.sign(ds_p) == np.sign(ds_m)) and (0.5 <= razon <= 2.0)

    ds_pa, ds_ma = ds(pred["azul"]), ds(med["azul"])
    ev = (f"Δs rojo: pred {ds_p:.2f} vs med {ds_m:.2f} (×{razon:.2f}, criterio 0.5–2) | "
          f"Δs azul [info]: pred {ds_pa:.2f} vs med {ds_ma:.2f} (×{ds_pa/ds_ma:.2f}) | "
          f"s rojo pred/med: " +
          ", ".join(f"m{m} {pred['rojo'][m]:.2f}/{med['rojo'][m]:.2f}" for m in (1, 2, 3, 4)) +
          f" | factor de estructura m1–3 ≥ {fmin13:.3f}")
    return "check 5.2 — predicción sin ajuste: Δs rojo", bool(ok), ev


if __name__ == "__main__":
    print(run())
