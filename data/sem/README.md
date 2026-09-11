# SEM — 78 imágenes

Las imágenes **están versionadas en este repo** (66.6 MB), en las 8 subcarpetas
`<muestra> <mitad>`. Sin ellas la Etapa 3 no se puede reproducir, y ése es el punto del
repositorio.

`MANIFEST.csv` lista cada archivo con: `archivo, carpeta, muestra, mitad, aumento_x,
px_nm, fov_um, eht_kv, wd_mm, ancho_px, alto_px`.

## Origen

Zeiss GeminiSEM 560, Centro de Microscopía Avanzada (CMA, UBA). Sesión 11/06/2026.
Cortes transversales de la tira A de acetato de celulosa, crio-fracturados en N₂ líquido
y metalizados. 4 muestras, cada una cortada al medio → mitades `arriba` y `abajo`.
Detalle completo en `../PROCEDENCIA.md` §4.

## Estructura

```
data/sem/
  1 arriba/  gcb8284.tif … (9)
  1 abajo/   … (9)
  2 arriba/  … (9)      2 abajo/  … (9)
  3 arriba/  … (9)      3 abajo/  … (9)
  4 arriba/  … (12)     4 abajo/  … (12)
```

| | muestras 1–3 | muestra 4 |
|---|---|---|
| imágenes por mitad | 9 = 3 regiones × 3 aumentos | 12 = 3 regiones × 4 aumentos |
| aumentos | 3000× / 8000× / 20000× | + 50000× |
| px_nm | 91.80 / 34.42 / 13.77 | + 5.51 |

## Dos cosas antes de analizarlas

1. **La escala sale de la metadata, no de la barra quemada.** Cada `.tif` trae el tamaño
   de píxel exacto en el tag TIFF Zeiss `34118` (primer float, en metros).
   `dosregimenes.feret.pixel_size_m()` lo lee. El check 3.2 contrasta ese valor contra la
   barra dibujada.
2. **Recortar el banner**: los ~60 px inferiores son la barra de información de Zeiss
   (texto + barra de escala) y contaminan cualquier umbralado.
   `dosregimenes.feret.cargar_gris()` ya los saca.

## Calidad: no todas las mitades sirven igual

Del cuaderno de laboratorio (11/06): *"abajo: no fuimos más abajo porque se veía que el
corte afectó la estructura porosa"*. Las mitades **`abajo` tienen daño de fractura** hacia
el borde inferior. Para morfometría cuantitativa se priorizan las mitades **`arriba`** y las
regiones centrales; `abajo` se usa como control de robustez, no como dato primario.
