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

---

## 2026-09-11 (e) — Etapa 5, primera parte · HERRAMIENTAS LISTAS, COMPARACIÓN BLOQUEADA

**Hecho**

- `src/dosregimenes/mie.py` real: `Q_sca`, `g`, promedios sobre P(D), `ell_star_diluido`.
- `src/dosregimenes/estructura.py` real: `S_py` de Percus–Yevick por integración numérica
  de `c(r)`, y `factor_transporte`.
- `src/dosregimenes/lamina.py` real: índice efectivo, reflectancia interna, `R_difusion`
  con bordes extrapolados, `espesor_optico`.
- `check 5.1` PASA: Rayleigh con pendiente 4 (error 1.3e-3) y **prefactor a +0.002 %** del
  `8/3|(m²−1)/(m²+2)|²` de la ec. (3); difracción ⟨Q_sca⟩ = 2.0196 (+0.98 % de 2).
- `check 5.4` PASA: `S(0)` coincide con `(1−η)⁴/(1+2η)²` **al 0.00 %** en η ∈ [0.15, 0.40];
  `|S(q→∞)−1| ≤ 0.009`.

**Sutileza de convención — resuelta y documentada**

El `x` de Mie usa λ EN EL MEDIO: `x_Mie = n_sol·x ≈ 1.47·x`. No es el `x = πD/λ₀` del eje
de la Etapa 4. Confundirlos mete un factor 1.47. Documentado en el encabezado de `mie.py`.
No afecta la conclusión (ambos grupos escalan igual; solape y hueco no cambian), y las
fronteras físicas calculadas con Mie, que no dependen de convención, son:

| definición | x_Mie | x_vacío |
|---|---|---|
| F1 (convención del proyecto) | 1.47 | 1.00 |
| F2 (p baja de 2) | 2.44 | **1.66** |
| F3 (máx \|dQ_sca/dx\|) | 3.18 | **2.16** |

F2 y F3 caen POR ENCIMA de F1, o sea que F1 = 1 es una elección conservadora, no un
artefacto. Las cuatro muestras siguen del mismo lado con cualquiera de las tres.

**Porosidad φ — dos rutas independientes coinciden**

%Area de ImageJ: Z1 (campo 94 µm, con pieles) 10.1 %; Z2 (campo 35 µm) 21.3 %; Z4 de m4
(campo 5.6 µm, dentro del núcleo) 33.0 %. Corrigiendo Z1 por la dilución de las pieles
(núcleo/total de la slide 13) da 0.18–0.20, que coincide con el 0.21 crudo de Z2.
Se adopta **φ = 0.20 ± 0.05 (m1–3)** y **0.33 ± 0.03 (m4)**.

**Primera corrida de la cadena completa — y tres problemas**

| m | ℓ*(470) | ℓ*(750) | L/ℓ* | R(470) pred | R(750) pred | s_pred (rojo) | s_med (rojo) |
|---|---|---|---|---|---|---|---|
| 1 | 22.0 | 24.0 | **2.00** | 0.507 | 0.493 | 0.06 | 0.19 |
| 2 | 23.3 | 25.3 | **1.68** | 0.480 | 0.467 | 0.06 | 0.20 |
| 3 | 29.4 | 31.7 | **1.31** | 0.443 | 0.432 | 0.05 | 0.22 |
| 4 | 2.41 | 5.94 | 8.74 | 0.830 | 0.686 | 0.51 | 1.44 |

**P1 · La difusión está fuera de rango para las muestras 1–3.** Requiere L ≫ ℓ* y da
L/ℓ* ≈ 1.3–2.0. Hace falta el Monte Carlo, que era opcional y pasa a ser necesario.

**P2 · R + T > 1 en los datos medidos.** Exceso +0.115 / +0.128 / +0.126 / +0.182 (m1–m4),
imposible en un material no absorbente. Y **no es constante**: la pendiente de ln(R+T) vs
ln λ es −0.10 a −0.16, o sea el exceso es MAYOR EN EL AZUL. El cuaderno documenta que el
patrón blanco era *"medio amarillento o gastado"*: un patrón degradado —y más degradado en
el azul— infla `R = S/P` y **también infla la pendiente `s` medida**. Es la explicación
candidata más simple y encaja con el perfil observado.

Dato a favor de que el problema está en R y no en T: **la T predicha por el modelo coincide
con la medida** (m1: 0.50 predicha vs 0.45–0.48 medida), mientras que la R no (0.49 vs 0.63).

**P3 · El modelo subestima `s` en todas las muestras**, pero no por igual:
déficit 0.13 / 0.14 / 0.17 en m1–3 (muy consistente entre sí) y **0.93 en m4**.
Un error de calibración multiplicativo con dependencia espectral desplaza `s` por igual en
todas las muestras, así que podría explicar el déficit de m1–3 pero **no el de m4**.

**Estado de `check 5.2`: NO SE CORRE TODAVÍA.** Correrlo ahora daría FALLA (factores 2.8–3.2
contra la tolerancia de 2), pero sería una falla no interpretable: falta el Monte Carlo (P1),
falta aplicar el factor de estructura a la cadena, y la escala de `R` está en duda (P2).
Declarar el resultado antes de cerrar esos tres sería exactamente lo que el proyecto dice
que no hay que hacer.

**Pendiente inmediato:** decidir qué hacer con la calibración de R (P2) — es una pregunta
sobre la medición, no sobre el modelo — y construir el Monte Carlo (P1).

---

## 2026-09-13 — Investigación de la calibración de R (P2)

**Datos nuevos del usuario**

1. El "patrón nuevo" medido el 02/06 es un **azulejo** hallado en el laboratorio (p. 30 del
   cuaderno), no un patrón de reflectancia, y **no se usó** en las mediciones finales.
2. No recuerda cuánto llevaba encendida la lámpara; es vieja, con fluctuaciones, y **pudo no
   estar estabilizada**.

**Intento descartado: corregir con el cociente patrón viejo / patrón nuevo**

Antes de saber que el nuevo era un azulejo se probó R_corr = R_med · (I_viejo/I_nuevo) · 0.98.
El cociente va de 0.92 (470 nm) a 1.12 (745 nm), pendiente +0.42. Resultado: no reduce el
exceso de R+T (1.115 → 1.117 en m1), **invierte** su pendiente (−0.10 → +0.15) y deja a
m1–3 con s_rojo **negativa** (−0.22 a −0.26). Se pasa de largo. Un cociente >1 en el rojo
era imposible para PTFE impecable — ahora se sabe por qué: el "nuevo" es un azulejo
esmaltado, ni lambertiano ni plano. **Descartado. Su espectro no se usa para nada.**

**Test de deriva de lámpara — hecho con los datos existentes**

Las 20 mediciones del 02/06 tienen hora en el encabezado; la sesión duró **72 min**.
Residuo de s respecto de la media de su muestra, contra el tiempo:

| | pendiente | significancia | cambio en 72 min |
|---|---|---|---|
| m1–3, s_azul | +0.0001 ± 0.0001 /min | 0.6σ | ≲ 0.01 |
| m1–3, s_rojo | +0.0001 ± 0.0001 /min | 1.1σ | ≲ 0.01 |
| m1–4, s_rojo | +0.0011 ± 0.0008 /min | 1.3σ | 0.08, arrastrado por un solo punto (m4 Aba, último) |

La muestra 1 da s_rojo = 0.187 / 0.191 / 0.187 / 0.185 / 0.185 a lo largo de 57 min.
**No hay deriva medible en m1–3.** La cota (≲0.02) es ~8× menor que el déficit del modelo
(0.13–0.17), así que **la lámpara no explica la discrepancia**. Queda como `check_2_3_deriva.py`.

**Lo que sigue abierto:** el patrón WS-1 amarillento. Es un sesgo fijado al calibrar, igual
para toda la sesión: no deja tendencia temporal y no hay referencia limpia para medirlo.

**Consecuencia metodológica — el observable inmune a la calibración**

Un error de calibración multiplicativo `R_med(λ) = R(λ)·f(λ)` viene del blanco, no de la
muestra, así que suma el mismo término `−d ln f/d ln λ` a la `s` de **todas** las muestras.
Por lo tanto

    Δs = s₄ − s₁₂₃   es inmune a ese sistemático, aunque s absoluta no lo sea.

Medido (600–745 nm): **Δs = 1.23**. Modelo por difusión: 0.51 − 0.06 = **0.45**. Todavía un
factor 2.7, pero ahora sin ambigüedad de calibración — y con la difusión fuera de rango
para m1–3 (P1), que el Monte Carlo tiene que resolver antes de juzgar.

Consistente con esto: los déficits de s en m1–3 son 0.13 / 0.14 / 0.17 — casi iguales entre
sí, que es exactamente la firma de un desplazamiento común de calibración.

**Propuesta para el resto de la Etapa 5:** Δs como observable primario de la comparación
modelo–medición (check 5.2), s absoluta como secundario con el sistemático del patrón
declarado, y `R + T ≤ 1` como restricción física. Monte Carlo antes de correr el check 5.2.

---

## 2026-09-13 (b) — Etapa 5: Monte Carlo, contraste con T, porosidad por muestra

**Monte Carlo — validado (`check_5_5_montecarlo.py`)**

Lámina no absorbente, Fresnel en los bordes, fase Henyey–Greenstein, incidencia normal.
Límite balístico: R = 0.0516 vs 0.0517 exacto, T = 0.9484 vs 0.9483. Régimen grueso
(L/ℓ* = 15): T coincide con difusión a −4.2 %. Ningún fotón sin escapar.

**Error propio en `estructura.factor_transporte` — corregido**

Devolvía el cociente de (1−g) *normalizado*, que omite que S(q)<1 también reduce la
dispersión total; ℓ* depende de la sección de transporte completa ∫ p·S·(1−cos θ) dΩ.
Agravante: en el primer intento sólo se corrigió el docstring y no el cálculo; se detectó
antes de usarlo. Test: el factor → 1 cuando η → 0. Magnitud: **despreciable para m1–3**
(0.996–0.999 aun a η = 0.33, porque con poros de ~2 µm casi todo el rango angular está a q
grande) y **enorme para m4** (0.10–0.15 a η = 0.33: con poros de ~0.1 µm todo el rango
angular cae donde S(q) ≪ 1). Es un factor 7–10× que sale de tratar una red bicontinua como
esferas duras de Percus–Yevick: dependiente del modelo.

**Ruido estadístico del Monte Carlo sobre s** (5 semillas, escala como 1/√N):

| | N = 40 000 | N = 160 000 |
|---|---|---|
| m1 s_azul / s_rojo | 0.063 ± 0.034 / 0.067 ± 0.025 | 0.075 ± 0.018 / 0.063 ± 0.013 |
| m4 s_azul / s_rojo | 0.310 ± 0.014 / 0.518 ± 0.022 | 0.308 ± 0.007 / 0.523 ± 0.006 |

La s predicha para m1–3 es **0.07 ± 0.02, plana en las dos bandas**. Diferencias de ~0.09
entre corridas vistas antes eran ruido. Déficit contra lo medido: **0.13 ± 0.02 en el rojo,
0.50 en el azul**.

**Contraste independiente con la transmitancia medida** (T no entra en el modelo)

| m | T med A (570) | T pred | rms del espectro | pendiente ln T med | pred |
|---|---|---|---|---|---|
| 1 | 0.464 | 0.495 | 0.029 | +0.18 | +0.05 |
| 2 | 0.471 | 0.529 | 0.054 | +0.20 | +0.06 |
| 3 | 0.449 | 0.572 | 0.117 | +0.22 | +0.04 |

Dos lecturas:

1. **La pendiente que falta no es sólo calibración.** T se mide con el haz directo como
   referencia, sin el patrón WS-1, en abril y con otro montaje — y muestra el mismo déficit
   de pendiente (~3×) que R. Dos calibraciones independientes coinciden: al modelo de
   macroporos **le falta dispersión con dependencia espectral**, en la dirección que se
   registró de antemano en la anomalía A3 (estructura sub-λ tipo Rayleigh). El exceso
   *adicional* de R en el azul (0.50 contra 0.13 en el rojo) sí podría ser en parte el
   patrón amarillento; con estos datos no se separan.
2. **El modelo invierte el orden de transparencia entre 1–3**: predice m3 la más
   transparente y lo medido la da la menos. Parte de la causa: φ se había estimado
   promediando las tres muestras (ver abajo). Otra parte: el espesor, medido a ojo, pesa
   mucho cuando L/ℓ* ≈ 2. En la tira A las diferencias medidas de T entre 1–3 son chicas
   (±0.01); en la tira B, m3 da 0.306, pero la tira B son otras muestras físicas y no se
   comparan con la morfología de la A.

**Muestra 4 — la dispersión dependiente es imprescindible**

| η (factor de estructura) | rms de T | s_rojo pred (med 1.44) | Δs rojo (med 1.23) | Δs azul (med 0.71) |
|---|---|---|---|---|
| 0 (sin estructura) | 0.327 | 0.54 | — | — |
| 0.20 | 0.096 | 1.20 | 1.14 | 0.81 |
| 0.25 | **0.022** | **1.45** | 1.38 | 0.98 |
| 0.275 | **0.021** | 1.59 | 1.53 | 1.10 |
| 0.33 (= φ medida) | 0.105 | 1.87 | 1.81 | 1.33 |

(80 000 fotones; m1–3 corridas con la misma estadística para Δs.)

- **Sin dispersión dependiente el modelo falla por completo para la muestra nanoporosa**
  (rms de T 0.33); para las micrométricas la corrección es despreciable. Es un resultado
  físico limpio y estándar: los scatterers sub-λ densos se apantallan entre sí.
- **Predicción sin parámetros ajustados** (η = φ = 0.33): Δs rojo 1.81 (1.47×), Δs azul 1.33
  (1.87×). Signo correcto y dentro de factor 2 → cumple el criterio registrado del check 5.2.
- **η ≈ 0.25–0.275 reproduce el espectro de T y la pendiente roja de R** (1.45 vs 1.44).
  Pero η se eligió barriendo contra T: **es un parámetro ajustado, no una predicción**, y se
  reporta así. Que el η efectivo de esferas duras sea algo menor que la φ medida es
  plausible para una red conectada (los poros no son esferas impenetrables), pero no se
  afirma más que eso.
- **Δs azul medido (0.71) queda por debajo de todas las predicciones.** No es m4: la s₁₂₃
  medida en el azul carga el exceso de 0.50 de las micrométricas. Δs es inmune sólo a
  errores de calibración *comunes*; si parte de ese exceso es física de m1–3 (A3), no se
  cancela. **Consecuencia: la banda roja es el contraste más limpio.**

**Porosidad por muestra — promediar las tres escondía una diferencia**

| | v1 Z1 corregido | v1 Z2 | limpios Z1 corregido | limpios Z2 | adoptada |
|---|---|---|---|---|---|
| m1 | 0.171 | 0.199 | 0.185 | 0.199 | **0.19** |
| m2 | 0.198 | 0.205 | 0.207 | 0.188 | **0.20** |
| m3 | 0.207 | 0.233 | 0.220 | 0.224 | **0.22** |

Todos los estimadores dan **m1 < m2 < m3**; la m3 tiene ~15–20 % más porosidad que la m1
(consistente con A2: más cola de poros grandes y mayor R medida). La limpios-Z3 (campo
dentro del núcleo) da 0.085–0.110 pero subestima, porque esa tabla excluye poros < 0.66 µm.

**Pendientes de esta etapa**

- Cadena m1–3 con φ por muestra y espesor ±15 % (corriendo).
- **Remedir espesores desde las SEM** — era una tarea de la Etapa 3 que quedó sin hacer y
  que el usuario pidió explícitamente. Con L/ℓ* ≈ 2 pasó a ser una incertidumbre dominante.
- Encuadre del check 5.2: la prueba primaria es la predicción SIN parámetros ajustados;
  la de η ajustado contra T va como refinamiento, rotulada como tal.

**Cadena m1–3 con φ por muestra y espesor ±15 %** (60 000 fotones)

| m | φ | L (µm) | L/ℓ* | T(550) pred | T(550) med |
|---|---|---|---|---|---|
| 1 | 0.19 | 39.1 / 46.0 / 52.9 | 1.62 / 1.90 / 2.19 | 0.533 / 0.502 / 0.481 | 0.459 |
| 2 | 0.20 | 34.9 / 41.0 / 47.1 | 1.44 / 1.69 / 1.94 | 0.554 / 0.528 / 0.503 | 0.467 |
| 3 | 0.22 | 34.0 / 40.0 / 46.0 | 1.22 / 1.44 / 1.66 | 0.582 / 0.556 / 0.530 | 0.444 |

Ni con φ por muestra ni con +15 % de espesor cierra: el modelo sigue demasiado transparente
y sigue invirtiendo el orden entre 1–3. s predicha sigue plana (0.04–0.12, dentro del ruido).
**A m3 le falta dispersión que ni porosidad ni espesor explican.**

Observación, no demostración: el faltante de T a espesor nominal ordena
**m3 (0.112) > m2 (0.061) > m1 (0.043)**, el mismo orden que la densidad de telaraña de la
prueba de factibilidad del eslabón A (5.24 > 3.98 > 3.26 µm⁻¹). Consistente con A3. Aquella
prueba era de 6 imágenes por muestra y sin calibrar, así que no se afirma más.

**Espesores remedidos desde las SEM a 3000× (v1)**

Espesor total — **confirma la slide 13 a 1–2 µm**:

| | remedido (mediana, n = 6) | slide 13 |
|---|---|---|
| m1 | 83.8 [83–84] | 83 |
| m2 | 80.4 [79–81] | 79 |
| m3 | 79.0 | 78 |
| m4 | 79.2 | 78 |

Dos imágenes marcadas válidas dan totales falsos (m3 gcb8347 = 67.6, m4 gcb8350 = 64.3): la
imagen de diagnóstico muestra que el criterio de textura confundió **pieles lisas** con fondo.
La mediana no se ve afectada.

Espesor del núcleo — **la v1 no sirve**: 8–18 µm en m1 (contra 46), 5–78 en m2–3. En el
diagnóstico se ve por qué: con suavizado de 2 µm y umbral al 30 % del máximo el algoritmo se
queda con la franja más densa del núcleo (la densidad de poros no es uniforme), y en m3 las
sombras del relieve de fractura se segmentan como poros. Se hace una v2.

**Espesores v2 y v3 — y la decisión**

v2 (suavizado 8 µm, umbral relativo entre nivel de piel y meseta; fondo = intensidad
extrema pegada al borde): el total se mantiene (82.5 / 79.3 / 78.1 / 79.8 µm) y las
medianas de núcleo pasan a 44 / 48 / 37 µm, pero imagen por imagen siguen fallas evidentes
(7, 8, 13, 17 µm).

Para descartar esas fallas **no** se usó "no coincide con la slide 13" (sería circular).
v3 agrega un criterio independiente del valor esperado: el núcleo debe capturar ≥ 70 % del
área de poros de la lámina. Resultado:

| | aceptados | núcleo (mediana) | slide 13 |
|---|---|---|---|
| m1 | 4 de 6 (rechaza fragmentos con 28 % y 19 %) | **48.4** [42–52] | 46 |
| m2 | 4 de 6 | 49.5 [48–52] | 41 |
| m3 | **1 de 6** | 61.2 | 40 |

**En m3 el criterio se invierte.** Acepta sólo el núcleo sobreestimado de gcb8308 (61 µm,
extendido hacia la zona fracturada, error que se había anticipado mirando el diagnóstico
de la v2) y rechaza los tres que se veían bien ubicados (capturan 52–69 %). Misma causa: en
m3 las sombras de fractura de las pieles cuentan como poros y contaminan el denominador.
No se bajó el umbral hasta que m3 aceptara los "buenos": sería ajustar el criterio al
resultado esperado.

**Decisión:** el espesor de núcleo del modelo es el de la slide 13 con ±15 %. Motivo: las
mediciones a ojo del Labo 6 quedaron validadas de forma independiente en el total (1–2 µm,
cuatro muestras) y en el núcleo de m1 (5 %), el único donde la medición automática es
confiable. El +21 % de m2 queda registrado. La sensibilidad ±15 % ya calculada no cambia
conclusiones. Método pasado a la biblioteca (`feret.extension_lamina`,
`feret.espesor_total_um`) con `check_3_3_espesores.py` sobre el total, que es robusto.

`check 3.3` PASA: total SEM vs slide 13 = −0.6 / +0.4 / +0.2 / +2.3 % (m1–m4).

---

## 2026-09-13 (c) — check 5.2: la predicción sin parámetros ajustados

**Diseño, fijado antes de mirar el resultado** (plan §J y entrada 2026-09-13 de este log):
observable Δs = s₄ − s̄₁₂₃ en la banda roja (inmune a errores de calibración comunes);
criterio: signo correcto y ×0.5–2. Modelo: P(D) de ImageJ → Mie promediado → ℓ* con φ por
muestra (0.19 / 0.20 / 0.22 / 0.33) → factor de estructura PY con **η = φ medida** → Monte
Carlo con espesor de núcleo de la slide 13. Ningún número sale de los espectros.

**Resultado — PASA**

| | predicho | medido | razón |
|---|---|---|---|
| **Δs rojo (600–745)** | **1.77** | **1.23** | **×1.43** |
| Δs azul (470–590) [informativo] | 1.36 | 0.72 | ×1.90 |
| s rojo m1 / m2 / m3 | 0.06 / 0.10 / 0.06 | 0.19 / 0.20 / 0.23 | |
| s rojo m4 | 1.84 | 1.44 | |

Factor de estructura en m1–3 ≥ 0.996 (despreciable, verificado dentro del check). 34 s.

**Qué dice.** Un modelo de dispersión de un solo tipo de poro por muestra, sin ajustar nada
a los espectros, reproduce el contraste espectral entre las micrométricas y la nanométrica
con el signo correcto y dentro de un factor 1.43 en la observable robusta. **El cambio de
régimen de dispersión explica la mayor parte del contraste.**

**Qué no dice — y por eso la respuesta a "¿enteramente?" es no.** Quedan dos residuos
identificados, con dirección conocida:

1. **Muestra 4 sobrepredicha** (1.84 vs 1.44). El factor de estructura de esferas duras con
   η = φ apantalla de más; con η ≈ 0.25 se reproducen T y s₄ (entrada anterior), pero ese η
   se ajustó contra T y no cuenta como predicción.
2. **Muestras 1–3 subpredichas en s absoluta** (déficit ~0.13 en rojo). Aparece también en la
   transmitancia, que no usa el patrón blanco, así que no es sólo calibración: al modelo de
   macroporos le falta dispersión dependiente de λ. Es la firma registrada de antemano para
   la anomalía A3 (estructura sub-λ intra-poro).

Descomposición del residuo (no es acuerdo, es contabilidad): los dos residuos empujan en la
dirección de achicar la sobrepredicción de Δs. Si las s₁₂₃ fueran las medidas, Δs predicho
bajaría a 1.63 (×1.33); si además s₄ fuera la de η = 0.25, a ~1.24. Lo segundo usa un
parámetro ajustado y datos; sólo muestra que los dos residuos identificados alcanzan para
dar cuenta del desvío, no que el modelo lo prediga.

**Δs azul (×1.90)** entra en factor 2 pero no se gatea: en el azul el exceso de pendiente de
m1–3 no es común a las cuatro muestras y Δs deja de ser inmune.

**Respuesta provisoria a la pregunta del proyecto:** el contraste entre las muestras 1–3 y la
4 se explica **mayoritariamente, no enteramente,** por el cambio de régimen de dispersión
(Mie ↔ transición Rayleigh) — con dispersión dependiente imprescindible del lado
nanométrico, y un faltante espectral en las micrométricas compatible con estructura sub-λ.

**Pendiente:** check 5.3 (ancla externa), Etapa 6 (frontera acotada y controles —
parcialmente hechos: espesor ±15 %, R+T), Etapa 7 (informe, verificación independiente).

---

## 2026-09-13 (d) — check 5.3: FALLA su criterio registrado

**Diseño** (fijado en el docstring antes de correrlo): la misma cadena del check 5.2,
alimentada con la morfología publicada por Syurik et al. 2017 para películas de PMMA
(poros 339 ± 109 nm, fracción 39 %, n = 1.49; P(D) lognormal por elección nuestra; capa
porosa sobre vidrio con absorbente negro detrás). Observable: R_total a 600 nm contra la
serie publicada de espesores. Criterio: ±0.10 absoluto en los tres. Se eligió R(L) y no l_t
como observable primario porque el paper extrae l_t como pendiente de T contra 1/L, que no
es exactamente ℓ*. Ficha completa en `notas/fichas.md`.

Cambios de biblioteca que requirió, con valores por defecto que no alteran nada anterior:
`montecarlo.correr(..., n_abajo)` (medio debajo de la lámina) y `mie.*(..., n_matriz)`
(índice de matriz constante). Verificado: en la batería el 5.2 vuelve a dar Δs 1.77 y el
5.5 R = 0.0516, idénticos.

**Resultado — FALLA**

| espesor de capa porosa | R(600) predicho | publicado | desvío |
|---|---|---|---|
| 9 µm | 0.45 | 0.57 | **−0.12** |
| 16 µm | 0.60 | 0.70 | **−0.10** (en el borde; no pasa) |
| 53 µm | 0.84 | 0.90 | −0.06 |

Informativo: ℓ*(400 / 600 / 800 nm) = 2.9 / 3.8 / 5.1 µm contra l_t publicado 3.5–4 µm (a
600 nm cae dentro); R(400) − R(800) = +16 y +8 puntos a 9 y 53 µm contra 13 y 7 publicados;
factor de estructura 0.74.

**Patrón:** el modelo subestima R y **el déficit se achica con el espesor** (−0.12 → −0.06).
Un error de calibración daría un corrimiento constante; esto apunta a algo que pesa más en
capas delgadas.

**Compromiso:** no se cambia el criterio ni se retocan entradas para que pase. El check queda
en FALLA en la batería hasta que el diagnóstico diga qué es. Diagnóstico en la entrada
siguiente. Sospechoso con antecedente: el factor de estructura de esferas duras con η = φ,
que en el check 5.2 ya apantallaba de más en la muestra nanoporosa.

---

## 2026-09-13 (e) — Diagnóstico de la falla del check 5.3

`scripts/05c_diagnostico_syurik.py` (80 000 fotones; no modifica el check):

| factor de estructura | ℓ* | R 9 µm (pub 0.57) | R 16 µm (pub 0.70) | R 53 µm (pub 0.90) | l_t extraído, con ordenada / por origen (pub 3.5–4) |
|---|---|---|---|---|---|
| ninguno | 2.80 µm | **0.53** (−0.04) | **0.68** (−0.02) | **0.88** (−0.02) | **3.84** / 4.67 |
| η = 0.25 | 3.46 | 0.47 (−0.10) | 0.63 (−0.07) | 0.85 (−0.05) | 4.24 / 5.35 |
| η = φ = 0.39 (pre-registrado) | 3.78 | 0.45 (−0.12) | 0.61 (−0.09) | 0.84 (−0.06) | 4.38 / 5.62 |

La capa sin poros de arriba suma ~+0.02 de especular (aire/PMMA 0.039 contra aire/espuma
0.019): no alcanza para explicar −0.12. (A 16 µm y η = φ el diagnóstico da −0.09 y el check
−0.10: diferencia de ruido con 80 000 contra 60 000 fotones; el check queda justo en el borde.)

**Diagnóstico**

1. **El resto de la cadena reproduce el ancla.** Sin factor de estructura los tres espesores
   caen a ≤0.04 de lo publicado y, a la vez, el l_t extraído con el procedimiento del paper
   (pendiente de 1 − R contra 1/L con ordenada libre) da 3.84 µm, dentro del rango publicado.
   Mie promediado sobre P(D), la densidad a porosidad φ, el índice efectivo y el Monte Carlo
   con el borde de vidrio funcionan en una película ajena.
2. **La pieza que falla es la intensidad del factor de estructura de esferas duras a η = φ:
   apantalla de más.** Explica el patrón: alarga ℓ*, y un ℓ* demasiado largo penaliza más a
   las capas delgadas, por eso el déficit se achica con el espesor.
3. **Corroboración en dos datasets independientes.** El mismo elemento falló en la misma
   dirección en la muestra 4 del check 5.2 (s₄ predicha 1.84 contra 1.44; η ≈ 0.25 ajustaba).
4. **No es "el factor de estructura sobra".** En la muestra 4 sin él el modelo era
   catastrófico (rms de T 0.33). Lo que falla es la magnitud de la supresión.
5. **Causa física más probable, identificable a priori:** se usó Percus–Yevick
   **monodisperso** con σ = ⟨D⟩. Los poros son polidispersos (desvío relativo ~32 % en
   Syurik, cola larga en nuestras muestras). La polidispersión sube S(q→0) y debilita la
   supresión a q pequeño, que es donde este factor actúa. Es una hipótesis: no se probó.

**Lo que NO se hace:** re-correr el 5.3 sin factor de estructura (o con η = 0.25) y
declararlo aprobado. Sería ajustar el modelo al ancla. **El check 5.3, tal como se registró,
FALLA**; lo que aporta es un diagnóstico corroborado.

**Consecuencias para lo ya concluido**

- Refuerza la lectura del check 5.2: el ×1.43 de sobrepredicción de Δs viene en parte de este
  mismo exceso de apantallamiento en m4.
- En m1–3 el factor de estructura vale ≥ 0.996, así que su déficit de pendiente (~0.13) **no**
  se explica por esto y sigue apuntando a A3.

**Decisión pendiente (del usuario):** implementar un factor de estructura polidisperso
justificado de antemano (p. ej. aproximación de desacople, Kotlarchyk & Chen 1983, sin
parámetros libres) y registrar un check nuevo que lo pruebe contra ambos datasets; o dejarlo
como limitación declarada y seguir a la Etapa 6.

---

## 2026-09-13 (f) — Factor de estructura polidisperso: la hipótesis queda refutada

El usuario eligió implementar la corrección polidispersa.

**Implementación.** `estructura.py`: aproximación de desacople,
S_ef(q) = 1 + β(q)[S_PY(q⟨D⟩) − 1], β = |⟨F⟩|²/⟨|F|²⟩ con amplitud de esfera homogénea sobre la
P(D) medida. Sin parámetros libres; `polidisperso=False` por defecto. `check_5_6_desacople.py`
PASA: con poros iguales β = 1 y S_ef = S_PY (error 3e-15); β(0) = ⟨D³⟩²/⟨D⁶⟩ exacto;
0 < β ≤ 1; S_ef → 1 a q grande. `check_5_4` sin cambios.

**Pre-registro.** `check_5_7_polidisperso.py` se commiteó (286b7f2) ANTES de su primera
ejecución, con cuatro criterios contra dos datasets a la vez. Checks 5.2 y 5.3 intactos.

**Resultado — FALLA**

| criterio | desacople | PY monodisperso (antes) |
|---|---|---|
| (A) Syurik R(600) a 9 / 16 / 53 µm, ±0.10 | 0.47 / 0.62 / 0.85 → **pasa por el borde** (−0.10) | 0.45 / 0.60 / 0.84 (falla) |
| (B) s₄ rojo dentro de las 5 regiones [1.28, 1.72] | **0.62 → falla** | 1.84 (falla) |
| (C) rms de T de m4 < 0.05 | **0.229 → falla** | 0.105 |
| (D) Δs rojo dentro de ×0.5–2 | **0.57 vs 1.23 (×0.46) → falla** | ×1.43 (pasa) |

Factor de estructura en Syurik: 0.74 → 0.80. En m4 la supresión casi desaparece: la muestra
queda como sin factor de estructura (s₄ sin S era 0.54; rms de T 0.33).

**La hipótesis "la polidispersión, tratada con desacople, corrige el exceso de
apantallamiento" queda refutada.** Los dos datasets responden en direcciones opuestas: en
Syurik la corrección mejora poco; en m4 se pasa de largo.

**Mecanismo — y corrección de una explicación dada en la conversación.** Antes de mirar los
números se sugirió que β sería muy chico en m4 por la cola larga de P(D). Es falso:

| | β(0) | desvío relativo de D | mediana | p99 | máx |
|---|---|---|---|---|---|
| m4 | 0.32 | 0.41 | 0.100 µm | 0.247 | 0.474 |
| Syurik (lognormal) | 0.45 | 0.32 | 0.339 µm (media) | — | — |
| m1 / m2 / m3 | 0.25 / 0.23 / 0.13 | 0.40 / 0.43 / 0.53 | ~1.75 µm | 4.7–6.6 | 7.8–9.8 |

(En m1–3 β es irrelevante: S ≈ 1 en todo su rango angular.)

Lo que realmente pasa: S_ef = 1 − β(1 − S_PY). En m4 la supresión de PY es muy profunda
(S_PY(0) = 0.07 a η = 0.33) y todo el rango angular cae en q chico, así que el resultado queda
controlado por β y no por S: con β ≈ 0.32 la supresión baja de ~0.93 a ~0.30 y el factor de
transporte sube de ~0.1 a ~0.7. El η ajustado contra T (0.25) indicaba que hacía falta un
factor de ~0.2–0.3: el desacople sobrecorrige por un factor ~3. En Syurik la supresión
promedio era menos profunda (factor 0.74) y la misma corrección casi no se nota.

**Por qué puede fallar el desacople acá (no probado).** Supone que el tamaño de un poro no
está correlacionado con la posición de sus vecinos. En un empaquetamiento denso eso es falso
—un poro grande desplaza a sus vecinos—, y la supresión real queda más fuerte que la que
predice el desacople. Además m4 no es un conjunto de esferas sino una red bicontinua.

**Lo que sí queda — una banda sistemática, no un ajuste.** Los dos cierres simples de
factor de estructura, ninguno ajustado a los datos, **acotan las observables de m4 y de Δs**:

| | desacople | medido | PY monodisperso |
|---|---|---|---|
| s₄ rojo | 0.62 | **1.44** | 1.84 |
| Δs rojo (razón pred/med) | ×0.46 | **×1** | ×1.43 |

La medición queda dentro de la banda. Esto se puede reportar como incertidumbre sistemática
del modelo por el tratamiento de la dispersión dependiente, sin elegir un η. **Para Syurik la
banda no contiene los datos** (los dos cierres quedan por debajo; sólo "sin factor de
estructura" llega): la asimetría entre datasets queda sin explicar.

**Estado del modelo de dispersión dependiente:** es el eslabón débil para espumas densas de
poros sub-λ. No se encontró un cierre sin parámetros que ajuste los dos datasets.

**Estado de checks:** 5.2 PASA (monodisperso), 5.3 FALLA (monodisperso), 5.6 PASA, 5.7 FALLA.
Las fallas quedan en la batería tal como se registraron.

---

## 2026-09-13 (g) — Etapa 6: pre-registro de los controles y de la frontera

El usuario pidió avanzar a la Etapa 6. Los criterios se escriben y commitean ANTES de correr
los checks 6.1–6.4; el detalle completo está en el docstring de cada check.

**Código nuevo.** `montecarlo.correr(..., mu_a)`: absorción por peso de camino, sin consumir
números aleatorios. `modelo.py`: la cadena de los checks 5.2/5.7 extraída (los checks 5.x no
se tocan). `controles.py`, `frontera.py`, `telarana.py` (índice de telaraña portado de la
prueba de factibilidad). `check 6.0` (implementación de la absorción) ya corrió y PASA:
error 1e-4 contra el límite balístico con absorción; μ_a = 0 da diferencia 0.

**Criterios**

| check | pregunta | criterio |
|---|---|---|
| 6.1 (a) | ¿el espesor genera el contraste? | 5 variantes (±15 % en fase y en contrafase, intercambio de espesores entre grupos): máx \|ΔΔs\| < 0.25·Δs_med |
| 6.1 (b) | ¿la absorción del sólido genera la pendiente de m4? | H_abs: dispersión de m4 congelada en 600 nm + μ_a,sol lineal desde 0 en 600; κ* da s₄ medida. Observable independiente de la calibración: Q = K(745)/K(600), K = X₄/⟨X⟩₁₂₃, X = (1−T)/R. Excluida si Q_med < Q_pred,mín − 3σ_Q (σ con tira B como sistemático) |
| 6.2 | ¿dónde está la frontera? | F1, F2, F3 (n en 470/750 nm, sesgo 0/+2 %) y F_s (cruce de s* en un barrido de x̃ con 2 entornos × 2 cierres, ≥ 2 cruces) dentro de [x̃₄(470)·1.3, mín x̃₁₂₃(750)·0.7]; CSV reproducible |
| 6.3 | ¿el contraste es tamaño o entorno (φ, L)? | factorial 2×2, reparto de Shapley: f_D ≥ 0.75 con los dos cierres |
| 6.4 | ¿las telarañas explican los residuos de m1–3? | gatea sólo la implementación (orden y ±15 % de la factibilidad). Con n = 3 ningún ρ es significativo (p = 1/6); lectura fijada: ρ = 1 en los dos residuos → "consistente, no demostrado"; otra cosa → "no respaldado" |

**Advertencia registrada de antemano (6.2):** pasar sólo dice que la teoría es compatible
con los datos; dos cúmulos separados ×5 no pueden ubicar la frontera más fino que sus cotas.

**Dato ya conocido al fijar 6.4** (entrada 2026-09-13 b): el faltante de T ordenaba
m3 > m2 > m1 igual que la telaraña; en s rojo el orden del 5.2 era m3 > m1 > m2. La lectura de
6.4 no se eligió para que dé "consistente".
