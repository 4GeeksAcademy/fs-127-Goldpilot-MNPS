import React, { useState } from "react";
import { motion } from "framer-motion";

export const StrategiesCard = () => {
    const [selected, setSelected] = useState(null);

    const strategies = [
        {
            id: "low",
            name: "LOW RISK",
            desc: "Preservación de capital mediante análisis macroeconómico y baja exposición.",
            icon: "🛡️",
            stats: { lot: "0.10", risk: "2%" }
        },
        {
            id: "med",
            name: "MEDIUM RISK",
            desc: "Equilibrio técnico basado en retrocesos de Fibonacci y liquidez institucional.",
            icon: "⚖️",
            stats: { lot: "0.25", risk: "5%" }
        },
        {
            id: "high",
            name: "HIGH RISK",
            desc: "Estrategia agresiva de acción del precio para maximizar retornos rápidos.",
            icon: "🔥",
            stats: { lot: "0.50", risk: "12%" }
        }
    ];

    // Esta función maneja el clic del botón dorado
    const handleActivate = () => {
        console.log("Protocolo seleccionado:", selected);
        alert(`¡Protocolo ${selected.toUpperCase()} configurado en la interfaz! (Listo para integración con Backend)`);
    };

    return (
        <div className="flex flex-wrap justify-center gap-8 w-full max-w-7xl mx-auto p-4">
            {strategies.map((s) => (
                <motion.div
                    key={s.id}
                    whileHover={{ y: -5 }}
                    onClick={() => setSelected(s.id)}
                    className={`relative flex-1 min-w-[300px] max-w-[380px] p-8 rounded-[32px] border transition-all duration-500 cursor-pointer overflow-hidden
                        ${selected === s.id 
                            ? "border-[var(--color-gold)] bg-white/10 shadow-[0_0_30px_rgba(195,143,55,0.15)]" 
                            : "border-white/10 bg-white/5 hover:border-white/30"}`}
                    style={{ backdropFilter: "blur(20px)", WebkitBackdropFilter: "blur(20px)" }}
                >
                    {selected === s.id && (
                        <div className="absolute top-0 right-0 p-4">
                            <div className="w-2 h-2 rounded-full bg-[var(--color-gold)] shadow-[0_0_10px_var(--color-gold)]" />
                        </div>
                    )}

                    <div className="text-4xl mb-6 opacity-80">{s.icon}</div>
                    
                    <h3 className="text-white font-bold tracking-widest text-xs uppercase mb-2 opacity-60">
                        Estrategia
                    </h3>
                    <h2 className="text-2xl font-medium text-white mb-4 tracking-tighter">
                        {s.name}
                    </h2>
                    
                    <p className="text-gray-400 text-sm leading-relaxed mb-8 h-12">
                        {s.desc}
                    </p>

                    <div className="pt-6 border-t border-white/10 flex justify-between items-center">
                        <div className="flex flex-col">
                            <span className="text-[10px] text-gray-500 uppercase tracking-widest">Lotes</span>
                            <span className="text-white font-medium">{s.stats.lot}</span>
                        </div>
                        <div className="flex flex-col text-right">
                            <span className="text-[10px] text-gray-500 uppercase tracking-widest">Riesgo</span>
                            <span className="text-[var(--color-gold)] font-medium">{s.stats.risk}</span>
                        </div>
                    </div>
                </motion.div>
            ))}

            {selected && (
                <motion.div 
                    initial={{ opacity: 0, y: 20 }} 
                    animate={{ opacity: 1, y: 0 }}
                    className="w-full text-center mt-12"
                >
                    <button 
                        onClick={handleActivate}
                        className="px-12 py-4 rounded-full text-black font-bold text-sm uppercase tracking-[0.2em] transition-all duration-300 transform hover:scale-105 shadow-[0_0_20px_rgba(195,143,55,0.4)]"
                        style={{ background: "var(--gradient-gold)" }}
                    >
                        Activar Protocolo {selected}
                    </button>
                </motion.div>
            )}
        </div>
    );
};