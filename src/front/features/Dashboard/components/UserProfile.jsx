import React from "react";

/**
 * Componente que muestra el perfil del usuario en la parte superior derecha del Dashboard.
 * Sigue la estética "Liquid Glass" del proyecto.
 */
export const UserProfile = () => {
    // Mock de datos del usuario
    const user = {
        name: "Olivia Brooks",
        email: "admin2@ftn.net",
        avatar: "https://i.pravatar.cc/150?u=olivia",
    };

    return (
        <div className="flex items-center gap-3 p-2 rounded-xl liquid-glass border border-white/10 hover:bg-white/5 transition-all cursor-pointer">
            <div className="flex flex-col items-end hidden md:flex">
                <span className="text-sm font-semibold text-white leading-none">
                    {user.name}
                </span>
                <span className="text-[10px] text-white/50 leading-tight">
                    {user.email}
                </span>
            </div>
            <div className="relative">
                <img
                    src={user.avatar}
                    alt={user.name}
                    className="w-10 h-10 rounded-lg object-cover border border-gold/30 shadow-glass-sm"
                />
                <div className="absolute -bottom-1 -right-1 w-3 h-3 bg-green-500 border-2 border-[var(--color-brown-dark)] rounded-full"></div>
            </div>
        </div>
    );
};
