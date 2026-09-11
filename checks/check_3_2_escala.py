"""check 3.2 — la escala de la metadata coincide con la barra quemada en el banner.

Toda la morfometría cuelga del tamaño de píxel que se lee del tag TIFF Zeiss 34118. Si ese
número estuviera mal, D estaría mal y x = πD/λ también. La barra de escala dibujada en el
banner es una referencia independiente: la pone el instrumento, no el análisis.

Criterio: |barra_medida / rótulo − 1| < 2 % en las cuatro magnificaciones.

Se espera un sesgo POSITIVO de ~1 px: el largo se mide como run de borde externo a borde
externo, no de centro a centro. A 74 px eso son 1.35 %, y es lo que se observa.
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from dosregimenes import DATA  # noqa: E402
from dosregimenes import feret  # noqa: E402

# (carpeta, archivo, rótulo impreso en el banner, nm)
CASOS = [
    ("1 arriba", "gcb8284", "10 µm", 10000.0),
    ("1 arriba", "gcb8285", "2 µm", 2000.0),
    ("1 arriba", "gcb8286", "1 µm", 1000.0),
    ("3 arriba", "gcb8310", "1 µm", 1000.0),
    ("4 arriba", "gcb8322", "400 nm", 400.0),
]
TOL = 0.02


def run():
    peor, desc, ok = 0.0, "", True
    for carpeta, stem, rotulo, esperado_nm in CASOS:
        p = DATA / "sem" / carpeta / f"{stem}.tif"
        px_nm = feret.pixel_size_m(p) * 1e9
        largo_px = feret.medir_barra_escala(p)
        medido = largo_px * px_nm
        rel = medido / esperado_nm - 1.0
        if abs(rel) > TOL:
            ok = False
        if abs(rel) > abs(peor):
            peor, desc = rel, f"{stem} ({rotulo})"
    return ("check 3.2 — escala: tag TIFF vs barra quemada", ok,
            f"{len(CASOS)} magnificaciones, peor desvío {peor*100:+.1f}% en {desc} "
            f"(tolerancia ±{TOL*100:.0f}%)")


if __name__ == "__main__":
    print(run())
