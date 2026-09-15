"""Extrai a tabela da estrutura remuneratoria do PDF oficial para data/.

As colunas Q.T. e Q.P. sao transcritas exatamente como constam no PDF de
origem (downloads/estrutura-remuneratoria-2025.pdf); nenhum valor e calculado.
"""
import json
import pathlib
import re

from pypdf import PdfReader

RAIZ = pathlib.Path(__file__).resolve().parent.parent
ORIGEM = RAIZ / "downloads" / "estrutura-remuneratoria-2025.pdf"
DESTINO = RAIZ / "data" / "estrutura-remuneratoria.json"
ANO = 2025

LINHA = re.compile(
    r"^(\d+)\s+(\d+)\s+(.+?)\s+(\d+)\s+"
    r"(R\$\s*[\d.,]+|R\$\s*–|R\$\s*-)\s+"
    r"(R\$\s*[\d.,]+|R\$\s*–|R\$\s*-)\s+"
    r"(R\$\s*[\d.,]+|R\$\s*–|R\$\s*-)$"
)


def valor(texto):
    texto = re.sub(r"\s+", " ", texto).strip()
    return "—" if re.fullmatch(r"R\$ ?[–-]", texto) else texto.replace("R$", "R$ ").replace("  ", " ")


def main():
    bruto = PdfReader(ORIGEM).pages[0].extract_text()
    cargos = []
    for linha in bruto.splitlines():
        m = LINHA.match(linha.strip())
        if not m:
            continue
        qt, qp, cargo, nivel, base, media, maxima = m.groups()
        cargos.append(
            {
                "cargo": cargo.strip(),
                "nivel": int(nivel),
                "quadro_total": int(qt),
                "quadro_preenchido": int(qp),
                "salario_base": valor(base),
                "faixa_media": valor(media),
                "faixa_maxima": valor(maxima),
                "adicionais": "—",
            }
        )
    cargos.sort(key=lambda c: (-c["nivel"], c["cargo"]))
    saida = {
        "ano": ANO,
        "total_quadro_preenchido": sum(c["quadro_preenchido"] for c in cargos),
        "cargos": cargos,
    }
    DESTINO.write_text(
        json.dumps(saida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    caminho = DESTINO
    try:
        caminho = DESTINO.relative_to(RAIZ)
    except ValueError:
        pass
    print(f"  {caminho} — {len(cargos)} cargos")


if __name__ == "__main__":
    main()
