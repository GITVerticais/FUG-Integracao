"""Cobre a transcricao de tools/pdf_to_json.py contra o PDF oficial.

Cada teste copia o PDF para tmp_path e aponta ORIGEM/DESTINO para la:
nada aqui toca data/.

Rodar com: python -m pytest tools/test_pdf_to_json.py -q
"""
import json
import pathlib
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import pdf_to_json  # noqa: E402

PDF_OFICIAL = (
    pathlib.Path(__file__).resolve().parent.parent
    / "downloads"
    / "estrutura-remuneratoria-2025.pdf"
)

CARGOS_SEM_FAIXA = (
    "Trainee",
    "Estagiário Ensino Médio",
    "Estagiário Superior",
    "Jovem Aprendiz",
)

CARGOS_OFICIAIS = [
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
NOMES_OFICIAIS = tuple(linha[0] for linha in CARGOS_OFICIAIS)

CAMPOS_CARGO = {
    "cargo",
    "nivel",
    "quadro_total",
    "quadro_preenchido",
    "salario_base",
    "faixa_media",
    "faixa_maxima",
    "adicionais",
}


def _extrair(tmp_path, monkeypatch):
    origem = tmp_path / "estrutura-remuneratoria-2025.pdf"
    shutil.copy(PDF_OFICIAL, origem)
    destino = tmp_path / "estrutura-remuneratoria.json"
    monkeypatch.setattr(pdf_to_json, "ORIGEM", origem)
    monkeypatch.setattr(pdf_to_json, "DESTINO", destino)
    pdf_to_json.main()
    return json.loads(destino.read_text(encoding="utf-8"))


def test_transcreve_20_cargos_do_pdf_oficial(tmp_path, monkeypatch):
    dados = _extrair(tmp_path, monkeypatch)

    assert dados["ano"] == 2025
    assert dados["total_quadro_preenchido"] == 35
    assert set(dados) == {"ano", "total_quadro_preenchido", "cargos"}
    assert len(dados["cargos"]) == 20
    for extraido, esperado in zip(dados["cargos"], CARGOS_OFICIAIS, strict=True):
        cargo, nivel, qt, qp, base, media, maxima = esperado
        assert set(extraido) == CAMPOS_CARGO
        assert extraido == {
            "cargo": cargo,
            "nivel": nivel,
            "quadro_total": qt,
            "quadro_preenchido": qp,
            "salario_base": base,
            "faixa_media": media,
            "faixa_maxima": maxima,
            "adicionais": "—",
        }


def test_ordena_por_nivel_decrescente_empate_por_nome(tmp_path, monkeypatch):
    cargos = _extrair(tmp_path, monkeypatch)["cargos"]
    nomes = [c["cargo"] for c in cargos]

    assert nomes == list(NOMES_OFICIAIS)
    assert nomes[0] == "Secretário Executivo"
    assert nomes[-1] == "Jovem Aprendiz"


def test_gerente_faixa_maxima_identica_ao_pdf(tmp_path, monkeypatch):
    cargos = _extrair(tmp_path, monkeypatch)["cargos"]
    gerente = next(c for c in cargos if c["cargo"] == "Gerente")

    assert gerente["faixa_maxima"] == "R$ 20.000,00"
    assert gerente["nivel"] == 8
    assert gerente["quadro_total"] == 3


def test_travessao_nao_vira_zero(tmp_path, monkeypatch):
    cargos = {c["cargo"]: c for c in _extrair(tmp_path, monkeypatch)["cargos"]}
    zeros = ("0", "R$ 0", "R$ 0,00")

    for nome in CARGOS_SEM_FAIXA:
        cargo = cargos[nome]
        assert cargo["faixa_media"] == "—"
        assert cargo["faixa_maxima"] == "—"

    for cargo in cargos.values():
        assert cargo["faixa_media"] not in zeros
        assert cargo["faixa_maxima"] not in zeros


def test_adicionais_sao_traco_em_todos_os_cargos(tmp_path, monkeypatch):
    cargos = _extrair(tmp_path, monkeypatch)["cargos"]
    assert {c["adicionais"] for c in cargos} == {"—"}
    assert all(c["adicionais"] != "" for c in cargos)
