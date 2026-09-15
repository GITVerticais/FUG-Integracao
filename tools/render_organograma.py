import pymupdf, pathlib

SRC = r"C:\Users\murilo verticais\Desktop\Anexo_II_Organograma_Geral_Oficial_FUG_2025 (1).pdf"
OUT = pathlib.Path("assets/img")

doc = pymupdf.open(SRC)
page = doc[0]
print("pagina:", page.rect)

svg = page.get_svg_image(text_as_path=False)
(OUT / "organograma-fug-2025.svg").write_text(svg, encoding="utf-8")

for scale, name in ((1.0, "organograma-fug-2025.png"), (0.5, "organograma-fug-2025-preview.png")):
    pix = page.get_pixmap(matrix=pymupdf.Matrix(scale, scale))
    pix.save(OUT / name)
    print(name, pix.width, "x", pix.height)
