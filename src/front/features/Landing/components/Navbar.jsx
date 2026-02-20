import React, { useState } from "react";
import { Link } from "react-router-dom";
import { X, Globe } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

/**
 * Navbar Minimalista "Centrada" - Estructura Atlas.
 * - Trigger: Botón "GP" centrado.
 * - Modal: Card centrada con estructura: Logo -> Visual -> Botones -> Cerrar.
 */
export const Navbar = () => {
    const [isOpen, setIsOpen] = useState(false);

    const toggleMenu = () => setIsOpen((prev) => !prev);

    return (
        <>
            {/* BARRA DE NAVEGACIÓN (Centrada) */}
            <nav className="fixed top-0 left-0 w-full z-50 px-8 py-6 flex justify-center items-center pointer-events-none">

                {/* BOTÓN TRIGGER (Solo visible si el menú está cerrado para evitar duplicidad visual) */}
                <AnimatePresence>
                    {!isOpen && (
                        <motion.button
                            initial={{ scale: 0, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0, opacity: 0 }}
                            onClick={toggleMenu}
                            className="pointer-events-auto relative z-50 w-12 h-12 rounded-full flex items-center justify-center font-bold text-sm text-black transition-all duration-300 hover:scale-105 active:scale-95 shadow-[var(--glow-gold)]"
                            style={{
                                background: "var(--gradient-gold)",
                                border: "1px solid rgba(255,255,255,0.2)",
                            }}
                        >
                            XS
                        </motion.button>
                    )}
                </AnimatePresence>

            </nav>

            {/* MODAL DROPDOWN (Overlay Centrado) */}
            <AnimatePresence>
                {isOpen && (
                    <div className="fixed inset-0 z-50 flex items-center justify-center">

                        {/* BACKDROP (Clic para cerrar) */}
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className="absolute inset-0 bg-black/60 backdrop-blur-sm"
                            onClick={toggleMenu}
                        />

                        {/* CARD ESTRUCTURA ATLAS */}
                        <motion.div
                            initial={{ opacity: 0, scale: 0.9, y: 20 }}
                            animate={{ opacity: 1, scale: 1, y: 0 }}
                            exit={{ opacity: 0, scale: 0.9, y: 20 }}
                            transition={{ type: "spring", stiffness: 350, damping: 25 }}
                            className="relative z-10 w-[90%] max-w-sm rounded-[32px] overflow-hidden flex flex-col items-center"
                            style={{
                                background: "rgba(30, 30, 30, 0.75)",
                                backdropFilter: "blur(40px)",
                                WebkitBackdropFilter: "blur(40px)",
                                border: "1px solid rgba(255, 255, 255, 0.15)",
                                boxShadow: "0 40px 80px -12px rgba(0, 0, 0, 0.7)"
                            }}
                        >
                            {/* BRILLO DE FONDO */}
                            <div className="absolute top-0 inset-x-0 h-32 bg-[var(--color-gold)] opacity-20 blur-3xl pointer-events-none" />

                            <div className="flex flex-col items-center w-full p-8 pb-6 gap-8 text-center relative z-20">

                                {/* 1. LOGO HEADER */}
                                <div className="flex items-center gap-2 text-white">
                                    <div className="w-6 h-6 rounded-full bg-[var(--color-gold)] flex items-center justify-center text-[10px] font-bold text-black">XS</div>
                                    <span className="font-bold tracking-tight text-lg">XSNIPER</span>
                                </div>

                                {/* 2. VISUAL ELEMENT (Ilustración Central) */}
                                <div className="relative w-32 h-32 flex items-center justify-center">
                                    <div className="absolute inset-0 bg-[var(--color-gold)] opacity-10 blur-xl rounded-full animate-pulse" />
                                    <Globe size={80} strokeWidth={0.5} className="text-[var(--color-gold)] opacity-80" />
                                </div>

                                {/* 3. BOTONES DE ACCIÓN */}
                                <div className="w-full flex flex-col gap-3">
                                    <Link to="/login" onClick={toggleMenu} className="w-full">
                                        <button className="w-full py-4 rounded-full bg-[var(--color-gold)] text-white font-bold text-sm tracking-wide hover:bg-[#d4af37] hover:shadow-[0_0_20px_var(--color-gold)] transition-all shadow-lg backdrop-blur-sm border border-white/20 uppercase">
                                            Iniciar Sesión
                                        </button>
                                    </Link>

                                    <Link to="/signup" onClick={toggleMenu} className="w-full">
                                        <button className="w-full py-4 rounded-full bg-white/5 text-white font-bold text-sm tracking-wide border border-white/10 hover:bg-white/10 hover:border-white/30 hover:shadow-[0_0_15px_rgba(255,255,255,0.1)] backdrop-blur-md transition-all uppercase">
                                            Registrarse
                                        </button>
                                    </Link>
                                </div>

                                {/* LINEA DIVISORIA */}
                                <div className="w-full h-px bg-white/10" />

                                {/* 4. BOTÓN CERRAR (Inferior) */}
                                <button
                                    onClick={toggleMenu}
                                    className="w-10 h-10 rounded-full border border-white/20 flex items-center justify-center text-white/60 hover:text-white hover:bg-white/10 transition-colors"
                                >
                                    <X size={18} />
                                </button>

                            </div>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>
        </>
    );
};
