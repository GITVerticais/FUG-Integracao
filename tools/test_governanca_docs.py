"""Trava os quatro PDFs oficiais na página de governança.

Rodar com: python -m pytest tools/test_governanca_docs.py -q
"""
import pathlib
import re
from html.parser import HTMLParser

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PAGINA = RAIZ / "app" / "governanca" / "page.tsx"
IFRAME_NOME = "visualizador-governanca"

DOCUMENTOS = (
    ("Regimento Interno", "regimento-interno.pdf"),
    ("Relatório Escola Movimento 2025", "relatorio-escola-movimento-2025.pdf"),
    ("Código de Ética", "codigo-de-etica.pdf"),
    ("Estatuto", "estatuto.pdf"),
)


def _html() -> str:
    return PAGINA.read_text(encoding="utf-8")


def _documentos(html: str) -> list[tuple[str, str]]:
    bloco = re.search(r"const DOCUMENTOS = \[([\s\S]*?)\] as const;", html)
    assert bloco, "lista de documentos ausente"
    return re.findall(r'\["([^"]+)", "([^"]+)"\]', bloco.group(1))


def _artigo(html: str) -> str:
    artigos = re.findall(r"<article\b[^>]*>([\s\S]*?)</article>", html)
    assert len(artigos) == 1, "um modelo de artigo, repetido para cada PDF"
    return artigos[0]


def _texto(markup: str) -> str:
    return " ".join(re.sub(r"<[^>]+>", " ", markup).split())


def _ancoras(markup: str) -> list[str]:
    return re.findall(r"<a\b([^>]*)>", markup)


_VOID = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
}


class _IframeAncestrais(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.current = None
        self.iframe = None

    def handle_starttag(self, tag, attrs):
        node = {"tag": tag, "attrs": dict(attrs), "parent": self.current}
        if tag == "iframe" and node["attrs"].get("name") == IFRAME_NOME:
            self.iframe = node
        if tag not in _VOID:
            self.current = node

    def handle_endtag(self, tag):
        if tag in _VOID or self.current is None:
            return
        self.current = self.current["parent"]


def _classes(node: dict) -> list[str]:
    bruto = node["attrs"].get("class") or node["attrs"].get("className") or node["attrs"].get("classname") or ""
    return bruto.split()


def test_titulo_identifica_o_modulo():
    html = _html()
    assert 'title: "Governança - Espaço de Integridade FUG"' in html
    h1 = re.search(r"<h1\b[^>]*>([\s\S]*?)</h1>", html)
    assert h1 and "Governança" in _texto(h1.group(1))


def test_quatro_nomes_exatos_nesta_ordem():
    html = _html()
    assert _documentos(html) == list(DOCUMENTOS)
    assert "{nome}" in html


def test_visualizar_aponta_o_pdf_no_iframe_da_pagina():
    html = _html()
    iframe = re.search(r"<iframe\b([^>]*)>", html)
    assert iframe, "iframe nativo ausente"
    attrs_iframe = iframe.group(1)
    assert f'name="{IFRAME_NOME}"' in attrs_iframe
    assert "title=" in attrs_iframe
    assert re.search(r"(?:^|\s)hidden(?:\s|=|$)", attrs_iframe), "visualizador deve começar oculto"
    assert "pdf.js" not in html.lower()
    assert "pdfjs" not in html.lower()
    assert re.search(r"</ul>\s*<iframe\b", html) is None
    assert len(re.findall(r"<iframe\b", html)) == 1
    artigo = _artigo(html)
    visualizar, baixar = _ancoras(artigo)
    assert 'href={`/downloads/${arquivo}`}' in visualizar
    assert f'target="{IFRAME_NOME}"' in visualizar
    assert 'target="_blank"' not in visualizar
    assert "download" not in visualizar.split()
    assert "Visualizar o PDF oficial do" in visualizar
    assert "download" not in baixar.split() or re.search(r"(?:^|\s)download(?:\s|=|$)", baixar)
    assert 'data-visualizador-host' in artigo
    assert "<iframe" not in artigo
    for nome, arquivo in DOCUMENTOS:
        assert arquivo in html
        assert nome in html


def test_script_move_visualizador_para_a_box_clicada():
    html = _html()
    for trecho in (
        'closest("article")',
        "data-visualizador-host",
        "appendChild",
        "viewer.hidden = false",
        "article.scrollIntoView",
        "ctrlKey",
        "preventDefault",
        'viewer.src = link.getAttribute("href")',
    ):
        assert trecho in html


def test_download_entrega_o_pdf_oficial_do_item():
    html = _html()
    _, baixar = _ancoras(_artigo(html))
    assert 'href={`/downloads/${arquivo}`}' in baixar
    assert re.search(r"(?:^|\s)download(?:\s|=|$)", baixar)
    assert "Baixar o PDF oficial do" in baixar
    for _nome, arquivo in DOCUMENTOS:
        caminho = RAIZ / "downloads" / arquivo
        assert caminho.is_file(), arquivo
        assert caminho.read_bytes()[:4] == b"%PDF", arquivo


def test_artigos_nao_empilham_scroll_margin_no_header():
    for artigo in re.findall(r"<article\b[^>]*>", _html()):
        assert "scroll-margin" not in artigo


def test_nao_publica_estrutura_remuneratoria():
    html = _html()
    assert "ESTRUTURA REMUNERATÓRIA" not in html
    assert "Estrutura Remuneratória" not in html
    assert "estrutura-remuneratoria" not in html


def test_acoes_nomeadas_com_foco_visivel_e_sem_overflow_horizontal():
    html = _html()
    parser = _IframeAncestrais()
    parser.feed(html)
    assert parser.iframe, "iframe nomeado ausente"
    cadeia = []
    node = parser.iframe
    while node is not None:
        cadeia.append(node)
        if node["tag"] == "main":
            break
        node = node["parent"]
    assert cadeia[-1]["tag"] == "main"
    for node in cadeia:
        assert "min-w-0" in _classes(node), node["tag"]
    config = (RAIZ / "tailwind.config.js").read_text(encoding="utf-8")
    assert 'primary: "#862120"' in config
    assert "focus-visible:outline-primary" in html
    assert "className={ACAO}" in _artigo(html)
    for nome, _arquivo in DOCUMENTOS:
        assert nome in html
