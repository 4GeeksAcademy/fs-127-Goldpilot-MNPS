import React, { useEffect, useRef } from "react";
import { Outlet, NavLink, useLocation, Navigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { UserProfile } from "./components/UserProfile";
import { LanguageSwitcher } from "./components/LanguageSwitcher";

/**
 * Ítem de navegación del sidebar.
 * Usa NavLink de React Router para que la URL controle el estado activo.
 */
const SidebarItem = ({ label, icon, to }) => {
    const baseClasses =
        "relative flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-medium transition-all duration-200 cursor-pointer select-none group";

    const activeClasses = "bg-white/[0.06] text-white border border-white/10";
    const inactiveClasses = "text-white/40 hover:text-white/70 hover:bg-white/[0.03] border border-transparent";

    return (
        <NavLink
            to={to}
            end={to === "/dashboard"}
            className={({ isActive }) => `${baseClasses} ${isActive ? activeClasses : inactiveClasses}`}
        >
            {({ isActive }) => (
                <>
                    {isActive && (
                        <span
                            className="absolute left-0 top-1/2 -translate-y-1/2 w-[3px] h-6 rounded-r-full"
                            style={{
                                background: "var(--color-gold)",
                                boxShadow: "0 0 10px var(--color-gold), 0 0 20px rgba(195,143,55,0.4)",
                            }}
                        />
                    )}
                    <span
                        className={`text-base transition-colors ${isActive ? "text-[var(--color-gold)]" : "text-white/30 group-hover:text-white/50"}`}
                    >
                        {icon}
                    </span>
                    <span>{label}</span>
                </>
            )}
        </NavLink>
    );
};

export const DashboardLayout = () => {
    const token = localStorage.getItem("token");
    if (!token) return <Navigate to="/login" replace />;

    const { t } = useTranslation();
    const location = useLocation();
    const mainRef = useRef(null);

    const storeUser = store?.user;
    const greeting = storeUser?.first_name || storeUser?.username || "Usuario";

    // Al recargar la página el store se reinicia: si hay token pero no user, recargar perfil
    useEffect(() => {
        if (!store?.user) {
            getProfile()
                .then((data) => dispatch({ type: "set_user_data", payload: data }))
                .catch(() => {});
        }
    }, []);

    useEffect(() => {
        if (mainRef.current) {
            mainRef.current.scrollTo({ top: 0, behavior: "smooth" });
        }
    }, [location.pathname]);

    const menuItems = [
        { label: "Dashboard", icon: "⊞", to: "/dashboard" },
        { label: "Estrategias", icon: "⌖", to: "/dashboard/strategies" },
        { label: "Wallets", icon: "◈", to: "/dashboard/wallets" },
        { label: "Historial", icon: "◳", to: "/dashboard/historial" },
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
                {/* Logo */}
                <div className="flex items-center gap-2.5 px-3 mb-2">
                    <div
                        className="w-8 h-8 rounded-full flex items-center justify-center text-[11px] font-black text-black flex-shrink-0"
                        style={{ background: "var(--gradient-gold)", boxShadow: "var(--glow-gold)" }}
                    >
                        XS
                    </div>
                    <span className="text-base font-bold tracking-tight text-white">XSNIPER</span>
                </div>

                {/* Menú */}
                <div className="flex flex-col gap-1">
                    {menuItems.map((item) => (
                        <SidebarItem
                            key={item.to}
                            label={item.label}
                            icon={item.icon}
                            to={item.to}
                        />
                    ))}
                </div>
            </aside>

            {/* ── ÁREA PRINCIPAL ── */}
            <main ref={mainRef} className="flex-1 flex flex-col min-w-0 overflow-y-auto">
                {/* Header */}
                <header
                    className="sticky top-0 z-10 w-full px-6 py-4 flex items-center gap-8 border-b border-white/[0.05]"
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
                    <div className="flex-1 flex flex-col hidden sm:flex">
                        <span className="text-2xl font-black tracking-tight text-white leading-none">
                            {t("header.greeting")} <span
                                className="font-black"
                                style={{ color: "var(--color-gold)", textShadow: "0 0 24px rgba(195,143,55,0.35)" }}
                            >{greeting}</span>
                        </span>
                        <span className="text-xs text-white/30 mt-1 tracking-wide">
                            {t("header.subtitle")}
                        </span>
                    </div>
                    <LanguageSwitcher />
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
