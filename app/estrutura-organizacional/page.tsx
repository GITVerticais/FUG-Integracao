import type { Metadata } from "next";
import Script from "next/script";
import diretorias from "../../data/diretorias.json";
import corpo from "../../data/corpo-funcional.json";
import remuneracao from "../../data/estrutura-remuneratoria.json";
import { blocoDiretorias, blocoCorpoFuncional, blocoEstruturaRemuneratoria } from "../../lib/tabelas.js";

export const metadata: Metadata = {
  title: "Estrutura Organizacional - Espaço de Integridade FUG",
  description: "Dirigentes, órgãos colegiados, corpo funcional e estrutura remuneratória da Fundação Ulysses Guimarães.",
};

const LINK = "inline-flex items-center gap-2 text-sm font-semibold text-primary hover:underline";
const ABA = "aba-link px-4 py-3 font-semibold border-b-2 hover:text-primary transition-colors";

export default function Estrutura() {
  return (
    <main className="flex-grow min-w-0" id="conteudo">
      <div className="max-w-7xl mx-auto px-6 py-10 md:py-14">
        <nav aria-label="Trilha de navegação" className="text-sm text-on-surface-variant mb-6">
          <a className="hover:text-primary" href="/">Início</a>
          <span className="mx-2" aria-hidden="true">/</span>
          <span className="text-on-background font-medium">Estrutura Organizacional</span>
        </nav>
        <h1 className="text-3xl md:text-4xl font-black text-primary font-headline tracking-tight mb-3">Estrutura Organizacional</h1>
        <p className="text-on-surface-variant font-semibold mb-4">Fundação Ulysses Guimarães – FUG</p>
        <p className="text-on-surface-variant leading-relaxed max-w-3xl">Acesse as seções abaixo para conferir os nomes dos dirigentes, dos membros dos órgãos colegiados, do corpo funcional e a estrutura remuneratória da Fundação Ulysses Guimarães.</p>
        <div className="abas">
          <nav aria-label="Seções da estrutura organizacional" className="mt-14 border-b border-outline-variant/40 flex flex-wrap gap-x-2">
            <a className={`${ABA} border-primary text-primary`} href="#diretorias">Dirigentes e Órgãos Colegiados</a>
            <a className={`${ABA} border-transparent text-on-surface-variant`} href="#corpo-funcional">Corpo Funcional</a>
            <a className={`${ABA} border-transparent text-on-surface-variant`} href="#estrutura-remuneratoria">Estrutura Remuneratória</a>
            <a className={`${ABA} border-transparent text-on-surface-variant`} href="#organograma">Organograma geral</a>
          </nav>

          <section aria-labelledby="titulo-diretorias" className="aba-painel pt-10" id="diretorias">
            <h2 className="text-2xl font-bold text-primary font-headline mb-3" id="titulo-diretorias">Dirigentes e Órgãos Colegiados</h2>
            <p className="text-on-surface-variant leading-relaxed max-w-3xl">Relação dos dirigentes e dos membros dos órgãos colegiados da Fundação Ulysses Guimarães, organizada por colegiado e por unidade de representação. Os números de CPF são exibidos de forma parcial, em conformidade com a Lei Geral de Proteção de Dados (Lei nº 13.709/2018).</p>
            <p className="mt-4">
              <a className={LINK} href="/downloads/diretorias-2025.xlsx" download aria-label="Baixar o XLSX oficial de Dirigentes e Órgãos Colegiados">
                <span aria-hidden="true" className="material-symbols-outlined text-base">download</span>Baixar o XLSX oficial
              </a>
            </p>
            <div dangerouslySetInnerHTML={{ __html: blocoDiretorias(diretorias) }} />
          </section>

          <section aria-labelledby="titulo-corpo-funcional" className="aba-painel pt-10" id="corpo-funcional" hidden>
            <h2 className="text-2xl font-bold text-primary font-headline mb-3" id="titulo-corpo-funcional">Corpo Funcional</h2>
            <p className="text-on-surface-variant leading-relaxed max-w-3xl">Relação dos membros do corpo funcional (empregados) da Fundação Ulysses Guimarães, com o respectivo cargo e a unidade de representação em que atuam.</p>
            <p className="mt-4">
              <a className={LINK} href="#estrutura-remuneratoria">Consultar a estrutura remuneratória</a>
            </p>
            <p className="mt-4">
              <a className={LINK} href="/downloads/corpo-funcional-2025.xlsx" download aria-label="Baixar o XLSX oficial do Corpo Funcional">
                <span aria-hidden="true" className="material-symbols-outlined text-base">download</span>Baixar o XLSX oficial
              </a>
            </p>
            <div dangerouslySetInnerHTML={{ __html: blocoCorpoFuncional(corpo) }} />
          </section>

          <section aria-labelledby="titulo-estrutura-remuneratoria" className="aba-painel pt-10" id="estrutura-remuneratoria" hidden>
            <h2 className="text-2xl font-bold text-primary font-headline mb-3" id="titulo-estrutura-remuneratoria">Estrutura Remuneratória</h2>
            <p className="text-on-surface-variant leading-relaxed max-w-3xl">Estrutura remuneratória dos cargos da Fundação Ulysses Guimarães, com o nível hierárquico, o salário base e as faixas média e máxima praticadas, além do quantitativo de vagas previstas e preenchidas em cada cargo.</p>
            <p className="mt-4">
              <a className={LINK} href="/downloads/estrutura-remuneratoria-2026.xlsx" download aria-label="Baixar o XLSX oficial da Estrutura Remuneratória">
                <span aria-hidden="true" className="material-symbols-outlined text-base">download</span>Baixar o XLSX oficial
              </a>
            </p>
            <div dangerouslySetInnerHTML={{ __html: blocoEstruturaRemuneratoria(remuneracao) }} />
          </section>

          <section aria-labelledby="titulo-organograma" className="aba-painel pt-10 organograma-figura" id="organograma" hidden>
            <h2 className="text-2xl font-bold text-primary font-headline mb-3" id="titulo-organograma">Organograma geral</h2>
            <p className="text-on-surface-variant leading-relaxed max-w-3xl">O organograma apresenta a estrutura geral da Fundação Ulysses Guimarães vigente em 2025. A leitura é feita de cima para baixo, em quatro camadas: a <strong>governança voluntária</strong> (Conselho Curador, Conselho Fiscal, Presidência e Diretoria Administrativa), o nível <strong>estratégico</strong> (Secretaria Executiva e Secretaria Executiva Adjunta), o nível <strong>tático</strong> (gerências, procuradoria, supervisões e coordenações) e o nível <strong>operacional</strong> (assistentes, auxiliares, trainees, estagiários e jovens aprendizes). À direita constam as 27 unidades de representação nos estados e no Distrito Federal. Os níveis 1 a 10 indicados à esquerda correspondem aos níveis da <a className="text-primary underline hover:no-underline" href="#estrutura-remuneratoria">estrutura remuneratória</a>.</p>
            <p className="mt-4">
              <a className={LINK} href="/img/organograma-fug-2025.png" target="_blank" rel="noopener">
                <span aria-hidden="true" className="material-symbols-outlined text-base">zoom_in</span>Ver em tamanho real
              </a>
            </p>
            <p className="mt-4">
              <a className={LINK} href="/downloads/organograma-fug-2025.pdf" download aria-label="Baixar o PDF oficial do Organograma geral">
                <span aria-hidden="true" className="material-symbols-outlined text-base">download</span>Baixar o PDF oficial
              </a>
            </p>
            <figure className="mt-8 bg-surface-container-lowest border border-outline-variant/40 rounded-lg overflow-hidden">
              <div className="organograma-figura-scroll">
                <img alt="Organograma geral da Fundação Ulysses Guimarães em 2025, organizado nos níveis de governança voluntária, estratégico, tático e operacional." className="min-w-[900px] w-full" height={1599} src="/img/organograma-fug-2025.svg" width={2611} />
              </div>
            </figure>
          </section>
        </div>
        <Script id="abas-estrutura" strategy="afterInteractive">{`
          function painelDoHash(hash) {
            var id = (hash || "").replace(/^#/, "");
            var el = id && document.getElementById(id);
            if (!el) return null;
            return el.classList.contains("aba-painel") ? el : el.closest(".aba-painel");
          }
          function mostrarPainel(id) {
            document.querySelectorAll(".aba-painel").forEach(function (painel) {
              painel.hidden = painel.id !== id;
            });
            document.querySelectorAll("a.aba-link").forEach(function (aba) {
              var ativa = aba.getAttribute("href") === "#" + id;
              aba.classList.toggle("border-primary", ativa);
              aba.classList.toggle("text-primary", ativa);
              aba.classList.toggle("border-transparent", !ativa);
              aba.classList.toggle("text-on-surface-variant", !ativa);
            });
          }
          function aplicarHash(hash) {
            var painel = painelDoHash(hash);
            if (painel) mostrarPainel(painel.id);
          }
          document.addEventListener("click", function (event) {
            if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
            var link = event.target.closest("a");
            if (!link || !painelDoHash(link.getAttribute("href"))) return;
            aplicarHash(link.getAttribute("href"));
          });
          window.addEventListener("hashchange", function () { aplicarHash(location.hash); });
          aplicarHash(location.hash);
        `}</Script>
      </div>
    </main>
  );
}
