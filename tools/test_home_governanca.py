"""Trava o link da home para a página de governança.

Rodar com: python -m pytest tools/test_home_governanca.py -q
"""
import pathlib
import re

HOME = pathlib.Path(__file__).resolve().parent.parent / "index.html"
DESTINO = HOME.parent / "governanca" / "index.html"


def _cartao_governanca(html: str) -> str:
    match = re.search(
        r"<!-- Governança -->.*?<!-- Estrutura Organizacional -->",
        html,
        re.DOTALL,
    )
    assert match, "cartão Governança não encontrado na home"
    return match.group(0)


def test_home_linka_governanca():
    html = HOME.read_text(encoding="utf-8")
    cartao = _cartao_governanca(html)
    ancora = re.search(r"<a\b([^>]*)>([\s\S]*?)</a>", cartao)
    assert ancora, "cartão sem âncora"
    attrs, inner = ancora.group(1), ancora.group(2)
    href = re.search(r'\bhref="([^"]*)"', attrs)
    assert href and href.group(1) == "governanca/index.html"
    assert "target=" not in attrs
    texto = " ".join(re.sub(r"<[^>]+>", " ", inner).split())
    assert "Governança" in texto
    assert "js-dev-button" not in cartao
    assert "js-btn-overlay" not in cartao
    assert "js-btn-content" not in cartao
    assert "em desenvolvimento" not in cartao
    assert DESTINO.is_file()
