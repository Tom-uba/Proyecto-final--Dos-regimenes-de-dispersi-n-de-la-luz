"""check 2.2 — la muestra 4 se separa de las micrométricas en la pendiente espectral.

Es el check que decide si la hipótesis sobrevive ya al nivel de los datos: si la s de la
muestra 4 no se distingue de la de las muestras 1–3, no hay dos regímenes que caracterizar.

Criterio a priori, por sub-banda:
    |s₄ − s̄₁₂₃| > 3 · σ(s₁, s₂, s₃)
con s por muestra = media de los dos métodos, y σ = desvío entre las TRES muestras
micrométricas (dispersión intra-grupo, que es la escala de lo que "no es un régimen
distinto"). Se exige en AMBAS sub-bandas.

Se reportan DOS varas, porque miden cosas distintas y la primera sola exagera:
  σ_entre  = dispersión muestra a muestra dentro de {1,2,3}. Es muy chica (~0.01–0.02)
             justamente porque las tres son casi idénticas.
  σ_ajuste = incertidumbre de un ajuste individual (~0.2–0.4), que es mayor.
La conclusión no depende de cuál se use, pero el número de "sigmas" sí.
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

    partes, ok = [], True
    for sub in pd.SUBBANDAS_NM:
        s = {m: float(np.mean([p.s for p in med[m] if p.subbanda == sub]))
             for m in (1, 2, 3, 4)}
        err = {m: float(np.mean([p.s_err for p in med[m] if p.subbanda == sub]))
               for m in (1, 2, 3, 4)}
        s123 = np.array([s[1], s[2], s[3]])
        sig_entre = float(s123.std(ddof=1))
        sig_ajuste = float(np.hypot(np.mean([err[m] for m in (1, 2, 3)]), err[4]))
        sep = abs(s[4] - s123.mean())
        n_entre = sep / sig_entre if sig_entre > 0 else np.inf
        n_ajuste = sep / sig_ajuste if sig_ajuste > 0 else np.inf
        if n_entre <= 3:
            ok = False
        partes.append(f"{sub[0]:.0f}-{sub[1]:.0f}nm: s₁₂₃={s123.mean():.2f}, s₄={s[4]:.2f}, "
                      f"Δ={sep:.2f} → {n_entre:.0f}σ_entre / {n_ajuste:.1f}σ_ajuste")

    return "check 2.2 — separación m4 vs m1–3", ok, "; ".join(partes)


if __name__ == "__main__":
    print(run())
