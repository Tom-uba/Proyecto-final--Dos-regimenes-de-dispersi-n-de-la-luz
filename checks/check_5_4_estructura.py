"""check 5.4 — el factor de estructura reproduce sus dos límites exactos.

S(q) de Percus–Yevick se integra numéricamente (ver el encabezado de estructura.py: la
forma cerrada de Ashcroft–Lekner es larga y fácil de transcribir mal). Este check es lo
que hace que esa decisión sea segura, porque los dos límites SÍ se conocen exactamente:

    S(q→0) = (1−η)⁴/(1+2η)²      compresibilidad, exacta en PY
    S(q→∞) → 1                    a q grande no hay correlación

Se verifican en todo el rango de η que usa el proyecto (0.15–0.40, que cubre φ ≈ 0.20 de
las muestras 1–3 y 0.33 de la muestra 4).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from dosregimenes import estructura as es  # noqa: E402

ETAS = (0.15, 0.20, 0.25, 0.33, 0.40)
TOL_CERO = 0.02
TOL_INF = 0.02


def run():
    peor_cero, peor_inf, ok = 0.0, 0.0, True
    for eta in ETAS:
        s0_num = float(es.S_py(1e-4, eta)[0])
        s0_exa = es.S_py_cero(eta)
        e0 = abs(s0_num / s0_exa - 1.0)

        sinf = es.S_py(np.linspace(60.0, 120.0, 40), eta)
        einf = float(np.max(np.abs(sinf - 1.0)))

        if e0 > TOL_CERO or einf > TOL_INF:
            ok = False
        peor_cero = max(peor_cero, e0)
        peor_inf = max(peor_inf, einf)

    ev = (f"η ∈ {ETAS}: S(0) coincide con (1−η)⁴/(1+2η)² dentro de {peor_cero*100:.2f}%; "
          f"|S(q→∞)−1| ≤ {peor_inf:.3f}")
    return "check 5.4 — límites exactos de S(q) (Percus–Yevick)", ok, ev


if __name__ == "__main__":
    print(run())
