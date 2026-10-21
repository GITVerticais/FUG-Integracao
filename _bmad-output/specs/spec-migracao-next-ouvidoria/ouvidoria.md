# Ouvidoria

Referência de comportamento: e-Ouv público do Sesc-DF (`https://transparencia-df.sesc.com.br/e-ouv`), adaptado à FUG. Confirmação, formato de protocolo e resultado da consulta daquele site não foram observados; o contrato abaixo é o desta versão.

## Páginas

| Rota | O que a pessoa faz |
|---|---|
| `/ouvidoria` | Quatro cartões: denúncia, reclamação, sugestão, elogio. Acessos Consultar e Estatísticas. Sem horário, telefone ou e-mail até a FUG entregar o texto. |
| `/ouvidoria/nova` | Um formulário. O tipo vem da query `tipo`. |
| `/ouvidoria/consultar` | Consulta só por protocolo. O campo do número aparece depois da escolha. |
| `/ouvidoria/estatisticas` | Totais do período, filtro de datas, impressão e download do agregado. Nenhuma linha individual. |
| `/ouvidoria/fila` | Uso interno, com login. Fora do menu público. |

## Formulário

| Campo | Regra |
|---|---|
| tipo | `denuncia`, `reclamacao`, `sugestao`, `elogio` |
| identificação | aberta, restrita ou anônima |
| pessoa | física ou jurídica, quando se identifica |
| nome, documento, e-mail, confirmação de e-mail, telefone | obrigatórios só na aberta ou na restrita; a confirmação tem de ser igual ao e-mail e não é gravada |
| UF, cidade | lista local; cidades filtradas no cliente; no anônimo não são gravadas |
| área, assunto | dois arquivos de configuração, id estável e rótulo editável; listas do Sesc não entram; o conteúdo é o da FUG |
| relato | obrigatório |
| anexos | até 6, 5 MB cada |

No anônimo o bloco de identificação some, os campos pessoais são limpos e nome, documento, e-mail, telefone, UF e cidade não são gravados. O protocolo é emitido. A confirmação mostra o protocolo uma vez, a frase de que ele só aparece nesta tela, o link para Consultar e o aviso de que o acompanhamento anônimo usa esse protocolo. A tela não envia e-mail.

Na restrita, a consulta pública mostra tipo, situação, datas e resposta publicada. Nome e documento ficam só na fila.

Validação no cliente e de novo no servidor. Envio com botão desabilitado e estado de espera. reCAPTCHA no POST.

## API

| Método e caminho | Faz | Devolve |
|---|---|---|
| `POST /api/manifestacoes` | Valida, grava, gera protocolo | Só o protocolo |
| `GET /api/manifestacoes/[protocolo]` | Consulta pública | Tipo, situação, datas e resposta publicada |
| `GET /api/estatisticas?de=&ate=` | Agrega o período | Contagens, sem texto de relato. O download é CSV UTF-8 com BOM: recorte, chave, quantidade |

Situações: `aberto`, `em_andamento`, `concluido`. A resposta publicada entra na consulta. A data de conclusão alimenta a faixa de tempo: até 7, 15, 20, 30 e acima de 30 dias.

O protocolo tem 16 caracteres Crockford (0–9 e A–Z sem I, L, O e U), em grupos de 4. A consulta ignora hífen e maiúsculas e aceita O como 0 e I ou L como 1. Acima de 30 consultas do mesmo IP em 10 minutos, a consulta é recusada. A impressão da estatística é a do navegador.

Estatística pública: quantidade por tipo, situação, área e faixa de tempo. Sem nome, relato ou protocolo.

## Fila

A conta é nomeada: e-mail e senha com hash, sessão em cookie HttpOnly assinado com o segredo de sessão. Não há cadastro público; quem mantém o app cria a conta. Quem está autenticado vê o relato completo, os anexos e a identificação quando ela existir. Pode mudar a situação e publicar a resposta que a consulta pública exibe. Concluir grava a data usada na faixa de tempo. Quem não está autenticado não abre a fila. Relato, identificação e anexo não saem da fila. O registro guarda a data de criação.
