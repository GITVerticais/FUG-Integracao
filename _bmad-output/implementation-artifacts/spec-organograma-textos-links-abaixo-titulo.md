---
title: 'Textos e links do organograma abaixo do título, no padrão das tabelas'
type: 'feature'
created: '2026-09-16'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** No painel Organograma geral, o texto explicativo e os links (PNG em tamanho real e PDF oficial) ficam na `figcaption` abaixo da figura. Nas demais abas, o parágrafo de intro e os downloads vêm logo abaixo do `h2`, antes do conteúdo.

**Approach:** Reordenar o painel para título → texto → links → figura, reusando o copy e os hrefs atuais e as classes das outras seções. A figura permanece só com a imagem; o `alt` continua sendo a alternativa textual.

</frozen-after-approval>

## Implementation Notes

- Painel `#organograma`: `h2` (`mb-3`) → parágrafo introdutório (`max-w-3xl`) → dois `p.mt-4` (PNG e PDF) → `figure` só com a imagem (`mt-8`, sem `figcaption`). Copy e hrefs reusados; `aria-label` no PDF no padrão das outras abas.
- Ícone do PDF oficial trocado de `picture_as_pdf` para `download`, igual às outras abas.
- `tools/test_abas.py`: trava a ordem título → intro (`p.max-w-3xl`) → hrefs PNG/PDF → figura; `download` + `aria-label` do PDF; `img` com `alt` dentro da `figure`; ausência de `figcaption`, `<p>` e `<a>` na figura.

## Review Triage Log

- Teste não trava `alt`/`img` na figura — **low**, agrupado com o contrato incompleto do teste novo; patch: assertivas de `img[alt]`, figura sem `<p>`/`<a>`, `download` e `aria-label` do PDF.
- Teste não trava “figura só com a imagem” — **low**, mesma causa; patch acima.
- Checagem de ordem por substring frouxa — **low**; patch parcial (`href` e classe do `p` de intro). Parser HTML estrutural rejeitado: correção maior que o risco.
- Teste não trava `aria-label`/`download` do PDF — **low**, mesma causa; patch acima.
- `figure` sem nome acessível após remover `figcaption` — **low**, rejeitado. A `section` já tem `aria-labelledby="titulo-organograma"` e o `img` tem `alt`; nomear a `figure` repetiria o título.
- `alt` agora repete as quatro camadas do intro — **low**, defer. O intent congelado pede manter o `alt`; encurtar é copy nova.
- Spec oneshot não registra override de CAP-2/CAP-4 do SPEC-organograma — **low**, defer. Atualizar o spec canônico sairia do escopo.
- Intro denso atrasa o diagrama no viewport estreito — **false**. O intent pede reusar o copy atual abaixo do título.
- PNG sem `aria-label`, `target="_blank"` sem aviso e href em `assets/img/` — **low**, defer. Pré-existente; só mudou de lugar.
- Ícone `picture_as_pdf` vs `download` das outras abas — **low**, patch: ícone `download`.
