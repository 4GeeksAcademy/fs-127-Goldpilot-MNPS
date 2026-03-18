import { useTranslation } from "react-i18next";

export const LanguageSwitcher = () => {
    const { i18n } = useTranslation();
    const current = i18n.language;

    const toggle = (lang) => {
        i18n.changeLanguage(lang);
        localStorage.setItem("lang", lang);
    };

    return (
        <div className="flex items-center gap-1 rounded-xl border border-white/[0.08] p-1"
            style={{ background: "rgba(255,255,255,0.03)", height: "48px" }}>
            {["en", "es"].map((lang) => (
                <button
                    key={lang}
                    onClick={() => toggle(lang)}
                    className={`px-3 py-1 rounded-lg text-xs font-semibold uppercase tracking-wide transition-all duration-150 ${
                        current === lang
                            ? "text-black"
                            : "text-white/30 hover:text-white/60"
                    }`}
                    style={current === lang ? { background: "var(--gradient-gold)" } : {}}
                >
                    {lang}
                </button>
            ))}
        </div>
    );
};
