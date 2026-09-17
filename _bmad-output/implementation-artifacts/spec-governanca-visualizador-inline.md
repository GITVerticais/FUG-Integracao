---
title: 'Visualizador de governança dentro da box do documento clicado'
type: 'feature'
created: '2026-09-16'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** O visualizador PDF fica abaixo dos quatro cartões. Quem clica Visualizar precisa descer até um iframe solto, desligado da box do documento.

**Approach:** Tirar o iframe de baixo da lista. O mesmo visualizador nativo passa a aparecer dentro da box do documento clicado, abaixo dos links Visualizar/Baixar daquele item. Até o primeiro clique, nenhuma área de leitura aparece. Clicar outro documento move o visualizador para a box daquele item.

</frozen-after-approval>

## Implementation Notes

- Um iframe nativo (`name=visualizador-governanca`) começa com `hidden`, fora da lista.
- Cada `article` tem `[data-visualizador-host]` abaixo dos links Visualizar/Baixar.
- No clique primário sem modificador: `preventDefault`, `appendChild` no host, `hidden = false`, `title` a partir do `h2`, `viewer.src = href`, `article.scrollIntoView` (scroll-margin 6rem no article, abaixo do header sticky).
- Ctrl/Cmd/Shift/Alt e botão não primário não movem o iframe.
- Arquivos: `governanca/index.html`, `tools/test_governanca_docs.py`. Home e PDFs intocados.
- `python -m pytest tools/test_governanca_docs.py tools/test_home_governanca.py -q` — 8 passed.

## Review Triage Log

- Sem JS o iframe fica `hidden` — **low** rejeitado: o intent exige mover para a box; Baixar continua disponível; noscript recolocaria o viewer abaixo da lista.
- `scrollIntoView` no iframe esconde o `h2` sob o header — **medium** patched: rola o `article`.
- Testes só grepam o script — **low** rejeitado: o restante da suíte é HTML estático; greps mais longos não provam o clique.
- `title` genérico / sem `aria-expanded` — **low** patched em parte (`title` atualiza com o h2); `aria-expanded` seria API nova.
- `appendChild` recarrega o iframe — **medium** patched: `src` definido depois da mudança.
- Spec sem matriz I/O / Design Notes da spec antiga — **false**: oneshot só tem Intent; spec `done` anterior não é contrato desta mudança.
- Clique com modificador ainda move o viewer — **medium** patched: ignora modificadores e botão não primário.
- `</ul>\\s*<iframe` não prova a box — **low** rejeitado: o host por article + script cobrem o contrato estático.
