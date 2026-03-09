import { useState, useRef, useEffect } from "react";
import { createPortal } from "react-dom";
import { useNavigate } from "react-router-dom";
import useGlobalReducer from "../../../hooks/useGlobalReducer.jsx";
import { getProfile } from "../api";

const fmtDate = (iso) => {
    if (!iso) return "–";
    return new Date(iso).toLocaleDateString("es-ES", { day: "2-digit", month: "long", year: "numeric" });
};

const ProfileModal = ({ onClose, storeUser, avatarSrc }) => {
    const [profile, setProfile] = useState(null);

    useEffect(() => {
        getProfile().then(setProfile).catch(() => {});
    }, []);

    const fullName = storeUser
        ? `${storeUser.first_name || ""} ${storeUser.last_name || ""}`.trim() || storeUser.username
        : "–";
    const initials = storeUser
        ? `${(storeUser.first_name || storeUser.username || "?")[0]}${(storeUser.last_name || "?")[0]}`.toUpperCase()
        : "?";

    // Cerrar con Escape
    useEffect(() => {
        const onKey = (e) => { if (e.key === "Escape") onClose(); };
        document.addEventListener("keydown", onKey);
        return () => document.removeEventListener("keydown", onKey);
    }, [onClose]);

    return createPortal(
        <div
            className="fixed inset-0 z-[100] flex items-center justify-center p-6"
            style={{ background: "rgba(0,0,0,0.65)", backdropFilter: "blur(16px)" }}
            onClick={onClose}
        >
            <div
                className="relative w-full max-w-lg rounded-3xl border border-white/[0.08]"
                style={{ background: "rgba(20,28,14,0.97)", backdropFilter: "blur(40px)", boxShadow: "0 40px 100px rgba(0,0,0,0.7), 0 0 0 1px rgba(255,255,255,0.04)" }}
                onClick={(e) => e.stopPropagation()}
            >
                {/* Botón cerrar */}
                <button
                    onClick={onClose}
                    className="absolute top-5 right-5 w-8 h-8 rounded-full flex items-center justify-center text-white/40 hover:text-white/80 transition-all z-10"
                    style={{ background: "rgba(255,255,255,0.07)", border: "1px solid rgba(255,255,255,0.1)" }}
                >
                    ✕
                </button>

                {/* Banda superior dorada */}
                <div
                    className="h-32 w-full rounded-t-3xl"
                    style={{ background: "linear-gradient(135deg, rgba(195,143,55,0.22) 0%, rgba(195,143,55,0.06) 100%)" }}
                />

                {/* Avatar centrado, solapando la banda */}
                <div className="flex flex-col items-center -mt-14 px-8 pb-8">
                    <div className="relative">
                        {avatarSrc ? (
                            <img
                                src={avatarSrc}
                                alt={fullName}
                                className="w-28 h-28 rounded-full object-cover border-4 border-[rgba(20,28,14,1)]"
                                style={{ boxShadow: "0 0 0 2px rgba(195,143,55,0.4), 0 12px 40px rgba(0,0,0,0.6)" }}
                            />
                        ) : (
                            <div
                                className="w-28 h-28 rounded-full flex items-center justify-center text-3xl font-black text-black border-4 border-[rgba(20,28,14,1)]"
                                style={{ background: "var(--gradient-gold)", boxShadow: "0 0 0 2px rgba(195,143,55,0.4), 0 12px 40px rgba(195,143,55,0.3)" }}
                            >
                                {initials}
                            </div>
                        )}
                        <div className="absolute bottom-1 right-1 w-5 h-5 bg-green-500 border-2 border-[rgba(20,28,14,1)] rounded-full" />
                    </div>

                    {/* Nombre y username */}
                    <h2 className="mt-4 text-2xl font-black text-white text-center leading-tight">{fullName}</h2>
                    <p className="text-sm text-white/40 mt-1 text-center">@{storeUser?.username}</p>

                    <span
                        className="mt-3 text-[11px] font-bold px-3 py-1 rounded-full"
                        style={{ background: "rgba(195,143,55,0.12)", color: "var(--color-gold)", border: "1px solid rgba(195,143,55,0.2)" }}
                    >
                        ● Cuenta activa
                    </span>

                    {/* Separador */}
                    <div className="w-full h-px mt-7 mb-5" style={{ background: "rgba(255,255,255,0.06)" }} />

                    {/* Datos */}
                    <div className="w-full flex flex-col gap-0 rounded-2xl overflow-hidden border border-white/[0.06]">
                        {[
                            { label: "Correo electrónico", value: storeUser?.email },
                            { label: "Teléfono", value: profile?.phone_number },
                            { label: "Fecha de nacimiento", value: fmtDate(profile?.birth_date) },
                            { label: "Miembro desde", value: fmtDate(profile?.created_at) },
                        ].map(({ label, value }, i) => (
                            <div
                                key={label}
                                className="flex items-center justify-between px-5 py-3.5 border-b border-white/[0.04] last:border-0"
                                style={{ background: i % 2 === 0 ? "rgba(255,255,255,0.02)" : "transparent" }}
                            >
                                <span className="text-xs text-white/40">{label}</span>
                                <span className="text-sm font-medium text-white">{value || "–"}</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>,
        document.body
    );
};

export const UserProfile = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [showProfile, setShowProfile] = useState(false);
    const dropdownRef = useRef(null);
    const navigate = useNavigate();
    const { store, dispatch } = useGlobalReducer();

    const storeUser = store?.user;
    const fullName = storeUser
        ? `${storeUser.first_name || ""} ${storeUser.last_name || ""}`.trim() || storeUser.username
        : "–";
    const email = storeUser?.email || "";
    const userId = storeUser?.id;
    const avatarSrc = storeUser?.avatar ?? (userId ? localStorage.getItem(`avatar_${userId}`) : null);
    const initials = storeUser
        ? `${(storeUser.first_name || storeUser.username || "?")[0]}`.toUpperCase()
        : "?";

    useEffect(() => {
        const handleClickOutside = (e) => {
            if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
                setIsOpen(false);
            }
        };
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    const handleLogout = () => {
        setIsOpen(false);
        dispatch({ type: "logout" });
        navigate("/");
    };

    const handleSettings = () => {
        setIsOpen(false);
        navigate("/dashboard/ajustes");
    };

    const handleViewProfile = () => {
        setIsOpen(false);
        setShowProfile(true);
    };

    return (
        <>
            <div className="relative" ref={dropdownRef}>
                {/* Trigger */}
                <button
                    onClick={() => setIsOpen((prev) => !prev)}
                    className="flex items-center gap-3 p-2 pl-3 rounded-xl liquid-glass border border-white/10 hover:bg-white/5 transition-all cursor-pointer"
                >
                    <div className="flex flex-col items-end hidden md:flex">
                        <span className="text-sm font-semibold text-white leading-none">{fullName}</span>
                        <span className="text-[10px] text-white/50 leading-tight">{email}</span>
                    </div>
                    <span className="text-white/40 text-xs transition-transform duration-200"
                        style={{ transform: isOpen ? "rotate(180deg)" : "rotate(0deg)" }}>
                        ▾
                    </span>
                    <div className="relative">
                        {avatarSrc ? (
                            <img src={avatarSrc} alt={fullName}
                                className="w-10 h-10 rounded-lg object-cover border border-white/10" />
                        ) : (
                            <div className="w-10 h-10 rounded-lg flex items-center justify-center text-sm font-bold text-black"
                                style={{ background: "var(--gradient-gold)" }}>
                                {initials}
                            </div>
                        )}
                        <div className="absolute -bottom-1 -right-1 w-3 h-3 bg-green-500 border-2 border-[var(--color-brown-dark)] rounded-full" />
                    </div>
                </button>

                {/* Dropdown */}
                {isOpen && (
                    <div
                        className="absolute right-0 top-full mt-2 w-48 rounded-2xl border border-white/10 overflow-hidden z-50"
                        style={{ background: "rgba(20,28,14,0.95)", backdropFilter: "blur(20px)" }}
                    >
                        <div className="flex flex-col py-1.5">
                            {/* Ver perfil */}
                            <button
                                onClick={handleViewProfile}
                                className="flex items-center gap-3 px-4 py-3 text-sm text-white/70 hover:text-white hover:bg-white/[0.05] transition-all text-left w-full"
                            >
                                <span className="text-base">◉</span>
                                Ver perfil
                            </button>

                            {/* Ajustes */}
                            <button
                                onClick={handleSettings}
                                className="flex items-center gap-3 px-4 py-3 text-sm text-white/70 hover:text-white hover:bg-white/[0.05] transition-all text-left w-full"
                            >
                                <span className="text-base">⚙</span>
                                Ajustes
                            </button>

                            {/* Separador */}
                            <div className="h-px mx-3 my-1" style={{ background: "rgba(255,255,255,0.06)" }} />

                            {/* Cerrar sesión */}
                            <button
                                onClick={handleLogout}
                                className="flex items-center gap-3 px-4 py-3 text-sm text-red-400 hover:text-red-300 hover:bg-red-500/[0.06] transition-all text-left w-full"
                            >
                                <span className="text-base">⎋</span>
                                Cerrar sesión
                            </button>
                        </div>
                    </div>
                )}
            </div>

            {/* Modal de perfil */}
            {showProfile && (
                <ProfileModal
                    onClose={() => setShowProfile(false)}
                    storeUser={storeUser}
                    avatarSrc={avatarSrc}
                />
            )}
        </>
    );
};
