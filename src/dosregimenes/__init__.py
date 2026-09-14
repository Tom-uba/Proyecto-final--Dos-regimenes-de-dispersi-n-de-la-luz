"""dos-regimenes — caracterización de los dos regímenes de reflectancia
del acetato de celulosa poroso.

Cadena de módulos (ver plan de trabajo):
    espectros   carga y promedio de R(λ), T(λ)   [Etapa 2]
    pendiente   s = -d ln R / d ln λ             [Etapa 2]
    feret       P(D) desde SEM                    [Etapa 3]
    nref        n_sol(λ)                          [Etapa 1/5]
    size_param  x = πD/λ, P(x,λ)                  [Etapa 4]
    mie         Q_sca(x, m), g                    [Etapa 5]
    estructura  factor de estructura S(q), ℓ*     [Etapa 5]
    lamina      R(λ) de lámina por difusión       [Etapa 5]
    montecarlo  transporte radiativo de lámina    [Etapa 5, opcional]
"""
import sys
from pathlib import Path

# Los checks y scripts imprimen µ, σ, ×, subíndices. En una consola de Windows con CP1252
# eso aborta con UnicodeEncodeError (lo encontró la verificación independiente con Codex,
# notas/segunda_opinion_codex.md, hallazgo 7). Se fuerza UTF-8 al importar el paquete.
for _flujo in (sys.stdout, sys.stderr):
    if hasattr(_flujo, "reconfigure") and (_flujo.encoding or "").lower().replace("-", "") != "utf8":
        _flujo.reconfigure(encoding="utf-8")

RAIZ = Path(__file__).resolve().parents[2]
DATA = RAIZ / "data"
FIGURES = RAIZ / "figures"

BANDA_NM = (470.0, 750.0)          # banda de análisis por defecto
MASCARA_NM = (560.0, 568.0)        # pico instrumental de la esfera (~564 nm)

__all__ = ["RAIZ", "DATA", "FIGURES", "BANDA_NM", "MASCARA_NM"]
