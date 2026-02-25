import React from "react";

/**
 * Panel lateral de cuenta de trading MetaTrader (MT4/MT5).
 * Muestra el estado de la cuenta conectada via MetaApi y permite añadir una cuenta.
 * Datos basados en el modelo MetaApiAccount + portfolio_snapshots del backend.
 *
 * Columnas de referencia (meta_api_accounts):
 *   meta_account_id, account_type ('demo'|'real'), broker, is_connected
 * Columnas de referencia (portfolio_snapshots):
 *   balance, equity, margin, free_margin, profit
 *
 * TODO: Conectar con GET /api/metaapi/account-info cuando el compañero implemente el servicio.
 */

/** Cuentas MetaTrader conectadas (mock — basado en meta_api_accounts) */
const MOCK_ACCOUNT = {
    broker: "Exness Technologies",
    account_type: "demo",
    is_connected: false,
    balance: 10000.00,
    equity: 10326.40,
    margin: 150.00,
    free_margin: 10176.40,
    currency: "USD",
};

/** Lista mock de wallets/cuentas conectadas (meta_api_accounts) */
const MOCK_WALLETS = [
    { id: 1, meta_account_id: "ACC-00123", broker: "Exness", account_type: "demo", is_connected: true, balance: 10000.00 },
    { id: 2, meta_account_id: "ACC-00456", broker: "ICMarkets", account_type: "real", is_connected: true, balance: 3200.50 },
    { id: 3, meta_account_id: "ACC-00789", broker: "FxPro", account_type: "demo", is_connected: false, balance: 5000.00 },
];

export const WalletPanel = () => {
    const { broker, account_type, is_connected, balance, equity, margin, free_margin, currency } = MOCK_ACCOUNT;

    return (
        <div
            className="rounded-2xl p-5 flex flex-col gap-5 border border-white/[0.06]"
            style={{ background: "rgba(255,255,255,0.03)", backdropFilter: "blur(16px)" }}
        >
            {/* Cabecera */}
            <div className="flex items-center justify-between gap-3">
                <h2 className="text-sm font-semibold text-white">Cuenta MetaTrader</h2>
                <span
                    className="flex items-center gap-1.5 text-[11px] font-bold px-2.5 py-1 rounded-full border"
                    style={is_connected
                        ? { color: "var(--color-olive)", background: "rgba(99,119,66,0.12)", borderColor: "rgba(99,119,66,0.2)" }
                        : { color: "rgba(255,255,255,0.3)", background: "rgba(255,255,255,0.04)", borderColor: "rgba(255,255,255,0.08)" }
                    }
                >
                    <span className="w-1.5 h-1.5 rounded-full inline-block"
                        style={{ background: is_connected ? "var(--color-olive)" : "rgba(255,255,255,0.2)" }} />
                    {is_connected ? "Conectado" : "Desconectado"}
                </span>
            </div>

            {/* Balance y equity */}
            <div
                className="flex flex-col gap-3 p-4 rounded-xl border border-white/[0.05]"
                style={{ background: "rgba(255,255,255,0.02)" }}
            >
                <div>
                    <p className="text-[11px] text-white/30">Balance</p>
                    <p className="text-2xl font-bold text-white tracking-tight leading-none mt-0.5">
                        {balance.toLocaleString("en-US", { minimumFractionDigits: 2 })}
                        <span className="text-sm font-normal text-white/25 ml-1">{currency}</span>
                    </p>
                </div>

                {/* Barra equity vs. balance */}
                <div className="w-full h-2 bg-white/[0.05] rounded-full overflow-hidden">
                    <div
                        className="h-full rounded-full"
                        style={{
                            width: `${Math.min((equity / balance) * 100, 100).toFixed(1)}%`,
                            background: equity >= balance ? "var(--color-olive)" : "#ef4444",
                        }}
                    />
                </div>
                <div className="flex justify-between text-[10px] text-white/20">
                    <span>Balance</span>
                    <span>Equity: ${equity.toLocaleString("en-US", { minimumFractionDigits: 2 })}</span>
                </div>
            </div>

            {/* Wallets / cuentas conectadas */}
            <div className="flex flex-col divide-y divide-white/[0.04]">
                {MOCK_WALLETS.map((wallet) => (
                    <div key={wallet.id} className="flex items-center gap-3 px-1 py-2.5 hover:bg-white/[0.02] transition-colors cursor-pointer">
                        {/* Icono con inicial del broker */}
                        <div className="w-8 h-8 rounded-xl bg-white/5 border border-white/[0.08] flex items-center justify-center text-xs font-bold flex-shrink-0"
                            style={{ color: "var(--color-gold)" }}>
                            {wallet.broker[0]}
                        </div>
                        {/* Broker + tipo */}
                        <div className="flex flex-col min-w-0 flex-1">
                            <p className="text-xs font-semibold text-white leading-tight truncate">{wallet.broker}</p>
                            <p className="text-[10px] text-white/30 leading-tight mt-0.5">{wallet.account_type === "real" ? "Real" : "Demo"} · {wallet.meta_account_id}</p>
                        </div>
                        {/* Balance + estado */}
                        <div className="flex flex-col items-end flex-shrink-0">
                            <p className="text-xs font-semibold text-white">${wallet.balance.toLocaleString()}</p>
                            <span className="text-[10px] mt-0.5" style={{ color: wallet.is_connected ? "var(--color-olive)" : "rgba(255,255,255,0.25)" }}>
                                {wallet.is_connected ? "● Activa" : "○ Inactiva"}
                            </span>
                        </div>
                    </div>
                ))}
            </div>

            {/* Métricas de margen */}
            <div className="flex flex-col divide-y divide-white/[0.04]">
                {[
                    { label: "Margen usado", value: `$${margin.toFixed(2)}` },
                    { label: "Margen libre", value: `$${free_margin.toLocaleString("en-US", { minimumFractionDigits: 2 })}` },
                    { label: "Tipo de cuenta", value: account_type === "demo" ? "Demo" : "Real" },
                    { label: "Broker", value: broker },
                ].map(({ label, value }) => (
                    <div key={label} className="flex items-center justify-between px-1 py-2.5">
                        <span className="text-[11px] text-white/30">{label}</span>
                        <span className="text-[11px] font-semibold text-white/70">{value}</span>
                    </div>
                ))}
            </div>

            {/* CTA — Añadir wallet */}
            <button
                className="w-full py-3 rounded-xl text-sm font-semibold transition-all hover:opacity-90 border text-center"
                style={{
                    color: "var(--color-gold)",
                    borderColor: "rgba(195,143,55,0.3)",
                    background: "rgba(195,143,55,0.06)",
                    letterSpacing: "0.02em",
                }}
            >
                + Añadir Wallet
            </button>
        </div>
    );
};
