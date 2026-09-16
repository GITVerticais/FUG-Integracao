---
id: SPEC-organograma
companions: []
sources:
  - downloads/organograma-fug-2025.pdf
---

> **Contrato canônico.** Este SPEC e os arquivos em `companions:` são o contrato completo do que construir, testar e validar. Documentos de origem listados no frontmatter servem à rastreabilidade — consulte-os apenas se precisar da narrativa que este contrato omite de propósito.

# Organograma geral da FUG

## Why

**Mandato.** O organograma oficial da Fundação Ulysses Guimarães (Anexo II, exercício 2025) existe somente como PDF A3 em paisagem, 2611×1599 pt. Nesse formato ele não é consumível na web: o cidadão precisa baixar um arquivo e abrir em outro programa para entender quem responde a quem na instituição. O organograma é o único artefato que mostra a estrutura inteira de uma vez — as três seções tabulares mostram pessoas, ele mostra a arquitetura. Sem ele, as tabelas são listas sem contexto.

Afeta: o cidadão que quer entender a instituição antes de procurar uma pessoa nela.

## Capabilities

- **CAP-1**
  - **intent:** O leitor vê o organograma oficial diretamente na página, sem baixar nada.
  - **success:** o diagrama renderiza como imagem vetorial legível em zoom 100% no desktop; em viewport de 375 px, a figura oferece scroll horizontal próprio sem que o `body` da página role lateralmente.

- **CAP-2**
  - **intent:** O leitor entende como ler o diagrama a partir de um texto logo abaixo dele.
  - **success:** o texto nomeia as quatro camadas (governança voluntária, estratégico, tático, operacional), menciona as 27 unidades de representação e liga os níveis 1 a 10 à seção de estrutura remuneratória.

- **CAP-3**
  - **intent:** Quem precisa do arquivo original consegue chegar nele.
  - **success:** a página oferece link para a imagem em tamanho real e para o PDF oficial, ambos a partir de `downloads/`.

- **CAP-4**
  - **intent:** Um leitor de tela transmite o que a imagem contém.
  - **success:** a figura usa `figure`/`figcaption`; o atributo `alt` descreve o conteúdo do diagrama, não o nome do arquivo.

## Constraints

- O diagrama é documento oficial: não pode ser redesenhado, reordenado, recolorido ou ter rótulos alterados.
- A proporção 1,63:1 em paisagem exige scroll horizontal contido na própria figura; o corpo da página nunca rola lateralmente.
- A conversão do PDF acontece no build, não no navegador: nenhuma biblioteca de renderização de PDF no cliente.

## Non-goals

- Organograma interativo, navegável ou com nós expansíveis.
- Versões de exercícios anteriores.
- Redesenho ou reestilização visual do diagrama para casar com a identidade do portal.
- Ligar cada caixa do organograma ao registro da pessoa que ocupa o cargo.

## Success signal

Um cidadão abre a página no celular, percorre o organograma lateralmente, lê o texto abaixo e consegue explicar a diferença entre Conselho Curador e Diretoria Administrativa sem ter baixado o PDF.

## Assumptions

- O SVG vetorial é preferível ao PNG: 124 KB contra 243 KB, e nítido em qualquer zoom.
- O organograma de 2025 é o vigente e não muda dentro do exercício.

## Open Questions

- O organograma fica acima das abas, como resumo que enquadra a página inteira, ou vira uma quarta aba ao lado das três seções?
- O texto explicativo foi redigido a partir da leitura do diagrama. Precisa de validação da FUG antes da publicação?
