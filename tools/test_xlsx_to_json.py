"""Cobre a sanitizacao de CPF em tools/xlsx_to_json.diretorias().

Cada teste monta uma planilha minima em tmp_path e aponta ORIGEM para la:
nada aqui toca downloads/ ou data/.

Rodar com: python -m pytest tools/test_xlsx_to_json.py -q
"""
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
                    "Rio de Janeiro",
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
            ],
        },
    )

    estaduais = next(
        r
        for r in colegiados["diretorias-estaduais"]
        if r["nome"] == "Maria Rita Carra Navarro"
    )
    curador = next(
        r
        for r in colegiados["conselho-curador"]
        if r["nome"] == "Maria Rita Carra Navarro"
    )

    assert estaduais["cpf"] == MASCARA_RITA
    assert estaduais["vago"] is False
    assert curador["cpf"] == MASCARA_RITA
    assert curador["vago"] is False
