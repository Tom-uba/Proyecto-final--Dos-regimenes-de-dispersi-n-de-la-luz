"""Ensambla el informe: HTML autocontenido y PDF.  [Etapa 7]

RESULTADO:   informe/informe.html (figuras incrustadas en base64) + informe/informe.pdf
ENTRADA:     informe/informe_fuente.html; figures/*.png (correr antes los scripts 02–06)
CÁLCULO:     reemplaza cada src="fig:<nombre>" por la PNG de figures/<nombre>.png. Falla si
             falta alguna figura, en vez de publicar un informe con huecos.
             El PDF lo imprime Edge o Chrome en modo headless (hojas A4, CSS de impresión).
DERIVADO vs LIBRERÍA:  nada numérico. Los números del texto salen de run.log y de
             notas/log.md; cada uno lleva el check que lo sostiene.
"""
from __future__ import annotations

import base64
import re
import subprocess
import tempfile
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
FUENTE = RAIZ / "informe" / "informe_fuente.html"
HTML = RAIZ / "informe" / "informe.html"
PDF = RAIZ / "informe" / "informe.pdf"
NAVEGADORES = [
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
]


def incrustar(texto: str) -> tuple[str, list[str]]:
    usadas = []

    def sub(m):
        nombre = m.group(1)
        png = RAIZ / "figures" / f"{nombre}.png"
        if not png.exists():
            raise FileNotFoundError(f"falta figures/{nombre}.png: correr el script que la genera")
        usadas.append(nombre)
        return 'src="data:image/png;base64,' + base64.b64encode(png.read_bytes()).decode() + '"'

    return re.sub(r'src="fig:([\w\-]+)"', sub, texto), usadas


def main() -> None:
    cuerpo, usadas = incrustar(FUENTE.read_text(encoding="utf-8"))
    doc = ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
           '</head>\n<body>\n' + cuerpo + '\n</body>\n</html>\n')
    HTML.write_text(doc, encoding="utf-8")

    nav = next((p for p in NAVEGADORES if p.exists()), None)
    if nav is None:
        raise SystemExit("07_informe: no hay Edge ni Chrome para imprimir el PDF")

    # El PDF viejo se borra ANTES de imprimir. Si no, un fallo silencioso del navegador
    # (pasa cuando ya hay otra instancia abierta) deja el archivo anterior en su lugar y
    # parece que salió bien: fue exactamente el error del 24/09/2026, que dejó el PDF
    # desactualizado en el repositorio mientras el HTML sí tenía las figuras nuevas.
    try:
        PDF.unlink(missing_ok=True)
    except PermissionError:
        raise SystemExit("07_informe: informe.pdf está abierto en un visor y no se puede "
                         "reemplazar. Cerralo y volvé a correr el script.") from None
    with tempfile.TemporaryDirectory() as perfil:
        subprocess.run([str(nav), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        f"--user-data-dir={perfil}", f"--print-to-pdf={PDF}",
                        "--virtual-time-budget=15000", HTML.as_uri()],
                       check=False, capture_output=True, timeout=180)
    if not PDF.exists():
        raise SystemExit("07_informe: el navegador no escribió el PDF (¿otra instancia abierta?)")
    if PDF.stat().st_mtime < HTML.stat().st_mtime:
        raise SystemExit("07_informe: el PDF es más viejo que el HTML: no se regeneró")
    print(f"07_informe: {len(usadas)} figuras, HTML {HTML.stat().st_size / 1e6:.1f} MB, "
          f"PDF {PDF.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    sys.exit(main())
