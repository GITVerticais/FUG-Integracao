---
title: 'Índice de colegiados em Dirigentes e Órgãos Colegiados'
type: 'feature'
created: '2026-09-15'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
context: ['{project-root}/_bmad-output/specs/spec-dirigentes-colegiados/SPEC.md']
baseline_commit: 'c78a337d722d7fd0a059db4d29f1530a543b10bd'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Em `#diretorias` as duas primeiras tabelas somam 216 linhas (108 + 9 + 108). O cidadão que busca Conselho Fiscal ou Editorial precisa rolar a página inteira; o problema é o salto entre colegiados, não a leitura de uma linha.

**Approach:** Publicar um índice no topo do BLOCO, com um link por colegiado apontando ao `h3` já existente (`titulo-colegiado-{id}`). Manter as cinco tabelas completas no HTML. Sem paginação e sem JavaScript.

## Decisões acordadas

- **Índice com âncoras.** Um link por colegiado no topo do BLOCO. Sem paginação, sem JS, sem esconder linhas.

## Boundaries & Constraints

**Always:**
- As cinco tabelas continuam inteiras no HTML servido; Ctrl+F e leitor de tela encontram qualquer nome sem virar página.
- O índice é gerado em `bloco_diretorias`, dentro de `BLOCO:diretorias`, a partir dos mesmos `colegiados` das tabelas — um `<a href="#titulo-colegiado-{id}">` por item, na ordem do JSON.
- Com hash no `h3` interno, o filtro CSS das abas permanece: só `#diretorias` visível; a aba "Dirigentes e Órgãos Colegiados" continua destacada. `scroll-margin-top` de `:target` já cobre o header fixo.
- Sem JS. Nomes e totais transcritos da origem. Marcadores `BLOCO:diretorias` preservados.

**Never:**
- Paginação, busca, filtro ou ordenação no cliente.
- Índice por UF, subtítulo de estado, tabela-por-UF, sticky extra, ou `max-height` nas molduras.
- Alterar colunas, linhas, captions, `data-vago` ou a exportação XLSX.
- Tocar `BLOCO:corpo-funcional`, `BLOCO:estrutura-remuneratoria`, `#organograma`, `xlsx_to_json.py` ou as tags `<script>` do rodapé.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Cinco colegiados | JSON com 5 ids | `<nav>` com 5 âncoras; cada `href` casa o `id` do `h3` correspondente | N/A |
| Um colegiado | fixture com 1 item | um link; um `h3`; uma tabela | N/A |
| Reexecução | `npm run tabelas` 2× | bytes do HTML inalterados | N/A |
| Hash no `h3` | URL `#titulo-colegiado-conselho-editorial` com CSS aplicado | painel `#diretorias` visível; os outros `.aba-painel` com `display: none` | N/A |
| Hash na aba | URL `#diretorias` | mesmo filtro vigente hoje; índice no topo do BLOCO | N/A |
| Sem hash | URL sem fragmento | os quatro painéis visíveis; índice não esconde nada | N/A |

</frozen-after-approval>

## Code Map

- `tools/build_tables.py` — `bloco_diretorias` L96–127 já emite `id="titulo-colegiado-{id}"` no `h3`. Inserir o `<nav>` no início do `div.mt-8`, antes do loop. Não alterar `bloco_corpo_funcional`, `bloco_estrutura_remuneratoria`, `SECOES` nem marcadores.
- `estrutura-organizacional/index.html` — BLOCO entre os comentários `BLOCO:diretorias`. Regenerar com `npm run tabelas`. Intro e link do XLSX (fora do BLOCO) não mudam. Não editar as tabelas à mão.
- `assets/css/input.css` — filtro L32–34 só casa `.aba-painel:target`. Acrescentar regra irmã para `.aba-painel :target` (descendente). Destaque da aba L55: também `.abas:has(#diretorias :target) .aba-link[href="#diretorias"]`. Compilar com `npm run css` → `assets/css/main.css`.
- `tools/test_build_tables.py` — cobre `bloco_diretorias` via `tmp_path`. Travar nav+hrefs na fixture de 5 colegiados **antes** de mudar o gerador. Não ler o `index.html` real.
- `tools/test_abas.py` — ordem das quatro abas. Não deve quebrar; não cobre CSS. Acrescentar asserção mínima em `input.css` (duas regras `:has(.aba-painel :target)` e `:has(#diretorias :target)`) ou teste irmão curto.
- `assets/js/exportar-xlsx.js` / downloads — fora. O índice não é `<table>`.

## Tasks & Acceptance

**Execution:**
- [x] `tools/test_build_tables.py` -- travar nav com N âncoras iguais aos `h3` da fixture, na mesma ordem -- TDD da matriz.
- [x] `tools/build_tables.py` -- emitir o `<nav aria-label="Colegiados desta seção">` no BLOCO -- CAP de salto.
- [x] `assets/css/input.css` -- filtro e destaque da aba com `:target` interno a `#diretorias` -- não desmontar as abas.
- [x] `tools/test_abas.py` (ou teste CSS irmão) -- asserção das duas regras novas em `input.css` -- regressão do `:has()`.
- [x] `estrutura-organizacional/index.html` + `assets/css/main.css` -- `npm run tabelas` e `npm run css`; segunda `tabelas` idempotente.

**Acceptance Criteria:**
- Dado JS desativado, quando `#diretorias` abre, então há um índice com cinco links e as cinco tabelas completas abaixo.
- Dado o índice, quando o cidadão ativa "Conselho Editorial", então a página rola até aquele `h3` e as outras abas permanecem ocultas.
- Dado Ctrl+F por um nome da Diretoria Estadual ou do Conselho Curador, então o navegador encontra a linha sem mudar de "página" de tabela.
- Dado URL `#diretorias` ou sem hash, então o comportamento das quatro abas permanece o de hoje.

## Implementation Notes

- 2026-09-15: `bloco_diretorias` emite o `<nav>` no início do `div.mt-8`; HTML regenerado só no BLOCO (+7 linhas). CSS irmão `:has(.aba-painel :target)` + destaque `:has(#diretorias :target)`.
- pytest `tools/test_build_tables.py tools/test_abas.py -q`: 26 passed. `test_indice_com_cinco_ancoras_na_ordem_dos_h3`, `test_indice_com_um_colegiado`, `test_reexecucao_nao_altera_bytes`, `test_filtro_de_abas_cobre_target_interno_em_diretorias`.
- `npm run tabelas` 2×: `sem alteracao`. `main.css` contém os dois seletores.
- Chrome headless: sem hash = quatro `display:block`; `#diretorias` e `#titulo-colegiado-conselho-editorial` = só diretorias visível; `#corpo-funcional` = só aquele painel. Screenshot 1280/`#diretorias` e 375 px: índice no topo, aba destacada; 375 empilha os cinco links.
- Review G1/G2: destaque `:target` interno nas quatro abas; `test_abas.py` lê `main.css` (display:none + quatro seletores). pytest 26 passed.

## Spec Change Log

## Review Triage Log

- **BH1** (blind-hunter) — `low` rejeitado — a conta 216 vs 225 está no bloco congelado; o HTML publicado lista 108/9/108 corretamente. Conserto seria editar spec.
- **BH2** (blind-hunter) — `low` — `input.css` L33–35 esconde qualquer painel sem `:target` descendente; o destaque extra só existe para `#diretorias :target` (L58). Hash em `#titulo-corpo-funcional` / `#titulo-estrutura-remuneratoria` / `#titulo-organograma` oculta irmãos sem sublinhar a aba.
- **BH3** (blind-hunter) — `false` — `<nav aria-label="Colegiados desta seção">` já é landmark; cinco `<a>` dentro dele são anunciados. Lista `ul`/`li` não é requisito do Always.
- **BH4** (blind-hunter) — `low` rejeitado — screenshot 1280 mostra os cinco nomes acima de Diretorias Estaduais; o cidadão não precisa de heading extra no uso diário, e o Always não pede.
- **BH5** (blind-hunter) — `false` — Always transcreve nomes e totais na página; o `href` leva o nome; o total permanece no `p` sob cada `h3`.
- **BH6** (blind-hunter) — `false` — aba `#diretorias` e o histórico do navegador devolvem o índice; não há controle extra no Never/Always.
- **BH7** (blind-hunter) — `low` rejeitado — `h3` já é o `:target` com `scroll-margin-top`; `tabindex="-1"` não é do contrato e quebraria o regex novo sem ganho no fluxo do cidadão.
- **BH8** (blind-hunter) — `false` — `xlsx_to_json` emite lista; JSON ausente aborta antes de `bloco_diretorias`. Lista vazia não chega do pipeline oficial.
- **BH9** (blind-hunter) — `medium` — mesmo gap de VG1: `test_filtro_de_abas_cobre_target_interno_em_diretorias` só lê `input.css`.
- **BH10** (blind-hunter) — `false` — Code Map manda o nav no início do `div.mt-8.space-y-12`; o gap de 3rem antes do primeiro `h3` é o espaçamento dessa árvore. Screenshot não mostra colisão.
- **BH11** (blind-hunter) — `low` — `scroll-behavior: smooth` já existia em `input.css` L6–8; o índice só aumenta os saltos. Pré-existente.
- **BH12** (blind-hunter) — `low` rejeitado — regex de ordem de atributos só falha se o markup do `h3`/`a` mudar; não é defeito do índice publicado.
- **EC1** (edge-case-hunter) — `low` — mesma raiz de BH2 (`input.css` L56–60).
- **EC2** (edge-case-hunter) — `false` — `dados.get("colegiados", [])` recebe lista do JSON oficial; `null` não é produzido por `xlsx_to_json.diretorias()`.
- **EC3** (edge-case-hunter) — `false` — os cinco `id` do JSON são únicos e preenchidos; colisão não ocorre na origem.
- **VG1** (verification-gap) — `medium` — pré-verificado. `test_abas.py` L31–34 não lê `main.css` nem a metade `:not(:has(:target))` do `display:none`. Página linka `main.css` em `index.html` L10.

**Agrupamento**
- G1 = BH2+EC1 — destaque de aba só em `#diretorias :target` — `low` → **patch**
- G2 = BH9+VG1 — teste não trava o CSS compilado — `medium` → **patch**
- G3 = BH11 — `prefers-reduced-motion` ausente — `low` → **defer**
## Design Notes

O `:target` das abas é um único fragmento na URL. `href="#titulo-colegiado-…"` tira `#diretorias` do alvo; a regra atual `.abas:has(.aba-painel:target)` desliga o filtro e os quatro painéis voltam a aparecer. Por isso o índice **não** funciona sem a regra de descendente:

```css
.abas:has(.aba-painel:target) .aba-painel:not(:target),
.abas:has(.aba-painel :target) .aba-painel:not(:has(:target)) {
  display: none;
}
```

Paginação quebraria o success signal do SPEC canônico (Ctrl+F sem JS) e o Always de tabela única por colegiado já congelado em `spec-dirigentes-colegiados.md`.

## Verification

**Commands:**
- `python -m pytest tools/test_build_tables.py tools/test_abas.py -q` -- expected: todos passam, inclusive nav+hrefs e regras CSS.
- `npm run tabelas` -- expected: exit 0; 2ª execução `git diff --quiet -- estrutura-organizacional/index.html`.
- `npm run css` -- expected: `assets/css/main.css` contém o `:has(.aba-painel :target)`.

**Manual checks (if no CLI):**
- Em `#diretorias`, clicar Conselho Fiscal e Conselho Editorial: scroll no `h3`; Corpo Funcional e Organograma não aparecem abaixo.
- Ctrl+F `Oséias` e o presidente do Conselho Curador, sem JS.
- 375 px: índice empilha; header sticky não cobre o `h3` alvo.
