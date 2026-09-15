---
title: 'Publicar CPF mascarado da Maria Rita e manter ordem das abas'
type: 'bugfix'
created: '2026-09-15'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** No Conselho Curador, São Paulo / Vice-Presidente, Maria Rita Carra Navarro sai com CPF `—` porque a célula da planilha ainda tem nota interna. O CPF mascarado já está na tabela de Diretorias Estaduais: `564.XXX.XXX-34`. A ordem das abas já está correta (Organograma primeiro; Estrutura Remuneratória por último) e precisa permanecer.

**Approach:** Publicar `564.XXX.XXX-34` nas duas linhas ocupadas da Maria Rita, sem marcar vago. Não editar o xlsx. Não alterar sanitização genérica de CPF fora da máscara. Não reordenar abas.

</frozen-after-approval>

## Implementation Notes

- `CORRECOES_CPF` em `tools/xlsx_to_json.py` mapeia o nome publicado `Maria Rita Carra Navarro` → `564.XXX.XXX-34`, só quando `sanitizar_cpf` cair em `—`. A máscara válida em Diretorias Estaduais não é sobrescrita. A nota do Conselho Curador continua na planilha; o xlsx não foi editado.
- `build_tables.sanitizar_cpf` permanece defesa genérica: nota interna no JSON ainda vira `—`.
- Abas já estavam na ordem pedida (Organograma → Dirigentes → Corpo Funcional → Estrutura Remuneratória); nenhum markup de nav foi alterado.
- Regenerado com `npm run dados` + `npm run tabelas`. Ambas as linhas da Maria Rita publicam `564.XXX.XXX-34`.
- Review: o teste do xlsx passou a cobrir as duas abas em CAIXA ALTA (máscara na Estadual, nota no Curador). Sanitização genérica ficou em teste separado.

## Review Triage Log

- Blind Hunter: testes não reproduzem o workbook real (duas abas, CAIXA ALTA, máscara vs nota) — **medium**. Confirmado em `planilha_diretorias` de uma aba só. Patch: `test_diretorias_publica_mascara_conhecida_da_maria_rita`.
- Blind Hunter: regra de não sobrescrever máscara válida sem teste — **medium**. Mesma causa; o caso Estadual com `564.XXX.XXX-34` agora trava isso.
- Blind Hunter: `test_cpf_mascarado_da_maria_rita_sai_identico_na_celula` não exercita o gerador — **low**, rejeitado. `build_tables` só transcreve JSON; o contrato da correção é `xlsx_to_json`.
- Blind Hunter: CI não lê `data/` nem o HTML publicado — **defer**. Arquitetura pré-existente dos testes isolados em `tmp_path`; esta mudança não introduziu o buraco.
- Blind Hunter: spec não nomeia a segunda linha / status in-progress / sem AC de abas — **false**. O intent congelado já pede as duas linhas; oneshot omite AC; status era o da etapa.
- Blind Hunter: nome do teste mistura override e sanitização genérica — **medium**. Patch: sanitização genérica voltou ao teste original; override ganhou teste próprio.
- Blind Hunter: chave pós-`nome_proprio` falha se o nome da planilha desviar — **low**, rejeitado. Os dois nomes oficiais já passam por `nome_proprio`; matching difuso inflaria o contrato.
- Blind Hunter: `total: 108` vs 4 `registros` no fixture de `build_tables` — **false**. O HTML usa o campo `total`; a divergência já existia com 2 registros.

