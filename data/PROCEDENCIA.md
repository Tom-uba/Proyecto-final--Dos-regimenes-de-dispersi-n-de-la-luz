# PROCEDENCIA — Proyecto "Dos regímenes de reflectancia"

> Borrador v1 (2026-09-10). Generado a partir del escaneo de `Labo 6\`, el informe y el
> cuaderno de laboratorio. **Revisar y corregir los puntos marcados `[CONFIRMAR]`.**
> Destino: `data/PROCEDENCIA.md` del repo `dos-regimenes/` (Etapa 0).

---

## 1. Contexto experimental

- **Base:** Laboratorio 6 — *"Medición de reflectancia y caracterización de películas porosas"*.
  Grupo de Electromagnetismo Aplicado, Depto. de Física, FCEN–UBA.
- **Directoras:** Dra. Diana Skigin, Dra. Marina Inchaussandague.
- **Mediciones y SEM:** N. De Albuquerque (LU 490/22), T. Chamorro (LU 629/22). Marzo–julio 2026.
- **Fuentes:** `Informe_Labo_6_Nico_y_Tomas (4).pdf` (21/07/2026); `Cuaderno de Laboratorio 6.pdf` (54 pág.).
- **Material:** láminas de acetato de celulosa espumadas con CO₂ supercrítico en el KIT.
  Tira A: saturación 180 min, 50 MPa, 80 °C, grosor nominal 70 µm. Cuatro muestras numeradas
  de arriba hacia abajo en la tira; la 4 (visiblemente más transparente, tonalidad azulada) es
  la del borde.
- **La conclusión del Labo 6 ya apunta a este proyecto:** presentación
  `Presentacion_Laboratorio_6_DeAlbuquerque_Chamorro.pptx.pdf`, slide 16
  (*"Escala porosa distinta → dispersión espectral distinta"*) y slide 17
  (*"Dos regímenes: las muestras 1–3 son micrométricas; la 4 es nanométrica"*). Este proyecto
  es el desarrollo cuantitativo de esa conclusión.
- **Inconsistencia registrada (no afecta este proyecto):** sobre las telarañas de la muestra 4,
  el cuaderno (p. 45) dice "completamente formada por poros con telarañas pero mucho más chicos";
  la presentación (slide 16) y el informe dicen "sin telarañas visibles". Para *dos regímenes*
  da igual: la muestra 4 es nanométrica (D ≈ 0.1 µm) en cualquier lectura.

## 2. Nomenclatura

- Letra = tira, número = muestra dentro de la tira. **Tira A y B = acetato de celulosa**
  (misma fabricación, "no presentan diferencias significativas"). Tiras C/D/E = PMMA.
- Este proyecto usa **solo tira A** para reflectancia y SEM; tira A/B para transmitancia
  (condicionado a validación).

---

## 3. DATASET 1 — Reflectancia R(λ)  · PRIMARIO · check 0.1 PASA

| campo | valor |
|---|---|
| Ruta | `Labo 6\02_06\distintas regiones\CA\` |
| Archivos | 20 · `tira_A_muestra_{1..4}_{Izq,Cen,Der,Arr,Aba}_Reflection__0__*.txt` |
| Estructura | 4 muestras × 5 regiones (Cen = centro; Izq/Der/Arr/Aba = puerto desplazado respecto del centro, muy solapadas por el puerto de 8 mm vs. tamaño de muestra) |
| Fecha | 02/06/2026 |
| Instrumento | esfera integradora Ocean Optics ISP-50-8-R-GT (puerto 8 mm ⌀, incidencia 8°, gloss trap); lámpara LS-1-LL; espectrómetro USB400; software OceanView |
| Adquisición | integración 2600 ms · 20 promedios (Scan to Average) · Boxcar 3 · Non-linearity Correction ON |
| Calibración | patrón blanco **viejo** (Ocean Optics WS-1, algo amarillento) + **"calibración nueva"** = 0 % de reflectancia fijado con la **lámpara de la esfera encendida y el puerto abierto** (descuenta la reflexión en el borde del puerto). Es la del §II del informe. |
| Formato | export OceanView, **ya en % de reflectancia** (blanco + oscuro aplicados internamente). Columnas: `λ[nm] \t R[%]`. 3648 px, rango 336–1792 nm. Datos tras la línea `>>>>>Begin Spectral Data<<<<<`. |

**check 0.1** — el promedio por muestra reproduce la Fig. 6 del informe en todo:

| | m1 | m2 | m3 | m4 |
|---|---|---|---|---|
| R(450 nm) | 76.3 % | 76.8 % | 79.3 % | 92.4 % |
| R(550 nm) | 65.7 % | 66.2 % | 68.4 % | 70.4 % |
| R(650 nm) | 62.8 % | 63.2 % | 64.9 % | 57.3 % |
| R(750 nm) | 61.1 % | 61.4 % | 62.8 % | 46.1 % |
| caída 450→750 | 15 pts | 15 pts | 17 pts | 46 pts |
| banda de dispersión (±1σ media) | ±1.7 % | ±0.4 % | ±2.6 % | ±3.7 % |

Afirmaciones del informe verificadas: 1–3 agrupadas y decrecientes ✓ · orden 3 > 2 > 1 ✓ ·
muestra 2 la más homogénea ✓ · muestra 4 arranca más alta, cae ~3× más, cruza a las otras
en ~585–595 nm, termina la más baja ✓ · banda de m4 la más ancha ✓.
Figura: `scratchpad\check01_fig6.png`.

**Artefactos instrumentales — excluir del ajuste de pendiente:**

- **λ ≲ 460 nm:** fluctuación de la lámpara de tungsteno; valores > 100 % en regiones de la
  muestra 4 (hasta 102 % @ 450 nm en `Arr`; el cuaderno reporta hasta 120 % cerca de 400 nm
  en otras tiras).
- **λ ≈ 564.1 nm:** pico instrumental de la esfera (depende de la estabilidad térmica de la lámpara).
- Regiones `Izq` de m1 y m3 son outliers bajos; `Aba` de m3 outlier alto → el promedio de
  5 regiones lo absorbe; la banda de dispersión lo refleja.

**Banda de análisis recomendada: 470–750 nm**, con máscara en 560–568 nm.

**Referencias de intensidad cruda** (para reprocesar desde cero si hiciera falta, mismo día):
`02_06\espectro_patron_nuevo.txt`, `02_06\espectro_patron_viejo_USB4F063981__0__1.txt`.

---

## 4. DATASET 2 — SEM  · PRIMARIO

| campo | valor |
|---|---|
| Ruta | `Labo 6\Imagenes del microscopio\26 06 11-Tomas Chamorro\` |
| Imágenes | 78 `.tif` · Zeiss GeminiSEM 560 · CMA (Centro de Microscopía Avanzada, UBA) · sesión 11/06/2026 |
| Preparación | muestras congeladas en N₂ líquido, cortadas a mano (muesca guía en el canto descartado), metalizadas |
| Carpetas | 8 = 4 muestras × {arriba, abajo} (las dos mitades de cada muestra cortada) |
| Imágenes por carpeta | muestras 1–3: 9 = 3 regiones (izq/centro/der) × 3 aumentos (3000× / 8000× / 20000×). Muestra 4: 12 = 3 regiones × 4 aumentos (+50000×, poros nanométricos) |
| Formato | 1024×768, 8-bit (paleta indexada), sin comprimir. Banner Zeiss + barra de escala quemados en los ~60 px inferiores → **recortar antes de analizar** |

**Escala embebida** (tag TIFF 34118, primer float = tamaño de píxel en m):

| aumento | nm/px | FOV (1024 px) |
|---|---|---|
| 3000× | 91.80 | 94.0 µm |
| 8000× | 34.42 | 35.2 µm |
| 20000× | 13.77 | 14.1 µm |
| 50000× | 5.51 | 5.6 µm |

Parámetros: EHT 3 kV · WD ≈ 6.8–8.5 mm (varió) · detector SE2 · dwell 50 ns.

**Notas de calidad (cuaderno, 11/06):**

- Las mitades **`abajo` tienen daño de corte** en la estructura porosa hacia el borde inferior
  (*"no fuimos más abajo porque se veía que el corte afectó la estructura"*).
  → priorizar mitades **`arriba` y regiones centrales** para morfometría cuantitativa;
  usar `abajo` solo como control de robustez.
- **Muestra 4:** *"completamente formada por poros con telarañas pero mucho más chicos"* —
  red bicontinua a escala ~100 nm. Requiere morfometría distinta (longitud característica /
  ancho de ligamento, no diámetro de poro cerrado).
- Carpetas relacionadas: `Imagenes del microscopio\Conteo con IA (no funciono)` (intento
  fallido de conteo automático), `Imagenes del microscopio\Por escala`.

**Morfometría previa (blanco de validación, check 3.1):**

- Feret medio: **~1.6 µm** (muestras 1–3), **~0.1 µm** (muestra 4). Cuaderno: pico de PSD ~1.5 µm,
  mayoría de poros entre 1 y 2 µm.
- **Espesores** (presentación, slide 13 — medidos a ojo, error considerable):

  | Muestra | Grosor total | Capa porosa |
  |---|---|---|
  | 1 | 83 µm | 46 µm |
  | 2 | 79 µm | 41 µm |
  | 3 | 78 µm | 40 µm |
  | 4 | 78 µm | **32 µm** |

  La capa porosa es la entrada del modelo de lámina (`d`). **Plan:** remedir la capa porosa
  desde las SEM de bajo aumento en la Etapa 3 y verificar que dé del mismo orden que estos
  valores. Estructura: 3 capas (dos pieles lisas + núcleo espumoso).

---

## 4bis. DATASET 2b — Tablas de ImageJ (morfometría)  · PRIMARIO para P(D)

Producidas por el pipeline de Fiji/ImageJ del Labo 6 sobre las mismas 78 imágenes.
Copiadas a `data/imagej/`. **Son la medición primaria de P(D)**: separan poros
individuales mucho mejor que la segmentación rápida de `src/dosregimenes/feret.py`
(circularidad media 0.86, solidez 0.89, contra manchones fusionados), que queda como
segunda implementación independiente para el check 3.1.

| archivo en `data/imagej/` | origen | contenido |
|---|---|---|
| `poros_m1a3_limpios.csv` | `Results_limpios.csv` (21/06/2026) | 11 437 poros, 54 imágenes: m1–3 × 2 mitades × 3 zonas × 3 zooms |
| `resumen_por_imagen_m1a3.csv` | `Resumen_por_imagen.csv` | una fila por imagen, con Muestra/Orientacion/Zona/Zoom |
| `poros_m4_z4.csv` | `Resultados muestra 4 Z4.csv` (02/07/2026) | 9 365 poros, 6 imágenes de la muestra 4 a 50000× |
| `resumen_por_imagen_m4_z4.csv` | `Resumen_Total muestra 4 Z4.csv` | resumen de esas 6 |
| `v1_summary_z1_gcb.csv`, `v1_poros_z1_gcb.csv` | `Por escala/Resultados zoom 4000/` (18/06) | versión anterior, con los nombres `gcb####` originales |
| `v1_summary_z2_gcb.csv`, `v1_poros_z2_gcb.csv` | `Por escala/Resultados zoom 8000/` (18/06) | ídem, 8000× |

**Nomenclatura de las etiquetas:** `<muestra><mitad>-<zona>-Z<zoom>.tif`, con
mitad `U`=arriba / `D`=abajo, zona `U`/`C`/`D` (las tres regiones), y
`Z1`=3000×, `Z2`=8000×, `Z3`=20000×, `Z4`=50000×.

**Erratum de rotulado:** el informe, la presentación y los nombres de carpeta dicen
**4000×** para el aumento más bajo. La metadata del instrumento dice **3000×**
(`MANIFEST.csv`, tag Zeiss). Manda la metadata. Los 18 archivos de `v1_summary_z1_gcb.csv`
son exactamente las 18 imágenes a 3000× de las muestras 1–3, lo que cierra el mapeo
`Z1 ↔ 3000× ↔ gcb####`.

**Resultado (aumento nativo de cada muestra):**

| muestra | aumento | n | media | mediana | moda | p10–p90 |
|---|---|---|---|---|---|---|
| 1 | 3000× | 2256 | 1.917 | **1.763** | 1.428 | 1.17–2.81 |
| 2 | 3000× | 2613 | 1.949 | **1.741** | 1.437 | 1.16–2.96 |
| 3 | 3000× | 2593 | 2.098 | **1.741** | 1.413 | 1.16–3.47 |
| 4 | 50000× | 9365 | 0.109 | **0.100** | 0.075 | 0.060–0.170 |

Todo en µm. Separación de tamaño m1–3 vs m4: **17.5×**, sin solapamiento entre las
distribuciones.

**Incertidumbre de D — la que manda no es la estadística.** La distribución tiene cola
larga, así que media/mediana/moda difieren ~40 % entre sí (1.99 / 1.75 / 1.39 en m1–3).
Y las dos versiones del propio análisis del Labo 6 difieren entre sí: `v1` da media
1.54 ± 0.12 µm en Z1 contra 1.99 µm de `limpios`, un 29 %. Más el ~11 % contra el pipeline
de Python. **Se adopta ±25–30 % como incertidumbre de D por elecciones de segmentación**,
y se propaga a `x = πD/λ`. No compromete la conclusión: `x` vale ~10 en m1–3 y ~0.57 en m4,
un factor 17, así que un 30 % no mueve a nadie de lado de la frontera.

**Lo que estas tablas NO cierran.** Los dos pipelines (ImageJ y Python) son umbralado sobre
las mismas imágenes: coincidir descarta errores de implementación, no un sesgo común. Eso
sólo lo cerraría anotación manual de contornos, que queda como limitación declarada.

---

## 5. DATASET 3 — Transmitancia T(λ)  · VÁLIDO (confirmado por el usuario)

| tira | ruta | fecha | n |
|---|---|---|---|
| A | `Labo 6\23_04\Transmitancia\tira_A\tira_A_muestra_{1..4}_Transmission__0__*.txt` | 23/04/2026 | 4 |
| B | `Labo 6\21_04\transmitancia\celulosa_tira_B\celulosa_tiraB_muestra{1..4}_Transmission__0__*.txt` | 21/04/2026 (integ. 3400 ms) | 4 |

- Aunque son de fecha temprana (antes del arreglo de calibración de reflectancia del 14/05),
  **la medición de transmitancia se hizo iluminando la muestra directamente con la fibra
  óptica**, sin la esfera en el camino → el problema del borde del puerto no aplica.
  **El usuario las da por válidas.**
- Uso previsto (cuaderno, 21/04): *"medir el camino libre medio"* — se usan para acotar
  μ_a(λ) en el control de la Etapa 6.
- Tira A y B: misma fabricación → intercambiables para la cota de absorción.
- Otros archivos (no se usan): `21_04\transmitancia\laminas\celulosa_lamina...` (lámina
  transparente, no porosa); `23_04\Transmitancia\tira_AM\...` (tira "AM", no identificada).

---

## 6. DATASET 4 — Referencias

| archivo / fuente | uso |
|---|---|
| `PhD Thesis Luisa Borgmann.pdf` (KIT, 2023) | benchmark óptico; **n(λ) primaria** (ver abajo) |
| `SciRep7Syurik46637(2017).pdf` | películas porosas de PMMA; benchmark y método; ancla externa (check 5.3) |
| `oceanviewioperation-manual.pdf` | parámetros de adquisición |
| *(buscar en Etapa 1)* | Bohren & Huffman (Mie); Vukusic 2007 / Wilts 2018 (Cyphochilus) |

### Índice de refracción del material sólido, n(λ)

- **PRIMARIA — Borgmann (2023), §2.2.2 (p. 23):** celulosa n ≈ **1.47 a 580 nm** (valor
  puntual; Borgmann cita refs [39,40]). En sus propios cálculos de Mie (Fig. 2.2 b, con
  MiePlot) usa n_matriz = 1.5. La tesis **no** da una curva de dispersión.
- **CONTRASTE — Sultanova, Kasarova & Nikolov (2009),** *"Dispersion properties of optical
  polymers"*, *Acta Physica Polonica A* **116**, 585–587. Obtenida de
  `refractiveindex.info` (organic → cellulose → Sultanova,
  <https://refractiveindex.info/?shelf=organic&book=cellulose&page=Sultanova>).
  Sellmeier: **n² − 1 = 1.124 λ² / (λ² − 0.011087)**, λ en µm, válida 0.437–1.052 µm.
  Da n = 1.480 / 1.472 / 1.468 / 1.465 a 450 / 550 / 650 / 750 nm; **1.470 a 580 nm →
  coincide con Borgmann**.
- **Salvedad:** ambas son para *celulosa*, no acetato de celulosa. El acetato (diacetato)
  tiene n_D ≈ 1.475–1.49 según acetilación y plastificante (p. ej.
  Long et al., *J. Membrane Sci.*, <https://www.sciencedirect.com/science/article/abs/pii/S0376738800800861>,
  ~1.47–1.48). → adoptar la curva de Sultanova como base y propagar **+0 a +2 %** en n como
  sistemático hacia el valor del acetato.
- **Decisión:** curva de dispersión = Sultanova 2009; valor de anclaje 580 nm = Borgmann
  (concuerdan). Contraste TiO₂ (n = 2.55–2.75) y aire (n = 1) para la figura de mérito, de
  Borgmann §2.2.1.

---

## 7. Datos NO usados (y por qué)

| conjunto | motivo |
|---|---|
| `mediciones 0904\`, `Mediciones random\` | tiras de 2021 no relacionadas, PMMA, pruebas |
| reflectancia de `16_04, 21_04, 23_04, 30_04, 05_05, 07_05` | calibración/fondo en desarrollo, antes del arreglo del 14/05 |
| reflectancia tira A de `14_05, 15_05, 19_05, 21_05, 28_05` | calibración nueva pero superadas por la serie del 02/06 (la que usa el informe). `28_05\patron viejo calibracion nueva` = antecedente directo (misma calibración, 2 regiones) → control cruzado opcional |
| `04_06\Promedio\` | promedios de tiras B/C/D, no A |
| todo lo de PMMA (tiras C/D/E) | fuera de alcance |

---

## 8. Decisiones cerradas (antes: preguntas al usuario)

1. **Transmitancia** tira A (23/04) y tira B (21/04): **válidas** — iluminación directa con fibra,
   sin problema del borde del puerto. Se usan para la cota de μ_a(λ) (Etapa 6).
2. **Espesores** (slide 13): capa porosa 46 / 41 / 40 / 32 µm (m1–m4), medidos a ojo.
   Se **remiden desde las SEM en la Etapa 3** y se comparan con estos.
3. **n(λ):** curva de Sultanova 2009 (Sellmeier), anclada al 1.47 @ 580 nm de Borgmann;
   sistemático +0–2 % hacia el acetato. Ver §6.
4. **Autoría** del informe: **Tomás Chamorro** ("A. Monzani" es seudónimo; editable al final).
