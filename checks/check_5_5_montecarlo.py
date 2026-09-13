"""check 5.5 — el Monte Carlo reproduce un límite exacto y la difusión donde ésta vale.

El Monte Carlo es la herramienta que va a decidir las muestras 1–3, donde la difusión no
aplica. Por eso se lo valida contra dos referencias que no dependen de él:

  (a) LÍMITE BALÍSTICO, ℓ* → ∞ (sin dispersión). Sólo actúan las dos interfaces, y la
      suma de reflexiones múltiples entre ellas da exactamente
          R = 2R₀/(1+R₀)      T = (1−R₀)/(1+R₀)      R₀ = ((n−1)/(n+1))²
      Criterio: |ΔR|, |ΔT| < 0.003 (≈6 σ estadísticos con 2·10⁵ fotones).

  (b) RÉGIMEN GRUESO, L/ℓ* = 15. La difusión con bordes extrapolados (lamina.py) debería
      valer. Se compara T, que es la cantidad más limpia: la del Monte Carlo contra
      (1−R₀)·T_difusión (el factor da cuenta de la especular de entrada, que la fórmula de
      difusión no incluye). Criterio a priori: diferencia relativa < 10 %.

  (c) CONTEO: sin absorción todo fotón sale; fracción sin escapar < 10⁻³.
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from dosregimenes import lamina as lm  # noqa: E402
from dosregimenes import montecarlo as mc  # noqa: E402

N_EF = 1.389          # índice efectivo de las muestras 1–3 (φ = 0.20)
TOL_BAL = 0.003
TOL_DIF = 0.10
TOL_ESC = 1e-3


def run():
    # (a) balístico
    L = 40.0
    bal = mc.correr(ell_star_um=1e9, g=0.0, n_ef=N_EF, d_um=L, n_fotones=200000, seed=1)
    R0 = bal["R0"]
    R_exa, T_exa = 2 * R0 / (1 + R0), (1 - R0) / (1 + R0)
    dR, dT = abs(bal["R_total"] - R_exa), abs(bal["T"] - T_exa)
    ok_a = dR < TOL_BAL and dT < TOL_BAL

    # (b) grueso: L/ℓ* = 15, g = 0.5 para que corra rápido
    ell = L / 15.0
    gru = mc.correr(ell_star_um=ell, g=0.5, n_ef=N_EF, d_um=L, n_fotones=20000, seed=2)
    T_dif = 1.0 - float(lm.R_difusion(L, ell, N_EF))
    T_ref = (1 - R0) * T_dif
    rel = gru["T"] / T_ref - 1.0
    ok_b = abs(rel) < TOL_DIF

    ok_c = bal["sin_escapar"] < TOL_ESC and gru["sin_escapar"] < TOL_ESC

    ev = (f"balístico: R={bal['R_total']:.4f} vs {R_exa:.4f}, T={bal['T']:.4f} vs {T_exa:.4f} | "
          f"L/ℓ*=15: T_MC={gru['T']:.4f} vs difusión {T_ref:.4f} ({rel*100:+.1f}%) | "
          f"sin escapar {max(bal['sin_escapar'], gru['sin_escapar']):.1e}")
    return "check 5.5 — Monte Carlo vs límite exacto y difusión", ok_a and ok_b and ok_c, ev


if __name__ == "__main__":
    print(run())
