import React from "react";

/**
 * Componente Hero para la Landing Page - VERSIÓN LIMPIA.
 * Solo muestra el video de fondo "Liquid Gold" sin texto ni botones sobrepuestos,
 * permitiendo que la interfaz respire y el foco esté en el movimiento del oro.
 */
export const Hero = () => {
    return (
        <section className="relative h-screen w-full flex items-center justify-center overflow-hidden">
            {/* FONDO DE VIDEO (Forzado) */}
            <div className="absolute inset-0 z-0">
                {/* Overlay sutil para matizar el brillo si es necesario, pero manteniendo la claridad */}
                <div className="absolute inset-0 bg-black/20 z-10" />

                <video
                    autoPlay
                    loop
                    muted
                    playsInline
                    className="w-full h-full object-cover scale-105"
                >
                    {/* Fuentes de video de oro líquido */}
                    <source src="https://assets.mixkit.co/videos/preview/mixkit-liquid-gold-swirling-in-a-dark-container-30231-large.mp4" type="video/mp4" />
                    <source src="https://cdn.coverr.co/videos/coverr-molten-gold-5347/1080p.mp4" type="video/mp4" />
                </video>
            </div>

            {/* ELEMENTOS DECORATIVOS: Degradado inferior para transición suave hacia la siguiente sección */}
            <div className="absolute bottom-0 w-full h-40 bg-gradient-to-t from-[var(--color-brown-dark)] to-transparent z-20" />
        </section>
    );
};
