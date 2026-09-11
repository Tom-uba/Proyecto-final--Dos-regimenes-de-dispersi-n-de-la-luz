"""Corre toda la batería de checks e imprime UNA línea por check.

Cada checks/check_*.py define:  run() -> (nombre: str, ok: bool | None, evidencia: str)
    ok = True/False  -> PASA / FALLA
    ok = None        -> PENDIENTE (etapa aún no hecha)

Salida: exit code = número de checks en FALLA.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

AQUI = Path(__file__).parent


def _cargar(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    fallas = 0
    for path in sorted(AQUI.glob("check_*.py")):
        try:
            nombre, ok, ev = _cargar(path).run()
        except Exception as e:  # noqa: BLE001
            nombre, ok, ev = path.stem, False, f"excepción: {e!r}"
        etiqueta = {True: "PASA", False: "FALLA", None: "PEND"}[ok]
        print(f"[{etiqueta}] {nombre}  —  {ev}")
        if ok is False:
            fallas += 1
    print(f"\n{fallas} falla(s).")
    return fallas


if __name__ == "__main__":
    sys.exit(main())
