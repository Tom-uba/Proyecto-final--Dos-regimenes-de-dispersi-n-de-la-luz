"""Controles de la Etapa 6: espesor, absorción y atribución.  [Etapa 6]

RESULTADO:   resultados/06_controles.csv + figures/06_controles.{pdf,png}
ENTRADA:     data/imagej/ (P(D)), data/reflectancia/, data/transmitancia/ (tiras A y B)
CÁLCULO:     dosregimenes.controles (control_espesor, control_absorcion, Q_medido,
             atribucion) → dosregimenes.modelo.cadena
DERIVADO vs LIBRERÍA:  Q_sca de miepython; todo lo demás propio.
ELECCIONES:  las de los docstrings de checks/check_6_1_controles.py y check_6_3_atribucion.py
CHECK:       checks/check_6_1_controles.py, checks/check_6_3_atribucion.py
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
from dosregimenes import FIGURES  # noqa: E402
from dosregimenes import controles as ct  # noqa: E402
from dosregimenes import imagej as ij  # noqa: E402

RESULTADOS = RAIZ / "resultados"
AZUL, ROJO, GRIS = "#33518f", "#a1552f", "0.45"


def main() -> None:
    poros = ij.cargar_poros()
    ds_med = ct.ds_medido()
    esp = ct.control_espesor(poros)
    ab = ct.control_absorcion(poros)
    QA, s_est = ct.Q_medido("A")
    QB, _ = ct.Q_medido("B")
    sQ = float(np.hypot(s_est, QA - QB))
    at = ct.atribucion(poros)

    RESULTADOS.mkdir(exist_ok=True)
    with open(RESULTADOS / "06_controles.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["control", "caso", "valor", "nota"])
        w.writerow(["medido", "Δs rojo", round(ds_med, 4), "s4 - media(s1,s2,s3)"])
        for k, v in esp.items():
            w.writerow(["espesor", k, round(v["ds"], 4), "Δs predicho rojo"])
        w.writerow(["absorcion", "Q medido tira A", round(QA, 4), f"sigma {sQ:.4f}"])
        w.writerow(["absorcion", "Q medido tira B", round(QB, 4), ""])
        for k, v in ab.items():
            w.writerow(["absorcion", f"Q H_abs {k}", round(v["Q_pred"], 4),
                        f"kappa {v['kappa_cm']:.1f} cm-1, A4(745) {v['A4_745']:.3f}, "
                        f"ds123 inducido {v['ds123_inducido']:+.3f}"])
        for k, v in at.items():
            w.writerow(["atribucion", f"f_D {k}", round(v["f_D"], 4), f"Δs total {v['total']:.3f}"])

    # Dos paneles, UN mensaje por panel, los dos sobre una recta numérica: lo que se
    # compara siempre es "dónde cae lo medido respecto de lo que exigiría la hipótesis".
    # La atribución (f_D) son dos números y va al texto del informe, no a un tercer panel.
    fig, axs = plt.subplots(2, 1, figsize=(8.4, 4.2), constrained_layout=True)

    # (a) espesor: todo lo que el espesor puede mover, contra lo medido
    ax = axs[0]
    ds0 = esp["nominal"]["ds"]
    var = [esp[k]["ds"] for k in esp if k != "nominal"]
    ax.hlines(0, min(var), max(var), color=AZUL, lw=8, alpha=0.30)
    ax.plot([ds0], [0], "o", color=AZUL, ms=8, zorder=3)
    ax.plot([ds_med], [0], "D", color="k", ms=8, zorder=3)
    ax.annotate("predicho: nominal y 5 variantes de espesor", (ds0, 0), xytext=(0, 15),
                textcoords="offset points", ha="center", fontsize=9, color=AZUL)
    ax.annotate("medido", (ds_med, 0), xytext=(0, -24), textcoords="offset points",
                ha="center", fontsize=9)
    ax.set_xlim(min(ds_med, min(var)) - 0.3, max(var) + 0.3)
    ax.set_xlabel("contraste Δs en la banda roja")
    ax.set_title("(a) El espesor no genera el contraste", fontsize=10.5, loc="left")

    # (b) absorción: Γ vale 1 sin absorción; la hipótesis lo corre y la medición no
    ax = axs[1]
    ax.axvline(1.0, color=GRIS, ls="--", lw=1.2)
    ax.annotate("sin absorción", (1.0, 0), xytext=(0, 15), textcoords="offset points",
                ha="center", fontsize=9, color=GRIS)
    ax.errorbar([QA], [0], xerr=[3 * sQ], fmt="D", color="k", ms=8, capsize=4, lw=1.3, zorder=3)
    ax.annotate("medido (±3σ)", (QA, 0), xytext=(0, -24), textcoords="offset points",
                ha="center", fontsize=9)
    for i, (k, v) in enumerate(ab.items()):
        ax.plot([v["Q_pred"]], [0], "o", color=ROJO, ms=8, zorder=3)
        ax.annotate(k, (v["Q_pred"], 0), xytext=(0, 15 if i == 0 else -24),
                    textcoords="offset points", ha="center", fontsize=9, color=ROJO)
    ax.set_xlim(min(v["Q_pred"] for v in ab.values()) - 0.12, 1.12)
    ax.set_xlabel("Γ = K(745) / K(600)")
    ax.set_title("(b) Si la muestra 4 cayera por absorción y no por dispersión, Γ estaría acá",
                 fontsize=10.5, loc="left")

    for ax in axs:
        ax.set_ylim(-0.75, 0.75)
        ax.set_yticks([])
        for lado in ("left", "right", "top"):
            ax.spines[lado].set_visible(False)
        ax.grid(alpha=0.20, axis="x", lw=0.6)

    FIGURES.mkdir(exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(FIGURES / f"06_controles.{ext}", dpi=150)
    print(f"06_controles: Δs medido {ds_med:.2f} | espesor peor "
          f"{max((esp[k]['ds'] - ds0 for k in esp), key=abs):+.2f} | Q medido {QA:.3f}±{sQ:.3f}, "
          f"H_abs " + ", ".join(f"{k} {v['Q_pred']:.3f}" for k, v in ab.items()) +
          " | f_D " + ", ".join(f"{k} {v['f_D']:.2f}" for k, v in at.items()))


if __name__ == "__main__":
    main()
