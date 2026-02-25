import { motion } from "framer-motion";
import { Mail, Lock } from "lucide-react";
import { inputBase, inputOk, submitBtn } from "./constants";
import EyeToggle from "./EyeToggle";

const LoginForm = ({ form, setForm, loading, onSubmit, showPassword, togglePassword }) => (
    <motion.form key="login"
        initial={{ opacity: 0, x: -16 }} animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: 16 }} transition={{ duration: 0.18 }}
        onSubmit={onSubmit} className="flex flex-col gap-4">

        <div className="relative">
            <Mail size={15} className="absolute left-4 top-1/2 -translate-y-1/2 text-white/35 pointer-events-none" />
            <input type="email" placeholder="Email" value={form.email}
                onChange={(e) => setForm(p => ({ ...p, email: e.target.value }))}
                required className={`${inputBase} ${inputOk} pl-11 pr-4`} />
        </div>

        <div className="relative">
            <Lock size={15} className="absolute left-4 top-1/2 -translate-y-1/2 text-white/35 pointer-events-none" />
            <input type={showPassword ? "text" : "password"}
                placeholder="Contraseña" value={form.password}
                onChange={(e) => setForm(p => ({ ...p, password: e.target.value }))}
                required className={`${inputBase} ${inputOk} pl-11 pr-12`} />
            <EyeToggle show={showPassword} onToggle={togglePassword} />
        </div>

        <button type="submit" disabled={loading} className={submitBtn}>
            {loading ? "Verificando..." : "Iniciar Sesión"}
        </button>
    </motion.form>
);

export default LoginForm;
