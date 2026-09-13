"""check 6.3 — el contraste predicho lo carga el tamaño de poro, no el entorno (φ, L).

PRE-REGISTRADO (notas/log.md, 2026-09-13 g). Cálculo en `controles.atribucion`.

Las muestras 1–3 y 4 no difieren sólo en D: la 4 tiene más porosidad (0.33 contra ~0.20)
y menos espesor de núcleo (32 contra ~42 µm). Diseño factorial 2×2 dentro del modelo:
P(D) ∈ {1–3 agrupadas, 4} × entorno (φ, L) ∈ {1–3, 4}. Se reparte el contraste predicho
Δs rojo entre los dos factores promediando el efecto de cada uno sobre los dos niveles del
otro (f_D + f_env = 1).

CRITERIO: f_D ≥ 0.75 con los DOS cierres de factor de estructura (monodisperso y desacople),
es decir, al menos tres cuartos del contraste espectral predicho vienen del cambio de
régimen y no de la porosidad o el espesor.
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from dosregimenes import controles as ct  # noqa: E402

UMBRAL = 0.75


def run():
    res = ct.atribucion()
    ok = all(v["f_D"] >= UMBRAL for v in res.values())
    ev = " | ".join(f"{k}: Δs total {v['total']:.2f}, f_D {v['f_D']:.2f}, f_env {v['f_env']:.2f}"
                    for k, v in res.items()) + f" (criterio f_D ≥ {UMBRAL})"
    return "check 6.3 — atribución del contraste: tamaño vs entorno", bool(ok), ev


if __name__ == "__main__":
    print(run())
