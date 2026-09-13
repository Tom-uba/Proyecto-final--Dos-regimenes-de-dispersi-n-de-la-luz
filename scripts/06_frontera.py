"""Frontera acotada: F1–F3, cotas de los datos y barrido del observable.  [Etapa 6]

RESULTADO:   resultados/06_frontera_s.csv (barrido) + resultados/06_frontera.csv (resumen)
             + figures/06_frontera_acotada.{pdf,png}
ENTRADA:     data/imagej/ (P(D)), data/reflectancia/ (s medida por región)
CÁLCULO:     dosregimenes.frontera (fronteras_mie, cota_datos, barrido, cruce)
             → dosregimenes.modelo.cadena (Mie + factor de estructura + Monte Carlo)
DERIVADO vs LIBRERÍA:  Q_sca de miepython; todo lo demás propio.
ELECCIONES:  forma de P(D) de m4 reescalada; entornos (φ, L) de los dos grupos; dos cierres
             de factor de estructura; 40 000 fotones por punto, semilla 13. Ver docstring de
             frontera.py.
CHECK:       checks/check_6_2_frontera.py
INCERTIDUMBRE: barras x ±30 % (sistemático de D); barras s = desvío entre las 5 regiones.
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
from dosregimenes import DATA, FIGURES, MASCARA_NM  # noqa: E402
from dosregimenes import espectros as sp  # noqa: E402
from dosregimenes import frontera as fr  # noqa: E402
from dosregimenes import imagej as ij  # noqa: E402
from dosregimenes import lamina as lm  # noqa: E402
from dosregimenes import modelo as md  # noqa: E402
from dosregimenes.espectros import _leer_txt  # noqa: E402

RESULTADOS = RAIZ / "resultados"
COLOR = {1: "#3b6ea5", 2: "#4a9b5c", 3: "#c0504d", 4: "#7b52a1"}
ESTILO = {("1-3", "monodisperso"): ("#8a3a38", "-"), ("1-3", "desacople"): ("#8a3a38", ":"),
          ("4", "monodisperso"): ("#7b52a1", "-"), ("4", "desacople"): ("#7b52a1", ":")}


def s_regiones(m: int) -> np.ndarray:
    out = []
    for f in sorted((DATA / "reflectancia").glob(f"tira_A_muestra_{m}_*_Reflection*.txt")):
        wl, v = _leer_txt(f)
        ok = (wl >= 600) & (wl <= 745) & ~((wl >= MASCARA_NM[0]) & (wl <= MASCARA_NM[1]))
        out.append(lm.pendiente(wl[ok], v[ok] / 100.0))
    return np.array(out)


def main() -> None:
    poros = ij.cargar_poros()
    filas = fr.barrido(poros)
    RESULTADOS.mkdir(exist_ok=True)
    with open(RESULTADOS / "06_frontera_s.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        w.writeheader()
        for r in filas:
            w.writerow({k: (round(v, 5) if isinstance(v, float) else v) for k, v in r.items()})

    F = fr.fronteras_mie()
    cot = fr.cota_datos(poros)
    R = sp.cargar_reflectancia()
    s_med = {m: md.s_medida(R[m]) for m in (1, 2, 3, 4)}
    s_star = 0.5 * (s_med[4] + np.mean([s_med[m] for m in (1, 2, 3)]))
    Fs = {}
    for ent in fr.ENTORNOS:
        for cierre in ("monodisperso", "desacople"):
            sel = [r for r in filas if r["entorno"] == ent and r["cierre"] == cierre]
            Fs[(ent, cierre)] = fr.cruce([r["x_mediana"] for r in sel], [r["s_rojo"] for r in sel], s_star)

    with open(RESULTADOS / "06_frontera.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["definicion", "x_min", "x_max", "nota"])
        w.writerow(["cota datos", round(cot["inf"], 3), round(cot["sup"], 3), "x4(470)*1.3, min x123(750)*0.7"])
        for k in ("F1", "F2", "F3"):
            w.writerow([k, round(F[k][0], 3), round(F[k][1], 3), "n_sol 470/750 nm, sesgo 0/+2 %"])
        for (ent, cierre), v in Fs.items():
            w.writerow([f"F_s entorno {ent} {cierre}", round(v, 3), round(v, 3), f"s* = {s_star:.3f}"])

    # ---- figura ----
    fig, ax = plt.subplots(figsize=(8.6, 5.0), constrained_layout=True)
    ax.axvspan(cot["inf"], cot["sup"], color="0.85", alpha=0.6, lw=0, zorder=0,
               label="permitido por los datos")
    for k, c in (("F2", "#33518f"), ("F3", "#a1552f")):
        ax.axvspan(*F[k], color=c, alpha=0.25, lw=0, zorder=1)
        ax.text(np.sqrt(F[k][0] * F[k][1]), 2.05, k, ha="center", fontsize=8.5, color=c)
    ax.axvline(1.0, color="0.25", ls="--", lw=1.1, zorder=2)
    ax.text(0.97, 2.05, "F1", ha="right", fontsize=8.5, color="0.25")
    ax.axhline(s_star, color="0.5", lw=0.8, ls="-.", zorder=2)
    ax.text(0.16, s_star + 0.04, f"s* = {s_star:.2f}", fontsize=8, color="0.4")

    for (ent, cierre), (col, ls) in ESTILO.items():
        sel = [r for r in filas if r["entorno"] == ent and r["cierre"] == cierre]
        ax.plot([r["x_mediana"] for r in sel], [r["s_rojo"] for r in sel], ls=ls, color=col,
                lw=1.6, label=f"modelo: entorno {ent}, {cierre}")
        if np.isfinite(Fs[(ent, cierre)]):
            ax.plot([Fs[(ent, cierre)]], [s_star], "v", color=col, ms=6)

    for m in (1, 2, 3, 4):
        xm = fr.x_mediana(ij.PD(m, poros=poros), fr.LAM_C)
        sr = s_regiones(m)
        ax.errorbar([xm], [s_med[m]], xerr=[[xm * 0.3], [xm * 0.3]], yerr=[sr.std()],
                    fmt="o", color=COLOR[m], ms=6, capsize=3, zorder=6)
        ax.annotate(f"m{m}", (xm, s_med[m]), xytext=(6, 6), textcoords="offset points",
                    fontsize=8.5, color=COLOR[m])

    ax.set_xscale("log")
    ax.set_xlim(0.14, 16)
    ax.set_ylim(-0.2, 2.2)
    ax.set_xlabel(r"x mediana $= \pi \tilde D/\lambda$   (λ = 669 nm)")
    ax.set_ylabel("pendiente espectral roja  s  (600–745 nm)")
    ax.grid(alpha=0.22, lw=0.6, which="both")
    ax.legend(fontsize=7.5, loc="upper right", frameon=False)
    ax.set_title("Frontera acotada: teoría de un poro, observable de lámina y datos", fontsize=10)
    FIGURES.mkdir(exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(FIGURES / f"06_frontera_acotada.{ext}", dpi=150)

    todos = [F["F1"][0], F["F2"][0], F["F3"][0], F["F2"][1], F["F3"][1]] + \
        [v for v in Fs.values() if np.isfinite(v)]
    print(f"06_frontera: cotas datos [{cot['inf']:.2f}, {cot['sup']:.2f}] | F2 {F['F2'][0]:.2f}-{F['F2'][1]:.2f} "
          f"F3 {F['F3'][0]:.2f}-{F['F3'][1]:.2f} | F_s " +
          ", ".join(f"{e}/{c} {v:.2f}" for (e, c), v in Fs.items()) +
          f" | frontera [{min(todos):.2f}, {max(todos):.2f}]")


if __name__ == "__main__":
    main()
