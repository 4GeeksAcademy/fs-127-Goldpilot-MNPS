import React, { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { PortfolioCard } from "../components/PortfolioCard";
import { getTradeHistory } from "../api";

/**
/**
 * @param {string} iso - Fecha en formato ISO 8601
 */
const fmt = (iso) => {
    if (!iso) return "–";
    const d = new Date(iso);
    return d.toLocaleDateString("es-ES", { day: "2-digit", month: "short" })
        + " "
        + d.toLocaleTimeString("es-ES", { hour: "2-digit", minute: "2-digit" });
};

/** Calcula las estadísticas del resumen a partir del array de trades */
const calcStats = (trades) => {
    const totalTrades = trades.length;
    const winning = trades.filter((t) => t.profit_loss > 0).length;
    const totalPnL = trades.reduce((acc, t) => acc + t.profit_loss, 0);
    const winRate = totalTrades > 0 ? (winning / totalTrades) * 100 : 0;
    return { totalTrades, winning, losing: totalTrades - winning, totalPnL, winRate };
};

/**
 * Página principal del Historial de Operaciones.
 * Muestra resumen estadístico + tabla completa de trades cerrados.
 */
export const HistorialPage = () => {
    const { t } = useTranslation();
    const [trades, setTrades] = useState([]);
    const [loading, setLoading] = useState(true);
    const [activeFilter, setActiveFilter] = useState("ALL");

    const FILTERS = [
        { label: t("historial.filterAll"), value: "ALL" },
        { label: t("historial.filterBuy"), value: "BUY" },
        { label: t("historial.filterSell"), value: "SELL" },
    ];

    useEffect(() => {
        getTradeHistory()
            .then((data) => setTrades(data.trades || []))
            .catch(() => setTrades([]))
            .finally(() => setLoading(false));
    }, []);

    const filteredTrades = activeFilter === "ALL"
        ? trades
        : trades.filter((t) => t.trade_type === activeFilter);

    const stats = calcStats(filteredTrades);
    const isProfitable = stats.totalPnL >= 0;

    return (
        <div className="flex flex-col gap-6 w-full">

            {/* Cabecera de la página */}
            <div className="pb-2 border-b border-white/[0.05]">
                <h1 className="text-2xl font-bold tracking-tight text-white">{t("historial.title")}</h1>
                <p className="text-xs text-white/30 mt-1">
                    {t("historial.subtitle")}
                </p>
            </div>

            {/* Resumen estadístico — 3 PortfolioCards */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <PortfolioCard
                    title={t("historial.totalOperations")}
                    value={String(stats.totalTrades)}
                    subtitle={`${stats.winning}G · ${stats.losing}P`}
                    icon="◳"
                    color="blue"
                />
                <PortfolioCard
                    title={t("dashboard.winRate")}
                    value={`${stats.winRate.toFixed(1)}%`}
                    subtitle={t("historial.filteredOperations")}
                    icon="%"
                    color={stats.winRate >= 50 ? "green" : "red"}
                />
                <PortfolioCard
                    title={t("dashboard.totalPnl")}
                    value={`${isProfitable ? "+" : ""}$${stats.totalPnL.toFixed(2)}`}
                    subtitle={t("historial.accumulatedResult")}
                    icon="◬"
                    trend={isProfitable ? "up" : "down"}
                    color={isProfitable ? "green" : "red"}
                />
            </div>

            {/* Tabla de historial completa */}
            <div
                className="rounded-2xl border border-white/[0.06] overflow-hidden"
                style={{ background: "rgba(255,255,255,0.03)", backdropFilter: "blur(16px)" }}
            >
                {/* Cabecera tabla + filtros */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 px-6 py-4 border-b border-white/[0.05]">
                    <h2 className="text-sm font-semibold text-white">{t("historial.closedOperations")}</h2>

                    {/* Filtros BUY / SELL / All */}
                    <div className="flex gap-1 p-1 rounded-xl" style={{ background: "rgba(255,255,255,0.04)" }}>
                        {FILTERS.map(({ label, value }) => (
                            <button
                                key={value}
                                onClick={() => setActiveFilter(value)}
                                className="px-3 py-1.5 rounded-lg text-xs font-semibold transition-all"
                                style={activeFilter === value
                                    ? { background: "rgba(195,143,55,0.15)", color: "var(--color-gold)", border: "1px solid rgba(195,143,55,0.25)" }
                                    : { color: "rgba(255,255,255,0.35)", border: "1px solid transparent" }
                                }
                            >
                                {label}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Tabla */}
                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead>
                            <tr className="text-[10px] font-medium text-white/30 uppercase tracking-wider border-b border-white/[0.04]">
                                <th className="text-left px-5 py-3">{t("historial.entry")}</th>
                                <th className="text-left px-4 py-3">{t("historial.exit")}</th>
                                <th className="text-left px-4 py-3 hidden lg:table-cell">{t("historial.index")}</th>
                                <th className="text-left px-4 py-3">{t("historial.type")}</th>
                                <th className="text-right px-4 py-3 hidden md:table-cell">Lots</th>
                                <th className="text-right px-4 py-3 hidden md:table-cell">SL</th>
                                <th className="text-right px-4 py-3 hidden md:table-cell">TP</th>
                                <th className="text-right px-5 py-3">{t("historial.revenue")}</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-white/[0.03]">
                            {filteredTrades.length === 0 ? (
                                <tr>
                                    <td colSpan={8} className="text-center py-12 text-xs text-white/20">
                                        {t("historial.noTradesForFilter")}
                                    </td>
                                </tr>
                            ) : (
                                filteredTrades.map((trade) => {
                                    const isProfit = trade.profit_loss >= 0;
                                    return (
                                        <tr
                                            key={trade.id}
                                            className="hover:bg-white/[0.02] transition-colors cursor-pointer"
                                        >
                                            {/* Fecha y hora de entrada (opened_at) */}
                                            <td className="px-5 py-4">
                                                <span className="text-xs text-white/50">{fmt(trade.opened_at)}</span>
                                            </td>

                                            {/* Fecha y hora de salida (closed_at) */}
                                            <td className="px-4 py-4">
                                                <span className="text-xs text-white/50">{fmt(trade.closed_at)}</span>
                                            </td>

                                            {/* Índice / meta_trade_id */}
                                            <td className="px-4 py-4 hidden lg:table-cell">
                                                <span className="text-[11px] font-mono text-white/30">{trade.meta_trade_id}</span>
                                            </td>

                                            {/* Tipo de operación (trade_type) */}
                                            <td className="px-4 py-4">
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
                                                    {trade.trade_type === "BUY" ? t("historial.buy") : t("historial.sell")}
                                                </span>
                                            </td>

                                            {/* Lots (lot_size) */}
                                            <td className="px-4 py-4 text-right hidden md:table-cell">
                                                <span className="text-xs text-white/50">{trade.lot_size.toFixed(2)}</span>
                                            </td>

                                            {/* Stop Loss (stop_loss) */}
                                            <td className="px-4 py-4 text-right hidden md:table-cell">
                                                <span className="text-xs" style={{ color: "#f87171" }}>
                                                    {trade.stop_loss.toFixed(2)}
                                                </span>
                                            </td>

                                            {/* Take Profit (take_profit) */}
                                            <td className="px-4 py-4 text-right hidden md:table-cell">
                                                <span className="text-xs" style={{ color: "var(--color-olive)" }}>
                                                    {trade.take_profit.toFixed(2)}
                                                </span>
                                            </td>

                                            {/* Revenue / P&L (profit_loss) */}
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

                {/* Footer de la tabla */}
                <div className="px-6 py-3 border-t border-white/[0.04] flex items-center justify-between">
                    <span className="text-[11px] text-white/20">
                        {filteredTrades.length} {filteredTrades.length === 1 ? t("historial.operation_one") : t("historial.operation_other")}
                    </span>
                    <span className="text-[10px] text-white/15">{t("historial.page")}</span>
                </div>
            </div>
        </div>
    );
};
