---
title: 'Baixar o XLSX oficial de downloads, sem gerar arquivo no navegador'
type: 'feature'
created: '2026-09-15'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** O botão de baixar XLSX foi planejado para gerar um arquivo novo no navegador com SheetJS. Isso duplica a fonte de verdade: os oficiais já estão em `downloads/`. As tags de `xlsx.full.min.js` e `exportar-xlsx.js` já estão no HTML; o JS local não existe.

**Approach:** O clique baixa o `.xlsx` versionado em `downloads/` via `<a download>` estático. Remover SheetJS e `exportar-xlsx.js`. Sem JavaScript novo.

</frozen-after-approval>

## Implementation Notes

- Só as seções com `.xlsx` em `downloads/`: `#diretorias` → `../downloads/diretorias-2025.xlsx`; `#corpo-funcional` → `../downloads/corpo-funcional-2025.xlsx`. `#estrutura-remuneratoria` não tem xlsx — não inventar botão. `#organograma` já tem o PDF; não mexer.
- Markup: copiar o `<a class="inline-flex items-center gap-2 text-sm font-semibold text-primary hover:underline" … download>` do PDF do organograma (`estrutura-organizacional/index.html` ~2035–2039). Ícone `download`, texto `Baixar o XLSX oficial`.
- Posição: depois do parágrafo introdutório de cada seção, **antes** de `BLOCO:*:INICIO`, para `npm run tabelas` não apagar.
- Remover as duas tags do rodapé (~2057–2058): CDN SheetJS 0.18.5 e `../assets/js/exportar-xlsx.js`. Não criar o JS.
- Não tocar `BLOCO:*`, `tools/build_tables.py`, `tools/xlsx_to_json.py`, `downloads/*`.
- Teste: assertar os dois `href` + `download` e a ausência de `xlsx.full.min.js` / `exportar-xlsx.js` no HTML publicado.
- Implementado: links estáticos após o parágrafo introdutório de `#diretorias` e `#corpo-funcional`; tags SheetJS/`exportar-xlsx.js` removidas do rodapé. `tools/test_exportacao_xlsx.py` cobre os dois hrefs (antes de `BLOCO:*`), `aria-label` distinto, existência dos arquivos em `downloads/` e a ausência do gerador JS. `python -m pytest tools/test_exportacao_xlsx.py tools/test_abas.py -q` — 3 passed. Sem ferramentas de browser nesta sessão.
- Review: `aria-label` distinto por seção; o texto visível permanece `Baixar o XLSX oficial`.

## Review Triage Log

- Blind Hunter: dois links com o mesmo nome acessível — **medium**. Confirmado. Patch: `aria-label` por seção.
- Blind Hunter: teste não confere existência em `downloads/` — **medium**. Confirmado. Patch: `Path.is_file()` no mesmo teste.
- Blind Hunter: teste não cobre rótulo/ícone/remuneratória/PDF — **low**, rejeitado. Contrato central (href + sem SheetJS) já coberto; expandir a suíte não corrige falha de usuário.
- Blind Hunter: regex exige `href` antes de `download` — **low**, rejeitado. Markup atual (e o do organograma) já usa essa ordem; reordenar atributos não é uso normal.
- Blind Hunter: SPEC-exportacao-dados e specs done ainda pedem SheetJS — **defer**. Contrato canônico antigo; corrigir exigiria editar specs fechadas.
- Blind Hunter: link não avisa que o arquivo é a planilha-fonte, não o dump da tela — **false**. O intent é servir o oficial de `downloads/`; aviso contradiria a decisão.
- Blind Hunter: `download` booleano / Safari / `Content-Disposition` — **low**, rejeitado. Mesmo padrão do PDF do organograma; Safari não foi observado.
- Blind Hunter: spec `in-progress` e Intent ainda cita as tags SheetJS — **false**. Intent descreve o problema de partida; o status era o da etapa.
