import Script from "next/script";

const CARTAO = "relative w-full h-full flex items-center bg-[#862120] text-white px-6 py-6 rounded-[4px] shadow-[0px_4px_12px_rgba(36,25,24,0.1)] hover:scale-[0.98] transition-all active:opacity-80";

export default function Home() {
  return (
    <main
      className="flex-grow flex flex-col items-center justify-center px-6 py-12 relative overflow-hidden"
      style={{ background: "linear-gradient(180deg, #F5F9FF 0%, #E8F0FF 100%)" }}
    >
      <div className="mb-16 text-center max-w-2xl">
        <h1 className="text-5xl font-black text-[#862120] font-headline tracking-tighter mb-4">Integridade FUG</h1>
        <p className="text-on-surface-variant text-lg leading-relaxed">Bem-vindo ao espaço de integridade. Selecione uma das áreas abaixo para prosseguir com suas atividades de conformidade.</p>
      </div>
      <div className="w-full max-w-3xl">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full">
          {/* Governança */}
          <div className="relative flex flex-col items-center">
            <a href="/governanca" className={CARTAO}>
              <div className="flex items-center w-full">
                <div className="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center mr-4 flex-shrink-0">
                  <span className="material-symbols-outlined text-white" aria-hidden="true">groups</span>
                </div>
                <span className="text-base font-semibold tracking-wide uppercase font-['Inter'] text-left">Governança</span>
              </div>
            </a>
          </div>

          {/* Estrutura Organizacional */}
          <div className="relative flex flex-col items-center">
            <a href="/estrutura-organizacional" className={CARTAO}>
              <div className="flex items-center w-full">
                <div className="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center mr-4 flex-shrink-0">
                  <span className="material-symbols-outlined text-white" aria-hidden="true">account_tree</span>
                </div>
                <span className="text-base font-semibold tracking-wide uppercase font-['Inter'] text-left">Estrutura Organizacional</span>
              </div>
            </a>
          </div>

          {/* Editais */}
          <div className="group relative flex flex-col items-center">
            <button type="button" className={`js-dev-button ${CARTAO} overflow-hidden`}>
              <div className="js-btn-content flex items-center w-full transition-opacity duration-300 group-hover:opacity-0">
                <div className="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center mr-4 flex-shrink-0">
                  <span className="material-symbols-outlined text-white">campaign</span>
                </div>
                <span className="text-base font-semibold tracking-wide uppercase font-['Inter'] text-left">Editais</span>
              </div>
              <div className="js-btn-overlay absolute inset-0 flex items-center justify-center bg-black/90 text-white opacity-0 transition-opacity duration-300 group-hover:opacity-100 font-bold uppercase tracking-widest text-sm">
                em desenvolvimento
              </div>
            </button>
          </div>

          {/* Dados Contábeis */}
          <div className="group relative flex flex-col items-center">
            <button type="button" className={`js-dev-button ${CARTAO} overflow-hidden`}>
              <div className="js-btn-content flex items-center w-full transition-opacity duration-300 group-hover:opacity-0">
                <div className="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center mr-4 flex-shrink-0">
                  <span className="material-symbols-outlined text-white">account_balance_wallet</span>
                </div>
                <span className="text-base font-semibold tracking-wide uppercase font-['Inter'] text-left">Dados Contábeis</span>
              </div>
              <div className="js-btn-overlay absolute inset-0 flex items-center justify-center bg-black/90 text-white opacity-0 transition-opacity duration-300 group-hover:opacity-100 font-bold uppercase tracking-widest text-sm">
                em desenvolvimento
              </div>
            </button>
          </div>

          {/* FAQ */}
          <div className="group relative flex flex-col items-center">
            <button type="button" className={`js-dev-button ${CARTAO} overflow-hidden`}>
              <div className="js-btn-content flex items-center w-full transition-opacity duration-300 group-hover:opacity-0">
                <div className="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center mr-4 flex-shrink-0">
                  <span className="material-symbols-outlined text-white">quiz</span>
                </div>
                <span className="text-base font-semibold tracking-wide uppercase font-['Inter'] text-left">FAQ</span>
              </div>
              <div className="js-btn-overlay absolute inset-0 flex items-center justify-center bg-black/90 text-white opacity-0 transition-opacity duration-300 group-hover:opacity-100 font-bold uppercase tracking-widest text-sm">
                em desenvolvimento
              </div>
            </button>
          </div>

          {/* Ouvidoria */}
          <div className="relative flex flex-col items-center">
            <a href="/ouvidoria" className={CARTAO}>
              <div className="flex items-center w-full">
                <div className="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center mr-4 flex-shrink-0">
                  <span className="material-symbols-outlined text-white" aria-hidden="true">hearing</span>
                </div>
                <span className="text-base font-semibold tracking-wide uppercase font-['Inter'] text-left">Ouvidoria</span>
              </div>
            </a>
          </div>
        </div>
      </div>
      <div className="absolute bottom-[-100px] left-[-100px] w-64 h-64 bg-[#862120]/5 rounded-full blur-3xl"></div>
      <div className="absolute top-10 right-[-50px] w-96 h-96 bg-[#944a00]/5 rounded-full blur-3xl"></div>
      <Script id="dev-cards" strategy="afterInteractive">{`
        document.querySelectorAll('.js-dev-button').forEach(button => {
          button.addEventListener('click', function() {
            const content = this.querySelector('.js-btn-content');
            const overlay = this.querySelector('.js-btn-overlay');
            content.classList.add('opacity-0');
            overlay.classList.add('opacity-100');
            setTimeout(() => {
              content.classList.remove('opacity-0');
              overlay.classList.remove('opacity-100');
              overlay.classList.add('opacity-0');
            }, 1500);
          });
        });
      `}</Script>
    </main>
  );
}
