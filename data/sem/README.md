# SEM — 78 imágenes

Los `.tif` **no están versionados** (67 MB, ~874 KB c/u). Este directorio versiona solo
`MANIFEST.csv`.

## Origen

Zeiss GeminiSEM 560, Centro de Microscopía Avanzada (CMA, UBA). Sesión 11/06/2026.
Cortes transversales de la tira A de acetato de celulosa, crio-fracturados en N₂ líquido
y metalizados. 4 muestras, cada una cortada al medio → mitades `arriba` y `abajo`.
Detalle en `../PROCEDENCIA.md` §4.

Ubicación original en la máquina donde se trabajó:
`…/Labo 6/Imagenes del microscopio/26 06 11-Tomas Chamorro/`
con 8 subcarpetas `<muestra> <mitad>` (`1 arriba`, `1 abajo`, …, `4 abajo`).

## Obtenerlas

Copiar las 8 subcarpetas dentro de este directorio, conservando los nombres:

```
data/sem/
  1 arriba/  gcb8284.tif …
  1 abajo/   …
  …
  4 abajo/   …
```

`MANIFEST.csv` lista cada archivo con: `carpeta, muestra, mitad, aumento_x, px_nm,
fov_um, eht_kv, wd_mm`. El tamaño de píxel (`px_nm`) sale de la metadata Zeiss embebida
(tag TIFF 34118) y es la escala de referencia — no depende de la barra quemada.

## Resumen

| | muestras 1–3 | muestra 4 |
|---|---|---|
| imágenes por mitad | 9 = 3 regiones × 3 aumentos | 12 = 3 regiones × 4 aumentos |
| aumentos | 3000× / 8000× / 20000× | + 50000× |
| px_nm | 91.80 / 34.42 / 13.77 | + 5.51 |

Banner Zeiss + barra de escala quemados en los ~60 px inferiores → recortar antes de analizar.
