# Fichas de fuentes

**Objetivo: no volver a abrir los PDF grandes.** Lo que se necesita de cada fuente está
acá. Ir al PDF original solo con `offset`/`limit` para un dato puntual que falte.

---

## Cuaderno de Laboratorio 6 (`…/Labo 6/Cuaderno de Laboratorio 6.pdf`, 54 pág.)

- Proyecto Labo 6: *"Medición de reflectancia y caracterización de películas porosas"*.
  Grupo de Electromagnetismo Aplicado, DF–FCEN–UBA. Directoras: D. Skigin, M. Inchaussandague.
- **Nomenclatura:** letra = tira, número = muestra. Tiras A y B = acetato de celulosa
  (misma fabricación: 180 min sat., 50 MPa, 80 °C, 70 µm nominal). Tiras C/D/E = PMMA.
- **Evolución de la calibración de reflectancia:**
  - Problema: el fondo negro y hasta "el ambiente" daban ~30 % de reflectancia → se
    concluyó que eran rayos que rebotan en el **borde del puerto** de la esfera sin salir.
  - Solución adoptada (14/05 en adelante): fijar el **0 % con la lámpara de la esfera
    encendida y el puerto abierto**. = "calibración nueva".
  - Patrón blanco: el **viejo** (Ocean Optics WS-1, algo amarillento; probaron otros, igual).
  - Parámetros finales: integración 2600 ms, 20 promedios, Boxcar 3, Non-linearity Corr. ON.
  - Anomalía instrumental a **564.1 nm** (depende de la estabilidad térmica de la lámpara).
  - Valores > 100 % cerca de 400 nm son conocidos (hasta 120 % en tira C).
- **02/06:** se re-miden las regiones de la tira A (la que se congela ese día para SEM) →
  `02_06\distintas regiones\CA\` = la Fig. 6. Regiones sobre una línea horizontal, muy
  solapadas por el puerto de 8 mm.
- **Transmitancia (21/04 tira B, 23/04 tira A):** iluminación directa con la fibra (sin
  esfera), integración 3400 ms. Propósito textual: *"medir el camino libre medio"*.
- **SEM (11/06, CMA):** 4 muestras × 2 mitades (arriba/abajo) × 3 regiones × 3–4 aumentos.
  WD ≈ 6.8 mm (varió), EHT = 3 kV.
  - *"abajo: no fuimos más abajo porque se veía que el corte afectó la estructura porosa"*
    → mitades `abajo` con daño de corte.
  - Muestra 4: *"completamente formada por poros con telarañas pero mucho más chicos"*
    (nota: el informe y la presentación dicen "sin telarañas visibles" — inconsistencia
    registrada; para *dos regímenes* da igual, la 4 es nanométrica).
- **Análisis (p. 52–53):** PSD 1–3 con pico ~1.5 µm; *"la reflectancia de un material
  poroso es máxima cuando el tamaño del poro es comparable a la longitud de onda"*.

## Presentación (`…/Labo 6/Presentacion_Laboratorio_6_DeAlbuquerque_Chamorro.pptx.pdf`, 19 slides)

- **Slide 13 — espesores (medidos a ojo, error considerable):**

  | muestra | grosor total | capa porosa |
  |---|---|---|
  | 1 | 83 µm | 46 µm |
  | 2 | 79 µm | 41 µm |
  | 3 | 78 µm | 40 µm |
  | 4 | 78 µm | 32 µm |

- Slide 14: Feret medio común ≈ 1.6 µm (muestras 1–3). Slide 15: muestra 4 ≈ 0.1 µm.
- **Slide 16:** *"Escala porosa distinta → dispersión espectral distinta."*
- **Slide 17 (conclusión):** *"Dos regímenes: las muestras 1–3 son micrométricas; la 4 es
  nanométrica."*

## Borgmann (2023), *Bio-inspired white porous polymers via scCO₂ foaming* (`…/Labo 6/PhD Thesis Luisa Borgmann.pdf`, 155 pág.)

- **§2.2.2 (p. 23):** biopolímeros — celulosa **n ≈ 1.47**, quitina 1.54, queratina 1.55,
  **a ~580 nm** (refs [39,40]).
- **§2.2.1 (p. 21–22):** dispersión por una partícula esférica; C_sca, Q_sca(diámetro, λ, m).
  Fig. 2.2 b calculada con **MiePlot**, luz 550 nm, medio n = 1.5. Q_sca puede superar 1.
  TiO₂ n = 2.55 (anatasa) – 2.75 (rutilo); ZnO n = 2.0; aire n = 1. Para TiO₂ el tamaño
  óptimo de partícula es 200–300 nm.
- No trae curva de dispersión n(λ) — solo el valor puntual 1.47 @ 580 nm.

## Sultanova, Kasarova & Nikolov (2009), *Acta Phys. Pol. A* 116, 585

- vía refractiveindex.info (organic/cellulose/Sultanova). Sellmeier, λ en µm, 0.437–1.052 µm:
  **n² − 1 = 1.124 λ² / (λ² − 0.011087)**.  n(580 nm) = 1.470 (coincide con Borgmann).
- Es la curva de dispersión que usa el proyecto (`dosregimenes.nref`).

## Syurik et al. (2017), *Sci. Rep.* 7:46637 (`…/Labo 6/SciRep7Syurik46637(2017).pdf`)

- Películas porosas de PMMA por scCO₂ (grupo KIT). Ancla externa del **check 5.3**.
- **Material:** PMMA, **n = 1.49 a 600 nm** (dispersión tomada de su ref. 42).
- **Morfología óptima** (50 MPa, 80 °C, 2 h; Fig. 4): diámetro de poro **339 ± 109 nm**,
  fracción de poros **39 %**; capa de 11 µm con R ≈ 60 % a 600 nm. A 60 °C (poros más chicos,
  menor fracción) R es alta a 400 nm y cae ~40 % hacia el rojo.
- **Serie de espesores** (Fig. 5a; 50 MPa, 80 °C; se supone la misma microestructura en toda
  la serie): capas porosas de 9 a 79 µm, sobre vidrio. R_total a 600 nm: **57 % a 9 ± 1 µm**,
  **~70 % a 16 µm**, **90 % a 53 ± 2 µm**. R(800) queda 13 y 7 puntos por debajo de R(400) a 9
  y 53 µm. Capa sin poros de 1–2 µm arriba, restada del espesor.
- **Camino libre de transporte:** l_t = **3.5–4 µm** (400–800 nm), extraído como pendiente de
  T contra 1/L ("ley de Ohm para la luz", siguiendo a Burresi et al. 2014), con T = 1 − R
  suponiendo absorción nula. Advierten que es menos preciso para L < 8 l_t. Ojo: esa pendiente
  incluye la longitud de extrapolación de los bordes y **no es exactamente ℓ***.
- **Medición:** PerkinElmer Lambda 1050, esfera integradora, R total (especular + difusa) a
  8°, referencia Spectralon, 3 posiciones por muestra; cara trasera del vidrio con absorbente
  negro.
- **Cyphochilus** (citado): escamas de 7 ± 1.5 µm con R 65–70 %.
