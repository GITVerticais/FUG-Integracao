---
title: 'Remover a nota de transcrição da estrutura remuneratória'
type: 'bugfix'
created: '2026-09-15'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `#estrutura-remuneratoria` mostra o parágrafo "Transcrição do PDF oficial de 2025. Vagas previstas são as posições do cargo no quadro; vagas preenchidas são as posições ocupadas segundo o mesmo PDF." Esse texto não deve aparecer na página.

**Approach:** Apagar o parágrafo pré-BLOCO que contém só essa frase. Manter o intro da seção, o `<a download>` do PDF e a legenda do BLOCO. Atualizar `tools/test_exportacao_xlsx.py` para deixar de exigir as notas e passar a garantir que a frase não volta.

</frozen-after-approval>

## Review Triage Log

- BH1 assert `"posições ocupadas segundo o mesmo PDF"` não casa o markup original quebrado entre `ocupadas` e `segundo` — **medium**. Confirmado no `<p>` removido. Patch: frase completa contra `re.sub(r"\s+", " ", seção)`.
- BH2 recorte só até `BLOCO:INICIO` não trava ausência na página nem a legenda do BLOCO — **medium** (ausência na `<section>`). Patch: busca da frase na seção inteira. Legenda do BLOCO: **low**, rejeitado — não foi apagada; `"35" not in markup` no BLOCO quebraria em `R$ 35.000,00` e células `35`.
- BH3 nada trava o intro que deve ficar — **low**, rejeitado. O intro não foi tocado.
- BH4 nada trava a legenda do BLOCO — **low**, rejeitado. Mesma evidência de BH2.
- BH5 asserts sem colapso de whitespace — **medium**. Mesma causa de BH1; mesmo patch.
- BH6 glossário de vagas previstas/preenchidas não foi substituído — **false**. O pedido é apagar a frase, não repor definição. O intro ainda nomeia os rótulos.
- BH7 spec done ainda exige notas CAP-4 — **medium**, defer. Atualizar `spec-estrutura-remuneratoria.md` sairia do escopo.
- BH8 docstring de `test_exportacao_xlsx.py` só fala de XLSX — **low**. Patch: uma linha no docstring. O teste desta seção já existia no arquivo.

## Implementation Notes

- TDD: `test_estrutura_remuneratoria_oferece_pdf_oficial_sem_notas_de_transcricao` vermelho com o parágrafo ainda no HTML; verde após apagar o `<p>` pré-BLOCO.
- Arquivos: `estrutura-organizacional/index.html` (remove o parágrafo), `tools/test_exportacao_xlsx.py` (proíbe a frase; mantém download do PDF e as proibições de 29/35/Q.T./Q.P.).
- Intro da seção, `<a download>` e a legenda do BLOCO (`Valores transcritos do PDF oficial, sem qualquer cálculo.`) permaneceram.
- `pytest tools/test_exportacao_xlsx.py tools/test_abas.py tools/test_build_tables.py -q` — 28 passed.
- Review: o assert `"posições ocupadas segundo o mesmo PDF"` era morto (quebra de linha no HTML original). Patch: a seção inteira, com whitespace colapsado, não pode conter a frase.
- Navegador MCP indisponível; conferido no HTML publicado e no pytest. Servidor `http.server:8765` recusou a leitura HTTP.
