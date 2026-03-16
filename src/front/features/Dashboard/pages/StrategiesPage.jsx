import { useTranslation } from "react-i18next";
import { StrategiesCard } from "../../../components/strategies/StrategiesCard";
import { BotControlPage } from "./BotControlPage";

export const StrategiesPage = () => {
    const { t } = useTranslation();

    return (
        <div className="flex flex-col gap-12 w-full p-4 animate-fade-in">
            <div className="pb-6 border-b border-white/[0.05]">
                <h1 className="text-3xl font-bold tracking-tight text-white">
                    {t("strategies.commandCenter").split(" ")[0]} <span className="text-[var(--color-gold)]">{t("strategies.commandCenter").split(" ")[1]}</span>
                </h1>
                <p className="text-gray-400 mt-2">
                    {t("strategies.subtitle")}
                </p>
            </div>

            <section className="space-y-6">
                <div className="flex items-center gap-3">
                    <span className="text-2xl">⎔</span>
                    <h2 className="text-xl font-semibold text-white">{t("strategies.investmentProtocols")}</h2>
                </div>
                <div className="bg-white/[0.02] rounded-[32px] p-2 border border-white/[0.05]">
                    <StrategiesCard />
                </div>
            </section>

            <section className="space-y-6 bg-gradient-to-b from-white/[0.03] to-transparent p-8 rounded-[40px] border border-white/[0.05]">
                <div className="flex items-center gap-3 mb-4">
                    <span className="text-2xl">◉</span>
                    <h2 className="text-xl font-semibold text-white">{t("strategies.executionStatus")}</h2>
                </div>
                <BotControlPage />
            </section>

            <div className="p-6 rounded-2xl bg-[var(--color-gold)]/5 border border-[var(--color-gold)]/10 text-center">
                <p className="text-xs text-[var(--color-gold)]/60 italic uppercase tracking-widest">
                    {t("strategies.selectStrategyWarning")}
                </p>
            </div>
        </div>
    );
};