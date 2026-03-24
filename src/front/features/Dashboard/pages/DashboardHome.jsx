import React, { useState, useEffect, useCallback } from "react";
import { useTranslation } from "react-i18next";
import { TradingViewChart } from "../components/TradingViewChart";
import { OverviewCard } from "../components/OverviewCard";
import { PortfolioCard } from "../components/PortfolioCard";
import { WalletPanel } from "../components/WalletPanel";
import { AdBanner } from "../components/AdBanner";
import { TradeTable } from "../components/TradeTable";
import { getWallets } from "../api";
import useGlobalReducer from "../../../hooks/useGlobalReducer";

const BACKEND = import.meta.env.VITE_BACKEND_URL;

const EMPTY_SUMMARY = {
    wallets: [],
    stats: { total_trades: 0, winning_trades: 0, losing_trades: 0, win_rate: 0, total_profit: 0 },
};

const fmt = (val, decimals = 2) =>
    val != null ? `$${Number(val).toLocaleString("en-US", { minimumFractionDigits: decimals })}` : "–";

const calcChangePercent = (equity, balance) => {
    if (equity == null || balance == null || balance === 0) return 0;
    return ((equity - balance) / balance) * 100;
};

// ── Quick Trade Panel ────────────────────────────────────────────────────────
const QuickTradePanel = () => {
    const [price, setPrice]           = useState(null);
    const [priceErr, setPriceErr]     = useState(null);
    const [volume, setVolume]         = useState("0.10");
    const [sl, setSl]                 = useState("");
    const [tp, setTp]                 = useState("");
    const [loading, setLoading]       = useState(false);
    const [result, setResult]         = useState(null);
    const [wallets, setWallets]       = useState([]);
    const [selectedWallet, setSelectedWallet] = useState(null); // null = auto

    const token   = () => localStorage.getItem("token");
    const headers = () => ({ Authorization: `Bearer ${token()}`, "Content-Type": "application/json" });

    const fetchPrice = useCallback(async () => {
        setPriceErr(null);
        try {
            const r    = await fetch(`${BACKEND}/api/market/price?symbol=XAUUSD`, { headers: { Authorization: `Bearer ${token()}` } });
            const data = await r.json();
            if (data.bid) setPrice(data.bid);
            else setPriceErr(data.error || "No price available");
        } catch {
            setPriceErr("Connection error");
        }
    }, []);

    useEffect(() => {
        fetchPrice();
        getWallets()
            .then(data => {
                const list = data.wallets || data || [];
                setWallets(list.filter(w => w.status === "connected"));
            })
            .catch(() => {});
    }, [fetchPrice]);

    const placeOrder = async (action) => {
        setLoading(true);
        setResult(null);
        const body = {
            action,
            entry:  price || 3100,
            volume: parseFloat(volume) || 0.01,
        };
        if (sl && parseFloat(sl) > 0)  body.sl = parseFloat(sl);
        if (tp && parseFloat(tp) > 0)  body.tp = parseFloat(tp);
        if (selectedWallet)            body.wallet_id = selectedWallet;

        try {
            const r = await fetch(`${BACKEND}/api/bot/manual-trade`, {
                method:  "POST",
                headers: headers(),
                body: JSON.stringify(body),
            });
            const data = await r.json();
            setResult(data);
            if (data.meta_trade_id || data.trade) {
                window.dispatchEvent(new CustomEvent('trade-placed'));
            }
        } catch (e) {
            setResult({ meta_error: e.message });
        } finally {
            setLoading(false);
        }
    };

    const activeWallet = wallets.find(w => w.id === selectedWallet);

    return (
        <div className="flex flex-col gap-3 p-4 rounded-xl border border-white/10"
             style={{ background: "rgba(255,255,255,0.03)" }}>

            <div className="flex flex-wrap items-center gap-3">
                {/* Live price */}
                <div className="flex items-center gap-2 min-w-[130px]">
                    <span className="text-[10px] text-white/30 uppercase tracking-widest">XAUUSD</span>
                    {price ? (
                        <span className="text-lg font-bold" style={{ color: "var(--color-gold)" }}>
                            ${Number(price).toFixed(2)}
                        </span>
                    ) : (
                        <span className="text-sm text-white/30">{priceErr || "…"}</span>
                    )}
                    <button onClick={fetchPrice} title="Actualizar precio"
                        className="w-6 h-6 rounded-md bg-white/5 border border-white/10 text-white/40 hover:text-white text-xs flex items-center justify-center transition-all">
                        ↻
                    </button>
                </div>

                <div className="w-px h-8 bg-white/10 hidden sm:block" />

                {/* Account selector */}
                {wallets.length > 0 && (
                    <div className="flex flex-col gap-1">
                        <label className="text-[9px] text-white/30 uppercase tracking-widest">Cuenta</label>
                        <select
                            value={selectedWallet ?? ""}
                            onChange={e => setSelectedWallet(e.target.value ? Number(e.target.value) : null)}
                            className="bg-black/40 border border-white/10 rounded-lg px-2 py-1.5 text-white text-xs outline-none focus:border-[var(--color-gold)] transition-colors cursor-pointer"
                        >
                            <option value="">Auto (primera conectada)</option>
                            {wallets.map(w => (
                                <option key={w.id} value={w.id}>
                                    {w.broker_name || w.server || `Wallet #${w.id}`}{w.is_prop_firm ? " · PROP" : ""}
                                </option>
                            ))}
                        </select>
                    </div>
                )}

                <div className="w-px h-8 bg-white/10 hidden sm:block" />

                {/* Inputs */}
                <div className="flex flex-wrap gap-2 items-center text-xs">
                    <div className="flex flex-col gap-1">
                        <label className="text-[9px] text-white/30 uppercase tracking-widest">Lotes</label>
                        <input type="number" step="0.01" min="0.01" value={volume}
                            onChange={e => setVolume(e.target.value)}
                            className="w-20 bg-black/40 border border-white/10 rounded-lg px-2 py-1.5 text-white text-xs outline-none focus:border-[var(--color-gold)] transition-colors text-center" />
                    </div>
                    <div className="flex flex-col gap-1">
                        <label className="text-[9px] text-white/30 uppercase tracking-widest">SL <span className="normal-case opacity-50">(opcional)</span></label>
                        <input type="number" step="0.01" value={sl} placeholder="—"
                            onChange={e => setSl(e.target.value)}
                            className="w-24 bg-black/40 border border-white/10 rounded-lg px-2 py-1.5 text-white text-xs outline-none focus:border-red-400 transition-colors text-center" />
                    </div>
                    <div className="flex flex-col gap-1">
                        <label className="text-[9px] text-white/30 uppercase tracking-widest">TP <span className="normal-case opacity-50">(opcional)</span></label>
                        <input type="number" step="0.01" value={tp} placeholder="—"
                            onChange={e => setTp(e.target.value)}
                            className="w-24 bg-black/40 border border-white/10 rounded-lg px-2 py-1.5 text-white text-xs outline-none focus:border-green-400 transition-colors text-center" />
                    </div>
                </div>

                <div className="w-px h-8 bg-white/10 hidden sm:block" />

                {/* BUY / SELL buttons */}
                <div className="flex gap-2">
                    <button onClick={() => placeOrder("BUY")} disabled={loading}
                        className="px-5 py-2 rounded-lg text-sm font-bold uppercase tracking-wider transition-all disabled:opacity-50"
                        style={{ background: "rgba(99,119,66,0.2)", border: "1px solid rgba(99,119,66,0.5)", color: "var(--color-olive)" }}>
                        {loading ? "…" : "▲ BUY"}
                    </button>
                    <button onClick={() => placeOrder("SELL")} disabled={loading}
                        className="px-5 py-2 rounded-lg text-sm font-bold uppercase tracking-wider transition-all disabled:opacity-50"
                        style={{ background: "rgba(195,143,55,0.12)", border: "1px solid rgba(195,143,55,0.4)", color: "var(--color-gold)" }}>
                        {loading ? "…" : "▼ SELL"}
                    </button>
                </div>
            </div>

            {/* Active account badge */}
            {activeWallet && (
                <div className="flex items-center gap-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-green-400" />
                    <span className="text-[10px] text-white/30">
                        Enviando a: <span className="text-white/60">{activeWallet.broker_name || activeWallet.server}</span>
                        {activeWallet.is_prop_firm && <span className="ml-1 text-yellow-400">PROP</span>}
                    </span>
                </div>
            )}

            {/* Result feedback */}
            {result && (
                <div className={`px-3 py-2 rounded-lg text-xs ${
                    result.meta_trade_id
                        ? "bg-green-500/10 border border-green-500/20 text-green-400"
                        : "bg-red-500/10 border border-red-500/20 text-red-400"
                }`}>
                    {result.meta_trade_id
                        ? `✓ Orden enviada a MetaTrader — ID ${result.meta_trade_id}`
                        : `✗ ${result.meta_error || result.msg || "No se pudo enviar a MetaTrader"}`}
                </div>
            )}
        </div>
    );
};
// ────────────────────────────────────────────────────────────────────────────

export const DashboardHome = () => {
    const { t } = useTranslation();
    const { store } = useGlobalReducer();
    const summary = store.dashboardSummary || EMPTY_SUMMARY;
    const { wallets, stats } = summary;
    const isProfitable = stats.total_profit >= 0;

    return (
        <div className="flex flex-col gap-5 w-full">
            <div className="pb-2 border-b border-white/[0.05]">
                <h1 className="text-2xl font-bold tracking-tight text-white">{t("dashboard.title")}</h1>
            </div>

            {/* Cards dinámicas */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 items-stretch">
                {wallets.length > 0 ? (
                    wallets.map((wallet) => (
                        <OverviewCard
                            key={wallet.id}
                            name={wallet.broker_name || wallet.server || "MetaTrader"}
                            symbol={wallet.platform?.toUpperCase() || "MT4"}
                            icon={wallet.status === "connected" ? "◈" : "◇"}
                            balanceUSD={wallet.balance ?? 0}
                            changePercent={calcChangePercent(wallet.equity, wallet.balance)}
                        />
                    ))
                ) : (
                    <div className="col-span-full flex items-center justify-center py-8 rounded-2xl border border-white/[0.06]"
                        style={{ background: "rgba(255,255,255,0.02)" }}>
                        <p className="text-sm text-white/30">{t("dashboard.noWallets")}</p>
                    </div>
                )}

                <PortfolioCard
                    title={t("dashboard.totalPnl")}
                    value={stats.total_profit !== 0 ? `${isProfitable ? "+" : ""}${fmt(stats.total_profit)}` : "–"}
                    subtitle={stats.total_trades > 0 ? `${stats.winning_trades}G / ${stats.losing_trades}P` : t("dashboard.noOperations")}
                    icon="◬" trend={isProfitable ? "up" : "down"} color={isProfitable ? "green" : "red"}
                />
                <PortfolioCard
                    title={t("dashboard.winRate")}
                    value={stats.total_trades > 0 ? `${Number(stats.win_rate).toFixed(1)}%` : "–"}
                    subtitle={`${stats.total_trades} ${t("dashboard.operations")}`} icon="%" color="blue"
                />
            </div>

            <div className="flex flex-col gap-6 w-full">
                <div className="w-full rounded-2xl p-5 border border-white/[0.06]" style={{ background: "rgba(255,255,255,0.03)", backdropFilter: "blur(16px)" }}>
                    <TradingViewChart />
                </div>

                <div className="w-full">
                    <WalletPanel />
                </div>

                <div className="w-full">
                    <TradeTable />
                </div>

                <div className="w-full">
                    <div className="pb-2 mb-1">
                        <h2 className="text-sm font-semibold text-white/60 uppercase tracking-widest">Operación Manual</h2>
                    </div>
                    <QuickTradePanel />
                </div>
            </div>

            <div className="w-full mt-2">
                <AdBanner />
            </div>
        </div>
    );
};
