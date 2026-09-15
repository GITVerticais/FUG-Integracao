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


def planilha_diretorias(caminho, linhas):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Conselho Curador"
    for i, (unidade, cargo, nome, cpf) in enumerate(linhas, start=5):
        ws.cell(i, 1, unidade)
        ws.cell(i, 2, cargo)
        ws.cell(i, 3, nome)
        ws.cell(i, 4, cpf)
    wb.save(caminho)
    return caminho


def test_diretorias_sanitiza_cpf_ocupado_sem_marcar_vago(tmp_path, monkeypatch):
    origem = tmp_path / "downloads"
    origem.mkdir()
    planilha_diretorias(
        origem / "diretorias-2025.xlsx",
        [
            (
                "São Paulo",
                "VICE-PRESIDENTE",
                "Maria Rita Carra Navarro",
                "FUG - Administrativo 2 adm2: não tem o CPF na planilha que tenho acesso",
            ),
            (
                "Rio de Janeiro",
                "VICE-PRESIDENTE",
                "Katia Damiana Alves Pereira Lobo",
                "773.XXX.XXX–04",
            ),
        ],
    )
    monkeypatch.setattr(xlsx_to_json, "ORIGEM", origem)

    registros = xlsx_to_json.diretorias()["colegiados"][0]["registros"]

    rita = next(r for r in registros if r["nome"] == "Maria Rita Carra Navarro")
    assert rita["cpf"] == "—"
    assert rita["vago"] is False

    katia = next(r for r in registros if r["nome"] == "Katia Damiana Alves Pereira Lobo")
    assert katia["cpf"] == "773.XXX.XXX-04"
    assert katia["vago"] is False
