---
title: 'Atualizar o ano dos footers para 2026'
type: 'chore'
created: '2026-09-18'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Os três footers publicados ainda mostram anos antigos: a home tem `© 2024` e as páginas internas têm `© 2025`.

**Approach:** Trocar só o ano do copyright de cada `<footer>` para 2026, sem alterar o restante do texto, o layout ou anos que não estão no footer.

</frozen-after-approval>

## Implementation Notes

- Alvos: `index.html` L128 (`© 2024 Espaço de Integridade.`); `governanca/index.html` L171 (`&copy; 2025`); `estrutura-organizacional/index.html` L1533 (`&copy; 2025`).
- Home: `2024` → `2026`. Manter `©` unicode e o ponto final. Internas: `2025` → `2026`. Manter `&copy;` e o restante (`Espaço de Integridade – Fundação Ulysses Guimarães.`).
- Não tocar: templates BMad, overlays da home, títulos/links/arquivos `2025` fora do footer (PDFs, XLSX, organograma, relatório).
- Reusar `tools/test_footers.py`: no recorte de cada `<footer>`, assert `2026` no texto visível e `2024`/`2025` ausentes. TDD: teste vermelho, HTML verde, `python -m pytest tools/test_footers.py -q`.
- TDD: `test_footers_copyright_2026` vermelho em `index.html` (`© 2024`). HTML: home `2024`→`2026`; internas `&copy; 2025`→`&copy; 2026`. `python -m pytest tools -q` — 74 passed.
- Review: teste passou a exigir `(?:©|&copy;)\s*2026` no HTML do footer; docstring atualizada. Browser: home, governança e estrutura mostram `© 2026`.

## Review Triage Log

- Spec ainda `in-progress` após o HTML — **false**. Oneshot só marca `done` depois do review.
- Teste aceitava `2026` solto, sem `©`/`&copy;` — **medium**. Patch: regex no markup do footer.
- Banir `2024`/`2025` no footer inteiro — **medium**. Mesmo gap; o ban largo saiu com o patch.
- `_texto()` não decodifica entities, símbolo poderia sumir — **medium**. Mesmo gap; o regex lê o HTML cru.
- Teste não trava “Fundação Ulysses Guimarães.” — **low**, rejeitado. `espaço de integridade` já estava travado; o pedido era só o ano.
- Docstring do teste não citava 2026 — **low**. Patch: docstring atualizada.
- `_footer()` pega só o primeiro `<footer>` — **low**, rejeitado. Pré-existente; cada página tem um footer.
- Notes duplicadas / `review_loop_iteration: 0` / triage ausente — **false**. Loop 0 é o oneshot; triage entra aqui.
- Spec antiga ainda documenta `© 2024` — **false**. Artefato `done` histórico, fora do escopo.
- Spec untracked — **false**. O commit inclui o artefato.
- Home `2024`→`2026` sem intervalo — **false**. O pedido foi 2026, não `2024–2026`.
- Constante `ANO_COPYRIGHT` — **low**, rejeitado. Número mágico anual em três HTMLs estáticos não pede constante.
