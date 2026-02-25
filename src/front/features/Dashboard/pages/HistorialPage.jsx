import React, { useState } from "react";
import { PortfolioCard } from "../components/PortfolioCard";

/**
 * Página de Historial de Operaciones — /dashboard/historial
 * Historia de usuario: "Como usuario quiero ver el historial de mis operaciones
 * para poder analizar mis inversiones."
 *
 * Datos mock alineados al modelo Trade (tabla: trades):
 *   meta_trade_id, symbol, trade_type, lot_size, open_price, close_price,
 *   stop_loss, take_profit, profit_loss, opened_at, closed_at, status
 *
 * TODO (Tarea 2 — Backend):
 *   Conectar con GET /api/dashboard/trades/history
 *   El endpoint ya existe en dashboard_controller.py con mock data.
 *   El compañero de back debe filtrar por user_id y status='closed'
 *   y devolver todos los campos del modelo Trade necesarios aquí.
 */

/** Mock completo alineado con la tabla `trades` del backend */
const MOCK_TRADES = [
    {
        id: 1,
        meta_trade_id: "MT-00123",
        symbol: "XAUUSD",
        trade_type: "BUY",
        lot_size: 0.10,
        open_price: 2015.50,
        close_price: 2028.30,
        stop_loss: 2005.00,
        take_profit: 2035.00,
        profit_loss: 128.00,
        opened_at: "2026-02-24T09:15:00",
        closed_at: "2026-02-24T11:42:00",
        status: "closed",
    },
    {
        id: 2,
        meta_trade_id: "MT-00124",
        symbol: "XAUUSD",
        trade_type: "SELL",
        lot_size: 0.10,
        open_price: 2031.20,
        close_price: 2019.80,
        stop_loss: 2042.00,
        take_profit: 2015.00,
        profit_loss: 114.00,
        opened_at: "2026-02-24T13:00:00",
        closed_at: "2026-02-24T15:30:00",
        status: "closed",
    },
    {
        id: 3,
        meta_trade_id: "MT-00125",
        symbol: "XAUUSD",
        trade_type: "BUY",
        lot_size: 0.05,
        open_price: 2022.00,
        close_price: 2017.50,
        stop_loss: 2010.00,
        take_profit: 2040.00,
        profit_loss: -45.00,
        opened_at: "2026-02-23T10:00:00",
        closed_at: "2026-02-23T12:15:00",
        status: "closed",
    },
    {
        id: 4,
        meta_trade_id: "MT-00126",
        symbol: "XAUUSD",
        trade_type: "SELL",
        lot_size: 0.15,
        open_price: 2028.75,
        close_price: 2014.20,
        stop_loss: 2040.00,
        take_profit: 2010.00,
        profit_loss: 145.50,
        opened_at: "2026-02-22T08:30:00",
        closed_at: "2026-02-22T10:45:00",
        status: "closed",
    },
    {
        id: 5,
        meta_trade_id: "MT-00127",
        symbol: "XAUUSD",
        trade_type: "BUY",
        lot_size: 0.10,
        open_price: 2010.00,
        close_price: 2006.50,
        stop_loss: 2000.00,
        take_profit: 2030.00,
        profit_loss: -35.00,
        opened_at: "2026-02-21T14:00:00",
        closed_at: "2026-02-21T16:20:00",
        status: "closed",
    },
    {
        id: 6,
        meta_trade_id: "MT-00128",
        symbol: "XAUUSD",
        trade_type: "BUY",
        lot_size: 0.20,
        open_price: 2008.00,
        close_price: 2021.30,
        stop_loss: 1998.00,
        take_profit: 2025.00,
        profit_loss: 266.00,
        opened_at: "2026-02-20T09:45:00",
        closed_at: "2026-02-20T14:10:00",
        status: "closed",
    },
];

/**
 * Formatea fecha ISO a "24 Feb 09:15"
 * @param {string} iso - Fecha en formato ISO 8601
 */
const fmt = (iso) => {
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

/** Filtros disponibles para el tipo de operación */
const FILTERS = [
    { label: "Todos", value: "ALL" },
    { label: "Compras", value: "BUY" },
    { label: "Ventas", value: "SELL" },
];

/**
 * Página principal del Historial de Operaciones.
 * Muestra resumen estadístico + tabla completa de trades cerrados.
 */
export const HistorialPage = () => {
    const [activeFilter, setActiveFilter] = useState("ALL");

    const filteredTrades = activeFilter === "ALL"
        ? MOCK_TRADES
        : MOCK_TRADES.filter((t) => t.trade_type === activeFilter);

    const stats = calcStats(filteredTrades);
    const isProfitable = stats.totalPnL >= 0;

    return (
        <div className="flex flex-col gap-6 w-full">

            {/* Cabecera de la página */}
            <div className="pb-2 border-b border-white/[0.05]">
                <h1 className="text-2xl font-bold tracking-tight text-white">Historial</h1>
                <p className="text-xs text-white/30 mt-1">
                    Registro completo de operaciones cerradas en XAUUSD
                </p>
            </div>

            {/* Resumen estadístico — 3 PortfolioCards */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <PortfolioCard
                    title="Total Operaciones"
                    value={String(stats.totalTrades)}
                    subtitle={`${stats.winning}G · ${stats.losing}P`}
                    icon="◳"
                    color="blue"
                />
                <PortfolioCard
                    title="Win Rate"
                    value={`${stats.winRate.toFixed(1)}%`}
                    subtitle="Operaciones filtradas"
                    icon="%"
                    color={stats.winRate >= 50 ? "green" : "red"}
                />
                <PortfolioCard
                    title="P&L Total"
                    value={`${isProfitable ? "+" : ""}$${stats.totalPnL.toFixed(2)}`}
                    subtitle="Resultado acumulado"
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
                    <h2 className="text-sm font-semibold text-white">Operaciones cerradas</h2>

                    {/* Filtros BUY / SELL / Todos */}
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
                                <th className="text-left px-5 py-3">Entrada</th>
                                <th className="text-left px-4 py-3">Salida</th>
                                <th className="text-left px-4 py-3 hidden lg:table-cell">Índice</th>
                                <th className="text-left px-4 py-3">Tipo</th>
                                <th className="text-right px-4 py-3 hidden md:table-cell">Lots</th>
                                <th className="text-right px-4 py-3 hidden md:table-cell">SL</th>
                                <th className="text-right px-4 py-3 hidden md:table-cell">TP</th>
                                <th className="text-right px-5 py-3">Revenue</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-white/[0.03]">
                            {filteredTrades.length === 0 ? (
                                <tr>
                                    <td colSpan={8} className="text-center py-12 text-xs text-white/20">
                                        No hay operaciones para el filtro seleccionado
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
                                                    {trade.trade_type === "BUY" ? "▲ Compra" : "▼ Venta"}
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
                        {filteredTrades.length} operación{filteredTrades.length !== 1 ? "es" : ""}
                    </span>
                    {/* TODO: Añadir paginación cuando el backend devuelva datos reales */}
                    <span className="text-[10px] text-white/15">Página 1 de 1</span>
                </div>
            </div>
        </div>
    );
};
