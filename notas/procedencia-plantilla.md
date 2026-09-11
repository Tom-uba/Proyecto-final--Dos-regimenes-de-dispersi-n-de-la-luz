# Plantilla de procedencia

Al cerrar cada número o figura del informe, dejar esto en el script/docstring que lo produce:

```
RESULTADO:   <qué es, con su valor y unidad>
ENTRADA:     <archivo(s) de datos + qué se leyó de cada uno>
CÁLCULO:     <módulo.función que lo produjo>
DERIVADO vs LIBRERÍA:  <qué se escribió desde cero / qué se llamó (miepython, scipy, …)>
ELECCIONES:  <toda opción con alternativa defendible: banda, umbral, modelo, aproximación>
CHECK:       <checks/check_X.py — qué verifica y con qué criterio>
INCERTIDUMBRE:  <de dónde sale y cómo se propagó>
```

Regla: un número sin CHECK es una afirmación, no un resultado. La evidencia de un check
es siempre un número o una ruta, nunca un adjetivo.
