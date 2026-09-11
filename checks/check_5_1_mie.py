"""check 5.1 — la rutina de Mie reproduce los dos límites analíticos de teoria.md.

Es el check que valida la herramienta antes de usarla para predecir nada. Los dos límites
son independientes de este proyecto: los fija la teoría (Bohren & Huffman), así que si la
rutina falla acá, falla y punto.

  (a) Rayleigh, x → 0:   Q_sca = (8/3) x⁴ |(m²−1)/(m²+2)|²      [teoria.md ec. (3)]
      Se exige la potencia (pendiente log-log = 4 ± 0.01) Y el prefactor (±0.5 %).
      Exigir sólo la pendiente sería flojo: cualquier x⁴ mal normalizado pasaría.

  (b) Difracción, x → ∞:  Q_sca → 2                              [teoria.md ec. (5)]
      Q_sca oscila ("ripple") alrededor de 2 con amplitud decreciente, así que no se pide
      convergencia punto a punto sino que el PROMEDIO sobre un tramo de x grandes esté a
      menos del 2 % de 2.

Ojo con la convención: acá se trabaja con el x de MIE (λ en el medio), que es n_sol veces
el x = πD/λ₀ del resto del proyecto. Ver el encabezado de src/dosregimenes/mie.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from dosregimenes import mie  # noqa: E402
from dosregimenes.nref import n_sol  # noqa: E402

M_REL = 1.0 / float(n_sol(580.0))     # aire en acetato de celulosa
TOL_POTENCIA = 0.01
TOL_PREFACTOR = 0.005
TOL_LIMITE = 0.02


def run():
    # (a) Rayleigh
    xs = np.array([0.005, 0.01, 0.02, 0.04])
    q, _ = mie.qsca_g_mie(xs, M_REL)
    pend = np.diff(np.log(q)) / np.diff(np.log(xs))
    err_pot = float(np.max(np.abs(pend - 4.0)))

    c_teo = 8.0 / 3.0 * abs((M_REL**2 - 1) / (M_REL**2 + 2)) ** 2
    c_num = float(q[0] / xs[0] ** 4)
    err_pre = abs(c_num / c_teo - 1.0)
    ok_a = err_pot < TOL_POTENCIA and err_pre < TOL_PREFACTOR

    # (b) límite de difracción: promedio sobre el ripple
    xg = np.linspace(300.0, 1200.0, 120)
    qg, _ = mie.qsca_g_mie(xg, M_REL)
    media = float(np.mean(qg))
    err_lim = abs(media / 2.0 - 1.0)
    ok_b = err_lim < TOL_LIMITE

    ev = (f"Rayleigh: pendiente 4 con error {err_pot:.1e}, prefactor {c_num:.6f} vs "
          f"{c_teo:.6f} teórico ({err_pre*100:+.3f}%) | "
          f"difracción: ⟨Q_sca⟩ = {media:.4f} en x∈[300,1200] ({err_lim*100:+.2f}% de 2)")
    return "check 5.1 — límites analíticos de Mie", ok_a and ok_b, ev


if __name__ == "__main__":
    print(run())
