# Revisión del informe «Dos regímenes de reflectancia»

## Impresión general

Se entiende bien la pregunta, la separación experimental entre dos poblaciones y el observable central \(\Delta s\).  
La secuencia morfología → dispersión → transporte → reflectancia está expuesta con una honestidad poco habitual sobre sus fallas.  
Cuesta, sin embargo, distinguir qué demuestra el experimento de qué atribuye internamente un modelo cuya pieza decisiva no fue validada.  
La convención no estándar para \(x\), varios símbolos tardíos y algunos pies poco autosuficientes obligan al lector a reconstruir partes del argumento.  
El resultado defendible es una asociación compatible con un cambio de régimen y de orden de magnitud correcto, no una identificación firme del origen físico.

## Hallazgos

### Graves

1. **La conclusión causal excede lo demostrado.** En §5 se afirma: «El contraste queda explicado en su origen físico —dos regímenes separados por el tamaño de poro relativo a la longitud de onda—». Pero el propio informe establece que la muestra 4 no es un conjunto de esferas sino una red bicontinua, que el factor de estructura es imprescindible para ella, que ninguno de los dos cierres reproduce simultáneamente la referencia externa y la muestra 4, y que la absorción no fue excluida. La evidencia sí muestra dos poblaciones morfológicas, dos firmas espectrales y compatibilidad cualitativa con Mie–Rayleigh; no identifica de manera única el mecanismo. La formulación «explicado en su origen físico» contradice esas limitaciones y también es más fuerte que el prudente «sí, en parte». **Arreglo:** reemplazarla por algo como «el cambio de escala de poro es una explicación compatible, que predice el signo y el orden de magnitud, pero la atribución causal no queda establecida»; mantener separadas observación, predicción del modelo y conclusión causal.

### Moderados

2. **No se propagan las incertidumbres que dominan la predicción.** En §4.3 se asigna a \(D\) un ±25–30 % por método y a \(L\) un ±15 %, pero en §4.5 se compara un único \(\Delta s_{\rm pred}=1.77\) con \(\Delta s_{\rm med}=1.23\) y se presenta la razón ×1.43 sin intervalo. El propio §5 reconoce que tampoco se propagan las incertidumbres de tamaño, porosidad y espesor. Así no puede saberse si ×1.43 es discrepancia, acuerdo o precisión espuria, ni sostener cuantitativamente «acierta la magnitud dentro de un 43 %». **Arreglo:** propagar conjuntamente \(P(D)\), escala/segmentación, \(\phi\), \(L\), variación entre regiones y cierre estructural, y reportar intervalos para cada \(s_i\), \(\Delta s\) y su razón. Si no se hace, presentar ×1.43 sólo como estimación nominal.

3. **La convención de \(x\) vuelve ambiguos los límites físicos.** En §2.2 se define \(x=\pi D/\lambda_{\rm vacío}\), pero se advierte que la serie usa \(x_{\rm Mie}=n_{\rm sol}x\). Inmediatamente después se escribe el límite de Rayleigh y la ecuación (2) con «\(x\lesssim1\)», usando en la fórmula de \(Q_{\rm sca}\) el símbolo \(x\) como si fuera el parámetro de Mie. El umbral cambia por un factor ≈1.47, precisamente relevante para F1–F3 y para afirmar dónde termina la transición. **Arreglo:** usar un solo parámetro estándar \(x_m=\pi n_{\rm sol}D/\lambda_0\) en toda la teoría, o reescribir explícitamente \(Q_{\rm sca}=(8/3)(n_{\rm sol}x)^4|(m^2-1)/(m^2+2)|^2\) y rotular todos los intervalos de frontera como expresados en \(x_{\rm vacío}\).

4. **El modelo decisivo se desarrolló mirando el resultado, pero el resumen todavía suena a predicción independiente.** §4.5 declara correctamente que «la prueba no fue ciega» y que una primera versión daba ×2.8–3.2 antes de completar Monte Carlo, factor de estructura y porosidad por muestra. Sin embargo, el resumen dice «sin ajustar ningún parámetro contra los espectros, se predijo» y «el modelo sin ajuste reproduce». No ajustar parámetros no elimina la selección de estructura del modelo con los resultados a la vista. **Arreglo:** en resumen y conclusiones llamarlo cálculo *post hoc* sin parámetros ajustados, o validarlo en nuevas muestras reservadas antes de recuperar la palabra «predicción» en sentido fuerte.

5. **Hay símbolos y construcciones importantes sin definición suficiente.** En §2.4 aparece \(n_{\rm ef}\) dentro de \(k=2\pi n_{\rm ef}/\lambda\), pero no se define ni se indica la regla de mezcla o fuente; el apéndice sólo lo clasifica como calculado. En la figura 5 aparece \(\Gamma\) y sólo se dice que vale 1 sin absorción, sin dar su expresión ni explicar qué mediciones combina. En §2.4, \(p\), F1–F3 y \(F_s\) se introducen con una descripción operacional, pero no se aclara con qué \(m\), longitud de onda o promedio se obtienen los intervalos. **Arreglo:** definir \(n_{\rm ef}\) y citar/justificar su modelo; escribir la fórmula de \(\Gamma\); especificar el procedimiento numérico de F1–F3 y \(F_s\), con su convención de \(x\).

6. **La aproximación esférica entra antes de quedar acotada como supuesto.** La ecuación (3), \(\rho=\phi/\langle\pi D^3/6\rangle\), convierte porosidad en densidad suponiendo poros esféricos separables. Pero §4.3 dice que la muestra 4 es «una red continua» y que su “diámetro” es sólo una escala característica. En ese caso ni una densidad de poros ni un volumen \(\pi D^3/6\) están físicamente bien definidos; esto afecta \(\ell^*\), no sólo el cierre \(S(q)\). **Arreglo:** declarar la hipótesis junto a (3), no recién en resultados/conclusiones, y evitar aplicar \(\rho\) de esferas a la red o justificar una equivalencia efectiva y cuantificar su sesgo.

7. **El resumen afirma que se descartaron explicaciones alternativas, pero una de ellas no se descartó.** La primera oración termina en «se descartaron explicaciones alternativas»; §4.7 y §5 dicen explícitamente que la absorción no quedó excluida. Además, el control de espesor sólo descarta que éste genere por sí solo todo el contraste dentro del modelo. **Arreglo:** cambiar por «se acotó el efecto del espesor y se ensayó, sin excluirla, una hipótesis de absorción».

8. **La significancia está presentada con denominadores distintos y sin datos para auditarlos.** En §4.2 se informa 4.9 σ usando «la incertidumbre del ajuste» y ~60 σ contra «la dispersión entre regiones», pero no se dan los errores numéricos de cada pendiente, el número efectivo de datos ni cómo se tratan correlaciones espectrales y entre regiones. El salto de 4.9 a 60 puede confundir precisión del ajuste con reproducibilidad. **Arreglo:** dar estimaciones ± incertidumbre, definir exactamente ambos σ y elegir como inferencia principal la unidad experimental independiente (regiones/muestras), aclarando el carácter descriptivo de lo demás.

9. **Faltan citas para dos ingredientes no triviales.** Las cuatro ecuaciones tienen una fuente próxima o identificable, pero la regla usada para \(n_{\rm ef}\) no está citada y tampoco queda documentada la expresión concreta que convierte \(L/\ell^*\) en \(R\) en el régimen de Monte Carlo/difusión. Citar a Zhu et al. para bordes extrapolados no basta para reconstruir toda esa cadena. **Arreglo:** citar la regla de medio efectivo y la formulación de transporte empleadas, indicando qué ecuaciones o algoritmos concretos se tomaron de cada fuente.

10. **Varias figuras no son autosuficientes a partir del pie y el texto, y cuatro no son llamadas por número en la prosa.** Las figuras 3–6 aparecen en secuencia, pero el cuerpo no dice «figura 3», «figura 4», etc.; la cercanía física sustituye la referencia. En particular, la figura 3 no define qué mide el eje vertical; la 5 no nombra las variables de sus dos rectas ni define todos los marcadores; y la 6 llama al eje «tamaño típico de poro» mientras la lectura discute \(x\), sin declarar con precisión cuál es la abscisa. **Arreglo:** hacer una llamada numerada antes de cada figura y reescribir cada pie indicando paneles, variables, unidades, codificación visual y mensaje esperado.

### Menores

11. **“Perímetro” es una explicación geométrica incorrecta de \(x\).** §2.2 dice «\(x\) compara el perímetro del poro con la longitud de onda», pero \(\pi D\) es la circunferencia; “perímetro” en 3D resulta impropio y, con la convención de vacío, tampoco es la razón estándar dentro del medio. **Arreglo:** decir «compara la circunferencia asociada al diámetro con la longitud de onda en vacío; el parámetro estándar en el medio es \(x_{\rm Mie}\)».

12. **“Las muestras 1–3 caen enteras del lado Mie” es demasiado absoluto.** En §4.4 la figura resume el 90 % de los poros, no el 100 %, y distribuciones anchas pueden tener colas. **Arreglo:** decir «su masa principal/el 90 % mostrado cae del lado Mie» y dar el criterio exacto detrás de «solape 0.000» (probabilidad, histograma o muestra finita).

13. **La ruta al apéndice no coincide con la entrega.** Al final de §5 se remite a `informe/apendice.pdf`, pero en el material entregado el archivo es `apendice.pdf` en la misma carpeta. **Arreglo:** usar una ruta válida en la versión distribuida o un enlace relativo estable.

14. **La frase sobre las “telarañas” empieza proponiendo una causa que el mismo párrafo no respalda.** §4.8 dice «El faltante de ~0.13 apunta a estructura más fina», pero luego concluye que el control no respalda la hipótesis. **Arreglo:** invertir el orden lógico: «Se probó si el faltante podía asociarse…; el control no la respalda y sólo queda como posibilidad».

15. **La bibliografía es rastreable pero demasiado abreviada para algunos artículos.** Varias entradas carecen de título y páginas completas o DOI; esto no genera citas huérfanas, pero dificulta localizar exactamente el resultado invocado. **Arreglo:** uniformar autoría, título, revista, volumen, páginas/artículo, año y DOI/URL.

## Ecuaciones

| Ecuación | ¿Correcta físicamente? | ¿Símbolos definidos? | ¿Citada? |
|---|---|---|---|
| (1) \(x=\pi D/\lambda\), \(m=n_{aire}/n_{sol}\) | **Sí, como convención propia**, y \(m\) es el contraste correcto para una esfera de aire en sólido. No es el parámetro estándar de Mie si \(\lambda\) es de vacío; el texto lo reconoce, pero después mezcla ambas convenciones. | **Sí** para \(D,\lambda,m,n_{aire},n_{sol}\); convendría definir unidades y distinguir desde el símbolo a \(x_{Mie}\). | **Sí:** Bohren y Huffman (1983); \(n(\lambda)\) se atribuye a Sultanova et al. y Borgmann. |
| (2) \(\sigma_{sca}\propto D^6/\lambda^4\), \(Q_{sca}\to2\) | **Correcta como ley límite**: la primera tiene dimensión de área una vez incluido el factor dependiente de índice y constantes; la segunda es el límite de extinción/dispersión para esfera grande no absorbente. **Ambigua** porque sus condiciones usan el \(x\) de vacío mientras la fórmula de Rayleigh precedente requiere \(x_{Mie}\). | **Parcial:** \(\sigma_{sca},D,\lambda,Q_{sca}\) se presentan, pero no se explicita en la ecuación qué factores se omitieron ni cuál \(x\) fija el límite. | **Sí:** Rayleigh se atribuye a Bohren y Huffman (1983) y el límite 2 a van de Hulst (1957). |
| (3) \(\rho=\phi/\langle\pi D^3/6\rangle\), \(\ell^*=[\rho\langle\sigma_{sca}(1-g)\rangle]^{-1}\) | **Correcta para una población de esferas dispersoras independientes** con promedios consistentes por número. No es directamente válida para una red bicontinua; además, la segunda parte requiere la posterior corrección de dispersión dependiente. | **Sí** para \(\rho,\phi,D,\ell^*,\sigma_{sca},g\) y el promedio sobre \(P(D)\); falta declarar aquí el supuesto esférico y qué ponderación define \(P(D)\). | **Sí, pero de modo algo indirecto:** Bohren y Huffman (1983) se cita en la frase que define \(g\). Sería mejor citar explícitamente toda la relación de transporte. |
| (4) \((d\sigma/d\Omega)_{ef}=(d\sigma/d\Omega)_{1\,poro}S(q)\) | **Correcta como aproximación de factor de estructura** para dispersión dependiente bajo sus supuestos; no es identidad general y su uso en una red bicontinua queda sin validar. | **Parcial:** \(S,q,k,\theta,\eta\) se explican alrededor; \(\Omega\) es sólo implícito y \(n_{ef}\) no se define ni se da su regla de cálculo. | **Sí para los cierres:** Percus–Yevick (1958) y Kotlarchyk y Chen (1983). Falta una cita explícita para la forma general y para \(n_{ef}\). |

## Figuras

| Figura | ¿Se entiende con pie y texto? | ¿Está llamada por número? | Qué falta o sobra |
|---|---|---|---|
| 1 | **Sí, casi por completo.** El texto define eje horizontal (longitud de onda), vertical (fracción reflejada), bandas y conclusión. | **Sí**, en §4.1. | Incluir nm en el pie, identificar allí la codificación de las cuatro muestras y aclarar si la franja es desviación estándar, rango u otra medida de dispersión. La frase «banda de análisis» debería dar sus límites. |
| 2 | **Sí en lo esencial.** Pie, texto y tabla permiten inferir muestra en abscisa y \(s\) en ordenada, además de símbolos y fondo. | **Sí**, en §4.2. | Decir explícitamente los ejes y si las barras son errores estándar, intervalos de confianza u otra incertidumbre. El texto dice sólo «incertidumbre del ajuste». |
| 3 | **Parcialmente.** Se entiende que compara distribuciones de \(D\), sus medianas y tamaños muestrales. | **No** en la prosa; sólo aparece su pie. | Definir eje horizontal con unidad y, sobre todo, el eje vertical: conteo, fracción, densidad lineal o densidad por logaritmo. Explicar qué normalización permite comparar muestras con distinto \(n\). |
| 4 | **Bastante, pero no del todo.** Se distinguen los dos paneles y la conclusión buscada. | **No** en la prosa; sólo aparece su pie. | Dar ejes y unidades del panel derecho, la longitud de onda usada para el panel izquierdo y qué distribución/ponderación produce las barras del 90 %. «Solape 0.000» necesita definición. |
| 5 | **Parcialmente.** El bloque de lectura comunica las conclusiones de espesor y absorción, pero el pie no permite reconstruir las rectas. | **No** en la prosa; sólo aparece su pie. | Nombrar la variable horizontal en cada panel, sus unidades/normalización, definir \(\Gamma\), identificar colores y símbolos y explicar qué conjunto de hipótesis representa «lo demás». |
| 6 | **Parcialmente.** Se entiende la idea del escalón, la banda del modelo, los puntos y la brecha. | **No** en la prosa; sólo aparece su pie. | Aclarar si la abscisa es \(D\), \(x\) o un reescalado de ambos, a qué \(\lambda\) corresponde, y definir «tamaño típico». Indicar qué límite de la banda corresponde a cada cierre; la frase «donde el modelo las ubica» es circular si los puntos usan sus tamaños medidos. |

## Citas y bibliografía

No encontré citas presentes en el texto que falten en la lista, ni referencias de la lista completamente huérfanas: Bohren–Huffman, van de Hulst, Percus–Yevick, Henyey–Greenstein, Kotlarchyk–Chen, Syurik et al., Borgmann, Sultanova et al., Vukusic et al., Wilts et al. y Zhu–Pine–Weitz aparecen en ambos lugares. Los déficits son de precisión y cobertura de ingredientes concretos (especialmente \(n_{ef}\) y el transporte), no de correspondencia formal entre citas y lista.

## Qué está bien

- La pregunta se formula al comienzo y el informe vuelve a ella en la conclusión; la respuesta «sí, en parte» es clara y está mejor calibrada que algunas frases causales posteriores.
- La separación entre observación (espectros y morfología), observable (\(\Delta s\)) y cadena de modelado es pedagógica y permite localizar dónde falla el argumento.
- Se explica correctamente que la pendiente de reflectancia de una lámina no tiene por qué ser 4 aun cuando la dispersión elemental esté en Rayleigh, por saturación y transporte múltiple.
- Los límites de Mie/Rayleigh, la anisotropía de transporte y la necesidad de abandonar difusión cuando \(L/\ell^*\) es pequeño se presentan con buena intuición física.
- El informe no oculta resultados adversos: declara el desarrollo no ciego, el criterio permisivo, las cuatro verificaciones fallidas, el control de absorción mal orientado y el desacuerdo entre cierres.
- La tabla de §4.6 hace visible que ningún tratamiento reproduce simultáneamente la referencia externa y la muestra 4; esa es una presentación útil y honesta.
- La frontera se reporta como intervalo y se distingue expresamente entre «acotar» y «medir»; también se reconoce que no hay muestras dentro de la brecha.
- Los números principales son internamente consistentes: medianas ≈1.75 y 0.10 µm, \(x\approx9.1\) y 0.52, \(s\approx0.21\) y 1.44, \(\Delta s=1.23\), razón nominal ×1.43 y brecha 0.87–5.10 coinciden entre resumen, resultados y conclusiones.
- Las referencias internas a §4.5, §4.6 y al apéndice corresponden a secciones existentes y pertinentes; el apéndice aporta procedencia, estado de verificaciones y limitaciones metodológicas reales.
- La bibliografía no contiene, en lo revisado, referencias enteramente sin uso ni citas sin entrada bibliográfica.
