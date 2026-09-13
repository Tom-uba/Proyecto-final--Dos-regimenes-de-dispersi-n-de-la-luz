"""Índice de "telaraña": estructura fina dentro de los poros grandes.  [Etapa 6]

Control de estructura interna (plan, Etapa 6, tarea 4). Portado de la prueba de factibilidad
del eslabón A (sesión del 2026-09-10; el script original quedó fuera del repo), con dos
cambios que se declaran:
  - el banner se detecta (`feret.cargar_gris`) en vez de recortar 60 px fijos;
  - API de scikit-image 0.26 (`max_size = min_size − 1`, ver `feret.segmentar_poros`).

Métrica, por imagen: largo de esqueleto de crestas claras finas (filtro de Sato con
σ = 20, 35, 55 y 80 nm) dentro del interior erosionado de los poros de diámetro equivalente
≥ 0.5 µm, dividido por el área de ese interior  →  µm⁻¹.

NO está calibrada contra anotación manual. Es un índice relativo entre muestras, útil sólo
para ordenarlas. Valores de la prueba de factibilidad (media de 6 imágenes a 20000×):
m1 3.26, m2 3.98, m3 5.24 µm⁻¹.
"""
from __future__ import annotations

import numpy as np

from . import DATA
from . import feret

D_MIN_UM = 0.5
IMAGENES = {
    1: ["gcb8286", "gcb8289", "gcb8292", "gcb8325", "gcb8328", "gcb8331"],
    2: ["gcb8295", "gcb8298", "gcb8301", "gcb8334", "gcb8337", "gcb8340"],
    3: ["gcb8304", "gcb8307", "gcb8310", "gcb8343", "gcb8346", "gcb8349"],
}
FACTIBILIDAD = {1: 3.26, 2: 3.98, 3: 5.24}


def ruta(stem: str):
    hits = sorted((DATA / "sem").glob(f"*/{stem}.tif"))
    if not hits:
        raise FileNotFoundError(stem)
    return hits[0]


def densidad(path) -> float:
    from scipy.ndimage import binary_erosion
    from skimage import exposure, filters
    from skimage.measure import label, regionprops
    from skimage.morphology import disk, remove_small_holes, remove_small_objects, skeletonize

    px = feret.pixel_size_m(path)
    px_nm, px_um = px * 1e9, px * 1e6
    g = exposure.equalize_adapthist(feret.cargar_gris(path), clip_limit=0.02)
    gs = filters.gaussian(g, 1.0)
    dark = gs < filters.threshold_otsu(gs) * 0.92
    dark = remove_small_holes(remove_small_objects(dark, max_size=199), max_size=99)

    lab = label(dark)
    dmin_px = D_MIN_UM * 1e-6 / px
    grandes = [r.label for r in regionprops(lab) if r.equivalent_diameter_area >= dmin_px]
    big = np.isin(lab, grandes)
    core = binary_erosion(big, structure=disk(3))
    if core.sum() <= 200:
        return 0.0

    sig = sorted({max(1, int(round(s / px_nm))) for s in (20, 35, 55, 80)})
    rid = filters.sato(g, sigmas=sig, black_ridges=False)
    rid = rid / (rid.max() + 1e-12)
    fib = (rid > filters.threshold_otsu(rid[core])) & core
    fib = remove_small_objects(fib, max_size=11)
    return float(skeletonize(fib).sum() * px_um / (core.sum() * px_um ** 2))


def por_muestra() -> dict:
    """{muestra: (media, desvío, valores)} sobre las 6 imágenes."""
    out = {}
    for m, stems in IMAGENES.items():
        v = np.array([densidad(ruta(s)) for s in stems])
        out[m] = (float(v.mean()), float(v.std()), v)
    return out
