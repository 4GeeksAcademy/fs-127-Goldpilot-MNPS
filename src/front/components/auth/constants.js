// ─── Country codes ─────────────────────────────────────────────────────────────
export const COUNTRY_CODES = [
    { code: "+34", flag: "🇪🇸", name: "España" },
    { code: "+1",  flag: "🇺🇸", name: "EE.UU." },
    { code: "+52", flag: "🇲🇽", name: "México" },
    { code: "+54", flag: "🇦🇷", name: "Argentina" },
    { code: "+57", flag: "🇨🇴", name: "Colombia" },
    { code: "+56", flag: "🇨🇱", name: "Chile" },
    { code: "+51", flag: "🇵🇪", name: "Perú" },
    { code: "+44", flag: "🇬🇧", name: "R. Unido" },
    { code: "+33", flag: "🇫🇷", name: "Francia" },
    { code: "+49", flag: "🇩🇪", name: "Alemania" },
    { code: "+39", flag: "🇮🇹", name: "Italia" },
    { code: "+55", flag: "🇧🇷", name: "Brasil" },
];

// ─── Password strength ─────────────────────────────────────────────────────────
export const getStrength = (pwd) => {
    if (!pwd) return 0;
    let score = 0;
    if (pwd.length >= 8) score++;
    if (/[A-Z]/.test(pwd) && /[a-z]/.test(pwd)) score++;
    if (/[0-9]/.test(pwd)) score++;
    if (/[^A-Za-z0-9]/.test(pwd)) score++;
    return score;
};

export const STRENGTH_CONFIG = {
    0: { label: "",          bar: "bg-white/10",   text: "" },
    1: { label: "Muy débil", bar: "bg-red-500",    text: "text-red-400" },
    2: { label: "Débil",     bar: "bg-orange-400", text: "text-orange-400" },
    3: { label: "Buena",     bar: "bg-yellow-400", text: "text-yellow-400" },
    4: { label: "Fuerte",    bar: "bg-green-400",  text: "text-green-400" },
};

// ─── Friendly error messages ───────────────────────────────────────────────────
const FRIENDLY_ERRORS = {
    "Ya existe un usuario con ese email":    "Este email ya está registrado. ¿Quieres iniciar sesión?",
    "Ya existe un usuario con ese username": "Este nombre de usuario ya está en uso. Prueba con otro.",
    "Credenciales invalidas":                "Email o contraseña incorrectos. Comprueba tus datos.",
    "Email no verificado. Revisa tu email para verificar tu cuenta.":
        "Aún no has verificado tu email. Busca el correo de verificación en tu bandeja de entrada.",
};

export const friendlyMessage = (raw) => FRIENDLY_ERRORS[raw] ?? raw;

// ─── Shared CSS classes ────────────────────────────────────────────────────────
export const inputBase = "w-full py-4 bg-white/5 border rounded-2xl text-white placeholder-white/30 focus:outline-none focus:bg-white/[0.07] transition-all duration-200 text-sm";
export const inputOk   = "border-white/10 focus:border-[var(--color-gold)]/60";
export const inputErr  = "border-red-500/50 focus:border-red-500/70";
export const errText   = "mt-1.5 text-xs text-red-400";
export const submitBtn = "w-full mt-1 py-4 rounded-full bg-[var(--color-gold)] text-white font-bold text-sm tracking-wide uppercase transition-all shadow-lg backdrop-blur-sm border border-white/20 hover:bg-[#d4af37] hover:shadow-[0_0_20px_var(--color-gold)] disabled:opacity-50 disabled:cursor-not-allowed";
