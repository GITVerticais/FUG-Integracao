"""Trava a ordem publicada das abas em estrutura-organizacional/index.html.

Rodar com: python -m pytest tools/test_abas.py -q
"""
import pathlib
import re

PAGINA = pathlib.Path(__file__).resolve().parent.parent / "estrutura-organizacional" / "index.html"

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
