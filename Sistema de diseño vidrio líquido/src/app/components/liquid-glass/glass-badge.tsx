import React from 'react';

interface GlassBadgeProps {
  children: React.ReactNode;
  variant?: 'default' | 'gold' | 'olive' | 'brown' | 'dark';
  size?: 'sm' | 'md';
  className?: string;
}

export function GlassBadge({ 
  children, 
  variant = 'default',
  size = 'md',
  className = ''
}: GlassBadgeProps) {
  
  const variants = {
    default: 'bg-[var(--glass-white)] border-white/40 text-black/80',
    gold: 'bg-[var(--glass-gold)] border-[#c38f37]/50 text-white',
    olive: 'bg-[var(--glass-olive)] border-[#637742]/50 text-white',
    brown: 'bg-[var(--glass-brown)] border-[#564535]/50 text-white',
    dark: 'bg-[var(--glass-brown-dark)] border-[#2c2117]/50 text-white',
  };
  
  const sizes = {
    sm: 'px-2 py-1 text-xs',
    md: 'px-3 py-1.5 text-sm',
  };
  
  return (
    <span className={`
      inline-flex items-center
      backdrop-blur-[var(--blur-md)]
      border
      rounded-[var(--radius-liquid-full)]
      font-medium
      shadow-[var(--shadow-glass-sm)]
      ${variants[variant]}
      ${sizes[size]}
      ${className}
    `}>
      {children}
    </span>
  );
}