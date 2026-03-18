import React from 'react';
import { motion } from 'motion/react';

interface GlassCardProps {
  children: React.ReactNode;
  variant?: 'default' | 'gradient-1' | 'gradient-2' | 'gradient-3' | 'gradient-4' | 'gradient-5';
  blur?: 'sm' | 'md' | 'lg' | 'xl';
  hover?: boolean;
  className?: string;
}

export function GlassCard({ 
  children, 
  variant = 'default',
  blur = 'md',
  hover = true,
  className = ''
}: GlassCardProps) {
  
  const blurStyles = {
    sm: 'backdrop-blur-[10px]',
    md: 'backdrop-blur-[20px]',
    lg: 'backdrop-blur-[40px]',
    xl: 'backdrop-blur-[60px]',
  };
  
  const variants = {
    default: 'bg-[var(--glass-white)] border-white/40',
    'gradient-1': 'bg-gradient-to-br from-white/90 to-white/60 border-white/40',
    'gradient-2': 'bg-gradient-to-br from-[#c38f37]/30 to-[#637742]/30 border-white/30',
    'gradient-3': 'bg-gradient-to-br from-[#637742]/30 to-[#243018]/40 border-white/30',
    'gradient-4': 'bg-gradient-to-br from-[#c38f37]/30 to-[#564535]/30 border-white/30',
    'gradient-5': 'bg-gradient-to-br from-[#564535]/30 to-[#2c2117]/40 border-white/30',
  };
  
  const baseStyles = `
    rounded-[var(--radius-liquid-lg)]
    border
    shadow-[var(--shadow-glass-lg)]
    p-6
    transition-all
    duration-300
  `;
  
  const hoverStyles = hover ? 'hover:shadow-[var(--shadow-glass-xl)] hover:scale-[1.02]' : '';
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className={`${baseStyles} ${blurStyles[blur]} ${variants[variant]} ${hoverStyles} ${className}`}
    >
      {/* Inner glow */}
      <div className="absolute inset-0 rounded-[var(--radius-liquid-lg)] bg-gradient-to-br from-white/10 to-transparent pointer-events-none" />
      <div className="relative z-10">{children}</div>
    </motion.div>
  );
}