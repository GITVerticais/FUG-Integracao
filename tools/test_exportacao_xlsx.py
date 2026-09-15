"""Trava o download dos XLSX oficiais em estrutura-organizacional/index.html.

Rodar com: python -m pytest tools/test_exportacao_xlsx.py -q
"""
import pathlib
import re

PAGINA = pathlib.Path(__file__).resolve().parent.parent / "estrutura-organizacional" / "index.html"
RAIZ = PAGINA.parent.parent

LINKS = (
    (
        "diretorias",
        "../downloads/diretorias-2025.xlsx",
        "Baixar o XLSX oficial de Dirigentes e Órgãos Colegiados",
    ),
    (
        "corpo-funcional",
        "../downloads/corpo-funcional-2025.xlsx",
        "Baixar o XLSX oficial do Corpo Funcional",
    ),
)


def _html():
    return PAGINA.read_text(encoding="utf-8")


def test_secoes_com_xlsx_oferecem_o_arquivo_oficial():
    html = _html()
    for secao, href, rotulo in LINKS:
        bloco = re.search(
            rf'<section\b[^>]*\bid="{secao}"[\s\S]*?<!-- BLOCO:{secao}:INICIO -->',
            html,
        )
        assert bloco, secao
        markup = bloco.group(0)
        assert re.search(
            rf'<a\b[^>]*\bhref="{re.escape(href)}"[^>]*\bdownload\b',
            markup,
        ), href
        assert f'aria-label="{rotulo}"' in markup
        nome = href.rsplit("/", 1)[-1]
        assert (RAIZ / "downloads" / nome).is_file(), nome


def test_nao_carrega_sheetjs_nem_exportar_xlsx():
    html = _html()
    assert "xlsx.full.min.js" not in html
    assert "exportar-xlsx.js" not in html
