import React from 'react';
import { motion } from 'motion/react';

interface GlassNavbarProps {
  logo?: React.ReactNode;
  children?: React.ReactNode;
  rightContent?: React.ReactNode;
}

export function GlassNavbar({ logo, children, rightContent }: GlassNavbarProps) {
  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="
        fixed top-4 left-4 right-4
        z-50
        px-6 py-4
        bg-[var(--glass-white)]
        backdrop-blur-[var(--blur-lg)]
        border border-white/40
        rounded-[var(--radius-liquid-lg)]
        shadow-[var(--shadow-glass-lg)]
      "
    >
      <div className="flex items-center justify-between">
        {/* Logo */}
        {logo && (
          <div className="flex items-center gap-3">
            {logo}
          </div>
        )}
        
        {/* Navigation Items */}
        {children && (
          <div className="flex items-center gap-2">
            {children}
          </div>
        )}
        
        {/* Right Content */}
        {rightContent && (
          <div className="flex items-center gap-3">
            {rightContent}
          </div>
        )}
      </div>
    </motion.nav>
  );
}

interface GlassNavItemProps {
  children: React.ReactNode;
  active?: boolean;
  onClick?: () => void;
}

export function GlassNavItem({ children, active, onClick }: GlassNavItemProps) {
  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={onClick}
      className={`
        px-4 py-2
        rounded-[var(--radius-liquid-sm)]
        text-sm font-medium
        transition-all duration-300
        ${active 
          ? 'bg-white/70 text-[#2c2117] shadow-[var(--shadow-glass-sm)]' 
          : 'text-[#564535] hover:bg-white/50 hover:text-[#2c2117]'
        }
      `}
    >
      {children}
    </motion.button>
  );
}