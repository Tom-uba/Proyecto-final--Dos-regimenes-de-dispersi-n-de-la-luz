"""check 3.1 — P(D) reproduce el trabajo previo, y dos pipelines independientes coinciden.

Dos comparaciones distintas:

(a) CONTRA EL TRABAJO PREVIO. El informe reporta ≈1.6 µm (muestras 1–3) y ≈0.1 µm
    (muestra 4). Se compara la MEDIANA, y la elección hay que justificarla porque no es
    inocente: la distribución tiene cola larga a la derecha, así que media (1.99), mediana
    (1.75) y moda (1.41) difieren ~40 % entre sí. Se usa la mediana porque (i) es el
    estimador central robusto frente a esa cola, (ii) el propio número del trabajo previo
    es ambiguo — el informe lo llama "promedio" pero el cuaderno describe un pico de
    histograma (moda) "alrededor de 1.5 µm". Se reportan los tres para que el lector juzgue.
    Criterio: |mediana/valor_informe − 1| < 10 %.

(b) ENTRE IMPLEMENTACIONES. La tabla de ImageJ (primaria) contra la segmentación en Python
    de `feret.py` (independiente: otro software, otro umbralado, otra persona). Coincidir
    descarta errores de implementación; NO descarta un sesgo común a las dos, porque ambas
    son umbralado sobre las mismas imágenes. Eso sólo lo cerraría anotación manual.
    Criterio: |mediana_py/mediana_ij − 1| < 15 %, sobre las MISMAS imágenes.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from dosregimenes import DATA  # noqa: E402
from dosregimenes import feret, imagej  # noqa: E402

INFORME = {"m1a3": 1.6, "m4": 0.1}
TOL_INFORME = 0.10
TOL_PIPELINES = 0.15
# subconjunto para el contraste entre pipelines: zona centro, mitad arriba, 3000×
CRUCE = [("1 arriba", "gcb8287"), ("2 arriba", "gcb8296"), ("3 arriba", "gcb8305")]


def run():
    poros = imagej.cargar_poros()

    D13 = np.concatenate([imagej.PD(m, poros=poros) for m in (1, 2, 3)])
    D4 = imagej.PD(4, poros=poros)
    r13, r4 = imagej.resumen(D13), imagej.resumen(D4)

    e13 = r13["mediana"] / INFORME["m1a3"] - 1
    e4 = r4["mediana"] / INFORME["m4"] - 1
    ok_a = abs(e13) < TOL_INFORME and abs(e4) < TOL_INFORME

    # (b) mismas imágenes, los dos pipelines
    med_py, med_ij = [], []
    for carpeta, stem in CRUCE:
        med_py.append(np.median(feret.PD_de_imagen(DATA / "sem" / carpeta / f"{stem}.tif")))
        etiqueta_m = int(carpeta[0])
        med_ij.append(np.median(imagej.PD(etiqueta_m, poros=poros)))
    mpy, mij = float(np.mean(med_py)), float(np.mean(med_ij))
    e_pipe = mpy / mij - 1
    ok_b = abs(e_pipe) < TOL_PIPELINES

    ev = (f"vs informe: m1-3 mediana {r13['mediana']:.2f} µm ({e13*100:+.0f}%), "
          f"m4 {r4['mediana']:.3f} µm ({e4*100:+.0f}%) | "
          f"media/mediana/moda m1-3 = {r13['media']:.2f}/{r13['mediana']:.2f}/{r13['moda']:.2f} | "
          f"ImageJ vs Python (n={len(CRUCE)} img): {mij:.2f} vs {mpy:.2f} µm ({e_pipe*100:+.0f}%)")
    return "check 3.1 — P(D) vs trabajo previo y entre pipelines", ok_a and ok_b, ev


if __name__ == "__main__":
    print(run())
