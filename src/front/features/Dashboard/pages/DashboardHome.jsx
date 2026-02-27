import React from "react";
import { TradingViewChart } from "../components/TradingViewChart";
import { PortfolioCard } from "../components/PortfolioCard";
import { WalletPanel } from "../components/WalletPanel";
import { AdBanner } from "../components/AdBanner";
import { TradeTable } from "../components/TradeTable";

const MOCK_SUMMARY = {
  account: {
    balance: 10000.00,
    equity: 10326.40,
    currency: "USD",
    margin: 150.00,
    free_margin: 10176.40,
    is_connected: false,
  },
  stats: {
    total_trades: 24,
    winning_trades: 16,
    losing_trades: 8,
    win_rate: 66.7,
    total_profit: 326.40,
  },
  strategy: {
    name: "Medio",
    risk_level: "2",
    is_active: true,
  },
};

/**
 * Datos mock del resumen de cuenta de trading.
 * Estructura alineada con GET /api/dashboard/summary del backend.
 * TODO: Reemplazar con useEffect + fetch al endpoint real cuando el backend esté conectado.
 */

/**
 * Página principal del Dashboard — GoldPilot XAUUSD.
 * Muestra estadísticas de cuenta, gráfico de Oro en vivo y historial de operaciones.
 */
export const DashboardHome = () => {
  const { account, stats } = MOCK_SUMMARY;
  const isProfitable = stats.total_profit >= 0;

  return (
    <div className="flex flex-col gap-5 w-full">

      <div className="pb-2 border-b border-white/[0.05]">
        <h1 className="text-2xl font-bold tracking-tight text-white">Dashboard</h1>
      </div>

      {/* Stats cards — Balance · Equity · P&L · Win Rate */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 items-stretch">
        <PortfolioCard
          title="Balance"
          value={`$${account.balance.toLocaleString("en-US", { minimumFractionDigits: 2 })}`}
          subtitle={account.currency}
          icon="◈"
          color="gold"
        />
        <PortfolioCard
          title="Equity"
          value={`$${account.equity.toLocaleString("en-US", { minimumFractionDigits: 2 })}`}
          subtitle="Tiempo real"
          icon="⇗"
          color="green"
        />
        <PortfolioCard
          title="Total P&L"
          value={`${isProfitable ? "+" : ""}$${stats.total_profit.toFixed(2)}`}
          subtitle={`${stats.winning_trades}G / ${stats.losing_trades}P`}
          icon="◬"
          trend={isProfitable ? "up" : "down"}
          color={isProfitable ? "green" : "red"}
        />
        <PortfolioCard
          title="Win Rate"
          value={`${stats.win_rate.toFixed(1)}%`}
          subtitle={`${stats.total_trades} operaciones`}
          icon="%"
          color="blue"
        />
      </div>
      {/* Layout de 2 columnas — igual que antes */}
      <div className="flex flex-col xl:flex-row gap-6 w-full">

        <div className="flex flex-col gap-5 flex-1 min-w-0">

          {/* Gráfico XAUUSD */}
          <div
            className="w-full rounded-2xl p-5 border border-white/[0.06]"
            style={{ background: "rgba(255,255,255,0.03)", backdropFilter: "blur(16px)" }}
          >
            <TradingViewChart />
          </div>

          {/* Historial de operaciones */}
          <TradeTable />
        </div>

        {/* Columna derecha — WalletPanel + AdBanner */}
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
