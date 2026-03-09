import React from "react";
import { Link, useLocation } from "react-router-dom";
import { motion } from "framer-motion";

/**
 * Navbar Horizontal Elegante
 * - Izquierda: Brand Logo.
 * - Derecha: Botones Iniciar Sesión / Registrarse.
 */
export const Navbar = () => {
    const location = useLocation();

    // No renderizar Navbar en las páginas de auth (login/signup) si no se desea.
    // Depende del diseño global, pero comúnmente en landing pages sí va.
    return (
        <nav className="fixed top-0 left-0 w-full z-50 px-8 py-4 flex justify-between items-center transition-all duration-300 bg-[var(--color-olive)]/20 backdrop-blur-lg border-b border-white/10 shadow-[var(--shadow-glass-md)]">
            {/* IZQUIERDA: Marca en cápsula iluminada para máximo contraste */}
            <Link to="/" className="flex items-center group relative cursor-pointer">
                <div className="flex justify-center items-center bg-white/15 backdrop-blur-md px-5 py-2 rounded-full border border-white/30 shadow-[0_0_15px_rgba(255,255,255,0.1)] transition-all duration-300 group-hover:bg-white/25 group-hover:shadow-[0_0_20px_rgba(255,255,255,0.2)]">
                    <img
                        src="/logo.png"
                        alt="XSniper Logo"
                        className="h-8 w-auto drop-shadow-sm transition-transform duration-300 group-hover:scale-105"
                    />
                </div>
            </Link>

            {/* DERECHA: Botones de Acción */}
            <div className="flex items-center gap-4">
                <Link to="/login">
                    <button className="px-6 py-2.5 rounded-full bg-white/5 text-white font-medium text-sm tracking-wide border border-white/10 hover:bg-white/10 hover:border-white/20 transition-all uppercase">
                        Iniciar Sesión
                    </button>
                </Link>

                <Link to="/signup">
                    <button className="px-6 py-2.5 rounded-full bg-[var(--color-gold)] text-black font-bold text-sm tracking-wide border border-transparent hover:bg-[#d4af37] hover:shadow-[0_0_20px_var(--color-gold)] transition-all uppercase">
                        Registrarse
                    </button>
                </Link>
            </div>
        </nav>
    );
};
