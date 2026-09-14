# Informe de verificación independiente

## 1. Resumen

El repositorio se instala y reproduce desde cero, con una salvedad de codificación de consola en Windows.
La figura 04, su CSV y los 20 checks reproducen los números de `run.log`; fallan los mismos cuatro checks (5.3, 5.7, 6.1 y 6.2).
La separación morfológica y espectral entre {1,2,3} y 4 está muy bien demostrada, y la implementación pasa controles numéricos sensatos.
No está demostrada con igual fuerza la atribución causal cuantitativa: el cierre de dispersión dependiente falla y ninguno de sus dos extremos reproduce por sí solo la muestra 4.
Mi veredicto es **“sí, en parte” como hipótesis consistente y plausible, pero no como explicación cuantitativa cerrada**.

## 2. Reproducción

| Paso | Resultado | Evidencia |
|---|---|---|
| Clonado | **PASA.** Se clonó el repositorio público en `./repo`, HEAD `c97f371`. No se escribió en el remoto. | `git clone ... repo`; `git log -1 --oneline` → `c97f371 Etapa 7: README...`. |
| Instalación indicada por README | **PASA.** `uv sync` creó `.venv`, usó CPython 3.14.7 e instaló 21 paquetes desde `uv.lock`. | Comando `uv sync`, código 0. No hubo que elegir versiones ni editar archivos. |
| Figura 04 | **PASA.** Generó PNG/PDF y mostró `x` mediana m1/m2/m3/m4 = 9.11/9.08/9.18/0.52, hueco ×5.1 y fracción de m4 sobre `x=1` 16.7% a 470 nm → 1.5% a 750 nm. | `uv run python scripts/04_mapa_regimenes.py`; inspección visual de `figures/04_mapa_regimenes.png`. |
| CSV de figura 04 | **PASA, idéntico.** | `git diff -- resultados/04_banda_x.csv` y `git status --short`: sin salida. |
| Batería, intento literal | **FALLA de reproducibilidad documental.** Abortó luego de 2 checks al imprimir Unicode bajo CP1252. | `uv run python checks/run_checks.py` → `UnicodeEncodeError` en `checks/run_checks.py:33`. |
| Batería, corrección ambiental | **PASA como reproducción.** Con `PYTHONUTF8=1` terminó en ~12 min, imprimió 4 fallas y todos los valores coincidieron con `run.log`. | `$env:PYTHONUTF8='1'; uv run python checks/run_checks.py` → `4 falla(s).` |
| Figura 06 | **PASA.** No venía versionada, tal como avisa el README; se regeneró desde el script. | `$env:PYTHONUTF8='1'; uv run python scripts/06_frontera.py`; inspección visual y `git diff` de sus CSV. |

Hasta dónde llegué: completé todos los pasos pedidos. Lo único que hubo que adivinar fue activar UTF-8 para la consola. No tuve que modificar código, elegir parámetros ni reconstruir comandos fuera del README. La ausencia inicial de los PNG no es un error: `README.md` dice explícitamente que no se versionan.

## 3. Checks

| Check | Resultado reproducido | ¿Coincide con `run.log`? |
|---|---:|---|
| 0.1 promedio vs Fig. 6 | PASA | Sí, incluidos R450=92%, R750=46% y caída relativa ×2.9. |
| 2.1 robustez de pendiente | PASA | Sí, peor discrepancia 5%. |
| 2.2 separación espectral | PASA | Sí, Δs azul 0.71 y rojo 1.23. |
| 2.3 deriva de lámpara | PASA | Sí, cambios 0.004/0.008. |
| 3.1 P(D) | PASA | Sí, medianas 1.75/0.100 µm y diferencia entre pipelines +11%. |
| 3.2 escala TIFF | PASA | Sí, peor desvío +1.9%. |
| 3.3 espesores | PASA | Sí, desvíos -0.6/+0.4/+0.2/+2.3%. |
| 4.1 grupos en x | PASA | Sí, solape contra m4 0.000 y hueco ×5.1. |
| 5.1 límites de Mie | PASA | Sí, potencia de Rayleigh y `Q_sca=2.0196`. |
| 5.2 predicción Δs | PASA | Sí, 1.77 vs 1.23 (×1.43). |
| 5.3 ancla Syurik | **FALLA** | Sí, desvíos -0.12/-0.10/-0.06. |
| 5.4 límites S(q) | PASA | Sí. |
| 5.5 Monte Carlo | PASA | Sí, balístico y difusión (-4.2%). |
| 5.6 desacople | PASA | Sí, identidades y límites numéricos. |
| 5.7 hipótesis polidispersa | **FALLA** | Sí, falla s4, rms(T) y Δs. |
| 6.0 absorción MC | PASA | Sí, error máximo 0.0001. |
| 6.1 espesor/absorción | **FALLA** | Sí; espesor pasa, absorción no queda excluida. |
| 6.2 frontera | **FALLA** | Sí, 3 de 4 cruces F_s fuera de las cotas. |
| 6.3 atribución | PASA | Sí, f_D=0.81/0.99. |
| 6.4 telarañas | PASA (implementación) | Sí; la lectura científica reportada es “no respaldado”. |

## 4. Hallazgos críticos

### Graves

1. **La evidencia no permite convertir “compatible con un cambio de régimen” en una atribución causal cuantitativa del 81–99%.** Verificado: el cierre monodisperso da `s4=1.84` frente a 1.44, mientras el desacople da 0.62; este último también da Δs=0.57 frente a 1.23 y rms(T)=0.229 (`run.log`, checks 5.2 y 5.7). Aun así, 6.3 declara 81% y 99% porque reparte, *dentro de esos mismos modelos*, un contraste calculado mediante efectos de Shapley (`src/dosregimenes/controles.py:163-186`). El 99% proviene precisamente del cierre que falla de forma fuerte. Además, las cuatro muestras no constituyen una intervención que cambie sólo D: cambian porosidad, espesor y topología. **Sugerencia:** presentar 81–99% como sensibilidad/atribución interna del modelo, no como fracción experimentalmente identificada; exigir un cierre validado o nuevas muestras que desacoplen D, φ, espesor y posición en la tira.

2. **La idealización geométrica central es especialmente frágil para m4.** La propia procedencia describe m4 como una red bicontinua y dice que requiere una longitud característica/ancho de ligamento, no diámetro de poro cerrado (`data/PROCEDENCIA.md:134-135`). Sin embargo, la cadena usa una P(D) como esferas de aire independientes para Mie (`src/dosregimenes/mie.py:3-20`) y luego cierres de esferas duras. Las fallas 5.3, 5.7 y 6.2 son coherentes con esta limitación. **Sugerencia:** medir correlaciones espaciales/estructura 2D o 3D de m4 y usar un modelo electromagnético para medio bicontinuo (o, como mínimo, validar un S(q) medido), antes de sostener una explicación cuantitativa.

### Moderados

3. **El check 5.2 es una prueba cualitativa bastante permisiva, no una validación cuantitativa fuerte.** Su gate sólo pide signo y razón entre 0.5 y 2 (`checks/check_5_2_prediccion.py:11-13,79-88`). Pasa con error de +43% en Δs; las pendientes absolutas predicha/medida son 0.06/0.19, 0.10/0.20, 0.06/0.23 y 1.84/1.44. El signo correcto es esperable al comparar poros x~9 con x~0.5. **Sugerencia:** incluir incertidumbres de entradas y Monte Carlo, evaluar bondad espectral sobre todos los λ y fijar una tolerancia ligada a esas incertidumbres, no un factor 2.

4. **El pre-registro de 5.2 no es auditable dentro del repositorio.** `git log -- checks/check_5_2_prediccion.py` muestra un único commit, `a35c429`, cuyo mensaje ya dice que el check pasa y que la razón es 1.43; criterio, código, resultado y entrada de log entraron juntos. En contraste, 5.7 (`286b7f2`) y 6.x (`07072ac`) sí tienen commits separados anteriores a resultados. Esto no demuestra acomodo, pero tampoco permite verificar el “fijado antes” desde el artefacto entregado. **Sugerencia:** para futuras pruebas, commit firmado/etiquetado del protocolo antes de ejecutar, con hash citado en el informe.

5. **El control de absorción no soporta inferencia a 3σ con el tratamiento de error actual.** R es del 02/06 y T de tira A del 23/04; tira B es del 21/04 (`data/PROCEDENCIA.md:231-242`). `Q_medido` propaga sólo el error estándar entre cinco regiones de R y considera T exacta (`src/dosregimenes/controles.py:91-112`); luego usa la diferencia A–B como un único sistemático. No incorpora repetición, incertidumbre instrumental/correlaciones de T ni la incertidumbre de emparejar campañas y tiras. El propio resultado más favorable a H_abs queda a sólo 2.1σ (`notas/log.md:903-910`). **Sugerencia:** medir R y T simultáneas y absolutas sobre las mismas regiones, con réplicas; modelar la covarianza completa y registrar un contraste bilateral correcto.

6. **“Los datos ubican la transición en [0.87,5.1]” debe leerse sólo como un intervalo vacío entre dos cúmulos.** Las cotas se construyen con las medianas extremas multiplicadas por un sistemático elegido de ±30% (`src/dosregimenes/frontera.py:13-17,61-67`); no hay muestras dentro de la transición. El propio check 6.2 falla: F_s depende del cierre y toma 0.38–1.19 (`run.log`; `notas/log.md:912-925`). **Sugerencia:** decir “los datos sólo acotan una brecha [0.87,5.10]” y fabricar/medir muestras con x intermedio para localizar la frontera.

### Menores

7. **La ruta de reproducción no es literalmente robusta en la consola Windows usada.** Los caracteres `—`, `×`, subíndices y griegos hacen fallar `print` bajo CP1252 (`checks/run_checks.py:33`). **Sugerencia:** documentar `PYTHONUTF8=1`, ejecutar Python con `-X utf8`, o reconfigurar `stdout` dentro del runner.

8. **Las incertidumbres morfológicas no se propagan al resultado principal.** Se reconoce ±25–30% por segmentación y que los dos pipelines comparten las mismas imágenes (`data/PROCEDENCIA.md:219-224`), pero 5.2 usa una P(D), φ y L nominales y un umbral fijo. **Sugerencia:** Monte Carlo jerárquico o análisis global de sensibilidad que entregue un intervalo para Δs_pred y f_D.

No encontré un error de unidades en `x`: el proyecto distingue correctamente `x=πD/λ0` del eje y `x_Mie=n_sol x` dentro de `miepython` (`src/dosregimenes/mie.py:6-25`). Tampoco encontré una normalización obviamente incorrecta en los límites de Mie, el factor de estructura o el conteo del Monte Carlo; los checks 5.1, 5.4–5.6 y 6.0 son controles pertinentes y reproducibles.

## 5. Qué está bien sostenido

- **Dos poblaciones morfológicas muy separadas:** medianas 1.75 y 0.100 µm; `x` medianas ~9.1 y 0.52; solape numérico 0.000 y hueco p95–p5 ×5.1. Un sesgo razonable de escala no borra esa separación.
- **Dos comportamientos espectrales observados:** Δs rojo=1.23 y azul=0.71, con separación grande entre grupos. La elección de Δs cancela correctamente un sesgo multiplicativo común del patrón.
- **La convención de x está controlada:** el código convierte a la longitud de onda en el medio antes de llamar a Mie.
- **La implementación básica está bien testeada:** límites de Rayleigh y difracción, límites exactos de Percus–Yevick/desacople, balance R+T, límite difusivo y absorción balística reproducen referencias internas/analíticas.
- **El espesor nominal no parece generar el contraste dentro de este modelo:** variarlo ±15% o intercambiarlo mueve Δs como máximo 0.16 frente a 1.23 medido.
- **Las fallas no fueron ocultadas:** `run.log`, README y log nombran las cuatro, y los pre-registros 5.7 y 6.x son comprobables en el historial Git. La discusión reconoce explícitamente la calibración, la absorción no excluida, la topología de m4 y el faltante de pendiente de m1–3.

## 6. Veredicto sobre “sí, en parte”

**Acepto “sí, en parte” sólo en sentido prudente:** los datos muestran inequívocamente dos escalas de estructura y dos respuestas espectrales, y Mie predice la dirección correcta del cambio. Eso hace que el cambio de régimen sea una explicación física plausible y probablemente importante.

No aceptaría todavía las formulaciones más fuertes —“lo produce mayoritariamente” o “el tamaño carga 81–99%”— como conclusiones experimentales. Son resultados internos de un modelo cuyo eslabón dominante para m4 no está validado, con un check principal de tolerancia amplia, una geometría esférica discutible y absorción no excluida. Antes de aceptar una respuesta cuantitativa pediría: muestras con tamaños intermedios y factores controlados, R/T absolutas simultáneas, caracterización estructural de la red bicontinua, propagación completa de incertidumbres y validación externa de un cierre de dispersión dependiente.
