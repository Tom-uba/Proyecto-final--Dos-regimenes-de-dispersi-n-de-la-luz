# Índice de refracción del sólido, n_sol(λ)

El scatterer es aire dentro del sólido, así que lo que importa es `m = n_aire / n_sol(λ)`
con `n_aire = 1`.

## Curva usada — Sultanova, Kasarova & Nikolov (2009)

*"Dispersion properties of optical polymers"*, **Acta Physica Polonica A 116, 585–587**.
Obtenida de `refractiveindex.info` → organic → cellulose → Sultanova
(<https://refractiveindex.info/?shelf=organic&book=cellulose&page=Sultanova>).

Ajuste de Sellmeier (λ en **µm**), válido 0.437–1.052 µm:

```
n_sol(λ)² − 1 = 1.124 · λ² / (λ² − 0.011087)
```

Valores:

| λ [nm] | n_sol |
|---|---|
| 450 | 1.480 |
| 550 | 1.472 |
| 580 | 1.470 |
| 650 | 1.468 |
| 750 | 1.465 |

## Anclaje — tesis de Borgmann (2023), §2.2.2 (p. 23)

Celulosa: **n ≈ 1.47 a 580 nm** (valor puntual; Borgmann cita sus refs [39,40]).
Coincide con Sultanova a 580 nm (1.470). En sus propios cálculos de Mie (Fig. 2.2 b,
MiePlot) Borgmann usa n_matriz = 1.5.

## Salvedad — celulosa vs. acetato de celulosa

Ambas fuentes son para *celulosa*, no acetato. El acetato (diacetato) tiene
n_D ≈ 1.475–1.49 según grado de acetilación y plastificante
(p. ej. Long et al., *J. Membrane Sci.*,
<https://www.sciencedirect.com/science/article/abs/pii/S0376738800800861>, ~1.47–1.48).

**Cómo se trata:** curva base = Sultanova; se propaga un sistemático de **+0 a +2 %** en
`n_sol` hacia el valor del acetato. Implementado en `dosregimenes.nref` con el parámetro
`bias`.

## Contrastes para la figura de mérito (Borgmann §2.2.1)

TiO₂: n = 2.55 (anatasa) – 2.75 (rutilo). ZnO: n = 2.0. Aire: n = 1.
