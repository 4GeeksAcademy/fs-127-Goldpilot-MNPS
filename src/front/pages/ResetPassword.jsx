import { useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { ArrowLeft } from "lucide-react";
import { authServices } from "../services/authServices";
import EyeToggle from "../components/auth/EyeToggle";
import PasswordStrengthBar from "../components/auth/PasswordStrengthBar";
import { inputBase, inputOk, inputErr, errText, submitBtn } from "../components/auth/constants";

const validate = (newPassword, confirmPassword) => {
    const e = {};
    if (newPassword.length < 8)
        e.new_password = "La contraseña necesita al menos 8 caracteres";
    if (!confirmPassword)
        e.confirm = "Repite la contraseña para confirmarla";
    else if (newPassword !== confirmPassword)
        e.confirm = "Las contraseñas no coinciden, revísalas";
    return e;
};

const ResetPassword = () => {
    const [searchParams] = useSearchParams();
    const token = searchParams.get("token");

    const [newPassword,     setNewPassword]     = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [showNew,     setShowNew]     = useState(false);
    const [showConfirm, setShowConfirm] = useState(false);
    const [fieldErrors, setFieldErrors] = useState({});
    const [error,   setError]   = useState("");
    const [success, setSuccess] = useState("");
    const [loading, setLoading] = useState(false);

    const passwordsMatch = confirmPassword && confirmPassword === newPassword;

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");

        if (!token) {
            setError("El enlace no es válido. Asegúrate de usar el enlace completo del email.");
            return;
        }

        const errors = validate(newPassword, confirmPassword);
        if (Object.keys(errors).length > 0) {
            setFieldErrors(errors);
            return;
        }
        setFieldErrors({});
        setLoading(true);
        try {
            const data = await authServices.resetPassword({ token, new_password: newPassword });
            setSuccess(data.msg || "Contraseña actualizada correctamente. Ya puedes iniciar sesión.");
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-[var(--color-brown-dark)] flex items-center justify-center relative overflow-hidden px-4 py-10">

            {/* Fondo vídeo */}
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
            <Link to="/login"
                className="absolute top-6 left-6 z-50 flex items-center gap-2 text-white/40 hover:text-[var(--color-gold)] transition-colors text-sm">
                <ArrowLeft size={15} /> Volver
            </Link>

            {/* Card */}
            <motion.div
                initial={{ opacity: 0, scale: 0.9, y: 20 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.9, y: 20 }}
                transition={{ type: "spring", stiffness: 350, damping: 25 }}
                className="relative z-30 w-[90%] max-w-[480px] rounded-[32px] overflow-hidden flex flex-col items-center"
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

                    {/* Título */}
                    <div className="text-center">
                        <h2 className="text-white font-bold text-xl tracking-tight">Nueva contraseña</h2>
                        <p className="mt-1 text-white/35 text-sm">
                            Elige una contraseña segura para tu cuenta.
                        </p>
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

                    {/* Formulario */}
                    {!success && (
                        <form onSubmit={handleSubmit} className="flex flex-col gap-4">

                            {/* Nueva contraseña */}
                            <div>
                                <div className="relative">
                                    <input type={showNew ? "text" : "password"}
                                        placeholder="Nueva contraseña (mín. 8 caracteres)" value={newPassword}
                                        onChange={(e) => { setNewPassword(e.target.value); setFieldErrors(p => ({ ...p, new_password: "" })); }}
                                        className={`${inputBase} ${fieldErrors.new_password ? inputErr : inputOk} pl-4 pr-12`} />
                                    <EyeToggle show={showNew} onToggle={() => setShowNew(v => !v)} />
                                </div>
                                <PasswordStrengthBar password={newPassword} />
                                {fieldErrors.new_password && <p className={errText}>{fieldErrors.new_password}</p>}
                            </div>

                            {/* Confirmar contraseña */}
                            <div>
                                <div className="relative">
                                    <input type={showConfirm ? "text" : "password"}
                                        placeholder="Confirmar contraseña" value={confirmPassword}
                                        onChange={(e) => { setConfirmPassword(e.target.value); setFieldErrors(p => ({ ...p, confirm: "" })); }}
                                        className={`${inputBase} pl-4 pr-12 ${
                                            fieldErrors.confirm
                                                ? inputErr
                                                : passwordsMatch
                                                    ? "border-green-500/50 focus:border-green-500/70"
                                                    : inputOk
                                        }`} />
                                    <EyeToggle show={showConfirm} onToggle={() => setShowConfirm(v => !v)} />
                                </div>
                                {fieldErrors.confirm && <p className={errText}>{fieldErrors.confirm}</p>}
                                {passwordsMatch && (
                                    <p className="mt-1.5 text-xs text-green-400">Las contraseñas coinciden ✓</p>
                                )}
                            </div>

                            <button type="submit" disabled={loading} className={submitBtn}>
                                {loading ? "Guardando..." : "Guardar nueva contraseña"}
                            </button>
                        </form>
                    )}

                    {/* Pie */}
                    {success && (
                        <Link to="/login" className={submitBtn + " text-center"}>
                            Iniciar sesión
                        </Link>
                    )}

                    {!success && (
                        <p className="text-center text-white/25 text-xs">
                            ¿Recuerdas tu contraseña?{" "}
                            <Link to="/login" className="text-[var(--color-gold)] hover:underline">Inicia sesión</Link>
                        </p>
                    )}

                </div>
            </motion.div>
        </div>
    );
};

export default ResetPassword;
