---
title: 'Estrutura remuneratória: 20 cargos transcritos do PDF, com notas e PDF ao lado'
type: 'feature'
created: '2026-09-15'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
context: ['{project-root}/_bmad-output/specs/spec-estrutura-remuneratoria/SPEC.md']
baseline_commit: 'b2288b5a96d2de2b9b60300311ce80673b5dd67e'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `#estrutura-remuneratoria` já lista os 20 cargos do PDF, mas os testes não travam os 20 cargos, a ordem por nível, a faixa máxima do Gerente nem o travessão ≠ zero. CAP-4 não tem notas. O PDF oficial não está ao lado da tabela.

**Approach:** Travar a transcrição coluna a coluna em teste; manter `Adicionais` com `—`; notas só com fatos de 2025 e o significado dos rótulos; `<a download>` do PDF fora do BLOCO. Sem conciliar 35 com 29 e sem remuneração nominal.

## Decisões acordadas

- **20 cargos do PDF**, ordenados por nível decrescente (empate: nome). Colunas do PDF: cargo, nível, vagas previstas (Q.T.), vagas preenchidas (Q.P.), salário base 2025, faixa média, faixa máxima. Não reduzir às três colunas do pedido inicial.
- **Rótulos por extenso.** Q.T. → `Vagas previstas`; Q.P. → `Vagas preenchidas`. Nenhuma sigla sem legenda.
- **`R$ –` do PDF vira travessão**, nunca `R$ 0,00` nem `0`. Vale para Trainee, Estagiário Ensino Médio, Estagiário Superior e Jovem Aprendiz.
- **29 e 35 ficam cada um na sua fonte.** Não conciliar, não recalcular efetivo, não reescrever cargo para casar com o corpo funcional.
- **PDF oficial ao lado**, estático, fora do BLOCO: `../downloads/estrutura-remuneratoria-2025.pdf`. Não inventar botão XLSX.
- **Adicionais (CAP-3):** manter a coluna, `—` em todas as linhas. O PDF não traz a coluna; o travessão marca ausência, não um adicional de outro órgão.
- **Notas (CAP-4):** só o que já é fato. Texto estático no recorte pré-BLOCO: transcrição do PDF oficial de 2025; vagas previstas são as posições do cargo no quadro; vagas preenchidas são as posições ocupadas segundo o mesmo PDF. Sem data de atualização, sem base normativa, sem soma de efetivo e sem cruzar com os 29 do corpo funcional.

## Boundaries & Constraints

**Always:**
- `downloads/estrutura-remuneratoria-2025.pdf` é a fonte; `data/estrutura-remuneratoria.json` é derivado. Contrato: `{ano, total_quadro_preenchido, cargos[{cargo,nivel,quadro_total,quadro_preenchido,salario_base,faixa_media,faixa_maxima,adicionais}]}`. `adicionais` é sempre `—`.
- Valores transcritos: nunca recalculados, arredondados, convertidos ou reformatados de modo a alterar o número.
- Intro CAP-5 (L1801–1803) permanece fora do BLOCO. Notas e download entram no mesmo padrão do XLSX do corpo funcional: depois do intro, antes de `BLOCO:estrutura-remuneratoria`.
- Marcadores `BLOCO:estrutura-remuneratoria` preservados; reexecução idempotente. Publicado em pt-br.

**Never:**
- Remuneração nominal individual, em qualquer forma.
- Editar `downloads/estrutura-remuneratoria-2025.pdf`.
- Tocar `BLOCO:diretorias`, `BLOCO:corpo-funcional`, `#organograma`, ordem das abas, `xlsx_to_json.py` ou os downloads XLSX já testados.
- Converter ausência de faixa em zero; preencher Adicionais com texto de outro órgão (`AUX-CRECHE` etc.).
- Publicar data de atualização, base normativa, soma de Q.P. ou qualquer menção aos 29 do corpo funcional nesta seção.
- Resolver silenciosamente 29 vs 35.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Injeção normal | JSON com 20 cargos oficiais | Uma `<table>`, 20 `<tr>` de dados, Gerente com faixa máxima `R$ 20.000,00` | N/A |
| Ordem | Níveis 10→1 no JSON já ordenado | Primeira linha Secretário Executivo; última Jovem Aprendiz | N/A |
| Travessão | `faixa_media`/`faixa_maxima` = `—` | Célula `—`; nenhuma célula `R$ 0` / `0,00` nessas faixas | N/A |
| Adicionais | campo ausente no PDF | Coluna `Adicionais` presente; cada célula `—` | N/A |
| Reexecução | `npm run tabelas` 2× | Bytes inalterados | N/A |
| JSON ausente | falta `estrutura-remuneratoria.json` | Nenhuma escrita | Aborta; `npm run dados`; exit != 0 |

</frozen-after-approval>

## Code Map

- `estrutura-organizacional/index.html` — `#estrutura-remuneratoria` L1797–2026; intro L1801–1803 **fora** do BLOCO (L1804/L2025). Sem `<a download>` do PDF (o XLSX das outras seções está no intro; o PDF do organograma é L2056). Acrescentar download + notas no recorte pré-BLOCO. Regenerar só o BLOCO. Nav L58–65 e demais seções: não tocar.
- `tools/build_tables.py` — `bloco_estrutura_remuneratoria` L155–191; `colunas` L157–166 incluem `Adicionais`; células L181–187. Não inventar contagem `N cargos.` (já coberto por `test_legenda_transcreve_total_da_origem`). Não alterar `bloco_diretorias`, `bloco_corpo_funcional`, `SECOES` L195.
- `tools/pdf_to_json.py` — extração L17–22 / L30–59; `valor()` converte `R$ –` em `—` L25–27; `adicionais` hardcoded `"—"` L47; `total_quadro_preenchido` é soma L53 (não publicar esse total como cálculo na página). Ordena `-nivel, cargo` L50. Não alterar `xlsx_to_json.py`.
- `data/estrutura-remuneratoria.json` — 20 cargos, `total_quadro_preenchido: 35`, faixas `—` em Trainee/estagiários/Jovem Aprendiz. Regenerar; não editar à mão.
- `downloads/estrutura-remuneratoria-2025.pdf` — origem. Não modificar.
- `tools/test_build_tables.py` — fixture ER L149–164 (1 cargo Gerente + `adicionais`). Estender para travessão, cabeçalhos e 20 linhas. `DADOS_MODELO` das outras seções permanece.
- `tools/test_pdf_to_json.py` — **a criar**. Travar 20 cargos, Gerente `R$ 20.000,00`, travessão ≠ zero, contra o PDF oficial (ou cópia em `tmp_path`).
- `tools/test_exportacao_xlsx.py` — assertar o href do PDF no recorte pré-BLOCO sem inventar XLSX nesta seção.
- `tools/test_abas.py` — ordem das abas. Não alterar.
- `package.json` — `dados` já chama `pdf_to_json.py`. Não alterar.

## Tasks & Acceptance

**Execution:**
- [x] `tools/test_pdf_to_json.py` -- cobrir 20 cargos, ordem por nível, Gerente faixa máxima `R$ 20.000,00`, travessão ≠ zero e `adicionais` = `—` **antes** de mudar o extrator -- TDD.
- [x] `tools/pdf_to_json.py` -- manter `adicionais: "—"` e a transcrição das faixas; só alterar se o teste vermelho exigir -- CAP-1, CAP-3.
- [x] `tools/test_build_tables.py` -- travar os 8 cabeçalhos (incl. Adicionais), 20 `<tr>` de dados, Gerente, travessão e célula `—` de adicionais **antes** de mudar o gerador -- TDD.
- [x] `tools/build_tables.py` -- manter `bloco_estrutura_remuneratoria` com a coluna Adicionais; só alterar se o teste vermelho exigir -- CAP-1, CAP-2, CAP-3.
- [x] `estrutura-organizacional/index.html` -- `<a download>` do PDF após o intro, antes do BLOCO; notas CAP-4 no mesmo recorte (2025 + rótulos; sem data, base, 29 ou soma); regenerar o BLOCO (`npm run dados` + `npm run tabelas`) -- CAP-4, CAP-5 permanece.
- [x] `tools/test_exportacao_xlsx.py` -- assertar o href do PDF pré-BLOCO, as notas factuais e a ausência de XLSX nesta seção -- CAP-4, success signal.

**Acceptance Criteria:**
- Dado JS desativado, quando `#estrutura-remuneratoria` abre, então há uma tabela com 20 linhas de dados, ordenadas por nível decrescente, colunas Cargo, Nível, Vagas previstas, Vagas preenchidas, Salário base, Faixa média, Faixa máxima e Adicionais, com `th scope="col"`.
- Dado o cargo Gerente, quando se lê a faixa máxima, então o valor publicado é `R$ 20.000,00`, idêntico ao PDF.
- Dado Trainee, Estagiário Ensino Médio, Estagiário Superior ou Jovem Aprendiz, quando a faixa média ou máxima é ausente no PDF, então a célula é `—` e nunca `0` / `R$ 0,00`; Adicionais é `—` em todas as linhas.
- Dado a seção, quando o leitor busca a fonte, então um link visível com `download` aponta para `../downloads/estrutura-remuneratoria-2025.pdf`, as notas citam o PDF de 2025 e o significado de vagas previstas/preenchidas, e o recorte não contém data de atualização, base normativa, `29` nem soma de efetivo.

## Implementation Notes

## Spec Change Log

## Review Triage Log

- BH1 `CARGOS_ER_20` não compara nível/Q.T./Q.P./base/média nas células — **medium**. Confirmado em `tools/test_build_tables.py:621-640`: só nomes, Gerente `[5]`/`[6]` e travessão. Swap de `quadro_total`/`quadro_preenchido` passaria. Patch: zip das 7 `<td>` com a tupla dourada.
- BH2 `test_pdf_to_json.py` não pina os 20 nomes nem os campos restantes — **medium**. Mesma causa: extrator contra o PDF oficial sem lista dourada; Assistente II errado ainda passaria. Patch: travar a sequência e os campos.
- BH3 `total_quadro_preenchido` não é afirmado como 35 — **medium**. Mesma causa: `test_transcreve_20_cargos_do_pdf_oficial` só checa o conjunto de chaves. A soma é checksum de Q.P.; a página não publica o total. Patch: `== 35` no JSON extraído.
- BH4 notas não proíbem `35` / `Q.T.` / `Q.P.` — **medium**. Confirmado em `tools/test_exportacao_xlsx.py:82-103`: há `29`, atualização e base normativa; não há `35` nem as siglas. Design Notes e Never (soma de Q.P., rótulo por extenso). Patch: três asserts no recorte pré-BLOCO.
- BH5 teste do PDF não trava `aria-label` nem “Baixar o PDF oficial” — **low**. O AC pede link visível; o href+`download` já está. O XLSX irmão trava `aria-label`. Patch: o mesmo padrão.
- BH6 Code Map desatualizado e logs vazios — **false**. Recusar: o conserto seria editar esta spec.
- BH7 `test_ordena` usa a lista extraída como esperado — **low**. `niveis == sorted(..., reverse=True)` é independente; a igualdade de nomes é tautológica. Mesma causa de BH2 (sequência não pinada).
- BH8 `gerar` não prova que o recorte CAP-4 sobrevive — **false**. `substituir` só troca o miolo entre marcadores (`tools/build_tables.py:230-241`); as notas estão fora do BLOCO. `test_estrutura_remuneratoria_oferece_pdf_oficial_com_notas` lê o HTML publicado.
- BH9 `_celulas_er` não afirma 7 `<td>`; colunas do Gerente na fixture não travadas — **medium**. A parte das colunas é a mesma de BH1. IndexError com menos células é falha alta do teste, não defeito (ver EC2).
- BH10 teste de 20 linhas não afirma a legenda nem proíbe “20 cargos.” / “35 registros.” — **false**. `bloco_estrutura_remuneratoria` grava a legenda fixa e não interpola `total_quadro_preenchido` nem `len(cargos)`. `test_legenda_transcreve_total_da_origem` já proíbe `1 cargos.`.
- EC1 PDF oficial ausente em `_extrair` — **false**. Fixture versionada em `downloads/`; `FileNotFoundError` é falha alta correta.
- EC2 linha com menos de sete `<td>` — **false**. IndexError falha o teste; o gerador emite sete células por cargo.

## Design Notes

A coluna Adicionais não existe no PDF. Manter `—` é declaração de ausência, não de valor: o extrator grava o campo para o gerador não interpolar vazio. As notas não citam 35 nem 29 — o quantitativo visível é só o das células. A legenda do BLOCO (`Valores transcritos do PDF oficial, sem qualquer cálculo.`) permanece; as notas pré-BLOCO acrescentam o ano e a leitura dos dois rótulos de vagas.

## Verification

**Commands:**
- `python -m pytest tools/test_pdf_to_json.py tools/test_build_tables.py tools/test_exportacao_xlsx.py tools/test_abas.py -q` -- expected: todos passam.
- `npm run dados` && `npm run tabelas` -- expected: JSON e BLOCO regenerados; segunda `tabelas` não altera bytes.

**Manual checks (if no CLI):**
- Abrir `#estrutura-remuneratoria`, conferir 20 linhas, Gerente `R$ 20.000,00`, Adicionais `—`, baixar o PDF e ler as notas (2025 + rótulos; sem 29).
