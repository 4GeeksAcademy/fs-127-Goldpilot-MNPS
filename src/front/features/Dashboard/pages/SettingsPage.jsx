import { useState, useEffect, useRef } from "react";
import { getProfile, updateProfile } from "../api";
import useGlobalReducer from "../../../hooks/useGlobalReducer";

const fmtDate = (iso) => {
    if (!iso) return "–";
    return new Date(iso).toLocaleDateString("es-ES", { day: "2-digit", month: "short", year: "numeric" });
};

const ReadField = ({ label, value }) => (
    <div className="flex items-center py-3.5 border-b border-white/[0.05] last:border-0">
        <span className="text-sm text-white/50 w-44 shrink-0">{label}</span>
        <div className="flex ml-auto w-52 items-center">
            <div className="flex-1 text-sm font-medium text-white">{value || "–"}</div>
            <div className="w-7 shrink-0 ml-3" />
        </div>
    </div>
);

const EditField = ({ label, value, onSave, saving }) => {
    const [editing, setEditing] = useState(false);
    const [draft, setDraft] = useState(value || "");
    const [error, setError] = useState("");
    const inputRef = useRef(null);

    useEffect(() => { setDraft(value || ""); }, [value]);
    useEffect(() => { if (editing) inputRef.current?.focus(); }, [editing]);

    const handleSave = async () => {
        if (!draft.trim()) { setError("Este campo no puede estar vacío"); return; }
        setError("");
        try { await onSave(draft.trim()); setEditing(false); }
        catch (e) { setError(e.message || "Error al guardar"); }
    };

    const handleCancel = () => { setDraft(value || ""); setError(""); setEditing(false); };

    return (
        <div className="py-3.5 border-b border-white/[0.05] last:border-0">
            <div className="flex items-center">
                <span className="text-sm text-white/50 w-44 shrink-0">{label}</span>
                {editing ? (
                    <div className="flex ml-auto w-52 items-center gap-2">
                        <input ref={inputRef} value={draft}
                            onChange={(e) => setDraft(e.target.value)}
                            onKeyDown={(e) => { if (e.key === "Enter") handleSave(); if (e.key === "Escape") handleCancel(); }}
                            className="text-sm text-white bg-white/[0.06] border border-white/10 rounded-lg px-3 py-1.5 w-40 focus:outline-none focus:border-[var(--color-gold)]/50"
                        />
                        <button onClick={handleSave} disabled={saving}
                            className="text-xs font-bold px-3 py-1.5 rounded-lg transition-all shrink-0"
                            style={{ background: "rgba(195,143,55,0.15)", color: "var(--color-gold)", border: "1px solid rgba(195,143,55,0.25)" }}>
                            Guardar
                        </button>
                        <button onClick={handleCancel} className="text-xs px-2 py-1.5 rounded-lg text-white/30 hover:text-white/60 transition-all">✕</button>
                    </div>
                ) : (
                    <div className="flex ml-auto w-52 items-center">
                        <div className="flex-1 text-sm font-medium text-white">{value || "–"}</div>
                        <button onClick={() => { setDraft(value || ""); setEditing(true); }}
                            className="w-7 h-7 rounded-lg flex items-center justify-center transition-all shrink-0 ml-3"
                            style={{ background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.08)" }}>
                            <span className="text-[11px] text-white/40">✎</span>
                        </button>
                    </div>
                )}
            </div>
            {error && <p className="text-xs text-red-400 mt-1.5 text-right">{error}</p>}
        </div>
    );
};

export const SettingsPage = () => {
    const { dispatch } = useGlobalReducer();
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);
    const [fetchError, setFetchError] = useState("");
    const [saving, setSaving] = useState(false);
    const [showCancelConfirm, setShowCancelConfirm] = useState(false);
    const avatarInputRef = useRef(null);
    const [avatarPreview, setAvatarPreview] = useState(null);

    useEffect(() => {
        getProfile()
            .then((data) => {
                setProfile(data);
                const saved = localStorage.getItem(`avatar_${data.id}`);
                if (saved) setAvatarPreview(saved);
            })
            .catch((e) => setFetchError(e.message || "No se pudieron cargar los datos del perfil"))
            .finally(() => setLoading(false));
    }, []);

    const handleSaveField = async (field, value) => {
        setSaving(true);
        try {
            const updated = await updateProfile({ [field]: value });
            setProfile(updated);
            dispatch({ type: "update_user", payload: { username: updated.username, first_name: updated.first_name, last_name: updated.last_name } });
        } finally {
            setSaving(false);
        }
    };

    const handleAvatarChange = (e) => {
        const file = e.target.files?.[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (ev) => {
            const base64 = ev.target.result;
            setAvatarPreview(base64);
            dispatch({ type: "set_avatar", payload: base64 });
        };
        reader.readAsDataURL(file);
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center py-24">
                <div className="w-8 h-8 rounded-full border-2 border-[var(--color-gold)]/30 border-t-[var(--color-gold)] animate-spin" />
            </div>
        );
    }

    if (fetchError) {
        return (
            <div className="flex flex-col gap-6 w-full">
                <div className="pb-2 border-b border-white/[0.05]">
                    <h1 className="text-2xl font-bold tracking-tight text-white">Ajustes</h1>
                </div>
                <div className="rounded-2xl border border-red-500/20 px-6 py-5" style={{ background: "rgba(239,68,68,0.05)" }}>
                    <p className="text-sm text-red-400">{fetchError}</p>
                    <button onClick={() => {
                        setFetchError(""); setLoading(true);
                        getProfile().then((d) => { setProfile(d); const s = localStorage.getItem(`avatar_${d.id}`); if (s) setAvatarPreview(s); })
                            .catch((e) => setFetchError(e.message)).finally(() => setLoading(false));
                    }}
                        className="mt-3 text-xs font-bold px-3 py-1.5 rounded-lg"
                        style={{ background: "rgba(195,143,55,0.15)", color: "var(--color-gold)", border: "1px solid rgba(195,143,55,0.25)" }}>
                        Reintentar
                    </button>
                </div>
            </div>
        );
    }

    const fullName = `${profile?.first_name || ""} ${profile?.last_name || ""}`.trim() || "–";
    const initials = `${(profile?.first_name || "?")[0]}${(profile?.last_name || "?")[0]}`.toUpperCase();

    return (
        <div className="flex flex-col gap-6 w-full">

            <div className="pb-2 border-b border-white/[0.05]">
                <h1 className="text-2xl font-bold tracking-tight text-white">Ajustes</h1>
            </div>

            <div className="grid grid-cols-1 xl:grid-cols-3 gap-6 items-stretch">

                {/* Columna principal: perfil */}
                <div className="xl:col-span-2 rounded-2xl border border-white/[0.06] overflow-hidden"
                    style={{ background: "rgba(255,255,255,0.03)", backdropFilter: "blur(16px)" }}>

                    <div className="px-6 py-4 border-b border-white/[0.05]">
                        <h2 className="text-sm font-semibold text-white">Ajustes del perfil</h2>
                    </div>

                    {/* Foto + resumen */}
                    <div className="px-6 pt-6 pb-5 flex items-center gap-5 border-b border-white/[0.05]">
                        <div className="relative shrink-0">
                            {avatarPreview ? (
                                <img src={avatarPreview} alt="avatar" className="w-16 h-16 rounded-2xl object-cover border border-white/10" />
                            ) : (
                                <div className="w-16 h-16 rounded-2xl flex items-center justify-center text-lg font-bold text-black"
                                    style={{ background: "var(--gradient-gold)", boxShadow: "0 0 16px rgba(195,143,55,0.3)" }}>
                                    {initials}
                                </div>
                            )}
                            <button onClick={() => avatarInputRef.current?.click()}
                                className="absolute -bottom-1.5 -right-1.5 w-6 h-6 rounded-full flex items-center justify-center text-[10px] text-black font-bold transition-all hover:scale-110"
                                style={{ background: "var(--gradient-gold)", boxShadow: "0 0 8px rgba(195,143,55,0.5)" }}
                                title="Cambiar foto">
                                ✎
                            </button>
                            <input ref={avatarInputRef} type="file" accept="image/*" className="hidden" onChange={handleAvatarChange} />
                        </div>
                        <div>
                            <p className="text-base font-bold text-white leading-tight">{fullName}</p>
                            <p className="text-xs text-white/40 mt-0.5">@{profile?.username}</p>
                            <p className="text-[11px] text-white/25 mt-1">Miembro desde {fmtDate(profile?.created_at)}</p>
                        </div>
                    </div>

                    <div className="px-6 py-2">
                        <EditField label="Usuario" value={profile?.username} saving={saving}
                            onSave={(v) => handleSaveField("username", v)} />
                        <ReadField label="Nombre completo" value={fullName} />
                        <ReadField label="Fecha de nacimiento" value={fmtDate(profile?.birth_date)} />
                        <ReadField label="Correo electrónico" value={profile?.email} />
                        <EditField label="Teléfono" value={profile?.phone_number} saving={saving}
                            onSave={(v) => handleSaveField("phone_number", v)} />
                    </div>
                </div>

                {/* Columna lateral */}
                <div className="flex flex-col gap-8 h-full">

                    <div className="rounded-2xl border border-white/[0.06] px-5 py-5"
                        style={{ background: "rgba(255,255,255,0.03)", backdropFilter: "blur(16px)" }}>
                        <h2 className="text-xs font-semibold text-white/40 uppercase tracking-wider mb-4">Estado de cuenta</h2>
                        <div className="flex flex-col gap-3">
                            <div className="flex items-center justify-between">
                                <span className="text-sm text-white/50">Estado</span>
                                <span className="text-xs font-bold px-2.5 py-1 rounded-full"
                                    style={{ background: "rgba(99,119,66,0.15)", color: "var(--color-olive)" }}>● Activa</span>
                            </div>
                            <div className="flex items-center justify-between">
                                <span className="text-sm text-white/50">Verificado</span>
                                <span className="text-xs font-bold px-2.5 py-1 rounded-full"
                                    style={{ background: "rgba(99,119,66,0.15)", color: "var(--color-olive)" }}>✓ Sí</span>
                            </div>
                            <div className="flex items-center justify-between">
                                <span className="text-sm text-white/50">Miembro desde</span>
                                <span className="text-sm font-medium text-white">{fmtDate(profile?.created_at)}</span>
                            </div>
                        </div>
                    </div>

                    <div className="mt-auto rounded-2xl border border-red-500/10 overflow-hidden"
                        style={{ background: "rgba(239,68,68,0.03)", backdropFilter: "blur(16px)" }}>
                        <div className="px-5 py-4 border-b border-red-500/[0.08]">
                            <h2 className="text-xs font-semibold text-red-400/70 uppercase tracking-wider">Zona de peligro</h2>
                        </div>
                        <div className="px-5 py-5">
                            <p className="text-sm font-medium text-white/70">Cancelar cuenta</p>
                            <p className="text-xs text-white/30 mt-1 mb-4">Esta acción es permanente e irreversible.</p>
                            {showCancelConfirm ? (
                                <div className="flex gap-2">
                                    <button className="flex-1 text-xs font-bold py-2 rounded-lg transition-all"
                                        style={{ background: "rgba(239,68,68,0.2)", color: "#f87171", border: "1px solid rgba(239,68,68,0.35)" }}
                                        onClick={() => {}}>
                                        Confirmar cancelación
                                    </button>
                                    <button className="text-xs px-3 py-2 rounded-lg text-white/30 hover:text-white/60 transition-all"
                                        onClick={() => setShowCancelConfirm(false)}>No</button>
                                </div>
                            ) : (
                                <button onClick={() => setShowCancelConfirm(true)}
                                    className="w-full text-xs font-bold py-2 rounded-lg transition-all"
                                    style={{ background: "rgba(239,68,68,0.08)", color: "rgba(239,68,68,0.6)", border: "1px solid rgba(239,68,68,0.15)" }}>
                                    Cancelar cuenta
                                </button>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};
