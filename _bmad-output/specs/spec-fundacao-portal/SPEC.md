---
id: SPEC-fundacao-portal
companions: []
sources:
  - index.html
---

> **Contrato canônico.** Este SPEC e os arquivos em `companions:` são o contrato completo do que construir, testar e validar. Documentos de origem listados no frontmatter servem à rastreabilidade — consulte-os apenas se precisar da narrativa que este contrato omite de propósito.

# Fundação técnica do portal

## Why

**Mandato e dor operacional.** O Espaço de Integridade da Fundação Ulysses Guimarães é hoje um único `index.html` que carrega Tailwind por CDN, sem build, sem layout compartilhado e sem nenhum caminho entre os documentos oficiais e a página publicada. A feature de Estrutura Organizacional precisa publicar 267 registros oficiais vindos de planilhas e PDFs, com atualização anual. Sem um pipeline repetível de origem para página e sem um CSS de produção, cada atualização anual vira edição manual de HTML — inaceitável num portal de transparência, onde número publicado é declaração institucional. Esta spec estabelece a base sobre a qual as outras cinco constroem.

Afeta: quem mantém o portal (atualização anual sem editar HTML) e o cidadão (página que abre rápido e funciona em leitor de tela).

## Capabilities

- **CAP-1**
  - **intent:** O portal serve CSS compilado e versionado, sem depender do Tailwind em tempo de execução no navegador.
  - **success:** `npm run css` gera `assets/css/main.css`; nenhuma página publicada referencia `cdn.tailwindcss.com`; a página renderiza com o layout correto sem requisição a CDN de CSS.

- **CAP-2**
  - **intent:** Um mantenedor converte as planilhas e PDFs oficiais em JSON normalizado com um comando.
  - **success:** `npm run dados` regenera `data/*.json` a partir de `downloads/`; executar duas vezes seguidas não produz diferença em `git diff`.

- **CAP-3**
  - **intent:** Os dados de origem são normalizados de forma explícita e auditável antes de virarem página.
  - **success:** caracteres de formatação invisível removidos, espaços colapsados, caixa de nomes próprios normalizada com partículas em minúsculas e siglas de UF preservadas; cada correção de digitação consta em um mapa nomeado no código, nunca embutida em regex.

- **CAP-4**
  - **intent:** O leitor navega entre as seções da página sem depender de JavaScript.
  - **success:** com JS desativado, as três seções permanecem visíveis e legíveis na ordem do documento; com `:has()` disponível, clicar em um link de seção exibe apenas o painel correspondente e a âncora é compartilhável.

- **CAP-5**
  - **intent:** As tabelas são geradas no arquivo HTML publicado, não montadas no cliente.
  - **success:** `npm run tabelas` substitui o conteúdo entre os marcadores `BLOCO:<secao>:INICIO` e `BLOCO:<secao>:FIM`; `curl` da página retorna o HTML com todas as linhas das tabelas presentes.

## Constraints

- Tailwind por CDN é proibido em produção: causa flash de conteúdo sem estilo e entrega payload desnecessário.
- O CSS compilado é versionado no repositório, para que quem só edita conteúdo não precise de Node instalado.
- As tabelas devem existir no HTML servido — portal de transparência exige indexação por buscador e leitura por leitor de tela sem JavaScript.
- O pipeline transcreve e normaliza formato; **nunca** calcula, concilia ou infere valores de origem.
- Os arquivos oficiais `.xlsx` e `.pdf` ficam versionados em `downloads/` e são a fonte de verdade de tudo que a página publica.
- Todo conteúdo publicado em pt-br.

## Non-goals

- Nenhum framework SPA ou gerador de sites estáticos (React, Vue, Next, Astro, 11ty) nesta etapa.
- Nenhum backend, banco de dados ou CMS.
- Migrar o `index.html` existente do CDN para o CSS compilado.
- Extrair header e footer para um layout compartilhado — a duplicação é aceitável em 2 páginas e vira dívida registrada a partir da quarta.
- Publicar exercícios anteriores a 2025.

## Success signal

Um mantenedor substitui a planilha em `downloads/`, executa `npm run build` e a página publicada reflete os novos dados sem que ninguém tenha aberto um arquivo HTML. O `git diff` resultante mostra apenas as linhas de dados que de fato mudaram.

## Assumptions

- Ano de referência 2025, conforme o organograma oficial Anexo II FUG 2025.
- Deploy é hospedagem estática; o build roda localmente ou em CI, nunca no servidor.
- A equipe que mantém o conteúdo não necessariamente tem Node instalado — daí o CSS versionado.

## Open Questions

- O `index.html` existente migra para o CSS compilado nesta spec, numa spec própria, ou permanece no CDN até o portal ter mais páginas?
- O build deve rodar em CI (GitHub Actions) a cada push, ou fica sob responsabilidade manual de quem atualiza?
