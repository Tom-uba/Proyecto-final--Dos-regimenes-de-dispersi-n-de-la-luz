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
