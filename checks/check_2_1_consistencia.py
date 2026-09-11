"""check 2.1 — la pendiente s es robusta a cómo se la mide.

Dos cosas distintas, y sólo la primera es una igualdad esperable:

(a) DENTRO de cada sub-banda, los dos métodos (regresión cuadrática de ln R vs ln λ y
    derivada de spline suavizado) deben coincidir. Criterio a priori:
        |Δs| ≤ max(2·σ_comb, 0.15·|s̄|)
    El 15 % relativo es el piso porque los métodos no estiman exactamente lo mismo
    (s en el centro geométrico de la banda vs. media de la derivada en la banda).

(b) ENTRE sub-bandas NO se exige que s sea igual: si hay curvatura, s cambia con λ, y de
    hecho cambia (esa es parte de la firma del régimen). Lo que sí se exige es que la
    CONCLUSIÓN sea robusta a la elección de banda: la muestra 4 debe tener s mayor que
    las tres muestras micrométricas en ambas sub-bandas.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from dosregimenes import BANDA_NM  # noqa: E402
from dosregimenes import espectros as sp  # noqa: E402
from dosregimenes import pendiente as pd  # noqa: E402


def run():
    esp = sp.cargar_reflectancia(banda=BANDA_NM)
    med = {m: pd.medir(esp[m]) for m in (1, 2, 3, 4)}

    peor_rel, peor_desc = 0.0, ""
    ok_a = True
    for m, ps in med.items():
        for sub in pd.SUBBANDAS_NM:
            reg = next(p for p in ps if p.metodo == "regresion" and p.subbanda == sub)
            spl = next(p for p in ps if p.metodo == "spline" and p.subbanda == sub)
            d = abs(reg.s - spl.s)
            sbar = abs(0.5 * (reg.s + spl.s))
            tol = max(2 * np.hypot(reg.s_err, spl.s_err), 0.15 * sbar)
            if d > tol:
                ok_a = False
            rel = d / max(sbar, 1e-9)
            if rel > peor_rel:
                peor_rel, peor_desc = rel, f"m{m} {sub[0]:.0f}-{sub[1]:.0f}nm"

    ok_b = True
    for sub in pd.SUBBANDAS_NM:
        def sbar(m):
            return np.mean([p.s for p in med[m] if p.subbanda == sub])
        if not all(sbar(4) > sbar(m) for m in (1, 2, 3)):
            ok_b = False

    ok = ok_a and ok_b
    ev = (f"métodos coinciden={ok_a} (peor discrepancia rel. {peor_rel*100:.0f}% en {peor_desc}); "
          f"m4 > m1,m2,m3 en ambas sub-bandas={ok_b}")
    return "check 2.1 — robustez de s (método y banda)", ok, ev


if __name__ == "__main__":
    print(run())
