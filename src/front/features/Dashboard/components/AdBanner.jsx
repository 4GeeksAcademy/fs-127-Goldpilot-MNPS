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

            {/* Logo Section */}
            <div className="relative flex items-center justify-center p-8 md:px-12 md:border-r border-white/[0.05] flex-shrink-0">
                <img
                    src="/logo-principal-blanco.png"
                    alt="GoldPilot"
                    className="h-14 w-auto drop-shadow-lg z-10"
                />
            </div>

            {/* Contenido & Stats */}
            <div className="relative z-10 flex flex-col md:flex-row flex-1 p-6 md:px-8 gap-6 md:gap-10 items-center justify-between">

                {/* Textos */}
                <div className="flex flex-col gap-2 flex-1 text-center md:text-left">
                    <div className="flex items-center gap-2 justify-center md:justify-start">
                        <span
                            className="text-[10px] font-bold tracking-widest uppercase"
                            style={{ color: "var(--color-gold)" }}
                        >
                            Haz el salto
                        </span>
                    </div>

                    <h3 className="text-xl md:text-2xl font-black text-white leading-tight tracking-tight mt-1">
                        Desbloquea Funciones Avanzadas
                    </h3>
                    <p className="text-sm text-white/40 leading-relaxed max-w-lg">
                        Multiplica tu potencial con estrategias exclusivas, alertas y reportes completos. <span style={{ color: "text-white font-medium" }}>Sube al siguiente nivel hoy</span>.
                    </p>
                </div>

                {/* Stats */}
                <div className="flex gap-4 md:gap-6 flex-shrink-0">
                    {[
                        { label: "ROI Histórico", value: "+127%" },
                        { label: "Alertas VIP", value: "Activas" },
                    ].map((stat) => (
                        <div key={stat.label} className="flex flex-col gap-0">
                            <p className="text-xl font-black" style={{ color: "var(--color-gold)" }}>{stat.value}</p>
                            <p className="text-[10px] text-white/40 uppercase tracking-widest mt-0.5">{stat.label}</p>
                        </div>
                    ))}
                </div>

                {/* Botón */}
                <div className="mt-2 md:mt-0 flex-shrink-0 w-full md:w-auto">
                    <button
                        className="w-full md:w-auto px-8 py-3.5 rounded-xl text-sm font-black transition-all hover:opacity-90 tracking-wide"
                        style={{
                            background: "var(--gradient-gold)",
                            color: "#1a1005",
                            boxShadow: "0 8px 24px rgba(195,143,55,0.25)",
                        }}
                    >
                        Mejorar a Pro →
                    </button>
                </div>

            </div>

            {/* Botón cerrar opcional (absoluto) */}
            <button className="absolute top-4 right-5 text-white/20 hover:text-white/50 text-xs transition-colors z-20">✕</button>
        </div>
    );
};
