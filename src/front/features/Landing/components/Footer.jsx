import React from "react";
import { Container, Grid, Flex, Text } from "@radix-ui/themes";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";

export const Footer = () => {
    return (
        <footer className="bg-black text-white pt-32 pb-16 overflow-hidden relative border-t border-white/5">
            <Container size="4" className="px-6 relative z-10">
                <motion.div
                    initial={{ y: 80, opacity: 0 }}
                    whileInView={{ y: 0, opacity: 1 }}
                    transition={{ duration: 0.8, ease: "easeOut" }}
                    viewport={{ once: true }}
                    className="mb-24 text-center md:text-left w-full overflow-hidden"
                >
                    <h2 className="text-[clamp(4rem,10vw,160px)] whitespace-nowrap leading-none font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-white to-gray-800 opacity-90 select-none">
                        XSNIPER
                    </h2>
                </motion.div>

                <Grid columns={{ initial: '1', sm: '3' }} gap="8" className="border-t border-white/10 pt-16">
                    
                    <Flex direction="column" gap="4">
                        <Text weight="bold" className="text-white uppercase tracking-[0.3em] text-[10px] mb-4 opacity-50">
                            Plataforma
                        </Text>
                        <Link to="/strategies" className="text-gray-400 hover:text-[var(--color-gold)] transition-colors text-sm">Estrategias</Link>
                    </Flex>

                    <Flex direction="column" gap="4">
                        <Text weight="bold" className="text-white uppercase tracking-[0.3em] text-[10px] mb-4 opacity-50">
                            Ayuda
                        </Text>
                        <Link to="/contact" className="text-gray-400 hover:text-[var(--color-gold)] transition-colors text-sm">Contacto</Link>
                    </Flex>

                    <Flex direction="column" gap="4">
                        <Text weight="bold" className="text-white uppercase tracking-[0.3em] text-[10px] mb-4 opacity-50">
                            Legal
                        </Text>
                        <Link to="/terms" className="text-gray-400 hover:text-[var(--color-gold)] transition-colors text-sm">Términos de Servicio</Link>
                    </Flex>
                </Grid>

                <div className="mt-20 pt-8 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-4">
                    <div className="flex flex-col">
                        <Text size="1" color="gray" className="opacity-40 uppercase tracking-[0.2em]">
                            © {new Date().getFullYear()} XSNIPER INC. PURA CERTEZA.
                        </Text>
                    </div>
                    <div className="h-[1px] flex-grow bg-gradient-to-r from-transparent via-white/10 to-transparent mx-8 hidden md:block" />
                    <Text size="1" color="gray" className="opacity-20 uppercase tracking-[0.1em] italic">
                        All assets protected by digital encryption
                    </Text>
                </div>
            </Container>
        </footer>
    );
};