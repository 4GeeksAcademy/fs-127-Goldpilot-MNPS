import React from "react";
import { StrategiesCard } from "../../../components/strategies/StrategiesCard";
import { BotControlPage } from "./BotControlPage"; // Asegúrate de que la ruta sea correcta

export const StrategiesPage = () => {
    return (
        <div className="flex flex-col gap-12 w-full p-4 animate-fade-in">
            {/* --- CABECERA --- */}
            <div className="pb-6 border-b border-white/[0.05]">
                <h1 className="text-3xl font-bold tracking-tight text-white">
                    Command <span className="text-[var(--color-gold)]">Center</span>
                </h1>
                <p className="text-gray-400 mt-2">
                    Configura tus protocolos de trading y gestiona la ejecución del bot.
                </p>
            </div>

            {/* --- SECCIÓN 1: CATÁLOGO DE ESTRATEGIAS --- */}
            <section className="space-y-6">
                <div className="flex items-center gap-3">
                    <span className="text-2xl">⎔</span>
                    <h2 className="text-xl font-semibold text-white">Protocolos de Inversión</h2>
                </div>
                <div className="bg-white/[0.02] rounded-[32px] p-2 border border-white/[0.05]">
                    <StrategiesCard />
                </div>
            </section>

            {/* --- SECCIÓN 2: CONTROL OPERATIVO --- */}
            <section className="space-y-6 bg-gradient-to-b from-white/[0.03] to-transparent p-8 rounded-[40px] border border-white/[0.05]">
                <div className="flex items-center gap-3 mb-4">
                    <span className="text-2xl">◉</span>
                    <h2 className="text-xl font-semibold text-white">Estado de Ejecución</h2>
                </div>
                
                {/* Aquí inyectamos tu componente de control */}
                <BotControlPage />
            </section>

            {/* --- FOOTER DE SEGURIDAD --- */}
            <div className="p-6 rounded-2xl bg-[var(--color-gold)]/5 border border-[var(--color-gold)]/10 text-center">
                <p className="text-xs text-[var(--color-gold)]/60 italic uppercase tracking-widest">
                    Asegúrate de tener una estrategia seleccionada antes de iniciar el bot.
                </p>
            </div>
        </div>
    );
};