---
id: SPEC-governanca
companions:
  - documentos-oficiais.md
sources:
  - "C:/Users/murilo verticais/Desktop/PORTAL-20260908T201342Z-1-001/PORTAL/Regimento Interno.pdf"
  - "C:/Users/murilo verticais/Desktop/PORTAL-20260908T201342Z-1-001/PORTAL/RELATÓRIO ESCOLA MOVIMENTO 2025.pdf"
  - "C:/Users/murilo verticais/Desktop/PORTAL-20260908T201342Z-1-001/PORTAL/Código de Ética.pdf"
  - "C:/Users/murilo verticais/Desktop/PORTAL-20260908T201342Z-1-001/PORTAL/Estatuto.pdf"
---

> **Contrato canônico.** Esta SPEC e os arquivos em `companions:` são o contrato completo do que construir, testar e validar. Os documentos listados em `sources:` servem à rastreabilidade; o conteúdo oficial deve ser publicado como PDF, sem transcrição.

# Governança

## Why

**Oportunidade.** O portal precisa reunir em um único ponto os documentos institucionais que orientam a governança e a atuação da FUG. Hoje, quem procura Regimento Interno, Estatuto, Código de Ética ou o Relatório Escola Movimento 2025 precisa localizar arquivos separados; uma página própria reduz esse atrito e deixa a fonte oficial disponível para leitura e download. Afeta cidadãos, participantes da Fundação, imprensa e órgãos de controle.

## Capabilities

- **CAP-1**
  - **intent:** O visitante acessa a página de Governança a partir da página inicial do portal.
  - **success:** a entrada `Governança` deixa de apresentar apenas estado de desenvolvimento e leva a uma página própria, cujo título e cabeçalho identificam o módulo.

- **CAP-2**
  - **intent:** O visitante identifica os quatro documentos disponíveis e escolhe aquele que deseja consultar.
  - **success:** a página apresenta, com os nomes exatos, Regimento Interno, Relatório Escola Movimento 2025, Código de Ética e Estatuto; nenhum dos quatro é omitido ou substituído por outro arquivo.

- **CAP-3**
  - **intent:** O visitante lê cada documento no navegador sem precisar baixá-lo antes.
  - **success:** cada um dos quatro documentos possui uma ação de visualização que abre o PDF oficial no fluxo de leitura do navegador; todos os arquivos podem ser percorridos página a página.

- **CAP-4**
  - **intent:** O visitante baixa individualmente o documento que selecionou.
  - **success:** existem quatro ações de download identificadas pelo nome do documento, e cada uma entrega o PDF correspondente ao item acionado, sem gerar um arquivo diferente ou misturar documentos.

- **CAP-5**
  - **intent:** O visitante usa a página independentemente de mouse, tamanho de tela ou tecnologia assistiva.
  - **success:** títulos, documentos e ações têm nomes acessíveis, recebem foco visível por teclado e permanecem utilizáveis em viewport móvel sem rolagem horizontal do corpo da página.

## Constraints

- A entrega é uma única página de Governança; os quatro documentos não ganham páginas de conteúdo separadas nesta etapa.
- Os PDFs fornecidos são a fonte de verdade. A publicação deve preservar os bytes e o conteúdo oficiais; não transcrever, resumir, editar, recompor ou converter os documentos.
- Cada documento deve ter um vínculo de visualização e um vínculo de download para o mesmo arquivo oficial correspondente.
- A página deve continuar sendo uma interface estática do portal: nenhuma biblioteca de leitura de PDF, processamento de conteúdo ou geração de PDF no navegador é necessária para cumprir o contrato.
- Os nomes dos quatro documentos devem permanecer distinguíveis e fiéis aos títulos fornecidos, inclusive o ano de 2025 do relatório.

## Non-goals

- Transcrição HTML, resumo, busca textual, anotação ou edição do conteúdo dos PDFs.
- Área administrativa para cadastrar, substituir ou versionar documentos.
- Publicação de documentos de exercícios diferentes dos quatro arquivos fornecidos.
- Autenticação, comentários ou fluxo de aprovação para acessar os documentos.

## Success signal

Um visitante abre o portal, entra em Governança, escolhe qualquer um dos quatro documentos, consegue lê-lo no navegador e baixa exatamente o PDF escolhido — inclusive em um celular e sem depender de copiar o conteúdo para outra página.

## Assumptions

- Os quatro arquivos fornecidos pelo usuário são as versões oficiais que devem ser publicadas.
- Os PDFs serão públicos e não exigirão autenticação.
- Os destinos normalizados descritos em `documentos-oficiais.md` são aceitáveis para a implementação, desde que os bytes originais sejam preservados.

## Open Questions

- A ação de visualização deve manter o PDF embutido na página ou abrir o visualizador nativo do navegador em uma nova aba?
- Os nomes de arquivo normalizados em `downloads/` devem ser mantidos ou a FUG exige os nomes originais com espaços e acentos?
