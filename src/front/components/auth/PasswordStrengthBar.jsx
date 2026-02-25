import { getStrength, STRENGTH_CONFIG } from "./constants";

const PasswordStrengthBar = ({ password }) => {
    const strength = getStrength(password);
    if (!password) return null;
    return (
        <div className="mt-2 flex items-center gap-2">
            <div className="flex gap-1 flex-1">
                {[1, 2, 3, 4].map((i) => (
                    <div key={i}
                        className={`h-1 flex-1 rounded-full transition-all duration-300 ${i <= strength ? STRENGTH_CONFIG[strength].bar : "bg-white/10"}`} />
                ))}
            </div>
            <span className={`text-xs min-w-[60px] text-right ${STRENGTH_CONFIG[strength].text}`}>
                {STRENGTH_CONFIG[strength].label}
            </span>
        </div>
    );
};

export default PasswordStrengthBar;
