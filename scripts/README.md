# scripts/

Un script por figura del informe. Nombre = `<etapa><n>_<slug>.py`, mismo slug que la
figura en `figures/`. Cada script:

- se corre con `uv run python scripts/<nombre>.py`,
- importa de `dosregimenes`, lee de `data/`, escribe en `figures/`,
- imprime **una línea** al terminar (qué figura generó y su número clave).

Todavía ninguno — se agregan desde la Etapa 2.
