import { useState } from "react";
import { Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { ArrowLeft } from "lucide-react";
import { authServices } from "../services/authServices";
import { inputBase, inputOk, inputErr, errText, submitBtn } from "../components/auth/constants";

const ForgotPassword = () => {
    const [email, setEmail]     = useState("");
    const [emailError, setEmailError] = useState("");
    const [error,   setError]   = useState("");
    const [success, setSuccess] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        setEmailError("");

        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            setEmailError("Introduce un email válido");
            return;
        }

        setLoading(true);
        try {
            const data = await authServices.forgotPassword({ email });
            setSuccess(data.msg || "Revisa tu email y haz clic en el enlace para restablecer tu contraseña.");
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
                        <h2 className="text-white font-bold text-xl tracking-tight">¿Olvidaste tu contraseña?</h2>
                        <p className="mt-1 text-white/35 text-sm">
                            Introduce tu email y te enviaremos un enlace para crear una nueva contraseña.
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
                            <div>
                                <input type="email" placeholder="Tu email" value={email}
                                    onChange={(e) => { setEmail(e.target.value); setEmailError(""); }}
                                    className={`${inputBase} ${emailError ? inputErr : inputOk} px-4`} />
                                {emailError && <p className={errText}>{emailError}</p>}
                            </div>

                            <button type="submit" disabled={loading} className={submitBtn}>
                                {loading ? "Enviando..." : "Enviar enlace"}
                            </button>
                        </form>
                    )}

                    {/* Pie */}
                    <p className="text-center text-white/25 text-xs">
                        ¿Recuerdas tu contraseña?{" "}
                        <Link to="/login" className="text-[var(--color-gold)] hover:underline">Inicia sesión</Link>
                    </p>

                </div>
            </motion.div>
        </div>
    );
};

export default ForgotPassword;
