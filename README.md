# dos-regimenes

Proyecto final del curso *Ondas Gravitacionales e Investigación Asistida por IA*.
Autor: **Tomás Chamorro**. Base experimental: Laboratorio 6, FCEyN–UBA (T. Chamorro,
N. De Albuquerque).

**Pregunta.** ¿El contraste entre la reflectancia de las muestras 1–3 y la de la muestra 4
de una tira de acetato de celulosa poroso se explica enteramente por un cambio de régimen
de dispersión —de Mie a la transición Rayleigh— al cruzar `x = πD/λ ~ 1`, y cómo se
caracteriza espectralmente cada régimen a cada lado de esa frontera?

**Respuesta (`informe/informe.html`, § 5).** *Sí, en parte:* el cambio de régimen es la
explicación física consistente, predicha en dirección y orden de magnitud, pero no una
explicación cuantitativa cerrada. Los datos muestran dos escalas de estructura (x ≈ 9 y
0.52, sin solape) y dos respuestas espectrales (Δs rojo = 1.23). Una predicción sin
parámetros ajustados (Mie + P(D) medida + factor de estructura + Monte Carlo) da Δs con signo
correcto y ×1.43, con un criterio amplio y no ciego (check 5.2). Dentro del modelo el
contraste lo carga el tamaño de poro (6.3) y no el espesor (6.1 a). La frontera cae en la
brecha `x ∈ [0.87, 5.1]`, sin muestras adentro. Falta: un cierre de dispersión dependiente
validado para espumas densas sub-λ (5.3, 5.7, 6.2 fallan), excluir la absorción con un
criterio registrado (6.1 b falla) y explicar el faltante de pendiente de las muestras 1–3.
Verificado de forma independiente con Codex: `notas/segunda_opinion_codex.md`.

## Reproducir desde cero

Requisitos: `git` y [`uv`](https://docs.astral.sh/uv/) (uv instala el Python que haga falta,
≥ 3.11). Probado en Windows 10 con uv 0.12.

```
git clone https://github.com/Tom-uba/Proyecto-final--Dos-regimenes-de-dispersi-n-de-la-luz.git dos-regimenes
cd dos-regimenes
uv sync
uv run python checks/run_checks.py
```

`run_checks.py` imprime una línea por check (`[PASA]` / `[FALLA]` + evidencia numérica) y
sale con código = número de fallas. **Resultado esperado: 4 fallas** (5.3, 5.7, 6.1, 6.2),
registradas a propósito con su diagnóstico; ver `run.log`. Tarda del orden de 15–20 min
(los checks 5.x y 6.x corren Monte Carlo). Un check suelto:
`uv run python checks/check_4_1_mapa.py`.

Figuras y tablas (las figuras no se versionan: se regeneran). Cada script documenta en su
encabezado entrada, cálculo, elecciones y el check que lo verifica.

| etapa | script | produce | check |
|---|---|---|---|
| 2 | `scripts/02_espectros_promedio.py` | `figures/02_espectros_promedio.*` | 0.1 |
| 2 | `scripts/02_pendiente_por_muestra.py` | `resultados/02_pendiente.csv`, figura | 2.1–2.3 |
| 3 | `scripts/03_distribucion_poros.py` | `resultados/03_PD.csv`, figura | 3.1, 3.2 |
| 3 | `scripts/03b_espesores.py` | `resultados/03b_espesores.csv`, diagnóstico | 3.3 |
| 4 | `scripts/04_mapa_regimenes.py` | `resultados/04_banda_x.csv`, `figures/04_mapa_regimenes.*` (figura de cabecera) | 4.1 |
| 5 | `scripts/05c_diagnostico_syurik.py` | tabla por stdout (diagnóstico de la falla 5.3) | 5.3 |
| 6 | `scripts/06_frontera.py` (~10 min) | `resultados/06_frontera*.csv`, `figures/06_frontera_acotada.*` | 6.2 |
| 6 | `scripts/06_controles.py` (~5 min) | `resultados/06_controles.csv`, `figures/06_controles.*` | 6.1, 6.3 |
| 7 | `scripts/07_informe.py` (después de 02–06) | `informe/informe.html` (autocontenido) + `informe/informe.pdf` | — |

Los checks de la Etapa 5 (5.1, 5.2, 5.4–5.7) y 6.0, 6.4 calculan directamente, sin script.

## Estructura

```
data/              datos de entrada + PROCEDENCIA.md (de dónde sale cada archivo)
  reflectancia/    20 espectros R(λ) de la tira A (02/06/2026) + 2 de patrón
  transmitancia/   4 de la tira A (23/04) + 4 de la tira B (21/04)
  sem/             78 imágenes SEM .tif (66.6 MB, versionadas) + MANIFEST.csv + README.md
  imagej/          tablas de poros del Labo 6 (fuente primaria de P(D))
  refs/            n(λ) del sólido y su procedencia
src/dosregimenes/  código: un módulo por eslabón (espectros, pendiente, feret, imagej,
                   size_param, mie, estructura, lamina, montecarlo, modelo, controles,
                   frontera, telarana)
checks/            un check por resultado; run_checks.py corre todos; PENDIENTES.md los lista
scripts/           un script por figura o tabla
resultados/        tablas derivadas (CSV)
figures/           figuras generadas (no versionadas)
notas/             log append-only (fuente de verdad), fichas de fuentes, notación
informe/           teoria.md (marco teórico); informe.html e informe.pdf (Etapa 7)
run.log            última corrida completa de la batería y tratamiento de cada falla
CLAUDE.md          instrucciones para agentes: notación, reglas de procedencia
```

## Estado

Etapas 0–7 completas: informe en `informe/informe.html` e `informe/informe.pdf`; segunda
opinión y prueba de reproducción con Codex en `notas/segunda_opinion_codex.md`.
Plan de trabajo: <https://claude.ai/code/artifact/3f4f2e60-2fa2-4f45-93db-d200e06b2599>
