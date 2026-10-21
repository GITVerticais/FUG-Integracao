# Fases

Cada fase termina com o site atual ainda no ar ou já substituído por completo. Os dois não ficam publicados ao mesmo tempo no endereço final. A fase 1 não espera o que ainda está com a FUG.

## Fase 0 — Preparar o app sem apagar o HTML

Saída: `next dev` sobe, o layout usa a paleta atual, e os HTML existentes continuam abrindo como hoje.

1. Acrescentar Next.js, React e React DOM.
2. Criar o layout com cabeçalho e rodapé extraídos do início, já com Denúncias em `/ouvidoria`. A rota pode existir vazia nesta fase.
3. Apontar o `content` do Tailwind para `app/` e `components/`.
4. O build copia `downloads/` para `public/downloads/`. A fonte oficial continua na raiz.
5. Registrar variáveis de ambiente de exemplo, sem valores secretos: `DATABASE_URL`, token de escrita do Vercel Blob, segredo de sessão, chaves do reCAPTCHA.

## Fase 1 — Trazer as três páginas

Saída: início, governança e estrutura no Next mostram o mesmo conteúdo, os downloads funcionam, e as travas de conteúdo passam na página nova.

1. Home com a grade de seis cartões. Governança, Estrutura e Ouvidoria são links. Editais, Dados Contábeis e FAQ seguem em desenvolvimento. FAQ deixa de ficar sozinho e centralizado.
2. Governança com os mesmos PDFs.
3. Estrutura lendo `data/*.json`, com `VACÂNCIA`, CPF mascarado e âncoras dos colegiados. As quatro tabelas vêm no HTML da primeira resposta.
4. Abas no componente, na ordem: dirigentes, corpo funcional, estrutura remuneratória, organograma. O cliente só troca o painel visível.
5. Organograma gravado em `public/img/`.
6. Substituir os testes que leem HTML e só então remover os três `index.html` e o script `tabelas`.

Verificação: seis cartões na ordem do SPEC; par FAQ + Ouvidoria na última linha; hover “em desenvolvimento” nos três cartões sem página; abrir Governança e Estrutura; baixar um PDF e uma planilha; abrir cada aba; confirmar cargo vago. Ouvidoria e Denúncias abrem `/ouvidoria`.

## Fase 2 — API e páginas públicas da ouvidoria

Saída: uma manifestação de teste gera protocolo, a consulta por esse protocolo devolve a situação sem dados pessoais no modo anônimo ou restrito, e a estatística mostra só totais.

1. Modelo no Neon: manifestação, anexos no Vercel Blob, situação, resposta publicada, datas.
2. `POST /api/manifestacoes` com validação de servidor, limite de anexo, reCAPTCHA, igualdade dos e-mails e recusa de UF e cidade no anônimo.
3. `GET /api/manifestacoes/[protocolo]` sem campos de identificação. Protocolo Crockford de 16 caracteres. Acima de 30 consultas do mesmo IP em 10 minutos, a consulta é recusada.
4. `GET /api/estatisticas` com filtro `de` e `ate`, e download CSV UTF-8 com BOM.
5. Páginas `/ouvidoria`, `/ouvidoria/nova`, `/ouvidoria/consultar` e `/ouvidoria/estatisticas`. A ouvidoria sai sem bloco de canal. A confirmação mostra o protocolo uma vez, a frase de que a tela não volta e o link para Consultar.
6. Dois arquivos de configuração para área e assunto, id estável e rótulo editável. O conteúdo das listas pode esperar; o formulário em produção não.

Verificação: enviar os quatro tipos; enviar anônimo e confirmar que a consulta não devolve identificação; consultar protocolo inexistente; abrir estatística com período vazio e com período que contém o teste.

## Fase 3 — Fila interna

Saída: uma conta autorizada muda a situação, publica a resposta, e essa resposta aparece na consulta pública. Quem não está autenticado não abre a fila.

1. Login da fila: conta nomeada, e-mail e senha com hash, cookie HttpOnly. Sem cadastro público. Os nomes das contas vêm da FUG antes desta fase.
2. `/ouvidoria/fila` com o relato completo e os anexos.
3. Ação de concluir, gravando a data usada na faixa de tempo.

Verificação: abrir a fila sem login; concluir uma manifestação; ver a resposta na consulta e a faixa de tempo na estatística.

## Fase 4 — Publicar

Saída: o endereço do portal serve o app Next, as URLs antigas respondem, e o formulário grava no banco de produção.

1. Publicar o app na Vercel, com Neon e Vercel Blob privado. O anexo não passa pelo corpo da Function.
2. Segredos só no ambiente de produção.
3. Conferir início, governança, estrutura, envio, consulta e estatística no ambiente publicado.
4. O formulário em produção espera as listas de área e assunto, a base legal, o prazo de retenção e o aviso do formulário.

## O que ainda espera a FUG

A fase 1 não espera lista, canal nem nomes. O mecanismo da fila, o Neon e o Vercel Blob já estão definidos. Antes da fase 3, a FUG indica quais pessoas recebem conta. Antes do formulário em produção, a FUG entrega as listas de área e assunto, a base legal, o prazo de retenção e o aviso do formulário. O texto de horário, telefone e e-mail não trava nada: a página sai sem esse bloco até o texto existir.
