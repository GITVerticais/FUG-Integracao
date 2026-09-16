---
title: 'Voltar ao índice só no final de cada tabela'
type: 'feature'
created: '2026-09-16'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Em Dirigentes e Órgãos Colegiados, o link "Voltar ao índice" aparece ao lado do título de cada colegiado (incluindo Diretorias Estaduais) e de novo no fim da tabela. O link do cabeçalho compete com o índice e com o título; o do rodapé fica colado na tabela.

**Approach:** Manter um único "Voltar ao índice" depois de cada tabela, com um pouco mais de espaço em relação à moldura. Remover o link do cabeçalho em todos os colegiados. O índice no topo permanece.

</frozen-after-approval>

## Implementation Notes

- Gerador: `tools/build_tables.py` `bloco_diretorias`. `_link_voltar_indice()` (L98–102) continua; tirar a chamada no flex do `h3` (L126–129). Depois da tabela, hoje `<p class="mt-3">` (L153); passar para `mt-8` (a moldura já usa `mt-6`; `mt-8` afasta o link sem CSS novo).
- Com o link do cabeçalho fora, o wrapper `flex ... justify-between` só envolve o `h3` — emitir o `h3` direto, sem o `div`.
- HTML publicado: só `BLOCO:diretorias` via `npm run tabelas`. Não editar `estrutura-organizacional/index.html` à mão.
- Testes em `tools/test_build_tables.py`: `test_indice_com_um_colegiado` espera 2 links → 1. `test_voltar_ao_indice_em_cada_colegiado` espera 10 links, 1 antes e 1 depois da tabela → 5 links, 0 antes, 1 depois, texto no `depois`. TDD: atualizar testes antes do gerador.
- Fora: outros BLOCOs, `SECOES`, CSS/JS, XLSX, `<nav id="indice-colegiados">`, abas.
- 2026-09-16: `_link_voltar_indice` só depois da tabela (`mt-8`). `h3` direto, sem flex. Nav ganhou `id="indice-colegiados"` e `tabindex="-1"` para o hash receber foco. `npm run tabelas` regenerou o BLOCO: 5 links, nenhum no cabeçalho. pytest `tools/test_build_tables.py -q`: 25 passed. `.mt-8` já existia no wrapper do BLOCO e no `main.css`; CSS não regenerado.

## Review Triage Log

- Nav do índice sem `tabindex="-1"` — medium; foco de teclado ficava no link que saiu da viewport. Patch: `tabindex="-1"` no `<nav>`.
- Cinco links com o mesmo nome acessível — low rejeitado; WCAG 2.4.4 aceita propósito pelo contexto da `<section aria-labelledby>`.
- Teste partia em `<table` e não em `</table>` — low; patch simples no recorte e na fixture de um colegiado.
- `mt-8` solto em vez de `CLS_*` — low rejeitado; uma ocorrência, outras classes do bloco também são literais.
- Índice sem heading visível nem highlight `:target` — false; os cinco nomes do `<nav>` já são o índice; highlight não foi pedido.
- `mt-8` + `space-y-12` e folga após o último colegiado — low rejeitado; o afastamento foi o pedido.
- Helpers no meio dos testes — low rejeitado; rearranjo sem efeito no comportamento.
- Testes não leem o `index.html` publicado — false; o gerador é coberto por fixture; a spec anterior do índice pede para não ler o HTML real.
