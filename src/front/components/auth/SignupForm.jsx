import { motion } from "framer-motion";
import { Mail, Lock, User, Phone, ChevronDown } from "lucide-react";
import { COUNTRY_CODES, inputBase, inputOk, inputErr, errText, submitBtn } from "./constants";
import EyeToggle from "./EyeToggle";
import PasswordStrengthBar from "./PasswordStrengthBar";

const SignupForm = ({
    form, setForm, loading, onSubmit,
    countryCode, setCountryCode,
    confirmPassword, setConfirmPassword,
    showPassword, togglePassword,
    showConfirm, toggleConfirm,
    fieldErrors, clearFieldError,
}) => {
    const passwordsMatch = confirmPassword && confirmPassword === form.password;

    return (
        <motion.form key="signup"
            initial={{ opacity: 0, x: 16 }} animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -16 }} transition={{ duration: 0.18 }}
            onSubmit={onSubmit} className="flex flex-col gap-4">

            {/* Nombre + Apellido */}
            <div className="flex gap-3">
                <div className="flex-1">
                    <div className="relative">
                        <User size={15} className="absolute left-4 top-1/2 -translate-y-1/2 text-white/35 pointer-events-none" />
                        <input type="text" placeholder="Nombre" value={form.first_name}
                            onChange={(e) => { setForm(p => ({ ...p, first_name: e.target.value })); clearFieldError("first_name"); }}
                            className={`${inputBase} ${fieldErrors.first_name ? inputErr : inputOk} pl-11 pr-4`} />
                    </div>
                    {fieldErrors.first_name && <p className={errText}>{fieldErrors.first_name}</p>}
                </div>
                <div className="flex-1">
                    <input type="text" placeholder="Apellido" value={form.last_name}
                        onChange={(e) => { setForm(p => ({ ...p, last_name: e.target.value })); clearFieldError("last_name"); }}
                        className={`${inputBase} ${fieldErrors.last_name ? inputErr : inputOk} px-4`} />
                    {fieldErrors.last_name && <p className={errText}>{fieldErrors.last_name}</p>}
                </div>
            </div>

            {/* Username */}
            <div>
                <div className="relative">
                    <span className="absolute left-4 top-1/2 -translate-y-1/2 text-white/35 text-sm font-semibold pointer-events-none">@</span>
                    <input type="text" placeholder="Nombre de usuario (mín. 3 caracteres)" value={form.username}
                        onChange={(e) => { setForm(p => ({ ...p, username: e.target.value })); clearFieldError("username"); }}
                        className={`${inputBase} ${fieldErrors.username ? inputErr : inputOk} pl-9 pr-4`} />
                </div>
                {fieldErrors.username && <p className={errText}>{fieldErrors.username}</p>}
            </div>

            {/* Email */}
            <div>
                <div className="relative">
                    <Mail size={15} className="absolute left-4 top-1/2 -translate-y-1/2 text-white/35 pointer-events-none" />
                    <input type="email" placeholder="Email" value={form.email}
                        onChange={(e) => { setForm(p => ({ ...p, email: e.target.value })); clearFieldError("email"); }}
                        className={`${inputBase} ${fieldErrors.email ? inputErr : inputOk} pl-11 pr-4`} />
                </div>
                {fieldErrors.email && <p className={errText}>{fieldErrors.email}</p>}
            </div>

            {/* Teléfono con prefijo de país */}
            <div>
                <div className="flex gap-2">
                    <div className="relative shrink-0">
                        <select value={countryCode}
                            onChange={(e) => setCountryCode(e.target.value)}
                            className="h-full py-4 pl-3 pr-7 bg-white/5 border border-white/10 rounded-2xl text-white text-sm focus:outline-none focus:border-[var(--color-gold)]/60 transition-all appearance-none cursor-pointer">
                            {COUNTRY_CODES.map((c) => (
                                <option key={c.code} value={c.code} className="bg-[#1c1c1c] text-white">
                                    {c.flag} {c.code}
                                </option>
                            ))}
                        </select>
                        <ChevronDown size={11} className="absolute right-2 top-1/2 -translate-y-1/2 text-white/40 pointer-events-none" />
                    </div>
                    <div className="relative flex-1">
                        <Phone size={15} className="absolute left-4 top-1/2 -translate-y-1/2 text-white/35 pointer-events-none" />
                        <input type="tel" placeholder="Número de teléfono" value={form.phone_number}
                            onChange={(e) => { setForm(p => ({ ...p, phone_number: e.target.value })); clearFieldError("phone_number"); }}
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
                        placeholder="Contraseña (mín. 8 caracteres)" value={form.password}
                        onChange={(e) => { setForm(p => ({ ...p, password: e.target.value })); clearFieldError("password"); }}
                        className={`${inputBase} ${fieldErrors.password ? inputErr : inputOk} pl-11 pr-12`} />
                    <EyeToggle show={showPassword} onToggle={togglePassword} />
                </div>
                <PasswordStrengthBar password={form.password} />
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
                    <EyeToggle show={showConfirm} onToggle={toggleConfirm} />
                </div>
                {fieldErrors.confirm && <p className={errText}>{fieldErrors.confirm}</p>}
                {passwordsMatch && (
                    <p className="mt-1.5 text-xs text-green-400">Las contraseñas coinciden ✓</p>
                )}
            </div>

            <button type="submit" disabled={loading} className={submitBtn}>
                {loading ? "Creando cuenta..." : "Crear Cuenta"}
            </button>
        </motion.form>
    );
};

export default SignupForm;
