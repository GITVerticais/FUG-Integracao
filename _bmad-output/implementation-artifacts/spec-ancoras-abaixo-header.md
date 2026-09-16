---
title: 'Âncoras visíveis abaixo do header sticky'
type: 'bugfix'
created: '2026-09-16'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Ao clicar nas âncoras das abas (e nos hashes internos) em Estrutura Organizacional, o header sticky cobre o topo dos títulos. O cidadão não lê o `h2`/`h3` alvo.

**Approach:** Compensar a altura do header no container de scroll (`html`), de modo que qualquer navegação por fragmento deixe o alvo inteiro abaixo do header. Sem JavaScript.

</frozen-after-approval>

## Implementation Notes

- Causa: `header` sticky cobre o alvo. `:target { scroll-margin-top: 6rem }` no alvo não bastava (nav das abas na zona do salto; `scroll-margin` + `scroll-padding` somam).
- Offset: `html { scroll-padding-top: 6rem }` (só o header; home e governança herdavam 8rem a mais). Extra das abas: `.aba-painel { scroll-margin-top: 2rem }` — vale no salto da seção, não nos `h3` internos.
- `governanca/index.html`: saiu `style="scroll-margin-top: 6rem"` dos quatro `article` (passaria a somar com o padding do `html`).
- Testes: `tools/test_abas.py` `test_scroll_das_ancoras_compensa_header_sticky`; `tools/test_governanca_docs.py` `test_artigos_nao_empilham_scroll_margin_no_header`. `npm run css`. pytest dos dois arquivos: 12 passed.

## Review Triage Log

- 8rem no `html` empurra Home/Governança (sem abas) — medium; patch: `6rem` no `html` + `2rem` em `.aba-painel`.
- Nav `flex-wrap` em viewport estreita não cabe em 8rem — low rejeitado; o padding de 6rem já tira o título de baixo do header; sticky na nav seria outro contrato.
- Nav das abas não é sticky — false; o pedido é título visível, não abas pinadas.
- `href` da aba aponta para a `section` com `pt-10`, não o `h2` — false; já era assim; o `pt-10` vira folga abaixo do offset.
- Teste só faz grep no CSS; `if target_bloco` era no-op; Governança não travava a remoção do inline — low; patch: asserts fechados no CSS + `test_artigos_nao_empilham_scroll_margin_no_header`. Clique real no DOM fica fora (este repo não tem runner de layout).
- Specs antigas ainda citam `:target { scroll-margin-top }` — defer; editar specs `done` não é desta mudança.
- `scroll-behavior: smooth` sem `prefers-reduced-motion` — false; a regra já existia no `html`; não entrou neste diff.
- `scroll-padding` não reagendaria o scroll depois do reflow `:has()` — maybe-false; o algoritmo de scroll-into-view usa padding e margin na mesma passagem; só um browser confirma. Se verdadeiro seria medium.
- `6rem`/`2rem` literais em vez de custom property — low rejeitado; o projeto já usa rem solto (`py-4`, `pt-10`).

