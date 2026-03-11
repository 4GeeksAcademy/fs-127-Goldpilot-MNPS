import React, { useEffect } from "react";
import { Theme, Container, Grid, Flex, Text, Section } from "@radix-ui/themes";
import "@radix-ui/themes/styles.css";
import { motion } from "framer-motion";
import { Navbar } from "../features/Landing/components/Navbar";
import { Footer } from "../features/Landing/components/Footer";

export const PressPage = () => {
    useEffect(() => {
        window.scrollTo(0, 0);
    }, []);

    const pressReleases = [
        {
            date: "OCT 2025",
            title: "XSNIPER supera los $50M en volumen ejecutado a través de MetaApi",
            tag: "HITO EMPRESARIAL"
        },
        {
            date: "AGO 2025",
            title: "Lanzamiento del nuevo algoritmo de Baja Volatilidad DXY-Core",
            tag: "PRODUCTO"
        },
        {
            date: "MAR 2025",
            title: "Pura Certeza: XSNIPER anuncia su ronda semilla de financiación",
            tag: "INVERSIÓN"
        }
    ];

    return (
        <Theme appearance="dark" accentColor="amber" grayColor="slate" panelBackground="translucent" radius="large">
            <div className="min-h-screen font-sans bg-black text-white selection:bg-[#D4AF37] selection:text-black">
                <Navbar />
                <main>
                    <Container size="4" className="pt-52 pb-20 px-6">
                        
                        {/* HERO SECTION */}
                        <motion.div 
                            initial={{ opacity: 0, y: 30 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 1 }}
                            className="text-center mb-40"
                        >
                            <h1 className="text-5xl md:text-7xl lg:text-[100px] font-bold tracking-tighter leading-[0.9] bg-gradient-to-b from-white via-white to-white/30 bg-clip-text text-transparent mb-12">
                                SALA DE <br/> PRENSA
                            </h1>
                            <Text className="text-gray-400 text-xl md:text-3xl max-w-4xl mx-auto block leading-relaxed font-light tracking-tight">
                                Comunicados oficiales, recursos de marca y notas para medios de comunicación sobre <span className="text-white font-medium">XSNIPER</span>.
                            </Text>
                        </motion.div>

                        <Grid columns={{ initial: "1", lg: "2" }} gap="9" className="mb-48">
                            
                            {/* COMUNICADOS RECIENTES */}
                            <motion.div initial={{ opacity: 0, x: -30 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }}>
                                <Text className="text-[var(--color-gold)] font-bold text-sm uppercase tracking-widest mb-8 block">
                                    Últimos Comunicados
                                </Text>
                                <div className="space-y-6">
                                    {pressReleases.map((pr, i) => (
                                        <div key={i} className="p-8 rounded-[32px] bg-[#0A0A0A] border border-white/10 hover:border-[var(--color-gold)]/50 transition-colors group cursor-pointer">
                                            <Flex justify="between" align="center" className="mb-4">
                                                <span className="text-xs font-bold uppercase tracking-widest text-gray-500 bg-white/5 px-3 py-1 rounded-full">{pr.tag}</span>
                                                <span className="text-sm font-mono text-[var(--color-gold)] opacity-70">{pr.date}</span>
                                            </Flex>
                                            <h3 className="text-2xl font-bold text-white group-hover:text-[var(--color-gold)] transition-colors leading-tight">
                                                {pr.title}
                                            </h3>
                                        </div>
                                    ))}
                                </div>
                            </motion.div>

                            {/* MEDIA KIT & CONTACTO */}
                            <motion.div initial={{ opacity: 0, x: 30 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} className="space-y-6">
                                <Text className="text-[var(--color-gold)] font-bold text-sm uppercase tracking-widest mb-8 block">
                                    Recursos para Medios
                                </Text>
                                
                                <div className="p-10 rounded-[40px] bg-gradient-to-br from-[#0A0A0A] to-[#050505] border border-white/10 relative overflow-hidden group">
                                    <div className="absolute top-0 right-0 w-32 h-32 bg-[var(--color-gold)]/5 rounded-full blur-2xl group-hover:bg-[var(--color-gold)]/10 transition-colors" />
                                    <div className="text-4xl mb-6">📦</div>
                                    <h3 className="text-3xl font-black text-white mb-4">Media Kit Oficial</h3>
                                    <Text className="text-gray-400 text-lg font-light mb-8 block">
                                        Descarga nuestros logotipos en alta resolución, paleta de colores corporativa y directrices de uso de marca.
                                    </Text>
                                    <button className="flex items-center gap-3 text-white font-medium hover:text-[var(--color-gold)] transition-colors">
                                        <span className="text-lg">Descargar ZIP (12MB)</span>
                                        <span>↓</span>
                                    </button>
                                </div>

                                <div className="p-10 rounded-[40px] bg-[#050505] border border-white/5">
                                    <h3 className="text-2xl font-bold text-white mb-4">Contacto de Prensa</h3>
                                    <Text className="text-gray-400 text-lg font-light mb-6 block">
                                        Para entrevistas, comentarios del mercado o consultas exclusivas, contacta con nuestro equipo de RRPP.
                                    </Text>
                                    <a href="mailto:press@xsniper.com" className="text-[var(--color-gold)] text-xl font-medium hover:text-white transition-colors">
                                        press@xsniper.com
                                    </a>
                                </div>
                            </motion.div>

                        </Grid>

                    </Container>
                </main>
                <Footer />
            </div>
        </Theme>
    );
};