import React, { useEffect } from "react";
import { Theme, Container, Grid, Flex, Text, Section } from "@radix-ui/themes";
import "@radix-ui/themes/styles.css";
import { motion } from "framer-motion";
import { Navbar } from "../features/Landing/components/Navbar";
import { Footer } from "../features/Landing/components/Footer";

export const ApiPage = () => {

    useEffect(() => {
        window.scrollTo(0, 0);
    }, []);

    const endpoints = [
        {
            method: "GET",
            color: "text-green-400",
            path: "/v1/market/signals",
            desc: "Obtén el flujo de señales algorítmicas en tiempo real para Gold (XAUUSD)."
        },
        {
            method: "POST",
            color: "text-blue-400",
            path: "/v1/trade/execute",
            desc: "Envía una orden directa de ejecución a través de tu túnel seguro de MetaApi."
        },
        {
            method: "WSS",
            color: "text-[var(--color-gold)]",
            path: "wss://stream.xsniper.com",
            desc: "Conexión WebSocket para monitoreo de latencia y telemetría de ticks."
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
                                DEVELOPERS <br/> & API REST
                            </h1>
                            
                            <Text className="text-gray-400 text-xl md:text-3xl max-w-4xl mx-auto block leading-relaxed font-light tracking-tight">
                                Conecta tu infraestructura directamente al motor <span className="text-white font-medium">XSNIPER</span>. Latencia ultrabaja, ejecución institucional y WebSockets.
                            </Text>
                        </motion.div>

                        {/* SECCIÓN DE CÓDIGO & ENDPOINTS */}
                        <Grid columns={{ initial: "1", lg: "2" }} gap="9" className="mb-48" align="center">
                            
                            {/* Bloque de Código Visual */}
                            <motion.div
                                initial={{ opacity: 0, x: -30 }}
                                whileInView={{ opacity: 1, x: 0 }}
                                viewport={{ once: true }}
                                className="bg-[#050505] border border-white/10 rounded-2xl overflow-hidden shadow-2xl"
                            >
                                <div className="bg-white/5 px-6 py-4 border-b border-white/5 flex gap-2">
                                    <div className="w-3 h-3 rounded-full bg-red-500/80" />
                                    <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
                                    <div className="w-3 h-3 rounded-full bg-green-500/80" />
                                </div>
                                <div className="p-8 overflow-x-auto text-sm md:text-base font-mono leading-loose text-gray-300">
                                    <span className="text-purple-400">const</span> xsniper = <span className="text-blue-400">require</span>(<span className="text-green-300">'@xsniper/sdk'</span>);<br/><br/>
                                    <span className="text-purple-400">const</span> client = <span className="text-purple-400">new</span> xsniper.<span className="text-yellow-200">Client</span>({`{`}<br/>
                                    &nbsp;&nbsp;apiKey: process.env.<span className="text-white">XSNIPER_API_KEY</span>,<br/>
                                    &nbsp;&nbsp;environment: <span className="text-green-300">'production'</span><br/>
                                    {`}`});<br/><br/>
                                    <span className="text-gray-500">// Escuchar señales del Oro</span><br/>
                                    client.streams.<span className="text-blue-300">gold</span>(<span className="text-yellow-200">signal</span> <span className="text-purple-400">=&gt;</span> {`{`}<br/>
                                    &nbsp;&nbsp;<span className="text-purple-400">if</span> (signal.confidence &gt; <span className="text-orange-400">0.95</span>) {`{`}<br/>
                                    &nbsp;&nbsp;&nbsp;&nbsp;client.trade.<span className="text-blue-300">execute</span>(signal);<br/>
                                    &nbsp;&nbsp;{`}`}<br/>
                                    {`}`});
                                </div>
                            </motion.div>

                            {/* Lista de Endpoints */}
                            <motion.div initial={{ opacity: 0, x: 30 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }}>
                                <div className="space-y-6">
                                    {endpoints.map((ep, i) => (
                                        <div key={i} className="p-6 rounded-[24px] bg-white/5 border border-white/5 hover:border-[var(--color-gold)]/30 transition-colors group">
                                            <Flex gap="4" align="center" className="mb-3">
                                                <span className={`${ep.color} font-mono font-bold text-sm bg-white/5 px-3 py-1 rounded-md`}>
                                                    {ep.method}
                                                </span>
                                                <Text className="font-mono text-white tracking-tight">
                                                    {ep.path}
                                                </Text>
                                            </Flex>
                                            <Text className="text-gray-400 font-light leading-relaxed">
                                                {ep.desc}
                                            </Text>
                                        </div>
                                    ))}
                                </div>
                            </motion.div>

                        </Grid>

                        {/* CTA API KEY */}
                        <Section className="border-t border-white/5 pt-20 flex flex-col items-center text-center mb-10">
                            <Text className="text-[var(--color-gold)] font-bold text-sm uppercase tracking-widest mb-6 block">
                                Entorno de Pruebas
                            </Text>
                            <h2 className="text-3xl md:text-5xl font-black text-white mb-8">
                                OBTÉN TU SANDBOX KEY
                            </h2>
                            <Text className="text-gray-400 text-xl max-w-2xl mb-10 font-light">
                                Crea una cuenta gratuita para acceder al entorno de pruebas (Sandbox) y lee la documentación completa.
                            </Text>
                            <button className="px-10 py-5 rounded-full bg-[var(--color-gold)] text-black font-bold tracking-widest uppercase hover:bg-white hover:scale-105 transition-all duration-300 shadow-[0_0_30px_rgba(212,175,55,0.2)]">
                                Leer Documentación
                            </button>
                        </Section>

                    </Container>
                </main>

                <Footer />
            </div>
        </Theme>
    );
};