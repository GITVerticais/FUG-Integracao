"""Trava o download dos XLSX oficiais em estrutura-organizacional/index.html.

Rodar com: python -m pytest tools/test_exportacao_xlsx.py -q
"""
import pathlib
import re

import openpyxl

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


def test_corpo_funcional_aponta_estrutura_remuneratoria_antes_do_bloco():
    html = _html()
    bloco = re.search(
        r'<section\b[^>]*\bid="corpo-funcional"[\s\S]*?<!-- BLOCO:corpo-funcional:INICIO -->',
        html,
    )
    assert bloco, "corpo-funcional"
    markup = bloco.group(0)
    assert re.search(r'<a\b[^>]*\bhref="#estrutura-remuneratoria"', markup)
    assert re.search(
        r'<a\b[^>]*\bhref="../downloads/corpo-funcional-2025.xlsx"[^>]*\bdownload\b',
        markup,
    )


def test_corpo_funcional_publica_29_linhas_e_legenda():
    html = _html()
    bloco = re.search(
        r"<!-- BLOCO:corpo-funcional:INICIO -->([\s\S]*?)<!-- BLOCO:corpo-funcional:FIM -->",
        html,
    )
    assert bloco, "corpo-funcional"
    markup = bloco.group(1)
    assert "29 registros." in markup
    tbody = re.search(r"<tbody>([\s\S]*?)</tbody>", markup)
    assert tbody
    assert len(re.findall(r"<tr\b", tbody.group(1))) == 29


def test_nao_carrega_sheetjs_nem_exportar_xlsx():
    html = _html()
    assert "xlsx.full.min.js" not in html
    assert "exportar-xlsx.js" not in html


def test_estrutura_remuneratoria_oferece_xlsx_oficial_sem_notas_de_transcricao():
    html = _html()
    secao = re.search(
        r'<section\b[^>]*\bid="estrutura-remuneratoria"[\s\S]*?</section>',
        html,
    )
    assert secao, "estrutura-remuneratoria"
    frase = (
        "Transcrição do PDF oficial de 2025. "
        "Vagas previstas são as posições do cargo no quadro; "
        "vagas preenchidas são as posições ocupadas segundo o mesmo PDF."
    )
    assert frase not in re.sub(r"\s+", " ", secao.group(0))
    bloco = re.search(
        r'<section\b[^>]*\bid="estrutura-remuneratoria"[\s\S]*?<!-- BLOCO:estrutura-remuneratoria:INICIO -->',
        html,
    )
    assert bloco, "estrutura-remuneratoria"
    markup = bloco.group(0)
    href = "../downloads/estrutura-remuneratoria-2026.xlsx"
    rotulo = "Baixar o XLSX oficial da Estrutura Remuneratória"
    assert re.search(
        rf'<a\b[^>]*\bhref="{re.escape(href)}"[^>]*\bdownload\b',
        markup,
    ), href
    assert f'aria-label="{rotulo}"' in markup
    assert re.search(r"</span>Baixar o XLSX oficial\s*</a>", markup)
    caminho = RAIZ / "downloads" / "estrutura-remuneratoria-2026.xlsx"
    assert caminho.is_file()
    assert "pdf" not in secao.group(0).lower()
    assert "29" not in markup
    assert "35" not in markup
    assert "Q.T." not in markup
    assert "Q.P." not in markup
    assert re.search(r"atualiza[cç][aã]o", markup, re.I) is None
    assert "base normativa" not in markup.lower()
    assert "acordo coletivo" not in markup.lower()

    ws = openpyxl.load_workbook(caminho, data_only=True).active
    qp_por_cargo = {}
    for linha in ws.iter_rows(min_row=2, max_col=3, values_only=True):
        cargo = (linha[2] or "").strip() if isinstance(linha[2], str) else linha[2]
        if cargo:
            qp_por_cargo[cargo] = int(linha[1] or 0)
    for nome in (
        "Secretário Executivo",
        "Secretário Executivo Adjunto",
        "Procurador Jurídico",
    ):
        assert qp_por_cargo[nome] == 1
