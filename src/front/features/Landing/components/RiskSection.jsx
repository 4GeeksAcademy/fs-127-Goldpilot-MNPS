import React from "react";
import { Container } from "@radix-ui/themes";
import { motion } from "framer-motion";

/**
 * Sección Minimalista Tipográfica - VERSIÓN BALANCEADA (Sin Botón).
 * - Espaciado: Aumentado para generar una sensación de lujo y "aire".
 * - Tipografía: El centro absoluto de la atención.
 */
export const RiskSection = () => {
    return (
        <section className="relative w-full pt-52 pb-60 bg-black flex items-center justify-center overflow-hidden">

            {/* FONDO LIMPIO */}
            <div className="absolute inset-0 bg-black z-0 pointer-events-none" />

            <Container size="3" className="relative z-10 px-6 text-center">
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, ease: "easeOut" }}
                    viewport={{ once: true, margin: "-10%" }}
                    className="flex flex-col items-center gap-12" // GAP AUMENTADO para mejor equilibrio
                >
                    {/* TÍTULO PRINCIPAL */}
                    <div className="flex flex-col items-center leading-[0.9] tracking-tighter">

                        {/* LÍNEA 1: Blanco puro */}
                        <h2 className="text-5xl md:text-7xl lg:text-8xl font-medium text-white text-center">
                            Más allá del riesgo.
                        </h2>

                        {/* LÍNEA 2: Dorado con Esfumado */}
                        <h2
                            className="text-5xl md:text-7xl lg:text-8xl font-medium text-center"
                            style={{
                                background: "linear-gradient(180deg, #FFFFFF 0%, var(--color-gold) 100%)",
                                WebkitBackgroundClip: "text",
                                WebkitTextFillColor: "transparent",
                                paddingBottom: "0.1em"
                            }}
                        >
                            Pura certeza.
                        </h2>
                    </div>

                    {/* BLOQUE DE TEXTO ESTRUCTURADO */}
                    <div
                        style={{
                            textAlign: 'center',
                            justifyContent: 'center',
                            display: 'flex',
                            flexDirection: 'column',
                            color: 'var(--color-grey-50, #808080)',
                            fontSize: '28px', // Ligeramente reducido para mayor elegancia
                            fontFamily: 'Roboto, sans-serif',
                            fontWeight: 400, // Peso más ligero para contraste
                            lineHeight: '1.4',
                            wordWrap: 'break-word',
                            maxWidth: '850px',
                        }}
                    >
                        Acceso único a experiencias exclusivas, desde<br className="hidden md:block" />
                        la seguridad de bóvedas físicas, hasta la liquidez<br className="hidden md:block" />
                        digital instantánea en los mercados globales,<br className="hidden md:block" />
                        todo a través de tu conserje Atlas.
                    </div>

                </motion.div>
            </Container>
        </section>
    );
};