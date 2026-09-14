Sos un verificador independiente. No conocés este proyecto y no tenés que confiar en lo que dice: tu trabajo es comprobarlo. Respondé en español.

Proyecto: repositorio público
https://github.com/Tom-uba/Proyecto-final--Dos-regimenes-de-dispersi-n-de-la-luz.git
Es un proyecto de física (dispersión de luz en láminas porosas de acetato de celulosa) hecho por un estudiante con ayuda de un agente de IA (Claude). La pregunta y la respuesta están al principio del README.

Tu directorio de trabajo es la carpeta actual. Todo lo que hagas va dentro de ella. NO modifiques el repositorio remoto (nada de push, ni issues, ni PR).

## Parte A — Prueba de reproducción (usá SÓLO el README como guía)

1. Cloná el repo en `./repo`.
2. Seguí las instrucciones del README para instalar el entorno (`uv` ya está instalado en esta máquina).
3. Reproducí la figura de cabecera: `scripts/04_mapa_regimenes.py`. Compará lo que imprime y el `resultados/04_banda_x.csv` que genera contra el que viene versionado en el repo (usá `git diff`/`git status` para ver si cambió).
4. Corré la batería de checks (`checks/run_checks.py`). Tarda 15–20 minutos; si tu herramienta tiene timeout, corré los checks de a uno. Compará cada línea con `run.log` del repo: ¿dan los mismos números? El README dice que se esperan 4 fallas.
5. Anotá hasta dónde llegaste, qué falló de las instrucciones y qué tuviste que adivinar.

## Parte B — Segunda opinión crítica

Leé con ojo de referee: `README.md`, `run.log`, `notas/log.md` (sobre todo las entradas del 2026-09-13), `informe/teoria.md`, y el código de `src/dosregimenes/` y `checks/` que sostiene las afirmaciones principales (checks 4.1, 5.2, 6.1, 6.2, 6.3). Mirá las figuras `figures/04_mapa_regimenes.png` y `figures/06_frontera_acotada.png` (regeneralas si hace falta: la de frontera tarda ~10 min con `scripts/06_frontera.py`).

Buscá, con evidencia concreta (archivo:línea, número, comando):
- errores de física o de código (unidades, convenciones de x, normalizaciones, estadística, un check que no verifica lo que dice);
- afirmaciones que el código o los números no sostienen, o que están sobre-vendidas;
- inconsistencias entre números del log, del run.log y lo que el código produce;
- criterios de checks que se hayan acomodado al resultado;
- lo que un referee pediría antes de aceptar la respuesta "sí, en parte".

Separá lo que verificaste corriendo algo de lo que es opinión. No inventes problemas para llenar la lista: si algo está bien, decilo.

## Entrega

Escribí el informe en `./INFORME_CODEX.md` con estas secciones:
1. Resumen (5 líneas).
2. Reproducción: tabla paso → resultado → evidencia.
3. Checks: tabla check → PASA/FALLA reproducido → ¿coincide con run.log?
4. Hallazgos críticos, ordenados por gravedad (grave / moderado / menor), cada uno con evidencia y sugerencia.
5. Qué está bien sostenido.
6. Veredicto sobre la respuesta "sí, en parte".
