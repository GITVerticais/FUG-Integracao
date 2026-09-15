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
