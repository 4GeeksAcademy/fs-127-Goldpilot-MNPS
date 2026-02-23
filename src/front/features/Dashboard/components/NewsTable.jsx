import React from "react";

/**
 * Tabla de noticias y transacciones del mercado crypto.
 * Datos mock de muestra para desarrollo.
 * TODO: Conectar con endpoint del backend GET /api/market/news cuando el compañero lo implemente.
 */
const MOCK_NEWS = [
    {
        id: 1,
        name: "Bitcoin",
        symbol: "BTC",
        icon: "₿",
        date: "15 Jan, 2023",
        lastPrice: "$28,165",
        status: "success",
        amount: "2.3 BTC",
        change: -18.66,
    },
    {
        id: 2,
        name: "Ethereum",
        symbol: "ETH",
        icon: "Ξ",
        date: "15 Jan, 2023",
        lastPrice: "$1,623",
        status: "success",
        amount: "2.3 ETH",
        change: 3.21,
    },
    {
        id: 3,
        name: "Solana",
        symbol: "SOL",
        icon: "◎",
        date: "14 Jan, 2023",
        lastPrice: "$22.50",
        status: "pending",
        amount: "15 SOL",
        change: -7.44,
    },
    {
        id: 4,
        name: "USDC",
        symbol: "USDC",
        icon: "◎",
        date: "13 Jan, 2023",
        lastPrice: "$1.00",
        status: "success",
        amount: "500 USDC",
        change: 0.01,
    },
    {
        id: 5,
        name: "Dogecoin",
        symbol: "DOGE",
        icon: "Ð",
        date: "12 Jan, 2023",
        lastPrice: "$0.081",
        status: "failed",
        amount: "10,000 DOGE",
        change: -12.3,
    },
];

/** Mapa de estado a estilos visuales */
const STATUS_STYLES = {
    success: { dot: "bg-emerald-400", label: "text-emerald-400", text: "Exitoso" },
    pending: { dot: "bg-yellow-400", label: "text-yellow-400", text: "Pendiente" },
    failed: { dot: "bg-red-400", label: "text-red-400", text: "Fallido" },
};

export const NewsTable = () => {
    return (
        <div className="liquid-glass border border-white/5 rounded-2xl overflow-hidden">
            {/* Cabecera de la tabla */}
            <div className="flex items-center justify-between p-5 border-b border-white/5">
                <h2 className="text-sm font-semibold text-white">Mercados</h2>
                <button className="w-8 h-8 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center text-white/50 hover:text-white hover:bg-white/10 transition-all text-xs">
                    →
                </button>
            </div>

            {/* Tabla */}
            <div className="overflow-x-auto">
                <table className="w-full">
                    <thead>
                        <tr className="text-[10px] font-medium text-white/30 uppercase tracking-wider">
                            <th className="text-left px-5 py-3">Nombre</th>
                            <th className="text-left px-4 py-3 hidden sm:table-cell">Fecha</th>
                            <th className="text-left px-4 py-3 hidden md:table-cell">Último Precio</th>
                            <th className="text-left px-4 py-3 hidden lg:table-cell">Estado</th>
                            <th className="text-right px-5 py-3">Cantidad</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-white/[0.03]">
                        {MOCK_NEWS.map((item) => {
                            const status = STATUS_STYLES[item.status] ?? STATUS_STYLES.pending;
                            const isPositive = item.change >= 0;

                            return (
                                <tr
                                    key={item.id}
                                    className="hover:bg-white/[0.02] transition-colors cursor-pointer"
                                >
                                    {/* Nombre + ícono */}
                                    <td className="px-5 py-4">
                                        <div className="flex items-center gap-3">
                                            <div className="w-9 h-9 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center text-base shrink-0">
                                                {item.icon}
                                            </div>
                                            <div>
                                                <p className="text-sm font-semibold text-white leading-none">
                                                    {item.name}
                                                </p>
                                                <p
                                                    className={`text-[10px] font-medium mt-0.5 ${isPositive ? "text-emerald-400" : "text-red-400"
                                                        }`}
                                                >
                                                    {isPositive ? "+" : ""}{item.change}%
                                                </p>
                                            </div>
                                        </div>
                                    </td>

                                    {/* Fecha */}
                                    <td className="px-4 py-4 hidden sm:table-cell">
                                        <span className="text-xs text-white/40">{item.date}</span>
                                    </td>

                                    {/* Precio */}
                                    <td className="px-4 py-4 hidden md:table-cell">
                                        <span className="text-sm font-medium text-white">{item.lastPrice}</span>
                                    </td>

                                    {/* Estado */}
                                    <td className="px-4 py-4 hidden lg:table-cell">
                                        <div className="flex items-center gap-2">
                                            <div className={`w-1.5 h-1.5 rounded-full ${status.dot}`} />
                                            <span className={`text-xs ${status.label}`}>{status.text}</span>
                                        </div>
                                    </td>

                                    {/* Cantidad */}
                                    <td className="px-5 py-4 text-right">
                                        <span className="text-sm font-bold text-white">{item.amount}</span>
                                    </td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>
        </div>
    );
};
