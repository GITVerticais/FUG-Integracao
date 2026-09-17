"""Trava footers sem 'em desenvolvimento' e o da home no fluxo da página.

Rodar com: python -m pytest tools/test_footers.py -q
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
HOME = ROOT / "index.html"
PAGINAS = (
    HOME,
    ROOT / "governanca" / "index.html",
    ROOT / "estrutura-organizacional" / "index.html",
)
FOOTER_RE = re.compile(r"<footer\b([^>]*)>(.*?)</footer>", re.DOTALL | re.IGNORECASE)
CARTOES_DEV = (
    (r"<!-- Editais -->.*?<!-- Dados Contábeis -->", "Editais"),
    (r"<!-- Dados Contábeis -->.*?<!-- FAQ -->", "Dados Contábeis"),
    (r"<!-- FAQ -->.*?</main>", "FAQ"),
)


def _rel(pagina: pathlib.Path) -> str:
    return pagina.relative_to(ROOT).as_posix()


def _texto(html: str) -> str:
    return " ".join(re.sub(r"<[^>]+>", " ", html).split()).casefold()


def _footer(pagina: pathlib.Path) -> tuple[str, str]:
    html = pagina.read_text(encoding="utf-8")
    match = FOOTER_RE.search(html)
    assert match, f"footer ausente em {_rel(pagina)}"
    return match.group(1), match.group(0)


def test_footers_sem_em_desenvolvimento():
    for pagina in PAGINAS:
        _attrs, footer = _footer(pagina)
        texto = _texto(footer)
        assert "em desenvolvimento" not in texto, _rel(pagina)
        assert "espaço de integridade" in texto, _rel(pagina)


def test_footer_home_nao_fica_fixo():
    html = HOME.read_text(encoding="utf-8")
    attrs, footer = _footer(HOME)
    classes = attrs.casefold()
    assert not re.search(r"\bsticky\b", classes)
    assert not re.search(r"\bfixed\b", classes)
    assert html.casefold().find("</main>") < html.casefold().find("<footer")
    texto = _texto(footer)
    for link in ("privacidade", "termos", "suporte"):
        assert link in texto


def test_botoes_sem_pagina_continuam_em_desenvolvimento():
    html = HOME.read_text(encoding="utf-8")
    for padrao, nome in CARTOES_DEV:
        match = re.search(padrao, html, re.DOTALL)
        assert match, f"cartão {nome} não encontrado na home"
        cartao = match.group(0)
        assert "js-dev-button" in cartao, nome
        overlay = re.search(
            r'<div class="js-btn-overlay[^"]*">([\s\S]*?)</div>',
            cartao,
        )
        assert overlay, f"overlay ausente em {nome}"
        assert "em desenvolvimento" in _texto(overlay.group(1)), nome
