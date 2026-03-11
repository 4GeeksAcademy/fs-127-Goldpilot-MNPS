import React from "react";

export const AdBanner = ({ className = "" }) => {
    return (
        <div
            className={`relative overflow-hidden rounded-2xl flex flex-col md:flex-row items-center border border-[rgba(195,143,55,0.18)] ${className}`}
            style={{
                background:
                    "linear-gradient(135deg, rgba(20,28,14,0.9) 0%, rgba(99,119,66,0.15) 100%)",
                backdropFilter: "blur(20px)",
            }}
        >
            {/* Orbs Decorativos */}
            <div
                className="absolute -top-32 -left-20 w-80 h-80 rounded-full opacity-10 blur-3xl pointer-events-none"
                style={{ background: "var(--color-gold)" }}
            />
            <div
                className="absolute -bottom-16 -right-16 w-64 h-64 rounded-full opacity-10 blur-3xl pointer-events-none"
                style={{ background: "var(--color-olive)" }}
            />

            {/* Contenedor Principal */}
            <div className="relative z-10 w-full flex flex-col md:flex-row items-center p-6 md:px-8 gap-6 md:gap-8 justify-between">

                {/* Agrupación Izquierda: Logo + Separador + Texto */}
                <div className="flex flex-col md:flex-row items-center gap-6 flex-1 text-center md:text-left">
                    {/* Logo Pequeño */}
                    <div className="flex-shrink-0 flex items-center justify-center">
                        <img
                            src="/logo-principal-blanco.png"
                            alt="GoldPilot"
                            className="h-10 md:h-12 w-auto drop-shadow-md"
                        />
                    </div>

                    {/* Separador Desktop */}
                    <div className="hidden md:block w-px h-12 bg-white/10" />

                    {/* Textos Claros */}
                    <div className="flex flex-col flex-1 gap-1">
                        <h3 className="text-xl md:text-2xl font-black text-white leading-tight tracking-tight">
                            Maximiza tu potencial con <span style={{ color: "var(--color-gold)" }}>GoldPilot PRO</span>
                        </h3>
                        <p className="text-sm text-white/50 leading-relaxed max-w-2xl">
                            Desbloquea el acceso a estrategias avanzadas, herramientas de análisis y alertas exclusivas en tiempo real.
                        </p>
                    </div>
                </div>

                {/* Botón CTA a la Derecha */}
                <div className="flex-shrink-0 w-full md:w-auto mt-2 md:mt-0">
                    <button
                        className="w-full md:w-auto px-8 py-3.5 rounded-xl text-sm font-black transition-all hover:scale-105 tracking-wide flex items-center justify-center gap-2"
                        style={{
                            background: "var(--gradient-gold)",
                            color: "#1a1005",
                            boxShadow: "0 8px 24px rgba(195,143,55,0.25)",
                        }}
                    >
                        Hazte Pro Ahora →
                    </button>
                </div>
            </div>

            {/* Cierre (Dismiss) */}
            <button className="absolute top-4 right-4 text-white/20 hover:text-white/50 text-xl transition-colors z-20 leading-none">×</button>
        </div>
    );
};
