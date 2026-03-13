import React from "react";

export const LiveStrategyCard = ({ id, name, risk, isActive, onSelect }) => {
    return (
        <div 
            onClick={() => onSelect(id)}
            className={`relative overflow-hidden transition-all duration-300 cursor-pointer border px-5 py-4 rounded-2xl ${
                isActive 
                ? "bg-white/[0.07] border-[var(--color-gold)] shadow-[0_0_20px_rgba(195,143,55,0.1)]" 
                : "bg-white/[0.02] border-white/10 hover:border-white/30"
            }`}
        >
            <div className="flex justify-between items-center mb-3">
                <div className="flex items-center gap-2">
                    <div className={`w-1.5 h-1.5 rounded-full ${isActive ? "bg-[var(--color-gold)] animate-pulse" : "bg-white/20"}`}></div>
                    <span className="text-[10px] font-bold text-white/40 uppercase tracking-[0.2em]">Protocol {id}</span>
                </div>
                {isActive && (
                    <span className="text-[9px] font-black text-[var(--color-gold)] uppercase tracking-widest bg-[var(--color-gold)]/10 px-2 py-0.5 rounded-full border border-[var(--color-gold)]/20">
                        Selected
                    </span>
                )}
            </div>

            <h3 className="text-lg font-bold text-white tracking-tight">{name}</h3>
            
            <div className="flex gap-6 mt-4">
                <div className="flex flex-col">
                    <span className="text-[8px] text-white/30 uppercase font-black tracking-tighter">Risk Assessment</span>
                    <span className={`text-[11px] font-bold ${risk === 'Alto' ? 'text-red-500' : 'text-green-500'}`}>
                        {risk.toUpperCase()}
                    </span>
                </div>
                <div className="flex flex-col">
                    <span className="text-[8px] text-white/30 uppercase font-black tracking-tighter">Execution Type</span>
                    <span className="text-[11px] text-white font-mono">DIRECT_MARKET</span>
                </div>
            </div>

            {/* Línea decorativa inferior que se ilumina si está activa */}
            <div className={`absolute bottom-0 left-0 h-[2px] transition-all duration-500 ${isActive ? "w-full bg-[var(--color-gold)]" : "w-0 bg-white/20"}`}></div>
        </div>
    );
};