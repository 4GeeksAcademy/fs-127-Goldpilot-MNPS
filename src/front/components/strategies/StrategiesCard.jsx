import { useState, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useTranslation } from "react-i18next";

import shieldIcon from "../../../monedas/shield.svg";
import balanzaIcon from "../../../monedas/balanza.svg";
import fireIcon from "../../../monedas/fire.svg";

export const StrategiesCard = () => {
    const { t } = useTranslation();
    const [selected, setSelected] = useState(null);
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null);
    
    const [customBalance, setCustomBalance] = useState(10000);
    const [customStartDate, setCustomStartDate] = useState("2024-01-01");

    const strategies = [
        {
            id: "low",
            name: t("strategies.card.low.name"),
            desc: t("strategies.card.low.desc"),
            icon: shieldIcon,
            stats: { lot: "0.10", risk: "2%" }
        },
        {
            id: "medium",
            name: t("strategies.card.medium.name"),
            desc: t("strategies.card.medium.desc"),
            icon: balanzaIcon,
            stats: { lot: "0.25", risk: "5%" }
        },
        {
            id: "high",
            name: t("strategies.card.high.name"),
            desc: t("strategies.card.high.desc"),
            icon: fireIcon,
            stats: { lot: "0.50", risk: "12%" }
        }
    ];

    const winRate = useMemo(() => {
        if (!results || !results.history || results.history.length === 0) return 0;
        const wins = results.history.filter(t => t.pnl > 0).length;
        return ((wins / results.history.length) * 100).toFixed(1);
    }, [results]);

    const handleActivate = async () => {
        if (!selected) return;
        setLoading(true);
        setResults(null);
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const url = `${baseUrl}/api/backtest/${selected}?balance=${customBalance}&start=${customStartDate}`;
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
        <div className="flex flex-col items-center gap-4 w-full max-w-7xl mx-auto p-4">

            <div className="flex flex-wrap justify-center items-stretch gap-4 w-full">
                {strategies.map((s) => (
                    <motion.div
                        key={s.id}
                        whileHover={{ y: -3 }}
                        onClick={() => { setSelected(s.id); setResults(null); }}
                        className={`relative flex flex-col flex-1 min-w-[280px] max-w-[360px] p-8 rounded-2xl border transition-all duration-500 cursor-pointer overflow-hidden gap-8
                            ${selected === s.id
                                ? "border-[var(--color-gold)] bg-white/10 shadow-[0_0_30px_rgba(195,143,55,0.12)]"
                                : "border-white/10 bg-white/5 hover:border-white/25"}`}
                        style={{ backdropFilter: "blur(20px)", WebkitBackdropFilter: "blur(20px)", minHeight: 340 }}
                    >
                        {selected === s.id && (
                            <div className="absolute top-3 right-3">
                                <div className="w-2 h-2 rounded-full bg-[var(--color-gold)] shadow-[0_0_8px_var(--color-gold)] animate-pulse" />
                            </div>
                        )}

                        {/* Icono centrado */}
                        <div className="flex flex-col items-center text-center gap-6 flex-1 justify-center">
                            <div className="w-20 h-20">
                                <div
                                    className={`w-full h-full transition-all duration-700 ${selected === s.id ? "scale-110" : "scale-100"}`}
                                    style={{
                                        backgroundColor: selected === s.id ? 'var(--color-gold)' : '#6b7280',
                                        maskImage: `url(${s.icon})`,
                                        WebkitMaskImage: `url(${s.icon})`,
                                        maskSize: 'contain',
                                        WebkitMaskSize: 'contain',
                                        maskRepeat: 'no-repeat',
                                        WebkitMaskRepeat: 'no-repeat',
                                        maskPosition: 'center',
                                        WebkitMaskPosition: 'center',
                                        filter: selected === s.id ? 'drop-shadow(0 0 10px rgba(212,175,55,0.5))' : 'none'
                                    }}
                                />
                            </div>
                            <div>
                                <h2 className="text-base font-bold text-white tracking-widest uppercase">{s.name}</h2>
                                <p className="text-gray-400 text-sm leading-relaxed mt-2 max-w-[220px] mx-auto">{s.desc}</p>
                            </div>
                        </div>

                        {/* Stats */}
                        <div className="pt-5 border-t border-white/10 flex justify-around items-center">
                            <div className="flex flex-col items-center gap-1">
                                <span className="text-[10px] text-white/30 uppercase tracking-widest">{t("strategies.card.lots")}</span>
                                <span className="text-white font-semibold">{s.stats.lot}</span>
                            </div>
                            <div className="w-px h-8 bg-white/10" />
                            <div className="flex flex-col items-center gap-1">
                                <span className="text-[10px] text-white/30 uppercase tracking-widest">{t("strategies.card.risk")}</span>
                                <span className="font-semibold" style={{ color: "var(--color-gold)" }}>{s.stats.risk}</span>
                            </div>
                        </div>
                    </motion.div>
                ))}
            </div>

            <div className="w-full flex flex-col items-center mt-4">
                <AnimatePresence mode="wait">
                    {!results && selected && (
                        <motion.div 
                            key="controls"
                            initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, scale: 0.9 }}
                            className="flex flex-col items-center gap-6"
                        >
                            <div className="flex flex-wrap justify-center gap-6 bg-white/5 p-6 rounded-3xl border border-white/10 shadow-2xl">
                                <div className="flex flex-col gap-2">
                                    <label className="text-[10px] text-gray-500 uppercase tracking-widest">{t("strategies.card.initialBalance")}</label>
                                    <input 
                                        type="number" 
                                        value={customBalance}
                                        onChange={(e) => setCustomBalance(e.target.value)}
                                        className="bg-[#0a0a0a] border border-white/10 rounded-xl p-3 text-white text-sm outline-none focus:border-[var(--color-gold)] transition-colors w-36 text-center font-mono"
                                    />
                                </div>
                                <div className="flex flex-col gap-2">
                                    <label className="text-[10px] text-gray-500 uppercase tracking-widest">{t("strategies.card.startDate")}</label>
                                    <input 
                                        type="date" 
                                        value={customStartDate}
                                        min="2020-01-01"
                                        max="2026-03-11"
                                        onChange={(e) => setCustomStartDate(e.target.value)}
                                        className="bg-[#0a0a0a] border border-white/10 rounded-xl p-3 text-gray-300 text-sm outline-none focus:border-[var(--color-gold)] transition-colors w-44 text-center"
                                        style={{ colorScheme: "dark" }}
                                    />
                                </div>
                            </div>

                            <button 
                                onClick={handleActivate}
                                disabled={loading}
                                className="px-12 py-4 rounded-full text-black font-bold text-sm uppercase tracking-[0.2em] transition-all duration-300 shadow-[0_10px_30px_rgba(195,143,55,0.3)] disabled:opacity-50 hover:scale-105 active:scale-95"
                                style={{ background: "var(--gradient-gold)" }}
                            >
                                {loading ? t("strategies.card.analyzing") : `${t("strategies.card.auditButton")} ${selected}`}
                            </button>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>

            <AnimatePresence>
                {results && (
                    <motion.div 
                        initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }}
                        className="w-full max-w-5xl mt-8 flex flex-col gap-6"
                    >
                        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                            <div className="p-6 rounded-3xl bg-white/5 border border-white/10 text-center">
                                <span className="text-[10px] text-gray-500 uppercase tracking-widest">{t("strategies.card.finalBalance")}</span>
                                <div className="text-2xl font-bold text-white mt-2 font-mono">${results.final_balance.toLocaleString()}</div>
                            </div>
                            <div className="p-6 rounded-3xl bg-white/5 border border-[var(--color-gold)] shadow-[0_0_15px_rgba(195,143,55,0.1)] text-center">
                                <span className="text-[10px] text-gray-500 uppercase tracking-widest">{t("strategies.card.profitLoss")}</span>
                                <div className={`text-2xl font-bold mt-2 font-mono ${results.profit_loss >= 0 ? "text-green-400" : "text-red-500"}`}>
                                    {results.profit_loss >= 0 ? "+" : ""}{results.profit_loss.toLocaleString()} USD
                                </div>
                            </div>
                            <div className="p-6 rounded-3xl bg-white/5 border border-white/10 text-center">
                                <span className="text-[10px] text-gray-500 uppercase tracking-widest">{t("strategies.card.winRate")}</span>
                                <div className="text-2xl font-bold text-white mt-2 font-mono">{winRate}%</div>
                            </div>
                            <div className="p-6 rounded-3xl bg-white/5 border border-white/10 text-center">
                                <span className="text-[10px] text-gray-500 uppercase tracking-widest">{t("strategies.card.totalTrades")}</span>
                                <div className="text-2xl font-bold text-white mt-2 font-mono">{results.trades_count}</div>
                            </div>
                        </div>

                        {/* BITÁCORA DE TRADES */}
                        <div className="rounded-[32px] bg-white/5 border border-white/10 overflow-hidden shadow-2xl">
                            <div className="p-6 border-b border-white/10 flex justify-between items-center bg-black/20">
                                <h3 className="text-white font-medium uppercase tracking-widest text-xs">{t("strategies.card.logTitle")}</h3>
                                <button onClick={() => setResults(null)} className="text-[var(--color-gold)] text-[10px] uppercase tracking-wider hover:text-white transition-all">
                                    {t("strategies.card.newAudit")}
                                </button>
                            </div>
                            
                            <div className="max-h-[400px] overflow-y-auto custom-scrollbar">
                                <table className="w-full text-left border-collapse">
                                    <thead className="sticky top-0 bg-[#0a0a0a] border-b border-white/10 text-[10px] text-gray-500 uppercase tracking-widest z-10">
                                        <tr>
                                            <th className="p-4 font-normal">{t("strategies.card.colDate")}</th>
                                            <th className="p-4 font-normal">{t("strategies.card.colDirection")}</th>
                                            <th className="p-4 font-normal">{t("strategies.card.colEntry")}</th>
                                            <th className="p-4 font-normal">{t("strategies.card.colExit")}</th>
                                            <th className="p-4 font-normal text-right">{t("strategies.card.colProfit")}</th>
                                            <th className="p-4 font-normal text-center">{t("strategies.card.colStatus")}</th>
                                        </tr>
                                    </thead>
                                    <tbody className="text-sm">
                                        {results.history.map((trade, i) => (
                                            <tr key={i} className="border-b border-white/5 hover:bg-white/[0.02] transition-colors">
                                                <td className="p-4 text-gray-400 font-mono text-[11px]">{trade.date}</td>
                                                <td className="p-4">
                                                    <span className={`px-2 py-0.5 rounded text-[9px] font-black tracking-tighter ${trade.type === 'BUY' ? 'bg-green-500/10 text-green-400' : 'bg-red-500/10 text-red-400'}`}>
                                                        {trade.type}
                                                    </span>
                                                </td>
                                                <td className="p-4 text-white/80 font-mono">${trade.entry_price}</td>
                                                <td className="p-4 text-gray-500 font-mono">${trade.exit_price}</td>
                                                <td className={`p-4 text-right font-mono font-bold ${trade.profit >= 0 ? "text-green-400" : "text-red-500"}`}>
                                                    {trade.profit >= 0 ? "+" : ""}{trade.profit}
                                                </td>
                                                <td className="p-4 text-center">
                                                    {trade.profit >= 0 ? "🎯" : "💀"}
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