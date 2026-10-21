export function Footer() {
  return (
    <footer className="bg-background dark:bg-slate-950 w-full pt-6 pb-24 md:pb-6 mt-auto flex flex-col items-center justify-center gap-2 px-8 border-t border-outline-variant/20">
      <div className="text-xs text-[#241918]/40 dark:text-slate-500 font-['Inter']">
        © 2026 Espaço de Integridade.
      </div>
      <div className="flex gap-6">
        <a className="text-sm text-[#241918]/70 hover:text-[#862120] transition-colors" href="#">Privacidade</a>
        <a className="text-sm text-[#241918]/70 hover:text-[#862120] transition-colors" href="#">Termos</a>
        <a className="text-sm text-[#241918]/70 hover:text-[#862120] transition-colors" href="#">Suporte</a>
      </div>
    </footer>
  );
}
