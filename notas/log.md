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
