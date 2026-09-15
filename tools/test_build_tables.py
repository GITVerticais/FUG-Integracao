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
                "cpf": "564.XXX.XXX-34",
                "vago": False,
            },
            {
                "unidade": "Nacional",
                "cargo": "SUPLENTE",
                "nome": "Fulano Nota Interna",
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
            },
            {
                "cargo": "Trainee",
                "nivel": 3,
                "quadro_total": 5,
                "quadro_preenchido": 0,
                "salario_base": "R$ 1.848,00",
                "faixa_media": "—",
                "faixa_maxima": "—",
                "adicionais": "—",
            },
        ],
    },
}

CABECALHOS_ER = (
    "Cargo",
    "Nível",
    "Vagas previstas",
    "Vagas preenchidas",
    "Salário base",
    "Faixa média",
    "Faixa máxima",
    "Adicionais",
)

CARGOS_ER_20 = [
    ("Secretário Executivo", 10, 1, 0, "R$ 25.000,00", "R$ 35.000,00", "R$ 45.000,00"),
    ("Secretário Executivo Adjunto", 10, 1, 0, "R$ 20.000,00", "R$ 30.000,00", "R$ 35.000,00"),
    ("Procurador Jurídico", 9, 1, 0, "R$ 14.000,00", "R$ 17.000,00", "R$ 20.000,00"),
    ("Gerente", 8, 3, 0, "R$ 14.000,00", "R$ 17.000,00", "R$ 20.000,00"),
    ("Chefe de Gabinete Diretoria Executiva", 7, 1, 1, "R$ 12.000,00", "R$ 15.000,00", "R$ 18.000,00"),
    ("Supervisor", 6, 10, 6, "R$ 11.000,00", "R$ 13.000,00", "R$ 16.000,00"),
    ("Coordenador", 5, 10, 6, "R$ 8.820,00", "R$ 13.000,00", "R$ 16.000,00"),
    ("Assistente Administrativo I", 4, 35, 0, "R$ 5.200,00", "R$ 6.000,00", "R$ 6.540,00"),
    ("Assistente Administrativo II", 4, 35, 0, "R$ 6.549,38", "R$ 6.900,00", "R$ 7.280,00"),
    ("Assistente Administrativo III", 4, 35, 1, "R$ 7.285,32", "R$ 7.900,00", "R$ 8.500,00"),
    ("Auxiliar Administrativo Junior", 3, 35, 6, "R$ 3.106,68", "R$ 3.500,00", "R$ 3.790,00"),
    ("Auxiliar Administrativo Pleno", 3, 35, 1, "R$ 3.800,00", "R$ 4.000,00", "R$ 4.400,00"),
    ("Auxiliar Administrativo Sênior", 3, 35, 3, "R$ 4.480,72", "R$ 4.900,00", "R$ 5.100,00"),
    ("Trainee", 3, 5, 0, "R$ 1.848,00", "—", "—"),
    ("Estagiário Ensino Médio", 2, 5, 2, "R$ 1.300,00", "—", "—"),
    ("Estagiário Superior", 2, 5, 2, "R$ 1.400,00", "—", "—"),
    ("Motorista", 2, 2, 2, "R$ 5.309,64", "R$ 5.900,00", "R$ 6.500,00"),
    ("Aux. Serv. Gerais", 1, 2, 1, "R$ 1.892,94", "R$ 2.100,00", "R$ 3.000,00"),
    ("Copeiro", 1, 1, 1, "R$ 3.704,40", "R$ 4.100,00", "R$ 5.000,00"),
    ("Jovem Aprendiz", 1, 5, 3, "R$ 713,00", "—", "—"),
]


def _cargo_er(cargo, nivel, qt, qp, base, media, maxima):
    return {
        "cargo": cargo,
        "nivel": nivel,
        "quadro_total": qt,
        "quadro_preenchido": qp,
        "salario_base": base,
        "faixa_media": media,
        "faixa_maxima": maxima,
        "adicionais": "—",
    }


def _celulas_er(markup, nome):
    achado = re.search(
        rf'<th class="[^"]*" scope="row">{re.escape(nome)}</th>([\s\S]*?)</tr>',
        markup,
    )
    assert achado, nome
    return re.findall(r"<td class=\"[^\"]*\">([^<]*)</td>", achado.group(1))


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


def test_cpf_mascarado_da_maria_rita_sai_identico_na_celula(repo):
    dados, pagina = repo
    build_tables.gerar(dados, pagina)
    saida = pagina.read_text(encoding="utf-8")
    trecho = trecho_da_linha(saida, "Maria Rita Carra Navarro")

    assert "Maria Rita Carra Navarro" in trecho
    assert "564.XXX.XXX-34" in trecho
    assert "data-vago" not in trecho
    assert "Não preenchido" not in trecho


def test_cpf_ocupado_fora_do_formato_vira_traco_sem_marcar_vago(repo):
    dados, pagina = repo
    build_tables.gerar(dados, pagina)
    saida = pagina.read_text(encoding="utf-8")
    trecho = trecho_da_linha(saida, "Fulano Nota Interna")

    assert "Fulano Nota Interna" in trecho
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


def test_corpo_funcional_colunas_nome_cargo_unidade(repo):
    dados, pagina = repo
    build_tables.gerar(dados, pagina)
    cf = bloco(pagina.read_text(encoding="utf-8"), "corpo-funcional")

    cabecalhos = re.findall(
        r'<th class="[^"]*" scope="col">(Nome|Cargo|Unidade)</th>', cf
    )
    assert cabecalhos == ["Nome", "Cargo", "Unidade"]
    assert cf.count('scope="col"') == 3

    celulas = re.findall(r'<td class="[^"]*">([^<]*)</td>', cf)
    assert celulas == ["João da Silva", "Copeiro", "Distrito Federal"]


def test_corpo_funcional_bloco_sem_dinheiro_nem_cpf(repo):
    dados, pagina = repo
    build_tables.gerar(dados, pagina)
    cf = bloco(pagina.read_text(encoding="utf-8"), "corpo-funcional")

    assert "R$" not in cf
    assert "CPF" not in cf
    assert "cpf" not in cf


def test_corpo_funcional_injeta_29_linhas_nome_cargo_unidade(tmp_path):
    registros = [
        {
            "unidade": f"Unidade {i:02d}",
            "nome": f"Pessoa {i:02d}",
            "cargo": f"Cargo {i:02d}",
        }
        for i in range(29)
    ]
    dados = escrever_dados(
        tmp_path / "data",
        ajustes={
            "corpo-funcional.json": {
                "ano": 2025,
                "total": 29,
                "registros": registros,
            }
        },
    )
    pagina = escrever_pagina(tmp_path / "index.html")
    build_tables.gerar(dados, pagina)
    cf = bloco(pagina.read_text(encoding="utf-8"), "corpo-funcional")

    assert cf.count("<table") == 1
    miolo = re.search(r"<tbody>([\s\S]*)</tbody>", cf)
    assert miolo is not None
    assert miolo.group(1).count("<tr") == 29
    cabecalhos = re.findall(
        r'<th class="[^"]*" scope="col">(Nome|Cargo|Unidade)</th>', cf
    )
    assert cabecalhos == ["Nome", "Cargo", "Unidade"]
    assert [r["nome"] for r in registros] == re.findall(
        r'<td class="[^"]*">(Pessoa \d{2})</td>', cf
    )
    assert "29 registros." in cf


def test_json_ausente_corpo_funcional_aborta_sem_escrever(tmp_path, capsys):
    dados = escrever_dados(tmp_path / "data", omitir=("corpo-funcional.json",))
    pagina = escrever_pagina(tmp_path / "index.html")
    antes = pagina.read_bytes()

    codigo = build_tables.main(["--dados", str(dados), "--pagina", str(pagina)])

    assert codigo == 1
    err = capsys.readouterr().err
    assert "corpo-funcional.json" in err
    assert "npm run dados" in err
    assert pagina.read_bytes() == antes


def test_estrutura_remuneratoria_oito_cabecalhos_incluindo_adicionais(repo):
    dados, pagina = repo
    build_tables.gerar(dados, pagina)
    er = bloco(pagina.read_text(encoding="utf-8"), "estrutura-remuneratoria")

    cabecalhos = re.findall(r'<th class="[^"]*" scope="col">([^<]+)</th>', er)
    assert cabecalhos == list(CABECALHOS_ER)
    assert er.count('scope="col"') == 8
    assert er.count("<table") == 1


def test_estrutura_remuneratoria_travessao_e_adicionais_nao_sao_zero(repo):
    dados, pagina = repo
    build_tables.gerar(dados, pagina)
    er = bloco(pagina.read_text(encoding="utf-8"), "estrutura-remuneratoria")

    gerente = _celulas_er(er, "Gerente")
    assert gerente[5] == "R$ 20.000,00"
    assert gerente[6] == "—"

    trainee = _celulas_er(er, "Trainee")
    assert trainee[3] == "R$ 1.848,00"
    assert trainee[4] == "—"
    assert trainee[5] == "—"
    assert trainee[6] == "—"
    assert trainee[4] not in ("0", "R$ 0", "R$ 0,00")
    assert trainee[5] not in ("0", "R$ 0", "R$ 0,00")

    for nome in ("Gerente", "Trainee"):
        assert _celulas_er(er, nome)[6] == "—"


def test_estrutura_remuneratoria_injeta_20_linhas_na_ordem_do_json(tmp_path):
    cargos = [_cargo_er(*linha) for linha in CARGOS_ER_20]
    dados = escrever_dados(
        tmp_path / "data",
        ajustes={
            "estrutura-remuneratoria.json": {
                "ano": 2025,
                "total_quadro_preenchido": 35,
                "cargos": cargos,
            }
        },
    )
    pagina = escrever_pagina(tmp_path / "index.html")
    build_tables.gerar(dados, pagina)
    er = bloco(pagina.read_text(encoding="utf-8"), "estrutura-remuneratoria")

    assert er.count("<table") == 1
    miolo = re.search(r"<tbody>([\s\S]*)</tbody>", er)
    assert miolo is not None
    assert miolo.group(1).count("<tr") == 20

    nomes = re.findall(r'<th class="[^"]*" scope="row">([^<]+)</th>', er)
    assert nomes[0] == "Secretário Executivo"
    assert nomes[-1] == "Jovem Aprendiz"
    assert nomes == [c["cargo"] for c in cargos]

    for nome, esperado in zip(nomes, CARGOS_ER_20, strict=True):
        cargo, nivel, qt, qp, base, media, maxima = esperado
        assert nome == cargo
        assert _celulas_er(er, nome) == [
            str(nivel),
            str(qt),
            str(qp),
            base,
            media,
            maxima,
            "—",
        ]

    cabecalhos = re.findall(r'<th class="[^"]*" scope="col">([^<]+)</th>', er)
    assert cabecalhos == list(CABECALHOS_ER)
