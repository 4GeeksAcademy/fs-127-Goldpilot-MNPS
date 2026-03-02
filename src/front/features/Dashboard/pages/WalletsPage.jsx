import React from "react";
import { WalletPanel } from "../components/WalletPanel";

export const WalletsPage = () => {
    return (
        <div className="flex flex-col gap-6 p-6 max-w-2xl">
            <div>
                <h1 className="text-xl font-bold text-white">Wallets</h1>
                <p className="text-sm text-white/40 mt-1">Gestiona tus cuentas MetaTrader conectadas</p>
            </div>
            <WalletPanel />
        </div>
    );
};
