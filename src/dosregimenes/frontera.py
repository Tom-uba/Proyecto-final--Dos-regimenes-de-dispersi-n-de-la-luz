"""La frontera, dada como intervalo.  [Etapa 6]

Definiciones en informe/teoria.md §6. Todo x es de VACÍO (x = πD/λ₀), el del eje de la
Etapa 4; las curvas de Mie se convierten con x = x_Mie / n_sol.

1. F1, F2, F3 — propiedades de la curva de Mie de UN poro de aire en el sólido:
     F1  x = 1 (convención; sin incertidumbre)
     F2  x donde p = d ln Q_sca / d ln x_Mie baja de 2 (mitad entre Rayleigh y el plateau)
     F3  x del máximo de |dQ_sca/dx|
   Intervalo: n_sol evaluado en los dos extremos de la banda (470 y 750 nm) y con el sesgo
   de índice 0 y +2 % (data/refs/n_lambda.md).

2. Lo que permiten los datos. Con dos cúmulos, la transición sólo se puede ubicar ENTRE
   ellos:
     cota inferior = x mediana de m4 en 470 nm        × 1.30
     cota superior = mín de x mediana de m1–3 en 750 nm × 0.70
   (±30 % sistemático de D, data/PROCEDENCIA.md §4bis; se toma el caso que más los acerca).

3. F_s — la frontera en el OBSERVABLE. Una muestra ficticia con la FORMA de P(D) de m4
   (desvío relativo 0.41, el de m1 es 0.40) reescalada para que su x mediana en
   λ_c = √(600·745) nm recorra X_BARRIDO; en los dos entornos (φ, L) de las muestras y con
   los dos cierres de factor de estructura. F_s es la x mediana donde s_pred rojo cruza
   s* = (s₄ + s̄₁₂₃)/2 medidas, bajando desde x grande (primer cruce, interpolado en log x).
   s* sale de los datos pero no se ajusta nada: es el punto medio entre los dos regímenes
   observados.
"""
from __future__ import annotations

import numpy as np

from . import imagej as ij
from . import lamina as lm
from . import mie
from . import modelo as md
from .nref import n_sol

LAM_C = float(np.sqrt(600.0 * 745.0))
X_BARRIDO = np.logspace(np.log10(0.15), np.log10(15.0), 17)
ENTORNOS = {"1-3": (0.2033, 42.33), "4": (0.33, 32.0)}
SISTEMATICO_D = 0.30
N_FOT_BARRIDO = 40000


def fronteras_mie(lams=(470.0, 750.0), biases=(0.0, 0.02)) -> dict:
    xm = np.logspace(np.log10(0.05), np.log10(60.0), 3000)
    F2, F3 = [], []
    for lam in lams:
        for b in biases:
            n = float(n_sol(lam, bias=b))
            q, _ = mie.qsca_g_mie(xm, 1.0 / n)
            p = np.gradient(np.log(q), np.log(xm))
            F2.append(float(xm[np.argmax(p < 2.0)] / n))
            F3.append(float(xm[np.argmax(np.abs(np.gradient(q, xm)))] / n))
    return dict(F1=(1.0, 1.0), F2=(min(F2), max(F2)), F3=(min(F3), max(F3)))


def x_mediana(D_um, lam_nm) -> float:
    return float(np.median(np.pi * np.asarray(D_um) * 1e3 / lam_nm))


def cota_datos(poros=None) -> dict:
    poros = ij.cargar_poros() if poros is None else poros
    D = {m: ij.PD(m, poros=poros) for m in (1, 2, 3, 4)}
    x4 = x_mediana(D[4], 470.0)
    x123 = min(x_mediana(D[m], 750.0) for m in (1, 2, 3))
    return dict(x4_470=x4, x123_750=x123,
                inf=x4 * (1 + SISTEMATICO_D), sup=x123 * (1 - SISTEMATICO_D))


def barrido(poros=None, n_fotones: int = N_FOT_BARRIDO, seed: int = md.SEED) -> list[dict]:
    poros = ij.cargar_poros() if poros is None else poros
    D4 = ij.PD(4, poros=poros)
    forma = D4 / np.median(D4)
    filas = []
    for ent, (phi, L) in ENTORNOS.items():
        for poli in (False, True):
            for xt in X_BARRIDO:
                filas.append(punto(forma, float(xt), ent, poli, n_fotones, seed))
    return filas


def punto(forma, xt: float, ent: str, poli: bool, n_fotones: int = N_FOT_BARRIDO,
          seed: int = md.SEED) -> dict:
    phi, L = ENTORNOS[ent]
    D = forma * xt * LAM_C / (np.pi * 1e3)
    c = md.cadena(D, md.ROJO, phi, L, poli, n_fotones=n_fotones, seed=seed)
    return dict(entorno=ent, cierre="desacople" if poli else "monodisperso", x_mediana=xt,
                s_rojo=lm.pendiente(md.ROJO, c["R_difusa"]), R600=float(c["R_difusa"][0]))


def cruce(x, s, s_star: float) -> float:
    """Primer cruce de s* bajando desde x grande; nan si la curva nunca llega a s*."""
    x, s = np.asarray(x, float), np.asarray(s, float)
    orden = np.argsort(x)[::-1]
    x, s = x[orden], s[orden]
    for i in range(1, len(x)):
        if s[i - 1] < s_star <= s[i]:
            t = (s_star - s[i - 1]) / (s[i] - s[i - 1])
            return float(np.exp(np.log(x[i - 1]) + t * (np.log(x[i]) - np.log(x[i - 1]))))
    return float("nan")
