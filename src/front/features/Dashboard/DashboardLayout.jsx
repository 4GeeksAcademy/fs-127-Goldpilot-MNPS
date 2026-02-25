import React, { useState, useEffect, useRef } from "react";
import { Outlet, NavLink, useLocation } from "react-router-dom";
import { UserProfile } from "./components/UserProfile";

/**
 * Ítem de navegación del sidebar.
 * Componente reutilizable para todos los ítems del menú.
 * @param {Object} props
 * @param {string} props.label - Etiqueta visible del ítem
 * @param {string} props.icon - Emoji/icono del ítem
 * @param {string} [props.to] - Ruta de destino (si se usa como NavLink)
 * @param {boolean} [props.active] - Fuerza estado activo manualmente
 */
const SidebarItem = ({ label, icon, to, active = false }) => {
    const baseClasses =
        "relative flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-medium transition-all duration-200 cursor-pointer select-none group";

    const activeClasses =
        "bg-white/[0.06] text-white border border-white/10";

    const inactiveClasses =
        "text-white/40 hover:text-white/70 hover:bg-white/[0.03]";

    return (
        <div className={`${baseClasses} ${active ? activeClasses : inactiveClasses}`}>
            {/* Barra de luz izquierda */}
            {active && (
                <span
                    className="absolute left-0 top-1/2 -translate-y-1/2 w-[3px] h-6 rounded-r-full"
                    style={{
                        background: "var(--color-gold)",
                        boxShadow: "0 0 10px var(--color-gold), 0 0 20px rgba(195,143,55,0.4)",
                    }}
                />
            )}
            <span className={`text-base transition-colors ${active ? "text-[var(--color-gold)]" : "text-white/30 group-hover:text-white/50"}`}>
                {icon}
            </span>
            <span>{label}</span>
        </div>
    );
};

/**
 * Layout principal del Dashboard.
 * Sidebar izquierdo fijo + área de contenido principal scrollable.
 */
export const DashboardLayout = () => {
    const [activeItem, setActiveItem] = useState("Dashboard");
    const location = useLocation();
    const mainRef = useRef(null);

    /** Hace scroll al tope del área de contenido al cambiar de ruta dentro del dashboard. */
    useEffect(() => {
        if (mainRef.current) {
            mainRef.current.scrollTo({ top: 0, behavior: "smooth" });
        }
    }, [location.pathname]);

    const menuItems = [
        { label: "Dashboard", icon: "⊞" },
        { label: "Wallets", icon: "◈" },
        { label: "Historial", icon: "◳" },
    ];

    return (
        <div
            className="h-screen text-white flex overflow-hidden"
            style={{ background: "var(--color-green-dark)" }}
        >
            {/* ── SIDEBAR ── */}
            <aside
                className="w-60 h-full flex-shrink-0 hidden lg:flex flex-col py-6 px-3 gap-6 border-r border-white/[0.06]"
                style={{ background: "rgba(20, 28, 14, 0.85)", backdropFilter: "blur(24px)" }}
            >
                {/* Logo — mismo que la landing (círculo dorado XS) */}
                <div className="flex items-center gap-2.5 px-3 mb-2">
                    <div
                        className="w-8 h-8 rounded-full flex items-center justify-center text-[11px] font-black text-black flex-shrink-0"
                        style={{ background: "var(--gradient-gold)", boxShadow: "var(--glow-gold)" }}
                    >
                        XS
                    </div>
                    <span className="text-base font-bold tracking-tight text-white">
                        XSNIPER
                    </span>
                </div>

                {/* Seción MENU */}
                <div className="flex flex-col gap-1">
                    {menuItems.map((item) => (
                        <div key={item.label} onClick={() => setActiveItem(item.label)}>
                            <SidebarItem
                                label={item.label}
                                icon={item.icon}
                                active={activeItem === item.label}
                            />
                        </div>
                    ))}
                </div>
            </aside>

            {/* ── ÁREA PRINCIPAL ── */}
            <main ref={mainRef} className="flex-1 flex flex-col min-w-0 overflow-y-auto">
                {/* Header */}
                <header className="sticky top-0 z-10 w-full px-6 py-4 flex items-center gap-8 border-b border-white/[0.05]"
                    style={{ background: "rgba(20, 28, 14, 0.7)", backdropFilter: "blur(16px)" }}
                >
                    {/* Logo mobile */}
                    <div className="lg:hidden flex items-center gap-2">
                        <div
                            className="w-7 h-7 rounded-full flex items-center justify-center text-[10px] font-black text-black"
                            style={{ background: "var(--gradient-gold)" }}
                        >
                            XS
                        </div>
                        <span className="text-sm font-bold text-white">XSNIPER</span>
                    </div>
                    {/* Saludo al usuario
                     * TODO: Reemplazar texto hardcoded con el nombre real del usuario autenticado.
                     * Fuente de datos: GET /api/users/me → first_name + last_name
                     * (tabla: users, columnas: first_name, last_name)
                     */}
                    <div className="flex-1 flex flex-col hidden sm:flex">
                        <span className="text-2xl font-black tracking-tight text-white leading-none">
                            Hola, <span
                                className="font-black"
                                style={{
                                    color: "var(--color-gold)",
                                    textShadow: "0 0 24px rgba(195,143,55,0.35)",
                                }}
                            >Olivia Brooks</span>
                        </span>
                        <span className="text-xs text-white/30 mt-1 tracking-wide">
                            Bienvenida a tu estrategia ganadora
                        </span>
                    </div>
                    <UserProfile />
                </header>

                {/* Contenido dinámico */}
                <section className="px-6 py-8 w-full max-w-[1400px] mx-auto flex flex-col gap-6">
                    <Outlet />
                </section>
            </main>
        </div>
    );
};
