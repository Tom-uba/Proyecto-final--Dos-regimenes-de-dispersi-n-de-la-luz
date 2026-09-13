"""check 3.3 — el espesor total medido en las SEM confirma el de la slide 13.

Los espesores de la presentación del Labo 6 (slide 13) se midieron a ojo. Con L/ℓ* ≈ 2 la
transmitancia depende fuerte del espesor, así que hacía falta una medición independiente.

Sólo se chequea el espesor TOTAL, que es robusto. El espesor del núcleo automático no es
confiable cuando las pieles tienen relieve de fractura (m3) — ver notas/log.md — y por eso
el modelo usa el núcleo de la slide 13 con ±15 % de incertidumbre. Que el total coincida a
pocos µm es lo que da confianza en esas mediciones a ojo.

Criterio a priori: para cada muestra, con al menos 2 imágenes a 3000× en las que la lámina
no toca el borde del campo, |mediana / slide13 − 1| < 5 %.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from dosregimenes import DATA  # noqa: E402
from dosregimenes import feret  # noqa: E402

SLIDE13_TOTAL = {1: 83.0, 2: 79.0, 3: 78.0, 4: 78.0}
TOL = 0.05
N_MIN = 2


def run():
    with open(DATA / "sem" / "MANIFEST.csv", encoding="utf-8") as f:
        imgs = [r for r in csv.DictReader(f) if int(r["aumento_x"]) == 3000]
    por_m: dict[int, list[float]] = {1: [], 2: [], 3: [], 4: []}
    for r in imgs:
        tot, ok = feret.espesor_total_um(DATA / "sem" / r["carpeta"] / r["archivo"])
        if ok:
            por_m[int(r["muestra"])].append(tot)

    ok, partes = True, []
    for m in (1, 2, 3, 4):
        v = por_m[m]
        if len(v) < N_MIN:
            ok = False
            partes.append(f"m{m}: sólo {len(v)} imágenes válidas")
            continue
        med = float(np.median(v))
        rel = med / SLIDE13_TOTAL[m] - 1
        if abs(rel) > TOL:
            ok = False
        partes.append(f"m{m} {med:.1f} vs {SLIDE13_TOTAL[m]:.0f} µm ({rel*100:+.1f}%, n={len(v)})")
    return "check 3.3 — espesor total SEM vs slide 13", ok, "; ".join(partes)


if __name__ == "__main__":
    print(run())
