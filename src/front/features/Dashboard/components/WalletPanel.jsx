import React from "react";

/**
 * Panel lateral derecho con wallets disponibles/conectadas.
 * Colores del sistema de diseño: gold/olive para positivo, rojo solo para negativo.
 * TODO: Reemplazar MOCK_WALLETS con llamada a GET /api/wallets cuando el backend esté listo.
 */
const MOCK_WALLETS = [
    { id: 1, name: "Ethereum", symbol: "ETH", amount: 0.924574, amountUSD: 1500, icon: "Ξ", change: -52.49 },
    { id: 2, name: "Bitcoin", symbol: "BTC", amount: 0.924574, amountUSD: 22741, icon: "₿", change: 12.31 },
    { id: 3, name: "Solana", symbol: "SOL", amount: 0.924574, amountUSD: 5143, icon: "◎", change: -52.49 },
    { id: 4, name: "USDC Coin", symbol: "USDC", amount: 0.924574, amountUSD: 5143, icon: "◎", change: 0.01 },
];

export const WalletPanel = () => {
    return (
        <div
            className="rounded-2xl p-5 flex flex-col gap-4 border border-white/[0.06]"
            style={{ background: "rgba(255,255,255,0.03)", backdropFilter: "blur(16px)" }}
        >
            {/* Cabecera */}
            <div className="flex items-center justify-between">
                <h2 className="text-sm font-semibold text-white">Wallets</h2>
                <span
                    className="text-[11px] font-bold px-2.5 py-1 rounded-full border"
                    style={{
                        color: "var(--color-gold)",
                        background: "rgba(195,143,55,0.1)",
                        borderColor: "rgba(195,143,55,0.2)",
                    }}
                >
                    {MOCK_WALLETS.length} disponibles
                </span>
            </div>

            {/* Balance total */}
            <div
                className="flex flex-col gap-2 p-4 rounded-xl border border-white/[0.05]"
                style={{ background: "rgba(255,255,255,0.02)" }}
            >
                <p className="text-[11px] text-white/30">Balance total</p>
                <p className="text-2xl font-bold text-white tracking-tight leading-none">
                    1,500 <span className="text-sm font-normal text-white/25">USD</span>
                </p>
                {/* Barra de distribución por activo */}
                <div className="w-full h-2 bg-white/[0.05] rounded-full mt-1 overflow-hidden flex">
                    <div className="h-full bg-[var(--color-gold)]" style={{ width: "60%" }} />
                    <div className="h-full bg-[var(--color-olive)]" style={{ width: "25%" }} />
                    <div className="h-full bg-[var(--color-brown-medium)]" style={{ width: "15%" }} />
                </div>
                <div className="flex justify-between text-[10px] text-white/20 mt-0.5">
                    <span>0%</span><span>34</span><span>65</span><span>100%</span>
                </div>
            </div>

            {/* Lista de wallets */}
            <div className="flex flex-col divide-y divide-white/[0.04]">
                {MOCK_WALLETS.map((wallet) => {
                    const isPositive = wallet.change >= 0;
                    return (
                        <div
                            key={wallet.id}
                            className="flex items-center gap-3 px-2 py-3 hover:bg-white/[0.03] transition-all cursor-pointer"
                        >
                            {/* Icono */}
                            <div className="w-8 h-8 rounded-xl bg-white/[0.06] border border-white/[0.07] flex items-center justify-center text-sm flex-shrink-0">
                                {wallet.icon}
                            </div>

                            {/* Nombre + cantidad — ocupa el espacio disponible */}
                            <div className="flex flex-col min-w-0 flex-1">
                                <p className="text-xs font-semibold text-white leading-tight truncate">{wallet.name}</p>
                                <p className="text-[10px] text-white/30 leading-tight mt-0.5 truncate">{wallet.amount} {wallet.symbol}</p>
                            </div>

                            {/* USD + % — siempre alineado a la derecha, nunca se comprime */}
                            <div className="flex flex-col items-end flex-shrink-0">
                                <p className="text-xs font-semibold text-white leading-tight">${wallet.amountUSD.toLocaleString()}</p>
                                <p
                                    className="text-[10px] font-medium leading-tight mt-0.5"
                                    style={{ color: isPositive ? "var(--color-olive)" : "#f87171" }}
                                >
                                    {isPositive ? "+" : ""}{wallet.change}%
                                </p>
                            </div>
                        </div>
                    );
                })}
            </div>

            {/* Bloque inferior: gas + CTA con respiración visual */}
            <div className="flex flex-col gap-3 mt-2">
                {/* Info de gas y tasas */}
                <div
                    className="flex flex-col gap-2 px-3 py-3 rounded-xl border border-white/[0.05]"
                    style={{ background: "rgba(255,255,255,0.02)" }}
                >
                    <div className="flex justify-between items-center">
                        <span className="text-[11px] text-white/30">1 BTC</span>
                        <span className="text-[11px] font-semibold text-white">$22,741</span>
                    </div>
                    <div className="flex justify-between items-center">
                        <span className="text-[11px] text-white/30">USDT</span>
                        <span className="text-[11px] font-semibold text-white">25%</span>
                    </div>
                    <div className="flex justify-between items-center">
                        <span className="text-[11px] text-white/30">Gas fee</span>
                        <span className="text-[11px] font-semibold text-white">$1.4</span>
                    </div>
                </div>

                {/* CTA Connect Wallet */}
                <button
                    className="w-full py-3 rounded-xl text-sm font-semibold transition-all hover:opacity-90 border text-center"
                    style={{
                        color: "var(--color-gold)",
                        borderColor: "rgba(195,143,55,0.3)",
                        background: "rgba(195,143,55,0.06)",
                        letterSpacing: "0.02em",
                    }}
                >
                    Connect Wallet
                </button>
            </div>
        </div>
    );
};
