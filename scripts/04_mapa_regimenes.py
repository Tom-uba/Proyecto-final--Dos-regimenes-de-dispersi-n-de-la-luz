"""Figura de cabecera: mapa de regímenes en el eje x = πD/λ.  [Etapa 4]

RESULTADO:   resultados/04_banda_x.csv + figures/04_mapa_regimenes.{pdf,png}
ENTRADA:     data/imagej/  (P(D) por muestra, Etapa 3)
CÁLCULO:     dosregimenes.size_param.nube_x / .banda_x / .solape
DERIVADO vs LIBRERÍA:  x = πD/λ y los resúmenes son propios; de scipy sólo gaussian_kde
             para dibujar densidades y calcular el solape.
ELECCIONES:  λ recorre la BANDA DE ANÁLISIS (470–750 nm), que es donde se midió la
             reflectancia — no el "visible" convencional 400–700 nm. Con 400–700 el
             cuadro es el mismo. La frontera es F1: x = 1 (informe/teoria.md §6).
             Cada muestra se toma en su aumento nativo (3000× las micrométricas, 50000×
             la nanométrica).
CHECK:       checks/check_4_1_mapa.py
INCERTIDUMBRE:  el ancho de cada nube ya incluye la polidispersión de los poros y el
             recorrido de λ. Encima va el ±25–30 % sistemático de D (PROCEDENCIA §4bis),
             que desplaza cada nube en bloque sin acercarlas entre sí.
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
from dosregimenes import BANDA_NM, FIGURES  # noqa: E402
from dosregimenes import imagej as ij  # noqa: E402
from dosregimenes import size_param as sx  # noqa: E402

RESULTADOS = RAIZ / "resultados"
COLOR = {1: "#3b6ea5", 2: "#4a9b5c", 3: "#c0504d", 4: "#7b52a1"}
AZUL, ROJO = "#33518f", "#a1552f"


def main() -> None:
    poros = ij.cargar_poros()
    D = {m: ij.PD(m, poros=poros) for m in (1, 2, 3, 4)}
    nubes = {m: sx.nube_x(D[m]) for m in (1, 2, 3, 4)}
    B = {m: sx.banda_x(m, D[m]) for m in (1, 2, 3, 4)}

    fig = plt.figure(figsize=(10.0, 5.0), constrained_layout=True)
    gs = fig.add_gridspec(1, 2, width_ratios=[2.2, 1.0])
    ax = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])

    # ---- panel izquierdo: el mapa ----
    ax.axvspan(0.02, sx.FRONTERA, color=AZUL, alpha=0.07, zorder=0)
    ax.axvspan(sx.FRONTERA, 200, color=ROJO, alpha=0.07, zorder=0)
    ax.axvline(sx.FRONTERA, color="0.25", ls="--", lw=1.3, zorder=5)

    for m in (1, 2, 3, 4):
        lx = np.log10(nubes[m])
        g = np.linspace(lx.min(), lx.max(), 500)
        # normalizada a pico 1: lo que se compara es ubicación y ancho, no la altura
        # (que depende del tamaño de cada población y del ancho de banda del KDE).
        dens = gaussian_kde(lx)(g)
        dens = dens / dens.max()
        ax.plot(10 ** g, dens, color=COLOR[m], lw=1.8, zorder=4)
        ax.fill_between(10 ** g, dens, color=COLOR[m], alpha=0.13, lw=0, zorder=3)
        y = -0.09 - 0.06 * (m - 1)
        ax.plot([B[m].x_p5, B[m].x_p95], [y, y], color=COLOR[m], lw=2.6,
                solid_capstyle="butt", zorder=4)
        ax.plot([B[m].x_mediana], [y], "o", color=COLOR[m], ms=5.5, zorder=5)

    p5_123 = min(B[m].x_p5 for m in (1, 2, 3))
    ax.annotate("", xy=(p5_123, 0.42), xytext=(B[4].x_p95, 0.42),
                arrowprops=dict(arrowstyle="<->", color="0.4", lw=1.1))
    ax.text(np.sqrt(p5_123 * B[4].x_p95), 0.46, f"×{p5_123/B[4].x_p95:.1f}",
            ha="center", fontsize=9.5, color="0.3")
    ax.text(0.055, 1.34, "Rayleigh / transición\n$\\sigma_{sca}\\propto\\lambda^{-4}$",
            fontsize=9, color=AZUL, ha="left", va="top")
    ax.text(85, 1.34, "Mie / grande\n$Q_{sca}\\to 2$",
            fontsize=9, color=ROJO, ha="right", va="top")
    ax.text(sx.FRONTERA * 1.15, 1.40, "F1:  x = 1", fontsize=8.5, color="0.25", ha="left")
    ax.text(0.055, -0.30, "barras: p5–p95", fontsize=8, color="0.45", ha="left")

    # etiquetas directas sobre las curvas: se leen mejor que una leyenda y no tapan nada
    ax.text(B[4].x_mediana, 1.10, f"Muestra 4\nx̃ = {B[4].x_mediana:.2f}", ha="center",
            va="bottom", fontsize=9, color=COLOR[4])
    ax.text(9.1, 1.10, "Muestras 1–3\nx̃ ≈ 9.1", ha="center", va="bottom",
            fontsize=9, color="#8a3a38")

    ax.set_xscale("log")
    ax.set_xlim(0.05, 100)
    ax.set_ylim(-0.34, 1.45)
    ax.set_yticks([])
    ax.set_xlabel(r"parámetro de tamaño   $x = \pi D/\lambda$"
                  f"        (λ ∈ {BANDA_NM[0]:.0f}–{BANDA_NM[1]:.0f} nm)")
    ax.set_ylabel("densidad de P(x)  (normalizada)", fontsize=9)
    ax.grid(alpha=0.22, lw=0.6, axis="x", which="both")
    ax.set_title("Las cuatro muestras sobre el eje de regímenes", fontsize=10)

    # ---- panel derecho: la cola de la muestra 4 cruzando la frontera ----
    lam = np.linspace(BANDA_NM[0], BANDA_NM[1], 60)
    frac = [np.mean(sx.x_de(D[4], l).ravel() > sx.FRONTERA) * 100 for l in lam]
    ax2.plot(lam, frac, color=COLOR[4], lw=2.0)
    ax2.fill_between(lam, frac, color=COLOR[4], alpha=0.15, lw=0)
    for l, dx, dy, ha in ((470, 14, 4, "left"), (750, -6, 8, "right")):
        f = np.mean(sx.x_de(D[4], float(l)).ravel() > sx.FRONTERA) * 100
        ax2.plot([l], [f], "o", color=COLOR[4], ms=5, zorder=4)
        ax2.annotate(f"{f:.1f} %", xy=(l, f), xytext=(dx, dy),
                     textcoords="offset points", ha=ha, fontsize=9.5, color=COLOR[4])
    ax2.set_xlabel("λ [nm]")
    ax2.set_ylabel("% de poros de la muestra 4 con x > 1", fontsize=9)
    ax2.grid(alpha=0.25, lw=0.6)
    ax2.set_xlim(BANDA_NM[0] - 5, BANDA_NM[1] + 5)
    ax2.set_ylim(0, 21)
    ax2.set_title("Sólo en el azul parte de la muestra 4\nalcanza el régimen eficiente",
                  fontsize=9.5)

    FIGURES.mkdir(exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(FIGURES / f"04_mapa_regimenes.{ext}", dpi=150)

    RESULTADOS.mkdir(exist_ok=True)
    with open(RESULTADOS / "04_banda_x.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["muestra", "n_pares", "x_p5", "x_p25", "x_mediana", "x_p75", "x_p95",
                    "frac_sobre_x1", "lam_min_nm", "lam_max_nm"])
        for m in (1, 2, 3, 4):
            b = B[m]
            w.writerow([m, b.n, round(b.x_p5, 3), round(b.x_p25, 3), round(b.x_mediana, 3),
                        round(b.x_p75, 3), round(b.x_p95, 3),
                        round(b.frac_sobre_frontera, 4), BANDA_NM[0], BANDA_NM[1]])

    print("04_mapa_regimenes: x mediana = " +
          ", ".join(f"m{m} {B[m].x_mediana:.2f}" for m in (1, 2, 3, 4)) +
          f"  |  hueco x{p5_123/B[4].x_p95:.1f}  |  m4 con x>1: "
          f"{frac[0]:.1f}% en 470 nm -> {frac[-1]:.1f}% en 750 nm")


if __name__ == "__main__":
    main()
