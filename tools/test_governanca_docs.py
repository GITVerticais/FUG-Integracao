"""Trava os quatro PDFs oficiais na página de governança.

Rodar com: python -m pytest tools/test_governanca_docs.py -q
"""
import pathlib
import re
from html.parser import HTMLParser

PAGINA = pathlib.Path(__file__).resolve().parent.parent / "governanca" / "index.html"
RAIZ = PAGINA.parent.parent
IFRAME_NOME = "visualizador-governanca"

DOCUMENTOS = (
    ("Regimento Interno", "regimento-interno.pdf"),
    ("Relatório Escola Movimento 2025", "relatorio-escola-movimento-2025.pdf"),
    ("Código de Ética", "codigo-de-etica.pdf"),
    ("Estatuto", "estatuto.pdf"),
)


def _html() -> str:
    return PAGINA.read_text(encoding="utf-8")


def _artigos(html: str) -> list[str]:
    artigos = re.findall(r"<article\b[^>]*>([\s\S]*?)</article>", html)
    assert len(artigos) == 4, "a página deve ter exatamente quatro documentos"
    return artigos


def _texto(markup: str) -> str:
    return " ".join(re.sub(r"<[^>]+>", " ", markup).split())


def _ancoras(markup: str) -> list[tuple[str, str]]:
    return re.findall(r"<a\b([^>]*)>([\s\S]*?)</a>", markup)


_VOID = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
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
        if tag in _VOID:
            return
        if self.current is not None:
            self.current = self.current["parent"]


def _cadeia_ate_main(html: str) -> list[dict]:
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
    assert cadeia[-1]["tag"] == "main", "iframe fora de main"
    return cadeia


def test_titulo_identifica_o_modulo():
    html = _html()
    titulo = re.search(r"<title>([^<]*)</title>", html)
    assert titulo, "título ausente"
    assert "Governança" in titulo.group(1)
    h1 = re.search(r"<h1\b[^>]*>([\s\S]*?)</h1>", html)
    assert h1 and "Governança" in _texto(h1.group(1))


def test_quatro_nomes_exatos_nesta_ordem():
    html = _html()
    h2s = [_texto(bloco) for bloco in re.findall(r"<h2\b[^>]*>([\s\S]*?)</h2>", html)]
    assert h2s == [nome for nome, _ in DOCUMENTOS]


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
    assert re.search(r"</ul>\s*<iframe\b", html) is None, "iframe não pode ficar solto abaixo da lista"
    iframes = re.findall(r"<iframe\b", html)
    assert len(iframes) == 1, "um único visualizador nativo"
    for artigo, (nome, arquivo) in zip(_artigos(html), DOCUMENTOS, strict=True):
        href = f"../downloads/{arquivo}"
        visualizar = None
        for attrs, inner in _ancoras(artigo):
            if "Visualizar" in _texto(inner):
                visualizar = attrs
                break
        assert visualizar, f"Visualizar ausente em {nome}"
        href_match = re.search(r'\bhref="([^"]*)"', visualizar)
        assert href_match and href_match.group(1) == href, nome
        assert f'target="{IFRAME_NOME}"' in visualizar, nome
        assert "target=\"_blank\"" not in visualizar
        assert "download" not in visualizar.split()
        assert 'data-visualizador-host' in artigo, nome
        assert "<iframe" not in artigo, f"iframe não começa dentro da box de {nome}"


def test_script_move_visualizador_para_a_box_clicada():
    html = _html()
    script = re.search(r"<script>([\s\S]*?)</script>", html)
    assert script, "script do visualizador ausente"
    corpo = script.group(1)
    assert 'closest("article")' in corpo
    assert "data-visualizador-host" in corpo
    assert "appendChild" in corpo
    assert "viewer.hidden = false" in corpo
    assert "article.scrollIntoView" in corpo
    assert "ctrlKey" in corpo
    assert "preventDefault" in corpo
    assert "viewer.src" in corpo


def test_download_entrega_o_pdf_oficial_do_item():
    html = _html()
    for artigo, (nome, arquivo) in zip(_artigos(html), DOCUMENTOS, strict=True):
        href = f"../downloads/{arquivo}"
        rotulo_ok = False
        baixar = None
        for attrs, inner in _ancoras(artigo):
            if "Baixar" in _texto(inner):
                baixar = attrs
                break
        assert baixar, f"Baixar ausente em {nome}"
        href_match = re.search(r'\bhref="([^"]*)"', baixar)
        assert href_match and href_match.group(1) == href, nome
        assert re.search(r"(?:^|\s)download(?:\s|=|$)", baixar), nome
        aria = re.search(r'aria-label="([^"]*)"', baixar)
        assert aria and nome in aria.group(1), nome
        rotulo_ok = True
        assert rotulo_ok
        caminho = RAIZ / "downloads" / arquivo
        assert caminho.is_file(), arquivo
        assert caminho.read_bytes()[:4] == b"%PDF", arquivo


def test_artigos_nao_empilham_scroll_margin_no_header():
    html = _html()
    for artigo in re.findall(r"<article\b[^>]*>", html):
        assert "scroll-margin" not in artigo


def test_nao_publica_estrutura_remuneratoria():
    html = _html()
    assert "ESTRUTURA REMUNERATÓRIA" not in html
    assert "Estrutura Remuneratória" not in html
    assert "estrutura-remuneratoria" not in html


def test_acoes_nomeadas_com_foco_visivel_e_sem_overflow_horizontal():
    html = _html()
    for node in _cadeia_ate_main(html):
        classes = node["attrs"].get("class", "").split()
        assert "min-w-0" in classes, node["tag"]
    css = (RAIZ / "assets" / "css" / "main.css").read_text(encoding="utf-8")
    assert re.search(
        r"\.focus-visible\\:outline-primary:focus-visible\{[^}]*outline-color:#862120",
        css,
    )
    for artigo, (nome, _) in zip(_artigos(html), DOCUMENTOS, strict=True):
        acoes = []
        for attrs, inner in _ancoras(artigo):
            texto = _texto(inner)
            if "Visualizar" in texto or "Baixar" in texto:
                acoes.append((attrs, texto))
                assert "focus-visible:outline-primary" in attrs, nome
                aria = re.search(r'aria-label="([^"]*)"', attrs)
                nome_acessivel = aria.group(1) if aria else texto
                assert nome in nome_acessivel, nome
        assert len(acoes) == 2, nome
