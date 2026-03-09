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
        <nav className="fixed top-0 left-0 w-full z-50 px-8 py-4 flex justify-between items-center transition-all duration-300 bg-black/50 backdrop-blur-md border-b border-white/10">
            {/* IZQUIERDA: Marca */}
            <Link to="/" className="flex items-center gap-3 group relative cursor-pointer">
                <div className="w-10 h-10 rounded-full bg-[var(--gradient-gold)] flex items-center justify-center text-xs font-bold text-black shadow-[0_0_15px_var(--glow-gold)] transition-transform group-hover:scale-105">
                    XS
                </div>
                <span className="font-bold tracking-tight text-xl text-white group-hover:text-[var(--color-gold)] transition-colors">
                    XSNIPER
                </span>
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
