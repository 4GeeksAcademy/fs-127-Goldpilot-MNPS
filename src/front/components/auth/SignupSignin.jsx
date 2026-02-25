import { useState } from "react";
import { useLocation, Link, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { ArrowLeft } from "lucide-react";
import { authServices } from "../../services/authServices";
import useGlobalReducer from "../../hooks/useGlobalReducer";
import { friendlyMessage } from "./constants";
import LoginForm from "./LoginForm";
import SignupForm from "./SignupForm";

const SignupSignin = () => {
    const { pathname } = useLocation();
    const navigate     = useNavigate();
    const { dispatch } = useGlobalReducer();
    const isLogin      = pathname === "/login";

    // Form state
    const [loginForm,  setLoginForm]  = useState({ email: "", password: "" });
    const [signupForm, setSignupForm] = useState({
        email: "", username: "", password: "",
        first_name: "", last_name: "", phone_number: "",
    });
    const [confirmPassword, setConfirmPassword] = useState("");
    const [countryCode, setCountryCode]         = useState("+34");

    // UI state
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirm,  setShowConfirm]  = useState(false);
    const [fieldErrors,  setFieldErrors]  = useState({});
    const [error,   setError]   = useState("");
    const [success, setSuccess] = useState("");
    const [loading, setLoading] = useState(false);
    const [showForm, setShowForm] = useState(true); // For animation when switching between login/signup

    // ─── Validation ───────────────────────────────────────────────────────────
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

    // ─── Handlers ─────────────────────────────────────────────────────────────
    const handleLogin = async (e) => {
        e.preventDefault();
        setError("");
        setLoading(true);
        try {
            const data = await authServices.login(loginForm);
            dispatch({ type: "set_user", payload: { user: data.user, token: data.access_token } });
            navigate("/dashboard");
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
            setShowForm(false);
        } catch (err) {
            setError(friendlyMessage(err.message));
        } finally {
            setLoading(false);
        }
    };

    const clearFieldError = (field) =>
        setFieldErrors((p) => ({ ...p, [field]: "" }));

    return (
        <div className="min-h-screen bg-[var(--color-brown-dark)] flex items-center justify-center relative overflow-hidden px-4 py-10">

            {/* Background video */}
            <div className="absolute inset-0 z-0">
                <video autoPlay loop muted playsInline
                    className="w-full h-full object-cover scale-105 opacity-90 mix-blend-luminosity">
                    <source src="/assets/videos/hero-background.mp4" type="video/mp4" />
                </video>
                <div className="absolute inset-0 bg-[var(--color-brown-dark)] mix-blend-color z-10 opacity-60" />
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,transparent_20%,var(--color-brown-dark)_100%)] z-20 opacity-90" />
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,var(--color-gold)_0%,transparent_40%)] z-20 mix-blend-overlay opacity-20" />
            </div>

            {/* Back link */}
            <Link to="/"
                className="absolute top-6 left-6 z-50 flex items-center gap-2 text-white/40 hover:text-[var(--color-gold)] transition-colors text-sm">
                <ArrowLeft size={15} /> Volver
            </Link>

            {/* Card */}
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
                    {(showForm && <div className="w-full flex flex-col gap-3">
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
                    </div>)}

                    <div className="w-full h-px bg-white/10" />

                    {/* Global messages */}
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

                    {/* Forms */}
                    <AnimatePresence mode="wait">
                        {isLogin
                            ? <LoginForm
                                form={loginForm} setForm={setLoginForm}
                                loading={loading} onSubmit={handleLogin}
                                showPassword={showPassword}
                                togglePassword={() => setShowPassword(v => !v)} />
                            : (showForm && <SignupForm
                                form={signupForm} setForm={setSignupForm}
                                loading={loading} onSubmit={handleSignup}
                                countryCode={countryCode} setCountryCode={setCountryCode}
                                confirmPassword={confirmPassword} setConfirmPassword={setConfirmPassword}
                                showPassword={showPassword} togglePassword={() => setShowPassword(v => !v)}
                                showConfirm={showConfirm}   toggleConfirm={() => setShowConfirm(v => !v)}
                                fieldErrors={fieldErrors}   clearFieldError={clearFieldError} />)
                        }
                    </AnimatePresence>

                    {/* Footer */}
                    <div className="flex flex-col items-center gap-2">
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
                        {isLogin && (
                            <p className="text-center text-white/25 text-xs">
                                ¿Quieres cambiar tu contraseña?{" "}
                                <Link to="/change-password" className="text-[var(--color-gold)] hover:underline">Cámbiala aquí</Link>
                            </p>
                        )}
                    </div>

                </div>
            </motion.div>
        </div>
    );
};

export default SignupSignin;
