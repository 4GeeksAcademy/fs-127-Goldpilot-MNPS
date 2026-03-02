import React from "react";
import { Theme, Container } from "@radix-ui/themes";
import { StrategiesCard } from "../components/strategies/StrategiesCard.jsx";

export const Home = () => {
    return (
        <Theme appearance="dark">
            <main className="min-h-screen bg-black pt-32 pb-20">
                <Container size="4">
                    <div className="text-center mb-16">
                        <h1 className="text-5xl md:text-6xl font-medium text-white tracking-tighter mb-4">
                            Configuración de <span style={{
                                background: "linear-gradient(180deg, #FFFFFF 0%, var(--color-gold) 100%)",
                                WebkitBackgroundClip: "text",
                                WebkitTextFillColor: "transparent",
                            }}>Sniper</span>
                        </h1>
                        <p className="text-gray-500 text-xl font-light">
                            Define el comportamiento de tu conserje digital.
                        </p>
                    </div>

                    <StrategiesCard />
                </Container>
            </main>
        </Theme>
    );
};