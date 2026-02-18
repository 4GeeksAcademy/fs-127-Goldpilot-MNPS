import React, { useState } from "react";
import { Link } from "react-router-dom";
import { Button, Flex, Box, Text, Heading } from "@radix-ui/themes";
import { MoveRight, Plus, X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

/**
 * Componente Navbar con Menú Expandible "Vidrio Líquido".
 * Reemplaza los botones visibles por un toggle "+" que revela un menú completo.
 */
export const Navbar = () => {
    const [isOpen, setIsOpen] = useState(false);

    const toggleMenu = () => setIsOpen(!isOpen);

    return (
        <>
            <nav className="fixed top-0 left-0 w-full z-50 px-6 py-6 flex items-center justify-between">
                {/* LOGO */}
                <Flex align="center" gap="2" className="z-50 relative">
                    <div className="w-10 h-10 bg-gradient-to-br from-[var(--color-gold)] to-[#F5E6BE] rounded-full flex items-center justify-center shadow-[var(--glow-gold)]">
                        <span className="text-black font-bold text-sm">GP</span>
                    </div>
                    <span className="text-xl font-bold tracking-tighter text-white mix-blend-difference">
                        GOLDPILOT
                    </span>
                </Flex>

                {/* BOTÓN TOGGLE (+) */}
                <button
                    onClick={toggleMenu}
                    className="z-50 relative w-12 h-12 rounded-full flex items-center justify-center bg-[var(--glass-white-lighter)] backdrop-blur-md border border-white/20 text-white hover:bg-[var(--color-gold)] transition-all duration-300 shadow-[var(--shadow-glass-sm)]"
                >
                    <motion.div
                        animate={{ rotate: isOpen ? 45 : 0 }}
                        transition={{ duration: 0.2 }}
                    >
                        <Plus size={24} strokeWidth={3} />
                    </motion.div>
                </button>
            </nav>

            {/* MENÚ EXPANDIBLE OVERLAY */}
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, backdropFilter: "blur(0px)" }}
                        animate={{ opacity: 1, backdropFilter: "blur(40px)" }}
                        exit={{ opacity: 0, backdropFilter: "blur(0px)" }}
                        transition={{ duration: 0.4 }}
                        className="fixed inset-0 z-40 bg-[var(--glass-brown-dark)] flex flex-col justify-center"
                    >
                        <Box className="container mx-auto px-6 grid md:grid-cols-2 gap-12 items-center">

                            {/* IZQUIERDA: TEXTO DE RELLENO / BRANDING */}
                            <motion.div
                                initial={{ x: -50, opacity: 0 }}
                                animate={{ x: 0, opacity: 1 }}
                                transition={{ delay: 0.2 }}
                                className="hidden md:block"
                            >
                                <Heading size="9" className="text-[var(--color-gold)] mb-6 font-display leading-tight">
                                    Excelencia <br /> Líquida.
                                </Heading>
                                <Text size="5" className="text-gray-300 max-w-md font-light">
                                    {/* TODO: INSERTAR COPY FINAL MENÚ */}
                                    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                                    Invertir en oro nunca ha sido tan fluido y transparente.
                                    Descubre una nueva era de estabilidad financiera.
                                </Text>
                            </motion.div>

                            {/* DERECHA: BOTONES DE ACCIÓN */}
                            <motion.div
                                initial={{ x: 50, opacity: 0 }}
                                animate={{ x: 0, opacity: 1 }}
                                transition={{ delay: 0.3 }}
                                className="flex flex-col gap-6"
                            >
                                <Link to="/login" onClick={toggleMenu}>
                                    <h3 className="text-5xl md:text-7xl font-bold text-white hover:text-[var(--color-gold)] transition-colors cursor-pointer tracking-tighter">
                                        Acceder
                                    </h3>
                                </Link>
                                <Link to="/signup" onClick={toggleMenu}>
                                    <h3 className="text-5xl md:text-7xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-[var(--color-gold)] to-[#F5E6BE] hover:opacity-80 transition-opacity cursor-pointer tracking-tighter flex items-center gap-4">
                                        Empezar <MoveRight size={48} className="text-[var(--color-gold)]" />
                                    </h3>
                                </Link>
                            </motion.div>

                        </Box>
                    </motion.div>
                )}
            </AnimatePresence>
        </>
    );
};
