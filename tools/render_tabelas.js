const fs = require("fs");
const path = require("path");
const { blocoDiretorias, blocoCorpoFuncional, blocoEstruturaRemuneratoria } = require("../lib/tabelas");

const SECOES = [
  ["diretorias", "diretorias.json", blocoDiretorias],
  ["corpo-funcional", "corpo-funcional.json", blocoCorpoFuncional],
  ["estrutura-remuneratoria", "estrutura-remuneratoria.json", blocoEstruturaRemuneratoria],
];

function carregar(dir) {
  const saida = {};
  for (const [secao, arquivo, construir] of SECOES) {
    const caminho = path.join(dir, arquivo);
    if (!fs.existsSync(caminho)) {
      throw new Error(
        "Arquivo de dados ausente: " + caminho + ". Rode `npm run dados` para regenerar data/*.json a partir de downloads/.",
      );
    }
    try {
      saida[secao] = construir(JSON.parse(fs.readFileSync(caminho, "utf8")));
    } catch (erro) {
      if (String(erro.message).startsWith("Arquivo de dados ausente:")) throw erro;
      throw new Error("JSON invalido em " + caminho + ": " + erro.message);
    }
  }
  return saida;
}

try {
  process.stdout.write(JSON.stringify(carregar(process.argv[2])));
} catch (erro) {
  console.error("erro: " + erro.message);
  process.exit(1);
}
