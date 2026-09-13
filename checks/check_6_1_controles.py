"""check 6.1 — controles: ni el espesor ni la absorción generan el contraste espectral.

PRE-REGISTRADO: criterios commiteados antes de la primera ejecución (notas/log.md,
2026-09-13 g). Cálculo en `dosregimenes.controles`.

(a) ESPESOR. Modelo nominal = el del check 5.2 (PY monodisperso, η = φ). Se recalcula
    Δs_pred rojo con los espesores de núcleo alterados y las mismas semillas (números
    aleatorios comunes, para que la diferencia no sea ruido del Monte Carlo):
        todos ×1.15 · todos ×0.85 · m4 ×1.15 y m1–3 ×0.85 · m4 ×0.85 y m1–3 ×1.15 ·
        intercambio (m4 con la media de 1–3, 42.3 µm; m1–3 con 32 µm)
    Número: máx |Δs(variante) − Δs(nominal)|.
    CRITERIO: < 0.25 · Δs_medido.

(b) ABSORCIÓN. Hipótesis alternativa H_abs: la caída de R de m4 hacia el rojo la produce
    absorción del sólido y no el régimen de dispersión.
    - Dispersión de m4 congelada en su valor a 600 nm (espectralmente plana) + absorción
      μ_a,sol(λ) = κ·(λ−600)/145 (cero en 600 nm: la mínima que hace caer R hacia el rojo).
      κ* = el que da s₄ = s₄ medida.
    - La MISMA absorción del sólido, aplicada a las cuatro muestras (m1–3 con su modelo
      nominal), predice un observable que no depende de la calibración absoluta de R:
          X = (1−T)/R      K(λ) = X₄ / ⟨X_m⟩₁₂₃      Q = K(745)/K(600)
      Sin absorción X = 1 exactamente y Q = 1. Un factor multiplicativo común del patrón
      blanco (el sospechoso del R+T > 1) se cancela en K.
    - Medido: R (5 regiones) y T de tira A, en ventanas 595–605 y 735–745 nm.
      σ_Q = √(σ_est² + (Q_A − Q_B)²): σ_est por el desvío entre regiones de R (error
      estándar), y Q_B el mismo cálculo con la T de tira B (misma fabricación).
    - Se hace con los dos cierres de factor de estructura y se toma el Q_pred MÁS CHICO
      (el que menos le exige a los datos).
    CRITERIO: H_abs excluida si  Q_medido < Q_pred,mín − 3 σ_Q.  Si ni κ = 0.1 µm⁻¹
    (1000 cm⁻¹) alcanza para producir s₄, H_abs cuenta como excluida (se reporta).
    Informativo: κ* en cm⁻¹ y cuánto subiría s̄₁₂₃ con esa absorción.
    Supuesto declarado: la R medida se compara con R_total del modelo (con especular).

PASA si (a) y (b).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from dosregimenes import controles as ct  # noqa: E402
from dosregimenes import imagej as ij  # noqa: E402

FRAC_ESPESOR = 0.25
N_SIGMA = 3.0


def run():
    poros = ij.cargar_poros()
    ds_med = ct.ds_medido()

    esp = ct.control_espesor(poros)
    ds0 = esp["nominal"]["ds"]
    desv = {k: v["ds"] - ds0 for k, v in esp.items() if k != "nominal"}
    peor = max(desv, key=lambda k: abs(desv[k]))
    ok_a = abs(desv[peor]) < FRAC_ESPESOR * ds_med

    ab = ct.control_absorcion(poros)
    QA, s_est = ct.Q_medido("A")
    QB, _ = ct.Q_medido("B")
    sQ = float(np.hypot(s_est, QA - QB))
    Qp = min(v["Q_pred"] for v in ab.values())
    ok_b = all(not v["alcanza"] for v in ab.values()) or (QA < Qp - N_SIGMA * sQ)

    ev = (f"(a) Δs nominal {ds0:.2f}; peor variante '{peor}' {desv[peor]:+.2f} "
          f"(|·| < {FRAC_ESPESOR * ds_med:.2f}) → {ok_a} | "
          f"(b) Q medido {QA:.3f} ± {sQ:.3f} (tira B {QB:.3f}) vs H_abs: " +
          ", ".join(f"{k} Q {v['Q_pred']:.3f} (κ* {v['kappa_cm']:.0f} cm⁻¹, A₄(745) "
                    f"{v['A4_745']:.2f}, Δs̄₁₂₃ {v['ds123_inducido']:+.2f})"
                    for k, v in ab.items()) +
          f"; separación {(Qp - QA) / sQ:.1f}σ → {ok_b}")
    return "check 6.1 — controles de espesor y absorción", bool(ok_a and ok_b), ev


if __name__ == "__main__":
    print(run())
