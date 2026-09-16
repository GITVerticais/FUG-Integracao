---
title: 'Página de Governança com os quatro PDFs oficiais'
type: 'feature'
created: '2026-09-16'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: '8a89648a017500190f5c759c9cca6519d8d3f392'
context:
  - '{project-root}/_bmad-output/specs/spec-governanca/SPEC.md'
  - '{project-root}/_bmad-output/specs/spec-governanca/documentos-oficiais.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** O cartão Governança da home só mostra "em desenvolvimento". Quem busca Regimento Interno, Relatório Escola Movimento 2025, Código de Ética ou Estatuto não tem um ponto único no portal.

**Approach:** Publicar uma página estática de Governança, ligada a partir da home, com os quatro PDFs oficiais para visualização no navegador e download individual, sem transcrever o conteúdo.

## Boundaries & Constraints

**Always:**
- Uma única página; os quatro documentos na mesma tela.
- Publicar exatamente estes quatro, com os nomes exibidos fiéis: Regimento Interno; Relatório Escola Movimento 2025; Código de Ética; Estatuto.
- Arquivos em `downloads/`: `regimento-interno.pdf`, `relatorio-escola-movimento-2025.pdf`, `codigo-de-etica.pdf`, `estatuto.pdf` (bytes idênticos à origem).
- Cada item tem visualização e download apontando para o mesmo PDF oficial.
- Visualização embutida na página via iframe nativo; o visitante não é mandado a outra aba.
- Interface estática, sem biblioteca de PDF.
- Cartão da home vira link na mesma aba, sem overlay "em desenvolvimento".
- Página utilizável por teclado, com nomes acessíveis e sem rolagem horizontal do corpo em viewport móvel.
- Implementar sobre o merge de `feature/estrutura-organizacional` em `feature/governanca` (não rebase; a branch já está no origin).

**Never:**
- Transcrever, resumir, editar, recompor ou gerar PDF no navegador.
- Páginas separadas por documento; área admin; autenticação; busca/anotação.
- Publicar outros arquivos da pasta de origem (ex.: ESTRUTURA REMUNERATÓRIA.pdf).
- Alterar cartões Editais, Dados Contábeis e FAQ; não reescrever `estrutura-organizacional/index.html`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Home → Governança | clique/Enter no cartão | navega para `governanca/index.html` na mesma aba; título identifica o módulo | N/A |
| Identificar os quatro | página aberta | os quatro nomes exatos visíveis, nesta ordem | N/A |
| Visualizar | acionar visualizar de um item | o PDF correspondente aparece no iframe da própria página | N/A |
| Baixar | acionar download de um item | o navegador recebe o PDF daquele item, não outro | N/A |
| Arquivo extra na origem | pasta Desktop contém outros PDFs | nenhum outro documento aparece na página | ignorar |
| Teclado / móvel | Tab e viewport estreita | ações recebem foco visível; corpo sem overflow-x | N/A |

</frozen-after-approval>

## Code Map

- `index.html` (HEAD `feature/governanca`) — cartão Governança L115–128: `<button class="js-dev-button">` + overlay. Alvo: virar `<a href="governanca/index.html">` no padrão do cartão EO em `feature/estrutura-organizacional` L63–74. Não tocar nos outros `js-dev-button`. Script da overlay só age em `.js-dev-button`.
- `feature/estrutura-organizacional:estrutura-organizacional/index.html` L1–50, L2089–2095 — casca a reutilizar: `../assets/css/main.css`, header sticky, breadcrumb, h1, footer. Não copiar abas/`BLOCO`.
- `feature/estrutura-organizacional:estrutura-organizacional/index.html` L1818–1821 e L2070–2073 — download: `<a href="../downloads/….pdf" download aria-label="…">`. Não usar o `target="_blank"` do organograma: a visualização aqui é iframe na página.
- `feature/estrutura-organizacional:tools/test_home_estrutura.py` — recorte por comentário HTML; assert `<a href>`, sem overlay, destino existe.
- `feature/estrutura-organizacional:tools/test_exportacao_xlsx.py` — `href` + `download` + `aria-label` + arquivo em disco; `xlsx.full.min.js` ausente (aqui: sem pdf.js).
- `feature/estrutura-organizacional:tailwind.config.js` `content` — incluir `./governanca/**/*.html` e regenerar CSS se classes novas.
- Origem (existem no Desktop): `Regimento Interno.pdf`, `RELATÓRIO ESCOLA MOVIMENTO 2025.pdf`, `Código de Ética.pdf`, `Estatuto.pdf`. Copiar com `shutil.copyfile`. Testes não devem depender do caminho Desktop.

## Tasks & Acceptance

**Execution:**
- [x] git — `git merge feature/estrutura-organizacional` em `feature/governanca` (sem rebase). Resolver conflitos da home preservando o cartão EO já linkado.
- [x] `tools/test_home_governanca.py` — recorte `<!-- Governança -->` … `<!-- Estrutura Organizacional -->`; `<a href="governanca/index.html">` sem `target`, sem overlay; destino existe. Vermelho primeiro.
- [x] `tools/test_governanca_docs.py` — os quatro nomes na ordem; cada Visualizar aponta o PDF no iframe (`target` do iframe nomeado ou `src` correspondente); cada download tem `href` + `download` + `aria-label` com o nome; os quatro arquivos existem em `downloads/` e começam com `%PDF`; sem pdf.js; `ESTRUTURA REMUNERATÓRIA` ausente. Vermelho primeiro.
- [x] `downloads/*.pdf` — copiar os quatro oficiais para os slugs acima; bytes idênticos à origem.
- [x] `governanca/index.html` — casca EO; h1 Governança; lista dos quatro; iframe nativo de leitura; download por item; foco visível; `min-w-0` no main.
- [x] `index.html` — só o cartão Governança vira o `<a>`; cartão EO e os `js-dev-button` restantes intactos.
- [x] `tailwind.config.js` + `npm run css` — incluir `./governanca/**/*.html`; regenerar só se classes novas.

**Acceptance Criteria:**
- Given a home, when o visitante aciona Governança, then abre `governanca/index.html` na mesma aba e o título da página identifica o módulo.
- Given a página de Governança, when o visitante lê a lista, then vê os quatro nomes exatos, nesta ordem, e nenhum outro documento.
- Given um dos quatro itens, when aciona visualizar, then o PDF correspondente aparece no iframe da página, sem nova aba.
- Given um dos quatro itens, when aciona baixar, then recebe aquele PDF oficial, não outro.
- Given teclado ou viewport móvel, when percorre a página, then as ações são nomeadas, recebem foco visível e o corpo não exige rolagem horizontal.

## Implementation Notes

## Spec Change Log

## Review Triage Log

- `false` — PDFs ausentes do diff / 404 no clone. `downloads/regimento-interno.pdf`, `relatorio-escola-movimento-2025.pdf`, `codigo-de-etica.pdf` e `estatuto.pdf` existem no worktree e não estão no `.gitignore`; o diff de review omitiu binários. O 404 só ocorreria se um commit futuro os omitisse.
- `false` — sem checksum / teste só `%PDF`. O Code Map manda o teste permanente exigir existência + `%PDF` e não depender do Desktop; a cópia inicial foi `copyfile`.
- `false` — Open Questions do SPEC.md canônico. Corrigir isso seria editar spec; iframe e slugs já estão no bloco congelado desta build.
- `false` — Implementation Notes / Change Log vazios. Seções de processo; o triage está neste log. Corrigir seria editar spec.
- `false` — rodapé “Esta página está em desenvolvimento.” Casca EO (`estrutura-organizacional/index.html:2091`); CAP-1 era o overlay da home.
- `false` — iframe sem empty-state. Markup da Design Notes: viewer vazio até Visualizar.
- `false` — iframe não nomeia o PDF atual. Interface estática; o nome está no `h2` e no `aria-label`.
- `medium` — Visualizar não traz o iframe à vista. Em viewport estreita os quatro cartões empurram `visualizador-governanca` abaixo da dobra; o PDF carrega fora da tela. `governanca/index.html:60-135`.
- `false` — sem fallback iOS/pdf.js. Intent congela iframe nativo sem biblioteca de PDF.
- `medium` — `test_acoes_nomeadas_com_foco_visivel_e_sem_overflow_horizontal` só grepa `min-w-0` em `<main>` e a substring `focus-visible:`. CAP-5 passaria com iframe sem contenção ou classe morta. `tools/test_governanca_docs.py:107-121`.
- `false` — cartão da home sem `focus-visible`. Replica o `<a>` da EO; não há `outline-none`; o anel nativo do `<a>` permanece. `index.html:49-50`.
- `false` — teste da home não trava Editais/FAQ. Os três cartões restantes ainda são `js-dev-button` (`index.html:76-108`).
- `false` — `<ul>` sem nome acessível. Os quatro nomes estão em `h2`.
- `maybe-false` — `vercel.json` sem `Content-Type`/`Content-Disposition` para PDF. Sem evidência de que o host mande `attachment`; Vercel costuma servir `.pdf` como `application/pdf`.
- `medium` — `tools/pdf_to_json.py:31` sem guarda se o PDF oficial falta. Pré-existente da EO, não causado por esta história.
- `medium` — `tools/pdf_to_json.py:32-56` pode gravar `cargos` vazio. Pré-existente da EO.
- `medium` — `tools/xlsx_to_json.py:94` sem guarda se o xlsx falta. Pré-existente da EO.
- `medium` — `tools/xlsx_to_json.py:97-122` quebra em linha curta. Pré-existente da EO.
- `medium` — `tools/render_organograma.py:19-28` pode deixar SVG/PNG parciais. Pré-existente da EO.
- `low` — `assets/css/input.css:6-7` ignora `prefers-reduced-motion`. Pré-existente; já havia defer em spec de colegiados.
- `low` — overlay da home sem `clearTimeout` em clique repetido. Script pré-existente; esta história não o alterou.
- `false` — iframe em branco se o browser não embute PDF. Mesmo limite do iframe nativo congelado.
- `medium` — Visualizar abaixo da dobra (edge-case). Mesmo defeito do iframe fora da vista.
- `false` — iOS ignora `download`. Visualizar e Baixar compartilham a URL por intent; `Content-Disposition: attachment` quebraria o iframe.
- `false` — 404 sem mensagem on-page. Os quatro PDFs existem; o estado não é alcançável neste tree.
- `low` — `tools/test_pdf_to_json.py:68` erra em vez de skip se o PDF da EO faltar. Pré-existente da EO.
- `false` — PDFs untracked (verification-gap). Mesma evidência dos arquivos presentes e commitáveis.
- `medium` — gap de verificação CAP-5 (verification-gap, pré-verificado). Mesmo teste fraco de overflow/foco.

## Design Notes

Lista de documentos, não abas. Um iframe nativo nomeado (não quatro embeds empilhados: CAP-3 pede ação de visualização; um viewer só carrega o PDF escolhido). `target="_blank"` fica fora.

```html
<iframe name="visualizador-governanca" title="Leitura do documento de governança" class="w-full min-h-[70vh]"></iframe>
<article>
  <h2>Regimento Interno</h2>
  <a href="../downloads/regimento-interno.pdf" target="visualizador-governanca">Visualizar</a>
  <a href="../downloads/regimento-interno.pdf" download aria-label="Baixar o PDF oficial do Regimento Interno">Baixar</a>
</article>
```

Cópia binária (`copyfile`). Conferir bytes na cópia inicial; o teste permanente exige `%PDF` + existência.

## Verification

**Commands:**
- `python -m pytest tools/test_home_governanca.py tools/test_governanca_docs.py -q` -- expected: pass
- `python -m pytest tools/test_home_estrutura.py -q` -- expected: pass; cartão EO intacto

**Manual checks (if no CLI):**
- Abrir `governanca/index.html`, visualizar e baixar os quatro PDFs; conferir conteúdo/arquivo.
- Viewport ~375px: sem scroll horizontal do `body`.
- Tab: ordem e anel de foco nas ações.
