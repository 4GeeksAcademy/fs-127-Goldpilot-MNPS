import React from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { X } from 'lucide-react';
import { GlassButton } from './glass-button';

interface GlassModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
}

export function GlassModal({ isOpen, onClose, title, children, footer }: GlassModalProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/40 backdrop-blur-sm z-[100]"
          />
          
          {/* Modal */}
          <div className="fixed inset-0 flex items-center justify-center z-[101] p-4">
            <motion.div
              initial={{ opacity: 0, scale: 0.9, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.9, y: 20 }}
              transition={{ type: 'spring', damping: 25, stiffness: 300 }}
              className="
                w-full max-w-md
                bg-[var(--glass-white)]
                backdrop-blur-[var(--blur-xl)]
                border border-white/40
                rounded-[var(--radius-liquid-xl)]
                shadow-[var(--shadow-glass-xl)]
                overflow-hidden
              "
              onClick={(e) => e.stopPropagation()}
            >
              {/* Header */}
              {title && (
                <div className="px-6 py-4 border-b border-white/30 flex items-center justify-between">
                  <h3 className="text-xl font-semibold text-[#2c2117]">{title}</h3>
                  <button
                    onClick={onClose}
                    className="
                      p-2 rounded-full
                      hover:bg-white/50
                      transition-colors
                      text-[#564535] hover:text-[#2c2117]
                    "
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>
              )}
              
              {/* Content */}
              <div className="px-6 py-4 text-[#2c2117]">
                {children}
              </div>
              
              {/* Footer */}
              {footer && (
                <div className="px-6 py-4 border-t border-white/30 flex gap-3 justify-end">
                  {footer}
                </div>
              )}
            </motion.div>
          </div>
        </>
      )}
    </AnimatePresence>
  );
}