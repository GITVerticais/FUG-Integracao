---
title: 'Fundação técnica do portal: CSS compilado, pipeline de dados e tabelas estáticas'
type: 'feature'
created: '2026-09-15'
status: 'done'
route: 'dispatch'
baseline_commit: '83108ff436d05cb9d75bbc83495b64e6962df589'
review_loop_iteration: 0
context: ['{project-root}/_bmad-output/specs/spec-fundacao-portal/SPEC.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `estrutura-organizacional/index.html` publica três seções vazias. `assets/css/main.css` nunca foi versionado, `tools/build_tables.py` não existe (`npm run tabelas` quebra), e `.aba-painel:not(:target)` esconde os três painéis quando a URL não tem hash — o oposto da navegação sem JavaScript que a CAP-4 exige. Sem isso, os 267 registros oficiais não chegam à página e cada atualização anual vira edição manual de HTML.

**Approach:** Fechar CAP-1 a CAP-5 da `SPEC-fundacao-portal`: versionar o CSS compilado, declarar as dependências Python do pipeline, reescrever o mecanismo de abas em `:has()` com todas as seções visíveis por padrão, e escrever o gerador que injeta as tabelas como HTML estático entre os marcadores `BLOCO:*` já presentes no arquivo publicado.

## Decisões acordadas

- **O `index.html` da raiz migra do CDN para o CSS compilado nesta spec.** Isso substitui o item de *Non-goals* da spec de origem, por decisão explícita do mantenedor: a proibição de `cdn.tailwindcss.com` passa a valer no portal inteiro em vez de conviver com duas estratégias de CSS. A migração é uma troca limpa — a paleta inline da página e `tailwind.config.js` têm os mesmos 47 tokens com hexes idênticos, o `<style>` inline é duplicata de `input.css`, e as `container-queries` carregadas pelo CDN não são usadas.
- **O build roda manualmente**, por quem atualiza os dados. Nenhuma CAP pede integração contínua; adicionar workflow de CI agora seria ampliação de escopo. Fica registrado como candidato a mudança futura.
- **A spec fica acima do teto de 1.600 tokens** por decisão do mantenedor: as cinco capacidades compartilham um único *success signal* e dividi-las criaria duas specs disputando `estrutura-organizacional/index.html` e `assets/css/input.css`.

## Boundaries & Constraints

**Always:**
- `downloads/*.xlsx` e `downloads/*.pdf` são a única fonte de verdade; todo script lê de lá por caminho relativo à raiz do repositório.
- O pipeline transcreve e normaliza formato — nunca calcula, concilia ou infere valores de origem.
- Determinismo: rodar `npm run build` duas vezes seguidas não produz diferença em `git diff`.
- As tabelas existem no HTML servido e são legíveis por leitor de tela e buscador sem JavaScript.
- Correções de digitação vivem em mapas nomeados no código, nunca embutidas em regex.
- Todo conteúdo publicado em pt-br; `assets/css/main.css` é versionado.

**Never:**
- Nenhum framework SPA ou gerador de sites estáticos; nenhum backend, banco ou CMS.
- Nenhuma referência a `cdn.tailwindcss.com` em nenhuma página do portal ao fim desta spec.
- Não extrair header/footer para layout compartilhado (dívida aceita até a quarta página).
- Não tocar em `assets/js/` nem nas duas tags `<script>` de exportação — pertencem a `SPEC-exportacao-dados`.
- Não publicar exercícios anteriores a 2025.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Injeção normal | `data/*.json` presentes, marcadores íntegros | Conteúdo entre `BLOCO:<secao>:INICIO` e `:FIM` substituído pelas tabelas; marcadores preservados | N/A |
| Reexecução | `npm run tabelas` rodado 2x | Segunda execução não altera bytes do arquivo | N/A |
| Marcador ausente | Falta `BLOCO:corpo-funcional:FIM` | Nenhuma escrita em disco | Aborta com mensagem nomeando o marcador e o arquivo; código de saída != 0 |
| JSON ausente | `data/diretorias.json` não existe | Nenhuma escrita em disco | Aborta orientando rodar `npm run dados`; código de saída != 0 |
| Cargo vago | Registro com `vago: true` | Célula exibe `Não preenchido`; linha marcada semanticamente | N/A |
| Conteúdo com caractere reservado | Nome ou cargo contendo `<` ou `&` | Escapado no HTML gerado | N/A |

</frozen-after-approval>

## Code Map

- `tools/build_tables.py` — **a criar**. Alvo da CAP-5.
- `estrutura-organizacional/index.html` — marcadores `BLOCO:diretorias`, `BLOCO:corpo-funcional`, `BLOCO:estrutura-remuneratoria` nas linhas 108-131; nav de seções em 90-98; painéis `.aba-painel` em 101/113/124. Linhas 144-145 (`xlsx` via cdnjs + `exportar-xlsx.js`): **não tocar**.
- `assets/css/input.css` — linhas 23-32: mecanismo de abas quebrado, a reescrever. `:target { scroll-margin-top }` em 11-13 fica.
- `tools/xlsx_to_json.py` — CAP-2/CAP-3 **já verdes**; reusar `limpar()` (linha 36) e `nome_proprio()` (46) se precisar normalizar na geração. Não alterar a lógica de extração.
- `tools/pdf_to_json.py` — idem; `adicionais` vem fixo como travessão.
- `data/*.json` — contratos de entrada do gerador: `corpo-funcional.json` traz `registros[{unidade,nome,cargo}]`; `diretorias.json` traz `colegiados[{id,nome,total,registros[{unidade,cargo,nome,cpf,vago}]}]`; `estrutura-remuneratoria.json` traz `cargos[{cargo,nivel,quadro_total,quadro_preenchido,salario_base,faixa_media,faixa_maxima,adicionais}]`.
- `index.html` (raiz) — a migrar. Linha 8: `<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries">`. Linhas 14-65: `<script id="tailwind-config">` com paleta idêntica à do `tailwind.config.js`. Logo em seguida, `<style>` com `.material-symbols-outlined`, já coberto por `input.css`. Os três blocos saem; entra `<link href="assets/css/main.css" rel="stylesheet">`. Não alterar o `<body>`.
- `tailwind.config.js` — paleta em tokens (`primary`, `surface-container`, `outline-variant`). `content` já cobre `./*.html`, então a raiz entra na varredura sem mudança. Usar esses nomes nas tabelas; não inventar cor literal.
- `tools/render_organograma.py` — linha 3 aponta para um caminho absoluto no Desktop. Corrigir para `downloads/organograma-fug-2025.pdf`.
- `package.json` — scripts `css`, `dados`, `tabelas`, `build` já definidos; `tabelas` aponta para o arquivo a criar.

## Tasks & Acceptance

**Execution:**
- [x] `requirements.txt` -- criar com `openpyxl`, `pypdf` e `pymupdf` em versões fixadas -- sem manifesto, `npm run dados` falha em máquina limpa e a CAP-2 não se sustenta.
- [x] `tools/render_organograma.py` -- trocar o caminho absoluto do Desktop por `downloads/organograma-fug-2025.pdf` relativo à raiz -- a constraint exige que `downloads/` seja a fonte de verdade de tudo que a página publica.
- [x] `assets/css/input.css` -- reescrever `@layer components`: todos os painéis visíveis por padrão; com `:has()` e um painel em `:target`, esconder os demais e destacar a aba correspondente. Remover `.aba-painel-padrao` e `.aba-link[aria-selected]`, que não existem no HTML -- CAP-4.
- [x] `tools/build_tables.py` -- criar o gerador que lê `data/*.json` e substitui o conteúdo entre os marcadores; escapar HTML; abortar sem escrever quando marcador ou JSON faltar -- CAP-5 e a matriz de I/O.
- [x] `tools/test_build_tables.py` -- cobrir a matriz: marcador ausente, JSON ausente, reexecução idempotente, escape de caractere reservado, registro `vago` -- nenhuma tarefa fecha sem teste passando.
- [x] `estrutura-organizacional/index.html` -- ajustar o markup da nav e dos painéis ao que o CSS novo exige; rodar `npm run tabelas` para materializar as tabelas -- CAP-5.
- [x] `index.html` (raiz) -- remover a tag do CDN, o `<script id="tailwind-config">` e o `<style>` inline; ligar `assets/css/main.css` -- decisão acordada: elimina o CDN do portal inteiro. Executar antes de gerar o CSS, para que a varredura do Tailwind enxergue as classes desta página.
- [x] `assets/css/main.css` -- gerar com `npm run css` e versionar, já com as classes das duas páginas -- CAP-1.

**Acceptance Criteria:**
- Dado JavaScript desativado, quando a página é aberta sem hash na URL, então as três seções aparecem visíveis e legíveis na ordem do documento.
- Dado um navegador com `:has()`, quando o leitor clica em "Corpo Funcional", então apenas aquele painel fica visível, a aba correspondente é destacada e a âncora `#corpo-funcional` é compartilhável e reproduz o mesmo estado.
- Dado o repositório recém-clonado, quando se roda `npm run build`, então `git diff` fica limpo e nenhuma página do portal referencia `cdn.tailwindcss.com`.
- Dada a página inicial servida sem rede para CDN de CSS, quando ela é aberta, então o layout renderiza igual ao que renderizava com o CDN, sem flash de conteúdo sem estilo.
- Dado o HTML servido, quando se busca pelo nome de um dirigente no fonte da página, então a linha correspondente está presente sem execução de JavaScript.

## Implementation Notes

**Verificação feita contra o diff e contra o navegador, não contra o relato de quem implementou.**

- CAP-4 confirmada em navegador real servindo por HTTP, com `main.css` de fato carregado (243 regras): sem hash os três painéis ficam em `display: block` e nenhuma aba destacada; com `#diretorias`, `#corpo-funcional` ou `#estrutura-remuneratoria`, apenas o painel correspondente permanece visível e apenas a aba correspondente assume `rgb(134, 33, 32)` (`primary`). O ancestral `.abas` (linha 92) envolve a nav e os três painéis, que é o que os seletores `:has()` exigem.
- Determinismo confirmado por hash: `sha256` do conjunto `data/*.json` + `main.css` + página publicada é idêntico antes do build, depois do primeiro e depois do segundo. `git diff -- data/` limpo, ou seja, o pipeline reproduz o JSON já commitado.
- 287 linhas de dados no HTML servido (238 diretorias + 29 corpo funcional + 20 cargos); 294 linhas `<tr` contando cabeçalhos. Nomes conferidos diretamente no fonte da página.
- Todos os utilitários Tailwind das duas páginas compilam em `main.css`, incluindo os de valor arbitrário da home (`bg-[#F5F9FF]`, `z-[60]`, `shadow-[0px_4px_12px...]`, `dark:*`, `group-hover:*`). Home renderiza com header, main, footer e h1 de altura não nula, sem nenhum elemento colapsado.
- Pins de `requirements.txt` conferidos contra o que existe no índice e no ambiente: `openpyxl==3.1.5` e `pypdf==6.18.0` instalados; `pymupdf==1.28.2` é a versão corrente e está instalada no Python 3.12 local, não no 3.14 que `python` resolve neste ambiente.

**Duas leituras de verificação que pareciam defeito e não eram**, registradas para quem revisar depois não repetir o caminho: `getComputedStyle(body).minHeight` devolve `0px` e transições de cor congelam em `currentTime: 0` quando o painel do navegador está oculto (`innerWidth`/`innerHeight` zerados). Medir só vale com viewport real.

**Fora do escopo, encontrado durante a verificação:** `estrutura-organizacional/index.html` referencia `assets/js/exportar-xlsx.js`, que não existe — o diretório está vazio. Pertence a `SPEC-exportacao-dados` e foi deliberadamente não tocado.

## Spec Change Log

## Review Triage Log

- BH1 SPEC.md de origem ainda lista a migração do CDN como Non-goal — **low**. O contrato canônico ficou atrás da decisão congelada. Fora do código desta história; vai para defer.
- BH2 Spec Change Log e Review Triage Log vazios — **false**. O log de triage é preenchido agora; o Change Log só existe após loopback. Recusar: o conserto seria editar esta spec.
- BH3 Code Map em tempo verbal pré-implementação — **false**. Recusar: o conserto seria editar esta spec.
- BH4 Matriz/testes omitem JSON inválido, HTML ausente, INICIO ausente, FIM antes de INICIO, coleções vazias, id ausente — **false**. `carregar` já envolve `JSONDecodeError`; `gerar` aborta se a página não existe; `_marcador` aborta se INICIO ou FIM faltam (FIM é buscado depois de INICIO). Coleção vazia e id vazio não são caminhos que o pipeline alcança.
- BH5 Legendas usam `len(registros)` / `len(cargos)` em vez do campo `total` da origem — **medium**. Confirmado em `tools/build_tables.py:94,123,157`. Nos JSON atuais diretorias e corpo coincidem (`total` == tamanho da lista), então o número publicado não mente hoje, mas é cálculo, não transcrição; em remuneratória `20 cargos` não existe na origem (`total_quadro_preenchido` é 35). Patch: transcrever `total` onde existe e não inventar contagem de cargos.
- BH6 Linha vaga sem marcação ARIA — **low**. A célula já entrega `Não preenchido` em `<em>`; `data-vago` não é API de AT. Recusar: o conserto adiciona superfície ARIA, e o critério da matriz já é cumprido pelo texto.
- BH7 Sem controle para voltar ao padrão (três seções visíveis) — **false**. CAP-4 não pede esse controle. `href="#conteudo"` e ids internos de h3 não ativam `.aba-painel:target`, então a página volta ao padrão de mostrar tudo.
- BH8 Abas sem `aria-current` — **low**. Recusar: o mecanismo acordado é CSS-only; `aria-current` dinâmico exigiria JavaScript, excluído pelo intent.
- BH9 `requirements.txt` não pina pytest nem a versão do Python; pymupdf não instala no 3.14 — **low**. A parte pymupdf/3.14 **não** quebra `npm run build` (`dados`/`tabelas`/`css` não importam pymupdf). A parte pytest é real: `python -m pytest tools/test_build_tables.py` falha sem o pacote. Patch: pin de pytest no manifesto.
- BH10 `render_organograma.py` fora de `npm run dados`/`build` — **medium**. Pré-existente: esta história só corrigiu o caminho do PDF. Defer.
- BH11 Home ainda diz "em desenvolvimento" e não liga para a página publicada — **false**. O intent congelado manda não alterar o `<body>` de `index.html`. Fora de escopo pelo próprio intent.
- BH12 Comandos de Verification contradizem o AC de `git diff` limpo — **false**. Recusar: o conserto seria editar esta spec.
- BH13 `grep -c "<tr"` conta cabeçalhos — **false**. Recusar: o conserto seria editar esta spec.
- BH14 SPEC-estrutura-remuneratoria bloqueia publicar 29 e 35 juntos — **medium**. Divergência institucional pré-existente; esta spec transcreve as duas origens. Defer.
- BH15 README sem instruções de pipeline — **low**. Recusar: stub pré-existente; expandir README não é correção direta do diff.
- BH16 Design Notes descrevem o CSS antigo — **false**. Recusar: o conserto seria editar esta spec.
- EC1 JSON/HTML ilegível ou não UTF-8 foge de `ErroDeGeracao` — **false**. O pipeline só emite UTF-8; `UnicodeDecodeError` não é um estado que o programa foi mostrado alcançando.
- EC2 Nós JSON nulos ou de tipo errado — **false**. Os JSON de `data/` são objetos com as chaves do Code Map; `AttributeError` nisso é falha alta, não defeito do gerador.
- EC3 Corpo funcional com `vago` sem marcar a `<tr>` — **false**. O contrato de `corpo-funcional.json` não tem `vago`; `_celula_nome` já cobriria a célula se o campo aparecesse.
- EC4 `vago` truthy não-booleano — **false**. A origem emite `true`/`false` JSON.
- EC5 `write_text` não atômico — **low**. Recusar: disco cheio no meio da escrita não é uso cotidiano; temp+replace adiciona complexidade.
- EC6 PDF ausente ou vazio em `render_organograma.py` — **low**. Pré-existente (o script já abria o PDF sem guarda; só o caminho mudou). Defer.
- EC7 `print` de sucesso com em-dash e "alteração" — **low**. Reproduzido: `PYTHONIOENCODING=ascii python tools/build_tables.py` termina em `UnicodeEncodeError` depois de `gerar()` retornar, exit 1. No Windows cotidiano (`cp1252`) passa. Patch: mensagem só ASCII.
- VG1 CSS das abas sem checagem automatizada — **medium**. Pré-verificado pelo verification-gap; disposição `defer`. Sem harness CSS/browser no repo; CI ficou fora do intent.
- VG2 Teste de cargo vago passa se o gerador ecoar o nome residual — **medium**. Pré-verificado. Fixture em `tools/test_build_tables.py:47` já traz `nome: "Não preenchido"`. Patch: nome residual + assertiva de que esse nome não sai.

## Design Notes

O mecanismo de abas sem JavaScript usa `:has()` num ancestral para que o estado padrão — nenhum hash — mostre tudo, e só a presença de um `:target` ative a filtragem. É o inverso do CSS atual, que esconde por padrão:

```css
/* Só filtra quando algum painel está em :target; sem hash, tudo aparece. */
.abas:has(.aba-painel:target) .aba-painel:not(:target) { display: none; }

/* Destaca a aba cujo href aponta para o painel em :target. */
.abas:has(#corpo-funcional:target) .aba-link[href="#corpo-funcional"] {
  @apply border-primary text-primary;
}
```

O destaque da aba precisa de uma regra por seção porque CSS não casa `href` com o `:target` corrente. São três seções: repetir é mais barato que introduzir JavaScript.

## Verification

**Commands:**
- `python -m pytest tools/test_build_tables.py -q` -- expected: todos os testes passam.
- `npm run build` -- expected: termina em 0; `git diff` mostra apenas linhas de dados que de fato mudaram.
- `npm run build && git diff --quiet` -- expected: código de saída 0 na segunda execução consecutiva (determinismo).
- `grep -rn "cdn.tailwindcss.com" index.html estrutura-organizacional/` -- expected: nenhuma ocorrência.
- `grep -c "<tr" estrutura-organizacional/index.html` -- expected: ao menos 267 linhas de dados no HTML servido.

**Manual checks (if no CLI):**
- Com JavaScript desativado no navegador, abrir `estrutura-organizacional/index.html` sem hash: as três seções visíveis. Clicar em cada aba: apenas o painel correspondente visível, aba destacada, URL compartilhável.
- Abrir `index.html` da raiz e comparar com o estado anterior à migração: mesma aparência, sem flash de conteúdo sem estilo ao carregar.
