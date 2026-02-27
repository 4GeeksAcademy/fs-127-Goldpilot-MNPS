import React from "react";
import { TradingViewChart } from "../components/TradingViewChart";
import { PortfolioCard } from "../components/PortfolioCard";
import { WalletPanel } from "../components/WalletPanel";
import { AdBanner } from "../components/AdBanner";
import { TradeTable } from "../components/TradeTable";
import { useState, useEffect } from 'react';
import { getBotStatus, startBot, stopBot, connectAccount, getAccount } 


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
export default function BotControlPage() {
  // -- State --
  const [botStatus, setBotStatus] = useState(null);
  const [account, setAccount] = useState(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [showConnectForm, setShowConnectForm] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // -- MetaApi connect form state --
  const [connectForm, setConnectForm] = useState({
    account_id: '',
    api_token: '',
    broker_name: '',
    account_type: 'demo',
  });

  // -- Fetch bot status on mount --
  useEffect(() => {
    fetchStatus();
  }, []);

  const fetchStatus = async () => {
    try {
      const data = await getBotStatus();
      setBotStatus(data);
      setAccount(data.account);
    } catch (err) {
      console.error('Error fetching bot status:', err);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Handle starting the bot.
   * Calls /api/bot/start and updates the UI.
   */
  const handleStart = async () => {
    setActionLoading(true);
    setError('');
    setSuccess('');
    try {
      await startBot();
      setSuccess('Bot started successfully!');
      fetchStatus();
    } catch (err) {
      setError(err.message);
    } finally {
      setActionLoading(false);
    }
  };

  /**
   * Handle stopping the bot.
   */
  const handleStop = async () => {
    setActionLoading(true);
    setError('');
    setSuccess('');
    try {
      await stopBot();
      setSuccess('Bot stopped.');
      fetchStatus();
    } catch (err) {
      setError(err.message);
    } finally {
      setActionLoading(false);
    }
  };

  /**
   * Handle MetaApi account connection.
   */
  const handleConnect = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    try {
      await connectAccount(connectForm);
      setSuccess('Account connected successfully!');
      setShowConnectForm(false);
      fetchStatus();
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-10 h-10 border-4 border-gold-500/30 border-t-gold-500 rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-white">Bot Control Panel</h2>

      {/* Alerts */}
      {error && (
        <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400">{error}</div>
      )}
      {success && (
        <div className="p-4 rounded-xl bg-green-500/10 border border-green-500/20 text-green-400">{success}</div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* ==================== BOT STATUS CARD ==================== */}
        <div className="glass-card p-8">
          <div className="flex items-center gap-4 mb-6">
            {/* Status indicator — large animated dot */}
            <div className={`w-16 h-16 rounded-2xl flex items-center justify-center ${
              botStatus?.bot_active
                ? 'bg-green-500/10 border border-green-500/20'
                : 'bg-dark-300 border border-gold-500/10'
            }`}>
              <div className={`w-6 h-6 rounded-full ${
                botStatus?.bot_active
                  ? 'bg-green-400 animate-pulse shadow-lg shadow-green-500/50'
                  : 'bg-gray-600'
              }`} />
            </div>
            <div>
              <h3 className="text-xl font-bold text-white">
                Bot is {botStatus?.bot_active ? 'Running' : 'Stopped'}
              </h3>
              <p className="text-gray-400 text-sm">
                {botStatus?.bot_active
                  ? 'The bot is actively trading XAUUSD'
                  : 'Start the bot to begin automated trading'}
              </p>
            </div>
          </div>

          {/* Start/Stop buttons */}
          <div className="flex gap-3">
            {botStatus?.bot_active ? (
              <button
                onClick={handleStop}
                disabled={actionLoading}
                className="btn-danger flex-1"
              >
                {actionLoading ? 'Stopping...' : 'Stop Bot'}
              </button>
            ) : (
              <button
                onClick={handleStart}
                disabled={actionLoading}
                className="btn-gold flex-1"
              >
                {actionLoading ? 'Starting...' : 'Start Bot'}
              </button>
            )}
          </div>
        </div>

        {/* ==================== CURRENT CONFIG ==================== */}
        <div className="glass-card p-8">
          <h3 className="text-lg font-semibold text-white mb-4">Current Configuration</h3>
          <div className="space-y-4">
            {/* Strategy info */}
            <div className="flex items-center justify-between py-3 border-b border-dark-300/50">
              <span className="text-gray-400">Active Strategy</span>
              <span className="text-white font-medium">
                {botStatus?.strategy?.name || 'None selected'}
              </span>
            </div>
            {/* Account info */}
            <div className="flex items-center justify-between py-3 border-b border-dark-300/50">
              <span className="text-gray-400">Broker Account</span>
              <span className="text-white font-medium">
                {account?.broker_name || 'Not connected'}
              </span>
            </div>
            <div className="flex items-center justify-between py-3 border-b border-dark-300/50">
              <span className="text-gray-400">Account Type</span>
              <span className={`px-2 py-1 rounded-lg text-xs font-medium ${
                account?.account_type === 'live'
                  ? 'bg-red-500/10 text-red-400'
                  : 'bg-green-500/10 text-green-400'
              }`}>
                {account?.account_type?.toUpperCase() || 'N/A'}
              </span>
            </div>
            <div className="flex items-center justify-between py-3">
              <span className="text-gray-400">Connection Status</span>
              <span className={`px-2 py-1 rounded-lg text-xs font-medium ${
                account?.status === 'connected'
                  ? 'bg-green-500/10 text-green-400'
                  : 'bg-gray-500/10 text-gray-400'
              }`}>
                {account?.status || 'N/A'}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* ==================== METAAPI CONNECTION ==================== */}
      <div className="glass-card p-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-lg font-semibold text-white">MetaApi Connection</h3>
            <p className="text-gray-400 text-sm">Connect your broker account via MetaApi</p>
          </div>
          {!account && (
            <button
              onClick={() => setShowConnectForm(!showConnectForm)}
              className="btn-gold text-sm"
            >
              {showConnectForm ? 'Cancel' : 'Connect Account'}
            </button>
          )}
        </div>

        {showConnectForm && !account && (
          <form onSubmit={handleConnect} className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-gray-400 mb-1">MetaApi Account ID</label>
              <input
                type="text"
                value={connectForm.account_id}
                onChange={(e) => setConnectForm({ ...connectForm, account_id: e.target.value })}
                className="glass-input"
                placeholder="Your MetaApi account ID"
                required
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">API Token</label>
              <input
                type="password"
                value={connectForm.api_token}
                onChange={(e) => setConnectForm({ ...connectForm, api_token: e.target.value })}
                className="glass-input"
                placeholder="Your MetaApi token"
                required
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Broker Name</label>
              <input
                type="text"
                value={connectForm.broker_name}
                onChange={(e) => setConnectForm({ ...connectForm, broker_name: e.target.value })}
                className="glass-input"
                placeholder="e.g., IC Markets"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Account Type</label>
              <select
                value={connectForm.account_type}
                onChange={(e) => setConnectForm({ ...connectForm, account_type: e.target.value })}
                className="glass-input"
              >
                <option value="demo">Demo</option>
                <option value="live">Live</option>
              </select>
            </div>
            <div className="sm:col-span-2">
              <button type="submit" className="btn-gold">Connect Account</button>
            </div>
          </form>
        )}

        {account && (
          <div className="glass-card bg-dark-300/40 p-4 rounded-xl">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gold-500/10 flex items-center justify-center">
                <svg className="w-5 h-5 text-gold-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <div>
                <p className="text-white font-medium">{account.broker_name} — {account.account_type}</p>
                <p className="text-gray-400 text-sm">Token: {account.api_token_masked}</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

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
