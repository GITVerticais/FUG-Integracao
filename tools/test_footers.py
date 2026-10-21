"""Trava footers, os seis cartões e o chrome compartilhado.

Rodar com: python -m pytest tools/test_footers.py -q
"""
import json
import pathlib
import re
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
HOME = ROOT / "app" / "page.tsx"
FOOTER = ROOT / "components" / "Footer.tsx"
HEADER = ROOT / "components" / "Header.tsx"
LAYOUT = ROOT / "app" / "layout.tsx"
CARTOES_DEV = (
    (r"\{/\* Editais \*/\}.*?\{/\* Dados Contábeis \*/\}", "Editais"),
    (r"\{/\* Dados Contábeis \*/\}.*?\{/\* FAQ \*/\}", "Dados Contábeis"),
    (r"\{/\* FAQ \*/\}.*?\{/\* Ouvidoria \*/\}", "FAQ"),
)
ORDEM = (
    "Governança",
    "Estrutura Organizacional",
    "Editais",
    "Dados Contábeis",
    "FAQ",
    "Ouvidoria",
)


def _texto(html: str) -> str:
    return " ".join(re.sub(r"<[^>]+>", " ", html).split()).casefold()


def _footer() -> str:
    return FOOTER.read_text(encoding="utf-8")


def test_footers_sem_em_desenvolvimento():
    footer = _footer()
    assert "em desenvolvimento" not in _texto(footer)
    assert "espaço de integridade" in _texto(footer)
    layout = LAYOUT.read_text(encoding="utf-8")
    assert "<Footer" in layout
    assert layout.index("<Header") < layout.index("{children}")
    assert layout.index("{children}") < layout.index("<Footer")


def test_footers_copyright_2026():
    assert re.search(r"(?:©|&copy;)\s*2026", _footer())


def test_footer_home_nao_fica_fixo():
    footer = _footer()
    assert not re.search(r"\bsticky\b", footer.casefold())
    assert not re.search(r"\bfixed\b", footer.casefold())
    home = HOME.read_text(encoding="utf-8")
    assert "<main" in home and "</main>" in home
    assert "<footer" not in home.casefold()
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
            r'<div className="js-btn-overlay[^"]*">([\s\S]*?)</div>',
            cartao,
        )
        assert overlay, f"overlay ausente em {nome}"
        assert "group-hover:opacity-100" in overlay.group(0), nome
        assert "<button" in cartao and "href=" not in cartao, nome
        assert "em desenvolvimento" in _texto(overlay.group(1)), nome
    assert "1500" in html


def test_seis_cartoes_faq_e_ouvidoria_na_ultima_linha():
    html = HOME.read_text(encoding="utf-8")
    pos = [html.index(nome) for nome in ORDEM]
    assert pos == sorted(pos)
    assert "grid-cols-1 md:grid-cols-2" in html
    assert "md:col-span-2" not in html
    ouv = html.split("{/* Ouvidoria */}", 1)[1].split("<Script", 1)[0]
    assert 'href="/ouvidoria"' in ouv
    assert "js-dev-button" not in ouv
    assert "em desenvolvimento" not in ouv
    assert (ROOT / "app" / "ouvidoria" / "page.tsx").is_file()


def test_destinos_do_chrome():
    header = HEADER.read_text(encoding="utf-8")
    assert header.count('href="/"') >= 2
    assert header.count('href="/ouvidoria"') == 2
    assert header.count('href="#"') == 2
    assert "Políticas" in header and "Treinamentos" in header
    assert re.search(r"<button\b[^>]*>account_circle</button>", header)
    treino = re.search(r"<div\b[^>]*>\s*<span[^>]*>school</span>[\s\S]*?Treino", header)
    assert treino
    assert "<a" not in treino.group(0)


def test_ouvidoria_sem_formulario_nem_canal():
    html = (ROOT / "app" / "ouvidoria" / "page.tsx").read_text(encoding="utf-8").casefold()
    for termo in ("<form", "mailto:", "tel:", "telefone", "e-mail", "email", "horário", "horario", "recaptcha"):
        assert termo not in html


def test_build_copia_downloads_antes_do_next():
    pkg = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    build = pkg["scripts"]["build"]
    assert build.index("node tools/copy_downloads.js") < build.index("next build")
    script = (ROOT / "tools" / "copy_downloads.js").read_text(encoding="utf-8")
    assert 'path.join("public", "downloads")' in script
    assert 'fs.cpSync("downloads"' in script
    with tempfile.TemporaryDirectory() as tmp:
        raiz = pathlib.Path(tmp)
        (raiz / "downloads").mkdir()
        (raiz / "downloads" / "arquivo.pdf").write_bytes(b"pdf")
        subprocess.run(
            ["node", str(ROOT / "tools" / "copy_downloads.js")],
            cwd=raiz,
            check=True,
        )
        assert (raiz / "public" / "downloads" / "arquivo.pdf").is_file()


def test_html_estatico_saiu_e_vercel_nao_publica_a_raiz():
    assert not (ROOT / "index.html").exists()
    assert not (ROOT / "governanca" / "index.html").exists()
    assert not (ROOT / "estrutura-organizacional" / "index.html").exists()
    vercel = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
    assert vercel.get("outputDirectory") != "."
    assert vercel.get("framework") == "nextjs"
