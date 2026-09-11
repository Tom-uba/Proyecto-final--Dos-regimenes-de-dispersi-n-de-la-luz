"""Lectura de las tablas de ImageJ del Labo 6.  [Etapa 3]

Éstas son la medición PRIMARIA de P(D): las produjo el pipeline de Fiji/ImageJ del
trabajo original, que separa poros individuales mucho mejor que la segmentación rápida de
`feret.py` (circularidad media 0.86, solidez 0.89 contra manchones fusionados).
`feret.py` queda como segunda implementación independiente para el check 3.1.

Procedencia y detalle: data/PROCEDENCIA.md §4bis.

Archivos en data/imagej/:
    poros_m1a3_limpios.csv        11437 poros, 54 imágenes (m1–3 × 2 mitades × 3 zonas × 3 zooms)
    resumen_por_imagen_m1a3.csv   una fila por imagen, con Muestra/Orientacion/Zona/Zoom
    poros_m4_z4.csv                9365 poros, 6 imágenes de la muestra 4 a 50000×
    resumen_por_imagen_m4_z4.csv   resumen de esas 6
    v1_*                           versión anterior del análisis (18/06), con nombres gcb####

Nomenclatura de las etiquetas: `<muestra><mitad>-<zona>-Z<zoom>.tif`
    mitad: U = arriba, D = abajo
    zona:  U / C / D  (las tres regiones medidas en cada mitad)
    zoom:  Z1 = 3000×, Z2 = 8000×, Z3 = 20000×, Z4 = 50000×
El rótulo "4000×" que aparece en el informe y en los nombres de carpeta es un error: la
metadata del instrumento dice 3000× (ver data/sem/MANIFEST.csv).
"""
from __future__ import annotations

import csv
import re
from dataclasses import dataclass

import numpy as np

from . import DATA

ZOOM_A_AUMENTO = {"Z1": 3000, "Z2": 8000, "Z3": 20000, "Z4": 50000}
_RE_LABEL = re.compile(r"^(\d)([UD])-([UCD])-(Z\d)", re.I)


@dataclass
class Poro:
    muestra: int
    mitad: str      # "arriba" | "abajo"
    zona: str       # "U" | "C" | "D"
    zoom: str       # "Z1".."Z4"
    feret: float    # µm  (Feret máximo)
    min_feret: float
    area: float     # µm²
    circ: float
    solidez: float


def _leer(nombre: str) -> list[dict]:
    with open(DATA / "imagej" / nombre, encoding="latin-1") as f:
        return list(csv.DictReader(f))


def _parse(label: str):
    m = _RE_LABEL.match(label.strip())
    if not m:
        return None
    return (int(m.group(1)), "arriba" if m.group(2).upper() == "U" else "abajo",
            m.group(3).upper(), m.group(4).upper())


def cargar_poros(incluir_m4: bool = True) -> list[Poro]:
    """Todos los poros, de las dos tablas, con su etiqueta decodificada."""
    out: list[Poro] = []
    fuentes = ["poros_m1a3_limpios.csv"] + (["poros_m4_z4.csv"] if incluir_m4 else [])
    for nombre in fuentes:
        for r in _leer(nombre):
            p = _parse(r.get("Label", ""))
            if p is None:
                continue
            try:
                out.append(Poro(muestra=p[0], mitad=p[1], zona=p[2], zoom=p[3],
                                feret=float(r["Feret"]), min_feret=float(r["MinFeret"]),
                                area=float(r["Area"]), circ=float(r["Circ."]),
                                solidez=float(r["Solidity"])))
            except (KeyError, ValueError):
                continue
    return out


def PD(muestra: int, zoom: str | None = None, solo_arriba: bool = False,
       poros: list[Poro] | None = None) -> np.ndarray:
    """Distribución de Feret (µm) de una muestra.

    zoom=None usa el aumento nativo de cada muestra: Z1 (3000×) para las micrométricas
    1–3 y Z4 (50000×) para la nanométrica 4, que es donde cada una está bien resuelta.
    solo_arriba descarta las mitades `abajo`, que tienen daño de corte (ver data/sem/README).
    """
    poros = cargar_poros() if poros is None else poros
    if zoom is None:
        zoom = "Z4" if muestra == 4 else "Z1"
    sel = [p.feret for p in poros
           if p.muestra == muestra and p.zoom == zoom
           and (not solo_arriba or p.mitad == "arriba")]
    return np.asarray(sel)


def resumen(D: np.ndarray) -> dict[str, float]:
    """Media, mediana, moda (pico de KDE) y percentiles de una distribución."""
    from scipy.stats import gaussian_kde

    if len(D) < 20:
        return dict(n=len(D), media=float("nan"), mediana=float("nan"),
                    moda=float("nan"), p10=float("nan"), p90=float("nan"))
    xs = np.linspace(D.min(), np.percentile(D, 99), 600)
    moda = float(xs[np.argmax(gaussian_kde(D)(xs))])
    return dict(n=len(D), media=float(D.mean()), mediana=float(np.median(D)),
                moda=moda, p10=float(np.percentile(D, 10)),
                p90=float(np.percentile(D, 90)))
