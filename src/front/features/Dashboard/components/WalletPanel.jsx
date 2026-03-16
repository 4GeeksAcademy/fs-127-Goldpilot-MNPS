import React, { useState, useEffect, useRef, useCallback } from "react";
import { useTranslation } from "react-i18next";
import { getWallets, addWallet, deleteWallet, getWalletConfigLink, syncWallet, getWalletBalance, searchServers } from "../api";

const PLATFORMS = [
    { value: "mt4", label: "MetaTrader 4" },
    { value: "mt5", label: "MetaTrader 5" },
];

const ACCOUNT_TYPES = [
    { value: "demo", label: "Demo" },
    { value: "live", label: "Real / Live" },
];

const inputCls = "w-full rounded-xl px-3 py-2.5 text-sm text-white bg-white/5 border border-white/10 outline-none placeholder-white/20 focus:border-white/20";

const flattenServers = (serversObj) => {
    const result = [];
    for (const [broker, servers] of Object.entries(serversObj || {})) {
        for (const server of servers) {
            result.push({ broker, server });
        }
    }
    return result;
};

const ServerSearchInput = ({ value, onChange, platform }) => {
    const { t } = useTranslation();
    const [suggestions, setSuggestions] = useState([]);
    const [open, setOpen] = useState(false);
    const [searching, setSearching] = useState(false);
    const debounceRef = useRef(null);
    const wrapperRef = useRef(null);

    const doSearch = useCallback(async (q, plat) => {
        if (q.length < 2) { setSuggestions([]); return; }
        setSearching(true);
        try {
            const res = await searchServers(q, plat);
            setSuggestions(flattenServers(res.servers));
        } catch {
            setSuggestions([]);
        } finally {
            setSearching(false);
        }
    }, []);

    const handleInput = (e) => {
        const q = e.target.value;
        onChange(q);
        setOpen(true);
        clearTimeout(debounceRef.current);
        debounceRef.current = setTimeout(() => doSearch(q, platform), 350);
    };

    const handleSelect = (serverName) => {
        onChange(serverName);
        setSuggestions([]);
        setOpen(false);
    };

    useEffect(() => {
        const handler = (e) => { if (wrapperRef.current && !wrapperRef.current.contains(e.target)) setOpen(false); };
        document.addEventListener("mousedown", handler);
        return () => document.removeEventListener("mousedown", handler);
    }, []);

    useEffect(() => {
        if (value.length >= 2) doSearch(value, platform);
    }, [platform]);

    return (
        <div ref={wrapperRef} className="relative">
            <input
                value={value}
                onChange={handleInput}
                onFocus={() => { if (suggestions.length) setOpen(true); }}
                placeholder={t("walletPanel.searchBrokerPlaceholder")}
                className={inputCls}
            />
            {searching && (
                <span className="absolute right-3 top-1/2 -translate-y-1/2 text-[10px] text-white/30">{t("walletPanel.searching")}</span>
            )}
            {open && suggestions.length > 0 && (
                <div className="absolute z-50 top-full mt-1 w-full rounded-xl border border-white/10 overflow-hidden shadow-2xl"
                    style={{ background: "#111", maxHeight: 200, overflowY: "auto" }}>
                    {suggestions.map(({ broker, server }) => (
                        <button
                            key={server}
                            type="button"
                            onMouseDown={() => handleSelect(server)}
                            className="w-full text-left px-3 py-2 hover:bg-white/5 flex flex-col gap-0.5 border-b border-white/[0.04] last:border-0">
                            <span className="text-[12px] text-white font-medium">{server}</span>
                            <span className="text-[10px] text-white/30">{broker}</span>
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
};

const ConfigLinkStep = ({ configLink, onDismiss }) => {
    const { t } = useTranslation();
    return (
        <div className="flex flex-col gap-3 p-3 rounded-xl border border-[rgba(195,143,55,0.2)]"
            style={{ background: "rgba(195,143,55,0.06)" }}>
            <div className="flex items-start gap-2">
                <span className="text-base mt-0.5">🔗</span>
                <p className="text-[11px] text-white/60 leading-relaxed">
                    {t("walletPanel.configLinkInstructions")}
                </p>
            </div>
            <div className="flex gap-2">
                <a href={configLink} target="_blank" rel="noopener noreferrer"
                    className="flex-1 py-2 rounded-xl text-xs font-semibold text-center"
                    style={{ background: "var(--color-gold)", color: "#000" }}>
                    {t("walletPanel.setupCredentials")}
                </a>
                <button onClick={onDismiss}
                    className="px-3 py-2 rounded-xl text-xs border"
                    style={{ color: "rgba(255,255,255,0.3)", borderColor: "rgba(255,255,255,0.08)" }}>
                    ✕
                </button>
            </div>
        </div>
    );
};

const WalletCard = ({ wallet, configLink, onDisconnect, onGetConfigLink, onSync, disconnecting, loadingLink, syncing }) => {
    const { t } = useTranslation();
    const isDraft = wallet.status === "draft";
    const [balance, setBalance] = useState(null); // { balance, equity, currency } | null

    useEffect(() => {
        if (!isDraft) {
            getWalletBalance(wallet.id).then(setBalance).catch(() => setBalance(null));
        }
    }, [wallet.id, isDraft]);

    return (
        <div className="flex flex-col gap-6 p-8 rounded-2xl border border-white/[0.08]"
            style={{ background: "rgba(255,255,255,0.03)" }}>

            <div className="flex items-center justify-between gap-4">
                <div className="flex items-center gap-4">
                    <div className="w-14 h-14 rounded-2xl bg-white/5 border border-white/[0.08] flex items-center justify-center text-xl font-black flex-shrink-0"
                        style={{ color: "var(--color-gold)" }}>
                        {(wallet.broker_name || wallet.server || "M")[0].toUpperCase()}
                    </div>
                    <div>
                        <p className="text-lg font-bold text-white leading-tight">
                            {wallet.broker_name || wallet.server || "MetaTrader"}
                        </p>
                        <p className="text-sm text-white/40 mt-1">
                            {wallet.platform?.toUpperCase()} · {wallet.account_type === "live" ? t("walletPanel.liveAccount") : t("walletPanel.demoAccount")}
                        </p>
                    </div>
                </div>
                <span className="flex items-center gap-2 text-xs font-bold px-3 py-1.5 rounded-full border flex-shrink-0"
                    style={isDraft
                        ? { color: "rgba(195,143,55,0.9)", background: "rgba(195,143,55,0.1)", borderColor: "rgba(195,143,55,0.25)" }
                        : { color: "#6aab45", background: "rgba(106,171,69,0.1)", borderColor: "rgba(106,171,69,0.3)" }
                    }>
                    <span className="w-2 h-2 rounded-full"
                        style={{ background: isDraft ? "rgba(195,143,55,0.9)" : "#6aab45" }} />
                    {isDraft ? t("walletPanel.pendingConfig") : t("walletPanel.connected")}
                </span>
            </div>

            {!isDraft && (
                <>
                    <div className="h-px bg-white/[0.06]" />
                    <div className="grid grid-cols-3 gap-4">
                        {[
                            { label: t("walletPanel.balance"), value: balance?.balance },
                            { label: t("walletPanel.equity"), value: balance?.equity },
                            { label: t("walletPanel.freeMargin"), value: balance?.free_margin },
                        ].map(({ label, value }) => (
                            <div key={label} className="flex flex-col gap-2 p-4 rounded-xl border border-white/[0.05]"
                                style={{ background: "rgba(255,255,255,0.02)" }}>
                                <span className="text-[11px] text-white/30 uppercase tracking-widest">{label}</span>
                                <span className="text-xl font-black leading-none"
                                    style={{ color: value != null ? "var(--color-gold)" : "rgba(255,255,255,0.15)" }}>
                                    {value != null
                                        ? Number(value).toLocaleString("es-ES", { minimumFractionDigits: 2, maximumFractionDigits: 2 })
                                        : "–"}
                                </span>
                                {value != null && balance?.currency && (
                                    <span className="text-xs text-white/25">{balance.currency}</span>
                                )}
                            </div>
                        ))}
                    </div>
                </>
            )}

            {configLink ? (
                <ConfigLinkStep configLink={configLink} onDismiss={() => onGetConfigLink(null)} />
            ) : isDraft && (
                <>
                    <div className="h-px bg-white/[0.06]" />
                    <div className="flex flex-col gap-4 p-5 rounded-xl border border-[rgba(195,143,55,0.2)]"
                        style={{ background: "rgba(195,143,55,0.04)" }}>
                        <p className="text-sm text-white/50 leading-relaxed">
                            {t("walletPanel.verifyConnectionInfo")}
                        </p>
                        <div className="flex gap-3">
                            <button onClick={() => onSync(wallet.id)} disabled={syncing}
                                className="flex-1 py-2.5 rounded-xl text-sm font-semibold border disabled:opacity-50"
                                style={{ color: "rgba(255,255,255,0.7)", borderColor: "rgba(255,255,255,0.15)", background: "rgba(255,255,255,0.05)" }}>
                                {syncing ? t("walletPanel.verifying") : t("walletPanel.verifyConnection")}
                            </button>
                            <button onClick={() => onGetConfigLink(wallet.id)} disabled={loadingLink}
                                className="flex-1 py-2.5 rounded-xl text-sm font-semibold disabled:opacity-50"
                                style={{ background: "var(--color-gold)", color: "#000" }}>
                                {loadingLink ? t("walletPanel.generating") : t("walletPanel.getLink")}
                            </button>
                        </div>
                    </div>
                </>
            )}

            <div className="h-px bg-white/[0.06]" />
            <div className="grid grid-cols-2 gap-3">
                {[
                    { label: t("walletPanel.loginAccount"), value: wallet.login || "–" },
                    { label: t("walletPanel.server"), value: wallet.server || "–" },
                    { label: t("walletPanel.platform"), value: wallet.platform?.toUpperCase() || "–" },
                    { label: t("walletPanel.registrationDate"), value: new Date(wallet.created_at).toLocaleDateString("es-ES") },
                ].map(({ label, value }) => (
                    <div key={label} className="flex flex-col gap-1 px-4 py-3 rounded-xl border border-white/[0.04]"
                        style={{ background: "rgba(255,255,255,0.015)" }}>
                        <span className="text-[11px] text-white/30 uppercase tracking-wide">{label}</span>
                        <span className="text-sm font-medium text-white/70 truncate">{value}</span>
                    </div>
                ))}
            </div>

            <div className="flex gap-3">
                <button onClick={() => onGetConfigLink(wallet.id)} disabled={loadingLink}
                    className="flex-1 py-3 rounded-xl text-sm font-semibold border disabled:opacity-40"
                    style={{ color: "var(--color-gold)", borderColor: "rgba(195,143,55,0.3)", background: "rgba(195,143,55,0.06)" }}>
                    {loadingLink ? t("walletPanel.generating") : t("walletPanel.reconfigure")}
                </button>
                <button onClick={() => onDisconnect(wallet.id)} disabled={disconnecting}
                    className="flex-1 py-3 rounded-xl text-sm font-semibold border disabled:opacity-40"
                    style={{ color: "rgba(255,80,80,0.8)", borderColor: "rgba(255,80,80,0.2)", background: "rgba(255,80,80,0.05)" }}>
                    {disconnecting ? t("walletPanel.disconnecting") : t("walletPanel.disconnectWallet")}
                </button>
            </div>
        </div>
    );
};

const AddWalletModal = ({ onClose, onSaved }) => {
    const { t } = useTranslation();
    const [form, setForm] = useState({ server: "", platform: "mt4", account_type: "demo", name: "" });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!form.server.trim()) { setError(t("walletPanel.brokerServerRequired")); return; }
        setLoading(true);
        setError("");
        try {
            const res = await addWallet(form);
            onSaved(res.wallet, res.configuration_link || "");
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4" style={{ background: "rgba(0,0,0,0.75)" }}>
            <div className="w-full max-w-md rounded-2xl border border-white/10 p-6 flex flex-col gap-5" style={{ background: "#0f0f0f" }}>
                <div className="flex items-center justify-between">
                    <h2 className="text-base font-bold text-white">{t("walletPanel.addMetaTraderAccount")}</h2>
                    <button onClick={onClose} className="text-white/30 hover:text-white text-xl leading-none">×</button>
                </div>
                <p className="text-xs text-white/40 leading-relaxed">{t("walletPanel.addAccountInstructions")}</p>
                <form onSubmit={handleSubmit} className="flex flex-col gap-3">
                    <div className="flex gap-3">
                        <div className="flex flex-col gap-1 flex-1">
                            <label className="text-[11px] text-white/40 font-medium">{t("walletPanel.platformLabel")}</label>
                            <select name="platform" value={form.platform} onChange={handleChange} className={inputCls}>
                                {PLATFORMS.map((p) => <option key={p.value} value={p.value} style={{ background: "#111" }}>{p.label}</option>)}
                            </select>
                        </div>
                        <div className="flex flex-col gap-1 w-32">
                            <label className="text-[11px] text-white/40 font-medium">{t("walletPanel.typeLabel")}</label>
                            <select name="account_type" value={form.account_type} onChange={handleChange} className={inputCls}>
                                {ACCOUNT_TYPES.map((ac) => <option key={ac.value} value={ac.value} style={{ background: "#111" }}>{ac.label}</option>)}
                            </select>
                        </div>
                    </div>
                    <div className="flex flex-col gap-1">
                        <label className="text-[11px] text-white/40 font-medium">{t("walletPanel.brokerServerLabel")}</label>
                        <ServerSearchInput
                            value={form.server}
                            onChange={(v) => setForm((f) => ({ ...f, server: v }))}
                            platform={form.platform}
                        />
                        <p className="text-[10px] text-white/20 mt-0.5">{t("walletPanel.searchBrokerHelp")}</p>
                    </div>
                    <div className="flex flex-col gap-1">
                        <label className="text-[11px] text-white/40 font-medium">{t("walletPanel.nameOptional")}</label>
                        <input name="name" value={form.name} onChange={handleChange}
                            placeholder={t("walletPanel.exampleAccountName")}
                            className={inputCls} />
                    </div>
                    {error && <p className="text-xs text-red-400">{error}</p>}
                    <button type="submit" disabled={loading}
                        className="w-full py-3 rounded-xl text-sm font-semibold mt-1 disabled:opacity-50"
                        style={{ background: "var(--color-gold)", color: "#000" }}>
                        {loading ? t("walletPanel.registeringAccount") : t("walletPanel.continue")}
                    </button>
                </form>
            </div>
        </div>
    );
};

export const WalletPanel = () => {
    const { t } = useTranslation();
    const [wallets, setWallets] = useState([]);
    const [configLinks, setConfigLinks] = useState({}); // { [wallet.id]: url }
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [disconnecting, setDisconnecting] = useState(null); // wallet id being disconnected
    const [loadingLink, setLoadingLink] = useState(null);    // wallet id fetching link
    const [syncing, setSyncing] = useState(null);            // wallet id being synced

    useEffect(() => {
        getWallets()
            .then((d) => setWallets(d.wallets || []))
            .catch(() => setWallets([]))
            .finally(() => setLoading(false));
    }, []);

    const handleSaved = (wallet, configLink) => {
        setWallets((prev) => [...prev, wallet]);
        if (configLink) setConfigLinks((prev) => ({ ...prev, [wallet.id]: configLink }));
        setShowModal(false);
    };

    const handleDisconnect = async (walletId) => {
        if (!confirm(t("walletPanel.disconnectConfirm"))) return;
        setDisconnecting(walletId);
        try {
            await deleteWallet(walletId);
            setWallets((prev) => prev.filter((w) => w.id !== walletId));
            setConfigLinks((prev) => { const next = { ...prev }; delete next[walletId]; return next; });
        } catch (e) {
            alert(e.message);
        } finally {
            setDisconnecting(null);
        }
    };

    const handleSync = async (walletId) => {
        setSyncing(walletId);
        try {
            const res = await syncWallet(walletId);
            setWallets((prev) => prev.map((w) => w.id === walletId ? res.wallet : w));
        } catch (e) {
            alert(e.message);
        } finally {
            setSyncing(null);
        }
    };

    const handleGetConfigLink = async (walletId) => {
        // null = dismiss current link banner
        if (walletId === null) { setConfigLinks((prev) => { const next = { ...prev }; return next; }); return; }
        setLoadingLink(walletId);
        try {
            const res = await getWalletConfigLink(walletId);
            setConfigLinks((prev) => ({ ...prev, [walletId]: res.configuration_link }));
        } catch (e) {
            alert(e.message);
        } finally {
            setLoadingLink(null);
        }
    };

    return (
        <>
            {showModal && <AddWalletModal onClose={() => setShowModal(false)} onSaved={handleSaved} />}

            <div className="flex flex-col gap-4">
                {/* Header row */}
                <div className="flex items-center justify-between">
                    <div>
                        <h2 className="text-sm font-semibold text-white">{t("walletPanel.metaTraderAccounts")}</h2>
                        {!loading && (
                            <p className="text-[11px] text-white/30 mt-0.5">
                                {wallets.length === 0 ? t("walletPanel.noAccountsConnected") : t("walletPanel.accountConnected", { count: wallets.length })}
                            </p>
                        )}
                    </div>
                    <button
                        onClick={() => setShowModal(true)}
                        className="flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-semibold border"
                        style={{ color: "var(--color-gold)", borderColor: "rgba(195,143,55,0.3)", background: "rgba(195,143,55,0.06)" }}>
                        {t("walletPanel.addWallet")}
                    </button>
                </div>

                {loading ? (
                    <p className="text-xs text-white/30 text-center py-8">{t("walletPanel.loading")}</p>
                ) : wallets.length === 0 ? (
                    <div className="flex flex-col items-center gap-4 py-10 rounded-2xl border border-white/[0.06]"
                        style={{ background: "rgba(255,255,255,0.02)" }}>
                        <div className="w-14 h-14 rounded-2xl bg-white/5 border border-white/[0.08] flex items-center justify-center text-3xl">◈</div>
                        <div className="text-center">
                            <p className="text-sm text-white/50">{t("walletPanel.noWalletsConnected")}</p>
                            <p className="text-xs text-white/25 mt-1 max-w-[200px]">
                                {t("walletPanel.addFirstAccount")}
                            </p>
                        </div>
                        <button onClick={() => setShowModal(true)}
                            className="px-5 py-2.5 rounded-xl text-sm font-semibold"
                            style={{ background: "var(--color-gold)", color: "#000" }}>
                            {t("walletPanel.addFirstWallet")}
                        </button>
                    </div>
                ) : (
                    /* Wallet list */
                    <div className="flex flex-col gap-6">
                        {wallets.map((wallet) => (
                            <WalletCard
                                key={wallet.id}
                                configLink={configLinks[wallet.id] || ""}
                                onDisconnect={handleDisconnect}
                                onGetConfigLink={handleGetConfigLink}
                                onSync={handleSync}
                                disconnecting={disconnecting === wallet.id}
                                loadingLink={loadingLink === wallet.id}
                                syncing={syncing === wallet.id}
                                wallet={wallet}
                            />
                        ))}
                    </div>
                )}
            </div>
        </>
    );
};
