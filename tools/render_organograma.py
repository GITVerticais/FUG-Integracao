"""Rasteriza o organograma oficial de downloads/ para assets/img/.

Fonte de verdade: downloads/organograma-fug-2025.pdf. Os caminhos sao
resolvidos a partir da raiz do repositorio, entao o script roda de
qualquer diretorio de trabalho. SVG, PNG e preview sao derivados; o
PDF oficial nao e modificado.
"""
import pathlib
import sys

import pymupdf

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SRC = RAIZ / "downloads" / "organograma-fug-2025.pdf"
OUT = RAIZ / "assets" / "img"


class ErroDeConversao(Exception):
    """Falha que impede a conversao; nada e escrito em disco."""


def converter(src, out):
    src = pathlib.Path(src)
    out = pathlib.Path(out)
    if not src.exists():
        raise ErroDeConversao(f"PDF ausente: {src}")

    doc = pymupdf.open(src)
    try:
        if doc.page_count == 0:
            raise ErroDeConversao(f"PDF sem paginas: {src}")
        out.mkdir(parents=True, exist_ok=True)
        page = doc[0]
        print("pagina:", page.rect)
        (out / "organograma-fug-2025.svg").write_text(
            page.get_svg_image(text_as_path=False), encoding="utf-8"
        )
        for scale, name in (
            (1.0, "organograma-fug-2025.png"),
            (0.5, "organograma-fug-2025-preview.png"),
        ):
            pix = page.get_pixmap(matrix=pymupdf.Matrix(scale, scale))
            pix.save(out / name)
            print(name, pix.width, "x", pix.height)
    finally:
        doc.close()


def main():
    try:
        converter(SRC, OUT)
    except ErroDeConversao as erro:
        print(f"erro: {erro}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
