# Plano de migração: Espaço de Integridade em Next.js, com ouvidoria

Documento de requisitos e planejamento para sair do portal estático atual e publicar a mesma informação em um app Next.js, com a ouvidoria no mesmo projeto.

O comportamento de referência da ouvidoria é o e-Ouv público do Sesc-DF (`https://transparencia-df.sesc.com.br/e-ouv`), adaptado à Fundação Ulysses Guimarães. A tela de confirmação, o formato do protocolo e a página de resultado da consulta daquele site não foram observados, porque nenhuma manifestação foi enviada.

## Objetivo

Publicar o Espaço de Integridade como um único app Next.js (App Router):

- início, governança e estrutura organizacional são rotas do mesmo app, com o mesmo conteúdo e as mesmas URLs públicas;
- a home tem seis cartões. A ouvidoria é o sexto e abre `/ouvidoria`;
- a ouvidoria recebe manifestação, devolve protocolo, permite consulta por esse protocolo e publica só estatísticas agregadas;
- a API mora no mesmo app, em Route Handlers (`app/api`). React desenha as telas. O endpoint é TypeScript de servidor, não um componente React.

## Situação atual

O site é HTML estático. Não há servidor, banco nem formulário que grave dados.

| Peça | Onde está | Papel |
|---|---|---|
| Início | `index.html` | Grade de cinco cartões: Governança, Estrutura Organizacional, Editais, Dados Contábeis e FAQ. O FAQ ocupa o centro da última linha porque é o único sem par. |
| Governança | `governanca/index.html` | Documentos oficiais em PDF, com visualizador. |
| Estrutura | `estrutura-organizacional/index.html` | Abas, tabelas e organograma. As tabelas são HTML injetado entre `<!-- BLOCO:<secao>:INICIO -->` e `<!-- BLOCO:<secao>:FIM -->`. |
| Estilo | `assets/css/input.css` → `assets/css/main.css` | Tailwind 3. As abas da estrutura usam `:has()` e `:target`, sem JavaScript. |
| Tokens | `tailwind.config.js` | Cores, Inter e raios. O `content` só varre `*.html`. |
| Dados | `data/*.json` | `diretorias.json`, `corpo-funcional.json`, `estrutura-remuneratoria.json`. |
| Planilhas e PDFs | `downloads/` | Fonte oficial. `npm run dados` gera os JSON. |
| Organograma | `tools/render_organograma.py` | Rasteriza `downloads/organograma-fug-2025.pdf` para `assets/img/`. |
| Build | `package.json` | `npm run build` roda dados, tabelas, organograma e CSS. |
| Testes | `tools/test_*.py` | Travas de HTML, CSS gerado, JSON e injeção de tabelas. |

Cabeçalho e rodapé estão copiados nas três páginas. Um `POST` de manifestação não tem onde ser gravado. Colocar o relato no Git ou num JSON do repositório não atende a ouvidoria.

## Arquitetura alvo

Um app Next.js na raiz do repositório. Hospedagem com runtime Node (o servidor do Next precisa ficar no ar). Hospedagem só de arquivo estático não executa a API.

```text
app/
  layout.tsx                          cabeçalho e rodapé únicos
  page.tsx                            início, com os seis cartões
  governanca/page.tsx
  estrutura-organizacional/page.tsx
  ouvidoria/page.tsx                  cartões dos tipos, consulta e estatísticas
  ouvidoria/nova/page.tsx             formulário
  ouvidoria/consultar/page.tsx
  ouvidoria/estatisticas/page.tsx
  ouvidoria/fila/page.tsx             uso interno, com login
  api/manifestacoes/route.ts          POST
  api/manifestacoes/[protocolo]/route.ts
  api/estatisticas/route.ts
  api/fila/...                        rotas internas
components/                           Header, Footer, tabelas, formulário
data/                                 JSON atuais, importados pelas páginas
public/downloads/                     PDFs e planilhas
public/img/                           organograma e demais imagens
```

Persistência da ouvidoria fica fora do Git:

- Postgres para manifestações, respostas e trilha de situação;
- armazenamento privado para anexos (não a pasta `public/`).

Variáveis de ambiente: URL do banco, segredo de sessão da fila, chave do reCAPTCHA no servidor. Nenhuma delas entra no cliente nem no repositório.

## Requisitos da home

A home é uma rota do app (`app/page.tsx`), no mesmo visual da grade atual: duas colunas no desktop, um cartão por linha no celular, fundo `#862120`, rótulo em caixa alta.

Ordem dos seis cartões:

| # | Rótulo | Destino |
|---|---|---|
| 1 | Governança | `/governanca` |
| 2 | Estrutura Organizacional | `/estrutura-organizacional` |
| 3 | Editais | permanece em desenvolvimento, sem página própria nesta versão |
| 4 | Dados Contábeis | permanece em desenvolvimento, sem página própria nesta versão |
| 5 | FAQ | permanece em desenvolvimento, sem página própria nesta versão |
| 6 | Ouvidoria | `/ouvidoria` |

Com o sexto cartão, a última linha fica completa: FAQ à esquerda e Ouvidoria à direita. Some o tratamento atual do FAQ (`md:col-span-2`, centralizado, meia largura). Editais, Dados Contábeis e FAQ continuam com o aviso “em desenvolvimento” no hover. Ouvidoria é um link, no mesmo padrão de Governança e Estrutura.

O item **Denúncias** do cabeçalho e do menu móvel também aponta para `/ouvidoria`. Políticas e Treinamentos seguem como estão hoje.

## Requisitos da ouvidoria

### Páginas públicas

1. **Ouvidoria** (`/ouvidoria`). Quatro cartões: denúncia, reclamação, sugestão e elogio. Dois acessos adicionais: Consultar e Estatísticas. Texto curto de horário e canal institucional, quando a fundação definir esses dados.
2. **Nova manifestação** (`/ouvidoria/nova`). Um formulário só. O tipo vem do cartão (query `tipo`).
3. **Consulta** (`/ouvidoria/consultar`). Só por protocolo. O campo do número aparece depois que a pessoa escolhe essa opção.
4. **Estatísticas** (`/ouvidoria/estatisticas`). Totais do período, com filtro de datas, impressão e download do agregado. Nenhuma linha de manifestação individual.

### Formulário

Campos:

- tipo: `denuncia`, `reclamacao`, `sugestao`, `elogio`;
- identificação: aberta, restrita ou anônima;
- pessoa física ou jurídica, quando a pessoa se identifica;
- nome, documento, e-mail, confirmação de e-mail e telefone, obrigatórios só na identificação aberta ou restrita;
- UF e cidade, com a lista de cidades filtrada no cliente a partir de uma lista local;
- área da fundação e assunto de integridade, com listas definidas pela FUG (as listas do Sesc não são reaproveitadas);
- relato, obrigatório;
- até 6 anexos, 5 MB cada.

No modo anônimo o bloco de identificação some, os campos pessoais são limpos e nada de nome, documento, e-mail ou telefone é gravado. O protocolo é emitido mesmo assim. Aviso na tela: o acompanhamento anônimo usa esse protocolo em Consultar.

Na identificação restrita, a consulta pública mostra tipo, situação, datas e resposta publicada. Nome e documento ficam só na fila interna.

Validação no cliente e de novo no servidor. Envio com botão desabilitado e estado de espera. reCAPTCHA no `POST`.

### API

| Método e caminho | Faz | Devolve |
|---|---|---|
| `POST /api/manifestacoes` | Valida, grava, gera protocolo | Só o protocolo |
| `GET /api/manifestacoes/[protocolo]` | Consulta pública | Tipo, situação, datas e resposta publicada |
| `GET /api/estatisticas?de=&ate=` | Agrega o período | Contagens, sem texto de relato |

Situações: `aberto`, `em_andamento`, `concluido`. A resposta publicada entra na consulta. A data de conclusão alimenta a faixa de tempo de resposta (até 7, 15, 20, 30 e acima de 30 dias).

O protocolo é um código aleatório longo, mostrado uma vez na confirmação. A consulta não aceita CPF nem CNPJ.

Estatística pública: quantidade por tipo, situação, área e faixa de tempo. Sem nome, relato ou protocolo.

### Fila interna

`/ouvidoria/fila` exige login. Lista o relato completo, os anexos e a identificação quando ela existir. Permite mudar a situação e publicar a resposta que a consulta pública exibe. Esta fila não entra no menu público.

### O que a ouvidoria não faz nesta versão

- busca por CPF ou CNPJ;
- pedido de acesso à informação (e-SIC);
- intranet do Sesc ou qualquer integração com o e-Ouv deles;
- gravação de manifestação em arquivo do repositório.

## Requisitos técnicos da migração

1. As URLs públicas atuais permanecem: `/`, `/governanca`, `/estrutura-organizacional`. Links internos entre início, governança e estrutura continuam válidos.
2. PDFs, planilhas para download e a imagem do organograma continuam acessíveis. Os caminhos novos ficam em `public/`.
3. `npm run dados` continua gerando `data/*.json` a partir das planilhas oficiais. A página de estrutura lê esses JSON. `tools/build_tables.py` deixa de escrever HTML dentro de `estrutura-organizacional/index.html`.
4. As abas da estrutura (dirigentes, corpo funcional, estrutura remuneratória, organograma) continuam utilizáveis sem depender de `:target` no CSS. O estado da aba fica no componente.
5. Cores, Inter e raios do `tailwind.config.js` são os mesmos. O `content` passa a incluir `app/**/*.tsx` e `components/**/*.tsx`.
6. Segredos e anexos não vão para `public/` nem para o Git.
7. O build do site passa a ser `next build`. A geração dos JSON permanece um passo anterior, quando as planilhas mudam.

## O que muda

### Páginas

| Arquivo atual | Destino | Mudança |
|---|---|---|
| `index.html` | `app/page.tsx` | Os cinco cartões atuais, mais Ouvidoria como sexto, em `/ouvidoria`. |
| `governanca/index.html` | `app/governanca/page.tsx` | Mesmos documentos e o visualizador. |
| `estrutura-organizacional/index.html` | `app/estrutura-organizacional/page.tsx` | Tabelas renderizadas a partir de `data/*.json`. Abas em estado do React. |
| Cabeçalho e rodapé repetidos | `components/Header.tsx`, `components/Footer.tsx` | Uma cópia só, usada pelo `app/layout.tsx`. |

Os três HTML saem do ar quando a página Next equivalente estiver publicada e os testes novos cobrirem o mesmo comportamento. Até lá, a fase em curso mantém o HTML antigo intacto.

### Estilo e build

- `assets/css/input.css`: as regras de aba (`.abas`, `:has()`, `:target`) saem do CSS global e entram no componente da estrutura. `scroll-padding` e a fonte dos ícones permanecem no CSS base do app.
- `assets/css/main.css`: o Next compila o Tailwind. O arquivo gerado pelo CLI deixa de ser a folha publicada.
- `tailwind.config.js`: `content` aponta para os arquivos do App Router.
- `package.json`: entram `next`, `react` e `react-dom`. Os scripts `css` e `css:watch` do CLI saem quando nenhuma página HTML depender mais deles. `dados` permanece. `tabelas` sai quando a página de estrutura ler o JSON direto. `organograma` permanece, com saída em `public/img/`. `build` do portal passa a ser a geração de dados necessária seguida de `next build`.

### Dados e scripts Python

| Script | Na versão nova |
|---|---|
| `tools/xlsx_to_json.py` | Permanece. Continua a fonte de `data/*.json`. |
| `tools/build_tables.py` | Para de injetar HTML. A marcação das tabelas (classes, `VACÂNCIA`, máscara de CPF) vira componente React que consome o mesmo JSON. As regras de escape e de cargo vago são as mesmas. |
| `tools/render_organograma.py` | Permanece. A pasta de saída passa de `assets/img/` para `public/img/`. |

`downloads/` pode continuar na raiz como fonte das planilhas, desde que a cópia publicada para o visitante esteja em `public/downloads/`. O script de build copia, ou os arquivos oficiais passam a viver só em `public/downloads/` e o conversor lê de lá. Escolher uma das duas opções na fase 1 e usar só ela.

### Testes

Estes arquivos leem HTML ou `main.css` e precisam de substituto na página React antes do HTML ser removido:

- `tools/test_home_governanca.py`
- `tools/test_home_estrutura.py`
- `tools/test_footers.py`
- `tools/test_abas.py`
- `tools/test_governanca_docs.py`

`tools/test_xlsx_to_json.py` e `tools/test_exportacao_xlsx.py` continuam, ajustando o caminho do arquivo publicado se ele mudar para `public/`. `tools/test_build_tables.py` continua válido enquanto a função de geração for usada em teste; quando a tabela for componente, a trava equivalente cobre o render do JSON (cargo vago, CPF mascarado, ordem das abas, links de download).

### O que permanece

- conteúdo de governança e da estrutura;
- `data/*.json` e o fluxo planilha → JSON;
- paleta e tipografia do `tailwind.config.js`;
- PDFs oficiais.

## Planejamento

Cada fase termina com o site atual ainda no ar ou já substituído por completo. Não há os dois publicados ao mesmo tempo no endereço final.

### Fase 0 — Preparar o app sem apagar o HTML

Critério de saída: `next dev` sobe, o layout usa a paleta atual, e os HTML existentes continuam abrindo como hoje.

1. Acrescentar Next.js, React e React DOM ao `package.json`.
2. Criar `app/layout.tsx` com `Header` e `Footer` extraídos do início, já com Denúncias em `/ouvidoria` (a rota pode existir como página vazia nesta fase).
3. Apontar o `content` do Tailwind para `app/` e `components/`.
4. Definir onde ficam os arquivos de `public/` (cópia no build ou mudança da pasta fonte).
5. Registrar variáveis de ambiente de exemplo, sem valores secretos: `DATABASE_URL`, segredo de sessão, chaves do reCAPTCHA.

### Fase 1 — Trazer as três páginas

Critério de saída: início, governança e estrutura no Next mostram o mesmo conteúdo, os downloads funcionam, e as travas de conteúdo passam na página nova.

1. `app/page.tsx` a partir de `index.html`, com a grade de seis cartões. Governança, Estrutura e Ouvidoria são links. Editais, Dados Contábeis e FAQ seguem marcados em desenvolvimento. FAQ deixa de ficar sozinho e centralizado.
2. `app/governanca/page.tsx` a partir de `governanca/index.html`, com os mesmos PDFs.
3. `app/estrutura-organizacional/page.tsx` lendo `data/*.json`. Componente de tabela com as classes e as regras que hoje estão em `build_tables.py` (`VACÂNCIA`, CPF mascarado, âncoras dos colegiados).
4. Abas da estrutura no componente, com a mesma ordem: dirigentes, corpo funcional, estrutura remuneratória, organograma.
5. `render_organograma.py` grava em `public/img/`.
6. Substituir os testes que leem HTML por testes do render ou do JSON, e só então remover os três `index.html` e o script `tabelas`.

### Fase 2 — API e páginas públicas da ouvidoria

Critério de saída: uma manifestação de teste gera protocolo, a consulta por esse protocolo devolve a situação sem dados pessoais no modo anônimo ou restrito, e a estatística mostra só totais.

1. Modelo no Postgres: manifestação, anexos, situação, resposta publicada, datas.
2. `POST /api/manifestacoes` com validação de servidor, limite de anexo e reCAPTCHA.
3. `GET /api/manifestacoes/[protocolo]` sem campos de identificação na resposta pública.
4. `GET /api/estatisticas` com filtro `de` e `ate`.
5. Páginas `/ouvidoria`, `/ouvidoria/nova`, `/ouvidoria/consultar` e `/ouvidoria/estatisticas`.
6. Listas de área e assunto da FUG em arquivo de configuração do app, separadas do código do formulário.

### Fase 3 — Fila interna

Critério de saída: uma conta autorizada muda a situação, publica a resposta, e essa resposta aparece na consulta pública. Quem não está autenticado não abre a fila.

1. Login da fila e sessão.
2. `/ouvidoria/fila` com o relato completo e os anexos.
3. Ação de concluir, gravando a data usada na faixa de tempo da estatística.

### Fase 4 — Publicar

Critério de saída: o endereço do portal serve o app Next, as URLs antigas respondem, e o formulário grava no banco de produção.

1. Hospedagem com Node, Postgres e disco privado de anexos.
2. Segredos só no ambiente de produção.
3. Conferir início, governança, estrutura, envio, consulta e estatística no ambiente publicado.

## Ordem de decisão antes da fase 2

Estas escolhas travam o modelo e a hospedagem. A fase 1 não depende delas.

- Listas de área e de assunto da fundação.
- Texto de horário, telefone e e-mail da ouvidoria, se a página for exibir canal além do formulário.
- Quem acessa a fila interna e como autentica.
- Onde o app e o banco vão rodar.

## Verificação por fase

- Fase 1: na home, conferir os seis cartões na ordem acima, o par FAQ + Ouvidoria na última linha e o hover “em desenvolvimento” nos três cartões sem página; abrir Governança e Estrutura; baixar um PDF e uma planilha; abrir cada aba da estrutura; confirmar cargo vago. O cartão Ouvidoria e o item Denúncias do menu abrem `/ouvidoria`.
- Fase 2: enviar os quatro tipos; enviar anônimo e confirmar que a consulta não devolve identificação; consultar protocolo inexistente; abrir estatística com período vazio e com período que contém o teste.
- Fase 3: abrir a fila sem login; concluir uma manifestação; ver a resposta na consulta e a faixa de tempo na estatística.
