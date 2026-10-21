export function Header() {
  return (
    <>
      <header className="bg-[#fff8f7] dark:bg-slate-950 w-full top-0 border-none sticky z-50">
        <div className="flex items-center justify-between px-6 py-4 w-full max-w-7xl mx-auto">
          <div className="text-xl font-bold text-[#862120] dark:text-[#f3dedb] font-['Inter'] tracking-tight">
            Espaço de Integridade
          </div>
          <nav className="hidden md:flex items-center gap-8">
            <a className="text-[#862120] dark:text-[#F29449] border-b-2 border-[#862120] font-semibold font-['Inter'] transition-all" href="/">Início</a>
            <a className="text-[#241918] dark:text-slate-400 hover:bg-[#ffe9e7] dark:hover:bg-slate-800 transition-colors px-2 py-1 rounded" href="/ouvidoria">Denúncias</a>
            <a className="text-[#241918] dark:text-slate-400 hover:bg-[#ffe9e7] dark:hover:bg-slate-800 transition-colors px-2 py-1 rounded" href="#">Políticas</a>
            <a className="text-[#241918] dark:text-slate-400 hover:bg-[#ffe9e7] dark:hover:bg-slate-800 transition-colors px-2 py-1 rounded" href="#">Treinamentos</a>
          </nav>
          <div className="flex items-center gap-4">
            <button className="material-symbols-outlined text-[#862120] dark:text-[#f3dedb] hover:bg-[#ffe9e7] p-2 rounded-full transition-all" type="button">account_circle</button>
          </div>
        </div>
      </header>
      <nav className="md:hidden fixed bottom-0 left-0 w-full flex justify-around items-center py-3 px-4 bg-[#fff8f7]/80 dark:bg-slate-950/80 backdrop-blur-xl shadow-[0px_-4px_20px_rgba(36,25,24,0.06)] z-[60] rounded-t-lg">
        <a className="flex flex-col items-center justify-center text-[#862120] dark:text-[#F29449] font-bold" href="/">
          <span className="material-symbols-outlined">home</span>
          <span className="text-[11px] font-medium uppercase tracking-wider font-['Inter']">Início</span>
        </a>
        <a className="flex flex-col items-center justify-center text-[#241918]/60 dark:text-slate-500 hover:text-[#862120] transition-all" href="/ouvidoria">
          <span className="material-symbols-outlined">campaign</span>
          <span className="text-[11px] font-medium uppercase tracking-wider font-['Inter']">Denúncias</span>
        </a>
        <div className="flex flex-col items-center justify-center text-[#241918]/60 dark:text-slate-500 hover:text-[#862120] transition-all">
          <span className="material-symbols-outlined">policy</span>
          <span className="text-[11px] font-medium uppercase tracking-wider font-['Inter']">Políticas</span>
        </div>
        <div className="flex flex-col items-center justify-center text-[#241918]/60 dark:text-slate-500 hover:text-[#862120] transition-all">
          <span className="material-symbols-outlined">school</span>
          <span className="text-[11px] font-medium uppercase tracking-wider font-['Inter']">Treino</span>
        </div>
      </nav>
    </>
  );
}
