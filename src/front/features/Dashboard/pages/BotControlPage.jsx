import React, { useState, useEffect, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { getBotStatus, startBot, stopBot, updateBotStrategy, getBotSignal, getWallets, setWalletPropFirm } from '../api';

const RISK_OPTIONS = [
    { id: 'low',    label: 'Conservative', risk: '0.5%', desc: 'PDH/PDL sweep · 0.5% per trade', color: 'rgba(99,119,66,0.18)',   border: 'rgba(99,119,66,0.6)',   text: 'var(--color-olive)' },
    { id: 'medium', label: 'Balanced',     risk: '1%',   desc: 'PDH/PDL sweep · 1% per trade',   color: 'rgba(195,143,55,0.14)', border: 'rgba(195,143,55,0.6)', text: 'var(--color-gold)'  },
    { id: 'high',   label: 'Aggressive',   risk: '3%',   desc: 'PDH/PDL sweep · 3% per trade',   color: 'rgba(239,68,68,0.12)',  border: 'rgba(239,68,68,0.5)',  text: '#f87171'            },
];

const PHASES = [
    { id: 'phase1', label: 'Phase 01',  detail: '$5 000 account · $300 profit target · $250 daily limit',  color: '#60a5fa' },
    { id: 'phase2', label: 'Phase 02',  detail: '$10 000 account · $600 profit target · $500 daily limit', color: '#a78bfa' },
    { id: 'phase3', label: 'Phase 03',  detail: '$15 000 account · $900 profit target · $750 daily limit', color: '#fbbf24' },
    { id: 'funded', label: 'Funded',    detail: '$20 000 account · $1 000 profit target · $800 daily limit', color: '#34d399' },
];

// ── Prop Firm Progress Bar ──────────────────────────────────────────────────
const PropFirmBar = ({ propFirm }) => {
    if (!propFirm) return null;
    const pnl     = propFirm.daily_pnl ?? 0;
    const target  = propFirm.target    ?? 300;
    const limit   = Math.abs(propFirm.limit ?? 250);
    const lossPct = Math.min(100, (Math.abs(Math.min(0, pnl)) / limit) * 100);
    const gainPct = Math.min(100, (Math.max(0, pnl) / target) * 100);

    return (
        <div className="mt-3 space-y-2">
            <div>
                <div className="flex justify-between text-[9px] text-white/30 mb-1">
                    <span>Profit {pnl >= 0 ? `+$${pnl.toFixed(2)}` : ''}</span>
                    <span>Target ${target.toFixed(0)}</span>
                </div>
                <div className="h-1.5 bg-white/8 rounded-full overflow-hidden">
                    <div className="h-full bg-gradient-to-r from-yellow-600 to-yellow-400 rounded-full transition-all" style={{ width: `${gainPct}%` }} />
                </div>
            </div>
            <div>
                <div className="flex justify-between text-[9px] text-white/30 mb-1">
                    <span>Daily loss {pnl < 0 ? `-$${Math.abs(pnl).toFixed(2)}` : '$0'}</span>
                    <span>Limit ${limit.toFixed(0)}</span>
                </div>
                <div className="h-1.5 bg-white/8 rounded-full overflow-hidden">
                    <div className={`h-full rounded-full transition-all ${lossPct > 80 ? 'bg-red-500' : lossPct > 50 ? 'bg-orange-400' : 'bg-emerald-500'}`}
                        style={{ width: `${lossPct}%` }} />
                </div>
            </div>
        </div>
    );
};

// ── Single Bot Card ─────────────────────────────────────────────────────────
const BotCard = ({ bot, onStop, onStart, onEval, actionLoading, signalLoading, signalResult }) => {
    const isActive  = bot.bot_active;
    const isProp    = bot.account?.is_prop_firm;
    const phase     = PHASES.find(p => p.id === bot.account?.prop_phase);
    const pf        = bot.prop_firm;
    const isBlocked = pf?.blocked;

    return (
        <div className="rounded-2xl p-5 border transition-all"
            style={{
                background: isActive ? 'rgba(34,197,94,0.04)' : 'rgba(255,255,255,0.02)',
                borderColor: isActive ? (isBlocked ? 'rgba(239,68,68,0.4)' : 'rgba(34,197,94,0.2)') : 'rgba(255,255,255,0.07)',
            }}>

            {/* Header row */}
            <div className="flex items-start justify-between gap-3 mb-4">
                <div className="flex items-center gap-3">
                    <div className={`w-2.5 h-2.5 rounded-full mt-0.5 flex-shrink-0 ${isActive ? (isBlocked ? 'bg-red-400' : 'bg-green-400 animate-pulse') : 'bg-white/15'}`} />
                    <div>
                        <p className="text-sm font-semibold text-white leading-tight">
                            {bot.account?.broker_name || bot.account?.server || `Wallet #${bot.wallet_id}`}
                        </p>
                        <p className="text-[10px] text-white/30 mt-0.5">
                            {bot.account?.platform?.toUpperCase()} · {bot.account?.account_type === 'live' ? 'Live' : 'Demo'}
                            {isProp && phase && <span style={{ color: phase.color }}> · {phase.label}</span>}
                        </p>
                    </div>
                </div>
                <span className={`flex-shrink-0 px-2.5 py-1 rounded-lg text-[10px] font-bold uppercase tracking-wider ${
                    isBlocked ? 'bg-red-500/15 text-red-400' :
                    isActive  ? 'bg-green-500/10 text-green-400' :
                                'bg-white/5 text-white/25'
                }`}>
                    {isBlocked ? '⛔ Blocked' : isActive ? '● Active' : '○ Stopped'}
                </span>
            </div>

            {/* Strategy row */}
            <div className="flex items-center justify-between py-2 border-y border-white/5 mb-4">
                <span className="text-[10px] text-white/30 uppercase tracking-widest">Strategy</span>
                {bot.strategy ? (
                    <span className="text-xs font-semibold" style={{ color: RISK_OPTIONS.find(r => r.id === bot.strategy.risk_level)?.text || 'white' }}>
                        {bot.strategy.name} · {RISK_OPTIONS.find(r => r.id === bot.strategy.risk_level)?.risk}
                    </span>
                ) : (
                    <span className="text-xs text-white/20 italic">None selected</span>
                )}
            </div>

            {/* Prop firm stats */}
            {isProp && pf && (
                <div className="grid grid-cols-2 gap-2 mb-4">
                    <div className="bg-white/4 rounded-xl p-2.5 text-center">
                        <p className="text-[9px] text-white/30 uppercase mb-1">Today P&L</p>
                        <p className={`text-sm font-bold ${(pf.daily_pnl ?? 0) >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                            {(pf.daily_pnl ?? 0) >= 0 ? '+' : ''}${(pf.daily_pnl ?? 0).toFixed(2)}
                        </p>
                    </div>
                    <div className="bg-white/4 rounded-xl p-2.5 text-center">
                        <p className="text-[9px] text-white/30 uppercase mb-1">Daily Limit</p>
                        <p className="text-sm font-bold text-red-400">-${Math.abs(pf.limit ?? 0).toFixed(0)}</p>
                    </div>
                    <PropFirmBar propFirm={pf} />
                </div>
            )}

            {/* Controls */}
            <div className="flex gap-2">
                {isActive ? (
                    <>
                        <button onClick={() => onEval(bot.wallet_id)} disabled={signalLoading}
                            className="flex-1 py-2 rounded-xl text-xs font-medium border border-yellow-500/25 bg-yellow-500/8 text-yellow-300/80 hover:bg-yellow-500/15 transition-all disabled:opacity-40">
                            {signalLoading ? 'Evaluating…' : 'Eval Signal'}
                        </button>
                        <button onClick={() => onStop(bot.wallet_id)} disabled={actionLoading}
                            className="px-4 py-2 rounded-xl text-xs font-medium border border-red-500/25 bg-red-500/8 text-red-400/80 hover:bg-red-500/15 transition-all disabled:opacity-40">
                            {actionLoading ? '…' : 'Stop'}
                        </button>
                    </>
                ) : (
                    <button onClick={() => onStart(bot.wallet_id)} disabled={actionLoading}
                        className="flex-1 py-2 rounded-xl text-xs font-medium border border-green-500/25 bg-green-500/8 text-green-400/80 hover:bg-green-500/15 transition-all disabled:opacity-40">
                        {actionLoading ? '…' : 'Start Bot'}
                    </button>
                )}
            </div>

            {/* Signal result */}
            {signalResult && isActive && (
                <div className={`mt-3 p-3 rounded-xl text-xs border ${
                    signalResult.status === 'TRADE_PLACED' ? 'bg-green-500/8 border-green-500/20 text-green-400' :
                    signalResult.status === 'ERROR'        ? 'bg-red-500/8 border-red-500/20 text-red-400' :
                                                             'bg-white/4 border-white/8 text-white/40'
                }`}>
                    {signalResult.status === 'TRADE_PLACED'
                        ? `✓ ${signalResult.signal?.action} @ $${signalResult.signal?.entry} · ${signalResult.signal?.volume} lots`
                        : signalResult.status === 'WAITING'
                            ? `Waiting — PDH $${signalResult.pdh} / PDL $${signalResult.pdl}`
                            : (signalResult.msg || JSON.stringify(signalResult))}
                </div>
            )}
        </div>
    );
};

// ── Configure Bot Wizard ────────────────────────────────────────────────────
const ConfigureBot = ({ wallets, onApply, loading }) => {
    const [walletId,   setWalletId]   = useState(null);
    const [phase,      setPhase]      = useState(null);
    const [riskLevel,  setRiskLevel]  = useState(null);

    const selectedWallet = wallets.find(w => w.id === walletId) || null;
    const isProp         = selectedWallet?.is_prop_firm;
    const canApply       = walletId !== null && riskLevel !== null && (!isProp || phase !== null);

    const handleApply = () => {
        if (!canApply) return;
        onApply({ walletId, phase: isProp ? phase : null, riskLevel });
    };

    return (
        <div className="space-y-5">
            {/* Step 1 — Wallet */}
            <div>
                <p className="text-[10px] text-white/30 uppercase tracking-widest mb-2.5">
                    <span className="inline-flex items-center justify-center w-4 h-4 rounded-full bg-white/10 text-white/50 mr-1.5 text-[9px]">1</span>
                    Select account
                </p>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {wallets.map(w => {
                        const isSel = walletId === w.id;
                        return (
                            <button key={w.id} onClick={() => { setWalletId(w.id); setPhase(null); }}
                                className="flex items-center gap-3 p-3 rounded-xl border text-left transition-all"
                                style={{
                                    background:   isSel ? 'rgba(195,143,55,0.08)' : 'rgba(255,255,255,0.02)',
                                    borderColor:  isSel ? 'rgba(195,143,55,0.5)'  : 'rgba(255,255,255,0.07)',
                                }}>
                                <div className={`w-2 h-2 rounded-full flex-shrink-0 ${w.status === 'connected' ? 'bg-green-400' : 'bg-white/20'}`} />
                                <div className="min-w-0">
                                    <p className="text-xs font-semibold text-white truncate">
                                        {w.broker_name || w.server || `Wallet #${w.id}`}
                                    </p>
                                    <p className="text-[10px] text-white/30">
                                        {w.platform?.toUpperCase()} · {w.account_type === 'live' ? 'Live' : 'Demo'}
                                        {w.is_prop_firm && <span className="ml-1 text-yellow-400 font-semibold">PROP</span>}
                                    </p>
                                </div>
                                {isSel && <span className="ml-auto text-yellow-400 text-sm flex-shrink-0">✓</span>}
                            </button>
                        );
                    })}
                    {wallets.length === 0 && (
                        <p className="text-xs text-white/25 col-span-2">No connected wallets found.</p>
                    )}
                </div>
            </div>

            {/* Step 2 — Phase (prop firm only) */}
            {isProp && (
                <div>
                    <p className="text-[10px] text-white/30 uppercase tracking-widest mb-2.5">
                        <span className="inline-flex items-center justify-center w-4 h-4 rounded-full bg-white/10 text-white/50 mr-1.5 text-[9px]">2</span>
                        Prop firm phase
                    </p>
                    <div className="grid grid-cols-2 gap-2">
                        {PHASES.map(p => {
                            const isSel = phase === p.id;
                            return (
                                <button key={p.id} onClick={() => setPhase(p.id)}
                                    className="p-3 rounded-xl border text-left transition-all"
                                    style={{
                                        background:  isSel ? `${p.color}18` : 'rgba(255,255,255,0.02)',
                                        borderColor: isSel ? `${p.color}70` : 'rgba(255,255,255,0.07)',
                                    }}>
                                    <p className="text-xs font-bold" style={{ color: isSel ? p.color : 'rgba(255,255,255,0.45)' }}>{p.label}</p>
                                    <p className="text-[9px] text-white/25 mt-0.5 leading-snug">{p.detail}</p>
                                </button>
                            );
                        })}
                    </div>
                </div>
            )}

            {/* Step 3 — Risk level */}
            <div>
                <p className="text-[10px] text-white/30 uppercase tracking-widest mb-2.5">
                    <span className="inline-flex items-center justify-center w-4 h-4 rounded-full bg-white/10 text-white/50 mr-1.5 text-[9px]">{isProp ? '3' : '2'}</span>
                    Risk level (V4 Ghost strategy)
                </p>
                <div className="grid grid-cols-3 gap-2">
                    {RISK_OPTIONS.map(opt => {
                        const isSel = riskLevel === opt.id;
                        return (
                            <button key={opt.id} onClick={() => setRiskLevel(opt.id)}
                                className="p-3 rounded-xl border text-left transition-all"
                                style={{
                                    background:  isSel ? opt.color  : 'rgba(255,255,255,0.02)',
                                    borderColor: isSel ? opt.border : 'rgba(255,255,255,0.07)',
                                }}>
                                <div className="flex items-center justify-between mb-1">
                                    <p className="text-xs font-bold" style={{ color: isSel ? opt.text : 'rgba(255,255,255,0.45)' }}>{opt.label}</p>
                                    <span className="text-[10px] font-bold px-1.5 py-0.5 rounded-md"
                                        style={{ background: opt.color, color: opt.text }}>{opt.risk}</span>
                                </div>
                                <p className="text-[9px] text-white/25 leading-snug">{opt.desc}</p>
                            </button>
                        );
                    })}
                </div>
            </div>

            {/* Apply button */}
            <button onClick={handleApply} disabled={!canApply || loading}
                className="w-full py-3 rounded-xl text-sm font-bold uppercase tracking-wider transition-all disabled:opacity-30"
                style={{
                    background: canApply ? 'rgba(195,143,55,0.15)' : 'rgba(255,255,255,0.04)',
                    border:     canApply ? '1px solid rgba(195,143,55,0.5)' : '1px solid rgba(255,255,255,0.08)',
                    color:      canApply ? 'var(--color-gold)' : 'rgba(255,255,255,0.2)',
                }}>
                {loading ? 'Applying…' : canApply ? 'Apply & Start Bot' : `Complete steps above`}
            </button>
        </div>
    );
};

// ── Main Page ───────────────────────────────────────────────────────────────
export const BotControlPage = () => {
    const { t } = useTranslation();
    const [bots,          setBots]          = useState([]);
    const [allWallets,    setAllWallets]    = useState([]);
    const [loading,       setLoading]       = useState(true);
    const [actionLoading, setActionLoading] = useState(false);
    const [signalLoading, setSignalLoading] = useState(false);
    const [signalResult,  setSignalResult]  = useState(null);
    const [feedback,      setFeedback]      = useState(null); // { type: 'ok'|'err', msg }

    const flash = (type, msg) => {
        setFeedback({ type, msg });
        setTimeout(() => setFeedback(null), 4000);
    };

    const fetchStatus = useCallback(async () => {
        try {
            const data = await getBotStatus();
            setBots(data.bots || []);
        } catch {
            // silent
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchStatus();
        getWallets()
            .then(d => setAllWallets(d.wallets || d || []))
            .catch(() => {});
    }, [fetchStatus]);

    const handleStop = async (walletId) => {
        setActionLoading(true);
        try {
            await stopBot(walletId);
            flash('ok', 'Bot stopped.');
            fetchStatus();
        } catch (e) {
            flash('err', e.message);
        } finally {
            setActionLoading(false);
        }
    };

    const handleStart = async (walletId) => {
        setActionLoading(true);
        try {
            await startBot(walletId);
            flash('ok', 'Bot started.');
            fetchStatus();
        } catch (e) {
            flash('err', e.message);
        } finally {
            setActionLoading(false);
        }
    };

    const handleEval = async (walletId) => {
        setSignalLoading(true);
        setSignalResult(null);
        try {
            const result = await getBotSignal();
            setSignalResult(result);
        } catch (e) {
            setSignalResult({ status: 'ERROR', msg: e.message });
        } finally {
            setSignalLoading(false);
        }
    };

    const handleApply = async ({ walletId, phase, riskLevel }) => {
        setActionLoading(true);
        try {
            if (phase) await setWalletPropFirm(walletId, phase);
            await updateBotStrategy(riskLevel, walletId);
            await startBot(walletId);
            flash('ok', 'Bot configured and started.');
            fetchStatus();
        } catch (e) {
            flash('err', e.message);
        } finally {
            setActionLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center h-40">
                <div className="w-8 h-8 border-2 border-white/10 border-t-white/40 rounded-full animate-spin" />
            </div>
        );
    }

    const activeBots  = bots.filter(b => b.bot_active);
    const stoppedBots = bots.filter(b => !b.bot_active);

    return (
        <div className="space-y-8">
            {/* Feedback banner */}
            {feedback && (
                <div className={`px-4 py-3 rounded-xl text-sm border ${
                    feedback.type === 'ok'
                        ? 'bg-green-500/8 border-green-500/20 text-green-400'
                        : 'bg-red-500/8 border-red-500/20 text-red-400'
                }`}>
                    {feedback.msg}
                </div>
            )}

            {/* ── Running bots ── */}
            {activeBots.length > 0 && (
                <div>
                    <div className="flex items-center gap-2 mb-4">
                        <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
                        <h3 className="text-xs font-semibold text-white/50 uppercase tracking-widest">
                            Running — {activeBots.length} bot{activeBots.length > 1 ? 's' : ''} active
                        </h3>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {activeBots.map(bot => (
                            <BotCard key={bot.wallet_id} bot={bot}
                                onStop={handleStop} onStart={handleStart} onEval={handleEval}
                                actionLoading={actionLoading} signalLoading={signalLoading}
                                signalResult={signalResult}
                            />
                        ))}
                    </div>
                </div>
            )}

            {/* ── Stopped bots ── */}
            {stoppedBots.length > 0 && (
                <div>
                    <h3 className="text-xs font-semibold text-white/25 uppercase tracking-widest mb-4">
                        Stopped — {stoppedBots.length} bot{stoppedBots.length > 1 ? 's' : ''}
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {stoppedBots.map(bot => (
                            <BotCard key={bot.wallet_id} bot={bot}
                                onStop={handleStop} onStart={handleStart} onEval={handleEval}
                                actionLoading={actionLoading} signalLoading={signalLoading}
                                signalResult={null}
                            />
                        ))}
                    </div>
                </div>
            )}

            {/* ── Configure new bot ── */}
            <div>
                <div className="flex items-center gap-2 mb-4">
                    <span className="text-white/25">+</span>
                    <h3 className="text-xs font-semibold text-white/40 uppercase tracking-widest">Configure a bot</h3>
                </div>
                <div className="rounded-2xl p-6 border border-white/7" style={{ background: 'rgba(255,255,255,0.02)' }}>
                    <ConfigureBot
                        wallets={allWallets.filter(w => w.status === 'connected')}
                        onApply={handleApply}
                        loading={actionLoading}
                    />
                </div>
            </div>
        </div>
    );
};
