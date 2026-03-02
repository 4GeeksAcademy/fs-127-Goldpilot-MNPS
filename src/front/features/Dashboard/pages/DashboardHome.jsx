import React, { useState, useEffect } from "react";
import { TradingViewChart } from "../components/TradingViewChart";
import { PortfolioCard } from "../components/PortfolioCard";
import { WalletPanel } from "../components/WalletPanel";
import { AdBanner } from "../components/AdBanner";
import { TradeTable } from "../components/TradeTable";
import { BotControlPage } from "./BotControlPage";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

const EMPTY_SUMMARY = {
    account: { balance: null, equity: null, currency: "USD", margin: null, free_margin: null, is_connected: false },
    stats: { total_trades: 0, winning_trades: 0, losing_trades: 0, win_rate: 0, total_profit: 0 },
};

const fmt = (val, decimals = 2) =>
    val != null ? `$${Number(val).toLocaleString("en-US", { minimumFractionDigits: decimals })}` : "–";

export const DashboardHome = () => {
    const [summary, setSummary] = useState(EMPTY_SUMMARY);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const token = localStorage.getItem("token");
        fetch(`${BACKEND_URL}/api/dashboard/summary`, {
            headers: { Authorization: `Bearer ${token}` },
        })
            .then((r) => (r.ok ? r.json() : null))
            .then((data) => { if (data) setSummary(data); })
            .catch(() => {})
            .finally(() => setLoading(false));
    }, []);

    const { account, stats } = summary;
    const isProfitable = stats.total_profit >= 0;

    return (
        <div className="flex flex-col gap-5 w-full">
            <div className="pb-2 border-b border-white/[0.05]">
                <h1 className="text-2xl font-bold tracking-tight text-white">Dashboard</h1>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 items-stretch">
                <PortfolioCard title="Balance" value={fmt(account.balance)} subtitle={account.currency} icon="◈" color="gold" />
                <PortfolioCard title="Equity" value={fmt(account.equity)} subtitle="Tiempo real" icon="⇗" color="green" />
                <PortfolioCard
                    title="Total P&L"
                    value={stats.total_profit !== 0 ? `${isProfitable ? "+" : ""}${fmt(stats.total_profit)}` : "–"}
                    subtitle={stats.total_trades > 0 ? `${stats.winning_trades}G / ${stats.losing_trades}P` : "Sin operaciones"}
                    icon="◬" trend={isProfitable ? "up" : "down"} color={isProfitable ? "green" : "red"}
                />
                <PortfolioCard
                    title="Win Rate"
                    value={stats.total_trades > 0 ? `${Number(stats.win_rate).toFixed(1)}%` : "–"}
                    subtitle={`${stats.total_trades} operaciones`} icon="%" color="blue"
                />
            </div>

            <div className="flex flex-col xl:flex-row gap-6 w-full">
                <div className="flex flex-col gap-5 flex-1 min-w-0">
                    <div className="w-full rounded-2xl p-5 border border-white/[0.06]" style={{ background: "rgba(255,255,255,0.03)", backdropFilter: "blur(16px)" }}>
                        <TradingViewChart />
                    </div>
                    <TradeTable />
                </div>
                <div className="w-full xl:w-72 shrink-0" style={{ alignSelf: "stretch", display: "grid", gridTemplateRows: "auto 1fr", gap: "1.25rem" }}>
                    <WalletPanel />
                    <AdBanner className="h-full" />
                </div>
            </div>

            <BotControlPage />
        </div>
    );
};
