---
title: 'Corpo funcional: 29 empregados, colunas Nome/Cargo/Unidade, sem remuneração individual'
type: 'feature'
created: '2026-09-15'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
context: ['{project-root}/_bmad-output/specs/spec-corpo-funcional/SPEC.md']
baseline_commit: '838311f2763bc92f397a03990356f708d4d2b028'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `#corpo-funcional` já lista 29 empregados, mas CAP-1 fura: colunas saem Unidade, Nome, Cargo — o contrato pede Nome, Cargo, Unidade. CAP-2 fura: não há link para a seção de estrutura remuneratória. Os testes não travam os 29 registros, a ordem por nome, o mapa de correções, o fill-down de ESTADOS nem a ausência de dinheiro e CPF.

**Approach:** Reordenar as colunas no gerador, acrescentar um link de seção para `#estrutura-remuneratoria` no HTML estático (fora do BLOCO) e travar CAP-1 a CAP-4 em teste. Sem redesenhar o painel e sem reconciliar os 29 com os 35 da remuneratória.

## Decisões acordadas

- **Colunas Nome, Cargo, Unidade** nesta ordem, `th scope="col"`, linhas ordenadas por nome. A unidade vem da coluna ESTADOS com fill-down.
- **Um link de seção**, não por linha. Cargos permanecem texto. A âncora é `#estrutura-remuneratoria`. Matching cargo-a-cargo com a tabela de faixas fica de fora: os nomes da planilha (Supervisor Financeiro, Estagiário, etc.) não são reescritos.
- **Quatro correções no conversor**, uma entrada por erro: `Servilços Gerais` → `Auxiliar de Serviços Gerais`; `Auxiliar Administrativo Senior` → `Auxiliar Administrativo Sênior`; `Elaíne Santos deJesus` → `Elaíne Santos de Jesus`; `RORAIMA RR` → `Roraima` (mapa de unidade; o xlsx não é editado).
- **29 registros transcritos da planilha.** Não inventar pessoas, não omitir a seção, não cruzar efetivo com o PDF de remuneração.

## Boundaries & Constraints

**Always:**
- `downloads/corpo-funcional-2025.xlsx` é a fonte; `data/corpo-funcional.json` é derivado. Contrato: `{ano, total, registros[{unidade,nome,cargo}]}`.
- Fill-down: célula ESTADOS vazia herda o último estado informado. Conferido contra a planilha (ex.: Sanmartin Ciceri herda Rio Grande do Sul).
- Nenhuma coluna, nota, atributo ou arquivo gerado contém valor monetário ou CPF. O XLSX oficial em `downloads/` permanece o original, com os erros de origem.
- Intro CAP-3 (parágrafo estático L1617–1619) permanece; o link CAP-2 entra depois dele e **antes** de `BLOCO:corpo-funcional`, no mesmo padrão do `<a download>` do XLSX.
- Marcadores `BLOCO:corpo-funcional` preservados; reexecução idempotente. Publicado em pt-br.

**Never:**
- CPF, admissão, matrícula, lotação por gerência ou remuneração nominal individual.
- Editar `downloads/corpo-funcional-2025.xlsx`.
- Tocar `BLOCO:diretorias`, `BLOCO:estrutura-remuneratoria`, `#organograma`, ordem das abas, `pdf_to_json.py`, `render_organograma.py` ou o download XLSX já testado.
- Reescrever cargo para casar com a tabela de faixas (Supervisor/Coordenador genéricos, Estagiário médio/superior).
- Resolver silenciosamente 29 vs 35.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Injeção normal | JSON com 29 registros | Uma `<table>`, 29 `<tr>` de dados, colunas Nome, Cargo, Unidade, ordenadas por nome | N/A |
| Fill-down ESTADOS | Linha com estado vazio após um estado preenchido | `unidade` do último estado informado | N/A |
| Correção de cargo | `Servilços Gerais` / `Auxiliar Administrativo Senior` | `Auxiliar de Serviços Gerais` / `Auxiliar Administrativo Sênior` | N/A |
| Correção de nome | `Elaíne Santos deJesus` | `Elaíne Santos de Jesus` | N/A |
| Correção de unidade | `RORAIMA RR` | `Roraima` (não `Roraima Rr`) | N/A |
| Sem dinheiro/CPF | JSON só com unidade/nome/cargo | Bloco sem `R$`, sem CPF, sem coluna extra | N/A |
| Reexecução | `npm run tabelas` 2× | Bytes inalterados | N/A |
| JSON ausente | falta `corpo-funcional.json` | Nenhuma escrita | Aborta; `npm run dados`; exit != 0 |

</frozen-after-approval>

## Code Map

- `estrutura-organizacional/index.html` — `#corpo-funcional` L1614–1790; intro L1617–1619 e XLSX L1620–1626 **fora** do BLOCO (L1628/L1789). Acrescentar o link CAP-2 entre intro e BLOCO. Regenerar só o BLOCO. Nav L58–65 e demais seções: não tocar.
- `tools/build_tables.py` — `bloco_corpo_funcional` L130–152; `colunas` L132 hoje `Unidade, Nome, Cargo`. Reordenar para `Nome, Cargo, Unidade`; atualizar caption L138–139 e as três `<td>`. Não alterar `bloco_diretorias`, `bloco_estrutura_remuneratoria`, `SECOES` L197, `_celula_nome` L71.
- `tools/xlsx_to_json.py` — `corpo_funcional()` L89–108; fill-down L97; `CORRECOES_CARGO` L23–26 e `CORRECOES_NOME` L28–30 aplicadas L98–99; sort L107. Acrescentar mapa nomeado de unidade (`RORAIMA RR` → `Roraima`) e aplicar no fill-down, antes de `nome_proprio`. Reusar `limpar`/`nome_proprio`. Não alterar `diretorias()`, `CORRECOES_CPF`, `sanitizar_cpf`.
- `data/corpo-funcional.json` — 29 registros, já ordenados e com as 3 correções. Regenerar; não editar à mão.
- `downloads/corpo-funcional-2025.xlsx` — origem (`ESTADOS`/`FUNCIONÁRIO`/`CARGO`, `min_row=2`). Não modificar.
- `tools/test_xlsx_to_json.py` — só cobre `diretorias()`. Estender com fixture de corpo funcional em `tmp_path` (mesmo padrão L21–45).
- `tools/test_build_tables.py` — fixture CF L142–147 (1 registro, 3 campos). Estender para ordem das colunas e ausência de `R$`/CPF no bloco. `DADOS_MODELO` das outras seções permanece.
- `tools/test_exportacao_xlsx.py` — href do XLSX antes do BLOCO L17–20. O novo `<a href="#estrutura-remuneratoria">` não pode quebrar esse teste; se preciso, assertar o link CAP-2 no mesmo recorte pré-BLOCO.
- `tools/test_abas.py` — ordem das abas. Não alterar.
- `package.json` — `dados`/`tabelas`/`build` já encadeiam. Não alterar.

## Tasks & Acceptance

**Execution:**
- [x] `tools/test_xlsx_to_json.py` -- cobrir fill-down, as 4 correções (incl. `RORAIMA RR` → `Roraima`), ordenação por nome e ausência de CPF/campo monetário no JSON **antes** de mudar o conversor -- TDD.
- [x] `tools/xlsx_to_json.py` -- mapa nomeado de unidade `RORAIMA RR` → `Roraima`; `corpo_funcional()` continua a única função tocada -- CAP-4.
- [x] `tools/test_build_tables.py` -- travar cabeçalho Nome, Cargo, Unidade e bloco sem `R$`/CPF **antes** de reordenar o gerador -- TDD.
- [x] `tools/build_tables.py` -- reordenar colunas e caption de `bloco_corpo_funcional` -- CAP-1.
- [x] `estrutura-organizacional/index.html` -- link estático `href="#estrutura-remuneratoria"` após o intro, antes do BLOCO; regenerar o BLOCO (`npm run dados` + `npm run tabelas`) -- CAP-2; CAP-3 permanece.
- [x] `tools/test_exportacao_xlsx.py` -- assertar o href da remuneratória no recorte pré-BLOCO sem soltar o download do XLSX -- CAP-2.

**Acceptance Criteria:**
- Dado JS desativado, quando `#corpo-funcional` abre, então há uma tabela com 29 linhas de dados, legendada com o total, colunas Nome, Cargo e Unidade nesta ordem, com `th scope="col"`.
- Dado a tabela publicada, quando se lê de cima a baixo, então os nomes estão em ordem alfabética e cada unidade corresponde ao bloco ESTADOS da planilha (incluindo fill-down).
- Dado a seção `#corpo-funcional`, quando o leitor busca faixa salarial, então um link visível aponta para `#estrutura-remuneratoria` e nenhuma célula, nota ou atributo da tabela contém valor monetário ou CPF.
- Dado as quatro grafias erradas da planilha (`Servilços Gerais`, `Senior` sem acento, `deJesus`, `RORAIMA RR`), quando o conversor roda, então a página publica as formas do mapa nomeado — inclusive `Roraima`, nunca `Roraima Rr` — sem editar o xlsx.

## Implementation Notes

## Spec Change Log

## Review Triage Log

| Camada | Achado | Verdict | Evidence |
|--------|--------|---------|----------|
| blind-hunter | Code Map fala em 3 correções vs 4 do CAP-4 | false | `Code Map` descreve o JSON pré-mudança (“já ordenados e com as 3 correções. Regenerar”); a 4ª entrada é `CORRECOES_UNIDADE`. Correção seria editar o spec. |
| blind-hunter | Implementation Notes / Change Log / Triage Log vazios em `in-review` | false | Seções preenchidas neste passo e no step-05; vazio no início do review é o fluxo. |
| blind-hunter | Página commitada não afirma 29 linhas / ordem / `Roraima` | medium | Mesma causa de verification-gap: fixtures em `tmp_path` não observam a transcrição oficial. |
| blind-hunter | Contrato JSON `{ano,total,registros}` não travado | low | Mesma causa: `corpo_funcional()` de teste nunca roda contra `downloads/`. |
| blind-hunter | `npm run tabelas` 2× não automatizado | false | `test_reexecucao_nao_altera_bytes` cobre `gerar()` duas vezes; `npm run tabelas` é esse script. Segunda execução: `sem alteracao`. |
| blind-hunter | Teste CAP-2 não trava texto, ordem, `id`, nem “sem link por linha” | false | Recorte pré-BLOCO já exclui a tabela; `href="#estrutura-remuneratoria"` está lá. `id="estrutura-remuneratoria"` pré-existia. Células do BLOCO são texto (`td` sem `<a>`). Ícone/`aria-label` são do download, não do link de seção. |
| blind-hunter | Fill-down só 1 vazio; sem ESTADOS inicial vazio | false | Planilha oficial: linha 2 já traz ACRE; não há ESTADOS vazio na primeira linha de dados. |
| blind-hunter | `CORRECOES_UNIDADE` só casa `RORAIMA RR` exato | false | Intent congela uma entrada por erro com essa grafia; o xlsx oficial traz exatamente `RORAIMA RR`. |
| blind-hunter | Fixture sem dinheiro/CPF não pega coluna extra | false | `test_corpo_funcional_colunas_nome_cargo_unidade` exige exatamente 3 `th` Nome/Cargo/Unidade; o gerador só interpola esses três campos. |
| blind-hunter | Sort só ASCII, sem pt-BR | false | Code Map aponta `sort(key=lambda r: r["nome"])` pós-`nome_proprio`; a página segue esse algoritmo. |
| blind-hunter | 29 vs 35 sem teste | false | Nenhum caminho cruza `corpo-funcional` com a remuneratória; a proibição é não reconciliar, não afirmar a diferença. |
| blind-hunter | Link sem `aria-label`/ícone; manual sem `:target` | false | Padrão do XLSX no Always é o `a.inline-flex` de seção, não o `download`. Texto visível basta. |
| blind-hunter | Linha sem FUNCIONÁRIO é descartada sem teste | false | XLSX oficial: `empty_nome == []` (29 nomes nas linhas 2–30). O `continue` não dispara nesta origem. |
| edge-case-hunter | ESTADOS em linha sem FUNCIONÁRIO não atualiza `estado_atual` (`xlsx_to_json.py:99-102`) | false | Mesma evidência: a planilha não tem FUNCIONÁRIO vazio. Situação inalcançável nesta origem. |
| edge-case-hunter | `Maria Elizabete` precede `Maria dos Remédios` após partículas minúsculas (`xlsx_to_json.py:112`) | false | Ordem publicada casa o sort já documentado no Code Map; locale pt-BR não foi contratado. |
| verification-gap | Teste de 29 linhas usa `Pessoa 00…` sintético; omitir um empregado oficial não quebra teste | medium | `test_corpo_funcional_injeta_29_linhas_*` e os fixtures de `xlsx_to_json` monkeypatcham `ORIGEM`/`tmp_path`. `test_exportacao_xlsx` lê a página real mas só o href pré-BLOCO. `corpo_funcional()` deriva `total` da planilha; a página commitada tem `29 registros.` em L1633. Disposition da camada: patch. |

## Design Notes

O link CAP-2 é de seção, não de célula: a planilha usa cargos que a tabela de faixas agrega (`Supervisor Financeiro` vs `Supervisor`; `Estagiário` sem nível). Um `<a>` por cargo fingiria correspondência 1:1. O fill-down é o mesmo da origem: 15 linhas de DF com ESTADOS vazio após `Distrito Federal`; `Sanmartin Ciceri` / `Estagiário` herda `RIO GRANDE DO SUL`.

## Verification

**Commands:**
- `python -m pytest tools/test_xlsx_to_json.py tools/test_build_tables.py tools/test_exportacao_xlsx.py tools/test_abas.py -q` -- expected: todos passam.
- `npm run dados` && `npm run tabelas` -- expected: JSON e BLOCO regenerados; segunda `tabelas` não altera bytes.

**Manual checks (if no CLI):**
- Abrir `#corpo-funcional`, conferir 29 linhas e a ordem Nome/Cargo/Unidade, clicar o link e cair em `#estrutura-remuneratoria`.
