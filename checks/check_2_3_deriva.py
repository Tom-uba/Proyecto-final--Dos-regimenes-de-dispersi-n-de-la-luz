"""check 2.3 — la lámpara no derivó durante la sesión de reflectancia del 02/06.

Motivo: la lámpara de tungsteno era vieja y pudo no estar estabilizada. Como R = S/P con el
blanco P tomado al calibrar, una deriva posterior sesgaría R según CUÁNDO se midió cada
espectro. Cada .txt trae su hora en el encabezado, así que es testeable sin datos nuevos.

Método: residuo de la pendiente s de cada espectro respecto de la media de SU muestra (así
se quita la diferencia real entre muestras) contra los minutos desde el primer espectro.
Se usan las muestras 1–3: la 4 dispersa mucho entre regiones y su última medición (Aba)
arrastra la tendencia sola.

Criterio a priori, en las dos sub-bandas:
    (a) pendiente compatible con cero a 3σ
    (b) cambio acumulado en toda la sesión < 0.05 en s
        (el déficit del modelo en m1–3 es 0.13–0.17; una deriva menor que 0.05 no lo explica)

Qué NO testea: un sesgo fijado en el momento de calibrar (p. ej. el patrón WS-1 amarillento)
afecta a toda la sesión por igual y no deja tendencia temporal. Ver PROCEDENCIA §3.
"""
from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from dosregimenes import DATA, MASCARA_NM  # noqa: E402
from dosregimenes import lamina as lm  # noqa: E402
from dosregimenes.espectros import _leer_txt  # noqa: E402

SUBS = {"azul": (470.0, 590.0), "rojo": (600.0, 745.0)}
TOL_SIGMA = 3.0
TOL_CAMBIO = 0.05


def _hora(txt: str) -> datetime:
    f = re.search(r"Date:\s+\w+\s+(\w+\s+\d+\s+[\d:]+)\s+\w+\s+(\d{4})", txt)
    return datetime.strptime(f"{f.group(1)} {f.group(2)}", "%b %d %H:%M:%S %Y")


def run():
    filas = []
    for f in sorted((DATA / "reflectancia").glob("tira_A_muestra_*_Reflection*.txt")):
        m = int(re.search(r"muestra_(\d)", f.name).group(1))
        if m == 4:
            continue
        txt = f.read_text(encoding="latin-1")
        wl, v = _leer_txt(f)
        ok = ~((wl >= MASCARA_NM[0]) & (wl <= MASCARA_NM[1]))
        fila = dict(m=m, t=_hora(txt))
        for nombre, (lo, hi) in SUBS.items():
            s = ok & (wl >= lo) & (wl <= hi)
            fila[nombre] = lm.pendiente(wl[s], v[s] / 100.0)
        filas.append(fila)

    t0 = min(r["t"] for r in filas)
    t = np.array([(r["t"] - t0).total_seconds() / 60.0 for r in filas])
    dur = float(t.max() - t.min())

    ok, partes = True, []
    for nombre in SUBS:
        medias = {m: np.mean([r[nombre] for r in filas if r["m"] == m]) for m in (1, 2, 3)}
        res = np.array([r[nombre] - medias[r["m"]] for r in filas])
        p, cov = np.polyfit(t, res, 1, cov=True)
        err = float(np.sqrt(cov[0, 0]))
        nsig = abs(p[0]) / err if err > 0 else np.inf
        cambio = abs(p[0]) * dur
        if nsig > TOL_SIGMA or cambio > TOL_CAMBIO:
            ok = False
        partes.append(f"{nombre}: {p[0]:+.5f}±{err:.5f}/min ({nsig:.1f}σ), "
                      f"cambio en {dur:.0f} min = {cambio:.3f}")

    return "check 2.3 — sin deriva de lámpara en la sesión", ok, "m1–3, " + "; ".join(partes)


if __name__ == "__main__":
    print(run())
