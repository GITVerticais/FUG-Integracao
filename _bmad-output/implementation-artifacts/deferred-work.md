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

