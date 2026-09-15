---
id: SPEC-dirigentes-colegiados
companions: []
sources:
  - downloads/diretorias-2025.xlsx
  - data/diretorias.json
---

> **Contrato canônico.** Este SPEC e os arquivos em `companions:` são o contrato completo do que construir, testar e validar. Documentos de origem listados no frontmatter servem à rastreabilidade — consulte-os apenas se precisar da narrativa que este contrato omite de propósito.

# Dirigentes e órgãos colegiados

## Why

**Mandato.** Quem dirige a Fundação Ulysses Guimarães é a informação de transparência mais procurada de um portal como este, e hoje ela não está publicada em lugar nenhum. São 238 dirigentes distribuídos em cinco colegiados — Diretorias Estaduais, Diretoria Administrativa, Conselho Curador, Conselho Fiscal e Conselho Editorial — incluindo representação nas 27 unidades da federação. A planilha oficial já entrega os CPF parcialmente mascarados, o que permite publicar a identificação sem violar a LGPD.

Afeta: cidadão, imprensa e órgãos de controle que precisam identificar responsáveis institucionais.

## Capabilities

- **CAP-1**
  - **intent:** O leitor encontra os membros de cada colegiado numa tabela própria daquele colegiado.
  - **success:** cinco tabelas publicadas — Diretorias Estaduais (108), Diretoria Administrativa (9), Conselho Curador (108), Conselho Fiscal (6), Conselho Editorial (7) — cada uma com título e total de membros visível.

- **CAP-2**
  - **intent:** Cada linha identifica a unidade de representação, o cargo, o nome e o CPF parcial.
  - **success:** as quatro colunas aparecem na ordem da planilha de origem, com cabeçalho `th` associado por escopo.

- **CAP-3**
  - **intent:** A identificação por CPF é publicada sem expor o número completo.
  - **success:** nenhum CPF completo no HTML publicado; todo valor segue o formato `ddd.XXX.XXX-dd` tal como vem da planilha oficial.

- **CAP-4**
  - **intent:** Cargos vagos aparecem como vagos, em vez de desaparecerem da tabela.
  - **success:** as três posições sem titular constam com o cargo preenchido e o nome marcado como "Não preenchido"; o total de linhas da tabela reflete os cargos previstos, não apenas os ocupados.

- **CAP-5**
  - **intent:** Dentro das Diretorias Estaduais o leitor localiza a unidade da federação que procura.
  - **success:** as 27 unidades são identificáveis visualmente na tabela, com a ordenação agrupando as linhas de cada unidade.

- **CAP-6**
  - **intent:** A seção abre com uma apresentação curta do que ela contém.
  - **success:** um parágrafo adaptado do modelo de referência, com nomenclatura da FUG e menção explícita ao mascaramento de CPF sob a LGPD.

## Constraints

- **LGPD (Lei nº 13.709/2018):** nenhum CPF completo pode chegar ao HTML publicado. A planilha já entrega mascarado e essa máscara não pode ser revertida, complementada ou cruzada com outra fonte.
- Sem busca, filtro ou ordenação em JavaScript — decisão explícita do cliente por tabela estática.
- Nomes são publicados como constam no documento oficial; apenas a caixa é normalizada.
- A tabela precisa existir no HTML servido, legível por leitor de tela e localizável pelo Ctrl+F do navegador.

## Non-goals

- Busca, filtro, ordenação ou paginação no cliente.
- Fotos, biografias, e-mails ou telefones dos dirigentes.
- Datas de posse, duração ou histórico de mandatos.
- Dirigentes de exercícios anteriores.

## Success signal

Um cidadão abre a seção e localiza, usando só o Ctrl+F do navegador, o presidente do Conselho Curador e o presidente da diretoria do seu próprio estado — sem instalar nada, sem JavaScript e sem baixar planilha.

## Assumptions

- As abas da planilha oficial correspondem um-a-um aos colegiados que devem ser publicados.
- O mascaramento de CPF na planilha foi feito pela própria FUG e é o formato aprovado para publicação.
- As três posições sem titular representam cargos genuinamente vagos, e não falha de preenchimento da planilha.

## Open Questions

- 108 linhas das Diretorias Estaduais numa tabela única é aceitável, ou o cliente prefere agrupar por unidade da federação com subtítulo por estado?
- Confirmar com a FUG que as três posições sem titular (Ceará – Diretor de Formação Política; Pará – Vice-Presidente e Diretor de Formação Política) estão de fato vagas e devem aparecer como tal.
- O cliente citou "Conselho de Orçamento" como exemplo, mas a planilha traz Conselho Editorial e não traz Conselho de Orçamento. Confirmar a lista definitiva de colegiados.
