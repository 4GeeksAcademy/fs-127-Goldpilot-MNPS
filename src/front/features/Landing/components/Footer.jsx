import React from "react";
import { Container, Grid, Flex, Text, Heading, Link as RadixLink } from "@radix-ui/themes";
import { motion } from "framer-motion";

/**
 * Footer estilo "Superpower" - BIG LETTERS.
 * Tipografía gigante, ocupando todo el ancho, minimalista y audaz.
 */
export const Footer = () => {
    return (
        <footer className="bg-black text-white pt-32 pb-12 overflow-hidden relative border-t border-white/5">

            <Container size="4" className="px-6 relative z-10">

                {/* BIG LETTERS TITLE */}
                <motion.div
                    initial={{ y: 100, opacity: 0 }}
                    whileInView={{ y: 0, opacity: 1 }}
                    transition={{ duration: 0.8, ease: "easeOut" }}
                    viewport={{ once: true }}
                    className="mb-24 text-center md:text-left"
                >
                    <h2 className="text-[12vw] leading-none font-bold tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-white to-gray-600 opacity-90 select-none">
                        XSNIPER
                    </h2>
                </motion.div>

                <Grid columns={{ initial: '1', sm: '2', md: '4' }} gap="8" className="border-t border-white/10 pt-12">

                    {/* COLUMNA 1: Brand */}
                    <Flex direction="column" gap="4">
                        <Text weight="bold" className="text-white uppercase tracking-widest text-xs mb-4">
                            Plataforma
                        </Text>
                        <RadixLink href="#" color="gray" className="hover:text-[var(--color-gold)] transition-colors">Estrategias</RadixLink>
                        <RadixLink href="#" color="gray" className="hover:text-[var(--color-gold)] transition-colors">Seguridad</RadixLink>
                        <RadixLink href="#" color="gray" className="hover:text-[var(--color-gold)] transition-colors">API</RadixLink>
                    </Flex>

                    {/* COLUMNA 2: Compañía */}
                    <Flex direction="column" gap="4">
                        <Text weight="bold" className="text-white uppercase tracking-widest text-xs mb-4">
                            Compañía
                        </Text>
                        <RadixLink href="#" color="gray" className="hover:text-[var(--color-gold)] transition-colors">Nosotros</RadixLink>
                        <RadixLink href="#" color="gray" className="hover:text-[var(--color-gold)] transition-colors">Carreras</RadixLink>
                        <RadixLink href="#" color="gray" className="hover:text-[var(--color-gold)] transition-colors">Prensa</RadixLink>
                    </Flex>

                    {/* COLUMNA 3: Legal */}
                    <Flex direction="column" gap="4">
                        <Text weight="bold" className="text-white uppercase tracking-widest text-xs mb-4">
                            Legal
                        </Text>
                        <RadixLink href="#" color="gray" className="hover:text-[var(--color-gold)] transition-colors">Términos</RadixLink>
                        <RadixLink href="#" color="gray" className="hover:text-[var(--color-gold)] transition-colors">Privacidad</RadixLink>
                    </Flex>

                    {/* COLUMNA 4: Social */}
                    <Flex direction="column" gap="4">
                        <Text weight="bold" className="text-white uppercase tracking-widest text-xs mb-4">
                            Social
                        </Text>
                        <Flex gap="4">
                            <RadixLink href="#" color="gray" className="hover:text-[var(--color-gold)]">X / Twitter</RadixLink>
                            <RadixLink href="#" color="gray" className="hover:text-[var(--color-gold)]">LinkedIn</RadixLink>
                        </Flex>
                        <Text size="1" color="gray" className="mt-8 opacity-50">
                            © 2024 Xsniper Inc. <br /> All rights reserved.
                        </Text>
                    </Flex>

                </Grid>
            </Container>
        </footer>
    );
};
