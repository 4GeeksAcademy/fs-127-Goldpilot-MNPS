import React, { useState, useRef, useEffect } from "react";

/**
 * Componente de perfil de usuario con dropdown de opciones.
 * Al hacer clic despliega: Ajustes y Cerrar Sesión.
 * Mantiene el diseño "Liquid Glass" existente.
 */
export const UserProfile = () => {
    const [isOpen, setIsOpen] = useState(false);
    const dropdownRef = useRef(null);

    // Datos mock del usuario — TODO: reemplazar con contexto de autenticación JWT
    const user = {
        name: "Olivia Brooks",
        email: "admin2@ftn.net",
        avatar: "https://i.pravatar.cc/150?u=olivia",
    };

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

    /** Manejador de cierre de sesión — TODO: conectar con POST /api/auth/logout */
    const handleLogout = () => {
        setIsOpen(false);
        // TODO: dispatch logout action / clear JWT token
        console.log("Cerrar sesión");
    };

    return (
        <div className="relative" ref={dropdownRef}>
            {/* Trigger — mismo estilo que antes */}
            <button
                onClick={() => setIsOpen((prev) => !prev)}
                className="flex items-center gap-3 p-2 pl-3 rounded-xl liquid-glass border border-white/10 hover:bg-white/5 transition-all cursor-pointer"
            >
                <div className="flex flex-col items-end hidden md:flex">
                    <span className="text-sm font-semibold text-white leading-none">
                        {user.name}
                    </span>
                    <span className="text-[10px] text-white/50 leading-tight">
                        {user.email}
                    </span>
                </div>
                {/* Chevron — indica que hay un menú desplegable */}
                <span
                    className="text-white/40 text-xs transition-transform duration-200"
                    style={{ transform: isOpen ? "rotate(180deg)" : "rotate(0deg)" }}
                >
                    ▾
                </span>
                <div className="relative">
                    <img
                        src={user.avatar}
                        alt={user.name}
                        className="w-10 h-10 rounded-lg object-cover border border-gold/30 shadow-glass-sm"
                    />
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
                            onClick={() => setIsOpen(false)}
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
