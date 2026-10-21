# Arquitetura

## Situação atual

Site em HTML estático, sem servidor, banco ou formulário que grave dados. Cabeçalho e rodapé estão copiados nas três páginas.

| Peça | Onde está | Papel |
|---|---|---|
| Início | `index.html` | Cinco cartões: Governança, Estrutura Organizacional, Editais, Dados Contábeis, FAQ |
| Governança | `governanca/index.html` | PDFs oficiais, com visualizador |
| Estrutura | `estrutura-organizacional/index.html` | Abas, tabelas e organograma. Tabelas injetadas entre `<!-- BLOCO:<secao>:INICIO -->` e `<!-- BLOCO:<secao>:FIM -->` |
| Estilo | `assets/css/input.css` → `assets/css/main.css` | Tailwind 3. Abas com `:has()` e `:target`, sem JavaScript |
| Tokens | `tailwind.config.js` | Cores, Inter e raios. `content` só varre `*.html` |
| Dados | `data/*.json` | `diretorias.json`, `corpo-funcional.json`, `estrutura-remuneratoria.json` |
| Origem | `downloads/` | Planilhas e PDFs oficiais. `npm run dados` gera os JSON |
| Organograma | `tools/render_organograma.py` | Rasteriza o PDF oficial para `assets/img/` |
| Build | `package.json` | `npm run build` roda dados, tabelas, organograma e CSS |
| Testes | `tools/test_*.py` | Travas de HTML, CSS gerado, JSON e injeção de tabelas |

## App alvo

```text
app/
  layout.tsx                          cabeçalho e rodapé únicos
  page.tsx                            início, seis cartões
  governanca/page.tsx
  estrutura-organizacional/page.tsx
  ouvidoria/page.tsx
  ouvidoria/nova/page.tsx
  ouvidoria/consultar/page.tsx
  ouvidoria/estatisticas/page.tsx
  ouvidoria/fila/page.tsx             uso interno, com login
  api/manifestacoes/route.ts          POST
  api/manifestacoes/[protocolo]/route.ts
  api/estatisticas/route.ts
  api/fila/...                        rotas internas
components/                           Header, Footer, tabelas, formulário
data/                                 JSON atuais, importados pelas páginas
public/downloads/                     PDFs e planilhas publicados
public/img/                           organograma e demais imagens
```

O app é publicado na Vercel. A Function não tem disco persistente e o corpo do request aceita no máximo 4,5 MB, então o anexo sobe direto ao Vercel Blob e o POST guarda só o texto e a referência do arquivo.

Persistência da ouvidoria fora do Git: Neon (Postgres ligado ao projeto pela `DATABASE_URL`) para manifestações, respostas e trilha de situação; Vercel Blob com acesso privado para anexos. Variáveis de exemplo, sem valor secreto: `DATABASE_URL`, token de escrita do Blob, segredo de sessão, chaves do reCAPTCHA. O token de escrita do Blob fica no servidor.

## Páginas que saem do HTML

| Arquivo atual | Destino | Mudança |
|---|---|---|
| `index.html` | `app/page.tsx` | Cinco cartões atuais mais Ouvidoria |
| `governanca/index.html` | `app/governanca/page.tsx` | Mesmos documentos e o visualizador |
| `estrutura-organizacional/index.html` | `app/estrutura-organizacional/page.tsx` | Tabelas a partir de `data/*.json`, as quatro no HTML da primeira resposta. O cliente só troca o painel visível |
| Cabeçalho e rodapé repetidos | `components/Header.tsx`, `components/Footer.tsx` | Uma cópia, usada pelo layout |

Os três HTML saem do ar quando a página Next equivalente estiver publicada e os testes novos cobrirem o mesmo comportamento.

## Estilo, scripts e dados

- Regras de aba (`.abas`, `:has()`, `:target`) saem do CSS global e entram no componente da estrutura. `scroll-padding` e a fonte dos ícones permanecem no CSS base.
- O Next compila o Tailwind. `assets/css/main.css` deixa de ser a folha publicada.
- `tailwind.config.js`: `content` passa a incluir `app/**/*.tsx` e `components/**/*.tsx`.
- `package.json`: entram `next`, `react` e `react-dom`. `css` e `css:watch` saem quando nenhuma página HTML depender deles. `dados` permanece. `tabelas` sai quando a estrutura ler o JSON direto. `organograma` permanece, com saída em `public/img/`. `build` é a geração de dados necessária seguida de `next build`.
- `tools/xlsx_to_json.py` permanece e continua a fonte de `data/*.json`.
- `tools/build_tables.py` para de injetar HTML. Classes, `VACÂNCIA`, máscara de CPF e escape viram componente que consome o mesmo JSON.
- `tools/render_organograma.py` permanece. A saída passa de `assets/img/` para `public/img/`.
- `downloads/` na raiz continua a fonte oficial. O build copia para `public/downloads/`. O conversor continua lendo a raiz.

## Testes que trocam de alvo antes do HTML sair

- `tools/test_home_governanca.py`
- `tools/test_home_estrutura.py`
- `tools/test_footers.py`
- `tools/test_abas.py`
- `tools/test_governanca_docs.py`

`tools/test_xlsx_to_json.py` e `tools/test_exportacao_xlsx.py` continuam, ajustando o caminho publicado se for para `public/`. `tools/test_build_tables.py` continua enquanto a função de geração for usada em teste; quando a tabela for componente, a trava equivalente cobre o render do JSON: cargo vago, CPF mascarado, ordem das abas e links de download.

Permanecem o conteúdo de governança e da estrutura, `data/*.json`, o fluxo planilha → JSON, a paleta e a tipografia, e os PDFs oficiais.
