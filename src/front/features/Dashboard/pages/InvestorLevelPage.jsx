import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { getTradeHistory, getDashboardSummary } from "../api";

const LEVELS = [
    {
        id: "base",
        karats: null,
        minGains: 0,
        color: "#9ca3af",
        glow: "rgba(156,163,175,0.2)",
        gradient: "linear-gradient(135deg, #6b7280, #9ca3af)",
        badge: "⬡",
        reward: "/9k.png",
        imgScale: 1,
    },
    {
        id: "k14",
        karats: 14,
        minGains: 5000,
        color: "#d4a843",
        glow: "rgba(212,168,67,0.3)",
        gradient: "linear-gradient(135deg, #a07428, #d4a843, #f0c96a)",
        badge: "◈",
        reward: "/14k.png",
        imgScale: 1,
    },
    {
        id: "k18",
        karats: 18,
        minGains: 20000,
        color: "#c38f37",
        glow: "rgba(195,143,55,0.4)",
        gradient: "linear-gradient(135deg, #8b6214, #c38f37, #e8b84b)",
        badge: "✦",
        reward: "/18k.png",
        imgScale: 1.25,
    },
    {
        id: "k24",
        karats: 24,
        minGains: 50000,
        color: "#ffd700",
        glow: "rgba(255,215,0,0.45)",
        gradient: "linear-gradient(135deg, #b8860b, #ffd700, #fffacd)",
        badge: "★",
        reward: "/24k.png",
        imgScale: 1.25,
    },
];

const getCurrentLevel = (g) => [...LEVELS].reverse().find((l) => g >= l.minGains) ?? LEVELS[0];
const getNextLevel = (cur) => { const i = LEVELS.findIndex((l) => l.id === cur.id); return i < LEVELS.length - 1 ? LEVELS[i + 1] : null; };
const getProgress = (g, cur, next) => next ? Math.min(100, ((g - cur.minGains) / (next.minGains - cur.minGains)) * 100) : 100;
const fmtMoney = (n) => new Intl.NumberFormat("es-ES", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(n);

export const InvestorLevelPage = () => {
    const { t } = useTranslation();
    const [totalGains, setTotalGains] = useState(0);
    const [loading, setLoading] = useState(true);
    const [zoomedReward, setZoomedReward] = useState(null);

    useEffect(() => {
        Promise.allSettled([getTradeHistory(), getDashboardSummary()]).then(([history, summary]) => {
            let gains = 0;
            if (history.status === "fulfilled") {
                const trades = Array.isArray(history.value) ? history.value : history.value?.trades ?? [];
                gains = trades.reduce((acc, tr) => { const p = parseFloat(tr.profit_loss ?? tr.profit ?? tr.gain ?? 0); return p > 0 ? acc + p : acc; }, 0);
            }
            if (gains === 0 && summary.status === "fulfilled") {
                const s = summary.value;
                gains = parseFloat(s?.total_profit ?? s?.profit ?? s?.gains ?? 0);
            }
            setTotalGains(Math.max(0, gains));
        }).finally(() => setLoading(false));
    }, []);

    const current = getCurrentLevel(totalGains);
    const next = getNextLevel(current);
    const progress = getProgress(totalGains, current, next);

    const HOW_IT_WORKS = [0, 1, 2, 3].map((i) => ({
        title: t(`investorLevel.howItWorks_${i}_title`),
        text: t(`investorLevel.howItWorks_${i}_text`),
    }));

    if (loading) {
        return (
            <div className="flex items-center justify-center h-full">
                <div className="w-8 h-8 rounded-full border-2 border-t-transparent animate-spin"
                    style={{ borderColor: "var(--color-gold)", borderTopColor: "transparent" }} />
            </div>
        );
    }

    return (
        <div className="flex flex-col gap-5 w-full">

            <div className="flex gap-5">

                <div
                    className="flex flex-col items-center p-7 rounded-2xl border border-white/[0.08] flex-1 gap-4"
                    style={{
                        background: "rgba(20,28,14,0.7)",
                        boxShadow: `0 0 60px ${current.glow}`,
                    }}
                >
                    <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-white/35 self-start">{t("investorLevel.currentLevel")}</p>
                    <img
                        src={current.reward}
                        alt={t(`investorLevel.level_${current.id}_label`)}
                        style={{
                            width: 220,
                            height: 220,
                            objectFit: "contain",
                            transform: `scale(${current.imgScale ?? 1})`,
                            filter: `drop-shadow(0 0 32px ${current.glow}) drop-shadow(0 0 60px ${current.glow})`,
                            display: "block",
                        }}
                    />

                    <div className="flex flex-col items-center gap-1 text-center">
                        <h1 className="text-3xl font-black text-white leading-none">{t(`investorLevel.level_${current.id}_name`)}</h1>
                        <p className="text-lg font-bold" style={{ color: current.color }}>{t(`investorLevel.level_${current.id}_label`)}</p>
                        <p className="text-sm text-white/40 mt-1">{t(`investorLevel.level_${current.id}_tagline`)}</p>
                    </div>

                    <div className="w-full mt-2">
                        <div className="flex items-end justify-between mb-3">
                            <div>
                                <p className="text-[11px] text-white/35 uppercase tracking-wider">{t("investorLevel.accumulatedGains")}</p>
                                <p className="text-2xl font-black text-white mt-0.5">{fmtMoney(totalGains)}</p>
                            </div>
                            {next && (
                                <div className="text-right">
                                    <p className="text-[11px] text-white/35 uppercase tracking-wider">{t("investorLevel.nextLevel")}</p>
                                    <p className="text-sm font-bold mt-0.5" style={{ color: next.color }}>{t(`investorLevel.level_${next.id}_label`)}</p>
                                    <p className="text-xs text-white/30">{t("investorLevel.remaining")} {fmtMoney(next.minGains - totalGains)}</p>
                                </div>
                            )}
                        </div>

                        {next ? (
                            <>
                                <div className="w-full h-2 rounded-full bg-white/[0.06] overflow-hidden">
                                    <div
                                        className="h-full rounded-full transition-all duration-700"
                                        style={{ width: `${progress}%`, background: next.gradient, boxShadow: `0 0 8px ${next.glow}` }}
                                    />
                                </div>
                                <p className="text-[10px] text-white/20 mt-1.5">
                                    {t("investorLevel.dailyUpdate")} · {Math.round(progress)}{t("investorLevel.progressTowards")} {t(`investorLevel.level_${next.id}_label`)}
                                </p>
                            </>
                        ) : (
                            <div className="flex items-center gap-2 mt-2">
                                <div className="h-2 flex-1 rounded-full" style={{ background: current.gradient }} />
                                <p className="text-xs font-bold shrink-0" style={{ color: current.color }}>{t("investorLevel.maxLevel")}</p>
                            </div>
                        )}
                    </div>
                </div>

                <div
                    className="w-80 shrink-0 flex flex-col p-6 rounded-2xl border border-white/[0.06]"
                    style={{ background: "rgba(255,255,255,0.02)" }}
                >
                    <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-white/35 mb-4">{t("investorLevel.yourProgress")}</p>

                    <div className="flex flex-col flex-1 justify-between">
                        {LEVELS.map((lvl, i) => {
                            const isActive = lvl.id === current.id;
                            const isUnlocked = totalGains >= lvl.minGains;
                            const isLast = i === LEVELS.length - 1;

                            return (
                                <div key={lvl.id} className="flex flex-col">
                                    <div className="flex gap-4 items-center">
                                        <div
                                            className="shrink-0 flex items-center justify-center rounded-full border-2"
                                            style={{
                                                width: 70,
                                                height: 70,
                                                borderColor: isActive ? lvl.color : "transparent",
                                                boxShadow: isActive ? `0 0 16px ${lvl.glow}` : "none",
                                                background: "transparent",
                                            }}
                                        >
                                            <img
                                                src={lvl.reward}
                                                alt={t(`investorLevel.level_${lvl.id}_label`)}
                                                style={{
                                                    width: Math.round(58 * (lvl.imgScale ?? 1)),
                                                    height: Math.round(58 * (lvl.imgScale ?? 1)),
                                                    objectFit: "contain",
                                                    filter: isUnlocked
                                                        ? `drop-shadow(0 0 8px ${lvl.glow})`
                                                        : "grayscale(1) brightness(0.6) opacity(0.5)",
                                                    display: "block",
                                                }}
                                            />
                                        </div>

                                        <div>
                                            <p className={`text-sm font-bold leading-none ${isActive ? "text-white" : isUnlocked ? "text-white/70" : "text-white/25"}`}>
                                                {t(`investorLevel.level_${lvl.id}_name`)}
                                                {lvl.karats && <span className="ml-1 text-xs" style={{ color: isUnlocked ? lvl.color : "rgba(255,255,255,0.2)" }}>{lvl.karats}K</span>}
                                            </p>
                                            <p className="text-[11px] text-white/30 mt-0.5">
                                                {lvl.minGains > 0 ? `${t("investorLevel.from")} ${fmtMoney(lvl.minGains)}` : t("investorLevel.initialLevel")}
                                            </p>
                                            {isActive && (
                                                <span className="inline-block mt-1 text-[9px] font-black px-1.5 py-0.5 rounded" style={{ background: lvl.gradient, color: "#000" }}>
                                                    {t("investorLevel.current")}
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                    {!isLast && (
                                        <div
                                            className="w-0.5 ml-[34px] my-1"
                                            style={{ background: isUnlocked ? lvl.gradient : "rgba(255,255,255,0.06)", height: 16 }}
                                        />
                                    )}
                                </div>
                            );
                        })}
                    </div>
                </div>
            </div>

            <div
                className="shrink-0 rounded-2xl border border-white/[0.06] px-6 py-5"
                style={{ background: "rgba(255,255,255,0.02)" }}
            >
                <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-white/35 mb-4">{t("investorLevel.unlockedRewards")}</p>
                <div className="flex gap-8 justify-around">
                    {LEVELS.map((lvl) => {
                        const unlocked = totalGains >= lvl.minGains;
                        return (
                            <div key={lvl.id} className="flex flex-col items-center gap-3">
                                <div className="relative" style={{ width: 110, height: 110 }}>
                                    <img
                                        src={lvl.reward}
                                        alt={t(`investorLevel.level_${lvl.id}_label`)}
                                        onClick={() => setZoomedReward(lvl)}
                                        style={{
                                            width: 110,
                                            height: 110,
                                            objectFit: "contain",
                                            cursor: "pointer",
                                            transform: `scale(${lvl.imgScale ?? 1})`,
                                            filter: unlocked
                                                ? `drop-shadow(0 0 18px ${lvl.glow})`
                                                : "grayscale(1) brightness(0.6) opacity(0.5)",
                                            transition: "filter 0.4s, transform 0.2s",
                                            display: "block",
                                        }}
                                        className="hover:scale-105 transition-transform"
                                    />
                                </div>
                                <div className="text-center">
                                    <p className="text-xs font-bold" style={{ color: unlocked ? lvl.color : "rgba(255,255,255,0.2)" }}>
                                        {t(`investorLevel.level_${lvl.id}_label`)}
                                    </p>
                                    <p className="text-[10px] text-white/25 mt-0.5">
                                        {unlocked ? t("investorLevel.unlocked") : `${t("investorLevel.from")} ${fmtMoney(lvl.minGains)}`}
                                    </p>
                                </div>
                            </div>
                        );
                    })}
                </div>

                {zoomedReward && (
                    <div
                        className="fixed inset-0 z-[200] flex items-center justify-center"
                        style={{ background: "rgba(0,0,0,0.75)", backdropFilter: "blur(12px)" }}
                        onClick={() => setZoomedReward(null)}
                    >
                        <div className="flex flex-col items-center gap-5" onClick={(e) => e.stopPropagation()}>
                            <img
                                src={zoomedReward.reward}
                                alt={t(`investorLevel.level_${zoomedReward.id}_label`)}
                                style={{
                                    width: 300,
                                    height: 300,
                                    objectFit: "contain",
                                    filter: totalGains >= zoomedReward.minGains
                                        ? `drop-shadow(0 0 40px ${zoomedReward.glow}) drop-shadow(0 0 80px ${zoomedReward.glow})`
                                        : "grayscale(1) brightness(0.6) opacity(0.5)",
                                    display: "block",
                                }}
                            />
                            <p className="text-xl font-black" style={{ color: zoomedReward.color }}>{t(`investorLevel.level_${zoomedReward.id}_label`)}</p>
                            <p className="text-xs text-white/40">{t("investorLevel.clickToClose")}</p>
                        </div>
                    </div>
                )}
            </div>

            <div
                className="shrink-0 rounded-2xl border border-white/[0.06] px-6 py-5"
                style={{ background: "rgba(255,255,255,0.02)" }}
            >
                <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-white/35 mb-4">{t("investorLevel.howItWorks")}</p>
                <div className="grid grid-cols-4 gap-6">
                    {HOW_IT_WORKS.map(({ title, text }) => (
                        <div key={title}>
                            <p className="text-xs font-semibold text-white mb-1">{title}</p>
                            <p className="text-[11px] text-white/35 leading-relaxed">{text}</p>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};
