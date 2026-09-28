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
ESTILO = RAIZ / "informe" / "estilo.css"
# Dos documentos con el mismo estilo: el informe (con límite de páginas) y el apéndice
# de verificación, que se separó el 27/09/2026 para que el informe entre en 5 páginas.
DOCUMENTOS = [("informe_fuente.html", "informe.html", "informe.pdf"),
              ("apendice_fuente.html", "apendice.html", "apendice.pdf")]
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


def armar(fuente: Path, html: Path) -> list[str]:
    """Inlinea el estilo compartido y las figuras, y escribe el HTML autocontenido."""
    texto = fuente.read_text(encoding="utf-8")
    if "<!--ESTILO-->" not in texto:
        raise SystemExit(f"07_informe: {fuente.name} no tiene el marcador <!--ESTILO-->")
    texto = texto.replace("<!--ESTILO-->",
                          "<style>\n" + ESTILO.read_text(encoding="utf-8") + "</style>")
    cuerpo, usadas = incrustar(texto)
    html.write_text('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
                    '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
                    '</head>\n<body>\n' + cuerpo + '\n</body>\n</html>\n', encoding="utf-8")
    return usadas


def imprimir(nav: Path, html: Path, pdf: Path) -> None:
    # El PDF viejo se borra ANTES de imprimir. Si no, un fallo silencioso del navegador
    # (pasa cuando el archivo está abierto en un visor) deja el anterior en su lugar y
    # parece que salió bien: fue el error del 24/09/2026, que dejó el PDF desactualizado
    # en el repositorio mientras el HTML sí tenía las figuras nuevas.
    try:
        pdf.unlink(missing_ok=True)
    except PermissionError:
        raise SystemExit(f"07_informe: {pdf.name} está abierto en un visor y no se puede "
                         "reemplazar. Cerralo y volvé a correr el script.") from None
    with tempfile.TemporaryDirectory() as perfil:
        subprocess.run([str(nav), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        f"--user-data-dir={perfil}", f"--print-to-pdf={pdf}",
                        "--virtual-time-budget=15000", html.as_uri()],
                       check=False, capture_output=True, timeout=180)
    if not pdf.exists():
        raise SystemExit(f"07_informe: el navegador no escribió {pdf.name}")
    if pdf.stat().st_mtime < html.stat().st_mtime:
        raise SystemExit(f"07_informe: {pdf.name} es más viejo que el HTML: no se regeneró")


def main() -> None:
    nav = next((p for p in NAVEGADORES if p.exists()), None)
    if nav is None:
        raise SystemExit("07_informe: no hay Edge ni Chrome para imprimir el PDF")
    for f, h, p in DOCUMENTOS:
        fuente, html, pdf = RAIZ / "informe" / f, RAIZ / "informe" / h, RAIZ / "informe" / p
        usadas = armar(fuente, html)
        imprimir(nav, html, pdf)
        print(f"07_informe: {p} — {len(usadas)} figuras, "
              f"HTML {html.stat().st_size / 1e6:.1f} MB, PDF {pdf.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    sys.exit(main())
