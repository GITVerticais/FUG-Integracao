- source_spec: `c:\Users\murilo verticais\Documents\GitHub\FUG-Integracao\_bmad-output\implementation-artifacts\spec-fundacao-portal.md`
  summary: O SPEC.md de origem ainda lista a migração do `index.html` da raiz para CSS compilado como Non-goal e deixa as Open Questions em aberto.
  evidence: A decisão congelada desta história já migrou a home e fechou as duas perguntas; o contrato canônico em `_bmad-output/specs/spec-fundacao-portal/SPEC.md` não foi atualizado, então uma spec posterior pode ler a proibição antiga.

- source_spec: `c:\Users\murilo verticais\Documents\GitHub\FUG-Integracao\_bmad-output\implementation-artifacts\spec-fundacao-portal.md`
  summary: `tools/render_organograma.py` não entra em `npm run dados` nem em `npm run build`.
  evidence: Trocar o PDF oficial e rodar o comando do mantenedor atualiza JSON e tabelas, mas não o SVG/PNG que a página serve; o script já existia fora do pipeline, esta história só corrigiu o caminho.

- source_spec: `c:\Users\murilo verticais\Documents\GitHub\FUG-Integracao\_bmad-output\implementation-artifacts\spec-fundacao-portal.md`
  summary: Corpo funcional (29) e estrutura remuneratória (35 preenchidos) foram publicados juntos apesar da pergunta bloqueante da spec de remuneração.
  evidence: `_bmad-output/specs/spec-estrutura-remuneratoria/SPEC.md` exige decisão institucional sobre qual número a FUG publica; esta história transcreveu as duas origens sem resolver a divergência.

- source_spec: `c:\Users\murilo verticais\Documents\GitHub\FUG-Integracao\_bmad-output\implementation-artifacts\spec-fundacao-portal.md`
  summary: `tools/render_organograma.py` quebra com exceção não tratada se o PDF faltar, estiver vazio ou `assets/img/` não existir.
  evidence: `pymupdf.open(SRC)` e `doc[0]` não têm guarda; o comportamento é pré-existente — só o caminho relativo foi alterado.

- source_spec: `c:\Users\murilo verticais\Documents\GitHub\FUG-Integracao\_bmad-output\implementation-artifacts\spec-fundacao-portal.md`
  summary: Não há teste automatizado de que, sem hash, as três seções permanecem visíveis com o CSS compilado.
  evidence: `tools/test_build_tables.py` não aplica stylesheet; o Verification da spec trata CAP-4 como passagem manual e o intent deixou CI de fora. Restaurar `.aba-painel:not(:target) { display: none; }` deixaria pytest e `npm run build` verdes.

- source_spec: `c:\Users\murilo verticais\Documents\GitHub\FUG-Integracao\_bmad-output\implementation-artifacts\spec-organograma.md`
  summary: O contrato de aba e scroll do organograma (375 px, quatro painéis, `:target`) pode regredir com pytest verde.
  evidence: `tools/test_render_organograma.py` só exercita a conversão em `tmp_path`; não há harness de browser no repositório. Confere-se hoje no Chrome à mão. Mover `#organograma` para fora de `.abas` deixaria os 8 testes verdes.

- source_spec: `c:\Users\murilo verticais\Documents\GitHub\FUG-Integracao\_bmad-output\implementation-artifacts\spec-organograma.md`
  summary: Tirar `npm run organograma` de `build` não quebra os testes da conversão.
  evidence: Os testes importam o módulo e fazem monkeypatch de `SRC`/`OUT`; nenhum lê `package.json` nem dispara o script npm. O mesmo vale para `tabelas` na spec da fundação.

- source_spec: `c:\Users\murilo verticais\Documents\GitHub\FUG-Integracao\_bmad-output\implementation-artifacts\spec-cpf-maria-rita-ordem-abas.md`
  summary: Os testes de `xlsx_to_json` e `build_tables` não leem `data/diretorias.json` nem o HTML publicado, então CI verde não impede o Conselho Curador da Maria Rita voltar a `—` após um regen parcial.
  evidence: Os testes isolam em `tmp_path` por contrato; esta correção só regenerou os artefatos na sessão. Uma suíte que abra `data/` e `estrutura-organizacional/index.html` travaria as duas linhas publicadas.

- source_spec: `c:\Users\murilo verticais\Documents\GitHub\FUG-Integracao\_bmad-output\implementation-artifacts\spec-exportacao-xlsx-downloads.md`
  summary: SPEC-exportacao-dados e notas de specs done ainda pedem SheetJS / não tocar as tags de exportação do rodapé.
  evidence: CAP-1/CAP-2 e as tags cdnjs continuam no contrato canônico; um agente posterior pode recolocar `xlsx.full.min.js` e `exportar-xlsx.js`.

- source_spec: `c:\Users\murilo verticais\Documents\GitHub\FUG-Integracao\_bmad-output\implementation-artifacts\spec-remover-frase-estrutura-remuneratoria.md`
  summary: `spec-estrutura-remuneratoria.md` (status done) ainda exige as notas CAP-4 com a transcrição do PDF de 2025 e o significado de vagas previstas/preenchidas.
  evidence: Um agente posterior pode recolocar o parágrafo para satisfazer o AC antigo; atualizar aquele spec sairia do escopo desta correção.

- source_spec: `C:\Users\murilo verticais\Documents\GitHub\FUG-Integracao\_bmad-output\implementation-artifacts\spec-indice-colegiados-diretorias.md`
  summary: `html { scroll-behavior: smooth }` não respeita `prefers-reduced-motion`.
  evidence: A regra já existia em `assets/css/input.css` L6–8; o índice só aumenta os saltos in-page. Override `scroll-behavior: auto` no media query não faz parte deste contrato.

- source_spec: `c:\Users\murilo verticais\Documents\GitHub\FUG-Integracao\_bmad-output\implementation-artifacts\spec-organograma-textos-links-abaixo-titulo.md`
  summary: O `alt` do organograma agora repete as quatro camadas que o intro acima da figura já descreve.
  evidence: O intent congelado pede manter o `alt` como alternativa textual; encurtar o texto seria copy nova não pedida.

- source_spec: `c:\Users\murilo verticais\Documents\GitHub\FUG-Integracao\_bmad-output\implementation-artifacts\spec-organograma-textos-links-abaixo-titulo.md`
  summary: SPEC-organograma ainda exige texto abaixo do diagrama (CAP-2) e `figure`/`figcaption` (CAP-4).
  evidence: Esta história moveu o texto para cima do `h2` e removeu a `figcaption`; o contrato canônico em `_bmad-output/specs/spec-organograma/SPEC.md` não foi atualizado.

- source_spec: `c:\Users\murilo verticais\Documents\GitHub\FUG-Integracao\_bmad-output\implementation-artifacts\spec-organograma-textos-links-abaixo-titulo.md`
  summary: O link “Ver em tamanho real” segue sem `aria-label`, abre em nova aba sem aviso e aponta para `assets/img/` em vez de `downloads/`.
  evidence: O markup já era esse na `figcaption`; só mudou de lugar. Corrigir seria acessibilidade/copy além do reorder.

- source_spec: `c:\Users\murilo verticais\Documents\GitHub\FUG-Integracao\_bmad-output\implementation-artifacts\spec-governanca.md`
  summary: `tools/pdf_to_json.py` aborta sem mensagem se o PDF oficial de remuneração faltar ou tiver zero páginas.
  evidence: Pré-existente da EO (`pdf_to_json.py:31`); esta história só entrou via merge.

- source_spec: `c:\Users\murilo verticais\Documents\GitHub\FUG-Integracao\_bmad-output\implementation-artifacts\spec-governanca.md`
  summary: `tools/pdf_to_json.py` pode sobrescrever o JSON com `cargos` vazio se nenhuma linha casar o regex.
  evidence: Pré-existente da EO (`pdf_to_json.py:32-56`); não há guarda `if not cargos`.

- source_spec: `c:\Users\murilo verticais\Documents\GitHub\FUG-Integracao\_bmad-output\implementation-artifacts\spec-governanca.md`
  summary: `tools/xlsx_to_json.py` levanta `FileNotFoundError` se o xlsx oficial não estiver em disco.
  evidence: Pré-existente da EO (`xlsx_to_json.py:94`); o merge não introduziu a guarda.

- source_spec: `c:\Users\murilo verticais\Documents\GitHub\FUG-Integracao\_bmad-output\implementation-artifacts\spec-governanca.md`
  summary: `tools/xlsx_to_json.py` aborta com `ValueError` se a linha da planilha for mais curta que o unpack.
  evidence: Pré-existente da EO (`xlsx_to_json.py:97-122`); falta `if len(linha) < 4: continue`.

- source_spec: `c:\Users\murilo verticais\Documents\GitHub\FUG-Integracao\_bmad-output\implementation-artifacts\spec-governanca.md`
  summary: `tools/render_organograma.py` pode deixar SVG/PNG parciais se o save do pixmap falhar depois do SVG.
  evidence: Pré-existente da EO (`render_organograma.py:19-28`); escrita não é atômica.

- source_spec: `c:\Users\murilo verticais\Documents\GitHub\FUG-Integracao\_bmad-output\implementation-artifacts\spec-governanca.md`
  summary: `html { scroll-behavior: smooth }` ignora `prefers-reduced-motion`.
  evidence: A regra já existia em `assets/css/input.css`; o merge da EO só a trouxe para esta branch.

- source_spec: `c:\Users\murilo verticais\Documents\GitHub\FUG-Integracao\_bmad-output\implementation-artifacts\spec-governanca.md`
  summary: Clique repetido no overlay `js-dev-button` antes de 1500ms deixa o primeiro timeout esconder o overlay ainda ativo.
  evidence: Script pré-existente da home (`index.html:163-178`); esta história não o alterou.

- source_spec: `c:\Users\murilo verticais\Documents\GitHub\FUG-Integracao\_bmad-output\implementation-artifacts\spec-governanca.md`
  summary: `tools/test_pdf_to_json.py` falha em vez de skip se o PDF de remuneração não estiver em `downloads/`.
  evidence: Pré-existente da EO (`test_pdf_to_json.py:68`); não há `pytest.skip` por arquivo ausente.

- source_spec: `c:\Users\murilo verticais\Documents\GitHub\FUG-Integracao\_bmad-output\implementation-artifacts\spec-governanca.md`
  summary: Não está confirmado se o host envia os PDFs de governança com `Content-Disposition` que impeça o iframe.
  evidence: `vercel.json` não declara headers de PDF; Visualizar e Baixar compartilham a mesma URL. Conferir a resposta HTTP de `downloads/*.pdf` em produção.

