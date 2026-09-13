"""check 5.3 — ancla externa: alimentada con la morfología publicada por Syurik et al.
(2017), la misma cadena de modelo reproduce la reflectancia que ellos midieron.

Por qué sirve como ancla: otro grupo, otro polímero (PMMA), otro instrumento (PerkinElmer
Lambda 1050 con esfera y referencia Spectralon, es decir SIN nuestro patrón amarillento),
y una serie de reflectancia contra espesor. Ninguno de esos números entró al desarrollo del
modelo; si la cadena estuviera mal armada, no tendría por qué acertarle a una película ajena.

ENTRADAS (todas de Sci. Rep. 7:46637; ficha en notas/fichas.md):
  - poros: diámetro 339 ± 109 nm (media ± desvío) y fracción 39 %, a 50 MPa y 80 °C
    (Fig. 4). El paper supone la misma microestructura en toda la serie de espesores.
    Elección nuestra: P(D) lognormal con esa media y ese desvío.
  - PMMA: n = 1.49 a 600 nm, constante.
  - Sustrato: vidrio con absorbente negro en la cara trasera (Methods). El borde inferior
    de la capa porosa da a vidrio (n = 1.52, valor estándar supuesto) y lo que entra al
    vidrio no vuelve.
  - Medición: reflectancia TOTAL (especular + difusa) a incidencia casi normal → R_total.
  - La capa sin poros de 1–2 µm de arriba se ignora; el paper la resta del espesor.

MODELO: el mismo del check 5.2 — Mie promediado sobre P(D) → ℓ* a porosidad φ →
factor de estructura Percus–Yevick con η = φ → Monte Carlo de lámina. Nada ajustado.

OBSERVABLE Y CRITERIO (fijados antes de correrlo):
  R_total a 600 nm para capas de 9, 16 y 53 µm contra 57 %, ~70 % y 90 % publicados.
  El paper no da incertidumbre de R; se adopta ±0.10 absoluto, del orden de lo que mueve el
  propio desvío publicado de la morfología (±109 nm en D). Deben cumplirse los tres.

INFORMATIVO (no gatea):
  - ℓ* del modelo a 400 / 600 / 800 nm contra l_t = 3.5–4 µm publicado. No gatea porque el
    paper extrae l_t como pendiente de T contra 1/L ("ley de Ohm para la luz"), que absorbe
    la longitud de extrapolación de los bordes y no es exactamente ℓ*.
  - R(400) − R(800) a 9 y 53 µm contra 13 y 7 puntos publicados.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from dosregimenes import estructura as es  # noqa: E402
from dosregimenes import lamina as lm  # noqa: E402
from dosregimenes import mie  # noqa: E402
from dosregimenes import montecarlo as mc  # noqa: E402

D_MEDIA_UM, D_DESVIO_UM = 0.339, 0.109
PHI = 0.39
N_PMMA = 1.49
N_VIDRIO = 1.52
ESPESORES_UM = (9.0, 16.0, 53.0)
R_PUBLICADA = (0.57, 0.70, 0.90)
TOL = 0.10
N_FOT = 60000
SEED = 17


def _PD() -> np.ndarray:
    s2 = np.log(1.0 + (D_DESVIO_UM / D_MEDIA_UM) ** 2)
    mu = np.log(D_MEDIA_UM) - s2 / 2.0
    return np.random.default_rng(3).lognormal(mu, np.sqrt(s2), 40000)


def _cadena(lam_nm):
    D = _PD()
    lam = np.atleast_1d(np.asarray(lam_nm, float))
    ell0, pr = mie.ell_star_diluido(D, lam, PHI, n_matriz=N_PMMA)
    n_ef = lm.n_efectivo(np.full(lam.shape, N_PMMA), PHI)
    g = pr["g_ef"]
    fS = es.factor_transporte(D, lam, n_ef, PHI, g)
    return ell0 / fS, g, n_ef, fS


def _R(ell, g, n_ef, L):
    return mc.correr(float(ell), float(g), float(n_ef), L, n_fotones=N_FOT, seed=SEED,
                     n_abajo=N_VIDRIO)["R_total"]


def run():
    ell, g, n_ef, fS = _cadena([600.0])
    R_mod = [_R(ell[0], g[0], n_ef[0], L) for L in ESPESORES_UM]
    desv = [m - p for m, p in zip(R_mod, R_PUBLICADA)]
    ok = all(abs(d) <= TOL for d in desv)

    l3, g3, n3, _ = _cadena([400.0, 600.0, 800.0])
    l48, g48, n48, _ = _cadena([400.0, 800.0])
    dR = {L: _R(l48[0], g48[0], n48[0], L) - _R(l48[1], g48[1], n48[1], L) for L in (9.0, 53.0)}

    ev = ("R(600): " + ", ".join(f"{L:.0f} µm {m:.2f} vs {p:.2f} ({d:+.2f})"
                                 for L, m, p, d in zip(ESPESORES_UM, R_mod, R_PUBLICADA, desv)) +
          f" (tol ±{TOL}) | [info] ℓ* 400/600/800 nm = {l3[0]:.1f}/{l3[1]:.1f}/{l3[2]:.1f} µm "
          f"vs l_t 3.5–4 publicado; factor de estructura {float(fS[0]):.2f} | "
          f"[info] R(400)−R(800): 9 µm {dR[9.0]*100:+.0f} pts (pub 13), 53 µm {dR[53.0]*100:+.0f} pts (pub 7)")
    return "check 5.3 — ancla externa: Syurik 2017 (PMMA)", bool(ok), ev


if __name__ == "__main__":
    print(run())
