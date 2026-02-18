import React from "react";
import { Container } from "@radix-ui/themes";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";

/**
 * Sección Minimalista Tipográfica - VERSIÓN CORREGIDA FINAL (V3).
 * - Título: 2 LÍNEAS. "Más allá del riesgo" (Blanco) -> "Pura certeza" (Dorado con Fade).
 * - Esfumado: Gradiente sutil desde Blanco puro hacia el Dorado Principal (#c38f37).
 * - Espaciado: MUY ajustado entre título y caja de texto.
 * - Descripción: Estilo exacto Atlas.
 */
export const RiskSection = () => {
    return (
        <section className="relative w-full py-40 bg-black flex items-center justify-center overflow-hidden">

            {/* FONDO LIMPIO */}
            <div className="absolute inset-0 bg-black z-0 pointer-events-none" />

            <Container size="3" className="relative z-10 px-6 text-center">
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, ease: "easeOut" }}
                    viewport={{ once: true, margin: "-10%" }}
                    className="flex flex-col items-center gap-2" // ESPACIADO MÍNIMO ENTRE ELEMENTOS
                >
                    {/* TÍTULO PRINCIPAL (ESTRUCTURA 2 LÍNEAS) */}
                    <div className="flex flex-col items-center leading-[0.9] tracking-tighter mb-4">

                        {/* LÍNEA 1: Blanco puro */}
                        <h2 className="text-5xl md:text-7xl lg:text-8xl font-medium text-white text-center">
                            Más allá del riesgo.
                        </h2>

                        {/* LÍNEA 2: Dorado con Esfumado/Gradiente */}
                        {/* El gradiente va de Blanco (arriba, conectando con la línea 1) a Dorado (abajo) */}
                        <h2
                            className="text-5xl md:text-7xl lg:text-8xl font-medium text-center"
                            style={{
                                background: "linear-gradient(180deg, #FFFFFF 0%, #c38f37 100%)",
                                WebkitBackgroundClip: "text",
                                WebkitTextFillColor: "transparent",
                                paddingBottom: "0.1em"
                            }}
                        >
                            Pura certeza.
                        </h2>
                    </div>

                    {/* BLOQUE DE TEXTO ESTRUCTURADO (Estilo Atlas Exacto) */}
                    <div
                        style={{
                            textAlign: 'center',
                            justifyContent: 'center',
                            display: 'flex',
                            flexDirection: 'column',
                            color: 'var(--color-grey-50, #808080)',
                            fontSize: '31.60px',
                            fontFamily: 'Roboto, sans-serif',
                            fontWeight: 500,
                            lineHeight: '41.86px',
                            wordWrap: 'break-word',
                            maxWidth: '900px',
                            marginTop: '-10px' // AJUSTE FINO NEGATIVO PARA PEGARLO MÁS VISUALMENTE SI HACE FALTA
                        }}
                    >
                        Acceso único a experiencias exclusivas, desde<br />
                        la seguridad de bóvedas físicas, hasta la liquidez<br />
                        digital instantánea en los mercados globales,<br />
                        todo a través de tu conserje Atlas.
                    </div>

                    {/* BOTÓN LIQUID GLASS */}
                    <div className="mt-8">
                        <Link to="/strategies">
                            <button className="px-8 py-4 rounded-full text-white font-medium text-lg transition-all duration-300 transform hover:scale-105 active:scale-95 border border-white/20 backdrop-blur-md bg-white/5 shadow-[0_4px_24px_rgba(0,0,0,0.5)] hover:bg-white/10 hover:border-white/30 hover:shadow-[0_0_20px_rgba(195,143,55,0.3)]">
                                Explorar Estrategias
                            </button>
                        </Link>
                    </div>

                </motion.div>
            </Container>
        </section>
    );
};
