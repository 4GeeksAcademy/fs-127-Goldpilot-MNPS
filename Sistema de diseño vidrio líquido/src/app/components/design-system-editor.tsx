import { useState, useEffect } from 'react';
import { GlassCard } from './liquid-glass';
import { motion } from 'motion/react';
import { ChevronDown, ChevronUp, Copy, Check } from 'lucide-react';

interface VariableSection {
  title: string;
  variables: {
    name: string;
    value: string;
    type: 'color' | 'number' | 'select' | 'text';
    options?: string[];
    unit?: string;
    min?: number;
    max?: number;
    step?: number;
  }[];
}

export function DesignSystemEditor() {
  const [expandedSections, setExpandedSections] = useState<Set<string>>(new Set(['colors']));
  const [copied, setCopied] = useState(false);
  
  const [variables, setVariables] = useState<Record<string, string>>({
    // Typography
    '--text-xs': '0.75rem',
    '--text-sm': '0.875rem',
    '--text-base': '1rem',
    '--text-lg': '1.125rem',
    '--text-xl': '1.25rem',
    '--text-2xl': '1.5rem',
    '--text-3xl': '1.875rem',
    '--text-4xl': '2.25rem',
    '--text-5xl': '3rem',
    '--font-weight-light': '300',
    '--font-weight-normal': '400',
    '--font-weight-medium': '500',
    '--font-weight-semibold': '600',
    '--font-weight-bold': '700',
    // Colors
    '--color-gold': '#c38f37',
    '--color-brown-medium': '#564535',
    '--color-brown-dark': '#2c2117',
    '--color-green-dark': '#243018',
    '--color-olive': '#637742',
    // Spacing
    '--spacing-xs': '4px',
    '--spacing-sm': '8px',
    '--spacing-md': '16px',
    '--spacing-lg': '24px',
    '--spacing-xl': '32px',
    // Radius
    '--radius-liquid-sm': '12px',
    '--radius-liquid-md': '20px',
    '--radius-liquid-lg': '28px',
    '--radius-liquid-xl': '36px',
    // Blur
    '--blur-sm': '10px',
    '--blur-md': '20px',
    '--blur-lg': '40px',
    '--blur-xl': '60px',
  });

  useEffect(() => {
    const root = document.documentElement;
    Object.entries(variables).forEach(([key, value]) => {
      root.style.setProperty(key, value);
    });
  }, [variables]);

  const sections: VariableSection[] = [
    {
      title: 'Colores de Paleta',
      variables: [
        { name: '--color-gold', value: variables['--color-gold'], type: 'color' },
        { name: '--color-brown-medium', value: variables['--color-brown-medium'], type: 'color' },
        { name: '--color-brown-dark', value: variables['--color-brown-dark'], type: 'color' },
        { name: '--color-green-dark', value: variables['--color-green-dark'], type: 'color' },
        { name: '--color-olive', value: variables['--color-olive'], type: 'color' },
      ],
    },
    {
      title: 'Tamaños de Fuente',
      variables: [
        { name: '--text-xs', value: variables['--text-xs'], type: 'text', unit: 'rem' },
        { name: '--text-sm', value: variables['--text-sm'], type: 'text', unit: 'rem' },
        { name: '--text-base', value: variables['--text-base'], type: 'text', unit: 'rem' },
        { name: '--text-lg', value: variables['--text-lg'], type: 'text', unit: 'rem' },
        { name: '--text-xl', value: variables['--text-xl'], type: 'text', unit: 'rem' },
        { name: '--text-2xl', value: variables['--text-2xl'], type: 'text', unit: 'rem' },
        { name: '--text-3xl', value: variables['--text-3xl'], type: 'text', unit: 'rem' },
        { name: '--text-4xl', value: variables['--text-4xl'], type: 'text', unit: 'rem' },
        { name: '--text-5xl', value: variables['--text-5xl'], type: 'text', unit: 'rem' },
      ],
    },
    {
      title: 'Pesos de Fuente',
      variables: [
        { name: '--font-weight-light', value: variables['--font-weight-light'], type: 'number', min: 100, max: 900, step: 100 },
        { name: '--font-weight-normal', value: variables['--font-weight-normal'], type: 'number', min: 100, max: 900, step: 100 },
        { name: '--font-weight-medium', value: variables['--font-weight-medium'], type: 'number', min: 100, max: 900, step: 100 },
        { name: '--font-weight-semibold', value: variables['--font-weight-semibold'], type: 'number', min: 100, max: 900, step: 100 },
        { name: '--font-weight-bold', value: variables['--font-weight-bold'], type: 'number', min: 100, max: 900, step: 100 },
      ],
    },
    {
      title: 'Espaciado',
      variables: [
        { name: '--spacing-xs', value: variables['--spacing-xs'], type: 'text', unit: 'px' },
        { name: '--spacing-sm', value: variables['--spacing-sm'], type: 'text', unit: 'px' },
        { name: '--spacing-md', value: variables['--spacing-md'], type: 'text', unit: 'px' },
        { name: '--spacing-lg', value: variables['--spacing-lg'], type: 'text', unit: 'px' },
        { name: '--spacing-xl', value: variables['--spacing-xl'], type: 'text', unit: 'px' },
      ],
    },
    {
      title: 'Border Radius',
      variables: [
        { name: '--radius-liquid-sm', value: variables['--radius-liquid-sm'], type: 'text', unit: 'px' },
        { name: '--radius-liquid-md', value: variables['--radius-liquid-md'], type: 'text', unit: 'px' },
        { name: '--radius-liquid-lg', value: variables['--radius-liquid-lg'], type: 'text', unit: 'px' },
        { name: '--radius-liquid-xl', value: variables['--radius-liquid-xl'], type: 'text', unit: 'px' },
      ],
    },
    {
      title: 'Blur',
      variables: [
        { name: '--blur-sm', value: variables['--blur-sm'], type: 'text', unit: 'px' },
        { name: '--blur-md', value: variables['--blur-md'], type: 'text', unit: 'px' },
        { name: '--blur-lg', value: variables['--blur-lg'], type: 'text', unit: 'px' },
        { name: '--blur-xl', value: variables['--blur-xl'], type: 'text', unit: 'px' },
      ],
    },
  ];

  const toggleSection = (title: string) => {
    setExpandedSections((prev) => {
      const next = new Set(prev);
      if (next.has(title)) {
        next.delete(title);
      } else {
        next.add(title);
      }
      return next;
    });
  };

  const handleVariableChange = (name: string, value: string) => {
    setVariables((prev) => ({ ...prev, [name]: value }));
  };

  const exportCSS = () => {
    const css = `:root {\n${Object.entries(variables)
      .map(([key, value]) => `  ${key}: ${value};`)
      .join('\n')}\n}`;
    
    navigator.clipboard.writeText(css);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-4">
      {/* Export Button */}
      <div className="flex justify-end">
        <button
          onClick={exportCSS}
          className="
            px-4 py-2
            bg-[var(--glass-gold-light)]
            backdrop-blur-md
            border border-[#c38f37]/40
            rounded-[var(--radius-liquid-md)]
            text-white text-sm font-medium
            shadow-[var(--shadow-glass-md)]
            hover:bg-[var(--glass-gold)]
            transition-all duration-300
            flex items-center gap-2
          "
        >
          {copied ? (
            <>
              <Check className="w-4 h-4" />
              ¡Copiado!
            </>
          ) : (
            <>
              <Copy className="w-4 h-4" />
              Exportar CSS
            </>
          )}
        </button>
      </div>

      {/* Sections */}
      {sections.map((section) => (
        <GlassCard key={section.title} variant="default" hover={false}>
          <button
            onClick={() => toggleSection(section.title)}
            className="w-full flex items-center justify-between mb-4"
          >
            <h4 className="text-lg font-semibold text-[#2c2117]">{section.title}</h4>
            <motion.div
              animate={{ rotate: expandedSections.has(section.title) ? 180 : 0 }}
              transition={{ duration: 0.3 }}
            >
              <ChevronDown className="w-5 h-5 text-[#2c2117]" />
            </motion.div>
          </button>

          {expandedSections.has(section.title) && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="space-y-3"
            >
              {section.variables.map((variable) => (
                <div key={variable.name} className="flex items-center gap-4">
                  <label className="flex-1 text-sm font-mono text-[#2c2117] min-w-[200px]">
                    {variable.name}
                  </label>
                  
                  {variable.type === 'color' && (
                    <div className="flex items-center gap-2">
                      <input
                        type="color"
                        value={variable.value}
                        onChange={(e) => handleVariableChange(variable.name, e.target.value)}
                        className="
                          w-12 h-10
                          rounded-[var(--radius-liquid-sm)]
                          border border-white/40
                          cursor-pointer
                        "
                      />
                      <input
                        type="text"
                        value={variable.value}
                        onChange={(e) => handleVariableChange(variable.name, e.target.value)}
                        className="
                          px-3 py-2
                          w-32
                          bg-white/50
                          backdrop-blur-sm
                          border border-white/40
                          rounded-[var(--radius-liquid-sm)]
                          text-sm font-mono text-[#2c2117]
                          focus:outline-none
                          focus:border-[#c38f37]/60
                        "
                      />
                    </div>
                  )}

                  {variable.type === 'number' && (
                    <input
                      type="range"
                      value={parseInt(variable.value)}
                      onChange={(e) => handleVariableChange(variable.name, e.target.value)}
                      min={variable.min}
                      max={variable.max}
                      step={variable.step}
                      className="flex-1 max-w-xs"
                    />
                  )}

                  {variable.type === 'text' && (
                    <input
                      type="text"
                      value={variable.value}
                      onChange={(e) => handleVariableChange(variable.name, e.target.value)}
                      className="
                        px-3 py-2
                        w-32
                        bg-white/50
                        backdrop-blur-sm
                        border border-white/40
                        rounded-[var(--radius-liquid-sm)]
                        text-sm font-mono text-[#2c2117]
                        focus:outline-none
                        focus:border-[#c38f37]/60
                      "
                    />
                  )}
                  
                  {variable.type === 'number' && (
                    <span className="text-sm font-mono text-[#564535] w-12 text-right">
                      {variable.value}
                    </span>
                  )}
                </div>
              ))}
            </motion.div>
          )}
        </GlassCard>
      ))}
    </div>
  );
}