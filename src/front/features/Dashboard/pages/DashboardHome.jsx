import React, { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { TradingViewChart } from "../components/TradingViewChart";
import { OverviewCard } from "../components/OverviewCard";
import { PortfolioCard } from "../components/PortfolioCard";
import { WalletPanel } from "../components/WalletPanel";
import { AdBanner } from "../components/AdBanner";
import { TradeTable } from "../components/TradeTable";
import { BotControlPage } from "./BotControlPage";
import { getDashboardSummary } from "../api";

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

export const DashboardHome = () => {
    const { t } = useTranslation();
    const [summary, setSummary] = useState(EMPTY_SUMMARY);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        getDashboardSummary()
            .then((data) => { if (data) setSummary(data); })
            .catch(() => { })
            .finally(() => setLoading(false));
    }, []);

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

            {/* Bloque de Gráfica y Tabla (SOLO UNO) */}
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