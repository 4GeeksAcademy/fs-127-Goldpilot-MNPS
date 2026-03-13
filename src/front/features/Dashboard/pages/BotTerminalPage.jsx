import React, { useState } from "react";
import { BotControlPage } from "./BotControlPage";
import { LiveStrategyCard } from "../components/LiveStrategyCard";

export const BotTerminalPage = () => {
    const [activeId, setActiveId] = useState(null);

    const liveStrategies = [
        { id: 1, name: "X-Sniper Scalper", risk: "Bajo" },
        { id: 2, name: "Gold Trend Master", risk: "Medio" },
        { id: 3, name: "Volatility Grid", risk: "Alto" }
    ];

    // Encontramos el objeto de la estrategia seleccionada para pasarlo al BotControl
    const selectedStrategy = liveStrategies.find(s => s.id === activeId);

    return (
        <div className="flex flex-col gap-10 w-full p-4 animate-fade-in">
            {/* CABECERA */}
            <div className="flex justify-between items-center pb-6 border-b border-white/[0.05]">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight text-white uppercase italic">
                        Live <span className="text-[var(--color-gold)]">Terminal</span>
                    </h1>
                    <p className="text-gray-400 text-sm mt-1">Gestión de activos y autorización de protocolos en tiempo real.</p>
                </div>
                <div className="flex items-center gap-3 px-4 py-2 rounded-2xl bg-white/[0.03] border border-white/[0.05]">
                    <span className="text-[10px] font-bold text-white/40 uppercase tracking-widest">Auth Status:</span>
                    <span className="text-[10px] font-bold text-green-500 uppercase">Secure</span>
                </div>
            </div>

            {/* SELECTOR DE PROTOCOLOS */}
            <section className="space-y-6">
                <div className="flex items-center gap-4">
                    <h2 className="text-xs font-black text-white/40 uppercase tracking-[0.3em]">Protocol Selection</h2>
                    <div className="flex-1 h-[1px] bg-white/[0.05]"></div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {liveStrategies.map((strat) => (
                        <LiveStrategyCard 
                            key={strat.id}
                            {...strat}
                            isActive={activeId === strat.id}
                            onSelect={setActiveId}
                        />
                    ))}
                </div>
            </section>

            {/* CONSOLA DE MANDO */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
                <div className="lg:col-span-2">
                    <div className="bg-white/[0.02] rounded-[40px] border border-white/[0.05] p-8 shadow-xl">
                        <div className="flex items-center gap-3 mb-10">
                            <div className="w-10 h-10 rounded-full bg-[var(--color-gold)]/5 flex items-center justify-center text-[var(--color-gold)] border border-[var(--color-gold)]/10">
                                ⚡
                            </div>
                            <h2 className="text-xl font-semibold text-white">Consola de Operaciones</h2>
                        </div>
                        
                        {/* 👇 Pasamos la estrategia seleccionada como prop 👇 */}
                        <BotControlPage selectedStrategy={selectedStrategy} />
                    </div>
                </div>

                {/* INFO LATERAL */}
                <div className="flex flex-col gap-6">
                    <div className="p-8 rounded-[40px] bg-white/[0.02] border border-white/[0.05]">
                        <h3 className="text-[10px] font-black text-white/30 uppercase tracking-[0.2em] mb-6">Security Context</h3>
                        <div className="space-y-6 font-mono text-xs">
                            <div className="flex justify-between border-b border-white/[0.03] pb-3">
                                <span className="text-gray-500 text-[10px]">MAX_LOSS_LIMIT</span>
                                <span className="text-white">5.00%</span>
                            </div>
                            <div className="flex justify-between border-b border-white/[0.03] pb-3">
                                <span className="text-gray-500 text-[10px]">EXECUTION_MODE</span>
                                <span className="text-[var(--color-gold)]">INSTANT</span>
                            </div>
                        </div>
                    </div>
                    <div className="px-6 py-4 rounded-2xl bg-white/[0.02] border border-white/[0.05] text-[10px] text-gray-500 italic leading-relaxed">
                        Los cambios de protocolo requieren una validación de margen antes de ser procesados por el motor MetaAPI.
                    </div>
                </div>
            </div>
        </div>
    );
};