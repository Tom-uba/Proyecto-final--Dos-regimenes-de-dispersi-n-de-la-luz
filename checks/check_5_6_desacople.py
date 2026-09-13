"""check 5.6 — la aproximación de desacople cumple sus límites exactos.

Valida la IMPLEMENTACIÓN, no la hipótesis física (eso es el check 5.7). Límites:

  (a) poros todos iguales → β(q) = 1 para todo q, y S_ef = S_PY monodisperso.
  (b) q → 0 → β(0) = ⟨D³⟩² / ⟨D⁶⟩  (F(0) ∝ volumen). Se compara con el valor calculado
      directamente de la muestra de tamaños, sobre una P(D) lognormal con desvío relativo 32 %.
  (c) 0 < β(q) ≤ 1 para todo q (desigualdad de Cauchy–Schwarz).
  (d) S_ef(q) → 1 a q grande.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from dosregimenes import estructura as es  # noqa: E402

ETA = 0.33
TOL = 0.02


def run():
    q = np.linspace(1e-3, 60.0, 300)

    iguales = np.full(1000, 0.30)
    b_ig = es.beta_desacople(iguales, q)
    s_ig = es.S_desacople(q, iguales, ETA)
    s_mono = es.S_py(q * 0.30, ETA)
    err_a = max(float(np.max(np.abs(b_ig - 1))), float(np.max(np.abs(s_ig - s_mono))))

    s2 = np.log(1 + 0.32 ** 2)
    D = np.random.default_rng(5).lognormal(np.log(0.3) - s2 / 2, np.sqrt(s2), 200000)
    Dc, w = es._histograma_D(D)
    b0_exacto = float((w @ Dc ** 3) ** 2 / (w @ Dc ** 6))
    b0_num = float(es.beta_desacople(D, [1e-4])[0])
    err_b = abs(b0_num / b0_exacto - 1)

    b = es.beta_desacople(D, q)
    ok_c = bool(np.all(b > 0) and np.all(b <= 1 + 1e-9))

    s_inf = es.S_desacople(np.linspace(200.0, 400.0, 40), D, ETA)
    err_d = float(np.max(np.abs(s_inf - 1)))

    ok = err_a < TOL and err_b < TOL and ok_c and err_d < TOL
    ev = (f"iguales: |β−1|,|S_ef−S_PY| ≤ {err_a:.1e} | β(0) = {b0_num:.4f} vs "
          f"⟨D³⟩²/⟨D⁶⟩ = {b0_exacto:.4f} ({err_b*100:+.2f}%) | 0<β≤1: {ok_c} "
          f"(mín {b.min():.3f}) | |S_ef(q→∞)−1| ≤ {err_d:.3f}")
    return "check 5.6 — límites de la aproximación de desacople", ok, ev


if __name__ == "__main__":
    print(run())
