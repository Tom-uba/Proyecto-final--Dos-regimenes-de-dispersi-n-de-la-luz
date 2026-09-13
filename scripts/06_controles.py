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

    fig, axs = plt.subplots(1, 3, figsize=(12.0, 4.2), constrained_layout=True)

    # (a) espesor
    ax = axs[0]
    nombres = list(esp)
    vals = [esp[k]["ds"] for k in nombres]
    ax.barh(range(len(nombres)), vals, color=[GRIS] + [AZUL] * (len(nombres) - 1), height=0.6)
    ds0 = esp["nominal"]["ds"]
    ax.axvspan(ds0 - 0.25 * ds_med, ds0 + 0.25 * ds_med, color=AZUL, alpha=0.10, lw=0)
    ax.axvline(ds_med, color="k", lw=1.4)
    ax.text(ds_med, len(nombres) - 0.35, " medido", fontsize=8.5, va="bottom")
    ax.set_yticks(range(len(nombres)), nombres, fontsize=8.5)
    ax.invert_yaxis()
    ax.set_xlabel("Δs rojo predicho")
    ax.set_title("(a) Espesor: la banda es la tolerancia\npre-registrada (±0.25·Δs medido)", fontsize=9.5)

    # (b) absorción
    ax = axs[1]
    etiquetas = ["sin\nabsorción", "medido\n(tira A)"] + [f"H_abs\n{k}" for k in ab]
    y = [1.0, QA] + [v["Q_pred"] for v in ab.values()]
    col = [GRIS, "k"] + [ROJO] * len(ab)
    ax.bar(range(len(y)), y, color=col, width=0.6)
    ax.errorbar([1], [QA], yerr=[3 * sQ], fmt="none", ecolor=AZUL, capsize=5, lw=1.4)
    ax.set_xticks(range(len(y)), etiquetas, fontsize=8.5)
    ax.set_ylim(min(0.8, min(y) - 0.1), max(y) + 0.15)
    ax.set_ylabel("Q = K(745)/K(600)")
    ax.set_title("(b) Absorción: lo que exigiría producir s₄\n(barra azul: ±3σ del medido)", fontsize=9.5)

    # (c) atribución
    ax = axs[2]
    ks = list(at)
    fD = [at[k]["f_D"] for k in ks]
    fE = [at[k]["f_env"] for k in ks]
    ax.bar(range(len(ks)), fD, color=AZUL, width=0.55, label="tamaño de poro (régimen)")
    ax.bar(range(len(ks)), fE, bottom=fD, color=ROJO, width=0.55, label="entorno (φ, L)")
    ax.axhline(0.75, color="k", ls="--", lw=1)
    ax.set_xticks(range(len(ks)), ks, fontsize=9)
    ax.set_ylabel("fracción del Δs predicho")
    ax.legend(fontsize=8, frameon=False, loc="lower right")
    ax.set_title("(c) Atribución del contraste\n(línea: criterio f_D ≥ 0.75)", fontsize=9.5)

    FIGURES.mkdir(exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(FIGURES / f"06_controles.{ext}", dpi=150)
    print(f"06_controles: Δs medido {ds_med:.2f} | espesor peor "
          f"{max((esp[k]['ds'] - ds0 for k in esp), key=abs):+.2f} | Q medido {QA:.3f}±{sQ:.3f}, "
          f"H_abs " + ", ".join(f"{k} {v['Q_pred']:.3f}" for k, v in ab.items()) +
          " | f_D " + ", ".join(f"{k} {v['f_D']:.2f}" for k, v in at.items()))


if __name__ == "__main__":
    main()
