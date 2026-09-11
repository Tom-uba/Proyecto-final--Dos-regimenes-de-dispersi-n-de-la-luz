"""check 0.1 — el promedio de los 20 espectros de tira A reproduce la Fig. 6 del informe.

Afirmaciones del informe verificadas (data/PROCEDENCIA.md §3):
  a) muestras 1–3 decrecientes con λ
  b) orden por reflectancia media: 3 > 2 > 1
  c) muestra 2 con la banda de dispersión más chica
  d) muestra 4: R(450) > todas 1–3 ; R(750) < todas 1–3 ; cae ≈ 3× más
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from dosregimenes import espectros as sp  # noqa: E402


def run():
    esp = sp.cargar_reflectancia(banda=(400.0, 800.0))
    lam = esp[1].lam

    def R(m, l):
        return esp[m].R[np.argmin(np.abs(lam - l))]

    dec = all(R(m, 450) > R(m, 750) for m in (1, 2, 3))
    med = {m: esp[m].R[(lam >= 450) & (lam <= 750)].mean() for m in (1, 2, 3)}
    orden = sorted(med, key=med.get, reverse=True) == [3, 2, 1]
    banda_min = min((1, 2, 3), key=lambda m: esp[m].sigma.mean()) == 2
    m4_alta = R(4, 450) > max(R(m, 450) for m in (1, 2, 3))
    m4_baja = R(4, 750) < min(R(m, 750) for m in (1, 2, 3))
    caida4 = R(4, 450) - R(4, 750)
    caida123 = np.mean([R(m, 450) - R(m, 750) for m in (1, 2, 3)])
    m4_cae_mas = caida4 > 2 * caida123

    ok = all([dec, orden, banda_min, m4_alta, m4_baja, m4_cae_mas])
    ev = (f"1-3 decrec={dec}; orden 3>2>1={orden}; banda_min=m2:{banda_min}; "
          f"m4 R450={R(4,450)*100:.0f}% R750={R(4,750)*100:.0f}%; "
          f"caída m4/{'(1-3)'}={caida4/caida123:.1f}×")
    return "check 0.1 — promedio vs Fig. 6", ok, ev


if __name__ == "__main__":
    print(run())
