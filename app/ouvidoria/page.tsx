import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Ouvidoria - Espaço de Integridade FUG",
};

export default function Ouvidoria() {
  return (
    <main className="flex-grow" id="conteudo">
      <div className="max-w-7xl mx-auto px-6 py-10 md:py-14">
        <h1 className="text-3xl md:text-4xl font-black text-primary font-headline tracking-tight">Ouvidoria</h1>
      </div>
    </main>
  );
}
