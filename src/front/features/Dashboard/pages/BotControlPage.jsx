import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { getBotStatus, startBot, stopBot } from '../api';

export const BotControlPage = ({ selectedStrategy }) => {
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
        if (!selectedStrategy) {
            setError("Seleccione un protocolo antes de iniciar.");
            return;
        }

        setActionLoading(true);
        setError('');
        setSuccess('');
        try {
            // Enviamos el nombre de la estrategia seleccionada al API
            await startBot(selectedStrategy.name);
            setSuccess(`${t('botControl.started')}: ${selectedStrategy.name}`);
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
            {error && <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm font-mono">{error}</div>}
            {success && <div className="p-4 rounded-xl bg-green-500/10 border border-green-500/20 text-green-400 text-sm font-mono">{success}</div>}

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* STATUS CARD */}
                <div className="glass-card p-8 border border-white/5 bg-white/[0.01] rounded-3xl">
                    <div className="flex items-center gap-4 mb-6">
                        <div className={`w-16 h-16 rounded-2xl flex items-center justify-center ${botStatus?.bot_active ? 'bg-green-500/10 border border-green-500/20' : 'bg-white/5'}`}>
                            <div className={`w-6 h-6 rounded-full ${botStatus?.bot_active ? 'bg-green-400 animate-pulse shadow-lg shadow-green-500/50' : 'bg-gray-600'}`} />
                        </div>
                        <div>
                            <h3 className="text-xl font-bold text-white">
                                {botStatus?.bot_active ? t('botControl.running') : t('botControl.stopped')}
                            </h3>
                            <p className="text-gray-400 text-xs uppercase tracking-widest mt-1">System Status</p>
                        </div>
                    </div>

                    <div className="flex gap-3">
                        {botStatus?.bot_active ? (
                            <button onClick={handleStop} disabled={actionLoading} className="btn-danger flex-1 py-3 rounded-xl font-bold">
                                {actionLoading ? t('botControl.stopping') : t('botControl.stopBot')}
                            </button>
                        ) : (
                            <button 
                                onClick={handleStart} 
                                disabled={actionLoading || !selectedStrategy} 
                                className={`flex-1 py-3 rounded-xl font-bold transition-all ${
                                    !selectedStrategy 
                                    ? 'bg-white/5 text-white/20 cursor-not-allowed' 
                                    : 'bg-[var(--color-gold)] text-black shadow-lg shadow-[var(--color-gold)]/20 hover:scale-[1.02]'
                                }`}
                            >
                                {actionLoading ? t('botControl.starting') : t('botControl.startBot')}
                            </button>
                        )}
                    </div>
                </div>

                {/* CONFIG CARD */}
                <div className="glass-card p-8 border border-white/5 bg-white/[0.01] rounded-3xl">
                    <h3 className="text-xs font-black text-white/30 uppercase tracking-[0.2em] mb-6">Current Configuration</h3>
                    <div className="space-y-4">
                        <div className="flex items-center justify-between py-2 border-b border-white/5">
                            <span className="text-gray-500 text-xs italic">Selected Protocol</span>
                            <span className="text-[var(--color-gold)] font-black text-xs uppercase tracking-tighter">
                                {selectedStrategy ? selectedStrategy.name : "Waiting..."}
                            </span>
                        </div>
                        <div className="flex items-center justify-between py-2 border-b border-white/5">
                            <span className="text-gray-500 text-xs italic">Account</span>
                            <span className="text-white text-xs font-mono">{account?.broker_name || "N/A"}</span>
                        </div>
                        <div className="flex items-center justify-between py-2">
                            <span className="text-gray-500 text-xs italic">Security Mode</span>
                            <span className="text-green-500 text-[10px] font-bold border border-green-500/30 px-2 py-0.5 rounded">AUTO_SHIELD</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};