import { useState } from "react";
import { useLocation, Link, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { Eye, EyeOff, Mail, Lock, User, Phone, ArrowLeft, ChevronDown } from "lucide-react";
import { authServices } from "../../services/authServices";
import useGlobalReducer from "../../hooks/useGlobalReducer";

// ─── Prefijos de país ─────────────────────────────────────────────────────────
const COUNTRY_CODES = [
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

// ─── Fuerza de contraseña ─────────────────────────────────────────────────────
const getStrength = (pwd) => {
    if (!pwd) return 0;
    let score = 0;
    if (pwd.length >= 8) score++;
    if (/[A-Z]/.test(pwd) && /[a-z]/.test(pwd)) score++;
    if (/[0-9]/.test(pwd)) score++;
    if (/[^A-Za-z0-9]/.test(pwd)) score++;
    return score;
};

const STRENGTH_CONFIG = {
    0: { label: "",          bar: "bg-white/10",   text: "" },
    1: { label: "Muy débil", bar: "bg-red-500",    text: "text-red-400" },
    2: { label: "Débil",     bar: "bg-orange-400", text: "text-orange-400" },
    3: { label: "Buena",     bar: "bg-yellow-400", text: "text-yellow-400" },
    4: { label: "Fuerte",    bar: "bg-green-400",  text: "text-green-400" },
};

// ─── Mensajes de error amigables ──────────────────────────────────────────────
const FRIENDLY_ERRORS = {
    "Ya existe un usuario con ese email":    "Este email ya está registrado. ¿Quieres iniciar sesión?",
    "Ya existe un usuario con ese username": "Este nombre de usuario ya está en uso. Prueba con otro.",
    "Credenciales invalidas":                "Email o contraseña incorrectos. Comprueba tus datos.",
    "Email no verificado. Revisa tu email para verificar tu cuenta.":
        "Aún no has verificado tu email. Busca el correo de verificación en tu bandeja de entrada.",
};

const friendlyMessage = (raw) => FRIENDLY_ERRORS[raw] ?? raw;

// ─── Componente ───────────────────────────────────────────────────────────────
const SignupSignin = () => {
    const { pathname } = useLocation();
    const navigate   = useNavigate();
    const { dispatch } = useGlobalReducer();
    const isLogin = pathname === "/login";

    // Formularios
    const [loginForm,  setLoginForm]  = useState({ email: "", password: "" });
    const [signupForm, setSignupForm] = useState({
        email: "", username: "", password: "",
        first_name: "", last_name: "", phone_number: "",
    });
    const [confirmPassword, setConfirmPassword] = useState("");
    const [countryCode, setCountryCode] = useState("+34");

    // UI
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirm,  setShowConfirm]  = useState(false);
    const [fieldErrors,  setFieldErrors]  = useState({});
    const [error,   setError]   = useState("");
    const [success, setSuccess] = useState("");
    const [loading, setLoading] = useState(false);

    const strength = getStrength(signupForm.password);
    const passwordsMatch = confirmPassword && confirmPassword === signupForm.password;

    // ─── Validación local ────────────────────────────────────────────────────
    const validateSignup = () => {
        const e = {};
        if (!signupForm.first_name.trim())
            e.first_name = "Introduce tu nombre";
        if (!signupForm.last_name.trim())
            e.last_name = "Introduce tu apellido";
        if (signupForm.username.trim().length < 3)
            e.username = "El usuario necesita al menos 3 caracteres";
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(signupForm.email))
            e.email = "Introduce un email válido (ej: nombre@email.com)";
        if (!signupForm.phone_number.trim())
            e.phone_number = "Introduce tu número de teléfono";
        if (signupForm.password.length < 8)
            e.password = "La contraseña necesita al menos 8 caracteres";
        if (!confirmPassword)
            e.confirm = "Repite la contraseña para confirmarla";
        else if (signupForm.password !== confirmPassword)
            e.confirm = "Las contraseñas no coinciden, revísalas";
        return e;
    };

    // ─── Handlers ────────────────────────────────────────────────────────────
    const handleLogin = async (e) => {
        e.preventDefault();
        setError("");
        setLoading(true);
        try {
            const data = await authServices.login(loginForm);
            localStorage.setItem("token", data.access_token);
            dispatch({ type: "set_user", payload: { user: data.user, token: data.access_token } });
            navigate("/");
        } catch (err) {
            setError(friendlyMessage(err.message));
        } finally {
            setLoading(false);
        }
    };

    const handleSignup = async (e) => {
        e.preventDefault();
        setError("");
        setSuccess("");
        const errors = validateSignup();
        if (Object.keys(errors).length > 0) {
            setFieldErrors(errors);
            return;
        }
        setFieldErrors({});
        setLoading(true);
        try {
            await authServices.signup({
                ...signupForm,
                phone_number: `${countryCode}${signupForm.phone_number}`,
            });
            setSuccess("¡Cuenta creada! Revisa tu email y haz clic en el enlace de verificación para poder iniciar sesión.");
        } catch (err) {
            setError(friendlyMessage(err.message));
        } finally {
            setLoading(false);
        }
    };

    const clearFieldError = (field) =>
        setFieldErrors((p) => ({ ...p, [field]: "" }));

    // ─── Clases reutilizables ─────────────────────────────────────────────────
    const inputBase =
        "w-full py-4 bg-white/5 border rounded-2xl text-white placeholder-white/30 focus:outline-none focus:bg-white/[0.07] transition-all duration-200 text-sm";
    const inputOk  = "border-white/10 focus:border-[var(--color-gold)]/60";
    const inputErr = "border-red-500/50 focus:border-red-500/70";
    const errText  = "mt-1.5 text-xs text-red-400";

    return (
        <div className="min-h-screen bg-[var(--color-brown-dark)] flex items-center justify-center relative overflow-hidden px-4 py-10">

            {/* ── Fondo de vídeo (igual que Hero de Paola) ── */}
            <div className="absolute inset-0 z-0">
                <video autoPlay loop muted playsInline
                    className="w-full h-full object-cover scale-105 opacity-90 mix-blend-luminosity">
                    <source src="/assets/videos/hero-background.mp4" type="video/mp4" />
                </video>
                <div className="absolute inset-0 bg-[var(--color-brown-dark)] mix-blend-color z-10 opacity-60" />
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,transparent_20%,var(--color-brown-dark)_100%)] z-20 opacity-90" />
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,var(--color-gold)_0%,transparent_40%)] z-20 mix-blend-overlay opacity-20" />
            </div>

            {/* Volver */}
            <Link to="/"
                className="absolute top-6 left-6 z-50 flex items-center gap-2 text-white/40 hover:text-[var(--color-gold)] transition-colors text-sm">
                <ArrowLeft size={15} /> Volver
            </Link>

            {/* ── Card principal ── */}
            <motion.div
                initial={{ opacity: 0, scale: 0.9, y: 20 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.9, y: 20 }}
                transition={{ type: "spring", stiffness: 350, damping: 25 }}
                className="relative z-30 w-[90%] max-w-[560px] rounded-[32px] overflow-hidden flex flex-col items-center"
                style={{
                    background: "rgba(30, 30, 30, 0.75)",
                    backdropFilter: "blur(40px)",
                    WebkitBackdropFilter: "blur(40px)",
                    border: "1px solid rgba(255, 255, 255, 0.15)",
                    boxShadow: "0 40px 80px -12px rgba(0, 0, 0, 0.7)",
                }}
            >
                <div className="absolute top-0 inset-x-0 h-40 bg-[var(--color-gold)] opacity-20 blur-3xl pointer-events-none" />

                <div className="relative z-20 w-full p-10 flex flex-col gap-7">

                    {/* Logo */}
                    <div className="flex items-center justify-center gap-2">
                        <div className="w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-bold text-black"
                            style={{ background: "var(--gradient-gold)" }}>XS</div>
                        <span className="font-bold tracking-tight text-white text-lg">XSNIPER</span>
                    </div>

                    {/* Tabs */}
                    <div className="w-full flex flex-col gap-3">
                        <Link to="/login" className="w-full">
                            <button className={`w-full py-4 rounded-full font-bold text-sm tracking-wide transition-all uppercase ${
                                isLogin
                                    ? "bg-[var(--color-gold)] text-white shadow-lg backdrop-blur-sm border border-white/20 hover:bg-[#d4af37] hover:shadow-[0_0_20px_var(--color-gold)]"
                                    : "bg-white/5 text-white border border-white/10 hover:bg-white/10 hover:border-white/30 backdrop-blur-md"
                            }`}>Iniciar Sesión</button>
                        </Link>
                        <Link to="/signup" className="w-full">
                            <button className={`w-full py-4 rounded-full font-bold text-sm tracking-wide transition-all uppercase ${
                                !isLogin
                                    ? "bg-[var(--color-gold)] text-white shadow-lg backdrop-blur-sm border border-white/20 hover:bg-[#d4af37] hover:shadow-[0_0_20px_var(--color-gold)]"
                                    : "bg-white/5 text-white border border-white/10 hover:bg-white/10 hover:border-white/30 backdrop-blur-md"
                            }`}>Registrarse</button>
                        </Link>
                    </div>

                    <div className="w-full h-px bg-white/10" />

                    {/* Mensajes globales */}
                    <AnimatePresence>
                        {error && (
                            <motion.div key="err"
                                initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -8 }}
                                className="px-4 py-3 rounded-xl bg-red-500/15 border border-red-500/25 text-red-300 text-sm leading-snug">
                                {error}
                            </motion.div>
                        )}
                        {success && (
                            <motion.div key="ok"
                                initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -8 }}
                                className="px-4 py-3 rounded-xl bg-[var(--color-gold)]/15 border border-[var(--color-gold)]/25 text-[var(--color-gold)] text-sm leading-snug">
                                {success}
                            </motion.div>
                        )}
                    </AnimatePresence>

                    {/* ── Formularios ── */}
                    <AnimatePresence mode="wait">

                        {/* LOGIN */}
                        {isLogin && (
                            <motion.form key="login"
                                initial={{ opacity: 0, x: -16 }} animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: 16 }} transition={{ duration: 0.18 }}
                                onSubmit={handleLogin} className="flex flex-col gap-4">

                                <div className="relative">
                                    <Mail size={15} className="absolute left-4 top-1/2 -translate-y-1/2 text-white/35 pointer-events-none" />
                                    <input type="email" placeholder="Email" value={loginForm.email}
                                        onChange={(e) => setLoginForm(p => ({ ...p, email: e.target.value }))}
                                        required className={`${inputBase} ${inputOk} pl-11 pr-4`} />
                                </div>

                                <div className="relative">
                                    <Lock size={15} className="absolute left-4 top-1/2 -translate-y-1/2 text-white/35 pointer-events-none" />
                                    <input type={showPassword ? "text" : "password"}
                                        placeholder="Contraseña" value={loginForm.password}
                                        onChange={(e) => setLoginForm(p => ({ ...p, password: e.target.value }))}
                                        required className={`${inputBase} ${inputOk} pl-11 pr-12`} />
                                    <button type="button" onClick={() => setShowPassword(v => !v)}
                                        className="absolute right-4 top-1/2 -translate-y-1/2 text-white/30 hover:text-white/60 transition-colors">
                                        {showPassword ? <EyeOff size={15} /> : <Eye size={15} />}
                                    </button>
                                </div>

                                <button type="submit" disabled={loading}
                                    className="w-full mt-1 py-4 rounded-full bg-[var(--color-gold)] text-white font-bold text-sm tracking-wide uppercase transition-all shadow-lg backdrop-blur-sm border border-white/20 hover:bg-[#d4af37] hover:shadow-[0_0_20px_var(--color-gold)] disabled:opacity-50 disabled:cursor-not-allowed">
                                    {loading ? "Verificando..." : "Iniciar Sesión"}
                                </button>
                            </motion.form>
                        )}

                        {/* SIGNUP */}
                        {!isLogin && (
                            <motion.form key="signup"
                                initial={{ opacity: 0, x: 16 }} animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: -16 }} transition={{ duration: 0.18 }}
                                onSubmit={handleSignup} className="flex flex-col gap-4">

                                {/* Nombre + Apellido */}
                                <div className="flex gap-3">
                                    <div className="flex-1">
                                        <div className="relative">
                                            <User size={15} className="absolute left-4 top-1/2 -translate-y-1/2 text-white/35 pointer-events-none" />
                                            <input type="text" placeholder="Nombre" value={signupForm.first_name}
                                                onChange={(e) => { setSignupForm(p => ({ ...p, first_name: e.target.value })); clearFieldError("first_name"); }}
                                                className={`${inputBase} ${fieldErrors.first_name ? inputErr : inputOk} pl-11 pr-4`} />
                                        </div>
                                        {fieldErrors.first_name && <p className={errText}>{fieldErrors.first_name}</p>}
                                    </div>
                                    <div className="flex-1">
                                        <input type="text" placeholder="Apellido" value={signupForm.last_name}
                                            onChange={(e) => { setSignupForm(p => ({ ...p, last_name: e.target.value })); clearFieldError("last_name"); }}
                                            className={`${inputBase} ${fieldErrors.last_name ? inputErr : inputOk} px-4`} />
                                        {fieldErrors.last_name && <p className={errText}>{fieldErrors.last_name}</p>}
                                    </div>
                                </div>

                                {/* Username */}
                                <div>
                                    <div className="relative">
                                        <span className="absolute left-4 top-1/2 -translate-y-1/2 text-white/35 text-sm font-semibold pointer-events-none">@</span>
                                        <input type="text" placeholder="Nombre de usuario (mín. 3 caracteres)" value={signupForm.username}
                                            onChange={(e) => { setSignupForm(p => ({ ...p, username: e.target.value })); clearFieldError("username"); }}
                                            className={`${inputBase} ${fieldErrors.username ? inputErr : inputOk} pl-9 pr-4`} />
                                    </div>
                                    {fieldErrors.username && <p className={errText}>{fieldErrors.username}</p>}
                                </div>

                                {/* Email */}
                                <div>
                                    <div className="relative">
                                        <Mail size={15} className="absolute left-4 top-1/2 -translate-y-1/2 text-white/35 pointer-events-none" />
                                        <input type="email" placeholder="Email" value={signupForm.email}
                                            onChange={(e) => { setSignupForm(p => ({ ...p, email: e.target.value })); clearFieldError("email"); }}
                                            className={`${inputBase} ${fieldErrors.email ? inputErr : inputOk} pl-11 pr-4`} />
                                    </div>
                                    {fieldErrors.email && <p className={errText}>{fieldErrors.email}</p>}
                                </div>

                                {/* Teléfono con prefijo de país */}
                                <div>
                                    <div className="flex gap-2">
                                        {/* Selector de país */}
                                        <div className="relative shrink-0">
                                            <select value={countryCode}
                                                onChange={(e) => setCountryCode(e.target.value)}
                                                className="h-full py-4 pl-3 pr-7 bg-white/5 border border-white/10 rounded-2xl text-white text-sm focus:outline-none focus:border-[var(--color-gold)]/60 transition-all appearance-none cursor-pointer">
                                                {COUNTRY_CODES.map((c) => (
                                                    <option key={c.code} value={c.code}
                                                        className="bg-[#1c1c1c] text-white">
                                                        {c.flag} {c.code}
                                                    </option>
                                                ))}
                                            </select>
                                            <ChevronDown size={11} className="absolute right-2 top-1/2 -translate-y-1/2 text-white/40 pointer-events-none" />
                                        </div>
                                        {/* Número */}
                                        <div className="relative flex-1">
                                            <Phone size={15} className="absolute left-4 top-1/2 -translate-y-1/2 text-white/35 pointer-events-none" />
                                            <input type="tel" placeholder="Número de teléfono" value={signupForm.phone_number}
                                                onChange={(e) => { setSignupForm(p => ({ ...p, phone_number: e.target.value })); clearFieldError("phone_number"); }}
                                                className={`${inputBase} ${fieldErrors.phone_number ? inputErr : inputOk} pl-11 pr-4`} />
                                        </div>
                                    </div>
                                    {fieldErrors.phone_number && <p className={errText}>{fieldErrors.phone_number}</p>}
                                </div>

                                {/* Contraseña + termómetro */}
                                <div>
                                    <div className="relative">
                                        <Lock size={15} className="absolute left-4 top-1/2 -translate-y-1/2 text-white/35 pointer-events-none" />
                                        <input type={showPassword ? "text" : "password"}
                                            placeholder="Contraseña (mín. 8 caracteres)" value={signupForm.password}
                                            onChange={(e) => { setSignupForm(p => ({ ...p, password: e.target.value })); clearFieldError("password"); }}
                                            className={`${inputBase} ${fieldErrors.password ? inputErr : inputOk} pl-11 pr-12`} />
                                        <button type="button" onClick={() => setShowPassword(v => !v)}
                                            className="absolute right-4 top-1/2 -translate-y-1/2 text-white/30 hover:text-white/60 transition-colors">
                                            {showPassword ? <EyeOff size={15} /> : <Eye size={15} />}
                                        </button>
                                    </div>
                                    {/* Termómetro de seguridad */}
                                    {signupForm.password && (
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
                                    )}
                                    {fieldErrors.password && <p className={errText}>{fieldErrors.password}</p>}
                                </div>

                                {/* Confirmar contraseña */}
                                <div>
                                    <div className="relative">
                                        <Lock size={15} className="absolute left-4 top-1/2 -translate-y-1/2 text-white/35 pointer-events-none" />
                                        <input type={showConfirm ? "text" : "password"}
                                            placeholder="Confirmar contraseña" value={confirmPassword}
                                            onChange={(e) => { setConfirmPassword(e.target.value); clearFieldError("confirm"); }}
                                            className={`${inputBase} pl-11 pr-12 ${
                                                fieldErrors.confirm
                                                    ? inputErr
                                                    : passwordsMatch
                                                        ? "border-green-500/50 focus:border-green-500/70"
                                                        : inputOk
                                            }`} />
                                        <button type="button" onClick={() => setShowConfirm(v => !v)}
                                            className="absolute right-4 top-1/2 -translate-y-1/2 text-white/30 hover:text-white/60 transition-colors">
                                            {showConfirm ? <EyeOff size={15} /> : <Eye size={15} />}
                                        </button>
                                    </div>
                                    {fieldErrors.confirm && <p className={errText}>{fieldErrors.confirm}</p>}
                                    {passwordsMatch && (
                                        <p className="mt-1.5 text-xs text-green-400">Las contraseñas coinciden ✓</p>
                                    )}
                                </div>

                                <button type="submit" disabled={loading}
                                    className="w-full mt-1 py-4 rounded-full bg-[var(--color-gold)] text-white font-bold text-sm tracking-wide uppercase transition-all shadow-lg backdrop-blur-sm border border-white/20 hover:bg-[#d4af37] hover:shadow-[0_0_20px_var(--color-gold)] disabled:opacity-50 disabled:cursor-not-allowed">
                                    {loading ? "Creando cuenta..." : "Crear Cuenta"}
                                </button>

                            </motion.form>
                        )}
                    </AnimatePresence>

                    {/* Pie */}
                    <p className="text-center text-white/25 text-xs">
                        {isLogin ? (
                            <>¿No tienes cuenta?{" "}
                                <Link to="/signup" className="text-[var(--color-gold)] hover:underline">Regístrate</Link>
                            </>
                        ) : (
                            <>¿Ya tienes cuenta?{" "}
                                <Link to="/login" className="text-[var(--color-gold)] hover:underline">Inicia sesión</Link>
                            </>
                        )}
                    </p>

                </div>
            </motion.div>
        </div>
    );
};

export default SignupSignin;
