import React from "react";
import { TradingViewChart } from "../components/TradingViewChart";
import { OverviewCard } from "../components/OverviewCard";
import { WalletPanel } from "../components/WalletPanel";
import { AdBanner } from "../components/AdBanner";
import { NewsTable } from "../components/NewsTable";

/**
 * Datos mock para las Overview Cards.
 * OverviewCard es el componente primario; estas son instancias reutilizadas.
 * TODO: Reemplazar con datos reales de GET /api/wallets/equity.
 */
const OVERVIEW_WALLETS = [
    { name: "Bitcoin", symbol: "BTC", icon: "₿", balanceUSD: 42350.21, changePercent: -6.75 },
    { name: "Ethereum", symbol: "ETH", icon: "Ξ", balanceUSD: 72326.25, changePercent: -3.75 },
    { name: "Reserve Wallet", symbol: "USDT", icon: "◎", balanceUSD: 3078.99, changePercent: 0.19 },
];

/**
 * Página principal del Dashboard.
 
 */
export const DashboardHome = () => {
    return (
        <div className="flex flex-col gap-5 w-full">


            <div className="pb-2 border-b border-white/[0.05]">
                <h1 className="text-2xl font-bold tracking-tight text-white">Dashboard</h1>
            </div>

            {/* Layout de 2 columnas — stretch por defecto hace que ambas tengan la misma altura */}
            <div className="flex flex-col xl:flex-row gap-6 w-full">

                <div className="flex flex-col gap-5 flex-1 min-w-0">


                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 items-stretch">
                        {OVERVIEW_WALLETS.map((wallet) => (
                            <OverviewCard key={wallet.symbol} {...wallet} />
                        ))}
                    </div>

                    {/* TradingView Chart */}
                    <div
                        className="w-full rounded-2xl p-5 border border-white/[0.06]"
                        style={{ background: "rgba(255,255,255,0.03)", backdropFilter: "blur(16px)" }}
                    >
                        <TradingViewChart />
                    </div>

                    {/* Tabla de mercado y noticias */}
                    <NewsTable />
                </div>


                <div
                    className="w-full xl:w-72 shrink-0"
                    style={{
                        alignSelf: "stretch",
                        display: "grid",
                        gridTemplateRows: "auto 1fr",
                        gap: "1.25rem",
                    }}
                >
                    <WalletPanel />
                    <AdBanner className="h-full" />
                </div>

            </div>
        </div>
    );
};
