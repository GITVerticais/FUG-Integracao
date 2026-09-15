"""Injeta as tabelas de estrutura organizacional no HTML publicado.

Le os JSON normalizados de data/ (produzidos por tools/xlsx_to_json.py e
tools/pdf_to_json.py a partir dos arquivos oficiais em downloads/) e substitui
o conteudo entre os marcadores

    <!-- BLOCO:<secao>:INICIO -->
    <!-- BLOCO:<secao>:FIM -->

de estrutura-organizacional/index.html. Os marcadores sao preservados, de modo
que rodar o script duas vezes seguidas nao altera um byte do arquivo.

O script apenas transcreve e escapa: nenhum valor e calculado, conciliado ou
inferido. Se um marcador ou um JSON faltar, aborta sem escrever nada.
"""
import argparse
import html
import json
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DADOS = RAIZ / "data"
PAGINA = RAIZ / "estrutura-organizacional" / "index.html"

# Exibido no lugar do nome quando o registro de origem vem sem titular.
CARGO_VAGO = "Não preenchido"

# Classes de apresentacao, em tokens do tailwind.config.js. Concentradas aqui
# para que a tabela inteira mude de aparencia num ponto so.
CLS_MOLDURA = "mt-6 overflow-x-auto rounded-lg border border-outline-variant/40 bg-surface-container-lowest"
CLS_TABELA = "w-full text-left text-sm"
CLS_CABECALHO = "bg-surface-container text-on-surface-variant"
CLS_TH = "px-4 py-3 font-semibold whitespace-nowrap"
CLS_TH_NUM = "px-4 py-3 font-semibold whitespace-nowrap text-right"
CLS_LINHA = "border-t border-outline-variant/30"
CLS_LINHA_VAGA = "border-t border-outline-variant/30 bg-surface-container-low"
CLS_TD = "px-4 py-3 align-top"
CLS_TD_NUM = "px-4 py-3 align-top text-right tabular-nums"
CLS_TITULO = "text-xl font-bold text-primary font-headline"
CLS_LEGENDA = "mt-1 text-sm text-on-surface-variant"


class ErroDeGeracao(Exception):
    """Falha que impede a geracao; nada e escrito em disco."""


def esc(valor):
    """Escapa para HTML. Nome ou cargo com `<` ou `&` sai neutralizado."""
    return html.escape("" if valor is None else str(valor), quote=True)


def carregar(dados_dir, arquivo):
    caminho = pathlib.Path(dados_dir) / arquivo
    if not caminho.exists():
        raise ErroDeGeracao(
            f"Arquivo de dados ausente: {caminho}. "
            f"Rode `npm run dados` para regenerar data/*.json a partir de downloads/."
        )
    try:
        return json.loads(caminho.read_text(encoding="utf-8"))
    except json.JSONDecodeError as erro:
        raise ErroDeGeracao(f"JSON invalido em {caminho}: {erro}") from erro


def _celula_nome(registro):
    """Cargo vago vira `Não preenchido`, com enfase que o distingue de um nome."""
    if registro.get("vago"):
        return f'<em class="text-on-surface-variant">{esc(CARGO_VAGO)}</em>'
    return esc(registro.get("nome", ""))


def _cabecalho(colunas):
    """colunas: lista de (rotulo, numerica)."""
    linhas = [f'<thead class="{CLS_CABECALHO}">', "<tr>"]
    for rotulo, numerica in colunas:
        cls = CLS_TH_NUM if numerica else CLS_TH
        linhas.append(f'<th class="{cls}" scope="col">{esc(rotulo)}</th>')
    linhas += ["</tr>", "</thead>"]
    return linhas


def bloco_diretorias(dados):
    """Uma tabela por colegiado: unidade, cargo, nome e CPF parcial."""
    colunas = [("Unidade", False), ("Cargo", False), ("Nome", False), ("CPF", False)]
    linhas = ['<div class="mt-8 space-y-12">']
    for colegiado in dados.get("colegiados", []):
        nome = colegiado.get("nome", "")
        id_titulo = f'titulo-colegiado-{colegiado.get("id", "")}'
        linhas += [
            f'<section aria-labelledby="{esc(id_titulo)}">',
            f'<h3 class="{CLS_TITULO}" id="{esc(id_titulo)}">{esc(nome)}</h3>',
            f'<p class="{CLS_LEGENDA}">{esc(colegiado.get("total", ""))} registros.</p>',
            f'<div class="{CLS_MOLDURA}">',
            f'<table class="{CLS_TABELA}">',
            f'<caption class="sr-only">{esc(nome)}: unidade de representação, '
            f"cargo, nome e CPF parcial de cada integrante.</caption>",
        ]
        linhas += _cabecalho(colunas)
        linhas.append("<tbody>")
        for registro in colegiado.get("registros", []):
            cls = CLS_LINHA_VAGA if registro.get("vago") else CLS_LINHA
            vago = ' data-vago="true"' if registro.get("vago") else ""
            linhas += [
                f'<tr class="{cls}"{vago}>',
                f'<td class="{CLS_TD}">{esc(registro.get("unidade", ""))}</td>',
                f'<td class="{CLS_TD}">{esc(registro.get("cargo", ""))}</td>',
                f'<td class="{CLS_TD}">{_celula_nome(registro)}</td>',
                f'<td class="{CLS_TD} whitespace-nowrap">{esc(registro.get("cpf", ""))}</td>',
                "</tr>",
            ]
        linhas += ["</tbody>", "</table>", "</div>", "</section>"]
    linhas.append("</div>")
    return linhas


def bloco_corpo_funcional(dados):
    """Tabela unica: unidade, nome e cargo de cada empregado."""
    colunas = [("Unidade", False), ("Nome", False), ("Cargo", False)]
    registros = dados.get("registros", [])
    linhas = [
        f'<p class="{CLS_LEGENDA}">{esc(dados.get("total", ""))} registros.</p>',
        f'<div class="{CLS_MOLDURA}">',
        f'<table class="{CLS_TABELA}">',
        '<caption class="sr-only">Corpo funcional: unidade de representação, '
        "nome e cargo de cada empregado.</caption>",
    ]
    linhas += _cabecalho(colunas)
    linhas.append("<tbody>")
    for registro in registros:
        linhas += [
            f'<tr class="{CLS_LINHA}">',
            f'<td class="{CLS_TD}">{esc(registro.get("unidade", ""))}</td>',
            f'<td class="{CLS_TD}">{_celula_nome(registro)}</td>',
            f'<td class="{CLS_TD}">{esc(registro.get("cargo", ""))}</td>',
            "</tr>",
        ]
    linhas += ["</tbody>", "</table>", "</div>"]
    return linhas


def bloco_estrutura_remuneratoria(dados):
    """Tabela unica, transcrita do PDF oficial coluna a coluna."""
    colunas = [
        ("Cargo", False),
        ("Nível", True),
        ("Vagas previstas", True),
        ("Vagas preenchidas", True),
        ("Salário base", True),
        ("Faixa média", True),
        ("Faixa máxima", True),
        ("Adicionais", False),
    ]
    cargos = dados.get("cargos", [])
    linhas = [
        f'<p class="{CLS_LEGENDA}">Valores transcritos do PDF oficial, sem qualquer cálculo.</p>',
        f'<div class="{CLS_MOLDURA}">',
        f'<table class="{CLS_TABELA}">',
        '<caption class="sr-only">Estrutura remuneratória: cargo, nível, vagas '
        "previstas e preenchidas, salário base, faixas média e máxima e adicionais.</caption>",
    ]
    linhas += _cabecalho(colunas)
    linhas.append("<tbody>")
    for cargo in cargos:
        linhas += [
            f'<tr class="{CLS_LINHA}">',
            f'<th class="{CLS_TD} font-medium" scope="row">{esc(cargo.get("cargo", ""))}</th>',
            f'<td class="{CLS_TD_NUM}">{esc(cargo.get("nivel", ""))}</td>',
            f'<td class="{CLS_TD_NUM}">{esc(cargo.get("quadro_total", ""))}</td>',
            f'<td class="{CLS_TD_NUM}">{esc(cargo.get("quadro_preenchido", ""))}</td>',
            f'<td class="{CLS_TD_NUM} whitespace-nowrap">{esc(cargo.get("salario_base", ""))}</td>',
            f'<td class="{CLS_TD_NUM} whitespace-nowrap">{esc(cargo.get("faixa_media", ""))}</td>',
            f'<td class="{CLS_TD_NUM} whitespace-nowrap">{esc(cargo.get("faixa_maxima", ""))}</td>',
            f'<td class="{CLS_TD}">{esc(cargo.get("adicionais", ""))}</td>',
            "</tr>",
        ]
    linhas += ["</tbody>", "</table>", "</div>"]
    return linhas


# secao -> (arquivo em data/, funcao que monta as linhas)
SECOES = {
    "diretorias": ("diretorias.json", bloco_diretorias),
    "corpo-funcional": ("corpo-funcional.json", bloco_corpo_funcional),
    "estrutura-remuneratoria": ("estrutura-remuneratoria.json", bloco_estrutura_remuneratoria),
}


def _marcador(documento, secao, momento, pagina, inicio=0):
    padrao = re.compile(rf"<!--\s*BLOCO:{re.escape(secao)}:{momento}\s*-->")
    achado = padrao.search(documento, inicio)
    if not achado:
        raise ErroDeGeracao(
            f"Marcador BLOCO:{secao}:{momento} não encontrado em {pagina}. "
            f"Nada foi escrito."
        )
    return achado


def _aninhar(linhas):
    """Recua as linhas conforme o aninhamento das tags.

    Regra simples porque o gerador so emite tags bem formadas, uma por linha:
    linha que abre um elemento e nao o fecha na mesma linha aumenta o nivel.
    """
    nivel = 0
    saida = []
    for linha in linhas:
        if linha.startswith("</"):
            nivel = max(0, nivel - 1)
        saida.append("    " * nivel + linha)
        if linha.startswith("<") and not linha.startswith("</") and "</" not in linha:
            nivel += 1
    return saida


def substituir(documento, secao, linhas, pagina):
    """Troca o miolo entre os marcadores da secao, preservando os marcadores."""
    abre = _marcador(documento, secao, "INICIO", pagina)
    fecha = _marcador(documento, secao, "FIM", pagina, inicio=abre.end())

    # Indentacao herdada da linha do marcador de abertura: mantem o HTML
    # gerado alinhado ao arquivo e o resultado estavel entre execucoes.
    coluna = abre.start() - (documento.rfind("\n", 0, abre.start()) + 1)
    recuo = " " * coluna

    miolo = "".join(f"{recuo}{linha}\n" for linha in _aninhar(linhas))
    return documento[: abre.end()] + "\n" + miolo + recuo + documento[fecha.start() :]


def gerar(dados_dir=DADOS, pagina=PAGINA):
    """Monta o documento inteiro em memoria e so entao escreve.

    Retorna True se o arquivo mudou. Qualquer falha levanta ErroDeGeracao
    antes de qualquer escrita.
    """
    pagina = pathlib.Path(pagina)
    if not pagina.exists():
        raise ErroDeGeracao(f"Página não encontrada: {pagina}. Nada foi escrito.")

    # Carrega todos os dados antes de mexer no documento: se um JSON faltar,
    # nenhuma secao chega a ser substituida.
    blocos = {
        secao: construir(carregar(dados_dir, arquivo))
        for secao, (arquivo, construir) in SECOES.items()
    }

    original = pagina.read_text(encoding="utf-8")
    documento = original
    for secao, linhas in blocos.items():
        documento = substituir(documento, secao, linhas, pagina)

    if documento == original:
        return False
    pagina.write_text(documento, encoding="utf-8", newline="\n")
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dados", default=DADOS, help="diretorio dos JSON normalizados")
    parser.add_argument("--pagina", default=PAGINA, help="HTML com os marcadores BLOCO:*")
    args = parser.parse_args(argv)

    try:
        mudou = gerar(args.dados, args.pagina)
    except ErroDeGeracao as erro:
        print(f"erro: {erro}", file=sys.stderr)
        return 1

    caminho = pathlib.Path(args.pagina)
    try:
        caminho = caminho.relative_to(RAIZ)
    except ValueError:
        pass
    print(f"  {caminho} - {'atualizado' if mudou else 'sem alteracao'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
