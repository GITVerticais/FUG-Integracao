---
title: 'Remover "em desenvolvimento" dos footers e desfixar o da home'
type: 'bugfix'
created: '2026-09-17'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Os três footers publicados ainda dizem que a página está em desenvolvimento, e o footer da home usa `sticky bottom-0`, então acompanha o scroll em vez de ficar só no final da página.

**Approach:** Tirar o texto de "em desenvolvimento" só dos `<footer>` das três páginas. Manter os overlays "em desenvolvimento" dos cartões da home que ainda não têm página (Editais, Dados Contábeis, FAQ). No footer da home, remover o pinning (`sticky`/`fixed`); deixar o bloco no fluxo, no final do documento.

</frozen-after-approval>

## Implementation Notes

- Alvos: `index.html` L125–138 (frase L128, "Status: Em desenvolvimento." L131, `sticky bottom-0` L126); `governanca/index.html` L169–175; `estrutura-organizacional/index.html` L1531–1537.
- Home: apagar o `<div>` da frase; em L131 deixar só `© 2024 Espaço de Integridade.` (sem Status). Manter os links Privacidade/Termos/Suporte. Trocar a class do `<footer>`: tirar `sticky bottom-0`; manter `mt-auto` e o `body` `min-h-screen flex flex-col`.
- Governança e Estrutura: apagar o `<p>Esta página está em desenvolvimento.</p>`; manter o copyright.
- Não tocar: `.js-dev-button` / `.js-btn-overlay` (Editais, Dados Contábeis, FAQ, script L162–180), nav mobile `fixed bottom-0` L139–160, templates BMad.
- Teste novo `tools/test_footers.py` no padrão de `tools/test_home_estrutura.py`: recortar cada `<footer>…</footer>`; assert `"em desenvolvimento"` ausente no footer das três páginas; assert o footer da home não tem `sticky` nem `fixed`; assert os três overlays dos cartões ainda contêm `em desenvolvimento`.
- TDD: `tools/test_footers.py` vermelho (2 failed, overlay verde); HTML verde; depois patch de review.
- Review: footer da home ganhou `pt-6 pb-24 md:pb-6` para não ficar sob a nav mobile; `npm run css` para emitir as utilities. Teste passou a exigir copyright, links da home, overlays nomeados e `</main>` antes de `<footer>`.
- `python -m pytest tools -q` — 69 passed. Sem MCP de browser nesta sessão.

## Review Triage Log

- Footer da home sob a nav `fixed bottom-0` no viewport curto — **medium**. `mt-auto` + `min-h-screen` colam o bloco no fundo. Patch: `pt-6 pb-24 md:pb-6` e `npm run css`.
- Teste não travava copyright nem Privacidade/Termos/Suporte — **medium**. Patch: asserts no texto do footer.
- Overlay test aceitava quaisquer 3 `.js-btn-overlay` — **medium**. Patch: recorte por `<!-- Editais -->` / `<!-- Dados Contábeis -->` / `<!-- FAQ -->`.
- `pagina.name` era `index.html` nas três páginas — **low**. Patch: caminho relativo a `ROOT`.
- `mt-2` nas links da home após remover a frase — **low**. Patch: classe removida; `gap-2` do footer basta.
- `gap-2`/`py-8` nos footers de governança e estrutura com um só parágrafo — **low**, rejeitado. Encolher padding mudaria o visual das internas sem pedido.
- Copyright 2024 na home vs 2025 nas internas — **false**. A home só perdeu o Status; o ano já era 2024.
- Teste não travava ordem no documento; nav depois do footer no DOM — **medium** na ordem (`</main>` antes de `<footer>`, patched). Nav depois do footer: **false** — chrome mobile pré-existente; spec não mexe nela.
- Links `href="#"` voltam ao topo — **defer**. Pré-existente; destinos reais seriam páginas novas. Entrada em `deferred-work.md`.
- Spec `in-progress` com linhas pré-edit — **false**. Finalize marca `done`; as linhas eram mapa de planejamento.
