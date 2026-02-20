import React from "react";

/**
 * Componente Hero para la Landing Page
 * Muestra el video de fondo "Video para hero.mp4" con un degradado difuminado para integración visual.
 */
export const Hero = () => {
    return (
        <section className="relative h-screen w-full flex items-center justify-center overflow-hidden bg-[var(--color-brown-dark)]">
            {/* FONDO DE VIDEO */}
            <div className="absolute inset-0 z-0">
                {/* 1. LAYER DE VIDEO: Base limpia */}
                <video
                    autoPlay
                    loop
                    muted
                    playsInline
                    className="w-full h-full object-cover scale-105 opacity-90 mix-blend-luminosity"
                >
                    <source src="/assets/videos/hero-background.mp4" type="video/mp4" />
                    Tu navegador no soporta videos HTML5.
                </video>

                {/* 2. LAYER DE COLOR: Tinte dorado/marrón para integrar el video con la marca */}
                <div className="absolute inset-0 bg-[var(--color-brown-dark)] mix-blend-color z-10 opacity-60" />

                {/* 3. LAYER DE PROFUNDIDAD (VIGNETTE): Oscurece los bordes para crear foco central */}
                {/* No usa blur, usa gradiente radial puro para dar sensación de "túnel" o profundidad */}
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,transparent_20%,var(--color-brown-dark)_100%)] z-20 opacity-90" />

                {/* 4. LAYER DE BRILLO SUTIL: Un toque de luz en el centro para resaltar el oro */}
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,var(--color-gold)_0%,transparent_40%)] z-20 mix-blend-overlay opacity-20" />

                {/* 5. TRANSICIÓN INFERIOR: Fundido perfecto hacia el siguiente contenido */}
                <div className="absolute bottom-0 left-0 right-0 h-64 bg-gradient-to-t from-[var(--color-brown-dark)] to-transparent z-30" />
            </div>
        </section>
    );
};
