import React, { useEffect } from "react"; // 1. Añadimos useEffect aquí
import { Theme, Container, Grid, Flex, Text, Section } from "@radix-ui/themes";
import "@radix-ui/themes/styles.css"; 
import { motion } from "framer-motion";
import { Navbar } from "../features/Landing/components/Navbar"; 
import { Footer } from "../features/Landing/components/Footer"; 

export const StrategiesPage = () => {

    // 2. EFECTO MAGNÉTICO: Forzar el scroll hacia arriba al montar la página
    useEffect(() => {
        window.scrollTo(0, 0);
    }, []);

    const strategyTypes = [
        {
            id: "low",
            title: "🛡️ Bajo Riesgo",
            focus: "Preservación de Capital",
            details: "Utiliza una correlación inversa entre el Nasdaq y el DXY. Entra al mercado solo tras confirmación de tendencia en SMA 50.",
            target: "Batir inflación con volatilidad mínima."
        },
        {
            id: "medium",
            title: "⚖️ Moderado",
            focus: "Optimización de Retrocesos",
            details: "Basada en niveles de Fibonacci (61.8%) y confluencia de RSI. Captura movimientos tendenciales del Oro con precisión quirúrgica.",
            target: "Balance entre seguridad y rentabilidad."
        },
        {
            id: "high",
            title: "🔥 Alto Riesgo",
            focus: "Explotación de Rupturas",
            details: "Identifica rangos de consolidación y opera rupturas de volatilidad extrema basadas exclusivamente en Acción del Precio.",
            target: "Maximización de capital en ciclos cortos."
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
                            <h1 className="text-6xl md:text-8xl lg:text-[120px] font-bold tracking-tighter leading-[0.85] bg-gradient-to-b from-white via-white to-white/30 bg-clip-text text-transparent mb-12">
                                ESTRATEGIAS DE <br/> ALTA PRECISIÓN
                            </h1>
                            
                            <Text className="text-gray-400 text-xl md:text-3xl max-w-4xl mx-auto block leading-relaxed font-light tracking-tight">
                                Algoritmos diseñados para el mercado de metales preciosos, ejecutados con la <span className="text-white font-medium">precisión de un sniper</span> y la seguridad de una bóveda.
                            </Text>
                        </motion.div>

                        {/* GRID DE ESTRATEGIAS */}
                        <Grid columns={{ initial: "1", md: "3" }} gap="6" className="mb-48">
                            {strategyTypes.map((s, index) => (
                                <motion.div
                                    key={s.id}
                                    initial={{ opacity: 0, y: 30 }}
                                    whileInView={{ opacity: 1, y: 0 }}
                                    transition={{ delay: index * 0.2 }}
                                    viewport={{ once: true }}
                                    className="p-10 rounded-[40px] bg-[#0A0A0A] border border-white/10 hover:border-[var(--color-gold)]/50 transition-all duration-500 group relative overflow-hidden flex flex-col justify-between"
                                >
                                    {/* Brillo de fondo */}
                                    <div className="absolute -top-24 -right-24 w-48 h-48 bg-[var(--color-gold)]/5 rounded-full blur-3xl group-hover:bg-[var(--color-gold)]/10 transition-colors" />

                                    <div>
                                        <Text className="text-[var(--color-gold)] font-bold text-sm uppercase tracking-widest mb-4 block">
                                            {s.focus}
                                        </Text>
                                        
                                        <h3 className="text-3xl md:text-4xl font-black text-white group-hover:text-[var(--color-gold)] transition-colors tracking-tight mb-6">
                                            {s.title}
                                        </h3>
                                        
                                        <Text className="text-gray-300 text-lg mb-10 block leading-relaxed font-light">
                                            {s.details}
                                        </Text>
                                    </div>
                                    
                                    <div className="pt-8 border-t border-white/10 mt-auto">
                                        <Text className="text-gray-500 text-xs uppercase tracking-widest block mb-2 font-medium">
                                            Objetivo de Inversión:
                                        </Text>
                                        <Text className="text-gray-200 text-base font-medium">
                                            {s.target}
                                        </Text>
                                    </div>
                                </motion.div>
                            ))}
                        </Grid>

                        {/* METODOLOGÍA */}
                        <Section className="bg-[#050505] rounded-[60px] p-8 lg:p-16 border border-white/5 relative overflow-hidden mb-20">
                            <Grid columns={{ initial: "1", md: "2" }} gap="9" align="center">
                                <motion.div initial={{ opacity: 0, x: -30 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }}>
                                    
                                    <h2 className="text-4xl md:text-5xl lg:text-6xl font-bold tracking-tight mb-12 text-white leading-[1.1]">
                                        <span className="whitespace-nowrap">Metodología</span> <br />
                                        <span className="text-[var(--color-gold)]">XSNIPER Engine</span>
                                    </h2>
                                    
                                    <div className="space-y-12">
                                        {[
                                            { step: "01", title: "Análisis Multi-Mercado", desc: "Monitoreo en milisegundos de Gold, DXY y Nasdaq." },
                                            { step: "02", title: "Validación Algorítmica", desc: "Backtesting de confluencia estadística antes de cada entrada." },
                                            { step: "03", title: "Ejecución MetaApi", desc: "Transmisión blindada de órdenes a tu cuenta de trading." }
                                        ].map((item, idx) => (
                                            <Flex key={idx} gap="6" align="start">
                                                <span className="text-[var(--color-gold)] font-black text-2xl opacity-50">{item.step}</span>
                                                <div className="space-y-2">
                                                    <Text className="text-white font-bold text-xl block tracking-tight">{item.title}</Text>
                                                    <Text className="text-gray-400 text-lg leading-relaxed">{item.desc}</Text>
                                                </div>
                                            </Flex>
                                        ))}
                                    </div>
                                </motion.div>
                                
                                {/* Visual decorativo */}
                                <div className="relative flex items-center justify-center mt-10 md:mt-0">
                                    <div className="absolute w-[300px] h-[300px] bg-[var(--color-gold)]/10 rounded-full blur-[120px]" />
                                    <div className="relative w-72 h-72 lg:w-80 lg:h-80 border border-white/10 rounded-full flex items-center justify-center">
                                        <motion.div 
                                            animate={{ rotate: 360 }}
                                            transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                                            className="absolute w-full h-full border-t-2 border-[var(--color-gold)] rounded-full"
                                        />
                                        <Text className="text-[var(--color-gold)] font-black text-6xl lg:text-7xl tracking-tighter drop-shadow-[0_0_15px_rgba(195,143,55,0.5)]">GOLD</Text>
                                    </div>
                                </div>
                            </Grid>
                        </Section>

                    </Container>
                </main>

                <Footer />
            </div>
        </Theme>
    );
};