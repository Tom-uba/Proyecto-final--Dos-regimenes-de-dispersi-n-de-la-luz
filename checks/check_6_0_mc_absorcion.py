"""check 6.0 — la absorción por peso de camino del Monte Carlo es correcta.

Valida la IMPLEMENTACIÓN que usa el control de absorción del check 6.1.

  (a) Límite balístico con absorción (ℓ* → ∞, incidencia normal, a = exp(−μ_a L)). Las
      reflexiones múltiples entre las dos caras dan exactamente
          R_total = R₀ + (1−R₀)² R₀ a² / (1 − R₀² a²)
          T       = (1−R₀)² a / (1 − R₀² a²)
      con μ_a·L = 0, 0.4 y 1.2. Criterio: ±0.003 (2·10⁵ fotones).
  (b) Pedir absorción no altera la corrida (no consume números aleatorios) y μ_a = 0
      reproduce las fracciones sin absorción: diferencia < 1e-12 con ℓ* finito.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from dosregimenes import montecarlo as mc  # noqa: E402

N_EF = 1.389
TOL = 0.003


def run():
    L = 40.0
    mu = np.array([0.0, 0.01, 0.03])
    bal = mc.correr(1e9, 0.0, N_EF, L, n_fotones=200000, seed=1, mu_a=mu)
    R0 = bal["R0"]
    a = np.exp(-mu * L)
    R_ex = R0 + (1 - R0) ** 2 * R0 * a ** 2 / (1 - R0 ** 2 * a ** 2)
    T_ex = (1 - R0) ** 2 * a / (1 - R0 ** 2 * a ** 2)
    err_a = float(max(np.abs(bal["R_total_abs"] - R_ex).max(), np.abs(bal["T_abs"] - T_ex).max()))

    d1 = mc.correr(8.0, 0.6, N_EF, L, n_fotones=20000, seed=4)
    d2 = mc.correr(8.0, 0.6, N_EF, L, n_fotones=20000, seed=4, mu_a=[0.0, 0.002])
    err_b = max(abs(d1["R_total"] - d2["R_total"]), abs(d1["T"] - d2["T"]),
                abs(d2["R_total_abs"][0] - d2["R_total"]), abs(d2["T_abs"][0] - d2["T"]))
    A = 1 - d2["R_total_abs"][1] - d2["T_abs"][1]

    ok = err_a < TOL and err_b < 1e-12
    ev = (f"balístico con absorción (μL = 0, 0.4, 1.2): máx error {err_a:.4f} (<{TOL}) | "
          f"μ_a = 0 y misma corrida: diferencia {err_b:.1e} | "
          f"informativo: A = {A:.3f} con μ_a = 0.002 µm⁻¹, L/ℓ* = 5")
    return "check 6.0 — absorción en el Monte Carlo", bool(ok), ev


if __name__ == "__main__":
    print(run())
