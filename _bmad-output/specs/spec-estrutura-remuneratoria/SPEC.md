---
id: SPEC-estrutura-remuneratoria
companions: []
sources:
  - downloads/estrutura-remuneratoria-2025.pdf
  - data/estrutura-remuneratoria.json
---

> **Contrato canônico.** Este SPEC e os arquivos em `companions:` são o contrato completo do que construir, testar e validar. Documentos de origem listados no frontmatter servem à rastreabilidade — consulte-os apenas se precisar da narrativa que este contrato omite de propósito.

# Estrutura remuneratória

## Why

**Mandato.** A estrutura remuneratória é a informação de transparência de maior escrutínio público: mostra quanto a instituição paga por cargo, sem expor quanto cada pessoa recebe. A FUG mantém 20 cargos distribuídos em 10 níveis, do Jovem Aprendiz ao Secretário Executivo, hoje publicados apenas como PDF. Publicá-la como tabela na página coloca a informação ao alcance de quem não baixa arquivos — e é a peça que dá sentido aos níveis 1 a 10 marcados no organograma.

Esta é também a seção mais arriscada do conjunto: é a única onde um número errado vira declaração institucional incorreta sobre remuneração pública.

Afeta: cidadão, imprensa e órgãos de controle.

## Capabilities

- **CAP-1**
  - **intent:** O leitor vê, por cargo, o nível hierárquico e as faixas salariais praticadas.
  - **success:** 20 cargos publicados, ordenados por nível decrescente, com salário base, faixa média e faixa máxima exatamente como constam no PDF oficial.

- **CAP-2**
  - **intent:** O leitor entende quantas vagas existem e quantas estão ocupadas em cada cargo.
  - **success:** as colunas de quantitativo aparecem com rótulo por extenso; nenhuma sigla é publicada sem legenda visível na página.

- **CAP-3**
  - **intent:** O leitor sabe quais adicionais podem incidir sobre a remuneração de cada cargo.
  - **success:** a coluna de adicionais possíveis é preenchida com informação fornecida pela FUG, ou a coluna é omitida — nunca publicada com valor inventado.

- **CAP-4**
  - **intent:** A tabela vem acompanhada das notas que explicam o que ela não diz sozinha.
  - **success:** abaixo da tabela constam a data de atualização, a base normativa e a explicação do quantitativo, no modelo das notas explicativas do site de referência.

- **CAP-5**
  - **intent:** A seção abre com uma apresentação curta do que ela contém.
  - **success:** um parágrafo adaptado do modelo de referência, com nomenclatura da FUG.

## Constraints

- Valores são **transcritos** do PDF oficial: nunca recalculados, arredondados, convertidos de moeda ou reformatados de modo a alterar o número.
- Os valores "R$ –" do PDF são preservados como travessão e **nunca** convertidos para zero: ausência de faixa não é faixa igual a zero.
- Nenhuma remuneração nominal individual, em qualquer forma.
- A divergência de efetivo entre esta seção e o corpo funcional não pode ser resolvida silenciosamente pelo código — é decisão institucional, não técnica.
- Siglas do documento de origem não vão para a página sem tradução.

## Non-goals

- Remuneração nominal individual.
- Histórico de reajustes ou série temporal de faixas.
- Cálculo de folha, encargos ou custo total do quadro.
- Exercícios anteriores a 2025.

## Success signal

Um jornalista abre a seção e consegue afirmar, com fonte, qual a faixa máxima do cargo de Gerente na FUG e quantas vagas desse cargo existem — e cada número que ele citar bate com o PDF oficial publicado ao lado.

## Assumptions

- Os 20 cargos extraídos do PDF representam a estrutura completa e vigente em 2025.
- "Q.T." e "Q.P." significam quadro total e quadro preenchido. **Esta é inferência, não fato do documento** — ver questões abertas.

## Open Questions

- **BLOQUEANTE.** O quantitativo preenchido do PDF soma **35** posições, enquanto a planilha de corpo funcional lista **29** pessoas. A divergência também aparece por cargo: Auxiliar Administrativo Júnior 6 no PDF contra 8 na planilha; Assistente Administrativo III 1 contra 3. Qual número a FUG publica? Enquanto isso não for respondido, as duas seções não podem ir ao ar juntas.
- Confirmar o significado exato de "Q.T." e "Q.P.". A leitura como quadro total e quadro preenchido é inferência minha e não consta no PDF.
- A coluna "adicionais possíveis" foi pedida pelo cliente, mas o PDF da FUG não a traz — o site de referência preenche com "AUX-CRECHE". Qual o conteúdo correto para a FUG?
- Qual a data de atualização e a base normativa (acordo coletivo, plano de cargos e salários) a citar nas notas explicativas?
- O cliente pediu "cargo, número de pessoas e possíveis adicionais", mas o PDF traz também nível, salário base e duas faixas. Publicar tudo, ou reduzir às três colunas pedidas?
