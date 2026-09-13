"""Tabla y figura de diagnóstico: espesores total y de núcleo desde las SEM a 3000×.  [Etapa 3b]

RESULTADO:   resultados/03b_espesores.csv + figures/03b_espesores_diag.png
ENTRADA:     data/sem/<muestra> <mitad>/*.tif a 3000× (24 imágenes, via MANIFEST.csv)
CÁLCULO:     dosregimenes.feret.extension_lamina (total), feret.segmentar_poros (núcleo)
DERIVADO vs LIBRERÍA:  detección de bordes y del núcleo propia; scipy sólo para filtros.
ELECCIONES:  (historia completa v1→v3 en notas/log.md, 2026-09-13)
             - total: fondo = intensidad extrema o desenfoque pegado al borde del campo;
               una imagen vale sólo si la lámina no toca el borde.
             - núcleo: fracción de poro por columna suavizada 8 µm; umbral a 40 % entre el
               nivel de las pieles (6 µm junto a cada borde) y la meseta (percentil 90);
               aceptado sólo si captura ≥ 70 % del área de poros de la lámina.
             - el núcleo automático NO se usa en el modelo: falla con pieles fracturadas
               (m3) y no resuelve los poros de m4 a 3000×. El modelo usa la slide 13 ±15 %.
CHECK:       checks/check_3_3_espesores.py (sólo el total, que es robusto)
INCERTIDUMBRE:  total: rango entre imágenes válidas (~1–6 µm). Núcleo: ver log.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import uniform_filter1d

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from dosregimenes import DATA, FIGURES  # noqa: E402
from dosregimenes import feret  # noqa: E402

RESULTADOS = RAIZ / "resultados"
MIN_CAPTURADO = 0.70


def main() -> None:
    with open(DATA / "sem" / "MANIFEST.csv", encoding="utf-8") as f:
        imgs = [r for r in csv.DictReader(f) if int(r["aumento_x"]) == 3000]

    filas, tiles = [], []
    for r in imgs:
        p = DATA / "sem" / r["carpeta"] / r["archivo"]
        m = int(r["muestra"])
        px_m = feret.pixel_size_m(p)
        um = px_m * 1e6
        a = np.asarray(Image.open(p).convert("L"), float) / 255.0
        a = a[: feret.detectar_banner(a)]
        W = a.shape[1]
        x0, x1 = feret.extension_lamina(a)
        total_ok = not (x0 <= 2 or x1 >= W - 2)

        nucleo, capt, c0, c1 = float("nan"), float("nan"), None, None
        if m != 4 and x1 - x0 > 100:
            fr = feret.segmentar_poros(a, px_m).mean(axis=0).astype(float)
            frs = uniform_filter1d(fr, max(3, int(round(8.0 / um))))
            k = max(3, int(round(6.0 / um)))
            base = float(np.median(np.r_[frs[x0:x0 + k], frs[x1 - k:x1]]))
            meseta = float(np.percentile(frs[x0:x1], 90))
            dentro = np.zeros(W, bool)
            dentro[x0:x1] = True
            c0, c1 = feret.run_mas_largo(dentro & (frs > base + 0.4 * (meseta - base)))
            tot = fr[x0:x1].sum()
            capt = float(fr[c0:c1].sum() / tot) if tot > 0 else 0.0
            nucleo = (c1 - c0) * um
        nucleo_ok = bool(np.isfinite(capt) and capt >= MIN_CAPTURADO)

        filas.append(dict(muestra=m, mitad=r["mitad"], archivo=r["archivo"],
                          total_um=round((x1 - x0) * um, 1), total_ok=total_ok,
                          nucleo_um=round(nucleo, 1), capturado=round(capt, 3),
                          nucleo_ok=nucleo_ok))

        t = Image.fromarray((a * 255).astype(np.uint8)).convert("RGB")
        d = ImageDraw.Draw(t)
        for x in (x0, max(x1 - 1, 0)):
            d.line([(x, 0), (x, a.shape[0])],
                   fill=(255, 60, 60) if total_ok else (255, 200, 0), width=6)
        if c0 is not None:
            for x in (c0, max(c1 - 1, 0)):
                d.line([(x, 0), (x, a.shape[0])],
                       fill=(0, 220, 255) if nucleo_ok else (255, 0, 255), width=6)
        tiles.append(t.resize((256, int(a.shape[0] * 256 / W))))

    orden = sorted(range(len(filas)),
                   key=lambda i: (filas[i]["muestra"], filas[i]["mitad"], filas[i]["archivo"]))
    h = max(t.size[1] for t in tiles)
    grid = Image.new("RGB", (256 * 6, h * 4), (0, 0, 0))
    for k, i in enumerate(orden):
        grid.paste(tiles[i], ((k % 6) * 256, (k // 6) * h))
    FIGURES.mkdir(exist_ok=True)
    grid.save(FIGURES / "03b_espesores_diag.png")

    RESULTADOS.mkdir(exist_ok=True)
    with open(RESULTADOS / "03b_espesores.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows([filas[i] for i in orden])

    res = []
    for m in (1, 2, 3, 4):
        tv = [x["total_um"] for x in filas if x["muestra"] == m and x["total_ok"]]
        res.append(f"m{m} total {np.median(tv):.1f} µm" if tv else f"m{m} total -")
    print("03b_espesores: " + ", ".join(res) +
          "  |  núcleo automático sólo confiable en m1 (ver log); el modelo usa slide 13 ±15 %")


if __name__ == "__main__":
    main()
