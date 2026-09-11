"""Figura y tabla: pendiente espectral s = -d ln R / d ln λ por muestra.  [Etapa 2]

RESULTADO:   resultados/02_pendiente.csv + figures/02_pendiente_por_muestra.{pdf,png}
ENTRADA:     data/reflectancia/ (20 espectros, tira A)
CÁLCULO:     dosregimenes.pendiente.medir  (2 métodos × 2 sub-bandas por muestra)
DERIVADO vs LIBRERÍA:  el estimador de s y su error son propios; de scipy solo
             UnivariateSpline, de numpy polyfit con covarianza.
ELECCIONES:  sub-bandas (470–590) y (600–745) nm, dentro de la banda de análisis y
             salteando la máscara instrumental de 560–568 nm. Dos métodos redundantes:
             regresión cuadrática de ln R vs ln λ (s evaluada en el centro geométrico) y
             derivada de un spline suavizado.
CHECK:       checks/check_2_1_consistencia.py, checks/check_2_2_separacion.py
INCERTIDUMBRE:  regresión → covarianza del ajuste pesado por la banda de dispersión;
             spline → desvío de la derivada dentro de la sub-banda.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from dosregimenes import BANDA_NM, FIGURES  # noqa: E402
from dosregimenes import espectros as sp  # noqa: E402
from dosregimenes import pendiente as pd  # noqa: E402

RESULTADOS = RAIZ / "resultados"
COLOR = {1: "#3b6ea5", 2: "#4a9b5c", 3: "#c0504d", 4: "#7b52a1"}
MARCA = {"regresion": "o", "spline": "s"}


def main() -> None:
    esp = sp.cargar_reflectancia(banda=BANDA_NM)
    filas = []
    for m in (1, 2, 3, 4):
        for p in pd.medir(esp[m]):
            filas.append(dict(muestra=p.muestra, metodo=p.metodo,
                              sub_lo=p.subbanda[0], sub_hi=p.subbanda[1],
                              s=round(p.s, 4), s_err=round(p.s_err, 4),
                              curvatura=round(p.curvatura, 4)))

    RESULTADOS.mkdir(exist_ok=True)
    with open(RESULTADOS / "02_pendiente.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)

    subs = pd.SUBBANDAS_NM
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.0), sharey=True)
    for ax, sub in zip(axes, subs):
        for m in (1, 2, 3, 4):
            for met, dx in (("regresion", -0.09), ("spline", 0.09)):
                fila = next(r for r in filas if r["muestra"] == m
                            and r["metodo"] == met and r["sub_lo"] == sub[0])
                ax.errorbar(m + dx, fila["s"], yerr=fila["s_err"], fmt=MARCA[met],
                            color=COLOR[m], ms=6, capsize=3, lw=1.3,
                            mfc="white" if met == "spline" else COLOR[m])
        ax.axvspan(0.5, 3.5, color="0.93", zorder=0)
        ax.set_xticks([1, 2, 3, 4])
        ax.set_xlabel("Muestra")
        ax.set_xlim(0.5, 4.5)
        ax.grid(alpha=0.25, lw=0.6, axis="y")
        ax.set_title(f"{sub[0]:.0f}–{sub[1]:.0f} nm", fontsize=10)
    axes[0].set_ylabel(r"$s = -\,d\ln R\,/\,d\ln\lambda$")
    h = [plt.Line2D([], [], marker="o", color="0.3", ls="", label="regresión"),
         plt.Line2D([], [], marker="s", color="0.3", ls="", mfc="white", label="spline")]
    axes[1].legend(handles=h, fontsize=8.5, loc="upper left")
    fig.suptitle("Pendiente espectral por muestra — gris: régimen de Mie (1–3)", fontsize=10)
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(FIGURES / f"02_pendiente_por_muestra.{ext}", dpi=150)

    resumen = []
    for m in (1, 2, 3, 4):
        ss = [r["s"] for r in filas if r["muestra"] == m]
        resumen.append(f"m{m} {np.mean(ss):.2f}")
    print("02_pendiente_por_muestra: s medio (4 estimaciones c/u) = " + ", ".join(resumen))


if __name__ == "__main__":
    main()
