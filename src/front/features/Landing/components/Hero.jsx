import React from "react";
import { motion } from "framer-motion";
import { Button, Container, Heading, Text, Flex } from "@radix-ui/themes";

/**
 * Componente Hero para la Landing Page - VERSIÓN CORREGIDA.
 * Fuerza la visualización del video y aplica la tipografía "Vidrio Líquido".
 */
export const Hero = () => {
    return (
        <section className="relative h-screen w-full flex items-center justify-center overflow-hidden">
            {/* FONDO DE VIDEO (Forzado) */}
            <div className="absolute inset-0 z-0">
                <div className="absolute inset-0 bg-[var(--color-brown-dark)]/40 z-10 mix-blend-overlay" />
                <div className="absolute inset-0 bg-gradient-to-b from-black/60 via-transparent to-black/80 z-10" />

                <video
                    autoPlay
                    loop
                    muted
                    playsInline
                    className="w-full h-full object-cover scale-105 opacity-90"
                >
                    {/* Fallback a multiples fuentes por seguridad */}
                    <source src="https://assets.mixkit.co/videos/preview/mixkit-liquid-gold-swirling-in-a-dark-container-30231-large.mp4" type="video/mp4" />
                    <source src="https://cdn.coverr.co/videos/coverr-molten-gold-5347/1080p.mp4" type="video/mp4" />
                </video>
            </div>

            <Container size="4" className="relative z-20 text-center px-4">
                <motion.div
                    initial={{ opacity: 0, y: 50, filter: "blur(10px)" }}
                    animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
                    transition={{ duration: 1.2, ease: "easeOut" }}
                >
                    <Heading
                        size="9"
                        className="tracking-tighter mb-8 leading-none drop-shadow-2xl"
                        style={{ fontFamily: 'inherit', fontSize: 'clamp(3rem, 8vw, 6rem)' }}
                    >
                        <span className="text-white">Excelencia</span> <br />
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-[var(--color-gold)] via-[#F5E6BE] to-[var(--color-gold)] animate-pulse">
                            Líquida.
                        </span>
                    </Heading>

                    <Text
                        as="p"
                        size="6"
                        className="max-w-xl mx-auto mb-12 leading-relaxed text-gray-200 font-light drop-shadow-md"
                    >
                        {/* TODO: INSERTAR COPY FINAL */}
                        La solidez del oro físico con la fluidez de la era digital.
                        Tu patrimonio, blindado y accesible.
                    </Text>

                    <Flex gap="6" justify="center">
                        <motion.button
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            className="bg-[var(--color-gold)] text-black px-8 py-4 rounded-full font-bold text-lg shadow-[var(--glow-gold)] hover:bg-[#F5E6BE] transition-colors"
                        >
                            Explorar Estrategias
                        </motion.button>

                        <motion.button
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            className="px-8 py-4 rounded-full font-bold text-lg border border-white/30 text-white backdrop-blur-sm hover:bg-white/10 transition-colors"
                        >
                            Saber más
                        </motion.button>
                    </Flex>
                </motion.div>
            </Container>

            {/* ELEMENTOS DECORATIVOS LÍQUIDOS */}
            <div className="absolute bottom-0 w-full h-32 bg-gradient-to-t from-[var(--color-brown-dark)] to-transparent z-20" />
        </section>
    );
};
