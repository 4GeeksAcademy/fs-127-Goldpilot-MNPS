import React from "react";
import { StrategiesCard } from "../../../components/strategies/StrategiesCard";

export const StrategiesPage = () => {
    return (
        <div className="flex flex-col gap-8 w-full p-6 animate-fade-in">
            {/* Cabecera estilizada */}
            <div className="pb-6 border-b border-white/[0.05]">
                <h1 className="text-3xl font-bold tracking-tight text-white">
                    Catálogo de <span className="text-[var(--color-gold)]">Protocolos</span>
                </h1>
                <p className="text-gray-400 mt-2 text-sm uppercase tracking-widest font-medium opacity-70">
                    Sistemas de trading algorítmico de alta precisión
                </p>
            </div>

            {/* Aquí vive tu componente dorado que conecta al Backend */}
            <div className="py-4">
                <StrategiesCard />
            </div>

            {/* Footer Informativo */}
            <div className="mt-auto p-6 rounded-3xl border border-white/[0.05] bg-white/[0.02] flex items-center gap-6">
                <div className="text-3xl text-[var(--color-gold)] opacity-50">🛡️</div>
                <div>
                    <h4 className="text-white font-semibold text-sm">Seguridad GoldPilot</h4>
                    <p className="text-xs text-gray-500 mt-1">
                        Todas las estrategias han sido testeadas en entornos reales. Recuerda que el rendimiento pasado no garantiza resultados futuros.
                    </p>
                </div>
            </div>
        </div>
    );
};