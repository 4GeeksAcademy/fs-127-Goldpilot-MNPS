import React, { useState, useEffect } from "react";
import { getTradeHistory } from "../api";

/**

/**
 * @param {string} isoString - Fecha en formato ISO 8601
 */
const formatDate = (isoString) => {
    if (!isoString) return "–";
    const date = new Date(isoString);
    return date.toLocaleDateString("es-ES", { day: "2-digit", month: "short" })
        + ", "
        + date.toLocaleTimeString("es-ES", { hour: "2-digit", minute: "2-digit" });
};

export const TradeHistoryTable = () => {
    const [trades, setTrades] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        getTradeHistory()
            .then((data) => setTrades((data.trades || []).slice(0, 5)))
            .catch(() => setTrades([]))
            .finally(() => setLoading(false));
    }, []);

    return (
        <div className="liquid-glass border border-white/5 rounded-2xl overflow-hidden">
            <div className="flex items-center justify-between p-5 border-b border-white/5">
                <h2 className="text-sm font-semibold text-white">Operaciones</h2>
                <button className="w-8 h-8 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center text-white/50 hover:text-white hover:bg-white/10 transition-all text-xs">
                    →
                </button>
            </div>

            {/* Tabla */}
            <div className="overflow-x-auto">
                <table className="w-full">
                    <thead>
                        <tr className="text-[10px] font-medium text-white/30 uppercase tracking-wider">
                            <th className="text-left px-5 py-3">Fecha</th>
                            <th className="text-left px-4 py-3">Símbolo</th>
                            <th className="text-left px-4 py-3 hidden sm:table-cell">Tipo</th>
                            <th className="text-right px-5 py-3">Resultado</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-white/[0.03]">
                        {loading ? (
                            <tr>
                                <td colSpan={4} className="text-center py-12 text-xs text-white/20">
                                    Cargando operaciones...
                                </td>
                            </tr>
                        ) : trades.length === 0 ? (
                            <tr>
                                <td colSpan={4} className="text-center py-12 text-xs text-white/20">
                                    Sin operaciones registradas
                                </td>
                            </tr>
                        ) : (
                            trades.map((trade) => {
                                const isProfit = trade.profit_loss >= 0;

                                return (
                                    <tr
                                        key={trade.id}
                                        className="hover:bg-white/[0.02] transition-colors cursor-pointer"
                                    >
                                        {/* Fecha */}
                                        <td className="px-5 py-4">
                                            <span className="text-xs text-white/40">
                                                {formatDate(trade.opened_at)}
                                            </span>
                                        </td>

                                        {/* Símbolo */}
                                        <td className="px-4 py-4">
                                            <div className="flex items-center gap-2">
                                                <div className="w-7 h-7 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center text-xs flex-shrink-0 font-bold"
                                                    style={{ color: "var(--color-gold)" }}>
                                                    Au
                                                </div>
                                                <span className="text-sm font-semibold text-white">
                                                    {trade.symbol}
                                                </span>
                                            </div>
                                        </td>

                                        {/* Tipo (BUY / SELL) */}
                                        <td className="px-4 py-4 hidden sm:table-cell">
                                            <span
                                                className="text-[11px] font-bold px-2.5 py-1 rounded-full"
                                                style={{
                                                    background: trade.trade_type === "BUY"
                                                        ? "rgba(99,119,66,0.15)"
                                                        : "rgba(195,143,55,0.12)",
                                                    color: trade.trade_type === "BUY"
                                                        ? "var(--color-olive)"
                                                        : "var(--color-gold)",
                                                }}
                                            >
                                                {trade.trade_type === "BUY" ? "▲ Compra" : "▼ Venta"}
                                            </span>
                                        </td>

                                        {/* Resultado P&L */}
                                        <td className="px-5 py-4 text-right">
                                            <span
                                                className="text-sm font-bold"
                                                style={{ color: isProfit ? "var(--color-olive)" : "#f87171" }}
                                            >
                                                {isProfit ? "+" : ""}${trade.profit_loss.toFixed(2)}
                                            </span>
                                        </td>
                                    </tr>
                                );
                            })
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};
