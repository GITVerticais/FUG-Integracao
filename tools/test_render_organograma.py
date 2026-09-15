"""Cobre a matriz de I/O de tools/render_organograma.py.

Cada teste monta origem e saida em tmp_path: nada aqui toca os
arquivos reais de downloads/ ou assets/img/.

Rodar com: python -m pytest tools/test_render_organograma.py -q
"""
import pathlib
import sys

import pymupdf
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import render_organograma  # noqa: E402

ARQUIVOS = (
    "organograma-fug-2025.svg",
    "organograma-fug-2025.png",
    "organograma-fug-2025-preview.png",
)


def pdf_com_pagina(caminho):
    caminho = pathlib.Path(caminho)
    doc = pymupdf.open()
    page = doc.new_page(width=200, height=100)
    page.insert_text((20, 50), "FUG")
    doc.save(caminho)
    doc.close()
    return caminho


def pdf_sem_paginas(caminho):
    """PDF valido com /Count 0: pymupdf abre, mas recusa salvar um doc vazio."""
    caminho = pathlib.Path(caminho)
    caminho.write_bytes(
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [] /Count 0 >>\nendobj\n"
        b"xref\n0 3\n0000000000 65535 f \n0000000009 00000 n \n"
        b"0000000058 00000 n \ntrailer\n<< /Size 3 /Root 1 0 R >>\n"
        b"startxref\n110\n%%EOF\n"
    )
    return caminho


def sentinelas(saida):
    saida.mkdir(parents=True, exist_ok=True)
    antes = {}
    for nome in ARQUIVOS:
        arquivo = saida / nome
        arquivo.write_bytes(b"sentinela-" + nome.encode("utf-8"))
        antes[nome] = arquivo.read_bytes()
    return antes


def assert_tres_arquivos(saida):
    for nome in ARQUIVOS:
        arquivo = saida / nome
        assert arquivo.is_file(), nome
        assert arquivo.stat().st_size > 0, nome
    svg = (saida / "organograma-fug-2025.svg").read_text(encoding="utf-8")
    assert "<svg" in svg
    assert (saida / "organograma-fug-2025.png").read_bytes().startswith(b"\x89PNG")
    assert (saida / "organograma-fug-2025-preview.png").read_bytes().startswith(b"\x89PNG")


def test_conversao_normal_escreve_os_tres_arquivos(tmp_path):
    pdf = pdf_com_pagina(tmp_path / "organograma-fug-2025.pdf")
    saida = tmp_path / "img"
    saida.mkdir()

    render_organograma.converter(pdf, saida)

    assert_tres_arquivos(saida)


def test_reexecucao_nao_altera_bytes(tmp_path):
    pdf = pdf_com_pagina(tmp_path / "organograma-fug-2025.pdf")
    saida = tmp_path / "img"
    saida.mkdir()

    render_organograma.converter(pdf, saida)
    primeira = {nome: (saida / nome).read_bytes() for nome in ARQUIVOS}

    render_organograma.converter(pdf, saida)

    for nome in ARQUIVOS:
        assert (saida / nome).read_bytes() == primeira[nome]


def test_pdf_ausente_aborta_sem_escrever(tmp_path):
    pdf = tmp_path / "organograma-fug-2025.pdf"
    saida = tmp_path / "img"
    antes = sentinelas(saida)

    with pytest.raises(render_organograma.ErroDeConversao) as erro:
        render_organograma.converter(pdf, saida)

    assert str(pdf) in str(erro.value)
    for nome in ARQUIVOS:
        assert (saida / nome).read_bytes() == antes[nome]


def test_pdf_sem_paginas_aborta_sem_escrever(tmp_path):
    pdf = pdf_sem_paginas(tmp_path / "organograma-fug-2025.pdf")
    saida = tmp_path / "img"
    antes = sentinelas(saida)

    with pytest.raises(render_organograma.ErroDeConversao) as erro:
        render_organograma.converter(pdf, saida)

    assert str(pdf) in str(erro.value)
    for nome in ARQUIVOS:
        assert (saida / nome).read_bytes() == antes[nome]


def test_pasta_de_saida_ausente_cria_e_escreve(tmp_path):
    pdf = pdf_com_pagina(tmp_path / "organograma-fug-2025.pdf")
    saida = tmp_path / "img"
    assert not saida.exists()

    render_organograma.converter(pdf, saida)

    assert saida.is_dir()
    assert_tres_arquivos(saida)


def test_main_devolve_1_quando_pdf_ausente(tmp_path, monkeypatch, capsys):
    pdf = tmp_path / "organograma-fug-2025.pdf"
    saida = tmp_path / "img"
    antes = sentinelas(saida)
    monkeypatch.setattr(render_organograma, "SRC", pdf)
    monkeypatch.setattr(render_organograma, "OUT", saida)

    codigo = render_organograma.main()

    assert codigo == 1
    assert str(pdf) in capsys.readouterr().err
    for nome in ARQUIVOS:
        assert (saida / nome).read_bytes() == antes[nome]


def test_main_devolve_1_quando_pdf_sem_paginas(tmp_path, monkeypatch, capsys):
    pdf = pdf_sem_paginas(tmp_path / "organograma-fug-2025.pdf")
    saida = tmp_path / "img"
    antes = sentinelas(saida)
    monkeypatch.setattr(render_organograma, "SRC", pdf)
    monkeypatch.setattr(render_organograma, "OUT", saida)

    codigo = render_organograma.main()

    assert codigo == 1
    assert str(pdf) in capsys.readouterr().err
    for nome in ARQUIVOS:
        assert (saida / nome).read_bytes() == antes[nome]


def test_main_devolve_0_no_caminho_feliz(tmp_path, monkeypatch):
    pdf = pdf_com_pagina(tmp_path / "organograma-fug-2025.pdf")
    saida = tmp_path / "img"
    monkeypatch.setattr(render_organograma, "SRC", pdf)
    monkeypatch.setattr(render_organograma, "OUT", saida)

    assert render_organograma.main() == 0
    assert_tres_arquivos(saida)
