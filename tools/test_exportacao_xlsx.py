"""Trava o download dos XLSX oficiais e as tabelas renderizadas de data/*.json.

Rodar com: python -m pytest tools/test_exportacao_xlsx.py -q
"""
import json
import pathlib
import re
import subprocess

import openpyxl

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PAGINA = RAIZ / "app" / "estrutura-organizacional" / "page.tsx"

LINKS = (
    (
        "diretorias",
        "/downloads/diretorias-2025.xlsx",
        "Baixar o XLSX oficial de Dirigentes e Órgãos Colegiados",
    ),
    (
        "corpo-funcional",
        "/downloads/corpo-funcional-2025.xlsx",
        "Baixar o XLSX oficial do Corpo Funcional",
    ),
)


def _html():
    return PAGINA.read_text(encoding="utf-8")


def _secoes():
    proc = subprocess.run(
        ["node", str(RAIZ / "tools" / "render_tabelas.js"), str(RAIZ / "data")],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return json.loads(proc.stdout)


def _celulas_er(markup, nome):
    achado = re.search(
        rf'<th class="[^"]*" scope="row">{re.escape(nome)}</th>([\s\S]*?)</tr>',
        markup,
    )
    assert achado, nome
    return re.findall(r'<td class="[^"]*">([^<]*)</td>', achado.group(1))


def _fatia(html, inicio, fim):
    i = html.index(inicio)
    j = html.index(fim, i)
    return html[i:j]


def test_pagina_chama_cada_bloco_com_o_json_certo():
    html = _html()
    assert "blocoDiretorias(diretorias)" in html
    assert "blocoCorpoFuncional(corpo)" in html
    assert "blocoEstruturaRemuneratoria(remuneracao)" in html


def test_secoes_com_xlsx_oferecem_o_arquivo_oficial():
    html = _html()
    for secao, href, rotulo in LINKS:
        markup = _fatia(html, f'id="{secao}"', "bloco")
        assert re.search(rf'href="{re.escape(href)}"[^>]*\bdownload\b', markup), href
        assert f'aria-label="{rotulo}"' in markup
        nome = href.rsplit("/", 1)[-1]
        assert (RAIZ / "downloads" / nome).is_file(), nome


def test_corpo_funcional_aponta_estrutura_remuneratoria_antes_do_bloco():
    markup = _fatia(_html(), 'id="corpo-funcional"', "blocoCorpoFuncional")
    assert re.search(r'<a\b[^>]*\bhref="#estrutura-remuneratoria"', markup)
    assert re.search(
        r'<a\b[^>]*\bhref="/downloads/corpo-funcional-2025.xlsx"[^>]*\bdownload\b',
        markup,
    )


def test_corpo_funcional_publica_29_linhas_e_legenda():
    markup = _secoes()["corpo-funcional"]
    assert "29 registros." in markup
    tbody = re.search(r"<tbody>([\s\S]*?)</tbody>", markup)
    assert tbody
    assert len(re.findall(r"<tr\b", tbody.group(1))) == 29


def test_nao_carrega_sheetjs_nem_exportar_xlsx():
    html = _html()
    assert "xlsx.full.min.js" not in html
    assert "exportar-xlsx.js" not in html
    assert "BLOCO:" not in html


def test_estrutura_remuneratoria_oferece_xlsx_oficial_sem_notas_de_transcricao():
    html = _html()
    markup = _fatia(html, 'id="estrutura-remuneratoria"', "blocoEstruturaRemuneratoria")
    frase = (
        "Transcrição do PDF oficial de 2025. "
        "Vagas previstas são as posições do cargo no quadro; "
        "vagas preenchidas são as posições ocupadas segundo o mesmo PDF."
    )
    assert frase not in re.sub(r"\s+", " ", markup)
    href = "/downloads/estrutura-remuneratoria-2026.xlsx"
    rotulo = "Baixar o XLSX oficial da Estrutura Remuneratória"
    assert re.search(rf'href="{re.escape(href)}"[^>]*\bdownload\b', markup), href
    assert f'aria-label="{rotulo}"' in markup
    assert re.search(r"</span>Baixar o XLSX oficial\s*</a>", markup)
    caminho = RAIZ / "downloads" / "estrutura-remuneratoria-2026.xlsx"
    assert caminho.is_file()
    assert "pdf" not in markup.lower()
    assert "29" not in markup
    assert "35" not in markup
    assert "Q.T." not in markup
    assert "Q.P." not in markup
    assert re.search(r"atualiza[cç][aã]o", markup, re.I) is None
    assert "base normativa" not in markup.lower()
    assert "acordo coletivo" not in markup.lower()
    assert "pdf" not in _secoes()["estrutura-remuneratoria"].lower()

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


def test_estrutura_remuneratoria_bloco_publicado_tem_20_cargos_2026():
    markup = _secoes()["estrutura-remuneratoria"]
    tbody = re.search(r"<tbody>([\s\S]*?)</tbody>", markup)
    assert tbody
    assert len(re.findall(r"<tr\b", tbody.group(1))) == 20

    for nome in (
        "Secretário Executivo",
        "Secretário Executivo Adjunto",
        "Procurador Jurídico",
    ):
        assert _celulas_er(markup, nome)[2] == "1"
    for nome in (
        "Gerente",
        "Assistente Administrativo I",
        "Assistente Administrativo II",
        "Trainee",
    ):
        assert _celulas_er(markup, nome)[2] == "0"
    assert _celulas_er(markup, "Secretário Executivo")[5] == "R$ 50.000,00"


def test_pagina_real_exibe_vacancia_nas_linhas_vagas():
    html = _secoes()["diretorias"]
    linhas = re.findall(r'<tr\b[^>]*data-vago="true"[^>]*>[\s\S]*?</tr>', html)
    assert linhas
    for linha in linhas:
        assert "VACÂNCIA" in linha
    assert "Não preenchido" not in html
