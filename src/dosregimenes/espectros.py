"""Carga y promedio de espectros OceanView (R y T).  [Etapa 2]

Procedencia de los datos: data/PROCEDENCIA.md §3 (reflectancia) y §5 (transmitancia).

- Reflectancia: data/reflectancia/tira_A_muestra_{1..4}_{Izq,Cen,Der,Arr,Aba}_Reflection__*.txt
  Ya en % de reflectancia (OceanView aplicó blanco + oscuro internamente).
- Transmitancia: data/transmitancia/  (tira A 23/04 + tira B 21/04), ya en %.

Formato OceanView: encabezado hasta la línea ">>>>>Begin Spectral Data<<<<<",
luego pares  "<lambda[nm]>\t<valor[%]>"  (decimales con punto). 3648 px, 336–1792 nm.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from . import BANDA_NM, DATA, MASCARA_NM

_BEGIN = "Begin Spectral Data"


def _leer_txt(path: Path) -> tuple[np.ndarray, np.ndarray]:
    """Devuelve (lambda_nm, valor_pct) de un .txt de OceanView."""
    txt = Path(path).read_text(encoding="latin-1").splitlines()
    i = next(k for k, l in enumerate(txt) if _BEGIN in l)
    wl, val = [], []
    for l in txt[i + 1:]:
        p = l.replace(",", ".").split()
        if len(p) >= 2:
            try:
                wl.append(float(p[0]))
                val.append(float(p[1]))
            except ValueError:
                pass
    return np.asarray(wl), np.asarray(val)


@dataclass
class Espectro:
    """Espectro medio de una muestra sobre N regiones."""

    muestra: int
    lam: np.ndarray          # nm, ya recortado a la banda
    R: np.ndarray            # fracción 0–1 (media de regiones)
    sigma: np.ndarray        # fracción 0–1 (desvío entre regiones)
    regiones: list[str]
    magnitud: str            # "R" o "T"

    @property
    def mascara_valida(self) -> np.ndarray:
        """True donde el punto NO cae en la máscara instrumental."""
        lo, hi = MASCARA_NM
        return ~((self.lam >= lo) & (self.lam <= hi))


def _cargar_dir(directorio: Path, patron: str, magnitud: str,
                banda: tuple[float, float]) -> dict[int, Espectro]:
    lo, hi = banda
    archivos = sorted(Path(directorio).glob(patron))
    if not archivos:
        raise FileNotFoundError(f"sin archivos {patron!r} en {directorio}")
    por_muestra: dict[int, list[tuple[str, np.ndarray]]] = {}
    lam_ref = None
    for f in archivos:
        m = re.search(r"muestra[_-]?(\d)", f.name)
        if not m:
            continue
        k = int(m.group(1))
        reg = re.search(r"muestra[_-]?\d[_-]?([A-Za-z]+)", f.name)
        reg = reg.group(1) if reg else f.stem
        wl, v = _leer_txt(f)
        if lam_ref is None:
            sel = (wl >= lo) & (wl <= hi)
            lam_ref = wl[sel]
        vi = np.interp(lam_ref, wl, v)
        por_muestra.setdefault(k, []).append((reg, vi))
    out = {}
    for k, lst in sorted(por_muestra.items()):
        arr = np.vstack([v for _, v in lst]) / 100.0
        out[k] = Espectro(
            muestra=k, lam=lam_ref, R=arr.mean(0), sigma=arr.std(0),
            regiones=[r for r, _ in lst], magnitud=magnitud,
        )
    return out


def cargar_reflectancia(banda: tuple[float, float] = BANDA_NM) -> dict[int, Espectro]:
    """Los 20 espectros de tira A (02/06/2026), promediados por muestra."""
    return _cargar_dir(DATA / "reflectancia", "tira_A_muestra_*_Reflection*.txt", "R", banda)


def cargar_transmitancia(tira: str = "A",
                         banda: tuple[float, float] = BANDA_NM) -> dict[int, Espectro]:
    """Transmitancia por muestra. tira 'A' (23/04) o 'B' (21/04)."""
    pat = {"A": "tira_A_muestra_*_Transmission*.txt",
           "B": "celulosa_tiraB_muestra*_Transmission*.txt"}[tira.upper()]
    return _cargar_dir(DATA / "transmitancia", pat, "T", banda)


load = cargar_reflectancia  # alias corto
