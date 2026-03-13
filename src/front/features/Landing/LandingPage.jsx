import React, { useEffect } from "react"; // <-- 1. Importamos useEffect
import { Theme } from "@radix-ui/themes";
import "@radix-ui/themes/styles.css";
import { Navbar } from "./components/Navbar";
import { Hero } from "./components/Hero";
import { RiskSection } from "./components/RiskSection";
import { Footer } from "./components/Footer";

/**
 * Componente LandingPage.
 * Orquesta todas las secciones de la página de aterrizaje pública.
 * Envuelto en Radix UI Theme para un diseño consistente.
 */
const LandingPage = () => {

    // 2. MAGIA DE SCROLL: Forzar el inicio de la página al entrar
    useEffect(() => {
        window.scrollTo(0, 0);
    }, []);

    return (
        <Theme appearance="dark" accentColor="amber" grayColor="slate" panelBackground="translucent" radius="large">
            <div className="min-h-screen font-sans selection:bg-[#D4AF37] selection:text-black">
                <Navbar />
                <main>
                    <Hero />
                    <RiskSection />
                </main>
                <Footer />
            </div>
        </Theme>
    );
};

export default LandingPage;