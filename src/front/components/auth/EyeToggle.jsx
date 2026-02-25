import { Eye, EyeOff } from "lucide-react";

const EyeToggle = ({ show, onToggle }) => (
    <button type="button" onClick={onToggle}
        className="absolute right-4 top-1/2 -translate-y-1/2 text-white/30 hover:text-white/60 transition-colors">
        {show ? <EyeOff size={15} /> : <Eye size={15} />}
    </button>
);

export default EyeToggle;
