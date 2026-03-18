import React, { useState, useEffect, useRef, useCallback } from "react";

/**
 * Tabla dinámica de operaciones de trading (XAUUSD).
 * - Polls DB every 5 s (free — no MetaAPI calls)
 * - Syncs open trades with MetaAPI every 2 min (2 MetaAPI calls per sync)
 */

const POLL_INTERVAL_MS = 5_000; // refresh from DB only — zero MetaAPI calls

const BASE = import.meta.env.VITE_BACKEND_URL;

const formatDate = (isoString) => {
    if (!isoString) return "—";
    const date = new Date(isoString);
    return date.toLocaleDateString("es-ES", { day: "2-digit", month: "short" })
        + ", "
        + date.toLocaleTimeString("es-ES", { hour: "2-digit", minute: "2-digit" });
};

export const TradeTable = () => {
    const [trades, setTrades]               = useState([]);
    const [loading, setLoading]             = useState(true);
    const [lastUpdated, setLastUpdated]     = useState(null);
    const [pendingCancel, setPendingCancel] = useState(null);
    const timeoutRef  = useRef(null);
    const pollRef = useRef(null);

    const authHeaders = () => ({
        Authorization: `Bearer ${localStorage.getItem("token")}`,
    });

    // ── Fetch trades from DB (no MetaAPI calls) ───────────────────────────
    const fetchTrades = useCallback(async () => {
        try {
            const [openRes, histRes] = await Promise.all([
                fetch(`${BASE}/api/dashboard/trades/open`,    { headers: authHeaders() }),
                fetch(`${BASE}/api/dashboard/trades/history`, { headers: authHeaders() }),
            ]);
            const [open, history] = await Promise.all([
                openRes.ok  ? openRes.json()  : { trades: [] },
                histRes.ok  ? histRes.json()  : { trades: [] },
            ]);
            const combined = [
                ...(open.trades    || []),
                ...(history.trades || []),
            ].sort((a, b) => new Date(b.opened_at) - new Date(a.opened_at));
            setTrades(combined);
            setLastUpdated(new Date());
        } catch {
            // silent — keep showing last data
        } finally {
            setLoading(false);
        }
    }, []);

    // ── Sync open trades with MetaAPI (2 calls) ───────────────────────────
    const syncTrades = useCallback(async () => {
        try {
            await fetch(`${BASE}/api/dashboard/sync`, {
                method:  "POST",
                headers: authHeaders(),
            });
            // After sync, refresh the table
            fetchTrades();
        } catch {
            // silent
        }
    }, [fetchTrades]);

    // ── Mount: initial fetch + poll DB only (no MetaAPI) ─────────────────
    useEffect(() => {
        fetchTrades();
        pollRef.current = setInterval(fetchTrades, POLL_INTERVAL_MS);
        return () => clearInterval(pollRef.current);
    }, [fetchTrades]);

    // ── Immediate refresh when a trade is placed elsewhere on the page ────
    useEffect(() => {
        const handler = () => fetchTrades();
        window.addEventListener('trade-placed', handler);
        return () => window.removeEventListener('trade-placed', handler);
    }, [fetchTrades]);

    // ── Pending cancel reset after 3 s ────────────────────────────────────
    useEffect(() => {
        if (pendingCancel === null) return;
        timeoutRef.current = setTimeout(() => setPendingCancel(null), 3000);
        return () => clearTimeout(timeoutRef.current);
    }, [pendingCancel]);

    const handleCancelClick = (tradeId) => {
        if (pendingCancel === tradeId) {
            clearTimeout(timeoutRef.current);
            setPendingCancel(null);
            fetch(`${BASE}/api/dashboard/trades/${tradeId}/cancel`, {
                method:  "PATCH",
                headers: authHeaders(),
            })
                .then(r => r.ok ? r.json() : Promise.reject())
                .catch(() => {})
                .finally(() => {
                    setTrades(prev => prev.filter(t => t.id !== tradeId));
                });
        } else {
            setPendingCancel(tradeId);
        }
    };

    const openCount   = trades.filter(t => t.status === "open").length;
    const closedCount = trades.filter(t => t.status === "closed").length;

    return (
        <div className="liquid-glass border border-white/5 rounded-2xl overflow-hidden">
            {/* Cabecera */}
            <div className="flex items-center justify-between p-5 border-b border-white/5">
                <div className="flex items-center gap-3">
                    <h2 className="text-sm font-semibold text-white">Operaciones</h2>
                    <div className="flex items-center gap-1.5">
                        {/* Live indicator */}
                        <span className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" />
                        <span className="text-[10px] text-white/30">
                            {openCount > 0 ? `${openCount} abiertas` : "sin abiertas"}
                            {closedCount > 0 ? ` · ${closedCount} cerradas` : ""}
                        </span>
                    </div>
                </div>
                <div className="flex items-center gap-3">
                    {lastUpdated && (
                        <span className="text-[9px] text-white/20">
                            {lastUpdated.toLocaleTimeString("es-ES", { hour: "2-digit", minute: "2-digit", second: "2-digit" })}
                        </span>
                    )}
                    <button
                        onClick={() => { fetchTrades(); syncTrades(); }}
                        title="Sincronizar ahora"
                        className="w-7 h-7 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center text-white/40 hover:text-white hover:bg-white/10 transition-all text-xs"
                    >
                        ↻
                    </button>
                </div>
            </div>

            {/* Tabla */}
            <div className="overflow-x-auto">
                {loading ? (
                    <div className="p-8 text-center text-white/30 text-sm">Cargando operaciones...</div>
                ) : trades.length === 0 ? (
                    <div className="p-8 text-center text-white/30 text-sm">Sin operaciones registradas</div>
                ) : (
                    <table className="w-full">
                        <thead>
                            <tr className="text-[10px] font-medium text-white/30 uppercase tracking-wider">
                                <th className="text-left px-5 py-3">Fecha</th>
                                <th className="text-left px-4 py-3">Símbolo</th>
                                <th className="text-left px-4 py-3 hidden sm:table-cell">Tipo</th>
                                <th className="text-left px-4 py-3 hidden md:table-cell">Bot</th>
                                <th className="text-right px-5 py-3">Resultado</th>
                                <th className="px-4 py-3" />
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-white/[0.03]">
                            {trades.map((trade) => {
                                const isProfit  = trade.profit_loss != null && trade.profit_loss >= 0;
                                const isOpen    = trade.status === "open";
                                const isPending = pendingCancel === trade.id;
                                const isProp    = trade.is_prop_firm;
                                const phaseLabel = trade.prop_phase ? trade.prop_phase.replace("phase", "Ph") : null;
                                const botLabel   = isProp
                                    ? `Prop${phaseLabel ? ` · ${phaseLabel}` : ""}`
                                    : (trade.wallet_name || "Demo");

                                return (
                                    <tr key={trade.id} className="hover:bg-white/[0.02] transition-colors">
                                        <td className="px-5 py-4">
                                            <span className="text-xs text-white/40">{formatDate(trade.opened_at)}</span>
                                        </td>
                                        <td className="px-4 py-4">
                                            <div className="flex items-center gap-2">
                                                <div className="w-7 h-7 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center text-xs flex-shrink-0 font-bold"
                                                    style={{ color: "var(--color-gold)" }}>
                                                    Au
                                                </div>
                                                <span className="text-sm font-semibold text-white">
                                                    {trade.symbol || "XAUUSD"}
                                                </span>
                                            </div>
                                        </td>
                                        <td className="px-4 py-4 hidden sm:table-cell">
                                            <span className="text-[11px] font-bold px-2.5 py-1 rounded-full"
                                                style={{
                                                    background: trade.trade_type === "BUY" ? "rgba(99,119,66,0.15)" : "rgba(195,143,55,0.12)",
                                                    color:      trade.trade_type === "BUY" ? "var(--color-olive)" : "var(--color-gold)",
                                                }}>
                                                {trade.trade_type === "BUY" ? "▲ Compra" : "▼ Venta"}
                                            </span>
                                        </td>
                                        <td className="px-4 py-4 hidden md:table-cell">
                                            <span className="text-[10px] font-semibold px-2 py-0.5 rounded-md"
                                                style={{
                                                    background: isProp ? "rgba(195,143,55,0.12)" : "rgba(255,255,255,0.06)",
                                                    color:      isProp ? "var(--color-gold)" : "rgba(255,255,255,0.35)",
                                                    border:     isProp ? "1px solid rgba(195,143,55,0.2)" : "1px solid rgba(255,255,255,0.08)",
                                                }}>
                                                {botLabel}
                                            </span>
                                        </td>
                                        <td className="px-5 py-4 text-right">
                                            {isOpen && trade.profit_loss == null ? (
                                                <span className="text-xs text-white/30 italic">En curso</span>
                                            ) : (
                                                <span className="text-sm font-bold"
                                                    style={{ color: isProfit ? "var(--color-olive)" : "#f87171" }}>
                                                    {isOpen && <span className="text-[9px] text-white/30 mr-1">~</span>}
                                                    {isProfit ? "+" : ""}${Number(trade.profit_loss).toFixed(2)}
                                                </span>
                                            )}
                                        </td>
                                        <td className="px-4 py-4 text-right">
                                            {isOpen && (
                                                <button onClick={() => handleCancelClick(trade.id)}
                                                    title={isPending ? "Haz clic de nuevo para confirmar" : "Cancelar operación"}
                                                    style={{
                                                        background: isPending ? "rgba(239,68,68,0.25)" : "rgba(239,68,68,0.08)",
                                                        border:     isPending ? "1px solid rgba(239,68,68,0.7)" : "1px solid rgba(239,68,68,0.2)",
                                                        color:      isPending ? "#f87171" : "rgba(239,68,68,0.45)",
                                                        boxShadow:  isPending ? "0 0 10px rgba(239,68,68,0.3)" : "none",
                                                        transition: "all 0.2s ease",
                                                    }}
                                                    className="text-[10px] font-bold px-3 py-1.5 rounded-lg uppercase tracking-wide cursor-pointer">
                                                    {isPending ? "¿Confirmar?" : "Cancelar"}
                                                </button>
                                            )}
                                        </td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                )}
            </div>
        </div>
    );
};
