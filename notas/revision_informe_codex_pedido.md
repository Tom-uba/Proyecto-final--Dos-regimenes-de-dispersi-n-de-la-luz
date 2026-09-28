# Revisión de un informe de física

Sos un referee que lee este informe **por primera vez**. Nadie te va a explicar nada: lo que
no se entienda leyéndolo es un defecto del informe, no tuyo. Respondé en español.

En esta carpeta están:

- `informe.pdf` — el informe, 5 páginas, dos columnas. Es lo que se evalúa.
- `apendice.pdf` — documento complementario con las verificaciones y la procedencia.
- `informe_texto.html` y `apendice_texto.html` — los mismos documentos en HTML, por si te
  resulta más cómodo extraer el texto (las figuras van incrustadas en base64; podés ignorarlas).

**Importante sobre las figuras:** no hace falta que las veas. Lo que tenés que juzgar es si
el **pie de figura y el texto que la acompaña alcanzan** para saber qué muestra, qué hay en
cada eje y qué conclusión se supone que uno saca. Si para entender una figura hay que
adivinar, eso es un hallazgo.

Opcional: el código y los datos están en un repositorio público,
`https://github.com/Tom-uba/Proyecto-final--Dos-regimenes-de-dispersi-n-de-la-luz.git`.
Podés clonarlo si querés contrastar algún número, pero **la revisión es del documento**, no
del código: no hace falta correr nada.

---

## Qué revisar

**1. Marco teórico.** ¿Alcanza para seguir los resultados? Buscá específicamente:
- términos, símbolos o conceptos que se usan en los resultados sin haber sido presentados;
- pasos que se dan por sabidos y que un lector de física general no tendría por qué saber;
- definiciones ambiguas o circulares.

**2. Ecuaciones.** Hay cuatro numeradas, y varias expresiones en el texto. Revisá:
- si son correctas como física (límites, casos particulares, consistencia dimensional);
- si cada símbolo que aparece está definido antes o en el momento;
- si están **citadas**: cada ecuación o dato tomado de la literatura debería decir de dónde sale.

**3. Citas y bibliografía.** ¿Hay afirmaciones que piden una cita y no la tienen? ¿Alguna
referencia de la lista que no se cite en el texto, o alguna cita que no esté en la lista?

**4. Figuras.** Para cada una de las seis: ¿se entiende qué muestra, qué representa cada eje
y qué hay que mirar, sólo con el pie y el texto? ¿El texto la llama por su número donde
corresponde? ¿Sobra o falta algo en la explicación?

**5. Resultados y lógica del argumento.** ¿Cada número que aparece está explicado? ¿Las
conclusiones se siguen de lo que se muestra? ¿Hay afirmaciones más fuertes que la evidencia,
o resultados presentados sin su incertidumbre?

**6. Consistencia interna.** ¿Los números coinciden entre el resumen, los resultados, las
tablas y las conclusiones? ¿Las secciones referidas ("§ 4.6", "el apéndice") existen y dicen
lo que se promete?

**7. Redacción y estructura.** Sólo lo que estorbe a la comprensión: párrafos confusos,
saltos lógicos, repeticiones, o cosas que deberían estar en otro lado.

---

## Cómo entregarlo

Escribí `REVISION.md` en esta carpeta, con:

1. **Impresión general** (5 líneas): qué se entiende bien y qué cuesta.
2. **Hallazgos**, ordenados por gravedad (**grave** / **moderado** / **menor**). Cada uno con:
   - dónde está (sección y, si podés, la frase exacta entre comillas),
   - qué problema tiene,
   - una sugerencia concreta de arreglo.
3. **Ecuaciones**: una tabla con las cuatro numeradas — si es correcta, si sus símbolos están
   definidos, si está citada.
4. **Figuras**: una tabla con las seis — si se entiende, qué falta.
5. **Qué está bien**, para no tocarlo.

No maquilles: si algo está mal, decilo. Y si algo te parece bien, decilo también, con la misma
claridad. Lo que no puedas evaluar, anotalo como tal en vez de suponer.
