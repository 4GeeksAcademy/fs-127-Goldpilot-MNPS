import React from 'react';

interface GlassInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  icon?: React.ReactNode;
}

export function GlassInput({ label, icon, className = '', ...props }: GlassInputProps) {
  return (
    <div className="flex flex-col gap-2">
      {label && (
        <label className="text-sm text-[#2c2117] font-semibold">
          {label}
        </label>
      )}
      <div className="relative">
        {icon && (
          <div className="absolute left-4 top-1/2 -translate-y-1/2 text-[#564535]">
            {icon}
          </div>
        )}
        <input
          className={`
            w-full
            px-4 py-3
            ${icon ? 'pl-12' : ''}
            bg-[var(--glass-white)]
            backdrop-blur-[var(--blur-md)]
            border border-white/40
            rounded-[var(--radius-liquid-md)]
            shadow-[var(--shadow-glass-sm)]
            text-[#2c2117]
            placeholder:text-[#564535]/70
            focus:outline-none
            focus:border-[#c38f37]/60
            focus:shadow-[var(--shadow-glass-md)]
            transition-all
            duration-300
            ${className}
          `}
          {...props}
        />
      </div>
    </div>
  );
}

interface GlassTextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
}

export function GlassTextarea({ label, className = '', ...props }: GlassTextareaProps) {
  return (
    <div className="flex flex-col gap-2">
      {label && (
        <label className="text-sm text-[#2c2117] font-semibold">
          {label}
        </label>
      )}
      <textarea
        className={`
          w-full
          px-4 py-3
          bg-[var(--glass-white)]
          backdrop-blur-[var(--blur-md)]
          border border-white/40
          rounded-[var(--radius-liquid-md)]
          shadow-[var(--shadow-glass-sm)]
          text-[#2c2117]
          placeholder:text-[#564535]/70
          focus:outline-none
          focus:border-[#c38f37]/60
          focus:shadow-[var(--shadow-glass-md)]
          transition-all
          duration-300
          resize-none
          ${className}
        `}
        {...props}
      />
    </div>
  );
}