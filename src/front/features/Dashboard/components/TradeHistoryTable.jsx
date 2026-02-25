import React from "react";

/**
 * Tabla de historial de operaciones de trading (XAUUSD).
 * Reemplaza NewsTable con datos reales del modelo Trade del backend.
 * Columnas: Fecha | Símbolo | Tipo | Resultado (P&L)
 * TODO: Conectar con GET /api/dashboard/trades/history cuando el backend esté listo.
 *
 * Esquema de datos basado en el modelo Trade:
 *   symbol, trade_type ('BUY'|'SELL'), profit_loss, opened_at, status
 */
const MOCK_TRADES = [
    { id: 1, symbol: "XAUUSD", trade_type: "BUY", profit_loss: 128.00, opened_at: "2026-02-24T09:15:00", status: "closed" },
    { id: 2, symbol: "XAUUSD", trade_type: "SELL", profit_loss: 114.00, opened_at: "2026-02-24T13:00:00", status: "closed" },
    { id: 3, symbol: "XAUUSD", trade_type: "BUY", profit_loss: -45.00, opened_at: "2026-02-23T10:00:00", status: "closed" },
    { id: 4, symbol: "XAUUSD", trade_type: "SELL", profit_loss: 145.50, opened_at: "2026-02-22T08:30:00", status: "closed" },
    { id: 5, symbol: "XAUUSD", trade_type: "BUY", profit_loss: -35.00, opened_at: "2026-02-21T14:00:00", status: "closed" },
];

/**
 * Formatea una fecha ISO a formato legible: "24 Feb, 09:15"
 * @param {string} isoString - Fecha en formato ISO 8601
 */
const formatDate = (isoString) => {
    const date = new Date(isoString);
    return date.toLocaleDateString("es-ES", { day: "2-digit", month: "short" })
        + ", "
        + date.toLocaleTimeString("es-ES", { hour: "2-digit", minute: "2-digit" });
};

export const TradeHistoryTable = () => {
    return (
        <div className="liquid-glass border border-white/5 rounded-2xl overflow-hidden">
            {/* Cabecera */}
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
                        {MOCK_TRADES.map((trade) => {
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
                        })}
                    </tbody>
                </table>
            </div>
        </div>
    );
};
