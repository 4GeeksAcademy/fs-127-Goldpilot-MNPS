import React from "react";
import { StrategiesCard } from "../../../components/strategies/StrategiesCard";
// ❌ Eliminamos la importación de BotControlPage

export const SimulationPage = () => {
    return (
        <div className="flex flex-col gap-12 w-full p-4 animate-fade-in">
            {/* --- CABECERA --- */}
            <div className="pb-6 border-b border-white/[0.05]">
                <h1 className="text-3xl font-bold tracking-tight text-white">
                    Laboratorio de <span className="text-[var(--color-gold)]">Simulación</span>
                </h1>
                <p className="text-gray-400 mt-2">
                    Analiza el rendimiento histórico de los protocolos. Pon a prueba las estrategias mediante backtesting sin riesgo.
                </p>
            </div>

            {/* --- SECCIÓN 1: SIMULADOR DE ESTRATEGIAS --- */}
            <section className="space-y-6">
                <div className="flex items-center gap-3">
                    <span className="text-2xl">⎔</span>
                    <h2 className="text-xl font-semibold text-white">Simulador de Protocolos (Backtest)</h2>
                </div>
                <div className="bg-white/[0.02] rounded-[32px] p-2 border border-white/[0.05]">
                    {/* Aquí se cargarán las gráficas e info de simulación */}
                    <StrategiesCard />
                </div>
            </section>

            {/* ❌ SE ELIMINÓ LA SECCIÓN 2: CONTROL OPERATIVO (BOT) */}

            {/* --- FOOTER DE AVISO LEGAL/SIMULACIÓN --- */}
            <div className="p-6 rounded-2xl bg-[var(--color-gold)]/5 border border-[var(--color-gold)]/10 text-center">
                <p className="text-xs text-[var(--color-gold)]/60 italic uppercase tracking-widest">
                    Aviso: Los resultados de las simulaciones se basan en datos históricos del mercado y no garantizan rendimientos futuros.
                </p>
            </div>
        </div>
    );
};
