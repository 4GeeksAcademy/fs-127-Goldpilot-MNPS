import React from 'react';
import { motion } from 'motion/react';

interface GlassToggleProps {
  checked: boolean;
  onChange: (checked: boolean) => void;
  label?: string;
  variant?: 'default' | 'gold' | 'olive' | 'brown';
}

export function GlassToggle({ 
  checked, 
  onChange, 
  label,
  variant = 'gold'
}: GlassToggleProps) {
  
  const variants = {
    default: 'bg-[var(--glass-white)]',
    gold: 'bg-[var(--glass-gold)]',
    olive: 'bg-[var(--glass-olive)]',
    brown: 'bg-[var(--glass-brown)]',
  };
  
  return (
    <div className="flex items-center gap-3">
      <button
        onClick={() => onChange(!checked)}
        className={`
          relative
          w-14 h-8
          rounded-[var(--radius-liquid-full)]
          border border-white/40
          backdrop-blur-[var(--blur-md)]
          shadow-[var(--shadow-glass-sm)]
          transition-all duration-300
          ${checked ? variants[variant] : 'bg-[var(--glass-white-light)]'}
        `}
      >
        <motion.div
          animate={{
            x: checked ? 24 : 2,
          }}
          transition={{ type: 'spring', damping: 20, stiffness: 300 }}
          className="
            absolute top-1 left-0
            w-6 h-6
            bg-white
            rounded-full
            shadow-[var(--shadow-glass-md)]
          "
        />
      </button>
      {label && (
        <span className="text-sm text-[#2c2117] font-medium">{label}</span>
      )}
    </div>
  );
}