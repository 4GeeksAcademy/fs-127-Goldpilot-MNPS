import React from "react";

/**
 * Banner publicitario ficticio — crece para llenar todo el espacio del sidebar derecho.
 * Contenido escalado: tipografía grande + imagen decorativa coherente con el tamaño.
 * TODO: Reemplazar con datos reales de campaña cuando estén disponibles.
 */
export const AdBanner = ({ className = "" }) => {
    return (
        <div
            className={`relative overflow-hidden rounded-2xl flex flex-col border border-[rgba(195,143,55,0.18)] ${className}`}
            style={{
                background:
                    "linear-gradient(160deg, rgba(195,143,55,0.14) 0%, rgba(20,28,14,0.85) 45%, rgba(99,119,66,0.09) 100%)",
                backdropFilter: "blur(20px)",
            }}
        >
            {/* Orb decorativo superior */}
            <div
                className="absolute -top-16 -right-16 w-56 h-56 rounded-full opacity-20 blur-3xl pointer-events-none"
                style={{ background: "var(--color-gold)" }}
            />
            <div
                className="absolute bottom-0 left-0 w-48 h-48 rounded-full opacity-10 blur-3xl pointer-events-none"
                style={{ background: "var(--color-olive)" }}
            />

            {/* Imagen decorativa centrañ */}
            <div className="relative flex items-center justify-center py-10 flex-1">
                {/* Aura exterior */}
                <div
                    className="absolute w-40 h-40 rounded-full blur-3xl opacity-20"
                    style={{ background: "var(--color-gold)" }}
                />
                {/* Círculo decorativo con logo XS */}
                <div
                    className="relative w-28 h-28 rounded-full flex items-center justify-center text-5xl font-black text-black z-10"
                    style={{
                        background: "var(--gradient-gold)",
                        boxShadow: "0 0 40px rgba(195,143,55,0.4), 0 0 80px rgba(195,143,55,0.15)",
                    }}
                >
                    XS
                </div>
            </div>

            {/* Contenido textual inferior */}
            <div className="relative z-10 flex flex-col gap-4 p-6 pt-0">
                {/* Tag */}
                <div className="flex items-center gap-2">
                    <span
                        className="text-[10px] font-bold tracking-widest uppercase"
                        style={{ color: "var(--color-gold)" }}
                    >
                        Patrocinado
                    </span>
                    <div className="h-px flex-1" style={{ background: "rgba(195,143,55,0.2)" }} />
                    <button className="text-white/20 hover:text-white/50 text-xs transition-colors">✕</button>
                </div>

                {/* Titular grande */}
                <div className="flex flex-col gap-2">
                    <h3 className="text-2xl font-black text-white leading-tight tracking-tight">
                        Maximiza<br />
                        tus ganancias
                    </h3>
                    <p className="text-sm text-white/40 leading-relaxed">
                        Estrategias avanzadas, alertas en tiempo real y análisis de mercado exclusivos con <span style={{ color: "var(--color-gold)" }}>GoldPilot Pro</span>.
                    </p>
                </div>

                {/* Stats rápidas */}
                <div className="grid grid-cols-2 gap-3">
                    {[
                        { label: "ROI Promedio", value: "+127%" },
                        { label: "Usuarios Pro", value: "4,200+" },
                    ].map((stat) => (
                        <div
                            key={stat.label}
                            className="flex flex-col gap-0.5 p-3 rounded-xl border border-white/[0.06]"
                            style={{ background: "rgba(255,255,255,0.03)" }}
                        >
                            <p className="text-lg font-bold" style={{ color: "var(--color-gold)" }}>{stat.value}</p>
                            <p className="text-[10px] text-white/30">{stat.label}</p>
                        </div>
                    ))}
                </div>

                {/* CTA */}
                <button
                    className="w-full py-3.5 rounded-xl text-sm font-black transition-all hover:opacity-90 tracking-wide"
                    style={{
                        background: "var(--gradient-gold)",
                        color: "#1a1005",
                        boxShadow: "0 8px 24px rgba(195,143,55,0.3)",
                    }}
                >
                    Explorar Pro →
                </button>
            </div>
        </div>
    );
};
