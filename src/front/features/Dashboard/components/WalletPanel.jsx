import React, { useState, useEffect, useRef, useCallback } from "react";
import { getWallet, connectWallet, disconnectWallet, searchServers, getConfigLink } from "../api";

const PLATFORMS = [
    { value: "mt4", label: "MetaTrader 4" },
    { value: "mt5", label: "MetaTrader 5" },
];

const ACCOUNT_TYPES = [
    { value: "demo", label: "Demo" },
    { value: "live", label: "Real / Live" },
];

const inputCls = "w-full rounded-xl px-3 py-2.5 text-sm text-white bg-white/5 border border-white/10 outline-none placeholder-white/20 focus:border-white/20";

/** Flattens MetaApi server response { "Broker": ["Server1", "Server2"] } into flat list */
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
                placeholder="Escribe tu broker o servidor..."
                className={inputCls}
            />
            {searching && (
                <span className="absolute right-3 top-1/2 -translate-y-1/2 text-[10px] text-white/30">buscando...</span>
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

/** Step 2 view shown after account is created in DRAFT state */
const ConfigLinkStep = ({ configLink, onDone }) => (
    <div className="flex flex-col gap-4">
        <div className="flex items-start gap-3 p-4 rounded-xl border border-[rgba(195,143,55,0.2)]"
            style={{ background: "rgba(195,143,55,0.06)" }}>
            <span className="text-lg mt-0.5">🔗</span>
            <div className="flex flex-col gap-1">
                <p className="text-sm font-semibold text-white">Paso 2: Configura tus credenciales</p>
                <p className="text-[11px] text-white/50 leading-relaxed">
                    Tu cuenta MetaTrader fue registrada. Ahora haz clic en el enlace de abajo para ingresar
                    tu número de cuenta y contraseña de forma segura en MetaApi.
                    El enlace expira en 7 días.
                </p>
            </div>
        </div>
        <a
            href={configLink}
            target="_blank"
            rel="noopener noreferrer"
            className="w-full py-3 rounded-xl text-sm font-semibold text-center block"
            style={{ background: "var(--color-gold)", color: "#000" }}>
            Configurar credenciales MT →
        </a>
        <button
            onClick={onDone}
            className="w-full py-2.5 rounded-xl text-sm font-medium border text-center"
            style={{ color: "rgba(255,255,255,0.4)", borderColor: "rgba(255,255,255,0.08)", background: "transparent" }}>
            Ya lo configuré
        </button>
    </div>
);

const AddWalletModal = ({ onClose, onSaved }) => {
    const [form, setForm] = useState({
        server: "", platform: "mt4", account_type: "demo", name: "",
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [configLink, setConfigLink] = useState("");

    const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!form.server.trim()) {
            setError("El servidor del broker es obligatorio.");
            return;
        }
        setLoading(true);
        setError("");
        try {
            const res = await connectWallet(form);
            setConfigLink(res.configuration_link || "");
            onSaved(res.wallet, res.configuration_link || "");
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    if (configLink) {
        return (
            <div className="fixed inset-0 z-50 flex items-center justify-center p-4" style={{ background: "rgba(0,0,0,0.7)" }}>
                <div className="w-full max-w-md rounded-2xl border border-white/10 p-6 flex flex-col gap-5" style={{ background: "#0f0f0f" }}>
                    <div className="flex items-center justify-between">
                        <h2 className="text-base font-bold text-white">Cuenta registrada</h2>
                        <button onClick={onClose} className="text-white/30 hover:text-white text-xl leading-none">×</button>
                    </div>
                    <ConfigLinkStep configLink={configLink} onDone={onClose} />
                </div>
            </div>
        );
    }

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4" style={{ background: "rgba(0,0,0,0.7)" }}>
            <div className="w-full max-w-md rounded-2xl border border-white/10 p-6 flex flex-col gap-5" style={{ background: "#0f0f0f" }}>
                <div className="flex items-center justify-between">
                    <h2 className="text-base font-bold text-white">Conectar cuenta MetaTrader</h2>
                    <button onClick={onClose} className="text-white/30 hover:text-white text-xl leading-none">×</button>
                </div>
                <p className="text-xs text-white/40 leading-relaxed">
                    Elige tu broker y plataforma. Luego recibirás un enlace seguro para ingresar
                    tus credenciales MT directamente en MetaApi — tu contraseña <strong className="text-white/60">nunca pasa por nuestros servidores</strong>.
                </p>
                <form onSubmit={handleSubmit} className="flex flex-col gap-3">
                    <div className="flex gap-3">
                        <div className="flex flex-col gap-1 flex-1">
                            <label className="text-[11px] text-white/40 font-medium">Plataforma</label>
                            <select name="platform" value={form.platform} onChange={handleChange}
                                className={inputCls}>
                                {PLATFORMS.map((p) => <option key={p.value} value={p.value} style={{ background: "#111" }}>{p.label}</option>)}
                            </select>
                        </div>
                        <div className="flex flex-col gap-1 w-32">
                            <label className="text-[11px] text-white/40 font-medium">Tipo</label>
                            <select name="account_type" value={form.account_type} onChange={handleChange}
                                className={inputCls}>
                                {ACCOUNT_TYPES.map((t) => <option key={t.value} value={t.value} style={{ background: "#111" }}>{t.label}</option>)}
                            </select>
                        </div>
                    </div>
                    <div className="flex flex-col gap-1">
                        <label className="text-[11px] text-white/40 font-medium">Servidor del broker *</label>
                        <ServerSearchInput
                            value={form.server}
                            onChange={(v) => setForm((f) => ({ ...f, server: v }))}
                            platform={form.platform}
                        />
                        <p className="text-[10px] text-white/20 mt-0.5">Escribe el nombre de tu broker para ver los servidores disponibles</p>
                    </div>
                    <div className="flex flex-col gap-1">
                        <label className="text-[11px] text-white/40 font-medium">Nombre (opcional)</label>
                        <input name="name" value={form.name} onChange={handleChange}
                            placeholder="ej: Mi cuenta Exness demo"
                            className={inputCls} />
                    </div>
                    {error && <p className="text-xs text-red-400">{error}</p>}
                    <button type="submit" disabled={loading} className="w-full py-3 rounded-xl text-sm font-semibold mt-1 disabled:opacity-50"
                        style={{ background: "var(--color-gold)", color: "#000" }}>
                        {loading ? "Registrando cuenta..." : "Continuar →"}
                    </button>
                </form>
            </div>
        </div>
    );
};

export const WalletPanel = () => {
    const [wallet, setWallet] = useState(null);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [disconnecting, setDisconnecting] = useState(false);
    const [pendingConfigLink, setPendingConfigLink] = useState("");
    const [loadingLink, setLoadingLink] = useState(false);

    useEffect(() => {
        getWallet().then((d) => setWallet(d.wallet)).catch(() => setWallet(null)).finally(() => setLoading(false));
    }, []);

    const handleDisconnect = async () => {
        if (!confirm("¿Desconectar esta wallet?")) return;
        setDisconnecting(true);
        try { await disconnectWallet(); setWallet(null); setPendingConfigLink(""); }
        catch (e) { alert(e.message); }
        finally { setDisconnecting(false); }
    };

    const handleGetConfigLink = async () => {
        setLoadingLink(true);
        try {
            const res = await getConfigLink();
            setPendingConfigLink(res.configuration_link || "");
        } catch (e) {
            alert(e.message);
        } finally {
            setLoadingLink(false);
        }
    };

    return (
        <>
            {showModal && (
                <AddWalletModal
                    onClose={() => setShowModal(false)}
                    onSaved={(w, link) => {
                        setWallet(w);
                        setPendingConfigLink(link);
                        setShowModal(false);
                    }}
                />
            )}
            <div className="rounded-2xl p-5 flex flex-col gap-5 border border-white/[0.06]" style={{ background: "rgba(255,255,255,0.03)", backdropFilter: "blur(16px)" }}>
                <div className="flex items-center justify-between gap-3">
                    <h2 className="text-sm font-semibold text-white">Cuenta MetaTrader</h2>
                    {wallet && (
                        <span className="flex items-center gap-1.5 text-[11px] font-bold px-2.5 py-1 rounded-full border"
                            style={
                                wallet.status === "draft"
                                    ? { color: "rgba(195,143,55,0.9)", background: "rgba(195,143,55,0.1)", borderColor: "rgba(195,143,55,0.2)" }
                                    : { color: "var(--color-olive)", background: "rgba(99,119,66,0.12)", borderColor: "rgba(99,119,66,0.2)" }
                            }>
                            <span className="w-1.5 h-1.5 rounded-full inline-block"
                                style={{ background: wallet.status === "draft" ? "rgba(195,143,55,0.9)" : "var(--color-olive)" }} />
                            {wallet.status === "draft" ? "Pendiente" : "Conectado"}
                        </span>
                    )}
                </div>

                {loading ? (
                    <p className="text-xs text-white/30 text-center py-4">Cargando...</p>
                ) : wallet ? (
                    <>
                        {/* Pending config banner */}
                        {(pendingConfigLink || wallet.status === "draft") && (
                            <div className="flex flex-col gap-3">
                                {pendingConfigLink ? (
                                    <ConfigLinkStep configLink={pendingConfigLink} onDone={() => setPendingConfigLink("")} />
                                ) : (
                                    <div className="flex flex-col gap-2 p-4 rounded-xl border border-[rgba(195,143,55,0.2)]"
                                        style={{ background: "rgba(195,143,55,0.06)" }}>
                                        <p className="text-[11px] text-white/60 leading-relaxed">
                                            Esta cuenta aún no tiene credenciales configuradas. Genera un enlace seguro para completar la configuración.
                                        </p>
                                        <button onClick={handleGetConfigLink} disabled={loadingLink}
                                            className="py-2 rounded-xl text-xs font-semibold disabled:opacity-50"
                                            style={{ background: "var(--color-gold)", color: "#000" }}>
                                            {loadingLink ? "Generando enlace..." : "Obtener enlace de configuración"}
                                        </button>
                                    </div>
                                )}
                            </div>
                        )}

                        <div className="flex flex-col gap-3 p-4 rounded-xl border border-white/[0.05]" style={{ background: "rgba(255,255,255,0.02)" }}>
                            <div className="flex items-center gap-3">
                                <div className="w-9 h-9 rounded-xl bg-white/5 border border-white/[0.08] flex items-center justify-center text-sm font-bold flex-shrink-0"
                                    style={{ color: "var(--color-gold)" }}>
                                    {(wallet.broker_name || wallet.server || "M")[0].toUpperCase()}
                                </div>
                                <div>
                                    <p className="text-sm font-semibold text-white">{wallet.broker_name || wallet.server || "MetaTrader"}</p>
                                    <p className="text-[11px] text-white/30 mt-0.5">
                                        {wallet.platform?.toUpperCase()} · {wallet.account_type === "live" ? "Real" : "Demo"}
                                    </p>
                                </div>
                            </div>
                        </div>
                        <div className="flex flex-col divide-y divide-white/[0.04]">
                            {[
                                { label: "Servidor", value: wallet.server || "–" },
                                { label: "Plataforma", value: wallet.platform?.toUpperCase() || "–" },
                                { label: "Tipo de cuenta", value: wallet.account_type === "live" ? "Real / Live" : "Demo" },
                                { label: "Estado", value: wallet.status === "draft" ? "Pendiente configuración" : wallet.status },
                                { label: "Registrado el", value: new Date(wallet.created_at).toLocaleDateString("es-ES") },
                            ].map(({ label, value }) => (
                                <div key={label} className="flex items-center justify-between px-1 py-2.5">
                                    <span className="text-[11px] text-white/30">{label}</span>
                                    <span className="text-[11px] font-semibold text-white/70 truncate max-w-[160px]">{value}</span>
                                </div>
                            ))}
                        </div>
                        <div className="flex flex-col gap-2">
                            {wallet.status !== "draft" && (
                                <button onClick={handleGetConfigLink} disabled={loadingLink}
                                    className="w-full py-2.5 rounded-xl text-sm font-semibold border text-center disabled:opacity-40"
                                    style={{ color: "var(--color-gold)", borderColor: "rgba(195,143,55,0.3)", background: "rgba(195,143,55,0.06)" }}>
                                    {loadingLink ? "Generando..." : "Reconfigurar credenciales"}
                                </button>
                            )}
                            <button onClick={() => setShowModal(true)} className="w-full py-2.5 rounded-xl text-sm font-semibold border text-center"
                                style={{ color: "rgba(255,255,255,0.5)", borderColor: "rgba(255,255,255,0.08)", background: "transparent" }}>
                                Cambiar Wallet
                            </button>
                            <button onClick={handleDisconnect} disabled={disconnecting} className="w-full py-2.5 rounded-xl text-sm font-semibold border text-center disabled:opacity-40"
                                style={{ color: "rgba(255,80,80,0.8)", borderColor: "rgba(255,80,80,0.15)", background: "rgba(255,80,80,0.04)" }}>
                                {disconnecting ? "Desconectando..." : "Desconectar"}
                            </button>
                        </div>
                    </>
                ) : (
                    <>
                        <div className="flex flex-col items-center gap-3 py-4 text-center">
                            <div className="w-12 h-12 rounded-2xl bg-white/5 border border-white/[0.08] flex items-center justify-center text-2xl">◈</div>
                            <p className="text-sm text-white/50">No hay wallet conectada</p>
                            <p className="text-xs text-white/25 leading-relaxed max-w-[180px]">Selecciona tu broker y plataforma para conectar tu cuenta MT4/MT5</p>
                        </div>
                        <button onClick={() => setShowModal(true)} className="w-full py-3 rounded-xl text-sm font-semibold border text-center"
                            style={{ color: "var(--color-gold)", borderColor: "rgba(195,143,55,0.3)", background: "rgba(195,143,55,0.06)" }}>
                            + Añadir Wallet
                        </button>
                    </>
                )}
            </div>
        </>
    );
};
