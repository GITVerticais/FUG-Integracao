"""Rasteriza o organograma oficial de downloads/ para assets/img/.

Fonte de verdade: downloads/organograma-fug-2025.pdf. Os caminhos sao
resolvidos a partir da raiz do repositorio, entao o script roda de
qualquer diretorio de trabalho.
"""
import pymupdf, pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SRC = RAIZ / "downloads" / "organograma-fug-2025.pdf"
OUT = RAIZ / "assets" / "img"

doc = pymupdf.open(SRC)
page = doc[0]
print("pagina:", page.rect)

svg = page.get_svg_image(text_as_path=False)
(OUT / "organograma-fug-2025.svg").write_text(svg, encoding="utf-8")

for scale, name in ((1.0, "organograma-fug-2025.png"), (0.5, "organograma-fug-2025-preview.png")):
    pix = page.get_pixmap(matrix=pymupdf.Matrix(scale, scale))
    pix.save(OUT / name)
    print(name, pix.width, "x", pix.height)
