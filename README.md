# dos-regimenes

Proyecto final del curso *Ondas Gravitacionales e Investigación Asistida por IA*.

**Pregunta.** ¿El contraste entre la reflectancia de las muestras 1–3 y la de la muestra 4
de una tira de acetato de celulosa poroso se explica enteramente por un cambio de régimen
de dispersión —de Mie a la transición Rayleigh— al cruzar `x = πD/λ ~ 1`, y cómo se
caracteriza espectralmente cada régimen a cada lado de esa frontera?

Base experimental: Laboratorio 6, FCEyN–UBA (T. Chamorro, N. De Albuquerque).
Autor del proyecto: **Tomás Chamorro**.

## Estructura

```
data/            datos de entrada + PROCEDENCIA.md (de dónde sale cada cosa)
  reflectancia/  20 espectros R(λ) tira A (02/06/2026) + 2 espectros de patrón
  transmitancia/ 4 tira A (23/04) + 4 tira B (21/04)
  sem/           MANIFEST.csv de las 78 SEM (los .tif NO se versionan, ver sem/README.md)
  refs/          n(λ) del sólido y su procedencia
src/dosregimenes/  código (un módulo por eslabón de la cadena)
checks/          un test por número; run_checks.py corre todos e imprime una línea c/u
scripts/         un script por figura del informe
figures/         salida
notas/           wiki del proyecto: notación, log append-only, fichas de fuentes
informe/         informe.html + informe.pdf (para personas)
```

## Reproducir

Requiere Python 3.11+ y [`uv`](https://docs.astral.sh/uv/).

```
uv sync
uv run python checks/run_checks.py        # corre la batería de verificaciones
uv run python scripts/<figura>.py         # regenera una figura
```

Las 78 imágenes SEM (`.tif`, 67 MB) no están en el repo. `data/sem/README.md` explica
cómo obtenerlas; `data/sem/MANIFEST.csv` lista cada archivo con su muestra, mitad, aumento
y tamaño de píxel (leído de la metadata Zeiss).

## Estado

Etapa 0 (preparación) completa. Ver `notas/log.md` y el plan de trabajo:
<https://claude.ai/code/artifact/3f4f2e60-2fa2-4f45-93db-d200e06b2599>
