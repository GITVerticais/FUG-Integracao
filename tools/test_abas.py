"""Trava a ordem publicada das abas em estrutura-organizacional/index.html.

Rodar com: python -m pytest tools/test_abas.py -q
"""
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PAGINA = RAIZ / "estrutura-organizacional" / "index.html"
CSS = RAIZ / "assets" / "css" / "input.css"
MAIN = RAIZ / "assets" / "css" / "main.css"

ORDEM = (
    "diretorias",
    "corpo-funcional",
    "estrutura-remuneratoria",
    "organograma",
)


def test_organograma_e_a_ultima_aba():
    html = PAGINA.read_text(encoding="utf-8")
    hrefs = re.findall(r'<a class="aba-link\b[^"]*"\s+href="#([^"]+)"', html)
    paineis = re.findall(
        r'<section\b[^>]*\bclass="[^"]*\baba-painel\b[^"]*"[\s\S]*?\bid="([^"]+)"',
        html,
    )
    assert hrefs == list(ORDEM)
    assert paineis == list(ORDEM)


def test_filtro_de_abas_cobre_target_interno_em_diretorias():
    css = CSS.read_text(encoding="utf-8")
    assert ":has(.aba-painel :target)" in css
    assert ":has(#diretorias :target)" in css

    main = MAIN.read_text(encoding="utf-8")
    assert re.search(
        r"\.aba-painel:not\(:has\(:target\)\)[^{]*\{[^}]*display:\s*none",
        main,
    )
    for painel in ORDEM:
        assert f".abas:has(#{painel} :target)" in main

