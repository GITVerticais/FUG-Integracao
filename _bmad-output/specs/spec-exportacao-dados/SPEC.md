---
id: SPEC-exportacao-dados
companions: []
sources: []
---

> **Contrato canônico.** Este SPEC e os arquivos em `companions:` são o contrato completo do que construir, testar e validar. Documentos de origem listados no frontmatter servem à rastreabilidade — consulte-os apenas se precisar da narrativa que este contrato omite de propósito.

# Exportação de dados

## Why

**Oportunidade.** Transparência que só se lê na tela obriga quem vai analisar os dados a copiar linha por linha. O portal de referência indicado pelo cliente resolve isso com um botão de salvar por seção, e a expectativa de quem consome dados públicos hoje é exatamente essa: o número que está na página deve sair em planilha sem retrabalho. Como as tabelas já são HTML estático no documento, a exportação pode ser gerada a partir da própria tabela publicada — o que garante, por construção, que o arquivo baixado é idêntico ao que está na tela.

Afeta: imprensa, pesquisadores e órgãos de controle que analisam os dados fora do navegador.

## Capabilities

- **CAP-1**
  - **intent:** O leitor baixa a tabela da seção em XLSX a partir da própria página.
  - **success:** o arquivo gerado abre no Excel e no LibreOffice sem aviso de formato e contém exatamente as linhas e colunas da tabela publicada, cabeçalho incluído.

- **CAP-2**
  - **intent:** A ausência de JavaScript não deixa interface quebrada.
  - **success:** com JS desativado ou com a biblioteca indisponível, o botão de exportação não é renderizado; nenhum controle morto aparece na página.

- **CAP-3**
  - **intent:** Quem prefere o documento oficial chega nele direto.
  - **success:** cada seção oferece link para o arquivo de origem correspondente em `downloads/`.

- **CAP-4**
  - **intent:** A estrutura comporta exercícios futuros sem retrabalho.
  - **success:** o seletor de ano existe e opera sobre uma lista de exercícios; publicado apenas 2025, acrescentar 2026 é acrescentar uma entrada de dados.

## Constraints

- XLSX apenas; ODS fora de escopo por decisão do cliente.
- SheetJS carregado de `cdnjs.cloudflare.com` com versão fixada — nenhum outro CDN é permitido pela política de conteúdo do portal.
- A exportação lê o DOM da tabela publicada; os dados não são duplicados em JSON no cliente.
- O botão é revelado por JavaScript e nunca renderizado pelo HTML estático.
- O arquivo exportado herda as restrições da seção de origem: CPF permanece mascarado, remuneração individual continua ausente.

## Non-goals

- Exportação em ODS, CSV, PDF ou JSON.
- Exportação de recorte filtrado — não há filtro nas tabelas.
- Exportação consolidada de várias seções num único arquivo.
- Publicação de exercícios anteriores a 2025.

## Success signal

Um jornalista clica em exportar na seção de dirigentes, abre o arquivo direto no Excel e começa a analisar — sem conversão, sem limpeza de coluna e sem ter aberto o PDF.

## Assumptions

- O cliente aceita XLSX como equivalente ao ODS praticado no portal de referência.
- A política de conteúdo do portal permite script de `cdnjs.cloudflare.com`.

## Open Questions

- Manter também o link direto para os `.xlsx` originais em `downloads/`, ou oferecer somente a exportação gerada na página?
- O nome do arquivo exportado deve seguir algum padrão institucional (por exemplo `fug-dirigentes-2025.xlsx`)?
- O seletor de ano deve aparecer já com 2025 como única opção, ou ficar oculto até existir um segundo exercício publicado?
