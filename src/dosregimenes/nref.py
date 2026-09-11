"""Índice de refracción del sólido, n_sol(λ).  [Etapa 1/5]

Fuente y procedencia completa: data/refs/n_lambda.md

- Curva: Sultanova, Kasarova & Nikolov (2009), Acta Phys. Pol. A 116, 585.
  Sellmeier (λ en µm):  n² − 1 = 1.124 λ² / (λ² − 0.011087),  válida 0.437–1.052 µm.
- Anclaje 580 nm: Borgmann (2023) §2.2.2, n ≈ 1.47  (coincide con Sultanova: 1.470).
- `bias`: sistemático +0..+0.02 (fracción) hacia el acetato de celulosa (n_D ≈ 1.475–1.49).
"""
from __future__ import annotations

import numpy as np

_A = 1.124
_L2 = 0.011087  # µm²


def n_sol(lam_nm, bias: float = 0.0) -> np.ndarray:
    """Índice de refracción del acetato de celulosa a lam_nm (nm).

    bias: desplazamiento relativo (0 = celulosa de Sultanova; 0.02 ≈ acetato).
    """
    lam_um = np.asarray(lam_nm, float) / 1000.0
    n = np.sqrt(1.0 + _A * lam_um**2 / (lam_um**2 - _L2))
    return n * (1.0 + bias)


def contraste(lam_nm, n_medio: float = 1.0, bias: float = 0.0) -> np.ndarray:
    """m = n_medio / n_sol(λ).  Para poros de aire en el sólido, n_medio = 1."""
    return n_medio / n_sol(lam_nm, bias=bias)


# valores de contraste para la figura de mérito (Borgmann §2.2.1)
N_TIO2 = (2.55, 2.75)   # anatasa, rutilo
N_ZNO = 2.0
N_AIRE = 1.0
