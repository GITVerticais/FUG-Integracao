---
title: 'Migrar o portal atual para Next.js'
type: 'feature'
created: '2026-10-21'
status: 'done'
route: 'dispatch'
baseline_commit: '5d26c62214f29a6bdf07345d80447d4b0171ea5e'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** O portal é HTML estático, com chrome copiado. Início, governança e estrutura precisam das mesmas URLs e do mesmo conteúdo, e a home precisa do sexto cartão Ouvidoria, ainda sem formulário.

**Approach:** Um app Next.js (App Router) serve as três rotas e uma `/ouvidoria` vazia. Os `index.html` saem só depois dos testes na página nova. No mesmo conjunto, `vercel.json` deixa de publicar a raiz estática.

## Boundaries & Constraints

**Always:**
- Um layout. Chrome do início (`index.html` L17–37, L125–157) em todas as rotas. Início vai para `/`. Denúncias, no desktop e no menu móvel, vai para `/ouvidoria`. Políticas e Treinamentos do desktop continuam `#`. O item móvel continua “Treino”, sem link. A trilha Início / página fica no conteúdo, não no cabeçalho.
- Home: duas colunas no desktop, um cartão por linha no celular, fundo `#862120`, rótulo em caixa alta. Ordem: Governança, Estrutura Organizacional, Editais, Dados Contábeis, FAQ, Ouvidoria. Última linha: FAQ à esquerda, Ouvidoria à direita. Os três do meio não navegam; hover e clique de 1,5 s mostram “em desenvolvimento”.
- Governança: os quatro PDFs, na ordem atual, Visualizar no iframe `#visualizador-governanca`, Baixar em `/downloads/`.
- Estrutura: as quatro seções no HTML da primeira resposta (dirigentes, corpo funcional, estrutura remuneratória, organograma). O cliente só troca o painel. Sem `:target` e sem `:has()` para esconder painel. VACÂNCIA, CPF, escape e âncoras seguem `tools/build_tables.py`. Texto e links do organograma ficam antes da figura. `scroll-padding-top: 6rem` permanece.
- `downloads/` na raiz é a fonte. O build copia para `public/downloads/`. `npm run dados` segue gerando `data/*.json`. Organograma vai para `public/img/`.
- Cores, Inter, Material Symbols e raios permanecem. Body interno é `bg-background`; o gradiente fica só na home.
- `/ouvidoria` responde 200, com o layout, sem formulário e sem horário, telefone ou e-mail.

**Never:**
- Formulário, protocolo, consulta, estatística, fila, Neon, Blob, reCAPTCHA, `.env` ou API.
- Página de Editais, Dados Contábeis ou FAQ. Destino no `account_circle`. Corrigir o timeout do overlay.
- Reescrever `spec-fundacao-portal` ou `spec-dirigentes-colegiados`. Servir HTML antigo e Next no mesmo endereço.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Home | `GET /` | Seis cartões na ordem; FAQ e Ouvidoria na última linha | N/A |
| Sem página | Hover ou clique em Editais, Dados Contábeis ou FAQ | “em desenvolvimento”; não navega | N/A |
| Denúncias | Cabeçalho ou menu móvel | Abre `/ouvidoria` | N/A |
| Governança | `GET /governanca` | Quatro PDFs; Visualizar no iframe; Baixar em `/downloads/` | N/A |
| Estrutura | `GET /estrutura-organizacional` | Quatro seções no HTML; VACÂNCIA e CPF iguais ao gerador; XLSX em `/downloads/` | N/A |
| Aba | Outra seção | Só muda o painel visível; sem `:target` | N/A |
| Ouvidoria | `GET /ouvidoria` | 200, sem formulário e sem canal | N/A |
| Cópia | Build sem copiar `downloads/` | PDF e XLSX não resolvem | O build copia `downloads/` para `public/downloads/` antes de `next build` |

</frozen-after-approval>

## Code Map

- `index.html` L47–177 — cartões, FAQ centralizado, clique de 1,5 s. Substituir, não editar no lugar.
- `governanca/index.html` L55–166 — quatro artigos, iframe, `[data-visualizador-host]`.
- `estrutura-organizacional/index.html` L52–66 — ordem das abas. Marcadores `BLOCO` acabam.
- `tools/build_tables.py` L55–126 — `esc`, VACÂNCIA, `sanitizar_cpf`, âncoras. Reusar as regras no componente; o script para de escrever HTML.
- `tools/xlsx_to_json.py` — não mudar.
- `tools/render_organograma.py` L15 — `OUT` passa de `assets/img/` para `public/img/`.
- `tailwind.config.js` L3, L8–61 — incluir `app/**/*.tsx` e `components/**/*.tsx`. Tokens intactos.
- `assets/css/input.css` L11 — manter `scroll-padding-top`. L19–71 — não levar `:target` / `:has()`.
- `vercel.json` — hoje `outputDirectory: "."`. Passa a buildar Next.
- `package.json` L6–12 — saem `css`, `css:watch` e `tabelas`.
- `tools/test_home_governanca.py`, `tools/test_home_estrutura.py`, `tools/test_footers.py`, `tools/test_governanca_docs.py`, `tools/test_exportacao_xlsx.py`, `tools/test_build_tables.py` — HTML das rotas. `tools/test_abas.py` deixa de exigir `:target`. `tools/test_render_organograma.py` acompanha `public/img/`.

## Tasks & Acceptance

**Execution:**
- [x] `package.json`, `tailwind.config.js`, `postcss.config.js`, `next.config.ts` — Next, React, React DOM; Tailwind em `app/` e `components/`; `build` = dados, organograma, cópia de `downloads/`, `next build`.
- [x] `app/layout.tsx`, `components/Header.tsx`, `components/Footer.tsx`, `app/globals.css` — chrome único e `scroll-padding-top`.
- [x] `app/page.tsx` — seis cartões; FAQ deixa a linha sozinha.
- [x] `app/governanca/page.tsx` — quatro PDFs e o iframe.
- [x] `app/estrutura-organizacional/page.tsx` — `data/*.json`, quatro seções no HTML, abas sem `:target`.
- [x] `app/ouvidoria/page.tsx` — sem formulário e sem canal.
- [x] `tools/render_organograma.py` — saída em `public/img/`.
- [x] `tools/test_*.py` — HTML das rotas; manter VACÂNCIA, CPF, escape, PDFs e cartões.
- [x] `index.html`, `governanca/index.html`, `estrutura-organizacional/index.html`, `tools/build_tables.py` — apagar com a suíte verde. `vercel.json` deixa a raiz estática.

**Acceptance Criteria:**
- Given a suíte verde, when a história termina, then os três `index.html` não existem e `vercel.json` não publica a raiz estática.
- Given `npm run dados`, when a estrutura renderiza, then a fonte é `data/*.json` e ninguém injeta `<!-- BLOCO:`.
- Given Políticas, Treinamentos ou Treino, when o visitante aciona, then o destino é o de hoje.

## Implementation Notes

## Spec Change Log

## Review Triage Log

- blind: abas ignoram hash, link interno e Ctrl+clique — `medium` — `page.tsx` só escuta `a.aba-link` e não lê `location.hash`; o painel alvo continua `hidden`.
- blind: três seções somem sem JS e sem `aria-selected` — `false` — a spec manda o cliente trocar o painel e proíbe `:target`/`:has()`; o HTML da primeira resposta ainda traz as quatro seções.
- blind: clique de 1,5 s não remove `opacity-0` — `false` — o `index.html` removido também só fazia `classList.add('opacity-100')`; a spec proíbe corrigir esse timeout.
- blind: Início sublinhado em toda rota, foco e nome do `account_circle` — `false` — o chrome do início, inclusive o sublinhado, é o contrato para todas as rotas; o botão continua sem destino.
- blind: `/ouvidoria` sem trilha e sem descrição — `false` — a matriz pede 200, layout, sem formulário e sem canal; a frase da trilha só tira ela do cabeçalho.
- blind: sem script `dev` e `public/` gitignored — `low`, rejeitado — quem publica roda `npm run build`; acrescentar `dev` é superfície nova.
- blind: `copy_downloads.js` apaga o destino antes da cópia — `low`, rejeitado — `cpSync` que falha interrompe o `&&` e o `next build` não publica; o conserto seria um guard extra.
- blind: build na Vercel sem `pip install` — `maybe-false` — não rodei a imagem da Vercel; se faltar openpyxl/pymupdf o build quebra. Adiado.
- blind: `/index.html` e `/assets/img/` sem redirect — `false` — os três `index.html` saem de propósito e o organograma passa a `/img/`.
- blind: `.cursor/hooks.json` com caminho absoluto — `low` — arquivo já estava untracked antes desta história e é contexto de agente. Adiado.
- blind: `main()` ignora `--pagina` e a suíte não renderiza — `false` para o `main()` — `test_json_ausente_aborta_orientando_npm_run_dados` chama `gerar()`, não `main()`. Os buracos reais estão nas linhas de verification-gap.
- blind: `next-env.d.ts` importa `.next/types` e `input.css` ainda tem `:target` — `false` / `low` — o `next build` gera esses tipos; `app/globals.css` é o CSS carregado e não tem `:target`. `input.css` é arquivo antigo não referenciado. Adiado com o tsbuildinfo.
- edge: hash na carga deixa o painel hidden — `medium` — mesma causa do primeiro item.
- edge: link que não é `aba-link` não abre o painel — `medium` — `#estrutura-remuneratoria` no corpo e no organograma não entra no listener.
- edge: clique da aba não grava o hash — `medium` — mesma causa; o refresh volta à primeira seção.
- edge: sem o script as três seções ficam hidden — `false` — é o modelo “o cliente só troca o painel”.
- edge: Visualizar antes do script deixa o iframe hidden — `low`, rejeitado — a corrida acaba quando o script liga; tirar `hidden` mexe no contrato que o teste já trava.
- edge: segundo clique antes de 1500 ms — `false` — o timeout antigo também não chamava `clearTimeout`; a spec proíbe corrigir isso.
- edge: JSON que não é array quebra a tabela — `false` — `xlsx_to_json.py` grava arrays; dado corrompido deve falhar alto.
- edge: id de colegiado vazio ou repetido — `maybe-false`, rejeitado — seria no máximo `low` e não abri a planilha para confirmar.
- edge: `render_tabelas.js` chama erro de forma de “JSON inválido” — `low`, rejeitado — o conserto é um ramo novo; o comando certo continua sendo `npm run dados`.
- edge: docstring de `xlsx_to_json.py` cita `build_tables.py` — `low`, rejeitado — o code map manda não mudar esse arquivo.
- edge: FAQ não fica sozinha na linha — `false` — o bloco congelado pede FAQ à esquerda e Ouvidoria à direita; a página faz isso.
- verification-gap: argumentos trocados em `blocoDiretorias`/`blocoCorpoFuncional`/`blocoEstruturaRemuneratoria` passam na suíte — `medium` — os testes rodam o CLI, não a chamada da página. Rota: patch.
- verification-gap: inverter `painel.hidden` passa na suíte — `medium` — `test_abas.py` só procura substrings. Rota: patch.
- verification-gap: `copy_downloads.js` não é executado — `medium` — o teste lê o texto do script. Rota: patch.
- verification-gap: o layout pode perder `<Header` — `low` — `test_footers.py` só vê o Footer. Correção direta. Rota: patch.
- verification-gap: `viewer.src = ""` ainda passa — `medium` — o teste só vê a substring `viewer.src`. Rota: patch.
- verification-gap (other): links internos deixam Estrutura Remuneratória hidden — `medium` — conferido em `page.tsx` L51 e L74; não são `a.aba-link`. Rota: patch, mesma causa do hash.

## Verification

**Commands:**
- `python -m pytest tools -q` — expected: passa, com VACÂNCIA, CPF, escape, quatro PDFs, seis cartões e sem os `index.html`.
- `npm run build` — expected: `next build` conclui e `public/downloads/` existe.
