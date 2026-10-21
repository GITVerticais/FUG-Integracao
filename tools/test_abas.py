"""Trava a ordem das abas e o scroll, sem :target.

Rodar com: python -m pytest tools/test_abas.py -q
"""
import pathlib
import re
import subprocess

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PAGINA = RAIZ / "app" / "estrutura-organizacional" / "page.tsx"
CSS = RAIZ / "app" / "globals.css"

ORDEM = (
    "diretorias",
    "corpo-funcional",
    "estrutura-remuneratoria",
    "organograma",
)


def test_organograma_e_a_ultima_aba():
    html = PAGINA.read_text(encoding="utf-8")
    nav = re.search(r'aria-label="Seções da estrutura organizacional"[\s\S]*?</nav>', html)
    assert nav
    hrefs = re.findall(r'href="#([^"]+)"', nav.group(0))
    paineis = re.findall(r'<section\b[^>]*\bid="([^"]+)"', html)
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
    intro = markup.find('<p className="text-on-surface-variant leading-relaxed max-w-3xl">')
    png = markup.find('href="/img/organograma-fug-2025.png"')
    pdf = markup.find('href="/downloads/organograma-fug-2025.pdf"')
    figura = markup.find("<figure")
    assert -1 not in (h2, intro, png, pdf, figura)
    assert h2 < intro < png < pdf < figura
    assert "<figcaption" not in markup
    assert 'aria-label="Baixar o PDF oficial do Organograma geral"' in markup
    assert re.search(
        r'<a\b[^>]*\bhref="/downloads/organograma-fug-2025.pdf"[^>]*\bdownload\b',
        markup,
    )
    inner = re.search(r"<figure\b[^>]*>(.*?)</figure>", markup)
    assert inner
    assert re.search(r'<img\b[^>]*\balt="[^"]+"', inner.group(1))
    assert "<p" not in inner.group(1)
    assert "<a " not in inner.group(1)


def test_abas_nao_escondem_painel_com_target_nem_has():
    css = CSS.read_text(encoding="utf-8")
    assert ":has(" not in css
    assert ":target" not in css
    pagina = PAGINA.read_text(encoding="utf-8")
    assert "aba-painel" in pagina
    assert "painel.hidden" in pagina


def test_toggle_revela_so_o_painel_do_clique_ou_do_hash():
    pagina = PAGINA.read_text(encoding="utf-8")
    script = re.search(
        r'<Script id="abas-estrutura"[^>]*>\{`([\s\S]*?)`\}</Script>',
        pagina,
    )
    assert script, "script das abas"
    proc = subprocess.run(
        ["node", "-e", _HARNESS],
        input=script.group(1),
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    assert proc.returncode == 0, proc.stderr


_HARNESS = r"""
const fs = require("fs");
const vm = require("vm");
const code = fs.readFileSync(0, "utf8");
function cls(names) {
  const set = new Set(names);
  return {
    contains(n) { return set.has(n); },
    toggle(n, on) { if (on) set.add(n); else set.delete(n); },
  };
}
function el(tag, id, names) {
  return {
    tag, id, hidden: false, parentNode: null,
    classList: cls(names),
    attrs: {},
    setAttribute(k, v) { this.attrs[k] = v; },
    getAttribute(k) { return k in this.attrs ? this.attrs[k] : null; },
    closest(sel) {
      for (let n = this; n; n = n.parentNode) {
        if (sel === "a" && n.tag === "a") return n;
        if (sel === ".aba-painel" && n.classList.contains("aba-painel")) return n;
      }
      return null;
    },
  };
}
function mount(hash) {
  const ids = ["diretorias", "corpo-funcional", "estrutura-remuneratoria", "organograma"];
  const nodes = [];
  const panels = ids.map((id) => {
    const panel = el("section", id, ["aba-painel"]);
    panel.hidden = id !== "diretorias";
    nodes.push(panel);
    return panel;
  });
  const links = ids.map((id) => {
    const link = el("a", "", ["aba-link"]);
    link.setAttribute("href", "#" + id);
    nodes.push(link);
    return link;
  });
  const clicks = [];
  const hashes = [];
  const location = { hash };
  vm.runInNewContext(code, {
    document: {
      addEventListener(type, fn) { if (type === "click") clicks.push(fn); },
      getElementById(id) { return nodes.find((n) => n.id === id) || null; },
      querySelectorAll(sel) {
        if (sel === ".aba-painel") return nodes.filter((n) => n.classList.contains("aba-painel"));
        if (sel === "a.aba-link") return nodes.filter((n) => n.tag === "a" && n.classList.contains("aba-link"));
        return [];
      },
    },
    location,
    window: {
      location,
      addEventListener(type, fn) { if (type === "hashchange") hashes.push(fn); },
    },
  });
  return { panels, links, clicks, hashes, location };
}
function visiveis(panels) {
  return panels.filter((panel) => !panel.hidden).map((panel) => panel.id).join(",");
}
const escolhido = mount("");
escolhido.clicks.forEach((fn) => fn({
  target: escolhido.links[1], button: 0, defaultPrevented: false,
  metaKey: false, ctrlKey: false, shiftKey: false, altKey: false,
  preventDefault() {},
}));
if (visiveis(escolhido.panels) !== "corpo-funcional") {
  console.error("click " + visiveis(escolhido.panels));
  process.exit(1);
}
escolhido.location.hash = "#estrutura-remuneratoria";
escolhido.hashes.forEach((fn) => fn());
if (visiveis(escolhido.panels) !== "estrutura-remuneratoria") {
  console.error("hash " + visiveis(escolhido.panels));
  process.exit(1);
}
const aberto = mount("#estrutura-remuneratoria");
if (visiveis(aberto.panels) !== "estrutura-remuneratoria") {
  console.error("load " + visiveis(aberto.panels));
  process.exit(1);
}
"""


def test_scroll_das_ancoras_compensa_header_sticky():
    css = CSS.read_text(encoding="utf-8")
    html_bloco = re.search(r"html\s*\{([^}]+)\}", css)
    assert html_bloco, "html"
    assert re.search(r"scroll-padding-top:\s*6rem", html_bloco.group(1))
    assert not re.search(r":target\s*\{[^}]*scroll-margin-top:", css)
    painel_bloco = re.search(r"\.aba-painel\s*\{([^}]+)\}", css)
    assert painel_bloco, ".aba-painel"
    assert re.search(r"scroll-margin-top:\s*2rem", painel_bloco.group(1))
