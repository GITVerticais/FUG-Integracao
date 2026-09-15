---
title: 'Organograma oficial na página, com scroll contido e conversão no build'
type: 'feature'
created: '2026-09-15'
status: 'done'
route: 'dispatch'
baseline_commit: '39a95265e39e2624754af16c2b498a1e2b38bb7e'
review_loop_iteration: 0
context: ['{project-root}/_bmad-output/specs/spec-organograma/SPEC.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** O organograma oficial (Anexo II, A3 paisagem) só é consumível como PDF. `estrutura-organizacional/index.html` já publica SVG + texto + links (linhas 52-87), mas CAP-1 não está fechada: o `body` não tem garantia de não rolar lateralmente em 375 px, e `tools/render_organograma.py` não entra em `npm run build` — trocar o PDF e rodar o comando do mantenedor não atualiza a imagem da página.

**Approach:** Fechar CAP-1 a CAP-4 da `SPEC-organograma`: mover o bloco para o mecanismo `.abas` como painel, conter o scroll horizontal na figura, ligar a conversão PDF→SVG/PNG ao build com pré-voo, e cobrir a matriz de I/O com testes. Reusar o markup de `figure`/`figcaption`/`alt` já presente — não redesenhar o diagrama.

## Decisões acordadas

- **O organograma é uma aba**, não um resumo acima da nav. Painel com `id="organograma"` e classe `aba-painel`, primeiro na nav e no DOM — se ficasse depois das três tabelas, o success signal (percorrer o diagrama no celular) ficaria abaixo de 267 linhas. Rótulo da aba: `Organograma geral`.
- **O texto da `figcaption` permanece o atual** (quatro camadas, 27 unidades, níveis 1–10). Validação institucional da FUG é processo editorial, fora desta spec.

## Boundaries & Constraints

**Always:**
- `downloads/organograma-fug-2025.pdf` é a única fonte de verdade do diagrama; SVG e PNG em `assets/img/` são derivados do build.
- O diagrama é documento oficial: não redesenhar, reordenar, recolorir nem alterar rótulos.
- Conversão no build, nunca no navegador; nenhuma biblioteca de PDF no cliente.
- Em viewport de 375 px a figura tem scroll horizontal próprio; o `body` não rola lateralmente.
- Sem hash, os quatro painéis permanecem visíveis na ordem do documento; com `:has()` e um painel em `:target`, só aquele aparece.
- Conteúdo publicado em pt-br.

**Never:**
- Organograma interativo, nós expansíveis ou ligação caixa→pessoa.
- Versões de exercícios anteriores a 2025.
- Redesenho para casar com a identidade visual do portal.
- Copiar PNG/SVG para `downloads/` — lá só entra o PDF oficial.
- Alterar o comportamento das três abas existentes, marcadores `BLOCO:*`, `tools/build_tables.py`, `xlsx_to_json.py`, `pdf_to_json.py` ou as tags de exportação.
- Introduzir JavaScript para o organograma.
- `overflow-x: hidden` no `body` (corta anel de foco e cabeçalho).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Conversão normal | PDF presente, `assets/img/` existe | Escreve `organograma-fug-2025.svg`, `.png` e `-preview.png` | N/A |
| Reexecução | script rodado 2x | Segunda execução não altera bytes dos três arquivos | N/A |
| PDF ausente | `downloads/organograma-fug-2025.pdf` não existe | Nenhuma escrita em `assets/img/` | Aborta nomeando o caminho; exit != 0 |
| PDF sem páginas | PDF abre com 0 páginas | Nenhuma escrita | Aborta; exit != 0 |
| Pasta de saída ausente | `assets/img/` não existe | Cria a pasta e escreve os três arquivos | N/A |

</frozen-after-approval>

## Code Map

- `estrutura-organizacional/index.html` — bloco hoje nas linhas 52-87, **fora** de `.abas` (linha 92). Mover para dentro de `.abas` como primeiro `section.aba-painel#organograma`. Acrescentar o primeiro `.aba-link` com `href="#organograma"`. Reusar `figure`/`figcaption`/`alt`/links; `img` em `../assets/img/organograma-fug-2025.svg` (2611×1599), PNG tamanho real em `assets/img/`, PDF em `downloads/`. Não tocar marcadores `BLOCO:*` nem as duas tags `<script>` do rodapé.
- `assets/css/input.css` — abas em `:has()` nas linhas 28-39 (três seletores). Acrescentar a quarta regra para `#organograma`. Componente nomeado de scroll da figura aqui. Não pôr `overflow-x: hidden` no `body`.
- `tools/render_organograma.py` — 24 linhas, execução no topo do módulo. `SRC` L10, `OUT` L11, `get_svg_image` L17, pixmaps 1.0 e 0.5 L20-22. Sem `main()`, sem guarda. Entra em `npm run build` (dívida BH10).
- `package.json` — `build` = `dados && tabelas && css`. Adicionar script `organograma` e encadear depois de `tabelas`.
- `assets/img/organograma-fug-2025.svg` / `.png` / `-preview.png` — já gerados. Regenerar só se o output do script mudar; versionar.
- `downloads/organograma-fug-2025.pdf` — origem. Não modificar.
- `tools/test_build_tables.py` — padrão `tmp_path`. Não alterar. Novo: `tools/test_render_organograma.py`.
- `requirements.txt` — `pymupdf==1.28.2` já pinado. Não alterar.

## Tasks & Acceptance

**Execution:**
- [x] `tools/test_render_organograma.py` -- cobrir a matriz (PDF ausente, PDF vazio, pasta de saída ausente, reexecução idempotente) **antes** de endurecer o script -- TDD.
- [x] `tools/render_organograma.py` -- `main()`, recusar PDF ausente ou sem páginas sem escrever, criar `assets/img/` se faltar -- constraint de conversão no build.
- [x] `package.json` -- script `organograma` encadeado em `build` -- CAP-1: trocar o PDF e rodar o comando do mantenedor atualiza a imagem.
- [x] `estrutura-organizacional/index.html` -- mover o bloco para `.abas` como primeiro painel `#organograma`; primeiro `.aba-link`; limitar largura do ancestral da figura -- CAP-1 e decisão de colocação.
- [x] `assets/css/input.css` -- quarta regra `:has(#organograma:target)` e componente de scroll da figura -- CAP-1; as três regras existentes permanecem.
- [x] `assets/css/main.css` -- regenerar com `npm run css` -- CSS compilado versionado.

**Acceptance Criteria:**
- Dado viewport de 375 px, quando o cidadão percorre o organograma, então só o contêiner da figura rola horizontalmente e `document.documentElement.scrollWidth` não excede `clientWidth`.
- Dado desktop em zoom 100%, quando a página abre, então o SVG é a imagem visível da figura e permanece nítido.
- Dado JavaScript desativado e URL sem hash, quando a página abre, então os quatro painéis (organograma primeiro) ficam visíveis, com figura, `figcaption` e os dois links no HTML servido.
- Dado um navegador com `:has()`, quando o leitor clica em "Organograma geral", então só aquele painel fica visível, a aba é destacada e `#organograma` é compartilhável.
- Dado o atributo `alt` da imagem, quando um leitor de tela o anuncia, então ele descreve o conteúdo do diagrama, não o nome do arquivo.
- Dado `downloads/organograma-fug-2025.pdf` substituído, quando se roda `npm run build`, então `assets/img/organograma-fug-2025.svg` e `.png` são regenerados.
- Dado o PDF ausente, quando se roda `python tools/render_organograma.py`, então exit != 0 e os arquivos em `assets/img/` não são tocados.

## Implementation Notes

- Destaque da aba ativa saiu de `@layer components` para `@layer utilities`. Os links já têm `text-on-surface-variant` e `border-transparent`; na camada de components a regra `:has()` perdia e a aba não mudava de cor. Chrome em 375 px, depois da transição de 150 ms: aba ativa `rgb(134, 33, 32)`.
- Verificação no Chrome (puppeteer-core, viewport 375×812): `document.documentElement.scrollWidth === clientWidth === 375`; `.organograma-figura-scroll` com `overflow-x: auto`, `scrollWidth` 900 / `clientWidth` 325. Sem hash: quatro painéis `display: block`, `#organograma` primeiro. Com `#organograma`: só aquele painel visível. Clique em Dirigentes esconde o organograma.
- Desktop 1280 px: SVG `currentSrc` aponta para `organograma-fug-2025.svg`, `naturalWidth` 2611×1599.
- `npm run organograma` duas vezes: `git diff --quiet` nos três derivados. `python -m pytest tools/test_render_organograma.py tools/test_build_tables.py -q`: 17 passed.

## Spec Change Log

## Review Triage Log

- BH1 figcaption não avisa que o A3 continua na horizontal — **low**. Texto pré-existente; CAP-2 pede camadas/27 unidades/níveis 1–10, que já estão. Recusar: o conserto é copy nova não pedida, e a barra nativa de `overflow-x: auto` já sinaliza o pan.
- BH2 `.organograma-figura-scroll` sem foco nem nome acessível — **low**. O wrapper `overflow-x-auto` anterior também não era focável. Recusar: `tabindex`+`aria-label` adiciona superfície ARIA; CAP-4 pede `figure`/`figcaption`/`alt`, já cumpridos.
- BH3 falta `overscroll-behavior-x: contain` — **low**. Chrome 375 px: `documentElement.scrollWidth === 375`; a página não tem overflow horizontal para encadear. Recusar: o toque no fim do pan é cosmético.
- BH4 `figure.overflow-hidden` pode recortar anel de foco — **low**. A classe já estava no `figure` antes desta spec. Recusar: Chrome mostrou a figura rolando no wrapper interno, não clipada.
- BH5/EC4 escrita não atômica SVG depois PNG — **low**. Disco cheio no meio da conversão não é uso cotidiano; temp+replace adiciona complexidade. Recusar.
- BH6/EC1 PDF corrompido/diretório foge de `ErroDeConversao` — **low**. `downloads/organograma-fug-2025.pdf` é o A3 versionado; o programa não foi mostrado alcançando arquivo ilegível. Recusar: o traceback do PyMuPDF é falha alta de mantenedor, não o caminho da matriz.
- BH7 sempre `doc[0]`, sem checar 2611×1599 — **false**. A conversão da página 0 é o comportamento do script; HTML com width/height fixos já existia. Recusar.
- BH8 testes usam PDF 200×100, não o oficial — **false**. O padrão do repositório é `tmp_path` (`test_build_tables.py`); a matriz pede três arquivos escritos, coberta pelos stubs.
- BH9 `test_main_devolve_1_quando_pdf_sem_paginas` não exige o caminho no stderr — **low**. Em `tools/test_render_organograma.py:156` só `assert capsys.readouterr().err`; a matriz pede abortar nomeando o caminho. O `converter()` correspondente já checa. Patch: assertiva do path.
- BH10 meta e lead não citam o organograma — **low**. O lead descreve as tabelas; a aba "Organograma geral" é o primeiro controle visível. Recusar: reescrever a intro é copy pública que o intent não fechou, e o cidadão encontra a aba sem o parágrafo.
- BH11 link `#estrutura-remuneratoria` esconde o diagrama — **false**. Decisão congelada: o organograma é aba; `:target` nas outras seções é o mecanismo das quatro abas.
- BH12 PNG em `assets/img/` e preview sem uso — **false**. Frozen: PNG é derivado em `assets/img/`; PDF oficial em `downloads/`; preview gerado e fora da página.
- BH13 `package.json` sem script `test` — **low**. Pré-existente: `test_build_tables.py` também não entra em npm. Recusar: adicionar script de teste não corrige o diff desta spec.
- EC2 PDF criptografado — **false**. A origem oficial não é criptografada; o programa não foi mostrado alcançando esse estado.
- EC3 PDF com mais de uma página — **low**. O Anexo II é uma página A3. Recusar: recusar páginas extras adiciona regra que a matriz não pede.
- EC5 `out` é arquivo, não pasta — **false**. `assets/img/` é diretório versionado; `FileExistsError` nisso não é estado que o pipeline alcança.
- EC6 hash `#titulo-organograma` não filtra abas — **low**. O `h2` com id próprio é o padrão das três seções já publicadas; o link da nav aponta para `#organograma`. Recusar: o cidadão não usa o id do título.
- VG1 contrato de aba/scroll pode regredir com pytest verde — **medium**. Pré-verificado. Sem harness de browser no repositório; a Verification da spec já marca isso como checagem manual; CI ficou fora do intent da fundação (VG1). Defer.
- VG2 `npm run build` pode perder `organograma` sem os testes falharem — **medium**. Pré-verificado. `test_build_tables.py` também não trava o encadeamento de `tabelas` em `build`. Defer.

## Design Notes

O `img` tem `min-w-[900px]` para forçar overflow em telas estreitas. Em flex/block, `min-width: auto` do ancestral deixa essa mínima inflar o `body`. Limitar o ancestral da figura (`min-width: 0` + `overflow-x: auto` no wrapper interno).

O PNG "tamanho real" permanece em `assets/img/` (derivado). O PDF oficial permanece em `downloads/`. `organograma-fug-2025-preview.png` continua gerado e não entra na página.

A quarta regra `:has()` segue o padrão das três existentes. Sem hash, nenhum painel está em `:target` e os quatro aparecem.

## Verification

**Commands:**
- `python -m pytest tools/test_render_organograma.py -q` -- expected: todos os testes passam.
- `python -m pytest tools/test_build_tables.py -q` -- expected: regressão das tabelas continua verde.
- `npm run build` -- expected: termina em 0; inclui a conversão do organograma.
- `npm run organograma && git diff --quiet -- assets/img/organograma-fug-2025.svg assets/img/organograma-fug-2025.png assets/img/organograma-fug-2025-preview.png` -- expected: segunda execução consecutiva não altera bytes.

**Manual checks (if no CLI):**
- Viewport 375 px em `#organograma`: a figura rola na horizontal; a página não. Sem hash: quatro seções visíveis, organograma primeiro. Clicar cada aba: só o painel correspondente.
- Zoom 100% desktop: SVG nítido. "Ver em tamanho real" abre o PNG; "Baixar o PDF oficial" baixa o PDF.
