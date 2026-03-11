import React, { useEffect } from "react";
import { Theme, Container, Grid, Flex, Text, Section } from "@radix-ui/themes";
import "@radix-ui/themes/styles.css";
import { motion } from "framer-motion";
import { Navbar } from "../features/Landing/components/Navbar";
import { Footer } from "../features/Landing/components/Footer";

export const SecurityPage = () => {

    // 1. Efecto Scroll Top
    useEffect(() => {
        window.scrollTo(0, 0);
    }, []);

    const securityFeatures = [
        {
            title: "Cifrado Extremo",
            focus: "AES-256 / TLS 1.3",
            desc: "Todas las comunicaciones entre tu Dashboard y los nodos de ejecución están blindadas con protocolos de cifrado de grado militar.",
            icon: "🔒"
        },
        {
            title: "Non-Custodial",
            focus: "Tus Llaves, Tus Fondos",
            desc: "XSNIPER nunca almacena ni toca tu capital. La ejecución se realiza vía API directamente en tu broker regulado.",
            icon: "🔑"
        },
        {
            title: "Auditoría Live",
            focus: "Verificación Continua",
            desc: "Cada trade es registrado y verificable. Nuestro motor realiza comprobaciones de integridad algorítmica cada 60 segundos.",
            icon: "📊"
        }
    ];

    return (
        // 2. Theme Wrapper de Radix
        <Theme appearance="dark" accentColor="amber" grayColor="slate" panelBackground="translucent" radius="large">
            
            <div className="min-h-screen font-sans bg-black text-white selection:bg-[#D4AF37] selection:text-black">
                <Navbar />
                
                <main>
                    {/* 3. Container size="4" para alinear con el Footer */}
                    <Container size="4" className="pt-52 pb-20 px-6">
                        
                        {/* HERO SECTION */}
                        <motion.div 
                            initial={{ opacity: 0, y: 30 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 1 }}
                            className="text-center mb-40"
                        >
                            <h1 className="text-5xl md:text-7xl lg:text-[100px] font-bold tracking-tighter leading-[0.9] bg-gradient-to-b from-white via-white to-white/30 bg-clip-text text-transparent mb-12">
                                SEGURIDAD DE GRADO <br/> INSTITUCIONAL
                            </h1>
                            
                            <Text className="text-gray-400 text-xl md:text-3xl max-w-4xl mx-auto block leading-relaxed font-light tracking-tight">
                                Tu capital es tu prioridad. Proteger la integridad de tus operaciones con <span className="text-white font-medium">infraestructura blindada</span> es la nuestra.
                            </Text>
                        </motion.div>

                        {/* GRID DE PILARES DE SEGURIDAD */}
                        <Grid columns={{ initial: "1", md: "3" }} gap="6" className="mb-48">
                            {securityFeatures.map((f, i) => (
                                <motion.div
                                    key={i}
                                    initial={{ opacity: 0, y: 30 }}
                                    whileInView={{ opacity: 1, y: 0 }}
                                    transition={{ delay: i * 0.2 }}
                                    viewport={{ once: true }}
                                    className="p-10 rounded-[40px] bg-[#0A0A0A] border border-white/10 hover:border-[var(--color-gold)]/50 transition-all duration-500 group relative overflow-hidden flex flex-col"
                                >
                                    {/* Brillo de fondo sutil */}
                                    <div className="absolute -top-24 -right-24 w-48 h-48 bg-[var(--color-gold)]/5 rounded-full blur-3xl group-hover:bg-[var(--color-gold)]/10 transition-colors" />

                                    <div className="text-5xl mb-8 opacity-80 group-hover:opacity-100 group-hover:scale-110 transition-all duration-500 origin-left">
                                        {f.icon}
                                    </div>

                                    <Text className="text-[var(--color-gold)] font-bold text-sm uppercase tracking-widest mb-4 block">
                                        {f.focus}
                                    </Text>
                                    
                                    <h3 className="text-3xl font-black text-white group-hover:text-[var(--color-gold)] transition-colors tracking-tight mb-6">
                                        {f.title}
                                    </h3>
                                    
                                    <Text className="text-gray-300 text-lg leading-relaxed font-light">
                                        {f.desc}
                                    </Text>
                                </motion.div>
                            ))}
                        </Grid>

                        {/* INFRAESTRUCTURA VISUAL */}
                        <Section className="bg-[#050505] rounded-[60px] p-12 lg:p-20 border border-white/5 relative overflow-hidden mb-20 flex flex-col items-center">
                            
                            {/* Brillos decorativos de fondo */}
                            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-2xl h-1/2 bg-[var(--color-gold)]/5 rounded-full blur-[100px] pointer-events-none" />

                            <motion.div 
                                initial={{ opacity: 0, y: 20 }} 
                                whileInView={{ opacity: 1, y: 0 }} 
                                viewport={{ once: true }}
                                className="relative z-10 flex flex-col items-center text-center w-full"
                            >
                                <div className="w-16 h-1 bg-gradient-to-r from-transparent via-[var(--color-gold)] to-transparent mb-10" />
                                
                                <h2 className="text-4xl md:text-6xl font-black tracking-tighter text-white mb-8">
                                    PROTOCOLO DE <span className="text-[var(--color-gold)]">BÓVEDA DIGITAL</span>
                                </h2>
                                
                                <Text className="text-gray-400 text-lg md:text-2xl max-w-3xl leading-relaxed font-light">
                                    Infraestructura distribuida en múltiples regiones para garantizar una disponibilidad del <span className="text-white font-medium">99.9%</span> y redundancia total frente a caídas del mercado.
                                </Text>
                            </motion.div>
                        </Section>

                    </Container>
                </main>

                <Footer />
            </div>
        </Theme>
    );
};