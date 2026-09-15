---
id: SPEC-corpo-funcional
companions: []
sources:
  - downloads/corpo-funcional-2025.xlsx
  - data/corpo-funcional.json
---

> **Contrato canônico.** Este SPEC e os arquivos em `companions:` são o contrato completo do que construir, testar e validar. Documentos de origem listados no frontmatter servem à rastreabilidade — consulte-os apenas se precisar da narrativa que este contrato omite de propósito.

# Corpo funcional

## Why

**Mandato.** Além dos dirigentes voluntários, a Fundação Ulysses Guimarães mantém um corpo funcional contratado — 29 empregados distribuídos entre a sede no Distrito Federal e unidades estaduais. Publicar quem são e que cargo ocupam é exigência corrente de transparência para entidades desta natureza, e é a contraparte nominal da tabela de estrutura remuneratória: uma mostra as faixas do cargo, a outra mostra quem ocupa os cargos, sem nunca cruzar as duas coisas numa remuneração individual.

Afeta: cidadão e órgãos de controle que verificam a proporcionalidade do quadro funcional.

## Capabilities

- **CAP-1**
  - **intent:** O leitor vê a relação completa dos empregados com cargo e unidade.
  - **success:** tabela com os 29 registros, ordenada por nome, colunas Nome, Cargo e Unidade.

- **CAP-2**
  - **intent:** A seção informa o cargo sem jamais expor a remuneração daquela pessoa.
  - **success:** nenhuma coluna, nota ou atributo da tabela contém valor monetário; a faixa salarial do cargo é alcançada por link para a seção de estrutura remuneratória.

- **CAP-3**
  - **intent:** A seção abre com uma apresentação curta do que ela contém.
  - **success:** um parágrafo adaptado do modelo de referência, com nomenclatura da FUG.

- **CAP-4**
  - **intent:** Erros de digitação da planilha de origem não são reproduzidos na página publicada.
  - **success:** as correções aplicadas constam num mapa nomeado no conversor, uma entrada por correção, rastreável em revisão de código.

## Constraints

- Sem CPF nesta seção: a planilha de corpo funcional não traz o campo e ele não deve ser buscado em outra fonte.
- Nunca publicar remuneração nominal individual, nem em nota, nem em atributo, nem no arquivo exportado.
- Nomes publicados como constam no documento oficial; apenas a caixa é normalizada.
- A unidade de representação vem da coluna ESTADOS da planilha, que usa preenchimento por bloco — o conversor propaga o último estado informado, e essa propagação precisa ser conferida contra a planilha.

## Non-goals

- CPF, data de admissão, matrícula ou vínculo contratual.
- Lotação detalhada por gerência, supervisão ou coordenação.
- Remuneração individual, em qualquer forma.
- Empregados de exercícios anteriores ou desligados.

## Success signal

Um cidadão localiza uma pessoa pelo nome, vê o cargo dela, clica no link da estrutura remuneratória e encontra a faixa daquele cargo — sem que a página jamais tenha dito quanto aquela pessoa ganha.

## Assumptions

- A coluna ESTADOS preenchida por bloco significa que as linhas seguintes pertencem ao último estado informado, e não que estejam sem lotação.
- Os 29 registros representam o quadro vigente em 2025.

## Open Questions

- As três correções de digitação precisam de confirmação da FUG antes da publicação: "Servilços Gerais" → "Auxiliar de Serviços Gerais"; "Auxiliar Administrativo Senior" → "Sênior"; "Elaíne Santos deJesus" → "de Jesus".
- A planilha traz "Estagiário" sem distinguir médio e superior, enquanto a estrutura remuneratória separa os dois níveis. Manter genérico na tabela nominal?
- Os cargos "Supervisor Financeiro", "Supervisor de departamento", "Coordenador de Comunicação" e "Coordenadora de Publicidade" são específicos, enquanto a estrutura remuneratória traz apenas "Supervisor" e "Coordenador". Confirmar se são o mesmo cargo com denominação de área.
- A relação com a divergência de efetivo apontada em `spec-estrutura-remuneratoria` (29 aqui contra 35 lá) precisa ser resolvida antes de as duas seções irem ao ar juntas.
