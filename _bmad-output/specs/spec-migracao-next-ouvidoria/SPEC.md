---
id: SPEC-migracao-next-ouvidoria
companions:
  - arquitetura.md
  - ouvidoria.md
  - fases.md
sources:
  - docs/plano-migracao-next-ouvidoria.md
---

> **Contrato canônico.** Este SPEC e os arquivos em `companions:` são o contrato completo do que construir, testar e validar. Documentos de origem listados no frontmatter servem à rastreabilidade — consulte-os apenas se precisar da narrativa que este contrato omite de propósito.

# Espaço de Integridade em Next.js, com ouvidoria

## Why

**Mandato e dor.** O Espaço de Integridade da Fundação Ulysses Guimarães é HTML estático: não há servidor, banco nem formulário que grave dados, e colocar o relato no Git ou num JSON do repositório não atende a ouvidoria. O portal precisa virar um único app que conserve o conteúdo e as URLs públicas de início, governança e estrutura, e que passe a receber manifestação, devolver protocolo, permitir consulta por esse protocolo e publicar só estatísticas agregadas. A referência de comportamento é o e-Ouv público do Sesc-DF, adaptado à FUG. Afeta quem manifesta, quem consulta, a equipe que trata a fila e quem mantém o portal.

## Capabilities

- **CAP-1**
  - **intent:** O visitante abre início, governança e estrutura organizacional nas mesmas URLs públicas, com o mesmo conteúdo.
  - **success:** `/`, `/governanca` e `/estrutura-organizacional` respondem; os links internos entre essas três páginas continuam válidos; um PDF de governança e uma planilha da estrutura baixam; o organograma abre.

- **CAP-2**
  - **intent:** A home apresenta seis cartões, e a ouvidoria é o sexto acesso.
  - **success:** a ordem é Governança (`/governanca`), Estrutura Organizacional (`/estrutura-organizacional`), Editais, Dados Contábeis, FAQ e Ouvidoria (`/ouvidoria`); Governança, Estrutura e Ouvidoria navegam; Editais, Dados Contábeis e FAQ mostram “em desenvolvimento” no hover e não têm página nesta versão; a última linha é FAQ à esquerda e Ouvidoria à direita, sem o FAQ centralizado sozinho.

- **CAP-3**
  - **intent:** O visitante chega à ouvidoria também pelo item Denúncias do cabeçalho e do menu móvel.
  - **success:** Denúncias abre `/ouvidoria`; Políticas e Treinamentos permanecem com o destino de hoje.

- **CAP-4**
  - **intent:** A pessoa registra denúncia, reclamação, sugestão ou elogio e recebe um protocolo.
  - **success:** cada um dos quatro tipos, enviado com relato, devolve só o protocolo; a confirmação mostra esse protocolo uma vez, a frase de que ele só aparece nesta tela e o link para Consultar; no anônimo, a mesma tela traz o aviso de acompanhamento; durante o envio o botão fica desabilitado e a tela mostra espera.

- **CAP-5**
  - **intent:** A pessoa escolhe identificação aberta, restrita ou anônima, e os dados pessoais seguem o modo escolhido.
  - **success:** no anônimo, nome, documento, e-mail, telefone, UF e cidade não são gravados, o protocolo sai mesmo assim e a tela avisa que o acompanhamento é em Consultar; na restrita, a consulta pública mostra tipo, situação, datas e resposta publicada, e nome e documento aparecem só na fila; nome, documento, e-mail, confirmação de e-mail e telefone são obrigatórios só na aberta ou na restrita; a confirmação de e-mail tem de ser igual ao e-mail; pessoa física ou jurídica só quando há identificação.

- **CAP-6**
  - **intent:** A pessoa consulta uma manifestação somente pelo protocolo.
  - **success:** a consulta devolve tipo, situação, datas e resposta publicada; protocolo inexistente não devolve manifestação; CPF e CNPJ não servem de chave; o campo do número só aparece depois que a pessoa escolhe consultar.

- **CAP-7**
  - **intent:** O público vê estatísticas agregadas de um período e pode imprimir ou baixar esse agregado.
  - **success:** o resultado é quantidade por tipo, situação, área e faixa de tempo de resposta (até 7, 15, 20, 30 e acima de 30 dias), com filtro de datas; o download é um CSV UTF-8 com BOM dessas contagens, colunas recorte, chave e quantidade; a impressão é a do navegador; período vazio e período com manifestação de teste devolvem só totais; não há nome, relato, protocolo nem linha individual.

- **CAP-8**
  - **intent:** Uma conta autorizada trata a manifestação e publica a resposta que a consulta pública passa a mostrar.
  - **success:** sem autenticação a fila não abre e não aparece no menu público; entrar exige uma conta nomeada já existente; a conta vê relato completo, anexos e a identificação quando existir, muda a situação e publica a resposta; ao concluir, a data gravada entra na faixa de tempo, e a resposta publicada aparece na consulta.

- **CAP-9**
  - **intent:** O mantenedor atualiza a estrutura a partir das planilhas oficiais, e o visitante vê as mesmas abas e as mesmas regras de tabela.
  - **success:** gerar os JSON a partir das planilhas e abrir a estrutura mostra, nesta ordem, dirigentes, corpo funcional, estrutura remuneratória e organograma; as quatro tabelas estão no HTML da primeira resposta; cargo vago, CPF mascarado, escape e âncoras dos colegiados seguem as regras atuais; as abas trocam o painel visível sem depender de `:target`.

## Constraints

- Um único app Next.js (App Router), com a API em Route Handlers no mesmo app. React desenha as telas; o endpoint é TypeScript de servidor. O app é publicado na Vercel. A Function não tem disco persistente; hospedagem só de arquivo estático não atende.
- Manifestações, respostas e trilha de situação ficam no Neon, Postgres ligado ao projeto na Vercel pela `DATABASE_URL`. Anexos ficam no Vercel Blob com acesso privado, fora do Git e de `public/`.
- O corpo de uma Function na Vercel aceita no máximo 4,5 MB. O anexo não entra nesse corpo: sobe direto ao Vercel Blob, e o POST grava o texto da manifestação e a referência do arquivo.
- `DATABASE_URL`, o token de escrita do Vercel Blob, o segredo de sessão da fila e as chaves do reCAPTCHA no servidor não entram no cliente nem no repositório.
- O POST de manifestação valida de novo no servidor, exige reCAPTCHA e aceita no máximo 6 anexos de 5 MB cada.
- A consulta pública devolve só tipo, situação, datas e resposta publicada. A chave é um protocolo aleatório longo, nunca CPF nem CNPJ.
- As situações da manifestação são `aberto`, `em_andamento` e `concluido`.
- Área e assunto vêm de listas da FUG, em configuração do app, separadas do código do formulário. As listas do Sesc não são reaproveitadas. UF e cidade vêm de lista local, com cidades filtradas no cliente.
- Há um único formulário de manifestação; o tipo é o do cartão escolhido.
- A home mantém duas colunas no desktop, um cartão por linha no celular, fundo `#862120` e rótulo em caixa alta.
- Cores, Inter e raios atuais permanecem. O build do portal é a geração de JSON necessária seguida de `next build`. A página de estrutura deixa de ser HTML injetado; escape e cargo vago continuam as mesmas regras. `npm run dados` continua gerando `data/*.json` quando as planilhas mudam.
- Cabeçalho e rodapé existem numa cópia só, no layout do app.
- O HTML atual permanece intacto até a página Next equivalente estar publicada e coberta por teste do mesmo comportamento. O endereço final não serve os dois ao mesmo tempo.
- A confirmação de e-mail tem de ser igual ao e-mail, sem espaços nas pontas e sem diferença de maiúsculas. Esse campo não é gravado. A confirmação não envia e-mail: mostra o protocolo, a frase de que ele só aparece nesta tela e o link para Consultar.
- No modo anônimo, UF e cidade não são gravadas. Área e assunto continuam.
- O protocolo tem 16 caracteres do alfabeto Crockford (0–9 e A–Z sem I, L, O e U), exibido em grupos de 4, gerado de forma aleatória. A consulta ignora hífen e maiúsculas e aceita O como 0 e I ou L como 1. Acima de 30 consultas do mesmo IP em 10 minutos, a consulta é recusada.
- O download da estatística é CSV UTF-8 com BOM, colunas recorte, chave e quantidade. A impressão é a do navegador.
- As quatro tabelas da estrutura vêm no HTML da primeira resposta. O cliente só troca o painel visível.
- `downloads/` na raiz continua a fonte oficial. O build copia para `public/downloads/`.
- A fila autentica conta nomeada, com e-mail e senha com hash, em cookie HttpOnly assinado com o segredo de sessão. Não há cadastro público: quem mantém o app cria a conta.
- Área e assunto ficam em dois arquivos de configuração, com id estável e rótulo editável, separados do formulário.
- A página da ouvidoria não exibe horário, telefone nem e-mail enquanto a FUG não entregar esse texto.
- Relato, identificação e anexo ficam só na conta da fila. O registro guarda a data de criação. O formulário em produção espera as listas de área e assunto, a base legal, o prazo de retenção e o aviso do formulário. As fases 0 a 3 não esperam esse texto.

## Non-goals

- Busca de manifestação por CPF ou CNPJ.
- Pedido de acesso à informação (e-SIC).
- Intranet do Sesc ou qualquer integração com o e-Ouv do Sesc-DF.
- Gravar manifestação em arquivo do repositório.
- Página própria para Editais, Dados Contábeis ou FAQ nesta versão.
- Copiar a tela de confirmação, o formato do protocolo ou a página de resultado do e-Ouv do Sesc-DF: essas telas não foram observadas.

## Success signal

No endereço publicado do portal, o app responde; `/`, `/governanca` e `/estrutura-organizacional` continuam válidas, com as tabelas da estrutura na primeira resposta; uma manifestação de teste de cada tipo gera protocolo mostrado uma vez; a consulta anônima ou restrita desse protocolo não devolve identificação; a estatística do período mostra só totais e o CSV repete esses totais; uma conta nomeada conclui a manifestação e a resposta aparece na consulta; quem não está autenticado não abre a fila.

## Open Questions

- Quais são as listas de área e de assunto da FUG?
- Qual é o texto oficial de horário, telefone e e-mail, se a FUG quiser exibir o canal?
- Quais pessoas recebem conta da fila?
- Qual é a base legal, o prazo de retenção e o texto do aviso no formulário?
