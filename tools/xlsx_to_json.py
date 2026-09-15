"""Converte as planilhas oficiais da FUG para os JSON normalizados em data/.

Fonte de verdade: os arquivos .xlsx em downloads/. Reexecute este script
sempre que as planilhas forem atualizadas e depois rode tools/build_tables.py.
"""
import json
import pathlib
import re
import unicodedata

import openpyxl

RAIZ = pathlib.Path(__file__).resolve().parent.parent
ORIGEM = RAIZ / "downloads"
DESTINO = RAIZ / "data"
ANO = 2025

# Particulas que permanecem em minusculas dentro de nomes proprios.
PARTICULAS = {"de", "da", "do", "das", "dos", "e", "di", "du", "del", "van", "von", "la"}

# Correcoes de digitacao encontradas nas planilhas de origem, aplicadas na
# normalizacao para que a pagina publicada nao reproduza o erro.
CORRECOES_CARGO = {
    "Servilços Gerais": "Auxiliar de Serviços Gerais",
    "Auxiliar Administrativo Senior": "Auxiliar Administrativo Sênior",
}

CORRECOES_NOME = {
    "Elaíne Santos deJesus": "Elaíne Santos de Jesus",
}

# CPF mascarado conhecido quando a celula da planilha traz nota interna
# em vez da mascara. So se aplica se sanitizar_cpf cair em "—" — mascara
# valida na propria linha nao e sobrescrita.
CORRECOES_CPF = {
    "Maria Rita Carra Navarro": "564.XXX.XXX-34",
}

# Exibido quando a planilha traz o cargo sem titular associado.
CARGO_VAGO = "Não preenchido"

# CPF ocupado publicado: mascara da planilha, com hifen ASCII. Qualquer outro
# valor (nota interna, vazio, lixo) vira o mesmo traco dos cargos vagos.
_MASCARA_CPF = re.compile(r"^\d{3}\.XXX\.XXX-\d{2}$")


def limpar(valor):
    if valor is None:
        return ""
    texto = str(valor)
    # Remove hifen suave e demais caracteres de formatacao invisiveis que vieram
    # de colagem entre editores e quebram a busca no navegador.
    texto = "".join(c for c in texto if unicodedata.category(c) != "Cf")
    return re.sub(r"\s+", " ", texto).strip()


def nome_proprio(texto):
    if not texto or texto != texto.upper() and texto != texto.lower():
        return texto

    def palavra(match):
        p = match.group(0)
        if p.lower() in PARTICULAS:
            return p.lower()
        return p[0].upper() + p[1:].lower()

    convertido = re.sub(r"[^\s\-/()]+", palavra, texto.lower())
    # Siglas de UF entre parenteses voltam para maiusculas: "(rs)" -> "(RS)".
    convertido = re.sub(r"\((\w{2})\)", lambda m: f"({m.group(1).upper()})", convertido)
    return convertido[0].upper() + convertido[1:] if convertido else convertido


def sanitizar_cpf(cpf):
    """Hifen Unicode vira ASCII; ocupado fora de ddd.XXX.XXX-dd vira —."""
    texto = ("" if cpf is None else str(cpf)).replace("\u2013", "-")
    if _MASCARA_CPF.fullmatch(texto):
        return texto
    return "—"


def escrever(nome, conteudo):
    caminho = DESTINO / nome
    caminho.write_text(
        json.dumps(conteudo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"  {caminho.relative_to(RAIZ)}")


def corpo_funcional():
    ws = openpyxl.load_workbook(ORIGEM / "corpo-funcional-2025.xlsx", data_only=True).active
    registros = []
    estado_atual = ""
    for linha in ws.iter_rows(min_row=2, values_only=True):
        estado, nome, cargo = (limpar(c) for c in linha[:3])
        if not nome:
            continue
        estado_atual = estado or estado_atual
        cargo = CORRECOES_CARGO.get(cargo, cargo)
        nome = CORRECOES_NOME.get(nome, nome)
        registros.append(
            {
                "unidade": nome_proprio(estado_atual),
                "nome": nome_proprio(nome),
                "cargo": cargo,
            }
        )
    registros.sort(key=lambda r: r["nome"])
    return {"ano": ANO, "total": len(registros), "registros": registros}


def diretorias():
    wb = openpyxl.load_workbook(ORIGEM / "diretorias-2025.xlsx", data_only=True)
    colegiados = []
    for ws in wb.worksheets:
        registros = []
        for linha in ws.iter_rows(min_row=5, values_only=True):
            unidade, cargo, nome, cpf = (limpar(c) for c in linha[:4])
            if not cargo:
                continue
            nome_pub = nome_proprio(nome) if nome else CARGO_VAGO
            cpf_pub = sanitizar_cpf(cpf) if nome else "—"
            if nome and cpf_pub == "—":
                cpf_pub = sanitizar_cpf(CORRECOES_CPF.get(nome_pub, cpf))
            registros.append(
                {
                    "unidade": unidade,
                    "cargo": cargo,
                    "nome": nome_pub,
                    "cpf": cpf_pub,
                    "vago": not nome,
                }
            )
        if not registros:
            continue
        colegiados.append(
            {
                "id": re.sub(r"[^a-z0-9]+", "-", nome_proprio(ws.title).lower()).strip("-"),
                "nome": nome_proprio(ws.title),
                "total": len(registros),
                "registros": registros,
            }
        )
    return {"ano": ANO, "colegiados": colegiados}


if __name__ == "__main__":
    DESTINO.mkdir(exist_ok=True)
    print("Gerando JSON a partir das planilhas oficiais:")
    escrever("corpo-funcional.json", corpo_funcional())
    escrever("diretorias.json", diretorias())
