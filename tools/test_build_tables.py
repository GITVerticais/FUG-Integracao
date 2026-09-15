"""Cobre a matriz de I/O de tools/build_tables.py.

Cada teste monta um repositorio minimo em tmp_path: nada aqui toca os
arquivos reais de data/ ou estrutura-organizacional/.

Rodar com: python -m pytest tools/test_build_tables.py -q
"""
import json
import pathlib
import re
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import build_tables  # noqa: E402

SECOES = ("diretorias", "corpo-funcional", "estrutura-remuneratoria")

PAGINA_MODELO = """<!DOCTYPE html>
<html lang="pt-br">
<body>
{blocos}
</body>
</html>
"""

COLEGIADOS_MODELO = [
    {
        "id": "diretorias-estaduais",
        "nome": "Diretorias Estaduais",
        "total": 3,
        "registros": [
            {
                "unidade": "Acre",
                "cargo": "PRESIDENTE",
                "nome": "Ana Acre",
                "cpf": "826.XXX.XXX-06",
                "vago": False,
            },
            {
                "unidade": "Ceará",
                "cargo": "PRESIDENTE",
                "nome": "Bruno Ceará",
                "cpf": "111.XXX.XXX-11",
                "vago": False,
            },
            {
                "unidade": "Ceará",
                "cargo": "DIRETOR(A) DE FORMAÇÃO POLÍTICA",
                "nome": "Não preenchido",
                "cpf": "—",
                "vago": True,
            },
        ],
    },
    {
        "id": "diretoria-administrativa",
        "nome": "Diretoria Administrativa",
        "total": 9,
        "registros": [
            {
                "unidade": "Nacional",
                "cargo": "PRESIDENTE",
                "nome": "Carla Admin",
                "cpf": "222.XXX.XXX-22",
                "vago": False,
            },
        ],
    },
    {
        "id": "conselho-curador",
        "nome": "Conselho Curador",
        "total": 108,
        "registros": [
            {
                "unidade": "São Paulo",
                "cargo": "VICE-PRESIDENTE",
                "nome": "Maria Rita Carra Navarro",
                "cpf": "FUG - Administrativo 2 adm2: não tem o CPF na planilha que tenho acesso",
                "vago": False,
            },
            {
                "unidade": "Rio de Janeiro",
                "cargo": "VICE-PRESIDENTE",
                "nome": "Katia Damiana Alves Pereira Lobo",
                "cpf": "773.XXX.XXX–04",
                "vago": False,
            },
        ],
    },
    {
        "id": "conselho-fiscal",
        "nome": "Conselho Fiscal",
        "total": 2,
        "registros": [
            {
                "unidade": "Nacional",
                "cargo": "PRESIDENTE",
                "nome": "Maria de Souza",
                "cpf": "000.XXX.XXX-00",
                "vago": False,
            },
            {
                "unidade": "Ceará",
                "cargo": "SUPLENTE",
                "nome": "Maria Residual",
                "cpf": "—",
                "vago": True,
            },
        ],
    },
    {
        "id": "conselho-editorial",
        "nome": "Conselho Editorial",
        "total": 7,
        "registros": [
            {
                "unidade": "Nacional",
                "cargo": "PRESIDENTE",
                "nome": "Elena Editorial",
                "cpf": "333.XXX.XXX-33",
                "vago": False,
            },
        ],
    },
]

DADOS_MODELO = {
    "diretorias.json": {
        "ano": 2025,
        "colegiados": COLEGIADOS_MODELO,
    },
    "corpo-funcional.json": {
        "ano": 2025,
        "total": 1,
        "registros": [
            {"unidade": "Distrito Federal", "nome": "João da Silva", "cargo": "Copeiro"}
        ],
    },
    "estrutura-remuneratoria.json": {
        "ano": 2025,
        "total_quadro_preenchido": 0,
        "cargos": [
            {
                "cargo": "Gerente",
                "nivel": 8,
                "quadro_total": 3,
                "quadro_preenchido": 0,
                "salario_base": "R$ 14.000,00",
                "faixa_media": "R$ 17.000,00",
                "faixa_maxima": "R$ 20.000,00",
                "adicionais": "—",
            }
        ],
    },
}


def escrever_dados(destino, ajustes=None, omitir=()):
    destino.mkdir(parents=True, exist_ok=True)
    for arquivo, conteudo in DADOS_MODELO.items():
        if arquivo in omitir:
            continue
        conteudo = (ajustes or {}).get(arquivo, conteudo)
        (destino / arquivo).write_text(
            json.dumps(conteudo, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    return destino


def escrever_pagina(caminho, secoes=SECOES, sem_fim=()):
    blocos = []
    for secao in secoes:
        blocos.append(f"        <!-- BLOCO:{secao}:INICIO -->")
        if secao not in sem_fim:
            blocos.append(f"        <!-- BLOCO:{secao}:FIM -->")
    caminho.write_text(
        PAGINA_MODELO.format(blocos="\n".join(blocos)), encoding="utf-8", newline="\n"
    )
    return caminho


def bloco(saida, secao):
    inicio = saida.index(f"<!-- BLOCO:{secao}:INICIO -->")
    fim = saida.index(f"<!-- BLOCO:{secao}:FIM -->")
    return saida[inicio:fim]


def trecho_da_linha(saida, texto, antes=5, depois=2):
    linhas = saida.splitlines()
    idx = next(i for i, linha in enumerate(linhas) if texto in linha)
    return "\n".join(linhas[max(0, idx - antes) : idx + depois + 1])


@pytest.fixture
def repo(tmp_path):
    dados = escrever_dados(tmp_path / "data")
    pagina = escrever_pagina(tmp_path / "index.html")
    return dados, pagina


def test_injeta_as_tres_secoes_preservando_marcadores(repo):
    dados, pagina = repo
    assert build_tables.gerar(dados, pagina) is True

    saida = pagina.read_text(encoding="utf-8")
    for secao in SECOES:
        assert f"<!-- BLOCO:{secao}:INICIO -->" in saida
        assert f"<!-- BLOCO:{secao}:FIM -->" in saida
    assert "Maria de Souza" in saida
    assert "João da Silva" in saida
    assert "Gerente" in saida
    # Uma <tr> por linha, para que o HTML servido seja grepavel.
    assert sum(1 for l in saida.splitlines() if "<tr" in l) >= 4


def test_reexecucao_nao_altera_bytes(repo):
    dados, pagina = repo
    build_tables.gerar(dados, pagina)
    primeira = pagina.read_bytes()

    assert build_tables.gerar(dados, pagina) is False
    assert pagina.read_bytes() == primeira


def test_marcador_de_fim_ausente_aborta_sem_escrever(tmp_path):
    dados = escrever_dados(tmp_path / "data")
    pagina = escrever_pagina(tmp_path / "index.html", sem_fim=("corpo-funcional",))
    antes = pagina.read_bytes()

    with pytest.raises(build_tables.ErroDeGeracao) as erro:
        build_tables.gerar(dados, pagina)

    assert "BLOCO:corpo-funcional:FIM" in str(erro.value)
    assert str(pagina) in str(erro.value)
    assert pagina.read_bytes() == antes


def test_json_ausente_aborta_orientando_npm_run_dados(tmp_path):
    dados = escrever_dados(tmp_path / "data", omitir=("diretorias.json",))
    pagina = escrever_pagina(tmp_path / "index.html")
    antes = pagina.read_bytes()

    with pytest.raises(build_tables.ErroDeGeracao) as erro:
        build_tables.gerar(dados, pagina)

    assert "diretorias.json" in str(erro.value)
    assert "npm run dados" in str(erro.value)
    assert pagina.read_bytes() == antes


def test_caractere_reservado_e_escapado(tmp_path):
    ajuste = json.loads(json.dumps(DADOS_MODELO["corpo-funcional.json"]))
    ajuste["registros"][0]["nome"] = 'Ana <script>alert("x")</script> & Cia'
    ajuste["registros"][0]["cargo"] = "Auxiliar & Suporte"
    dados = escrever_dados(tmp_path / "data", ajustes={"corpo-funcional.json": ajuste})
    pagina = escrever_pagina(tmp_path / "index.html")

    build_tables.gerar(dados, pagina)
    saida = pagina.read_text(encoding="utf-8")

    assert "<script>alert" not in saida
    assert "Ana &lt;script&gt;" in saida
    assert "Auxiliar &amp; Suporte" in saida


def test_registro_vago_exibe_nao_preenchido_e_marca_a_linha(repo):
    dados, pagina = repo
    build_tables.gerar(dados, pagina)
    saida = pagina.read_text(encoding="utf-8")

    linha_vaga = next(l for l in saida.splitlines() if 'data-vago="true"' in l)
    assert linha_vaga.strip().startswith("<tr")
    assert "<em class=\"text-on-surface-variant\">Não preenchido</em>" in saida
    assert "Maria Residual" not in saida
    trecho_vago = trecho_da_linha(saida, 'data-vago="true"', depois=5)
    assert 'whitespace-nowrap">—</td>' in trecho_vago
    # A linha preenchida ao lado nao herda a marcacao.
    assert saida.count('data-vago="true"') == 2


def test_legenda_transcreve_total_da_origem(tmp_path):
    ajuste_dir = json.loads(json.dumps(DADOS_MODELO["diretorias.json"]))
    ajuste_dir["colegiados"][3]["total"] = 99
    ajuste_cf = json.loads(json.dumps(DADOS_MODELO["corpo-funcional.json"]))
    ajuste_cf["total"] = 77
    dados = escrever_dados(
        tmp_path / "data",
        ajustes={
            "diretorias.json": ajuste_dir,
            "corpo-funcional.json": ajuste_cf,
        },
    )
    pagina = escrever_pagina(tmp_path / "index.html")

    build_tables.gerar(dados, pagina)
    saida = pagina.read_text(encoding="utf-8")

    assert "99 registros." in saida
    assert "77 registros." in saida
    assert "2 registros." not in saida
    assert "1 cargos." not in saida


def test_main_devolve_1_e_nao_escreve_quando_falta_json(tmp_path, capsys):
    dados = escrever_dados(tmp_path / "data", omitir=("estrutura-remuneratoria.json",))
    pagina = escrever_pagina(tmp_path / "index.html")
    antes = pagina.read_bytes()

    codigo = build_tables.main(["--dados", str(dados), "--pagina", str(pagina)])

    assert codigo == 1
    assert "npm run dados" in capsys.readouterr().err
    assert pagina.read_bytes() == antes


def test_main_devolve_0_no_caminho_feliz(repo):
    dados, pagina = repo
    assert build_tables.main(["--dados", str(dados), "--pagina", str(pagina)]) == 0


def test_cinco_colegiados_viram_cinco_tabelas_com_quatro_colunas(repo):
    dados, pagina = repo
    build_tables.gerar(dados, pagina)
    diretorias = bloco(pagina.read_text(encoding="utf-8"), "diretorias")

    assert diretorias.count("<table") == 5
    for nome, total in (
        ("Diretorias Estaduais", "3 registros."),
        ("Diretoria Administrativa", "9 registros."),
        ("Conselho Curador", "108 registros."),
        ("Conselho Fiscal", "2 registros."),
        ("Conselho Editorial", "7 registros."),
    ):
        assert f">{nome}</h3>" in diretorias
        assert total in diretorias

    cabecalhos = re.findall(
        r'<th class="[^"]*" scope="col">(Unidade|Cargo|Nome|CPF)</th>', diretorias
    )
    assert cabecalhos == ["Unidade", "Cargo", "Nome", "CPF"] * 5
    assert diretorias.count('scope="col"') == 20


def test_cpf_mascarado_sai_identico_na_celula(repo):
    dados, pagina = repo
    build_tables.gerar(dados, pagina)
    trecho = trecho_da_linha(pagina.read_text(encoding="utf-8"), "Ana Acre")
    assert "826.XXX.XXX-06" in trecho
    assert "data-vago" not in trecho


def test_traco_unicode_no_cpf_vira_hifen_ascii(repo):
    dados, pagina = repo
    build_tables.gerar(dados, pagina)
    saida = pagina.read_text(encoding="utf-8")
    trecho = trecho_da_linha(saida, "Katia Damiana Alves Pereira Lobo")
    assert "773.XXX.XXX-04" in trecho
    assert "773.XXX.XXX–04" not in saida
    assert "data-vago" not in trecho


def test_cpf_ocupado_fora_do_formato_vira_traco_sem_marcar_vago(repo):
    dados, pagina = repo
    build_tables.gerar(dados, pagina)
    saida = pagina.read_text(encoding="utf-8")
    trecho = trecho_da_linha(saida, "Maria Rita Carra Navarro")

    assert "Maria Rita Carra Navarro" in trecho
    assert "whitespace-nowrap\">—</td>" in trecho
    assert "data-vago" not in trecho
    assert "FUG - Administrativo" not in saida
    assert "Não preenchido" not in trecho


def test_cpf_completo_ocupado_nao_aparece_no_html(tmp_path):
    ajuste = json.loads(json.dumps(DADOS_MODELO["diretorias.json"]))
    ajuste["colegiados"][1]["registros"].append(
        {
            "unidade": "Nacional",
            "cargo": "SUPLENTE",
            "nome": "Fulano Completo",
            "cpf": "123.456.789-00",
            "vago": False,
        }
    )
    dados = escrever_dados(tmp_path / "data", ajustes={"diretorias.json": ajuste})
    pagina = escrever_pagina(tmp_path / "index.html")

    build_tables.gerar(dados, pagina)
    saida = pagina.read_text(encoding="utf-8")
    trecho = trecho_da_linha(saida, "Fulano Completo")

    assert "123.456.789-00" not in saida
    assert "Fulano Completo" in trecho
    assert 'whitespace-nowrap">—</td>' in trecho
    assert "data-vago" not in trecho
