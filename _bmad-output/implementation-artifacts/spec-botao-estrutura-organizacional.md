---
title: 'Botão da home leva à página de estrutura organizacional'
type: 'feature'
created: '2026-09-15'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** O cartão "Estrutura Organizacional" da home é um botão que, no clique, só exibe "em desenvolvimento". A página `estrutura-organizacional/index.html` já publica o conteúdo oficial, mas o cidadão não chega nela a partir da home.

**Approach:** Trocar esse único controle por um link estático para a página da estrutura, na mesma aba, sem overlay de "em desenvolvimento". Os demais cartões da home permanecem como estão.

</frozen-after-approval>

## Implementation Notes

- Alvo: `index.html` L63–77. Hoje é `<button type="button" class="js-dev-button">` com `.js-btn-content` + overlay "em desenvolvimento". O script L168–186 só age em `.js-dev-button`; ao remover a classe deste cartão, o script dos outros quatro cartões segue intacto.
- Destino: `estrutura-organizacional/index.html` (mesmo padrão relativo inverso de `href="../index.html"` na página destino). Sem hash, sem `target="_blank"`.
- Elemento: `<a href="estrutura-organizacional/index.html">` com as classes visuais do cartão (`relative overflow-hidden w-full h-full flex items-center bg-[#862120] ...`). Sem `js-dev-button`, sem overlay, sem `.js-btn-content`. Manter ícone `account_tree` e o rótulo "Estrutura Organizacional".
- Não alterar os cartões Governança / Editais / os outros dois, o nav do header, o rodapé, `estrutura-organizacional/index.html`, CSS, nem o `<script>` da home.
- Teste no padrão de `tools/test_abas.py`: ler o `index.html` publicado. Travar (1) um `<a href="estrutura-organizacional/index.html">` cujo texto visível contém "Estrutura Organizacional"; (2) que esse âncora não tenha `js-dev-button` nem o texto "em desenvolvimento". Escrever o teste antes da edição do HTML.
- `tools/test_home_estrutura.py` escrito primeiro (vermelho no `<button>`). `index.html` L63–74 viraram o `<a>` sem overlay. `python -m pytest tools/test_home_estrutura.py -q` verde. CSS não regenerado: classes já existiam nos outros cartões.
- Recorte do teste usa o comentário `<!-- Estrutura Organizacional -->` até `<!-- Editais -->`, o mesmo âncora HTML que o arquivo já tinha.
- Revisão: o teste passou a parsear o `<a>` (texto visível, href exato, sem `target`, destino existe, sem classes de overlay). No cartão: `aria-hidden` no ícone, remoção de `overflow-hidden` e de `group`.

## Review Triage Log

- Teste `"Estrutura Organizacional" in cartao` casa o comentário HTML — medium; o recorte inclui o comentário; o teste agora parseia o inner do `<a>`.
- Destino em disco não era assertado — medium; `DESTINO.is_file()` no padrão de `test_exportacao_xlsx.py`.
- `target="_blank"` passaria no regex — medium; assert `target=` ausente nos attrs do `<a>`.
- Overlay podia voltar com outro texto; ícone `account_tree` não travado — medium no overlay (`js-btn-overlay`/`js-btn-content`); low no nome do ícone (acoplamento a ligature), rejeitado.
- Ícone sem `aria-hidden` — medium; a página destino já esconde `material-symbols-outlined` em links reais; patch no span.
- Foco teclado cortado por `overflow-hidden` — medium; a classe era do overlay. Removida. Sem classes Tailwind novas (evita regenerar CSS).
- `group` e wrapper interno sobrando — low; `group` removido (só servia o overlay). Inner `flex` mantido para paridade visual com os outros cartões.
- Teste não trava os outros quatro `.js-dev-button` — false/out of scope; esta mudança não os toca.
- Spec ainda `in-progress` — false; o finalize do oneshot é que marca `done`.
