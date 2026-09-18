---
title: 'Hotfix: tabela de cargos/salários 2026 e rótulo VACÂNCIA'
type: 'bugfix'
created: '2026-09-18'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
context: []
baseline_commit: '3e5895a40d80f5364a79f61507d4dc7c1a6cf4bd'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `#estrutura-remuneratoria` ainda publica o Anexo III 2025 (PDF, Q.P. zerado nos cargos do print, salários velhos). Em dirigentes, cargo vago sai como `Não preenchido`.

**Approach:** Trocar a origem da remuneratória pelo XLSX do Desktop; republicar os 20 cargos; gravar Q.P. 1 só em Secretário Executivo, Adjunto e Procurador (tabela e XLSX versionado); no colegiado, vago vira `VACÂNCIA`.

## Boundaries & Constraints

**Always:**
- Origem: `c:\Users\murilo verticais\Desktop\Anexo III - Tabela de Cargos e Salários (2).xlsx` copiado para `downloads/estrutura-remuneratoria-2026.xlsx`. Header `Salário Base 2026` → `ano: 2026`.
- Q.P. = 1 só em Secretário Executivo, Secretário Executivo Adjunto e Procurador Jurídico — na tabela publicada e na coluna Q.P. do XLSX em `downloads/`. Os outros zeros da planilha (Gerente, Assistente I, Assistente II, Trainee) permanecem 0. Extrator transcreve o XLSX já corrigido; sem lista hardcoded de override.
- 20 cargos. Ordenar `-nivel`, empate `cargo`. `adicionais` sempre `—`. `R$ –` / `R$ -` → `—`, nunca zero.
- Células numéricas da planilha viram `R$ X.XXX,00` (ex.: `50000` → `R$ 50.000,00`; `R$6.900,00` → `R$ 6.900,00`). Trailing space em `Jovem Aprendiz` some.
- Download da seção: XLSX 2026, texto/aria no padrão das outras seções (`Baixar o XLSX oficial`). Remover o PDF da remuneratória.
- Vago em dirigentes: constante `CARGO_VAGO = "VACÂNCIA"` em `xlsx_to_json.py` e `build_tables.py` (não há colegiado “Diretoria Executiva”; o rótulo vive em Diretorias Estaduais).
- Regenerar com `npm run dados` + `npm run tabelas`. Pipeline idempotente.

**Never:**
- Remuneração nominal individual.
- Tocar `downloads/diretorias-2025.xlsx`, `corpo-funcional-2025.xlsx`, organograma, ordem das abas, CSS.
- Inventar botão SheetJS / gerar XLSX no navegador.
- Recalcular efetivo, conciliar 29 vs quadro, publicar soma de Q.P. na UI.
- Manter `downloads/estrutura-remuneratoria-2025.pdf` como fonte ou link da seção.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Transcrição | XLSX com 20 linhas + tipos mistos | JSON/HTML com 20 cargos; Secretário Executivo faixa máx. `R$ 50.000,00`; Chefe de Gabinete base `R$ 12.511,20`; Estagiário Superior base `R$ 1.500,00`; Copeiro máx. `R$ 5.947,41`; Trainee faixas `—` | N/A |
| Travessão | `R$ –` na planilha | Célula `—`; nenhuma `R$ 0` / `0,00` nessas faixas | N/A |
| Q.P. dos 3 | Secretário Executivo, Adjunto, Procurador | `quadro_preenchido` = 1 no JSON, no HTML e no XLSX versionado | N/A |
| Q.P. demais zeros | Gerente, Assistente I, Assistente II, Trainee | `quadro_preenchido` permanece 0 | N/A |
| Download | Seção remuneratória | `href="../downloads/estrutura-remuneratoria-2026.xlsx"` + `download`; arquivo existe; sem PDF nessa seção | N/A |
| Vago | `nome` vazio na planilha de diretorias | `<em>VACÂNCIA</em>`, `data-vago="true"`, CPF `—`; texto `Não preenchido` some da página | N/A |
| XLSX ausente | falta o arquivo em `downloads/` | Nenhuma escrita em `data/estrutura-remuneratoria.json` | Aborta; `npm run dados`; exit != 0 |

</frozen-after-approval>

## Code Map

- `downloads/estrutura-remuneratoria-2026.xlsx` — copiar o Anexo III; setar Q.P.=1 nas 3 linhas (Secretário, Adjunto, Procurador). Remover `downloads/estrutura-remuneratoria-2025.pdf`.
- `tools/xlsx_to_json.py` — acrescentar extração da remuneratória (cols A–G, `min_row=2`). Reusar `escrever`. Não alterar `diretorias()`/`corpo_funcional()` além de `CARGO_VAGO`.
- `tools/pdf_to_json.py` — retirar do `npm run dados`; apagar ou deixar de referenciar.
- `package.json` — `dados` só via `xlsx_to_json.py`.
- `data/estrutura-remuneratoria.json` — regenerar; não editar à mão.
- `tools/build_tables.py` — `CARGO_VAGO` L28; `_celula_nome` L73–77; `bloco_estrutura_remuneratoria` L182–218 (legenda “PDF oficial” → planilha). `bloco_diretorias` só via a constante.
- `estrutura-organizacional/index.html` — link pré-BLOCO L1258–1264; BLOCO regenerado. Fora dos BLOCOs: só o `<a download>` da remuneratória.
- `tools/test_pdf_to_json.py` → testes da extração XLSX (20 cargos, valores 2026, travessão; Q.P. 1 nos 3, 0 em Gerente/Assistentes/Trainee).
- `tools/test_build_tables.py` — `CARGOS_ER_20` L188–209; `test_registro_vago_exibe_nao_preenchido_e_marca_a_linha` L342–354 (`VACÂNCIA`). Fixture `DADOS_MODELO` pode ficar 2025.
- `tools/test_exportacao_xlsx.py` — `test_estrutura_remuneratoria_oferece_pdf_oficial_sem_notas_de_transcricao` L82–117: href XLSX 2026; tirar `assert "xlsx" not in markup`.

## Tasks & Acceptance

**Execution:**
- [x] `tools/test_xlsx_to_json.py` (ou sucessor do `test_pdf_to_json.py`) -- travar 20 cargos, valores 2026, travessão, Q.P. 1 nos 3 e 0 nos demais zeros **antes** do extrator -- TDD.
- [x] `downloads/estrutura-remuneratoria-2026.xlsx` -- copiar o Anexo III; gravar Q.P.=1 em Secretário, Adjunto e Procurador; apagar o PDF 2025.
- [x] `tools/xlsx_to_json.py` + `package.json` -- extrair remuneratória do XLSX; `CARGO_VAGO = "VACÂNCIA"`; tirar `pdf_to_json.py` do `dados`.
- [x] `tools/test_build_tables.py` -- oráculo 2026 + `VACÂNCIA` **antes** de mudar o gerador -- TDD.
- [x] `tools/build_tables.py` -- constante `VACÂNCIA`; legenda da remuneratória sem “PDF”.
- [x] `estrutura-organizacional/index.html` -- href/aria do XLSX 2026 fora do BLOCO; `npm run dados` + `npm run tabelas`.
- [x] `tools/test_exportacao_xlsx.py` -- href XLSX 2026 + arquivo existe + sem PDF na seção.

**Acceptance Criteria:**
- Given o XLSX 2026 em `downloads/`, when `npm run dados && npm run tabelas`, then a tabela tem 20 cargos 2026, Q.P. 1 em Secretário/Adjunto/Procurador e 0 em Gerente/Assistente I/II/Trainee.
- Given um registro de diretoria sem nome, when a tabela é gerada, then o nome visível é `VACÂNCIA` em maiúsculas e `Não preenchido` não aparece.
- Given a seção `#estrutura-remuneratoria`, when o cidadão baixa o oficial, then o arquivo é `estrutura-remuneratoria-2026.xlsx` (não o PDF 2025) e a coluna Q.P. dos 3 cargos já está em 1.

## Implementation Notes

- Origem 2026 copiada para `downloads/estrutura-remuneratoria-2026.xlsx`; Q.P.=1 só nas 3 linhas de Secretário/Adjunto/Procurador; PDF 2025 removido.
- `xlsx_to_json.estrutura_remuneratoria()` transcreve cols A–G (`min_row=2`), formata número→`R$ X.XXX,00`, `R$ –`/`R$ -`→`—`, ano pelo header `Salário Base 2026`. Sem override hardcoded de Q.P. XLSX ausente aborta `main()` sem escrever o JSON.
- `CARGO_VAGO = "VACÂNCIA"` em extrator e gerador. `pdf_to_json.py` / `test_pdf_to_json.py` apagados; `npm run dados` só chama o XLSX; `pypdf` saiu de `requirements.txt`.
- Página: download `estrutura-remuneratoria-2026.xlsx` no padrão das outras seções; BLOCO regenerado com 20 cargos 2026 e legenda da planilha. Pipeline `npm run dados` + `npm run tabelas` idempotente.

## Spec Change Log

## Review Triage Log

- BH1 logs vazios — **false**. Primeira passagem de review; o processo é que preenche estes logs. Corrigir agora seria editar o spec desta build.
- BH2 specs parentes ainda citam PDF 2025 — **low**. Artefato de stories `done`; a página já aponta o XLSX 2026. Não é regressão deste hotfix.
- BH3 specs parentes ainda definem `Não preenchido` — **low**. Idem: rótulo publicado já é `VACÂNCIA`; os specs fechados não são lidos pelo build.
- BH4 origem no Desktop — **false**. A cópia durável está em `downloads/estrutura-remuneratoria-2026.xlsx`; o caminho Desktop foi a origem única da cópia.
- BH5 “oficial” com Q.P. editado — **false**. Decisão 2B: o XLSX versionado com Q.P. 1 nos 3 cargos é o arquivo oficial publicado.
- BH6 ano 2026 ausente no copy da tabela — **false**. `ano` vai para o JSON; a UI já não exibia o exercício depois da remoção das notas CAP-4. O spec não pede o ano no cabeçalho visível.
- BH7 `R$ —` (em dash) — **false**. A planilha usa U+2013; `valor_monetario` casa `R\$\s*[–\-]` e os testes de travessão passaram.
- BH8 planilha sem cargos — **false**. O XLSX versionado tem 20 linhas com cargo; folha vazia não foi apresentada ao programa.
- BH9 JSON obsoleto se o XLSX faltar — **false**. A matriz pede abortar sem escrever `estrutura-remuneratoria.json`, não apagar o derivado anterior.
- BH10 exportacao não trava Q.P. 0 no XLSX — **false**. `test_estrutura_remuneratoria_transcreve_20_cargos_do_xlsx_oficial` já afirma Gerente/Assistente I/II/Trainee = 0 contra o arquivo oficial.
- BH11 Code Map com nomes velhos de teste — **false**. Correção seria editar o spec desta build.
- BH12 fixture `nome: "Não preenchido"` — **false**. Com `vago: true`, `_celula_nome` publica `CARGO_VAGO`, não o campo `nome`.
- BH13 docstring do extrator — **false**. O módulo já declara `downloads/*.xlsx` como fonte; a remuneratória passou a ser um desses arquivos.
- BH14 `deferred-work.md` cita `pdf_to_json.py` — **low**. Entradas de stories anteriores; o arquivo foi apagado neste hotfix, mas o deferred não é contrato de execução.
- BH15 filename 2026 vs `ano` parseado — **false**. Spec fixa o nome `estrutura-remuneratoria-2026.xlsx`; o header da planilha é `Salário Base 2026`.
- BH16 matriz sem folha vazia — **false**. Completar a matriz seria editar o spec desta build; o arquivo real não é vazio.
- EC1 Q.T./Q.P./nível não numérico — **false**. Todas as 20 linhas oficiais são numéricas; `int()` não é alcançado com lixo.
- EC2 salário só com espaço — **false**. Nenhuma célula monetária da planilha é whitespace-only.
- EC3 em dash / minus unicode — **false**. Travessões da origem são U+2013, cobertos pelo regex atual.
- EC4 salário dígitos em string — **false**. A origem traz `float` ou texto `R$ …`, não dígitos crus.
- EC5 XLSX corrompido — **false**. A matriz cobre ausência do arquivo; zip inválido não foi apresentado.
- EC6 aba só com cabeçalho — **false**. A origem tem 20 cargos; `if not cargo: continue` só descarta linhas vazias abaixo.
- EC7 regex do PDF não pula linha malformada — **false**. O extrator XLSX ignora linha sem cargo; headers/notas sem nome não viram cargo.
- VG1 BLOCO remuneratória publicado sem assert — **medium**. `test_exportacao_xlsx.py` corta o markup no INICIO do BLOCO e não lê as `<td>`; restaurar Q.P. 0 / `R$ 45.000,00` no HTML deixa pytest verde.
- VG2 VACÂNCIA publicada sem assert — **medium**. Só fixtures isoladas cobrem o rótulo; `Não preenchido` de volta nas três `<em>` da página real não quebra a suíte.
