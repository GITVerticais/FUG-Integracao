---
title: 'Dirigentes e colegiados: máscara de CPF e testes das cinco tabelas'
type: 'feature'
created: '2026-09-15'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
context: ['{project-root}/_bmad-output/specs/spec-dirigentes-colegiados/SPEC.md']
baseline_commit: '4b5cbe287dbb690ff18c6b71ec547cd8c954c5f6'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `#diretorias` já publica as cinco tabelas e a intro CAP-6, mas a CAP-3 fura: o CPF de Maria Rita Carra Navarro (SP, Vice-Presidente do Conselho Curador) sai como nota interna da planilha. Os testes não travam 5 tabelas, máscara `ddd.XXX.XXX-dd` nem as 27 UFs contíguas.

**Approach:** Sanitizar CPF ocupado fora do formato para `—` (sem marcar a linha vaga), normalizar hífen Unicode, e travar CAP-1 a CAP-6 em teste. Sem redesenhar o painel.

## Decisões acordadas

- **Tabela única por colegiado.** Diretorias Estaduais e Conselho Curador permanecem uma tabela cada, Unidade em cada célula, linhas da mesma UF contíguas. Sem subtítulo, sem `rowgroup`, sem tabela-por-UF.
- **CPF-nota vira `—`.** Maria Rita Carra Navarro continua ocupada (`vago: false`, nome visível); só o CPF publicado é `—`. Qualquer outro CPF ocupado fora de `ddd.XXX.XXX-dd` recebe o mesmo tratamento. O build não aborta.
- **Cinco colegiados da planilha.** Diretorias Estaduais, Diretoria Administrativa, Conselho Curador, Conselho Fiscal, Conselho Editorial. Não omitir Editorial nem criar Conselho de Orçamento.

## Boundaries & Constraints

**Always:**
- `downloads/diretorias-2025.xlsx` é a fonte; `data/diretorias.json` é derivado.
- Nenhum CPF completo no HTML. CPF ocupado: `ddd.XXX.XXX-dd` (hífen ASCII) ou `—` se a origem não trouxe máscara. Traço Unicode (`–`) vira `-` sem mexer em dígitos. Vago: CPF `—` e `data-vago="true"`.
- Máscara não revertida, completada nem cruzada com outra fonte.
- Sem busca/filtro/ordenação/paginação em JS. Nomes como no oficial; só caixa via `nome_proprio`.
- Tabelas no HTML servido, `th scope="col"`, Ctrl+F e leitor de tela. Marcadores `BLOCO:diretorias` preservados; reexecução idempotente.
- Intro CAP-6 fica fora do BLOCO (`h2`/`p` estáticos). Publicado em pt-br.

**Never:**
- Fotos, bios, contato, posse ou exercícios anteriores a 2025.
- Tocar `BLOCO:corpo-funcional`, `BLOCO:estrutura-remuneratoria`, `#organograma`, `assets/js/exportar-xlsx.js` ou as duas tags `<script>` do rodapé.
- Inventar dígitos de CPF ou buscar em outra planilha.
- Inventar coluna, subtítulo ou tabela-por-UF no DOM — a exportação lê a tabela publicada.
- Abortar o build por CPF ocupado fora do formato.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Injeção normal | JSON com 5 colegiados | 5 `<table>` com `h3`, total e colunas Unidade, Cargo, Nome, CPF | N/A |
| Cargo vago | `vago: true` | Nome `Não preenchido`; CPF `—`; `data-vago="true"` | N/A |
| CPF mascarado | `826.XXX.XXX-06` | Célula idêntica | N/A |
| Traço Unicode | `773.XXX.XXX–04` | Publicado `773.XXX.XXX-04` | N/A |
| CPF ocupado fora do formato | nota interna, `vago: false` | CPF `—`; nome permanece; sem `data-vago` | N/A |
| Reexecução | `npm run tabelas` 2× | Bytes inalterados | N/A |
| JSON ausente | falta `diretorias.json` | Nenhuma escrita | Aborta; exit != 0 |

</frozen-after-approval>

## Code Map

- `estrutura-organizacional/index.html` — `#diretorias` L106–1640; intro L107–112 fora do BLOCO; marcadores L113/L1639. Cinco tabelas já no ar (108/9/108/6/7). Nav L58–65 e scripts L2056–2057: não tocar.
- `tools/build_tables.py` — `bloco_diretorias` L84–115; `_celula_nome` L67; `esc` L49; `CARGO_VAGO` L28. Sanitizar CPF ocupado fora do formato na célula. Não alterar os outros `bloco_*`, `SECOES` nem o contrato de marcadores.
- `tools/xlsx_to_json.py` — `diretorias()` L92–120; `min_row=5`; cols 0–3; `vago: not nome`. Hoje CPF é pass-through — passar a normalizar hífen e trocar ocupado fora do formato por `—`. Reusar `limpar`/`nome_proprio`. Não alterar `corpo_funcional()` nem `CORRECOES_*`.
- `data/diretorias.json` — contrato `{ano, colegiados[{id,nome,total,registros[{unidade,cargo,nome,cpf,vago}]}]}`. Regenerar; não editar à mão.
- `downloads/diretorias-2025.xlsx` — origem. Não modificar.
- `tools/test_build_tables.py` — vago L177, escape L162, totais L190. Estender; fixture hoje tem 1 colegiado.
- `package.json` — `dados`/`tabelas`/`build` já encadeiam. Não alterar.

## Tasks & Acceptance

**Execution:**
- [x] `tools/test_build_tables.py` -- cobrir a matriz (5 tabelas, 4 colunas, máscara, vago, traço Unicode, CPF-nota → `—` sem `data-vago`) **antes** de mudar o gerador -- TDD.
- [x] `tools/xlsx_to_json.py` -- normalizar hífen; CPF ocupado fora de `ddd.XXX.XXX-dd` vira `—` sem `vago: true` -- CAP-3 na origem.
- [x] `tools/build_tables.py` -- mesma sanitização na célula CPF; layout das tabelas permanece uma por colegiado -- CAP-3; CAP-5 já satisfeita pela ordem atual.
- [x] `estrutura-organizacional/index.html` -- regenerar só o BLOCO (`npm run dados` + `npm run tabelas`). Intro L107–112 permanece.

**Acceptance Criteria:**
- Dado JS desativado, quando `#diretorias` abre, então há cinco tabelas — Diretorias Estaduais (108), Diretoria Administrativa (9), Conselho Curador (108), Conselho Fiscal (6), Conselho Editorial (7) — com título e total visíveis.
- Dado uma linha, quando se lê o cabeçalho, então Unidade, Cargo, Nome e CPF nesta ordem, com `th scope="col"`.
- Dado o HTML publicado, quando se busca CPF, então cada valor é `ddd.XXX.XXX-dd` ou `—`, e nenhum CPF completo aparece.
- Dado Ceará – Diretor de Formação Política e Pará – Vice-Presidente e Diretor de Formação Política, quando a tabela renderiza, então o cargo está preenchido, o nome é "Não preenchido" e a linha conta no total.
- Dado Maria Rita Carra Navarro, quando a linha renderiza, então o nome permanece, o CPF é `—` e a linha não tem `data-vago`.
- Dado as Diretorias Estaduais, quando o cidadão busca a UF no Ctrl+F, então as 27 unidades são localizáveis e as linhas de cada UF ficam contíguas na mesma tabela.
- Dado o parágrafo L109–112, quando a seção abre, então menciona a FUG e o mascaramento de CPF sob a LGPD.

## Implementation Notes

## Spec Change Log

## Review Triage Log

- **BH1** (blind-hunter) — `low` rejeitado — Approach pede CAP-1 a CAP-6 em teste; a suíte nova trava a matriz (5 tabelas, colunas, máscara, vago, U+2013, nota→`—`). CAP-5 é ordem da planilha transcrita, sem sort no gerador; CAP-6 é intro estática fora do BLOCO. Travar 27 UFs reais exigiria fixture enorme ou ler `index.html`, o que `test_build_tables.py` recusa. Defeito improvável no uso diário; o conserto não é correção direta.
- **BH2** (blind-hunter) — `false` — `test_cinco_colegiados_*` afirma o `total` da fixture; `test_legenda_transcreve_total_da_origem` já prova que 108/6 vêm do JSON. Totais de produção não cabem no `tmp_path`.
- **BH3** (blind-hunter) — `medium` — `xlsx_to_json.diretorias()` passou a sanitizar e nenhum pytest importa o módulo. Restaurar pass-through deixa `test_build_tables.py` verde e regrava a nota da Maria Rita no JSON.
- **BH4** (blind-hunter) — `false` — a spec exige sanitizar nas duas pontas. `limpar` já corre em `diretorias()` L110 antes de `sanitizar_cpf`; máscara com espaço/Cf não chega ao HTML pelo pipeline.
- **BH5** (blind-hunter) — `false` — Always/matriz fixam só U+2013; qualquer outro traço é “ocupado fora do formato” → `—`. Vazio ocupado → `—`; Excel lixo → `—`; o build não ganhou `sys.exit` novo.
- **BH6** (blind-hunter) — `low` — Always pede nenhum CPF completo no HTML. A regex exige `XXX`, então `123.456.789-00` vira `—`, mas nenhum teste trava isso. Um caso na fixture basta.
- **BH7** (blind-hunter) — `false` — `npm run tabelas` responde `sem alteracao`; o diff de 3 células é o produto da regeneração, não edição manual.
- **BH8** (blind-hunter) — `false` / rejeitado (editar spec) — o intent congelado desta história autoriza `—`; o CAP-3 do `SPEC.md` de contexto é o contrato antigo que esta mudança substitui.
- **BH9** (blind-hunter) — rejeitado (editar spec) — Code Map/logs vazios são o artefato de planejamento, não defeito do código publicado.
- **BH10** (blind-hunter) — `false` — `trecho_da_linha(..., antes=5)` incluir vizinho `data-vago` faria o teste falhar, não passar em silêncio. `count == 2` bate com as duas vagas da fixture.
- **EC1** (edge-case-hunter) — `false` — `773.XXX.XXX—04` (U+2014) não é máscara ASCII após trocar só U+2013; publicar `—` é a regra da matriz, não perda de máscara válida.
- **EC2** (edge-case-hunter) — `false` — `limpar` faz strip na origem; JSON derivado não carrega máscara com whitespace.
- **EC3** (edge-case-hunter) — `low` rejeitado — mesma raiz de BH1 (CAP-5/6 fora da matriz operacional). Ver BH1.
- **VG1** (verification-gap) — `medium` — pré-verificado. `sanitizar_cpf` em `xlsx_to_json.py:66-71` e chamada em `:118`; zero `import xlsx_to_json` / `test_xlsx`. HTML continua coberto por `test_build_tables.py`.

**Agrupamento**
- G1 = BH3+VG1 — pytest não executa a sanitização em `diretorias()` — `medium` → **patch**
- G2 = BH6 — falta caso de CPF completo no gerador HTML — `low` → **patch**

## Design Notes

A intro CAP-6 fica fora do BLOCO: o gerador só transcreve tabelas.

CAP-5 fecha com a tabela única já publicada: Unidade em cada célula + linhas da mesma UF contíguas. Não há CSS novo.

Sanitização de CPF ocupado é substituição de formato, não inferência: não completa dígitos, só troca lixo/`–` por `—`/`-`.

## Verification

**Commands:**
- `python -m pytest tools/test_build_tables.py -q` -- expected: todos passam, inclusive a matriz nova.
- `npm run dados` -- expected: JSON regenerado; CPF da Maria Rita = `—`; `773.XXX.XXX-04` com hífen ASCII.
- `npm run tabelas` -- expected: exit 0; 2ª execução `git diff --quiet -- estrutura-organizacional/index.html`.
- `python -m pytest tools/test_render_organograma.py -q` -- expected: regressão verde.

**Manual checks (if no CLI):**
- Ctrl+F pelo presidente do Conselho Curador e pelo presidente da diretoria de um estado, sem JS.
- Célula de Maria Rita Carra Navarro = `—`; nome visível; linha sem destaque de vago.
- 375 px: tabelas rolam na moldura; as quatro abas seguem o `:has()` vigente.
