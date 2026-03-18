import React from 'react';
import { motion } from 'motion/react';

interface GlassButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'gold' | 'olive' | 'brown' | 'dark' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  glow?: boolean;
}

export function GlassButton({ 
  variant = 'primary', 
  size = 'md', 
  children, 
  glow = false,
  className = '',
  ...props 
}: GlassButtonProps) {
  
  const baseStyles = `
    relative overflow-hidden border backdrop-blur-md
    transition-all duration-300 font-medium
    active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed
  `;
  
  const variants = {
    primary: `
      bg-[var(--glass-white)] border-white/40 text-black/90
      hover:bg-white/80 hover:border-white/60
      shadow-[var(--shadow-glass-md)]
    `,
    secondary: `
      bg-[var(--glass-black-light)] border-white/30 text-white
      hover:bg-black/50 hover:border-white/40
      shadow-[var(--shadow-glass-md)]
    `,
    gold: `
      bg-[var(--glass-gold)] border-[#c38f37]/50 text-white
      hover:bg-[#c38f37] hover:border-[#c38f37]/70
      shadow-[var(--shadow-glass-md)]
      ${glow ? 'shadow-[var(--glow-gold)]' : ''}
    `,
    olive: `
      bg-[var(--glass-olive)] border-[#637742]/50 text-white
      hover:bg-[#637742] hover:border-[#637742]/70
      shadow-[var(--shadow-glass-md)]
      ${glow ? 'shadow-[var(--glow-olive)]' : ''}
    `,
    brown: `
      bg-[var(--glass-brown)] border-[#564535]/50 text-white
      hover:bg-[#564535] hover:border-[#564535]/70
      shadow-[var(--shadow-glass-md)]
      ${glow ? 'shadow-[var(--glow-brown)]' : ''}
    `,
    dark: `
      bg-[var(--glass-brown-dark)] border-[#2c2117]/50 text-white
      hover:bg-[#2c2117] hover:border-[#2c2117]/70
      shadow-[var(--shadow-glass-md)]
    `,
    outline: `
      bg-black/20 border-white/50 text-white
      hover:bg-black/30 hover:border-white/70
      shadow-[var(--shadow-glass-sm)]
    `,
  };
  
  const sizes = {
    sm: 'px-4 py-2 text-sm rounded-[var(--radius-liquid-sm)]',
    md: 'px-6 py-3 text-base rounded-[var(--radius-liquid-md)]',
    lg: 'px-8 py-4 text-lg rounded-[var(--radius-liquid-lg)]',
  };
  
  return (
    <motion.button
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`}
      {...props}
    >
      {/* Glass shine effect */}
      <span className="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent opacity-0 hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
      <span className="relative z-10">{children}</span>
    </motion.button>
  );
}