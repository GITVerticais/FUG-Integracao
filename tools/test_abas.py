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


def test_organograma_texto_e_links_antes_da_figura():
    html = PAGINA.read_text(encoding="utf-8")
    secao = re.search(
        r'<section\b[^>]*\bid="organograma"[\s\S]*?</section>',
        html,
    )
    assert secao, "organograma"
    markup = re.sub(r"\s+", " ", secao.group(0))
    h2 = markup.find('id="titulo-organograma"')
    intro = markup.find('<p class="text-on-surface-variant leading-relaxed max-w-3xl">')
    png = markup.find('href="../assets/img/organograma-fug-2025.png"')
    pdf = markup.find('href="../downloads/organograma-fug-2025.pdf"')
    figura = markup.find("<figure")
    assert -1 not in (h2, intro, png, pdf, figura)
    assert h2 < intro < png < pdf < figura
    assert "<figcaption" not in markup
    assert 'aria-label="Baixar o PDF oficial do Organograma geral"' in markup
    assert re.search(
        r'<a\b[^>]*\bhref="../downloads/organograma-fug-2025.pdf"[^>]*\bdownload\b',
        markup,
    )
    inner = re.search(r"<figure\b[^>]*>(.*?)</figure>", markup)
    assert inner
    assert re.search(r'<img\b[^>]*\balt="[^"]+"', inner.group(1))
    assert "<p" not in inner.group(1)
    assert "<a " not in inner.group(1)


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

