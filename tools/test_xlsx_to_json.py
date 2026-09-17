"""Cobre a sanitizacao de CPF em tools/xlsx_to_json.diretorias() e a
normalizacao de tools/xlsx_to_json.corpo_funcional().

Cada teste monta uma planilha minima em tmp_path e aponta ORIGEM para la:
nada aqui toca downloads/ ou data/.

Rodar com: python -m pytest tools/test_xlsx_to_json.py -q
"""
import json
import pathlib
import sys

import openpyxl

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import xlsx_to_json  # noqa: E402

NOTA_INTERNA = "FUG - Administrativo 2 adm2: não tem o CPF na planilha que tenho acesso"
MASCARA_RITA = "564.XXX.XXX-34"


def planilha_diretorias(caminho, abas):
    """abas: dict titulo -> lista de (unidade, cargo, nome, cpf)."""
    wb = openpyxl.Workbook()
    primeira = True
    for titulo, linhas in abas.items():
        ws = wb.active if primeira else wb.create_sheet()
        primeira = False
        ws.title = titulo
        for i, (unidade, cargo, nome, cpf) in enumerate(linhas, start=5):
            ws.cell(i, 1, unidade)
            ws.cell(i, 2, cargo)
            ws.cell(i, 3, nome)
            ws.cell(i, 4, cpf)
    wb.save(caminho)
    return caminho


def _registros_por_colegiado(tmp_path, monkeypatch, abas):
    origem = tmp_path / "downloads"
    origem.mkdir()
    planilha_diretorias(origem / "diretorias-2025.xlsx", abas)
    monkeypatch.setattr(xlsx_to_json, "ORIGEM", origem)
    return {
        c["id"]: c["registros"] for c in xlsx_to_json.diretorias()["colegiados"]
    }


def test_diretorias_sanitiza_cpf_ocupado_sem_marcar_vago(tmp_path, monkeypatch):
    registros = _registros_por_colegiado(
        tmp_path,
        monkeypatch,
        {
            "Conselho Curador": [
                (
                    "Nacional",
                    "VICE-PRESIDENTE",
                    "Katia Damiana Alves Pereira Lobo",
                    "773.XXX.XXX–04",
                ),
                (
                    "Nacional",
                    "SUPLENTE",
                    "Fulano Nota Interna",
                    NOTA_INTERNA,
                ),
            ]
        },
    )["conselho-curador"]

    katia = next(r for r in registros if r["nome"] == "Katia Damiana Alves Pereira Lobo")
    assert katia["cpf"] == "773.XXX.XXX-04"
    assert katia["vago"] is False

    fulano = next(r for r in registros if r["nome"] == "Fulano Nota Interna")
    assert fulano["cpf"] == "—"
    assert fulano["vago"] is False


def test_diretorias_publica_mascara_conhecida_da_maria_rita(tmp_path, monkeypatch):
    colegiados = _registros_por_colegiado(
        tmp_path,
        monkeypatch,
        {
            "DIRETORIAS ESTADUAIS": [
                (
                    "São Paulo",
                    "VICE-PRESIDENTE",
                    "MARIA RITA CARRA NAVARRO",
                    MASCARA_RITA,
                ),
            ],
            "CONSELHO CURADOR": [
                (
                    "São Paulo",
                    "VICE-PRESIDENTE",
                    "MARIA RITA CARRA NAVARRO",
                    NOTA_INTERNA,
                ),
                (
                    "Nacional",
                    "PRESIDENTE",
                    "WELLINGTON MOREIRA FRANCO",
                    "103.XXX.XXX-91",
                ),
            ],
        },
    )

    estaduais = next(
        r
        for r in colegiados["diretorias-estaduais"]
        if r["nome"] == "Maria Rita Carra Navarro"
    )
    nomes_curador = [r["nome"] for r in colegiados["conselho-curador"]]

    assert estaduais["cpf"] == MASCARA_RITA
    assert estaduais["vago"] is False
    assert "Maria Rita Carra Navarro" not in nomes_curador
    assert "Wellington Moreira Franco" in nomes_curador


def test_conselho_curador_mantem_so_unidade_nacional(tmp_path, monkeypatch):
    colegiados = _registros_por_colegiado(
        tmp_path,
        monkeypatch,
        {
            "CONSELHO CURADOR": [
                ("Nacional", "PRESIDENTE", "WELLINGTON MOREIRA FRANCO", "103.XXX.XXX-91"),
                ("nacional", "VICE-PRESIDENTE", "CARLOS ALBERTO CHIODINI", "005.XXX.XXX-42"),
                ("São Paulo", "VICE-PRESIDENTE", "MARIA RITA CARRA NAVARRO", MASCARA_RITA),
                ("Rio de Janeiro", "CONSELHEIRO TITULAR", "ALGUEM ESTADUAL", "111.XXX.XXX-11"),
            ],
            "DIRETORIAS ESTADUAIS": [
                ("São Paulo", "PRESIDENTE", "ALGUEM ESTADUAL", "111.XXX.XXX-11"),
            ],
        },
    )
    curador = colegiados["conselho-curador"]
    assert [r["nome"] for r in curador] == [
        "Wellington Moreira Franco",
        "Carlos Alberto Chiodini",
    ]
    assert all(r["unidade"].casefold() == "nacional" for r in curador)
    assert [r["unidade"] for r in colegiados["diretorias-estaduais"]] == ["São Paulo"]


def test_conselho_curador_oficial_tem_15_nacionais():
    curador = next(
        c for c in xlsx_to_json.diretorias()["colegiados"] if c["id"] == "conselho-curador"
    )
    assert curador["total"] == 15
    assert len(curador["registros"]) == 15
    assert all(r["unidade"].casefold() == "nacional" for r in curador["registros"])
    nomes = [r["nome"] for r in curador["registros"]]
    assert "Wellington Moreira Franco" in nomes
    assert "Maria Rita Carra Navarro" not in nomes



def planilha_corpo_funcional(caminho, linhas):
    """linhas: lista de (estado, nome, cargo). Cabecalho na linha 1; dados a partir da 2."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.cell(1, 1, "ESTADOS")
    ws.cell(1, 2, "FUNCIONÁRIO")
    ws.cell(1, 3, "CARGO")
    for i, (estado, nome, cargo) in enumerate(linhas, start=2):
        ws.cell(i, 1, estado)
        ws.cell(i, 2, nome)
        ws.cell(i, 3, cargo)
    wb.save(caminho)
    return caminho


def _corpo_funcional(tmp_path, monkeypatch, linhas):
    origem = tmp_path / "downloads"
    origem.mkdir()
    planilha_corpo_funcional(origem / "corpo-funcional-2025.xlsx", linhas)
    monkeypatch.setattr(xlsx_to_json, "ORIGEM", origem)
    return xlsx_to_json.corpo_funcional()


def test_corpo_funcional_propaga_estados_vazio(tmp_path, monkeypatch):
    dados = _corpo_funcional(
        tmp_path,
        monkeypatch,
        [
            ("RIO GRANDE DO SUL", "LUIZ FERNANDO RODRIGUES DA ROSA", "Auxiliar"),
            ("", "Sanmartin Ciceri", "Estagiário"),
        ],
    )
    por_nome = {r["nome"]: r for r in dados["registros"]}
    assert por_nome["Sanmartin Ciceri"]["unidade"] == "Rio Grande do Sul"


def test_corpo_funcional_aplica_correcoes_nomeadas(tmp_path, monkeypatch):
    dados = _corpo_funcional(
        tmp_path,
        monkeypatch,
        [
            ("RORAIMA RR", "Elaíne Santos deJesus", "Servilços Gerais"),
            ("", "FABIOLA DOS SANTOS LIMA", "Auxiliar Administrativo Júnior"),
            ("DISTRITO FEDERAL", "ANA SILVA", "Auxiliar Administrativo Senior"),
        ],
    )
    por_nome = {r["nome"]: r for r in dados["registros"]}

    elaine = por_nome["Elaíne Santos de Jesus"]
    assert elaine["cargo"] == "Auxiliar de Serviços Gerais"
    assert elaine["unidade"] == "Roraima"

    fabiola = por_nome["Fabiola dos Santos Lima"]
    assert fabiola["unidade"] == "Roraima"

    assert por_nome["Ana Silva"]["cargo"] == "Auxiliar Administrativo Sênior"

    publicado = json.dumps(dados, ensure_ascii=False)
    assert "Roraima Rr" not in publicado
    assert "Servilços" not in publicado
    assert "deJesus" not in publicado
    assert "Senior" not in publicado


def test_corpo_funcional_ordena_por_nome(tmp_path, monkeypatch):
    dados = _corpo_funcional(
        tmp_path,
        monkeypatch,
        [
            ("ACRE", "ZECA ULTIMO", "Copeiro"),
            ("CEARÁ", "ANA PRIMEIRA", "Motorista"),
        ],
    )
    assert [r["nome"] for r in dados["registros"]] == ["Ana Primeira", "Zeca Ultimo"]


def test_corpo_funcional_nao_traz_cpf_nem_valor_monetario(tmp_path, monkeypatch):
    dados = _corpo_funcional(
        tmp_path,
        monkeypatch,
        [("DISTRITO FEDERAL", "JOÃO DA SILVA", "Copeiro")],
    )
    publicado = json.dumps(dados, ensure_ascii=False)
    assert "cpf" not in publicado.lower()
    assert "R$" not in publicado
    for registro in dados["registros"]:
        assert set(registro) == {"unidade", "nome", "cargo"}


def test_corpo_funcional_transcreve_29_registros_da_planilha_oficial():
    dados = xlsx_to_json.corpo_funcional()
    assert "ano" in dados
    assert dados["total"] == 29
    assert len(dados["registros"]) == 29
    assert dados["total"] == len(dados["registros"])
