# Log del proyecto (append-only)

Una entrada por sesión de trabajo. Al cerrar cada etapa: qué se hizo, qué dio
`run_checks.py`, y todo desacuerdo con valores publicados y cómo se trató.

---

## 2026-09-10 — Etapa 0 (preparación) · COMPLETA

**Hecho**

- Repo `dos-regimenes/` creado en `…/Curso intensivo IA/`. Estructura, `CLAUDE.md`
  (contrato de notación + reglas de tokens), `pyproject.toml` (numpy, scipy, matplotlib,
  scikit-image, miepython), `.gitignore`.
- `data/PROCEDENCIA.md`: inventario completo de datasets con procedencia, calibración,
  artefactos y qué se descarta.
- Datos copiados: `data/reflectancia/` (20 espectros tira A del 02/06 + 2 de patrón),
  `data/transmitancia/` (4 tira A del 23/04 + 4 tira B del 21/04).
- `data/sem/MANIFEST.csv`: 78 filas con muestra, mitad, aumento, px_nm (de la metadata
  Zeiss), FOV, EHT, WD. Los `.tif` (67 MB) NO se versionan — `data/sem/README.md` explica
  cómo obtenerlos.
- `data/refs/n_lambda.md`: n_sol(λ) = Sultanova 2009 (Sellmeier), anclada al 1.47 @ 580 nm
  de Borgmann; sistemático +0–2 % hacia el acetato. Implementado en `src/dosregimenes/nref.py`.
- Módulos reales: `espectros.py` (carga OceanView), `pendiente.py` (s por regresión y
  spline, 2 sub-bandas), `nref.py`, `size_param.py`, `feret.py` (portado de la fase de
  factibilidad). Stubs con contrato: `mie.py`, `estructura.py`, `lamina.py`, `montecarlo.py`.
- `checks/`: `run_checks.py` + `check_0_1_fig6.py` (real). Resto listado en `PENDIENTES.md`.

**Checks**

- `check 0.1` PASA. El promedio de los 20 espectros del 02/06 reproduce todas las
  afirmaciones de la Fig. 6 del informe:
  R(450 nm) = 76 / 77 / 79 / 92 % (m1–m4); R(750 nm) = 61 / 61 / 63 / 46 %;
  orden 3 > 2 > 1; m2 la de banda más chica (±0.4 %); m4 cae ≈ 3× más y cruza en ~590 nm.

**Decisiones / desacuerdos**

- El dataset de reflectancia de la Fig. 6 quedó confirmado: `02_06\distintas regiones\CA\`.
- Banda de análisis fijada en **470–750 nm** con máscara **560–568 nm** (valores > 100 % y
  ruido de lámpara por debajo de ~460 nm; pico instrumental a 564 nm).
- Transmitancia (tira A y B, fechas tempranas): **válidas** — se midió iluminando directo
  con la fibra, sin la esfera, así que el problema del borde del puerto no aplica.
- La conclusión del propio Labo 6 (presentación, slides 16–17: *"dos regímenes… escala
  porosa distinta → dispersión espectral distinta"*) es exactamente lo que este proyecto
  desarrolla cuantitativamente.
- **Sin hook y sin skill** (decisión de costo de tokens): la disciplina de procedencia vive
  en `CLAUDE.md`; la verificación es `run_checks.py` explícito.

**Pendiente de infraestructura**

- `git init` + primer commit: falta instalar git (`winget install --id Git.Git -e`).
- `uv sync` / `uv.lock`: falta correr una vez que el entorno esté.

**Próximo:** Etapa 1 (marco teórico) — en paralelo, Etapa 2 (reducción de datos ópticos).

---

## 2026-09-11 — Etapas 1 y 2 · COMPLETAS

### Etapa 2 — reducción de datos ópticos

**Hecho**

- Sub-bandas corregidas a **(470–590)** y **(600–745) nm** (antes arrancaban en 450, fuera
  de la banda de análisis). La máscara de 560–568 nm se saltea dentro de la primera.
- `scripts/02_espectros_promedio.py` → `figures/02_espectros_promedio.{pdf,png}`.
  Cruce de la muestra 4 con el promedio de 1–3 en **λ ≈ 586 nm**.
- `scripts/02_pendiente_por_muestra.py` → `resultados/02_pendiente.csv` (16 filas: 4
  muestras × 2 métodos × 2 sub-bandas) y `figures/02_pendiente_por_muestra.{pdf,png}`.
- Nuevo directorio `resultados/` para tablas numéricas derivadas que cita el informe.

**Resultado central — pendiente espectral `s = −d ln R / d ln λ`**

| sub-banda | s₁₂₃ | s₄ | Δ |
|---|---|---|---|
| 470–590 nm | 0.58 | 1.30 | 0.71 |
| 600–745 nm | **0.21** | **1.44** | **1.23** |

Las muestras micrométricas se **aplanan** hacia el rojo (0.58 → 0.21) mientras la
nanométrica se mantiene empinada (1.30 → 1.44). Es la firma esperada: plateau acromático
de Mie vs. flanco cromático de la transición.

**Checks**

- `check 2.1` PASA — los dos métodos coinciden (peor discrepancia relativa **5 %**, en
  m1 600–745 nm) y el orden m4 > m1,m2,m3 se mantiene en ambas sub-bandas.
- `check 2.2` PASA — pero con un matiz que se reporta explícito, no se esconde:

  | sub-banda | Δ | σ_entre (muestra a muestra en 1–3) | σ_ajuste (por ajuste individual) |
  |---|---|---|---|
  | 470–590 | 0.71 | 61σ | **1.3σ** |
  | 600–745 | 1.23 | 59σ | **4.9σ** |

  El "61σ" usa la dispersión entre las muestras 1–3, que es minúscula (0.01–0.02) porque
  esas tres son casi idénticas. Con la vara conservadora (incertidumbre del ajuste,
  0.2–0.4) la separación es **sólida en el rojo pero marginal en el azul**. El check se
  reescribió para reportar las dos varas.

**Hallazgo metodológico**

**La banda discriminante es 600–745 nm.** Es donde el contraste entre regímenes es máximo
(1–3 ya aplanadas, 4 todavía empinada). La comparación modelo–medición de las Etapas 5 y 6
debe ponderar esa banda.

### Etapa 1 — marco teórico

**Hecho**

- `informe/teoria.md`: capítulo autocontenido con ecuaciones numeradas (1)–(10) y citadas.
  Cubre: parámetro de tamaño y contraste (m ≈ 0.68, el scatterer es aire en sólido, m < 1);
  límites Rayleigh (Q_sca = 8/3 x⁴|…|², σ ∝ D⁶/λ⁴) y difracción (Q_sca → 2, paradoja de la
  extinción); la transición; ℓ* y la reflectancia de lámina; factor de estructura de
  Percus–Yevick y dispersión dependiente; óptimo de blancura.
- **Frontera definida operacionalmente.** Tres candidatas: F1 `x = 1` (estándar, no depende
  de Mie), F2 el `x` donde `|d ln σ_sca/d ln λ|` baja de un umbral, F3 el `x` del máximo de
  `|dQ_sca/dx|`. **F1 designada primaria**; F2 y F3 se calculan en la Etapa 5 como
  sensibilidad. Razón decisiva: las 4 muestras caen lejos de la frontera por ambos lados
  (x ≈ 0.45–0.8 vs. 7–13), así que la conclusión **no depende** de dónde se ponga la línea.

**Punto conceptual que quedó establecido (§3.3 de `teoria.md`)**

`s` medida **no** es el exponente de `σ_sca(λ)`. La cadena σ_sca → ℓ* → R comprime los
exponentes porque `R` está acotada y satura. Un medio perfectamente Rayleigh **no** da
`s = 4`. Por eso medir `s₄ ≈ 1.4` no refuta el régimen de transición — y por eso hace falta
el modelo de lámina de la Etapa 5 para convertir una pendiente en una afirmación sobre el
régimen. Esto es lo que la Etapa 5 tiene que reproducir sin parámetros de ajuste.

### Entorno reproducible · CERRADO

- `uv` 0.12.13 instalado. `uv sync` construyó el entorno: 21 paquetes, incluido
  **miepython 3.3.0** (lo que necesita la Etapa 5). `uv.lock` versionado.
- Verificado que todo reproduce **sin parches de `PYTHONPATH`**:
  `uv run python checks/run_checks.py` → 3 checks, 0 fallas, valores idénticos a los
  obtenidos con el intérprete prestado. Los scripts también.
- La ruta de reproducción del README (`uv sync` → `uv run …`) ya es real, no aspiracional.

**Pendiente**

- Las ecuaciones con límite conocido ((3) y (5) de `teoria.md`) esperan sus tests en
  `check_5_1_*`.

**Próximo:** Etapa 3 (morfometría: P(D) desde las SEM, con el conjunto de anotación manual).

---

## 2026-09-11 (b) — Etapa 3 · COMPLETA

**Cambio de plan: aparecieron las tablas de ImageJ del Labo 6.**

El usuario tenía ya calculado el diámetro de Feret por poro para todas las imágenes.
Se copiaron a `data/imagej/` (2.9 MB, 8 archivos) y **pasan a ser la medición primaria de
P(D)**; `src/dosregimenes/feret.py` queda como segunda implementación independiente.
Motivo: el pipeline de ImageJ separa poros individuales (circ. 0.86, solidez 0.89), el mío
los fusiona en manchones e infla la cola. Detalle en `data/PROCEDENCIA.md` §4bis.

**Hecho**

- Las 78 `.tif` se versionaron en `data/sem/` (66.6 MB). Sin ellas la Etapa 3 no se
  reproduce desde un clon, que era el punto del repositorio.
- `src/dosregimenes/imagej.py`: loader de las tablas, decodificación de etiquetas
  `<muestra><mitad>-<zona>-Z<zoom>`, `PD()` y `resumen()`.
- `scripts/03_distribucion_poros.py` → `resultados/03_PD.csv` y
  `figures/03_distribucion_poros.{pdf,png}` (eje log, las dos escalas en un panel).
- `feret.py`: banner detectado dinámicamente (ocupa 41 px, no los 60 fijos que yo
  restaba — se recuperaron 19 filas de imagen útil) y `medir_barra_escala()`.
  Las cuatro perillas de segmentación ahora son constantes con nombre.

**Resultado central — P(D) en el aumento nativo de cada muestra**

| muestra | aumento | n | mediana | separación |
|---|---|---|---|---|
| 1 | 3000× | 2256 | 1.763 µm | |
| 2 | 3000× | 2613 | 1.741 µm | |
| 3 | 3000× | 2593 | 1.741 µm | |
| 4 | 50000× | 9365 | **0.100 µm** | **17.5×** |

Las tres micrométricas coinciden en la mediana al 1 %. Las distribuciones **no se solapan**.

**Checks**

- `check 3.1` PASA. m1–3 mediana 1.75 µm (+10 % vs. el 1.6 del informe); m4 0.100 µm (+0 %).
  ImageJ vs Python sobre las mismas 3 imágenes: 1.75 vs 1.95 µm (+11 %).
- `check 3.2` PASA. Escala del tag TIFF vs. barra quemada en 4 magnificaciones: peor
  desvío **+1.9 %** (tolerancia 2 %). El sesgo es positivo y sistemático porque el largo se
  mide de borde externo a borde externo; a 74 px, 1 px son 1.35 %.

**Hallazgos**

1. **La incertidumbre de D es ±25–30 %, y es de elección de análisis, no estadística.**
   Media/mediana/moda difieren 40 % entre sí por la cola. Las dos versiones del propio
   análisis del Labo 6 difieren 29 % entre ellas (v1: 1.54 µm; limpios: 1.99 µm en Z1).
   El "1.6 µm" del informe cae en el medio de ese rango. No compromete nada: `x` ≈ 10 vs
   0.57 es un factor 17, y un 30 % no cruza a nadie la frontera.
2. **Erratum de rotulado:** informe, presentación y carpetas dicen 4000× para el aumento
   más bajo; la metadata del instrumento dice **3000×**. Manda la metadata. Mapeo
   `Z1 ↔ 3000× ↔ gcb####` cerrado vía `v1_summary_z1_gcb.csv`.
3. **Las mitades `abajo` no sesgan el tamaño.** Descartarlas mueve la mediana
   +4.1 / −0.6 / −3.8 / +1.0 % en m1/m2/m3/m4 — signo **no** consistente, o sea dispersión
   entre regiones y no el daño de corte. Se usan las dos mitades por el n mayor.
   (Mi docstring inicial decía "<3 %"; era falso, se corrigió.)
4. **La anotación manual bajó de necesaria a opcional.** Dos pipelines independientes
   coinciden al 11 % y el ±30 % no amenaza la conclusión. Queda como limitación declarada:
   ambos son umbralado sobre las mismas imágenes, así que descartan errores de
   implementación pero no un sesgo común.

**Bug propio, encontrado y corregido:** al hacer el banner dinámico dejé el recorte abierto
(`a[y0:]`), y como la última fila del archivo es clara volvía a entrar y rompía la medición
de la barra (+133 % en vez de +1.9 %). `bloque_banner()` ahora devuelve inicio y fin.

**Próximo:** Etapa 4 (mapa de regímenes: P(x, λ) por muestra sobre el eje x = πD/λ).

---

## 2026-09-11 (c) — Etapa 4 · COMPLETA

**Hecho**

- `src/dosregimenes/size_param.py` reescrito: `nube_x()` (la muestra de P(x) sobre todos
  los pares D × λ), `banda_x()` (percentiles y fracción sobre la frontera) y `solape()`
  (coeficiente ∫min(f,g) sobre log₁₀x, que es la métrica con la que se decide "disjuntas").
- `scripts/04_mapa_regimenes.py` → `resultados/04_banda_x.csv` y
  `figures/04_mapa_regimenes.{pdf,png}` — la figura de cabecera del informe.
- λ recorre la **banda de análisis (470–750 nm)**, no el "visible" 400–700 convencional:
  es donde efectivamente se midió R. Con 400–700 el cuadro no cambia.

**Resultado central — las cuatro muestras en el eje x**

| muestra | p5 | mediana | p95 | frac. con x > 1 |
|---|---|---|---|---|
| 1 | 5.35 | 9.11 | 17.93 | 100 % |
| 2 | 5.34 | 9.08 | 19.26 | 100 % |
| 3 | 5.31 | 9.18 | 22.93 | 100 % |
| 4 | 0.27 | **0.52** | 1.05 | **6.2 %** |

**Check**

- `check 4.1` PASA. Solape entre las micrométricas: **0.92–0.98**. Solape de cualquiera de
  ellas con la muestra 4: **0.000**. Hueco entre p95(m4)=1.05 y p5(m1–3)=5.31: **factor 5.1**.

**Hallazgo: el mecanismo del cruce espectral**

La cola superior de la muestra 4 cruza la frontera, y cuánto lo hace depende de λ:

| muestra 4 | x mediana | x p95 | frac. x > 1 |
|---|---|---|---|
| en 470 nm | 0.67 | 1.28 | **16.7 %** |
| en 750 nm | 0.42 | 0.80 | **1.5 %** |

Un 17 % de sus poros alcanza el régimen eficiente en el azul y prácticamente ninguno en el
rojo. Eso da un mecanismo concreto para lo medido en la Etapa 2: la muestra 4 es la **más**
reflectante en el azul (R=0.92 a 450 nm, por encima de las tres micrométricas) y la **menos**
en el rojo (R=0.46 a 750 nm), con cruce en ~586 nm. **Es una hipótesis, no una demostración**:
convertirla en predicción cuantitativa es exactamente el trabajo de la Etapa 5.

**Por qué la conclusión es robusta.** El hueco de factor 5.1 entre los dos grupos es mucho
mayor que el ±25–30 % de incertidumbre en D (PROCEDENCIA §4bis), que además desplaza las
nubes en bloque sin acercarlas. Y como F1 (x = 1) cae dentro de ese hueco vacío, mover la
definición de frontera dentro de un factor ~5 no cambia de qué lado queda cada muestra.

**Error propio:** corrí `Get-Content | Set-Content -Encoding utf8` sobre un archivo UTF-8
para un reemplazo trivial y le rompí todos los acentos (mojibake). Se reescribió el archivo
entero. Para editar archivos con acentos, usar la herramienta de edición, nunca un
round-trip de texto por PowerShell.

**Próximo:** Etapa 5 (predicción de s sin parámetros de ajuste: Mie + P(D) + factor de
estructura → ℓ*(λ) → R de lámina → s predicha, contra la s medida de la Etapa 2).

---

## 2026-09-11 (d) — Revisión de anomalías de la Etapa 4

Se revisó si los resultados salieron como se esperaba. Las medianas sí (9.1 y 0.52, contra
7–13 y 0.45–0.8 predichos en `teoria.md`). Aparecieron tres desviaciones.

### A1 · Error de documentación en `teoria.md` — CORREGIDO

La tabla de §1 daba `x = 7–13` para las muestras 1–3. Ese rango sale de fijar `D` y variar
sólo `λ` (ancho factor 1.6). El ancho real es factor **3.4–4.3**:

| muestra | p5–p95 real | factor | con D fijo | factor |
|---|---|---|---|---|
| 1 | 5.35–17.93 | 3.4 | 7.38–11.78 | 1.6 |
| 2 | 5.34–19.26 | 3.6 | 7.29–11.64 | 1.6 |
| 3 | 5.31–22.93 | 4.3 | 7.29–11.64 | 1.6 |
| 4 | 0.27–1.05 | 3.8 | 0.42–0.67 | 1.6 |

**La polidispersión aporta más del doble de ancho que el recorrido de λ.** Tabla corregida
y nota agregada en `teoria.md` §1.

### A2 · La muestra 3 tiene el doble de cola — A VIGILAR EN ETAPA 5

| muestra | mediana | p90 | p99 | frac(D>3 µm) |
|---|---|---|---|---|
| 1 | 1.763 | 2.808 | 4.75 | 7.9 % |
| 2 | 1.741 | 2.955 | 5.01 | 9.4 % |
| 3 | 1.741 | 3.472 | 6.55 | **15.0 %** |

Misma mediana, casi el doble de poros grandes. Y la muestra 3 es la de **mayor reflectancia
medida** (Etapa 2) y la de banda de dispersión más ancha entre las tres (±2.6 %). Con n=3 es
anecdótico; la Etapa 5 lo confirma o lo rompe: si el modelo reproduce el orden m3 > m2 > m1
a partir de las colas de `P(D)`, la correlación es real.

### A3 · Hay estructura sub-micrométrica que `P(D)` no incluye — LIMITACIÓN REAL

La tabla de ImageJ no tiene nada por debajo de ~0.66 µm en m1–3, ni siquiera a 20000×
(resolución 0.041 µm). Podía ser ausencia o filtrado. Se corrió `feret.py` sobre las mismas
imágenes con `d_min_um` bajado de 0.15 a 0.03:

| | ImageJ a 20000× | `feret.py`, misma imagen |
|---|---|---|
| n | 54–126 | **186–323** |
| D mínimo | 0.66–0.69 µm | **0.14–0.16 µm** |
| mediana | 1.25–1.42 µm | 0.35–0.51 µm |

**Hay estructura sub-micrométrica y el análisis de ImageJ la excluye.** Identidad más
probable: la **telaraña intra-poro** que el informe del Labo 6 documenta en m1–3 y que mi
umbralado fragmenta (ver la prueba de factibilidad). No es equivalente a la red nanoporosa
de m4, que es la morfología del material y no una decoración dentro de un poro.

**Consecuencia para la Etapa 5:** el `P(D)` que alimenta el modelo describe **sólo la
población de macroporos** de m1–3. Si esa estructura sub-λ dispersa, el modelo la omite, y
como sería dispersión tipo Rayleigh la firma esperada es que **el modelo subestime la
dispersión de m1–3 preferentemente en el azul**. Es una predicción falsable: si el residuo
de la Etapa 5 aparece justo ahí, es evidencia de que la telaraña contribuye ópticamente —
que era la pregunta de la propuesta hermana archivada.

Queda como **limitación declarada** del proyecto, con su firma esperada escrita de
antemano para que no se pueda racionalizar después.
