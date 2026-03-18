/**
 * ============================================================
 * GoldPilot - Bot Control Page
 * ============================================================
 * Flow:
 *   1. Select a risk level (Low / Medium / High) → calls POST /bot/strategy
 *   2. Click Start Bot → calls POST /bot/start
 *   3. Click "Evaluar Señal" → calls POST /bot/signal
 *      - WAITING: no setup right now
 *      - TRADE_PLACED: order sent to MetaAPI + recorded in DB
 * ============================================================
 */

import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { getBotStatus, startBot, stopBot, updateBotStrategy, getBotSignal, getWallets, setWalletPropFirm } from '../api';

const BASE = import.meta.env.VITE_BACKEND_URL;

const STRATEGY_OPTIONS = [
    {
        id: "low",
        label: "Low Risk",
        risk: "0.5%",
        desc: "V4 Ghost Conservative — PDH/PDL sweep, 0.5% riesgo/operación",
        color: "rgba(99,119,66,0.15)",
        textColor: "var(--color-olive)",
    },
    {
        id: "medium",
        label: "Medium Risk",
        risk: "1%",
        desc: "V4 Ghost Balanced — PDH/PDL sweep, 1% riesgo/operación",
        color: "rgba(195,143,55,0.12)",
        textColor: "var(--color-gold)",
    },
    {
        id: "high",
        label: "High Risk",
        risk: "3%",
        desc: "V4 Ghost Aggressive — PDH/PDL sweep, 3% riesgo/operación",
        color: "rgba(239,68,68,0.1)",
        textColor: "#f87171",
    },
];

const PHASE_LABELS = {
    phase1: { label: "Phase 01 — Evaluation", balance: "$5K",  color: "text-blue-400",   border: "border-blue-500/20" },
    phase2: { label: "Phase 02 — Approval",   balance: "$10K", color: "text-purple-400", border: "border-purple-500/20" },
    phase3: { label: "Phase 03 — Final",       balance: "$15K", color: "text-yellow-400", border: "border-yellow-500/20" },
    funded: { label: "Funded Account",         balance: "$20K", color: "text-green-400",  border: "border-green-500/30" },
};

const PropFirmPanel = ({ propFirm }) => {
    if (!propFirm) return null;
    const pnl         = propFirm.daily_pnl ?? 0;
    const target      = propFirm.target    ?? 300;
    const limit       = propFirm.limit     ?? -250;
    const blocked     = propFirm.blocked;
    const phase       = propFirm.phase;
    const phaseInfo   = PHASE_LABELS[phase] || { label: "Prop Firm", balance: "", color: "text-yellow-400", border: "border-yellow-500/20" };
    const progressPct = Math.min(100, Math.max(0, (Math.max(0, pnl) / target) * 100));
    const lossUsedPct = Math.min(100, Math.max(0, (Math.abs(Math.min(0, pnl)) / Math.abs(limit)) * 100));

    return (
        <div className={`glass-card p-6 border ${blocked ? 'border-red-500/40' : phaseInfo.border}`}>
            <div className="flex items-center justify-between mb-4">
                <div>
                    <h3 className={`text-sm font-bold uppercase tracking-widest ${phaseInfo.color}`}>
                        {phaseInfo.label}
                    </h3>
                    <p className="text-xs text-white/30 mt-0.5">Initial balance {phaseInfo.balance} · 1% risk per trade</p>
                </div>
                <span className={`px-2 py-1 rounded-lg text-xs font-bold ${blocked ? 'bg-red-500/20 text-red-400' : 'bg-green-500/10 text-green-400'}`}>
                    {blocked ? '⛔ BLOCKED TODAY' : '✓ Trading Allowed'}
                </span>
            </div>

            <div className="grid grid-cols-3 gap-3 mb-4">
                <div className="bg-white/5 rounded-xl p-3 text-center">
                    <p className="text-[10px] text-white/40 uppercase tracking-widest mb-1">Today's P&L</p>
                    <p className={`text-lg font-bold ${pnl >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                        {pnl >= 0 ? '+' : ''}${pnl.toFixed(2)}
                    </p>
                </div>
                <div className="bg-white/5 rounded-xl p-3 text-center">
                    <p className="text-[10px] text-white/40 uppercase tracking-widest mb-1">Profit Target</p>
                    <p className={`text-lg font-bold ${phaseInfo.color}`}>${target.toFixed(0)}</p>
                    <p className="text-[10px] text-white/30">6% of balance</p>
                </div>
                <div className="bg-white/5 rounded-xl p-3 text-center">
                    <p className="text-[10px] text-white/40 uppercase tracking-widest mb-1">Max Loss</p>
                    <p className="text-lg font-bold text-red-400">${Math.abs(limit).toFixed(0)}</p>
                    <p className="text-[10px] text-white/30">per day</p>
                </div>
            </div>

            {/* Profit progress */}
            <div className="mb-3">
                <div className="flex justify-between text-[10px] text-white/40 mb-1">
                    <span>Profit Progress</span>
                    <span>${Math.max(0, pnl).toFixed(2)} / ${target.toFixed(0)}</span>
                </div>
                <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                    <div className="h-full bg-gradient-to-r from-yellow-600 to-yellow-400 rounded-full transition-all duration-500" style={{ width: `${progressPct}%` }} />
                </div>
            </div>

            {/* Loss used */}
            <div>
                <div className="flex justify-between text-[10px] text-white/40 mb-1">
                    <span>Daily Loss Used</span>
                    <span>${Math.abs(Math.min(0, pnl)).toFixed(2)} / ${Math.abs(limit).toFixed(0)}</span>
                </div>
                <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                    <div
                        className={`h-full rounded-full transition-all duration-500 ${lossUsedPct > 80 ? 'bg-red-500' : lossUsedPct > 50 ? 'bg-orange-400' : 'bg-emerald-500'}`}
                        style={{ width: `${lossUsedPct}%` }}
                    />
                </div>
            </div>

            {phase !== 'funded' && (
                <p className="text-[10px] text-white/20 mt-3 text-center">
                    Pass this phase → advance to next · Funded account after Phase 03
                </p>
            )}
        </div>
    );
};

export const BotControlPage = () => {
    const { t } = useTranslation();
    const [botStatus, setBotStatus]         = useState(null);
    const [account, setAccount]             = useState(null);
    const [propFirm, setPropFirm]           = useState(null);
    const [wallets, setWallets]             = useState([]);
    const [selectedWalletId, setSelectedWalletId] = useState(null);
    const [selectedPhase, setSelectedPhase] = useState(null);
    const [loading, setLoading]             = useState(true);
    const [actionLoading, setActionLoading] = useState(false);
    const [strategyLoading, setStrategyLoading] = useState(false);
    const [signalLoading, setSignalLoading]     = useState(false);
    const [testTradeLoading, setTestTradeLoading] = useState(false);
    const [selectedRisk, setSelectedRisk]   = useState(null);
    const [signalResult, setSignalResult]   = useState(null);
    const [error, setError]                 = useState('');
    const [success, setSuccess]             = useState('');

    useEffect(() => {
        fetchStatus();
        getWallets().then(data => setWallets(data.wallets || data)).catch(() => {});
    }, []);

    const fetchStatus = async () => {
        try {
            const data = await getBotStatus();
            setBotStatus(data);
            setAccount(data.account);
            setPropFirm(data.prop_firm ?? null);
            if (data.strategy?.risk_level) {
                setSelectedRisk(data.strategy.risk_level);
            }
            // sync wallets with bot state
            if (data.bots) {
                setWallets(prev => prev.map(w => {
                    const bot = data.bots.find(b => b.wallet_id === w.id);
                    return bot ? { ...w, _bot: bot } : w;
                }));
            }
        } catch (err) {
            console.error('Error fetching bot status:', err);
        } finally {
            setLoading(false);
        }
    };

    const selectedWallet = wallets.find(w => w.id === selectedWalletId) || null;
    const isPropWallet   = selectedWallet?.is_prop_firm || false;

    const handleSelectStrategy = async (riskId) => {
        setSelectedRisk(riskId);
        setStrategyLoading(true);
        setError('');
        setSuccess('');
        try {
            // If prop firm wallet with a phase selected, save the phase first
            if (selectedWalletId && selectedPhase) {
                await setWalletPropFirm(selectedWalletId, selectedPhase);
            }
            await updateBotStrategy(riskId, selectedWalletId || null);
            const walletLabel = selectedWallet ? ` → ${selectedWallet.broker_name || 'Wallet #' + selectedWalletId}` : '';
            const phaseLabel  = selectedPhase ? ` (${selectedPhase})` : '';
            setSuccess(`Estrategia ${riskId.toUpperCase()} seleccionada${walletLabel}${phaseLabel}`);
            fetchStatus();
        } catch (err) {
            setError(err.message);
        } finally {
            setStrategyLoading(false);
        }
    };

    const handleStart = async (walletId = null) => {
        setActionLoading(true);
        setError('');
        setSuccess('');
        try {
            await startBot(walletId);
            setSuccess(t('botControl.started'));
            fetchStatus();
        } catch (err) {
            setError(err.message);
        } finally {
            setActionLoading(false);
        }
    };

    const handleStop = async (walletId = null) => {
        setActionLoading(true);
        setError('');
        setSuccess('');
        setSignalResult(null);
        try {
            await stopBot(walletId);
            setSuccess(t('botControl.stopped_msg'));
            fetchStatus();
        } catch (err) {
            setError(err.message);
        } finally {
            setActionLoading(false);
        }
    };

    const handleTestTrade = async (status = "open") => {
        setTestTradeLoading(true);
        setError('');
        try {
            const token = localStorage.getItem("token");
            const resp  = await fetch(`${BASE}/api/bot/manual-trade`, {
                method:  "POST",
                headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
                body: JSON.stringify({ status, profit_loss: status === "closed" ? 120.0 : null }),
            });
            const data = await resp.json();
            if (resp.ok) {
                setSuccess(`Operación de prueba insertada (${status}) — ID #${data.trade.id}`);
            } else {
                setError(data.description || "Error al insertar operación");
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setTestTradeLoading(false);
        }
    };

    const handleEvalSignal = async () => {
        setSignalLoading(true);
        setError('');
        setSignalResult(null);
        try {
            const result = await getBotSignal();
            setSignalResult(result);
        } catch (err) {
            setError(err.message);
        } finally {
            setSignalLoading(false);
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
            <h2 className="text-2xl font-bold text-white">{t('botControl.title')}</h2>

            {/* Alerts */}
            {error && (
                <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400">{error}</div>
            )}
            {success && (
                <div className="p-4 rounded-xl bg-green-500/10 border border-green-500/20 text-green-400">{success}</div>
            )}

            {/* ==================== STRATEGY SELECTOR ==================== */}
            <div className="glass-card p-6">
                <h3 className="text-sm font-semibold text-white/60 uppercase tracking-widest mb-4">
                    Seleccionar Estrategia
                </h3>

                {/* Wallet selector */}
                {wallets.length > 0 && (
                    <div className="mb-4">
                        <p className="text-[10px] text-white/40 uppercase tracking-widest mb-2">Account</p>
                        <div className="flex flex-wrap gap-2">
                            {wallets.filter(w => w.status === 'connected').map(w => {
                                const isSelected = selectedWalletId === w.id;
                                return (
                                    <button
                                        key={w.id}
                                        onClick={() => { setSelectedWalletId(isSelected ? null : w.id); setSelectedPhase(null); }}
                                        className={`px-3 py-2 rounded-xl text-xs font-medium border transition-all ${
                                            isSelected
                                                ? 'bg-gold-500/20 border-gold-500/60 text-yellow-300'
                                                : 'bg-white/5 border-white/10 text-white/50 hover:border-white/20 hover:text-white/80'
                                        }`}
                                    >
                                        <span className={`inline-block w-1.5 h-1.5 rounded-full mr-1.5 ${w.is_prop_firm ? 'bg-purple-400' : 'bg-green-400'}`} />
                                        {w.broker_name || `Wallet #${w.id}`}
                                        {w.is_prop_firm && <span className="ml-1.5 text-purple-400 text-[10px]">PROP</span>}
                                        <span className="ml-1.5 text-white/30">{w.account_type?.toUpperCase()}</span>
                                    </button>
                                );
                            })}
                        </div>
                    </div>
                )}

                {/* Phase selector — only shown for prop firm wallets */}
                {selectedWallet?.is_prop_firm !== undefined && selectedWalletId && (
                    <div className="mb-4">
                        <p className="text-[10px] text-white/40 uppercase tracking-widest mb-2">Prop Firm Phase</p>
                        <div className="flex flex-wrap gap-2">
                            {[
                                { id: 'phase1', label: 'Phase 01', sub: '$5K · $300 target · $250 limit', color: 'text-blue-400',   border: 'border-blue-500/40'   },
                                { id: 'phase2', label: 'Phase 02', sub: '$10K · $600 target · $500 limit', color: 'text-purple-400', border: 'border-purple-500/40' },
                                { id: 'phase3', label: 'Phase 03', sub: '$15K · $900 target · $750 limit', color: 'text-yellow-400', border: 'border-yellow-500/40' },
                                { id: 'funded', label: 'Funded',   sub: '$20K · $1K target · $800 limit',  color: 'text-green-400',  border: 'border-green-500/40'  },
                            ].map(p => {
                                const isSelected = selectedPhase === p.id;
                                return (
                                    <button
                                        key={p.id}
                                        onClick={() => setSelectedPhase(isSelected ? null : p.id)}
                                        className={`px-3 py-2 rounded-xl text-left border transition-all ${
                                            isSelected ? `bg-white/5 ${p.border}` : 'bg-white/3 border-white/8 hover:border-white/20'
                                        }`}
                                    >
                                        <p className={`text-xs font-bold ${isSelected ? p.color : 'text-white/50'}`}>{p.label}</p>
                                        <p className="text-[10px] text-white/30 mt-0.5">{p.sub}</p>
                                    </button>
                                );
                            })}
                        </div>
                    </div>
                )}

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    {STRATEGY_OPTIONS.map((opt) => {
                        const isActive = selectedRisk === opt.id;
                        return (
                            <button
                                key={opt.id}
                                onClick={() => handleSelectStrategy(opt.id)}
                                disabled={strategyLoading}
                                style={{
                                    background: isActive ? opt.color : "rgba(255,255,255,0.03)",
                                    border: isActive
                                        ? `1px solid ${opt.textColor}`
                                        : "1px solid rgba(255,255,255,0.08)",
                                    boxShadow: isActive ? `0 0 12px ${opt.color}` : "none",
                                }}
                                className="p-4 rounded-xl text-left transition-all duration-200 cursor-pointer"
                            >
                                <div className="flex items-center justify-between mb-2">
                                    <span
                                        className="text-sm font-bold uppercase tracking-wider"
                                        style={{ color: isActive ? opt.textColor : "rgba(255,255,255,0.5)" }}
                                    >
                                        {opt.label}
                                    </span>
                                    <span
                                        className="text-xs font-bold px-2 py-0.5 rounded-full"
                                        style={{
                                            background: opt.color,
                                            color: opt.textColor,
                                        }}
                                    >
                                        {opt.risk}
                                    </span>
                                </div>
                                <p className="text-xs text-white/30 leading-relaxed">{opt.desc}</p>
                            </button>
                        );
                    })}
                </div>
            </div>

            {/* ==================== BOT CARDS — one per wallet ==================== */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {(botStatus?.bots || []).map(bot => {
                    const isActive = bot.bot_active;
                    const isProp   = bot.account?.is_prop_firm;
                    const phase    = PHASE_LABELS[bot.account?.prop_phase] || null;
                    return (
                        <div key={bot.wallet_id} className={`glass-card p-6 border ${
                            isActive
                                ? isProp ? 'border-purple-500/30' : 'border-green-500/20'
                                : 'border-white/5'
                        }`}>
                            {/* Header */}
                            <div className="flex items-center justify-between mb-5">
                                <div className="flex items-center gap-3">
                                    <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${
                                        isActive
                                            ? isProp ? 'bg-purple-500/10 border border-purple-500/20' : 'bg-green-500/10 border border-green-500/20'
                                            : 'bg-white/5 border border-white/10'
                                    }`}>
                                        <div className={`w-3 h-3 rounded-full ${
                                            isActive
                                                ? isProp ? 'bg-purple-400 animate-pulse' : 'bg-green-400 animate-pulse'
                                                : 'bg-gray-600'
                                        }`} />
                                    </div>
                                    <div>
                                        <p className="text-sm font-bold text-white">{bot.account?.broker_name || `Wallet #${bot.wallet_id}`}</p>
                                        <p className="text-[11px] text-white/40">
                                            {isProp && phase ? `${phase.label} · ` : ''}{bot.account?.account_type?.toUpperCase()} · {bot.account?.platform?.toUpperCase()}
                                        </p>
                                    </div>
                                </div>
                                <span className={`px-2 py-1 rounded-lg text-[10px] font-bold uppercase ${
                                    isActive
                                        ? isProp ? 'bg-purple-500/20 text-purple-300' : 'bg-green-500/10 text-green-400'
                                        : 'bg-white/5 text-white/30'
                                }`}>
                                    {isActive ? 'Running' : 'Stopped'}
                                </span>
                            </div>

                            {/* Strategy info */}
                            <div className="flex items-center justify-between py-2 mb-4 border-b border-white/5">
                                <span className="text-xs text-white/40">Strategy</span>
                                <span className="text-xs font-medium text-white">
                                    {bot.strategy?.name || <span className="text-white/20">None selected</span>}
                                </span>
                            </div>

                            {/* Prop firm mini stats */}
                            {isProp && bot.prop_firm && (
                                <div className="grid grid-cols-2 gap-2 mb-4">
                                    <div className="bg-white/5 rounded-lg p-2 text-center">
                                        <p className="text-[9px] text-white/30 uppercase">Today P&L</p>
                                        <p className={`text-sm font-bold ${bot.prop_firm.daily_pnl >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                                            {bot.prop_firm.daily_pnl >= 0 ? '+' : ''}${bot.prop_firm.daily_pnl?.toFixed(2)}
                                        </p>
                                    </div>
                                    <div className="bg-white/5 rounded-lg p-2 text-center">
                                        <p className="text-[9px] text-white/30 uppercase">Max Loss</p>
                                        <p className="text-sm font-bold text-red-400">${Math.abs(bot.prop_firm.limit)}</p>
                                    </div>
                                </div>
                            )}

                            {/* Controls */}
                            <div className="flex gap-2">
                                {isActive ? (
                                    <>
                                        <button
                                            onClick={handleEvalSignal}
                                            disabled={signalLoading}
                                            className="flex-1 text-xs py-2 rounded-lg border border-yellow-500/30 bg-yellow-500/10 text-yellow-300 hover:bg-yellow-500/20 transition-all"
                                        >
                                            {signalLoading ? '...' : 'Evaluar Señal'}
                                        </button>
                                        <button
                                            onClick={() => handleStop(bot.wallet_id)}
                                            disabled={actionLoading}
                                            className="flex-1 text-xs py-2 rounded-lg border border-red-500/30 bg-red-500/10 text-red-400 hover:bg-red-500/20 transition-all"
                                        >
                                            {actionLoading ? '...' : 'Stop'}
                                        </button>
                                    </>
                                ) : (
                                    <button
                                        onClick={() => handleStart(bot.wallet_id)}
                                        disabled={actionLoading}
                                        className="flex-1 text-xs py-2 rounded-lg border border-green-500/30 bg-green-500/10 text-green-400 hover:bg-green-500/20 transition-all"
                                    >
                                        {actionLoading ? '...' : 'Start Bot'}
                                    </button>
                                )}
                            </div>

                            {/* Signal result (only shown on active bot) */}
                            {signalResult && isActive && (
                                <div className={`mt-3 p-3 rounded-xl border text-xs ${
                                    signalResult.status === "TRADE_PLACED"
                                        ? "bg-green-500/10 border-green-500/20 text-green-400"
                                        : signalResult.status === "ERROR"
                                            ? "bg-red-500/10 border-red-500/20 text-red-400"
                                            : "bg-white/5 border-white/10 text-white/40"
                                }`}>
                                    {signalResult.status === "TRADE_PLACED" ? (
                                        <>✓ {signalResult.signal?.action} @ ${signalResult.signal?.entry} · {signalResult.signal?.volume} lots</>
                                    ) : signalResult.status === "WAITING" ? (
                                        <>Waiting · PDH ${signalResult.pdh} / PDL ${signalResult.pdl}</>
                                    ) : (
                                        <>{signalResult.msg}</>
                                    )}
                                </div>
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );
};
