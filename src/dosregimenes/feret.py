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


def bloque_banner(a: np.ndarray) -> tuple[int, int]:
    """Filas [y0, y1) que ocupa el banner Zeiss: el bloque contiguo de filas oscuras al pie.

    Más preciso que restar BANNER_PX fijo: en estas imágenes el banner ocupa 41 px, no 60,
    y el recorte fijo tiraba 19 filas de imagen útil.

    Dos trampas, las dos encontradas a los golpes:
      - la ÚLTIMA fila del archivo es clara (borde), así que no sirve recorrer desde abajo
        parando en la primera fila no oscura: hay que buscar el bloque oscuro más largo;
      - y por lo mismo el bloque tiene que devolver también su FIN, porque si se recorta
        `a[y0:]` esa fila clara vuelve a entrar y arruina la medición de la barra.
    """
    h = a.shape[0]
    ini = max(0, h - 90)
    oscura = np.median(a[ini:], axis=1) < 0.25
    mejor, blk = (0, h - BANNER_PX, h), None
    for i, v in enumerate(oscura):
        if v and blk is None:
            blk = i
        elif not v and blk is not None:
            if i - blk > mejor[0]:
                mejor = (i - blk, ini + blk, ini + i)
            blk = None
    if blk is not None and len(oscura) - blk > mejor[0]:
        mejor = (len(oscura) - blk, ini + blk, h)
    return (mejor[1], mejor[2]) if mejor[0] > 10 else (h - BANNER_PX, h)


def detectar_banner(a: np.ndarray) -> int:
    """Fila donde empieza el banner Zeiss."""
    return bloque_banner(a)[0]


def medir_barra_escala(path: str | Path, xmax: int = 220) -> int:
    """Largo en píxeles de la barra de escala quemada (tercio izquierdo del banner).

    Se mide como el run horizontal claro más largo dentro del banner. El resultado
    sobreestima ~1 px porque va de borde externo a borde externo y no de centro a
    centro (a 74 px eso es 1.35 %); ver check 3.2.
    """
    a = np.asarray(Image.open(path).convert("L"), float) / 255.0
    y0, y1 = bloque_banner(a)
    ban = a[y0:y1, :xmax]
    mejor = 0
    for thr in (0.30, 0.40, 0.50, 0.60):
        for row in ban > thr:
            d = np.diff(np.concatenate(([0], row.astype(np.int8), [0])))
            ini, fin = np.where(d == 1)[0], np.where(d == -1)[0]
            if len(ini):
                mejor = max(mejor, int((fin - ini).max()))
    return mejor


def cargar_gris(path: str | Path, recortar_banner: bool = True) -> np.ndarray:
    """Imagen en gris [0,1], sin el banner Zeiss ni bordes casi constantes."""
    a = np.asarray(Image.open(path).convert("L"), float) / 255.0
    if recortar_banner:
        a = a[: detectar_banner(a)]
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


# --- espesores (Etapa 3, completado en la Etapa 5) ---------------------------------
# Geometría de los cortes a 3000×: capas verticales piel | núcleo | piel; el espesor se
# mide en x. Historia del método en notas/log.md (v1 → v3):
#   - el ESPESOR TOTAL es robusto: confirma la slide 13 a 1–2 µm en las cuatro muestras;
#   - el NÚCLEO automático sólo es confiable con pieles limpias (m1). En m3 las sombras del
#     relieve de fractura se segmentan como poros y rompen tanto la detección como
#     cualquier criterio de calidad basado en área de poros. Por eso el espesor de núcleo
#     que usa el modelo es el de la slide 13, con ±15 % de incertidumbre.


def run_mas_largo(b: np.ndarray) -> tuple[int, int]:
    """Índices [ini, fin) del tramo contiguo True más largo de un vector booleano."""
    mejor, ini = (0, 0, 0), None
    for i, v in enumerate(np.append(b, False)):
        if v and ini is None:
            ini = i
        elif not v and ini is not None:
            if i - ini > mejor[0]:
                mejor = (i - ini, ini, i)
            ini = None
    return mejor[1], mejor[2]


def extension_lamina(a: np.ndarray) -> tuple[int, int]:
    """Columnas [x0, x1) que ocupa la lámina en un corte a bajo aumento (sin banner).

    Fondo = intensidad extrema (casi negro o casi blanco) o desenfoque fuerte, y SÓLO si
    está pegado al borde del campo: se camina desde cada borde y se para en la primera
    columna que no es fondo. (Un criterio sólo de textura cortaba las pieles lisas.)
    Si x0 ≈ 0 o x1 ≈ ancho, la lámina toca el borde y el total no es medible.
    """
    from scipy.ndimage import gaussian_filter, uniform_filter1d

    W = a.shape[1]
    med = np.median(a, axis=0)
    tex = uniform_filter1d(np.abs(a - gaussian_filter(a, 3.0)).mean(axis=0), 15)
    ref = np.median(tex[W // 3: 2 * W // 3])
    fondo = (med < 0.12) | (med > 0.90) | (tex < 0.15 * ref)
    x0 = 0
    while x0 < W and fondo[x0]:
        x0 += 1
    x1 = W
    while x1 > x0 and fondo[x1 - 1]:
        x1 -= 1
    return x0, x1


def espesor_total_um(path: str | Path) -> tuple[float, bool]:
    """(espesor total en µm, válido). Válido = la lámina no toca el borde del campo."""
    px = pixel_size_m(path)
    a = np.asarray(Image.open(path).convert("L"), float) / 255.0
    a = a[: detectar_banner(a)]
    x0, x1 = extension_lamina(a)
    return (x1 - x0) * px * 1e6, not (x0 <= 2 or x1 >= a.shape[1] - 2)
