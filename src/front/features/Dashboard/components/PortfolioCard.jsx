import React from "react";

/**
 * Tarjeta de estadística del portfolio de trading.
 * Muestra métricas reales de cuenta: Balance, Equity, P&L, Win Rate.
 * Nombre alineado con el doc del proyecto (sección 5.1 Componentes: PortfolioCard).
 *
 * @param {string}  props.title    - Título de la métrica (ej: "Balance")
 * @param {string}  props.value    - Valor formateado (ej: "$10,000.00")
 * @param {string}  props.subtitle - Subtítulo descriptivo (ej: "USD" o "Real-time")
 * @param {string}  props.icon     - Emoji o carácter del icono
 * @param {'up'|'down'} [props.trend] - Tendencia opcional para la barra inferior
 * @param {'gold'|'green'|'red'|'blue'} [props.color] - Paleta de color del acento
 */
export const PortfolioCard = ({
    title = "Métrica",
    value = "--",
    subtitle = "",
    icon = "◈",
    trend,
    color = "gold",
}) => {
    /** Paleta de acento por color nombrado */
    const PALETTE = {
        gold: { orb: "var(--color-gold)", bar: "var(--color-gold)", badge: "rgba(195,143,55,0.15)", text: "var(--color-gold)" },
        green: { orb: "var(--color-olive)", bar: "var(--color-olive)", badge: "rgba(99,119,66,0.15)", text: "var(--color-olive)" },
        red: { orb: "#ef4444", bar: "#ef4444", badge: "rgba(239,68,68,0.12)", text: "#f87171" },
        blue: { orb: "rgba(96,165,250,0.9)", bar: "rgba(96,165,250,0.9)", badge: "rgba(96,165,250,0.12)", text: "rgba(96,165,250,1)" },
    };

    const palette = PALETTE[color] ?? PALETTE.gold;
    const barWidth = trend === "up" ? "72%" : trend === "down" ? "35%" : "55%";

    return (
        <div
            className="relative overflow-hidden rounded-2xl p-6 flex flex-col gap-5 border border-white/[0.06] hover:border-white/10 transition-all group cursor-pointer h-full"
            style={{ background: "rgba(255,255,255,0.03)", backdropFilter: "blur(16px)" }}
        >
            {/* Orb decorativo */}
            <div
                className="absolute -top-6 -right-6 w-24 h-24 rounded-full blur-2xl opacity-10 pointer-events-none transition-opacity group-hover:opacity-20"
                style={{ background: palette.orb }}
            />

            {/* Cabecera: icono + título */}
            <div className="flex items-center justify-between relative z-10">
                <div className="flex items-center gap-3 min-w-0 flex-1 overflow-hidden mr-2">
                    <div
                        className="w-9 h-9 rounded-xl flex items-center justify-center text-lg flex-shrink-0 border border-white/[0.08]"
                        style={{ background: palette.badge }}
                    >
                        <span style={{ color: palette.text }}>{icon}</span>
                    </div>
                    <p className="text-sm font-semibold text-white/60 leading-none">{title}</p>
                </div>

                {trend && (
                    <span
                        className="text-[11px] font-bold px-2.5 py-1 rounded-full flex-shrink-0"
                        style={{ background: palette.badge, color: palette.text }}
                    >
                        {trend === "up" ? "▲" : "▼"}
                    </span>
                )}
            </div>

            {/* Valor principal */}
            <div className="relative z-10">
                <p className="text-xl font-bold tracking-tight text-white leading-none">{value}</p>
                {subtitle && <p className="text-[11px] text-white/25 mt-1">{subtitle}</p>}
            </div>

            {/* Barra de acento inferior */}
            <div className="w-full h-[3px] rounded-full bg-white/[0.05] overflow-hidden relative z-10">
                <div
                    className="h-full rounded-full transition-all duration-1000"
                    style={{ width: barWidth, background: palette.bar }}
                />
            </div>
        </div>
    );
};
