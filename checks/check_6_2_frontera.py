"""check 6.2 — la frontera, como intervalo, es compatible con lo que permiten los datos.

PRE-REGISTRADO (notas/log.md, 2026-09-13 g). Definiciones en `dosregimenes.frontera`.

Cotas de los datos: la transición tiene que caer entre los dos cúmulos, con el ±30 %
sistemático de D aplicado en la dirección que los acerca:
    [x̃₄(470 nm)·1.30 ,  mín x̃₁₂₃(750 nm)·0.70]

CRITERIOS (todos):
  (1) los intervalos de F1, F2 y F3 (n_sol en 470/750 nm, sesgo 0/+2 %) caen dentro de las
      cotas de los datos;
  (2) al menos 2 de las 4 curvas s_pred(x̃) del barrido (2 entornos × 2 cierres) cruzan
      s* = (s₄ + s̄₁₂₃)/2 medida, y todos los cruces F_s caen dentro de las cotas;
  (3) procedencia: el CSV del barrido (scripts/06_frontera.py) se reproduce en un punto
      recalculado acá (entorno 4, monodisperso, x̃ más cercano a 0.5), |Δs| < 1e-3.

Lo que se reporta como FRONTERA: el intervalo que cubre F1, F2, F3 y F_s.
Advertencia registrada de antemano: pasar (1)–(2) sólo dice que la teoría es COMPATIBLE con
los datos. Con dos cúmulos separados ×5 los datos no pueden ubicar la frontera más fino que
sus propias cotas.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from dosregimenes import espectros as sp  # noqa: E402
from dosregimenes import frontera as fr  # noqa: E402
from dosregimenes import imagej as ij  # noqa: E402
from dosregimenes import modelo as md  # noqa: E402

CSV = RAIZ / "resultados" / "06_frontera_s.csv"


def run():
    if not CSV.exists():
        return "check 6.2 — frontera acotada", False, f"falta {CSV.name}: correr scripts/06_frontera.py"
    poros = ij.cargar_poros()
    cot = fr.cota_datos(poros)
    F = fr.fronteras_mie()
    dentro = lambda a, b: cot["inf"] <= a and b <= cot["sup"]  # noqa: E731
    ok1 = all(dentro(*F[k]) for k in ("F1", "F2", "F3"))

    R = sp.cargar_reflectancia()
    s_med = {m: md.s_medida(R[m]) for m in (1, 2, 3, 4)}
    s_star = 0.5 * (s_med[4] + np.mean([s_med[m] for m in (1, 2, 3)]))

    with open(CSV, encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    Fs = {}
    for ent in fr.ENTORNOS:
        for cierre in ("monodisperso", "desacople"):
            sel = [r for r in filas if r["entorno"] == ent and r["cierre"] == cierre]
            Fs[f"{ent}/{cierre}"] = fr.cruce([float(r["x_mediana"]) for r in sel],
                                             [float(r["s_rojo"]) for r in sel], s_star)
    cruzan = {k: v for k, v in Fs.items() if np.isfinite(v)}
    ok2 = len(cruzan) >= 2 and all(dentro(v, v) for v in cruzan.values())

    D4 = ij.PD(4, poros=poros)
    xt = float(fr.X_BARRIDO[np.argmin(np.abs(np.log(fr.X_BARRIDO / 0.5)))])
    p = fr.punto(D4 / np.median(D4), xt, "4", False)
    fila = next(r for r in filas if r["entorno"] == "4" and r["cierre"] == "monodisperso"
                and abs(float(r["x_mediana"]) - xt) < 1e-3)
    err3 = abs(p["s_rojo"] - float(fila["s_rojo"]))
    ok3 = err3 < 1e-3

    lo = min([F["F1"][0], F["F2"][0], F["F3"][0]] + list(cruzan.values()))
    hi = max([F["F1"][1], F["F2"][1], F["F3"][1]] + list(cruzan.values()))
    ev = (f"cotas de los datos [{cot['inf']:.2f}, {cot['sup']:.2f}] | F2 [{F['F2'][0]:.2f}, "
          f"{F['F2'][1]:.2f}], F3 [{F['F3'][0]:.2f}, {F['F3'][1]:.2f}] → {ok1} | s* {s_star:.2f}: "
          + ", ".join(f"F_s {k} {v:.2f}" for k, v in Fs.items()) +
          f" → {ok2} | CSV reproducido |Δs| {err3:.1e} → {ok3} | FRONTERA x ∈ [{lo:.2f}, {hi:.2f}]")
    return "check 6.2 — frontera acotada", bool(ok1 and ok2 and ok3), ev


if __name__ == "__main__":
    print(run())
