import React, { useEffect } from "react";
import { Theme, Container, Grid, Flex, Text, Section } from "@radix-ui/themes";
import "@radix-ui/themes/styles.css";
import { motion } from "framer-motion";
import { Navbar } from "../features/Landing/components/Navbar";
import { Footer } from "../features/Landing/components/Footer";

export const AboutUsPage = () => {
    useEffect(() => {
        window.scrollTo(0, 0);
    }, []);

    const values = [
        {
            title: "Precisión Algorítmica",
            desc: "Eliminamos el factor humano. Nuestras decisiones están basadas en modelos matemáticos probados y backtesting institucional.",
            icon: "🎯"
        },
        {
            title: "Transparencia Absoluta",
            desc: "Sin cajas negras. Cada ejecución, cada latencia y cada resultado es auditable por nuestros clientes en tiempo real.",
            icon: "👁️"
        },
        {
            title: "Seguridad por Diseño",
            desc: "La preservación del capital dicta nuestra arquitectura. Infraestructura non-custodial y encriptación militar en cada nodo.",
            icon: "🛡️"
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
                            <Text className="text-[var(--color-gold)] font-bold text-sm uppercase tracking-widest mb-6 block">
                                Nuestra Visión
                            </Text>
                            <h1 className="text-5xl md:text-7xl lg:text-[100px] font-bold tracking-tighter leading-[0.9] bg-gradient-to-b from-white via-white to-white/30 bg-clip-text text-transparent mb-12">
                                PURA CERTEZA <br/> EN EL CAOS
                            </h1>
                            <Text className="text-gray-400 text-xl md:text-3xl max-w-4xl mx-auto block leading-relaxed font-light tracking-tight">
                                Nacimos con un objetivo claro: democratizar la <span className="text-white font-medium">tecnología de ejecución institucional</span> para el mercado de metales preciosos.
                            </Text>
                        </motion.div>

                        {/* VALORES CORE */}
                        <Grid columns={{ initial: "1", md: "3" }} gap="6" className="mb-48">
                            {values.map((v, i) => (
                                <motion.div
                                    key={i}
                                    initial={{ opacity: 0, y: 30 }}
                                    whileInView={{ opacity: 1, y: 0 }}
                                    transition={{ delay: i * 0.2 }}
                                    viewport={{ once: true }}
                                    className="p-10 rounded-[40px] bg-[#0A0A0A] border border-white/10 hover:border-[var(--color-gold)]/50 transition-all duration-500 group relative overflow-hidden"
                                >
                                    <div className="absolute -top-24 -right-24 w-48 h-48 bg-[var(--color-gold)]/5 rounded-full blur-3xl group-hover:bg-[var(--color-gold)]/10 transition-colors" />
                                    <div className="text-5xl mb-8 opacity-80">{v.icon}</div>
                                    <h3 className="text-3xl font-black text-white group-hover:text-[var(--color-gold)] transition-colors tracking-tight mb-6">
                                        {v.title}
                                    </h3>
                                    <Text className="text-gray-300 text-lg leading-relaxed font-light block">
                                        {v.desc}
                                    </Text>
                                </motion.div>
                            ))}
                        </Grid>

                        {/* EL MANIFIESTO */}
                        <Section className="bg-[#050505] rounded-[60px] p-12 lg:p-20 border border-white/5 relative overflow-hidden mb-20 flex flex-col items-center text-center">
                            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-2xl h-1/2 bg-[var(--color-gold)]/5 rounded-full blur-[100px] pointer-events-none" />
                            <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="relative z-10 w-full max-w-4xl">
                                <div className="w-16 h-1 bg-gradient-to-r from-transparent via-[var(--color-gold)] to-transparent mb-10 mx-auto" />
                                <h2 className="text-4xl md:text-5xl font-black tracking-tighter text-white mb-10">
                                    EL MANIFIESTO XSNIPER
                                </h2>
                                <Text className="text-gray-400 text-xl leading-relaxed font-light mb-8 block text-justify md:text-center">
                                    El trading discrecional está obsoleto. Las emociones destruyen el capital, y la velocidad humana no puede competir contra la latencia de los servidores de Wall Street. 
                                </Text>
                                <Text className="text-gray-300 text-xl leading-relaxed font-medium block text-justify md:text-center">
                                    Hemos construido el puente definitivo entre la tecnología cuantitativa y el inversor moderno. No predecimos el futuro; <span className="text-[var(--color-gold)]">reaccionamos matemáticamente al presente.</span>
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