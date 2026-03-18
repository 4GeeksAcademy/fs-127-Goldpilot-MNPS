import React from "react";
import { useTranslation } from "react-i18next";
import { WalletPanel } from "../components/WalletPanel";

export const WalletsPage = () => {
    const { t } = useTranslation();
    return (
        <div className="flex flex-col gap-6 p-6 max-w-5xl w-full">
            <div>
                <h1 className="text-xl font-bold text-white">{t("wallets.title")}</h1>
                <p className="text-sm text-white/40 mt-1">{t("wallets.subtitle")}</p>
            </div>
            <WalletPanel />
        </div>
    );
};
