"""check 4.1 — las nubes P(x) forman dos grupos disjuntos.

Es el check que sostiene la palabra "dos" del título del proyecto. Si las cuatro muestras
se solaparan en el eje x no habría dos regímenes que caracterizar, habría un continuo.

Criterio a priori, con el coeficiente de solape ∫min(f_a, f_b) sobre log10(x)
(0 = disjuntas, 1 = idénticas):
    (a) las tres micrométricas se solapan entre sí:  solape > 0.80 en los tres pares
    (b) la nanométrica es disjunta de cada una:      solape < 0.05

Se reporta además el hueco entre el p95 de la muestra 4 y el p5 de las micrométricas. Ese
hueco es lo que hace que la conclusión no dependa de dónde se ponga exactamente la frontera
(F1: x = 1, informe/teoria.md §6).
"""
from __future__ import annotations

import sys
from itertools import combinations
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from dosregimenes import imagej as ij  # noqa: E402
from dosregimenes import size_param as sx  # noqa: E402

TOL_JUNTAS = 0.80
TOL_DISJUNTAS = 0.05


def run():
    poros = ij.cargar_poros()
    nubes = {m: sx.nube_x(ij.PD(m, poros=poros)) for m in (1, 2, 3, 4)}

    juntas = {f"m{a}-m{b}": sx.solape(nubes[a], nubes[b]) for a, b in combinations((1, 2, 3), 2)}
    disjuntas = {f"m{a}-m4": sx.solape(nubes[a], nubes[4]) for a in (1, 2, 3)}

    ok_a = all(v > TOL_JUNTAS for v in juntas.values())
    ok_b = all(v < TOL_DISJUNTAS for v in disjuntas.values())

    b = {m: sx.banda_x(m, ij.PD(m, poros=poros)) for m in (1, 2, 3, 4)}
    p5_123 = min(b[m].x_p5 for m in (1, 2, 3))
    hueco = p5_123 / b[4].x_p95

    ev = (f"solape m1-3 entre sí: {min(juntas.values()):.2f}–{max(juntas.values()):.2f} "
          f"(>{TOL_JUNTAS}); vs m4: {max(disjuntas.values()):.3f} (<{TOL_DISJUNTAS}) | "
          f"x mediana: m1-3 ≈ {b[1].x_mediana:.1f}, m4 = {b[4].x_mediana:.2f} | "
          f"hueco p95(m4)={b[4].x_p95:.2f} → p5(m1-3)={p5_123:.2f}, factor {hueco:.1f}")
    return "check 4.1 — dos grupos disjuntos en el eje x", ok_a and ok_b, ev


if __name__ == "__main__":
    print(run())
