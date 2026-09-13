"""check 6.4 — control de estructura interna: telarañas vs residuos de m1–3.

PRE-REGISTRADO (notas/log.md, 2026-09-13 g).

Qué se gatea: sólo la IMPLEMENTACIÓN. El índice de telaraña portado al repo
(`dosregimenes.telarana`) debe reproducir la prueba de factibilidad: mismo orden
m3 > m2 > m1 y cada media dentro de ±15 % (3.26 / 3.98 / 5.24 µm⁻¹).

Qué se reporta sin gatear, y por qué: con tres muestras la correlación de rangos de
Spearman sólo puede valer −1, −0.5, 0.5 o 1, y la probabilidad de ρ = 1 por azar es 1/6.
Ningún resultado puede ser significativo. Lectura fijada de antemano:
  - ρ = 1 con los dos residuos → "consistente con estructura sub-λ intra-poro, no demostrado";
  - cualquier otra cosa → "no respaldado por este control".
Residuos: (i) faltante de transmitancia a 550 nm, T_pred − T_med (tira A, 545–555 nm);
(ii) faltante de pendiente roja, s_med − s_pred. Modelo nominal del check 5.2.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from dosregimenes import controles as ct  # noqa: E402
from dosregimenes import espectros as sp  # noqa: E402
from dosregimenes import imagej as ij  # noqa: E402
from dosregimenes import modelo as md  # noqa: E402
from dosregimenes import telarana as tl  # noqa: E402

TOL = 0.15


def run():
    dens = tl.por_muestra()
    media = {m: dens[m][0] for m in (1, 2, 3)}
    orden = media[3] > media[2] > media[1]
    rel = {m: media[m] / tl.FACTIBILIDAD[m] - 1 for m in (1, 2, 3)}
    ok = bool(orden and all(abs(r) <= TOL for r in rel.values()))

    poros = ij.cargar_poros()
    D = {m: ij.PD(m, poros=poros) for m in (1, 2, 3)}
    T = sp.cargar_transmitancia("A")
    R = sp.cargar_reflectancia()
    faltT, faltS = {}, {}
    for m in (1, 2, 3):
        Tp = md.cadena(D[m], [550.0], md.PHI[m], md.L_NUCLEO[m])["T"][0]
        ok_w = (T[m].lam >= 545) & (T[m].lam <= 555)
        faltT[m] = float(Tp - T[m].R[ok_w].mean())
    sp_ = ct.s_pred_rojo({**D, 4: D[1]}, md.L_NUCLEO)
    for m in (1, 2, 3):
        faltS[m] = md.s_medida(R[m]) - sp_[m]

    x = [media[m] for m in (1, 2, 3)]
    rT = spearmanr(x, [faltT[m] for m in (1, 2, 3)])[0]
    rS = spearmanr(x, [faltS[m] for m in (1, 2, 3)])[0]
    lectura = ("consistente, no demostrado" if (np.isclose(rT, 1) and np.isclose(rS, 1))
               else "no respaldado por este control")
    ev = (f"índice m1/m2/m3 {media[1]:.2f}/{media[2]:.2f}/{media[3]:.2f} µm⁻¹ vs factibilidad "
          f"({', '.join(f'{rel[m]*100:+.0f}%' for m in (1, 2, 3))}; orden {orden}) → {ok} | "
          f"faltante T(550) {faltT[1]:.3f}/{faltT[2]:.3f}/{faltT[3]:.3f} ρ {rT:+.1f} | "
          f"faltante s rojo {faltS[1]:.2f}/{faltS[2]:.2f}/{faltS[3]:.2f} ρ {rS:+.1f} | "
          f"n = 3, p(ρ=1 al azar) = 1/6 → {lectura}")
    return "check 6.4 — estructura interna (telarañas)", ok, ev


if __name__ == "__main__":
    print(run())
