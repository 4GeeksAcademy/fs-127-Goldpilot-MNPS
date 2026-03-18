import React from "react";
import { Container } from "@radix-ui/themes";
import { motion } from "framer-motion";

export const RiskSection = () => {
    return (
        <section className="relative w-full pt-52 pb-60 bg-black flex items-center justify-center overflow-hidden">

            <div className="absolute inset-0 bg-black z-0 pointer-events-none" />

            <Container size="3" className="relative z-10 px-6 text-center">
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, ease: "easeOut" }}
                    viewport={{ once: true, margin: "-10%" }}
                    className="flex flex-col items-center gap-12" 
                >
                    <div className="flex flex-col items-center leading-[0.9] tracking-tighter">

                        <h2 className="text-[clamp(4rem,10vw,90px)] whitespace-nowrap font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-white to-gray-800 opacity-90 select-none" style={{ lineHeight: 1.15, paddingBottom: "0.1em" }}>
                            Más allá del riesgo.
                        </h2>

                        <h2
                            className="text-[clamp(4rem,10vw,80px)] whitespace-nowrap leading-none font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-white to-gray-800 opacity-90 select-none"
                            style={{
                                background: "linear-gradient(180deg, #FFFFFF 0%, var(--color-gold) 100%)",
                                WebkitBackgroundClip: "text",
                                WebkitTextFillColor: "transparent",
                                paddingBottom: "0.2em"
                            }}
                        >
                            Seguridad.
                        </h2>
                    </div>

                    <div
                        style={{
                            textAlign: 'center',
                            ustifyContent: 'center',
                            display: 'flex',
                            flexDirection: 'column',
                            color: 'var(--color-grey-50, #808080)',
                            fontSize: '29px', 
                            fontFamily: 'Roboto, sans-serif',
                            fontWeight: 400, 
                            lineHeight: '1.',
                            wordWrap: 'break-word',
                            maxWidth: '3000px',
                        }}
                    >
                        Accede a una forma más inteligente de invertir en oro compra y vende oro digital respaldado, con la confianza de seguir el precio real del mercado y la flexibilidad de operar al instante a nivel global. Todo de manera sencilla, transparente y gestionado directamente desde tu asistente.
                    </div>

                </motion.div>
            </Container>
        </section>
    );
};