import React, { useEffect } from "react";
import { Theme, Container, Grid, Flex, Text } from "@radix-ui/themes";
import "@radix-ui/themes/styles.css";
import { motion } from "framer-motion";
import { Navbar } from "../features/Landing/components/Navbar";
import { Footer } from "../features/Landing/components/Footer";

export const ContactPage = () => {

    // 1. Efecto Scroll Top
    useEffect(() => {
        window.scrollTo(0, 0);
    }, []);

    const contactChannels = [
        {
            id: "support",
            title: "Soporte Técnico",
            focus: "Clientes y Operativa",
            desc: "Resolución de incidencias, dudas sobre el Dashboard y monitoreo de ejecución algorítmica en tiempo real.",
            email: "support@xsniper.com",
            icon: "🎧"
        },
        {
            id: "api",
            title: "Integración API",
            focus: "Brokers & MetaApi",
            desc: "Asistencia dedicada para la conexión de llaves API, latencia de nodos y configuración de entornos de ejecución.",
            email: "api-ops@xsniper.com",
            icon: "⚡"
        },
        {
            id: "corporate",
            title: "Corporativo",
            focus: "Prensa y Partners",
            desc: "Relaciones institucionales, oportunidades de inversión a gran escala y contacto para medios de comunicación.",
            email: "press@xsniper.com",
            icon: "🏢"
        }
    ];

    return (
        <Theme appearance="dark" accentColor="amber" grayColor="slate" panelBackground="translucent" radius="large">
            
            <div className="min-h-screen font-sans bg-black text-white selection:bg-[#D4AF37] selection:text-black">
                <Navbar />
                
                <main>
                    <Container size="4" className="pt-52 pb-40 px-6">
                        
                        {/* HERO SECTION */}
                        <motion.div 
                            initial={{ opacity: 0, y: 30 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 1 }}
                            className="text-center mb-40"
                        >
                            <h1 className="text-5xl md:text-7xl lg:text-[100px] font-black tracking-tighter leading-[0.9] bg-gradient-to-b from-white via-white to-white/30 bg-clip-text text-transparent mb-12 uppercase">
                                Contacto
                            </h1>
                            
                            <Text className="text-gray-400 text-xl md:text-3xl max-w-4xl mx-auto block leading-relaxed font-light tracking-tight">
                                Asistencia para nuestra red de clientes. Comunicación directa y respuesta <span className="text-white font-medium">prioritaria</span> para asegurar tu operativa.
                            </Text>
                        </motion.div>

                        {/* GRID DE CANALES DE CONTACTO */}
                        <Grid columns={{ initial: "1", md: "3" }} gap="6">
                            {contactChannels.map((c, i) => (
                                <motion.div
                                    key={c.id}
                                    initial={{ opacity: 0, y: 30 }}
                                    whileInView={{ opacity: 1, y: 0 }}
                                    transition={{ delay: i * 0.2 }}
                                    viewport={{ once: true }}
                                    className="p-10 rounded-[40px] bg-[#0A0A0A] border border-white/10 hover:border-[var(--color-gold)]/50 transition-all duration-500 group relative overflow-hidden flex flex-col h-full"
                                >
                                    {/* Brillo de fondo sutil */}
                                    <div className="absolute -top-24 -right-24 w-48 h-48 bg-[var(--color-gold)]/5 rounded-full blur-3xl group-hover:bg-[var(--color-gold)]/15 transition-colors" />

                                    <div className="text-5xl mb-8 opacity-80 group-hover:opacity-100 group-hover:scale-110 transition-all duration-500 origin-left">
                                        {c.icon}
                                    </div>

                                    <div className="flex-grow">
                                        <Text className="text-[var(--color-gold)] font-bold text-sm uppercase tracking-widest mb-4 block">
                                            {c.focus}
                                        </Text>
                                        
                                        <h3 className="text-3xl font-black text-white group-hover:text-[var(--color-gold)] transition-colors tracking-tight mb-6">
                                            {c.title}
                                        </h3>
                                        
                                        <Text className="text-gray-400 text-lg leading-relaxed font-light mb-10 block">
                                            {c.desc}
                                        </Text>
                                    </div>

                                    {/* Enlace de Email anclado al fondo */}
                                    <div className="pt-8 border-t border-white/10 mt-auto">
                                        <a 
                                            href={`mailto:${c.email}`} 
                                            className="inline-flex items-center gap-3 text-white font-medium hover:text-[var(--color-gold)] transition-colors group/link"
                                        >
                                            <span className="text-lg">{c.email}</span>
                                            <span className="transform group-hover/link:translate-x-2 transition-transform">→</span>
                                        </a>
                                    </div>
                                </motion.div>
                            ))}
                        </Grid>
                    </Container>
                </main>

                <Footer />
            </div>
        </Theme>
    );
};