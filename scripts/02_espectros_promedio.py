"""Figura: R(λ) promedio de las 4 muestras con su banda de dispersión.  [Etapa 2]

RESULTADO:   figures/02_espectros_promedio.{pdf,png} + λ de cruce de la muestra 4
ENTRADA:     data/reflectancia/tira_A_muestra_{1..4}_{5 regiones}_Reflection*.txt
CÁLCULO:     dosregimenes.espectros.cargar_reflectancia (media y desvío entre regiones)
DERIVADO vs LIBRERÍA:  promedio/desvío propios; matplotlib solo para dibujar
ELECCIONES:  se dibuja 400–800 nm para contexto, pero se sombrea la banda de análisis
             (470–750 nm) y se marca la máscara instrumental (560–568 nm).
CHECK:       checks/check_0_1_fig6.py (el promedio reproduce la Fig. 6 del informe)
INCERTIDUMBRE:  banda = ±1σ entre las 5 regiones medidas de cada muestra
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from dosregimenes import BANDA_NM, FIGURES, MASCARA_NM  # noqa: E402
from dosregimenes import espectros as sp  # noqa: E402

COLOR = {1: "#3b6ea5", 2: "#4a9b5c", 3: "#c0504d", 4: "#7b52a1"}


def main() -> None:
    esp = sp.cargar_reflectancia(banda=(400.0, 800.0))
    lam = esp[1].lam

    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    ax.axvspan(*BANDA_NM, color="0.92", zorder=0, label="banda de análisis")
    ax.axvspan(*MASCARA_NM, color="#d9b38c", alpha=0.55, zorder=1,
               label="máscara instrumental (564 nm)")

    for m in (1, 2, 3, 4):
        e = esp[m]
        ax.plot(lam, e.R, color=COLOR[m], lw=1.6, zorder=3, label=f"Muestra {m}")
        ax.fill_between(lam, e.R - e.sigma, e.R + e.sigma,
                        color=COLOR[m], alpha=0.18, lw=0, zorder=2)

    # cruce de la muestra 4 con el promedio de 1-3
    cluster = np.mean([esp[m].R for m in (1, 2, 3)], axis=0)
    dif = esp[4].R - cluster
    sel = (lam > 500) & (lam < 700)
    idx = np.where(np.diff(np.sign(dif[sel])))[0]
    lam_cruce = float(lam[sel][idx[0]]) if len(idx) else float("nan")
    if np.isfinite(lam_cruce):
        ax.axvline(lam_cruce, color="0.35", ls=":", lw=1.1, zorder=4)
        ax.annotate(f"cruce ≈ {lam_cruce:.0f} nm", xy=(lam_cruce, 0.5),
                    xytext=(lam_cruce + 12, 0.46), fontsize=8.5, color="0.25")

    ax.set_xlabel("Longitud de onda  λ  [nm]")
    ax.set_ylabel("Reflectancia difusa  R")
    ax.set_xlim(400, 800)
    ax.set_ylim(0.35, 1.05)
    ax.grid(alpha=0.25, lw=0.6)
    ax.legend(fontsize=8.5, ncol=2, loc="upper right", framealpha=0.9)
    ax.set_title("Reflectancia media por muestra — tira A, 5 regiones c/u (02/06/2026)",
                 fontsize=10)
    fig.tight_layout()

    FIGURES.mkdir(exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(FIGURES / f"02_espectros_promedio.{ext}", dpi=150)

    r = {m: np.interp([450, 550, 650, 750], lam, esp[m].R) for m in (1, 2, 3, 4)}
    print(f"02_espectros_promedio: cruce m4 ≈ {lam_cruce:.0f} nm; "
          f"R(450)/R(750) = " + ", ".join(f"m{m} {r[m][0]:.2f}/{r[m][3]:.2f}" for m in (1, 2, 3, 4)))


if __name__ == "__main__":
    main()
