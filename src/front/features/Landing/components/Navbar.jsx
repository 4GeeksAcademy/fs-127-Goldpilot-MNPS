import React from "react";
import { Link, useLocation } from "react-router-dom";
import { motion } from "framer-motion";

export const Navbar = () => {
    const location = useLocation();

    return (
        <nav className="fixed top-0 left-0 w-full z-50 px-8 py-4 flex justify-between items-center transition-all duration-300 bg-white/10 backdrop-blur-md border-b border-white/20 shadow-[0_4px_30px_rgba(0,0,0,0.1)]">
            <Link to="/" className="flex items-center group relative cursor-pointer">
                <img
                    src="/logo.png"
                    alt="XSniper Logo"
                    className="h-10 w-auto drop-shadow-sm transition-transform duration-300 group-hover:scale-105"
                />
            </Link>

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
