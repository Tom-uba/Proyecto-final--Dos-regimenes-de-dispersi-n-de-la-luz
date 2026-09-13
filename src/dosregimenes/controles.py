"""Controles de la Etapa 6: espesor, absorción y atribución del contraste.  [Etapa 6]

Todos los números salen de `modelo.cadena`. Los criterios viven en los checks 6.1 y 6.3;
acá sólo se calcula.

Observable, igual que en el check 5.2: Δs = s₄ − s̄₁₂₃ en la banda roja (600–745 nm), con
s calculada sobre R_difusa del modelo.
"""
from __future__ import annotations

import numpy as np

from . import espectros as sp
from . import imagej as ij
from . import lamina as lm
from . import modelo as md


def _ds(s: dict) -> float:
    return float(s[4] - np.mean([s[1], s[2], s[3]]))


def _D(poros=None) -> dict:
    poros = ij.cargar_poros() if poros is None else poros
    return {m: ij.PD(m, poros=poros) for m in (1, 2, 3, 4)}


def s_pred_rojo(D: dict, L: dict, polidisperso: bool = False) -> dict:
    return {m: lm.pendiente(md.ROJO, md.cadena(D[m], md.ROJO, md.PHI[m], L[m],
                                               polidisperso)["R_difusa"])
            for m in (1, 2, 3, 4)}


def ds_medido() -> float:
    R = sp.cargar_reflectancia()
    return _ds({m: md.s_medida(R[m]) for m in (1, 2, 3, 4)})


# ---------------------------------------------------------------------------------------
# (a) espesor
# ---------------------------------------------------------------------------------------
# (factor para m1–3, factor para m4); None = intercambio de espesores entre grupos
VARIANTES_L = {
    "nominal": (1.0, 1.0),
    "todos x1.15": (1.15, 1.15),
    "todos x0.85": (0.85, 0.85),
    "m4 x1.15, m1-3 x0.85": (0.85, 1.15),
    "m4 x0.85, m1-3 x1.15": (1.15, 0.85),
    "intercambio": None,
}


def control_espesor(poros=None) -> dict:
    D = _D(poros)
    L123 = float(np.mean([md.L_NUCLEO[m] for m in (1, 2, 3)]))
    out = {}
    for nombre, f in VARIANTES_L.items():
        if f is None:
            L = {1: md.L_NUCLEO[4], 2: md.L_NUCLEO[4], 3: md.L_NUCLEO[4], 4: L123}
        else:
            L = {m: md.L_NUCLEO[m] * (f[1] if m == 4 else f[0]) for m in (1, 2, 3, 4)}
        s = s_pred_rojo(D, L)
        out[nombre] = dict(L=L, s=s, ds=_ds(s))
    return out


# ---------------------------------------------------------------------------------------
# (b) absorción
# ---------------------------------------------------------------------------------------
KAPPA = np.concatenate(([0.0], np.logspace(-5, -1, 160)))   # μ_a,sol en 745 nm [µm⁻¹]
VENTANAS = ((595.0, 605.0), (735.0, 745.0))


def perfil_absorcion(lam_nm) -> np.ndarray:
    """Forma de μ_a,sol(λ): 0 en 600 nm, 1 en 745 nm, lineal. Es la absorción MÍNIMA que
    hace caer R hacia el rojo: no absorbe donde no hace falta."""
    return np.clip((np.asarray(lam_nm, float) - 600.0) / 145.0, 0.0, None)


def _X(R_total, T):
    """(1 − T)/R: vale exactamente 1 sin absorción."""
    return (1.0 - T) / R_total


def _Q_de_X(X4, X123):
    """Q = K(745)/K(600), K = X₄ / ⟨X_m⟩₁₂₃. Índices 0 → 600 nm, 1 → 745 nm."""
    K = X4 / np.mean(X123, axis=0)
    return float(K[1] / K[0])


def Q_medido(tira: str = "A", n_draws: int = 4000, seed: int = 0) -> tuple[float, float]:
    """(Q, σ estadístico por el desvío entre regiones de R, error estándar con n = 5)."""
    R = sp.cargar_reflectancia()
    T = sp.cargar_transmitancia(tira)

    def ventana(e, lo, hi):
        ok = (e.lam >= lo) & (e.lam <= hi)
        return float(e.R[ok].mean()), float(e.sigma[ok].mean())

    r = np.array([[ventana(R[m], *v)[0] for v in VENTANAS] for m in (1, 2, 3, 4)])
    sr = np.array([[ventana(R[m], *v)[1] for v in VENTANAS] for m in (1, 2, 3, 4)])
    sr = sr / np.sqrt(len(R[1].regiones))
    t = np.array([[ventana(T[m], *v)[0] for v in VENTANAS] for m in (1, 2, 3, 4)])

    X = _X(r, t)
    Q = _Q_de_X(X[3], X[:3])
    rng = np.random.default_rng(seed)
    draws = []
    for _ in range(n_draws):
        Xd = _X(r + rng.normal(0.0, 1.0, r.shape) * sr, t)
        draws.append(_Q_de_X(Xd[3], Xd[:3]))
    return Q, float(np.std(draws))


def _interp_kappa(kappa_obj, arr):
    """Interpola en κ (arrays con primera dimensión = KAPPA)."""
    return np.array([np.interp(kappa_obj, KAPPA, arr[:, j]) for j in range(arr.shape[1])])


def control_absorcion(poros=None) -> dict:
    """Hipótesis alternativa H_abs para cada cierre de factor de estructura."""
    D = _D(poros)
    R = sp.cargar_reflectancia()
    s4_obj = md.s_medida(R[4])
    w = perfil_absorcion(md.ROJO)
    i600, i745 = 0, len(md.ROJO) - 1

    res = {}
    for poli in (False, True):
        c4 = md.cadena(D[4], md.ROJO, md.PHI[4], md.L_NUCLEO[4], poli, congelar_nm=600.0,
                       mu_a_sol=np.outer(KAPPA, w))
        Rdif = c4["R_total_abs"] - c4["R_especular"][None, :]
        s_k = np.array([lm.pendiente(md.ROJO, Rdif[j]) for j in range(KAPPA.size)])
        alcanza = bool(s_k.max() >= s4_obj)
        if alcanza:
            j = int(np.argmax(s_k >= s4_obj))
            kap = float(np.interp(s4_obj, s_k[j - 1:j + 1], KAPPA[j - 1:j + 1]))
        else:
            kap = float(KAPPA[-1])
        R4 = _interp_kappa(kap, c4["R_total_abs"])
        T4 = _interp_kappa(kap, c4["T_abs"])
        X4 = _X(R4[[i600, i745]], T4[[i600, i745]])

        X123, ds123 = [], []
        for m in (1, 2, 3):
            c = md.cadena(D[m], md.ROJO, md.PHI[m], md.L_NUCLEO[m], poli,
                          mu_a_sol=np.outer([0.0, kap], w))
            X123.append(_X(c["R_total_abs"][1, [i600, i745]], c["T_abs"][1, [i600, i745]]))
            Rd = c["R_total_abs"] - c["R_especular"][None, :]
            ds123.append(lm.pendiente(md.ROJO, Rd[1]) - lm.pendiente(md.ROJO, Rd[0]))

        res["desacople" if poli else "monodisperso"] = dict(
            kappa_um=kap, kappa_cm=kap * 1e4, alcanza=alcanza, s4_obj=s4_obj,
            Q_pred=_Q_de_X(X4, np.array(X123)),
            A4_745=float(1 - R4[i745] - T4[i745]),
            ds123_inducido=float(np.mean(ds123)))
    return res


# ---------------------------------------------------------------------------------------
# atribución: ¿cuánto del contraste predicho es tamaño de poro y cuánto entorno (φ, L)?
# ---------------------------------------------------------------------------------------
def atribucion(poros=None) -> dict:
    """Diseño factorial 2×2: P(D) ∈ {1–3 agrupadas, 4} × entorno (φ, L) ∈ {1–3, 4}.

    f_D = promedio de los dos efectos de cambiar P(D) / contraste total, y f_env ídem para
    el entorno (reparto de Shapley de dos factores: f_D + f_env = 1 exactamente).
    """
    poros = ij.cargar_poros() if poros is None else poros
    P = {"1-3": np.concatenate([ij.PD(m, poros=poros) for m in (1, 2, 3)]),
         "4": ij.PD(4, poros=poros)}
    ENT = {"1-3": (float(np.mean([md.PHI[m] for m in (1, 2, 3)])),
                   float(np.mean([md.L_NUCLEO[m] for m in (1, 2, 3)]))),
           "4": (md.PHI[4], md.L_NUCLEO[4])}
    res = {}
    for poli in (False, True):
        s = {}
        for p in P:
            for e, (phi, L) in ENT.items():
                s[(p, e)] = lm.pendiente(md.ROJO, md.cadena(P[p], md.ROJO, phi, L, poli)["R_difusa"])
        total = s[("4", "4")] - s[("1-3", "1-3")]
        eD = 0.5 * ((s[("4", "1-3")] - s[("1-3", "1-3")]) + (s[("4", "4")] - s[("1-3", "4")]))
        eE = 0.5 * ((s[("1-3", "4")] - s[("1-3", "1-3")]) + (s[("4", "4")] - s[("4", "1-3")]))
        res["desacople" if poli else "monodisperso"] = dict(
            s={f"P{p}|ent{e}": v for (p, e), v in s.items()}, total=total,
            f_D=eD / total, f_env=eE / total)
    return res
