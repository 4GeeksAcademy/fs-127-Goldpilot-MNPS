import React from "react";
import { Container, Heading, Text, Grid, Flex, Box } from "@radix-ui/themes";
import { Star, Shield, TrendingUp, Cpu } from "lucide-react";
import { motion } from "framer-motion";

/**
 * Sección de Riesgos Corregida - SIN TARJETAS.
 * Utiliza un diseño de lista tipográfica limpia y elegante sobre fondo oscuro.
 */
export const RiskSection = () => {

    const features = [
        {
            icon: <TrendingUp size={32} className="text-[var(--color-gold)]" />,
            title: "Volatilidad Controlada",
            desc: "Nuestros algoritmos ajustan la exposición en tiempo real, mitigando las fluctuaciones naturales del mercado."
        },
        {
            icon: <Shield size={32} className="text-[var(--color-gold)]" />,
            title: "Custodia Segura",
            desc: "Tus activos están respaldados por oro físico en bóvedas de alta seguridad, auditadas trimestralmente."
        },
        {
            icon: <Cpu size={32} className="text-[var(--color-gold)]" />,
            title: "Liquidez Instantánea",
            desc: "Convierte tus posiciones a moneda fiat en segundos, sin las barreras tradicionales del metal físico."
        },
        {
            icon: <Star size={32} className="text-[var(--color-gold)]" />,
            title: "Transparencia Total",
            desc: "Monitorea cada movimiento y auditoría desde tu dashboard personal en tiempo real."
        }
    ];

    return (
        <section className="py-32 bg-[var(--color-brown-dark)] relative overflow-hidden">
            {/* FONDO DECORATIVO SUTIL */}
            <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-b from-black via-[var(--color-brown-dark)] to-black opacity-80 z-0 pointer-events-none" />

            <Container size="4" className="relative z-10 px-6">

                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    viewport={{ once: true }}
                    className="mb-24"
                >
                    <Heading size="8" className="text-white mb-6 font-display tracking-tight">
                        Más allá del riesgo. <br />
                        <span className="text-[var(--color-gold)]">Pura certeza.</span>
                    </Heading>
                    <Text size="5" className="text-gray-400 max-w-2xl font-light">
                        Eliminamos fricciones innecesarias.
                        Diseñado para el inversor que exige precisión quirúrgica.
                    </Text>
                </motion.div>

                <Grid columns={{ initial: '1', md: '2' }} gapX="9" gapY="9">
                    {features.map((item, index) => (
                        <motion.div
                            key={index}
                            initial={{ opacity: 0, x: -20 }}
                            whileInView={{ opacity: 1, x: 0 }}
                            transition={{ delay: index * 0.1, duration: 0.6 }}
                            viewport={{ once: true }}
                            className="group"
                        >
                            <Flex direction="column" gap="4">
                                <Flex align="center" gap="4" className="mb-2">
                                    <div className="p-3 rounded-full bg-[var(--glass-white-lighter)] backdrop-blur-sm group-hover:bg-[var(--glass-gold-lighter)] transition-colors duration-500">
                                        {item.icon}
                                    </div>
                                    <Heading size="6" className="text-white font-medium">
                                        {item.title}
                                    </Heading>
                                </Flex>

                                <Text size="4" className="text-gray-400 font-light leading-relaxed pl-16 border-l border-white/10 group-hover:border-[var(--color-gold)] transition-colors duration-500">
                                    {item.desc}
                                </Text>
                            </Flex>
                        </motion.div>
                    ))}
                </Grid>

            </Container>
        </section>
    );
};
