---
title: 'Conselho Curador: só os 15 nomes Nacionais'
type: 'bugfix'
created: '2026-09-17'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** A tabela Conselho Curador em `#diretorias` publica 108 linhas. Só as 15 com Unidade `Nacional` são do colegiado; as 93 com UF foram adicionadas por engano.

**Approach:** No conversor, na aba Conselho Curador, manter só linhas cuja primeira coluna é Nacional. Recalcular `total` (15). Regenerar JSON e HTML. Planilha e demais colegiados intactos.

</frozen-after-approval>

## Implementation Notes

- Filtro só em `xlsx_to_json.diretorias()`, após montar `id_colegiado`: `conselho-curador` guarda `unidade.casefold() == "nacional"`. `total` = `len(registros)`. Planilha e o gerador `build_tables.py` intactos.
- `test_build_tables.py` só mudou `total`/legenda 108→15; as linhas da fixture do Curador continuam mistas de propósito — o gerador transcreve o JSON, o filtro vive no conversor.
- Fixture de CPF da Katia no conversor passou de RJ para Nacional; Maria Rita deixa de sair no Curador e permanece nas Diretorias Estaduais.
- Regenerados `data/diretorias.json` e o BLOCO de `estrutura-organizacional/index.html` (15 linhas, legenda `15 registros.`).
- Comentário no filtro explica o recorte (linhas de UF coladas na aba).

## Review Triage Log

- Spec sem lista dos 15 nomes / GWT / status in-progress — false. Oneshot não leva essas seções; nomes estão no JSON/HTML; status vai a done aqui.
- Sem aviso de que o XLSX oficial ainda tem 93 UF — medium. HTML agora diverge da planilha. Defer: aviso seria copy editorial; xlsx não se edita.
- Caption `unidade de representação` — false. A coluna Unidade permanece; valor `Nacional`.
- Intro “por unidade de representação” — false. Continua verdadeiro para a seção (estaduais).
- Specs done ainda dizem Curador 108 — low. Defer: contratos históricos fora do escopo.
- Fixture `test_build_tables` ainda tem UF no Curador — false. Gerador transcreve JSON; ausência de Maria Rita no Curador está em `test_xlsx_to_json`.
- Teste oficial não trava os 15 nomes nem o HTML — low rejeitado. Pedido é o filtro Nacional; skip de xlsx ausente também não existe no teste dos 29 do corpo funcional.
- Falta comentário why no filtro — low. Patch: uma linha no conversor.
- Implementation Notes diziam `build_tables` intacto após editar o teste — low. Patch: notas distinguem gerador vs fixture.
- Filtro vazio some com a tabela — false. `if not registros: continue` já existia; a planilha atual tem 15 Nacionais.
- Comentário de `CORRECOES_CPF` fala do Curador — false. O comentário não cita o colegiado.
- Sem frase “estes são os nacionais” — false. Cada linha já publica Unidade `Nacional`.
