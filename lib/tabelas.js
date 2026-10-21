/** Regras de tools/build_tables.py: escape, VACÂNCIA, CPF e âncoras. */
const CARGO_VAGO = "VACÂNCIA";
const MASCARA_CPF = /^\d{3}\.XXX\.XXX-\d{2}$/;
const TRACO = "\u2014";

const CLS_MOLDURA = "mt-6 overflow-x-auto rounded-lg border border-outline-variant/40 bg-surface-container-lowest";
const CLS_TABELA = "w-full text-left text-sm";
const CLS_CABECALHO = "bg-surface-container text-on-surface-variant";
const CLS_TH = "px-4 py-3 font-semibold whitespace-nowrap";
const CLS_TH_NUM = "px-4 py-3 font-semibold whitespace-nowrap text-right";
const CLS_LINHA = "border-t border-outline-variant/30";
const CLS_LINHA_VAGA = "border-t border-outline-variant/30 bg-surface-container-low";
const CLS_TD = "px-4 py-3 align-top";
const CLS_TD_NUM = "px-4 py-3 align-top text-right tabular-nums";
const CLS_TITULO = "text-xl font-bold text-primary font-headline";
const CLS_LEGENDA = "mt-1 text-sm text-on-surface-variant";
const CLS_LINK = "text-sm font-semibold text-primary hover:underline";
const ID_INDICE_COLEGIADOS = "indice-colegiados";

function esc(valor) {
  const texto = valor == null ? "" : String(valor);
  return texto
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#x27;");
}

function txt(obj, chave) {
  const valor = obj == null ? undefined : obj[chave];
  return valor == null ? "" : valor;
}

function celulaNome(registro) {
  if (registro && registro.vago) {
    return `<em class="text-on-surface-variant">${esc(CARGO_VAGO)}</em>`;
  }
  return esc(txt(registro, "nome"));
}

function sanitizarCpf(cpf) {
  const texto = (cpf == null ? "" : String(cpf)).replaceAll("\u2013", "-");
  return MASCARA_CPF.test(texto) ? texto : TRACO;
}

function cabecalho(colunas) {
  const linhas = [`<thead class="${CLS_CABECALHO}">`, "<tr>"];
  for (const [rotulo, numerica] of colunas) {
    const cls = numerica ? CLS_TH_NUM : CLS_TH;
    linhas.push(`<th class="${cls}" scope="col">${esc(rotulo)}</th>`);
  }
  linhas.push("</tr>", "</thead>");
  return linhas;
}

function linkVoltarIndice() {
  return `<a class="${CLS_LINK}" href="#${ID_INDICE_COLEGIADOS}">Voltar ao índice</a>`;
}

function blocoDiretorias(dados) {
  const colunas = [["Unidade", false], ["Cargo", false], ["Nome", false], ["CPF", false]];
  const colegiados = (dados && dados.colegiados) || [];
  const linhas = ['<div class="mt-8 space-y-12">'];
  linhas.push(
    `<nav id="${ID_INDICE_COLEGIADOS}" tabindex="-1" aria-label="Colegiados desta seção" class="flex flex-col gap-2 sm:flex-row sm:flex-wrap sm:gap-x-6">`,
  );
  for (const colegiado of colegiados) {
    const idTitulo = `titulo-colegiado-${txt(colegiado, "id")}`;
    linhas.push(`<a class="${CLS_LINK}" href="#${esc(idTitulo)}">${esc(txt(colegiado, "nome"))}</a>`);
  }
  linhas.push("</nav>");
  for (const colegiado of colegiados) {
    const nome = txt(colegiado, "nome");
    const idTitulo = `titulo-colegiado-${txt(colegiado, "id")}`;
    linhas.push(
      `<section aria-labelledby="${esc(idTitulo)}">`,
      `<h3 class="${CLS_TITULO}" id="${esc(idTitulo)}">${esc(nome)}</h3>`,
      `<p class="${CLS_LEGENDA}">${esc(txt(colegiado, "total"))} registros.</p>`,
      `<div class="${CLS_MOLDURA}">`,
      `<table class="${CLS_TABELA}">`,
      `<caption class="sr-only">${esc(nome)}: unidade de representação, cargo, nome e CPF parcial de cada integrante.</caption>`,
    );
    linhas.push(...cabecalho(colunas));
    linhas.push("<tbody>");
    for (const registro of (colegiado && colegiado.registros) || []) {
      const cls = registro && registro.vago ? CLS_LINHA_VAGA : CLS_LINHA;
      const vago = registro && registro.vago ? ' data-vago="true"' : "";
      linhas.push(
        `<tr class="${cls}"${vago}>`,
        `<td class="${CLS_TD}">${esc(txt(registro, "unidade"))}</td>`,
        `<td class="${CLS_TD}">${esc(txt(registro, "cargo"))}</td>`,
        `<td class="${CLS_TD}">${celulaNome(registro)}</td>`,
        `<td class="${CLS_TD} whitespace-nowrap">${esc(sanitizarCpf(txt(registro, "cpf")))}</td>`,
        "</tr>",
      );
    }
    linhas.push(
      "</tbody>",
      "</table>",
      "</div>",
      `<p class="mt-8">${linkVoltarIndice()}</p>`,
      "</section>",
    );
  }
  linhas.push("</div>");
  return linhas.join("\n");
}

function blocoCorpoFuncional(dados) {
  const colunas = [["Nome", false], ["Cargo", false], ["Unidade", false]];
  const registros = (dados && dados.registros) || [];
  const linhas = [
    `<p class="${CLS_LEGENDA}">${esc(txt(dados, "total"))} registros.</p>`,
    `<div class="${CLS_MOLDURA}">`,
    `<table class="${CLS_TABELA}">`,
    '<caption class="sr-only">Corpo funcional: nome, cargo e unidade de representação de cada empregado.</caption>',
  ];
  linhas.push(...cabecalho(colunas));
  linhas.push("<tbody>");
  for (const registro of registros) {
    linhas.push(
      `<tr class="${CLS_LINHA}">`,
      `<td class="${CLS_TD}">${celulaNome(registro)}</td>`,
      `<td class="${CLS_TD}">${esc(txt(registro, "cargo"))}</td>`,
      `<td class="${CLS_TD}">${esc(txt(registro, "unidade"))}</td>`,
      "</tr>",
    );
  }
  linhas.push("</tbody>", "</table>", "</div>");
  return linhas.join("\n");
}

function blocoEstruturaRemuneratoria(dados) {
  const colunas = [
    ["Cargo", false],
    ["Nível", true],
    ["Vagas previstas", true],
    ["Vagas preenchidas", true],
    ["Salário base", true],
    ["Faixa média", true],
    ["Faixa máxima", true],
    ["Adicionais", false],
  ];
  const cargos = (dados && dados.cargos) || [];
  const linhas = [
    `<p class="${CLS_LEGENDA}">Valores transcritos da planilha oficial, sem qualquer cálculo.</p>`,
    `<div class="${CLS_MOLDURA}">`,
    `<table class="${CLS_TABELA}">`,
    '<caption class="sr-only">Estrutura remuneratória: cargo, nível, vagas previstas e preenchidas, salário base, faixas média e máxima e adicionais.</caption>',
  ];
  linhas.push(...cabecalho(colunas));
  linhas.push("<tbody>");
  for (const cargo of cargos) {
    linhas.push(
      `<tr class="${CLS_LINHA}">`,
      `<th class="${CLS_TD} font-medium" scope="row">${esc(txt(cargo, "cargo"))}</th>`,
      `<td class="${CLS_TD_NUM}">${esc(txt(cargo, "nivel"))}</td>`,
      `<td class="${CLS_TD_NUM}">${esc(txt(cargo, "quadro_total"))}</td>`,
      `<td class="${CLS_TD_NUM}">${esc(txt(cargo, "quadro_preenchido"))}</td>`,
      `<td class="${CLS_TD_NUM} whitespace-nowrap">${esc(txt(cargo, "salario_base"))}</td>`,
      `<td class="${CLS_TD_NUM} whitespace-nowrap">${esc(txt(cargo, "faixa_media"))}</td>`,
      `<td class="${CLS_TD_NUM} whitespace-nowrap">${esc(txt(cargo, "faixa_maxima"))}</td>`,
      `<td class="${CLS_TD}">${esc(txt(cargo, "adicionais"))}</td>`,
      "</tr>",
    );
  }
  linhas.push("</tbody>", "</table>", "</div>");
  return linhas.join("\n");
}

module.exports = {
  blocoDiretorias,
  blocoCorpoFuncional,
  blocoEstruturaRemuneratoria,
};
