import React, { useState, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";

export const StrategiesCard = () => {
    const [selected, setSelected] = useState(null);
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null);

    const strategies = [
        { id: "low", name: "LOW RISK", desc: "Correlación inversa Nasdaq/DXY y retest de SMA 50.", icon: "🛡️", stats: { lot: "0.10", risk: "2%" } },
        { id: "medium", name: "MEDIUM RISK", desc: "Retroceso Fibonacci 61.8% y confluencia RSI en H1.", icon: "⚖️", stats: { lot: "0.25", risk: "5%" } },
        { id: "high", name: "HIGH RISK", desc: "Estrategia agresiva de ruptura de rango (Breakout).", icon: "🔥", stats: { lot: "0.50", risk: "12%" } }
    ];

    // Cálculo inteligente del Win Rate
    const winRate = useMemo(() => {
        if (!results || !results.history || results.history.length === 0) return 0;
        const wins = results.history.filter(t => t.profit > 0).length;
        return ((wins / results.history.length) * 100).toFixed(1);
    }, [results]);

    const handleActivate = async () => {
        if (!selected) return;
        
        setLoading(true);
        setResults(null);
        
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const url = `${baseUrl}/api/backtest/${selected}`;

        try {
            const response = await fetch(url);
            const data = await response.json();
            
            if (data.status === "success") {
                setResults(data);
            } else {
                alert("Error en el motor: " + data.error);
            }
        } catch (error) {
            console.error("Error de conexión:", error);
            alert("No se pudo conectar con el motor de backtesting.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col items-center gap-8 w-full max-w-7xl mx-auto p-4 pb-20">
            {/* GRID DE ESTRATEGIAS */}
            <div className="flex flex-wrap justify-center gap-8 w-full">
                {strategies.map((s) => (
                    <motion.div
                        key={s.id}
                        whileHover={{ y: -5 }}
                        onClick={() => { setSelected(s.id); setResults(null); }}
                        className={`relative flex-1 min-w-[300px] max-w-[380px] p-8 rounded-[32px] border transition-all duration-500 cursor-pointer overflow-hidden
                            ${selected === s.id 
                                ? "border-[var(--color-gold)] bg-white/10 shadow-[0_0_30px_rgba(195,143,55,0.2)]" 
                                : "border-white/10 bg-white/5 hover:border-white/30"}`}
                        style={{ backdropFilter: "blur(20px)", WebkitBackdropFilter: "blur(20px)" }}
                    >
                        {selected === s.id && (
                            <div className="absolute top-0 right-0 p-4">
                                <div className="w-2 h-2 rounded-full bg-[var(--color-gold)] shadow-[0_0_10px_var(--color-gold)] animate-pulse" />
                            </div>
                        )}
                        <div className="text-4xl mb-6 opacity-80">{s.icon}</div>
                        <h2 className="text-2xl font-medium text-white mb-4 tracking-tighter">{s.name}</h2>
                        <p className="text-gray-400 text-sm leading-relaxed mb-8 h-12">{s.desc}</p>
                        
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
            </div>

            {/* BOTÓN DE EJECUCIÓN */}
            <div className="w-full flex flex-col items-center mt-4">
                <AnimatePresence mode="wait">
                    {!results && selected && (
                        <motion.button 
                            key="btn"
                            initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, scale: 0.9 }}
                            onClick={handleActivate}
                            disabled={loading}
                            className="px-12 py-4 rounded-full text-black font-bold text-sm uppercase tracking-[0.2em] transition-all duration-300 shadow-[0_0_20px_rgba(195,143,55,0.4)] disabled:opacity-50"
                            style={{ background: "var(--gradient-gold)" }}
                        >
                            {loading ? "Analizando Mercado Histórico..." : `Auditar Estrategia ${selected}`}
                        </motion.button>
                    )}
                </AnimatePresence>
            </div>

            {/* DASHBOARD DE RESULTADOS Y BITÁCORA */}
            <AnimatePresence>
                {results && (
                    <motion.div 
                        initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }}
                        className="w-full max-w-5xl mt-8 flex flex-col gap-6"
                    >
                        {/* MÉTRICAS RÁPIDAS */}
                        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                            <div className="p-6 rounded-2xl bg-white/5 border border-white/10 text-center">
                                <span className="text-[10px] text-gray-500 uppercase tracking-widest">Balance Final</span>
                                <div className="text-2xl font-bold text-white mt-2">${results.final_balance.toLocaleString()}</div>
                            </div>
                            <div className="p-6 rounded-2xl bg-white/5 border border-[var(--color-gold)] shadow-[0_0_15px_rgba(195,143,55,0.1)] text-center">
                                <span className="text-[10px] text-gray-500 uppercase tracking-widest">Profit / Loss</span>
                                <div className={`text-2xl font-bold mt-2 ${results.profit_loss >= 0 ? "text-green-400" : "text-red-500"}`}>
                                    {results.profit_loss >= 0 ? "+" : ""}{results.profit_loss.toLocaleString()} USD
                                </div>
                            </div>
                            <div className="p-6 rounded-2xl bg-white/5 border border-white/10 text-center">
                                <span className="text-[10px] text-gray-500 uppercase tracking-widest">Win Rate</span>
                                <div className="text-2xl font-bold text-white mt-2">{winRate}%</div>
                            </div>
                            <div className="p-6 rounded-2xl bg-white/5 border border-white/10 text-center">
                                <span className="text-[10px] text-gray-500 uppercase tracking-widest">Total Trades</span>
                                <div className="text-2xl font-bold text-white mt-2">{results.trades_count}</div>
                            </div>
                        </div>

                        {/* TABLA DE AUDITORÍA */}
                        <div className="rounded-[24px] bg-white/5 border border-white/10 overflow-hidden">
                            <div className="p-6 border-b border-white/10 flex justify-between items-center bg-black/20">
                                <h3 className="text-white font-medium uppercase tracking-widest text-sm">Bitácora de Vuelo</h3>
                                <button onClick={() => setResults(null)} className="text-[var(--color-gold)] text-[10px] uppercase tracking-wider hover:underline transition-all">
                                    Cerrar Auditoría
                                </button>
                            </div>
                            
                            {/* Contenedor con Scroll */}
                            <div className="max-h-[400px] overflow-y-auto custom-scrollbar">
                                <table className="w-full text-left border-collapse">
                                    <thead className="sticky top-0 bg-[#121212] border-b border-white/10 text-[10px] text-gray-500 uppercase tracking-widest z-10">
                                        <tr>
                                            <th className="p-4 font-normal">Fecha</th>
                                            <th className="p-4 font-normal">Dirección</th>
                                            <th className="p-4 font-normal">Precio Entrada</th>
                                            <th className="p-4 font-normal">Precio Salida</th>
                                            <th className="p-4 font-normal text-right">Beneficio</th>
                                            <th className="p-4 font-normal text-center">Resultado</th>
                                        </tr>
                                    </thead>
                                    <tbody className="text-sm">
                                        {results.history.map((trade, i) => (
                                            <tr key={i} className="border-b border-white/5 hover:bg-white/[0.03] transition-colors">
                                                <td className="p-4 text-gray-400 font-mono text-xs">{trade.date}</td>
                                                <td className="p-4">
                                                    <span className={`px-2 py-1 rounded text-[10px] font-bold tracking-wider ${trade.type === 'BUY' ? 'bg-green-500/10 text-green-400' : 'bg-red-500/10 text-red-400'}`}>
                                                        {trade.type}
                                                    </span>
                                                </td>
                                                <td className="p-4 text-white">${trade.entry_price}</td>
                                                <td className="p-4 text-gray-400">${trade.exit_price}</td>
                                                <td className={`p-4 text-right font-bold ${trade.profit >= 0 ? "text-green-400" : "text-red-500"}`}>
                                                    {trade.profit >= 0 ? "+" : ""}{trade.profit}
                                                </td>
                                                <td className="p-4 text-center">
                                                    {trade.profit >= 0 ? "✅" : "❌"}
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};