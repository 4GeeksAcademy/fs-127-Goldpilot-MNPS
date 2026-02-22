import React from "react";

/**
 * Tarjeta de resumen de una wallet (componente primario y reutilizable).
 * Positivo → colores del sistema de diseño (gold/olive).
 * Negativo → rojo (único uso permitido del rojo en el sistema).
 *
 * @param {Object} props
 * @param {string} props.name - Nombre del activo (ej: "Bitcoin")
 * @param {string} props.symbol - Símbolo del activo (ej: "BTC")
 * @param {string} props.icon - Emoji/icono del activo
 * @param {number} props.balanceUSD - Balance en USD
 * @param {number} props.changePercent - Porcentaje de cambio (positivo o negativo)
 */
export const OverviewCard = ({
    name = "Bitcoin",
    symbol = "BTC",
    icon = "₿",
    balanceUSD = 42350.21,
    changePercent = -6.75,
}) => {
    const isPositive = changePercent >= 0;

    /* Paleta del sistema de diseño según rendimiento */
    const colorPositive = {
        badge: "bg-[rgba(99,119,66,0.15)] text-[var(--color-olive)] border border-[rgba(99,119,66,0.25)]",
        bar: "bg-[var(--color-olive)]",
        icon: "text-[var(--color-olive)]",
    };

    const colorNegative = {
        badge: "bg-red-500/10 text-red-400 border border-red-500/20",
        bar: "bg-red-500",
        icon: "text-red-400",
    };

    const color = isPositive ? colorPositive : colorNegative;

    return (
        <div
            className="relative overflow-hidden rounded-2xl p-5 flex flex-col gap-4 border border-white/[0.06] hover:border-white/10 transition-all group cursor-pointer h-full"
            style={{
                background: "rgba(255,255,255,0.03)",
                backdropFilter: "blur(16px)",
            }}
        >
            {/* Orb decorativo */}
            <div
                className="absolute -top-6 -right-6 w-24 h-24 rounded-full blur-2xl opacity-10 pointer-events-none transition-opacity group-hover:opacity-20"
                style={{
                    background: isPositive ? "var(--color-olive)" : "#ef4444",
                }}
            />

            {/* Cabecera: icono + símbolo + badge rendimiento */}
            <div className="flex items-center justify-between relative z-10">
                <div className="flex items-center gap-3 min-w-0 flex-1 overflow-hidden mr-2">
                    <div className="w-9 h-9 rounded-xl bg-white/[0.06] border border-white/[0.08] flex items-center justify-center text-lg flex-shrink-0">
                        {icon}
                    </div>
                    <div className="min-w-0">
                        <p className="text-sm font-semibold text-white leading-none truncate">{name}</p>
                        <p className="text-[11px] text-white/30 mt-0.5">{symbol}</p>
                    </div>
                </div>

                <span className={`flex items-center gap-1 text-[11px] font-bold px-2.5 py-1 rounded-full flex-shrink-0 ${color.badge}`}>
                    {isPositive ? "▲" : "▼"}
                    {Math.abs(changePercent).toFixed(2)}%
                </span>
            </div>

            {/* Balance en USD */}
            <div className="relative z-10">
                <p className="text-xl font-bold tracking-tight text-white leading-none">
                    ${balanceUSD.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                </p>
                <p className="text-[11px] text-white/25 mt-1">Equity en USD</p>
            </div>

            {/* Barra de progreso */}
            <div className="w-full h-[3px] rounded-full bg-white/[0.05] overflow-hidden relative z-10">
                <div
                    className={`h-full rounded-full transition-all duration-1000 ${color.bar}`}
                    style={{ width: `${Math.min(Math.abs(changePercent) * 8, 100)}%` }}
                />
            </div>
        </div>
    );
};
