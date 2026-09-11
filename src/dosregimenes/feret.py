"""Distribución de tamaño de poro P(D) desde las SEM.  [Etapa 3]

Pipeline (probado en la fase de factibilidad, ver notas/log.md):
  1. tamaño de píxel exacto desde la metadata Zeiss (tag TIFF 34118), NO la barra quemada.
  2. recorte del banner inferior (~60 px) y de bordes casi constantes.
  3. segmentación de poros (oscuro): Otsu + filtro de tamaño.
  4. diámetro de Feret por poro (regionprops).

Validación (check 3.1): media de P(D) ≈ 1.6 µm (muestras 1–3), ≈ 0.1 µm (muestra 4),
dentro de ±10 % de los valores del informe.
Validación (check 3.2): px del tag vs. barra de escala medida, < 2 %.

Muestra 4: red bicontinua nanométrica -> "diámetro de poro" es una longitud característica
de la malla; se caracteriza aparte (ancho de ligamento / superficie específica).

TODO Etapa 3: conjunto de anotación manual (5 imágenes, 2 anotadores) para calibrar el
umbral y cuantificar el sesgo (Bland-Altman).
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
from PIL import Image

BANNER_PX = 60

# --- perillas libres de la segmentación -------------------------------------
# Estos cuatro valores NO salen de ninguna medición: se eligieron a ojo en la fase de
# factibilidad. El diámetro medido depende de ellos, así que hasta que el conjunto de
# anotación manual los calibre (Etapa 3), todo D que salga de acá es "D dado este umbral".
FACTOR_OTSU = 0.92        # multiplica el umbral de Otsu: <1 agranda los poros
CLIP_LIMIT = 0.02         # realce de contraste local (CLAHE)
SIGMA_SUAVIZADO = 1.0     # px, gaussiana previa al umbralado
D_MIN_UM_DEFECTO = 0.15   # µm, poros más chicos se descartan como ruido


def pixel_size_m(path: str | Path) -> float | None:
    """Tamaño de píxel en metros, del tag Zeiss 34118 (primer float)."""
    im = Image.open(path)
    raw = getattr(im, "tag_v2", {}).get(34118) or getattr(im, "tag_v2", {}).get(34119)
    if isinstance(raw, str):
        nums = re.findall(r"[-+]?\d\.\d{6}e[-+]\d{2}", raw)
        if nums:
            return float(nums[0])
    return None


def cargar_gris(path: str | Path, recortar_banner: bool = True) -> np.ndarray:
    """Imagen en gris [0,1], sin el banner Zeiss ni bordes casi constantes."""
    a = np.asarray(Image.open(path).convert("L"), float) / 255.0
    if recortar_banner:
        a = a[: a.shape[0] - BANNER_PX]
    cs, rs = a.std(0), a.std(1)
    x0 = int(np.argmax(cs > 0.02))
    x1 = a.shape[1] - int(np.argmax(cs[::-1] > 0.02))
    y0 = int(np.argmax(rs > 0.02))
    y1 = a.shape[0] - int(np.argmax(rs[::-1] > 0.02))
    return a[y0:y1, x0:x1]


def segmentar_poros(gris: np.ndarray, px_m: float, d_min_um: float = D_MIN_UM_DEFECTO):
    """Máscara booleana de poros (regiones oscuras) por Otsu + filtro de tamaño."""
    from skimage import exposure, filters
    from skimage.morphology import remove_small_holes, remove_small_objects

    g = exposure.equalize_adapthist(gris, clip_limit=CLIP_LIMIT)
    gs = filters.gaussian(g, SIGMA_SUAVIZADO)
    dark = gs < filters.threshold_otsu(gs) * FACTOR_OTSU
    min_px = max(64, int((d_min_um * 1e-6 / px_m) ** 2))
    # skimage >= 0.26: max_size elimina objetos de area <= valor; el min_size viejo
    # eliminaba area < valor. Se resta 1 para conservar el comportamiento.
    dark = remove_small_objects(dark, max_size=min_px - 1)
    dark = remove_small_holes(dark, max_size=min_px // 2 - 1)
    return dark


def feret_poros(mask: np.ndarray, px_m: float) -> np.ndarray:
    """Diámetro de Feret (µm) de cada poro de la máscara."""
    from skimage.measure import label, regionprops

    return np.array([r.feret_diameter_max * px_m * 1e6
                     for r in regionprops(label(mask))])


def PD_de_imagen(path: str | Path) -> np.ndarray:
    """Feret (µm) de todos los poros de una imagen SEM."""
    px = pixel_size_m(path)
    if px is None:
        raise ValueError(f"sin escala en metadata: {path}")
    g = cargar_gris(path)
    return feret_poros(segmentar_poros(g, px), px)
