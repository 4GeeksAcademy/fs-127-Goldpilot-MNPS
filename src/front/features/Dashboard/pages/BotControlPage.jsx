/**
 * ============================================================
 * GoldPilot - Bot Control Page
 * ============================================================
 * Manages the trading bot.
 *
 * Sections:
 * 1. Bot Status Card — Shows if bot is running, with start/stop
 * 2. Current Configuration — Shows active strategy and account
 *
 * MetaApi connection is handled in the Wallets page.
 * ============================================================
 */

import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { getBotStatus, startBot, stopBot } from '../api';

export const BotControlPage = () => {
    const { t } = useTranslation();
    const [botStatus, setBotStatus] = useState(null);
    const [account, setAccount] = useState(null);
    const [loading, setLoading] = useState(true);
    const [actionLoading, setActionLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

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

    const handleStart = async () => {
        setActionLoading(true);
        setError('');
        setSuccess('');
        try {
            await startBot();
            setSuccess(t('botControl.started'));
            fetchStatus();
        } catch (err) {
            setError(err.message);
        } finally {
            setActionLoading(false);
        }
    };

    const handleStop = async () => {
        setActionLoading(true);
        setError('');
        setSuccess('');
        try {
            await stopBot();
            setSuccess(t('botControl.stopped_msg'));
            fetchStatus();
        } catch (err) {
            setError(err.message);
        } finally {
            setActionLoading(false);
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

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* ==================== BOT STATUS CARD ==================== */}
                <div className="glass-card p-8">
                    <div className="flex items-center gap-4 mb-6">
                        <div className={`w-16 h-16 rounded-2xl flex items-center justify-center ${botStatus?.bot_active
                            ? 'bg-green-500/10 border border-green-500/20'
                            : 'bg-dark-300 border border-gold-500/10'
                            }`}>
                            <div className={`w-6 h-6 rounded-full ${botStatus?.bot_active
                                ? 'bg-green-400 animate-pulse shadow-lg shadow-green-500/50'
                                : 'bg-gray-600'
                                }`} />
                        </div>
                        <div>
                            <h3 className="text-xl font-bold text-white">
                                {t('botControl.botIs')} {botStatus?.bot_active ? t('botControl.running') : t('botControl.stopped')}
                            </h3>
                            <p className="text-gray-400 text-sm">
                                {botStatus?.bot_active
                                    ? t('botControl.activelyTrading')
                                    : t('botControl.startPrompt')}
                            </p>
                        </div>
                    </div>

                    <div className="flex gap-3">
                        {botStatus?.bot_active ? (
                            <button
                                onClick={handleStop}
                                disabled={actionLoading}
                                className="btn-danger flex-1"
                            >
                                {actionLoading ? t('botControl.stopping') : t('botControl.stopBot')}
                            </button>
                        ) : (
                            <button
                                onClick={handleStart}
                                disabled={actionLoading}
                                className="btn-gold flex-1"
                            >
                                {actionLoading ? t('botControl.starting') : t('botControl.startBot')}
                            </button>
                        )}
                    </div>
                </div>

                {/* ==================== CURRENT CONFIG ==================== */}
                <div className="glass-card p-8">
                    <h3 className="text-lg font-semibold text-white mb-4">{t('botControl.currentConfig')}</h3>
                    <div className="space-y-4">
                        <div className="flex items-center justify-between py-3 border-b border-dark-300/50">
                            <span className="text-gray-400">{t('botControl.activeStrategy')}</span>
                            <span className="text-white font-medium">
                                {botStatus?.strategy?.name || t('botControl.noneSelected')}
                            </span>
                        </div>
                        <div className="flex items-center justify-between py-3 border-b border-dark-300/50">
                            <span className="text-gray-400">{t('botControl.brokerAccount')}</span>
                            <span className="text-white font-medium">
                                {account?.broker_name || t('botControl.notConnected')}
                            </span>
                        </div>
                        <div className="flex items-center justify-between py-3 border-b border-dark-300/50">
                            <span className="text-gray-400">{t('botControl.accountType')}</span>
                            <span className={`px-2 py-1 rounded-lg text-xs font-medium ${account?.account_type === 'live'
                                ? 'bg-red-500/10 text-red-400'
                                : 'bg-green-500/10 text-green-400'
                                }`}>
                                {account?.account_type?.toUpperCase() || t('common.na')}
                            </span>
                        </div>
                        <div className="flex items-center justify-between py-3">
                            <span className="text-gray-400">{t('botControl.connectionStatus')}</span>
                            <span className={`px-2 py-1 rounded-lg text-xs font-medium ${account?.status === 'connected'
                                ? 'bg-green-500/10 text-green-400'
                                : 'bg-gray-500/10 text-gray-400'
                                }`}>
                                {account?.status || t('common.na')}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};
