import type { Metadata } from "next";
import Script from "next/script";

export const metadata: Metadata = {
  title: "Governança - Espaço de Integridade FUG",
  description: "Documentos oficiais de governança da Fundação Ulysses Guimarães: Regimento Interno, Relatório Escola Movimento 2025, Código de Ética e Estatuto.",
};

const ACAO = "inline-flex items-center gap-2 text-sm font-semibold text-primary hover:underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary";

const DOCUMENTOS = [
  ["Regimento Interno", "regimento-interno.pdf"],
  ["Relatório Escola Movimento 2025", "relatorio-escola-movimento-2025.pdf"],
  ["Código de Ética", "codigo-de-etica.pdf"],
  ["Estatuto", "estatuto.pdf"],
] as const;

export default function Governanca() {
  return (
    <main className="flex-grow min-w-0" id="conteudo">
      <div className="max-w-7xl mx-auto px-6 py-10 md:py-14 min-w-0">
        <nav aria-label="Trilha de navegação" className="text-sm text-on-surface-variant mb-6">
          <a className="hover:text-primary focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary" href="/">Início</a>
          <span className="mx-2" aria-hidden="true">/</span>
          <span className="text-on-background font-medium">Governança</span>
        </nav>
        <h1 className="text-3xl md:text-4xl font-black text-primary font-headline tracking-tight mb-3">Governança</h1>
        <p className="text-on-surface-variant font-semibold mb-4">Fundação Ulysses Guimarães – FUG</p>
        <p className="text-on-surface-variant leading-relaxed max-w-3xl">Consulte os documentos oficiais de governança. Visualize cada PDF nesta página ou baixe o arquivo correspondente.</p>
        <div className="mt-10 grid grid-cols-1 gap-8 min-w-0">
          <ul className="space-y-6 min-w-0">
            {DOCUMENTOS.map(([nome, arquivo]) => (
              <li className="min-w-0" key={arquivo}>
                <article className="rounded-lg border border-outline-variant/40 bg-surface-container-lowest p-5 min-w-0">
                  <h2 className="text-xl font-bold text-primary font-headline mb-4">{nome}</h2>
                  <div className="flex flex-wrap gap-4">
                    <a className={ACAO} href={`/downloads/${arquivo}`} target="visualizador-governanca" aria-label={`Visualizar o PDF oficial do ${nome}`}>
                      <span aria-hidden="true" className="material-symbols-outlined text-base">visibility</span>Visualizar
                    </a>
                    <a className={ACAO} href={`/downloads/${arquivo}`} download aria-label={`Baixar o PDF oficial do ${nome}`}>
                      <span aria-hidden="true" className="material-symbols-outlined text-base">download</span>Baixar
                    </a>
                  </div>
                  <div data-visualizador-host className="min-w-0 w-full"></div>
                </article>
              </li>
            ))}
          </ul>
        </div>
        <iframe hidden id="visualizador-governanca" name="visualizador-governanca" title="Leitura do documento de governança" className="mt-4 w-full min-h-[70vh] min-w-0 max-w-full border border-outline-variant/40 rounded-lg bg-surface-container-lowest"></iframe>
        <Script id="visualizador-governanca-script" strategy="afterInteractive">{`
          document.querySelectorAll('a[target="visualizador-governanca"]').forEach(function (link) {
            link.addEventListener("click", function (event) {
              if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
                return;
              }
              var article = link.closest("article");
              var host = article && article.querySelector("[data-visualizador-host]");
              var viewer = document.getElementById("visualizador-governanca");
              if (!host || !viewer) {
                return;
              }
              event.preventDefault();
              host.appendChild(viewer);
              viewer.hidden = false;
              var heading = article.querySelector("h2");
              if (heading) {
                viewer.title = "Leitura do " + heading.textContent.trim();
              }
              viewer.src = link.getAttribute("href");
              article.scrollIntoView({ block: "start" });
            });
          });
        `}</Script>
      </div>
    </main>
  );
}
