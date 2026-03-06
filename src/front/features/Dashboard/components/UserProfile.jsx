import React, { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import useGlobalReducer from "../../../hooks/useGlobalReducer.jsx";

/**
 * Componente de perfil de usuario con dropdown de opciones.
 * Al hacer clic despliega: Ajustes y Cerrar Sesión.
 * Mantiene el diseño "Liquid Glass" existente.
 */
export const UserProfile = () => {
    const [isOpen, setIsOpen] = useState(false);
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

    /** Cierra el dropdown al hacer clic fuera del componente */
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

    return (
        <div className="relative" ref={dropdownRef}>
            {/* Trigger — mismo estilo que antes */}
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
                    className="absolute right-0 top-full mt-2 w-44 rounded-2xl border border-white/10 overflow-hidden z-50"
                    style={{ background: "rgba(20,28,14,0.95)", backdropFilter: "blur(20px)" }}
                >
                    <div className="flex flex-col py-1.5">
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
    );
};
