import { useEffect, useState, useRef } from "react";
import { useSearchParams, Link } from "react-router-dom";
import { motion } from "framer-motion";
import { CheckCircle, XCircle, Loader } from "lucide-react";
import { authServices } from "../services/authServices";

const ConfirmPasswordChange = () => {
    const [searchParams] = useSearchParams();
    const token = searchParams.get("token");

    const [status,  setStatus]  = useState("loading"); // loading | success | error
    const [message, setMessage] = useState("");
    const called = useRef(false);

    useEffect(() => {
        if (called.current) return;
        called.current = true;

        if (!token) {
            setStatus("error");
            setMessage("El enlace no es válido. Asegúrate de usar el enlace completo del email.");
            return;
        }

        authServices.confirmPasswordChange(token)
            .then((data) => {
                setStatus("success");
                setMessage(data.msg || "Contraseña actualizada correctamente.");
            })
            .catch((err) => {
                setStatus("error");
                setMessage(err.message || "El enlace no es válido o ya ha sido usado.");
            });
    }, [token]);

    return (
        <div className="min-h-screen bg-[var(--color-brown-dark)] flex items-center justify-center relative overflow-hidden px-4">

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

            {/* Card */}
            <motion.div
                initial={{ opacity: 0, scale: 0.9, y: 20 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                transition={{ type: "spring", stiffness: 350, damping: 25 }}
                className="relative z-30 w-[90%] max-w-md rounded-[32px] overflow-hidden"
                style={{
                    background: "rgba(30, 30, 30, 0.75)",
                    backdropFilter: "blur(40px)",
                    WebkitBackdropFilter: "blur(40px)",
                    border: "1px solid rgba(255, 255, 255, 0.15)",
                    boxShadow: "0 40px 80px -12px rgba(0, 0, 0, 0.7)",
                }}
            >
                <div className="absolute top-0 inset-x-0 h-32 bg-[var(--color-gold)] opacity-20 blur-3xl pointer-events-none" />

                <div className="relative z-20 p-10 flex flex-col items-center gap-6 text-center">

                    {/* Logo */}
                    <div className="flex items-center gap-2">
                        <div className="w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-bold text-black"
                            style={{ background: "var(--gradient-gold)" }}>XS</div>
                        <span className="font-bold tracking-tight text-white text-lg">XSNIPER</span>
                    </div>

                    {/* Icono de estado */}
                    <div className="mt-2">
                        {status === "loading" && (
                            <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1, ease: "linear" }}>
                                <Loader size={52} className="text-[var(--color-gold)] opacity-80" />
                            </motion.div>
                        )}
                        {status === "success" && (
                            <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ type: "spring", stiffness: 300 }}>
                                <CheckCircle size={52} className="text-green-400" />
                            </motion.div>
                        )}
                        {status === "error" && (
                            <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ type: "spring", stiffness: 300 }}>
                                <XCircle size={52} className="text-red-400" />
                            </motion.div>
                        )}
                    </div>

                    {/* Título */}
                    <h2 className="text-white font-bold text-xl tracking-tight">
                        {status === "loading" && "Confirmando cambio..."}
                        {status === "success" && "¡Contraseña actualizada!"}
                        {status === "error"   && "Enlace no válido"}
                    </h2>

                    {/* Mensaje */}
                    {message && (
                        <p className={`text-sm leading-relaxed ${
                            status === "success" ? "text-white/60" : "text-red-300"
                        }`}>
                            {message}
                        </p>
                    )}

                    {/* Botón acción */}
                    {status !== "loading" && (
                        <Link to="/login" className="w-full">
                            <button className="w-full py-4 rounded-full bg-[var(--color-gold)] text-white font-bold text-sm tracking-wide uppercase transition-all shadow-lg backdrop-blur-sm border border-white/20 hover:bg-[#d4af37] hover:shadow-[0_0_20px_var(--color-gold)]">
                                {status === "success" ? "Iniciar sesión" : "Volver al inicio"}
                            </button>
                        </Link>
                    )}

                </div>
            </motion.div>
        </div>
    );
};

export default ConfirmPasswordChange;
