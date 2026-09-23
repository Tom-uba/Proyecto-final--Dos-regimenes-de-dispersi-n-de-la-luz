"""Figura y tabla: distribución de tamaño de poro P(D) por muestra.  [Etapa 3]

RESULTADO:   resultados/03_PD.csv + figures/03_distribucion_poros.{pdf,png}
ENTRADA:     data/imagej/poros_m1a3_limpios.csv (11437 poros, m1–3, 3000×)
             data/imagej/poros_m4_z4.csv        (9365 poros, m4, 50000×)
CÁLCULO:     dosregimenes.imagej.PD / .resumen
DERIVADO vs LIBRERÍA:  la medición de Feret es del pipeline de Fiji/ImageJ del Labo 6
             (primaria); acá sólo se agrega, resume y grafica. La moda usa
             scipy.stats.gaussian_kde. `dosregimenes.feret` es la segunda implementación
             independiente y se contrasta en el check 3.1, no acá.
ELECCIONES:  cada muestra se toma en su aumento nativo — 3000× para las micrométricas
             (1–3) y 50000× para la nanométrica (4) — que es donde cada una está bien
             resuelta. Eje log porque las dos escalas difieren ~17×.
             Se usan las DOS mitades. Descartar `abajo` (la que tiene daño de corte) mueve
             la mediana +4.1 / −0.6 / −3.8 / +1.0 % en m1/m2/m3/m4: el signo NO es
             consistente, así que es dispersión entre regiones y no un sesgo sistemático
             del daño. Se prefiere entonces el n mayor. Ver notas/log.md.
CHECK:       checks/check_3_1_PD.py (vs trabajo previo y entre pipelines)
             checks/check_3_2_escala.py (la escala de la que cuelga todo esto)
INCERTIDUMBRE:  la dispersión entre estadísticos (media/mediana/moda difieren ~40 % por la
             cola) domina sobre el error estadístico. Se reportan los tres.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from dosregimenes import FIGURES  # noqa: E402
from dosregimenes import imagej as ij  # noqa: E402

RESULTADOS = RAIZ / "resultados"
COLOR = {1: "#3b6ea5", 2: "#4a9b5c", 3: "#c0504d", 4: "#7b52a1"}


def main() -> None:
    poros = ij.cargar_poros()
    datos = {m: ij.PD(m, poros=poros) for m in (1, 2, 3, 4)}
    filas = []

    fig, ax = plt.subplots(figsize=(8.0, 4.6))
    for m, D in datos.items():
        r = ij.resumen(D)
        aum = 50000 if m == 4 else 3000
        filas.append(dict(muestra=m, aumento_x=aum, n=r["n"],
                          media_um=round(r["media"], 4), mediana_um=round(r["mediana"], 4),
                          moda_um=round(r["moda"], 4), p10_um=round(r["p10"], 4),
                          p90_um=round(r["p90"], 4)))
        xs = np.logspace(np.log10(max(D.min(), 1e-3)), np.log10(np.percentile(D, 99.5)), 400)
        dens = gaussian_kde(np.log10(D))(np.log10(xs))
        ax.plot(xs, dens, color=COLOR[m], lw=1.8,
                label=f"Muestra {m}  ({aum//1000}k×,  n={r['n']})")
        ax.fill_between(xs, dens, color=COLOR[m], alpha=0.12, lw=0)
        ax.axvline(r["mediana"], color=COLOR[m], ls=":", lw=1.1, alpha=0.8)

    ax.set_xscale("log")
    ax.set_xlabel("Diámetro de Feret  D  [µm]   (línea punteada: mediana)")
    ax.set_ylabel("densidad  (por década)")
    ax.set_xlim(0.03, 12)
    ax.grid(alpha=0.25, lw=0.6, which="both")
    ax.legend(fontsize=8.5, loc="upper left")
    med13 = np.median(np.concatenate([datos[m] for m in (1, 2, 3)]))
    ax.annotate(f"×{med13/np.median(datos[4]):.0f}", xy=(0.36, ax.get_ylim()[1] * 0.55),
                ha="center", fontsize=10, color="0.3")
    ax.annotate("", xy=(np.median(datos[4]) * 1.25, ax.get_ylim()[1] * 0.5),
                xytext=(med13 * 0.8, ax.get_ylim()[1] * 0.5),
                arrowprops=dict(arrowstyle="<->", color="0.45", lw=1.0))
    ax.set_title("Distribución de tamaño de poro por muestra", fontsize=10)
    fig.tight_layout()

    FIGURES.mkdir(exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(FIGURES / f"03_distribucion_poros.{ext}", dpi=150)

    RESULTADOS.mkdir(exist_ok=True)
    with open(RESULTADOS / "03_PD.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)

    print("03_distribucion_poros: medianas = " +
          ", ".join(f"m{r['muestra']} {r['mediana_um']:.3f} µm" for r in filas) +
          f"  |  separación m1-3 / m4 = {med13/np.median(datos[4]):.1f}×")


if __name__ == "__main__":
    main()
