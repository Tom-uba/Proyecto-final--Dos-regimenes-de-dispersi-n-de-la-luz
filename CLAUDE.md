# Instrucciones para el agente — proyecto `dos-regimenes`

## Qué es esto

Proyecto final: caracterizar los dos regímenes de dispersión (Mie vs. transición Rayleigh)
en la reflectancia de láminas porosas de acetato de celulosa y acotar la frontera en
`x = πD/λ`. La cadena de trabajo (8 etapas) está en el plan; el estado actual en
`notas/log.md`.

## Contrato de notación (fijo — no renombrar)

| símbolo | significado | unidad |
|---|---|---|
| `D` | diámetro de Feret del poro | µm (interno: m) |
| `lam` (λ) | longitud de onda en vacío | nm (interno: m) |
| `x` | parámetro de tamaño, `x = π·D/λ` | — |
| `m` | contraste de índice, `m = n_aire / n_solido` | — |
| `n_sol(λ)` | índice del sólido (acetato de celulosa) | — |
| `s` | pendiente espectral, `s = −d ln R / d ln λ` | — |
| `R`, `T`, `A` | reflectancia, transmitancia, absorción difusas | fracción (0–1) |
| `phi` (φ) | porosidad (fracción de volumen de aire) | — |
| `Qsca`, `g` | eficiencia de dispersión y anisotropía (Mie) | — |
| `ell` (ℓ*) | camino libre medio de transporte | µm |
| `d` | espesor de la capa porosa | µm |

Unidades: las funciones exponen µm/nm en la interfaz; internamente trabajan en SI.
Banda de análisis por defecto: **470–750 nm**, con máscara en **560–568 nm** (pico
instrumental). Justificación en `data/PROCEDENCIA.md`.

## Reglas de trabajo

1. **Procedencia obligatoria.** Cada número y cada figura del informe lleva, en el script
   o el docstring que lo produce: qué archivo de datos entró, qué función lo calculó, qué
   se derivó vs. qué se llamó de librería, y el check que lo verifica. Plantilla en
   `notas/procedencia-plantilla.md`.
2. **Un check por resultado.** Vive en `checks/`. `checks/run_checks.py` los corre todos.
   Cada check imprime **una línea**: `PASA`/`FALLA` + evidencia (un número o una ruta,
   nunca un adjetivo).
3. **Al cerrar una etapa**: correr `run_checks.py`, anotar en `notas/log.md` (append-only)
   qué se hizo, qué dio, y cualquier desacuerdo con valores publicados y cómo se trató.
4. **La muestra 4 se modela aparte**: es una red bicontinua nanométrica (D ≈ 0.1 µm), no
   "poros + paredes". Ver `data/PROCEDENCIA.md` §4.
5. **Mitades SEM**: usar `arriba` y regiones centrales para morfometría cuantitativa; las
   mitades `abajo` tienen daño de corte (`data/PROCEDENCIA.md` §4).

## Costo de tokens — reglas

- **Sin `Stop`-hook.** La verificación es explícita (`run_checks.py`). Un hook que bloquea
  el fin de turno re-envía todo el contexto en cada reintento; no compensa acá.
- **Sin skill de procedencia** por ahora — la disciplina está en este archivo. Se agrega
  una skill corta solo si en la práctica se relaja.
- Los checks y los scripts imprimen **poco**: una línea por resultado. Nada de volcar
  arrays, diffs o logs largos al stdout.
- **No releer PDFs grandes.** `PhD Thesis Luisa Borgmann.pdf` (155 pág.) y el cuaderno de
  laboratorio ya están fichados en `notas/fichas.md`. Ir al PDF solo con `offset`/`limit`
  para un dato puntual que falte.
- Los espectros crudos (3648 puntos × 30 archivos) se cargan con
  `dosregimenes.espectros.load()` — nunca se pegan en el chat.
- `notas/` es la fuente de verdad. Actualizar el log en vez de re-derivar.

## Entorno

`uv sync` con `pyproject.toml`. Dependencias: numpy, scipy, matplotlib, scikit-image,
miepython. Nada más sin anotarlo en el log y en `pyproject.toml`.
