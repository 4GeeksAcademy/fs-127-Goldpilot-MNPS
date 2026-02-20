import { GlassCard } from './liquid-glass';

export function TypographyShowcase() {
  const fontSizes = [
    { name: '--text-xs', label: 'Extra Small', example: 'The quick brown fox jumps over the lazy dog' },
    { name: '--text-sm', label: 'Small', example: 'The quick brown fox jumps over the lazy dog' },
    { name: '--text-base', label: 'Base', example: 'The quick brown fox jumps over the lazy dog' },
    { name: '--text-lg', label: 'Large', example: 'The quick brown fox jumps over the lazy dog' },
    { name: '--text-xl', label: 'Extra Large', example: 'The quick brown fox jumps over the lazy dog' },
    { name: '--text-2xl', label: '2XL', example: 'The quick brown fox jumps' },
    { name: '--text-3xl', label: '3XL', example: 'The quick brown fox' },
    { name: '--text-4xl', label: '4XL', example: 'Quick Brown Fox' },
    { name: '--text-5xl', label: '5XL', example: 'Typography' },
  ];

  const fontWeights = [
    { name: '--font-weight-light', label: 'Light (300)' },
    { name: '--font-weight-normal', label: 'Normal (400)' },
    { name: '--font-weight-medium', label: 'Medium (500)' },
    { name: '--font-weight-semibold', label: 'Semibold (600)' },
    { name: '--font-weight-bold', label: 'Bold (700)' },
    { name: '--font-weight-extrabold', label: 'Extrabold (800)' },
  ];

  const lineHeights = [
    { name: '--leading-none', label: 'None (1)', value: '1' },
    { name: '--leading-tight', label: 'Tight (1.25)', value: '1.25' },
    { name: '--leading-snug', label: 'Snug (1.375)', value: '1.375' },
    { name: '--leading-normal', label: 'Normal (1.5)', value: '1.5' },
    { name: '--leading-relaxed', label: 'Relaxed (1.625)', value: '1.625' },
    { name: '--leading-loose', label: 'Loose (2)', value: '2' },
  ];

  return (
    <div className="space-y-6">
      {/* Font Sizes */}
      <GlassCard variant="default">
        <h3 className="text-xl font-semibold text-[#2c2117] mb-6">Tamaños de Fuente</h3>
        <div className="space-y-4">
          {fontSizes.map((size) => (
            <div key={size.name} className="border-b border-white/30 pb-4 last:border-0">
              <div className="flex items-baseline gap-4 mb-2">
                <span className="text-xs font-mono text-[#564535] w-32">{size.name}</span>
                <span className="text-sm text-[#637742]">{size.label}</span>
              </div>
              <p
                style={{ fontSize: `var(${size.name})` }}
                className="text-[#2c2117] font-medium"
              >
                {size.example}
              </p>
            </div>
          ))}
        </div>
      </GlassCard>

      {/* Font Weights */}
      <GlassCard variant="gradient-2">
        <h3 className="text-xl font-semibold text-[#2c2117] mb-6">Pesos de Fuente</h3>
        <div className="space-y-3">
          {fontWeights.map((weight) => (
            <div key={weight.name} className="flex items-center gap-4">
              <span className="text-xs font-mono text-[#564535] w-48">{weight.name}</span>
              <p
                style={{ fontWeight: `var(${weight.name})` }}
                className="text-lg text-[#2c2117]"
              >
                {weight.label} - The quick brown fox jumps over the lazy dog
              </p>
            </div>
          ))}
        </div>
      </GlassCard>

      {/* Line Heights */}
      <GlassCard variant="gradient-3">
        <h3 className="text-xl font-semibold text-[#2c2117] mb-6">Alturas de Línea</h3>
        <div className="space-y-4">
          {lineHeights.map((leading) => (
            <div key={leading.name} className="border-b border-white/30 pb-4 last:border-0">
              <div className="flex items-baseline gap-4 mb-2">
                <span className="text-xs font-mono text-[#564535] w-40">{leading.name}</span>
                <span className="text-sm text-[#637742]">{leading.label}</span>
              </div>
              <p
                style={{ lineHeight: leading.value }}
                className="text-base text-[#2c2117] max-w-2xl"
              >
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.
              </p>
            </div>
          ))}
        </div>
      </GlassCard>

      {/* Letter Spacing */}
      <GlassCard variant="gradient-4">
        <h3 className="text-xl font-semibold text-[#2c2117] mb-6">Espaciado de Letras</h3>
        <div className="space-y-3">
          <div className="flex items-center gap-4">
            <span className="text-xs font-mono text-[#564535] w-40">--tracking-tighter</span>
            <p style={{ letterSpacing: 'var(--tracking-tighter)' }} className="text-lg text-[#2c2117]">
              The quick brown fox jumps
            </p>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-xs font-mono text-[#564535] w-40">--tracking-tight</span>
            <p style={{ letterSpacing: 'var(--tracking-tight)' }} className="text-lg text-[#2c2117]">
              The quick brown fox jumps
            </p>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-xs font-mono text-[#564535] w-40">--tracking-normal</span>
            <p style={{ letterSpacing: 'var(--tracking-normal)' }} className="text-lg text-[#2c2117]">
              The quick brown fox jumps
            </p>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-xs font-mono text-[#564535] w-40">--tracking-wide</span>
            <p style={{ letterSpacing: 'var(--tracking-wide)' }} className="text-lg text-[#2c2117]">
              The quick brown fox jumps
            </p>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-xs font-mono text-[#564535] w-40">--tracking-wider</span>
            <p style={{ letterSpacing: 'var(--tracking-wider)' }} className="text-lg text-[#2c2117]">
              The quick brown fox jumps
            </p>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-xs font-mono text-[#564535] w-40">--tracking-widest</span>
            <p style={{ letterSpacing: 'var(--tracking-widest)' }} className="text-lg text-[#2c2117]">
              THE QUICK BROWN FOX
            </p>
          </div>
        </div>
      </GlassCard>

      {/* Font Families */}
      <GlassCard variant="default">
        <h3 className="text-xl font-semibold text-[#2c2117] mb-6">Familias de Fuentes</h3>
        <div className="space-y-4">
          <div>
            <span className="text-xs font-mono text-[#564535] block mb-2">--font-display</span>
            <p style={{ fontFamily: 'var(--font-display)' }} className="text-2xl text-[#2c2117] font-semibold">
              Display Font - Para títulos y encabezados principales
            </p>
          </div>
          <div>
            <span className="text-xs font-mono text-[#564535] block mb-2">--font-body</span>
            <p style={{ fontFamily: 'var(--font-body)' }} className="text-base text-[#2c2117]">
              Body Font - Para texto de cuerpo, párrafos y contenido general. Esta fuente está optimizada para legibilidad en tamaños medianos.
            </p>
          </div>
          <div>
            <span className="text-xs font-mono text-[#564535] block mb-2">--font-mono</span>
            <p style={{ fontFamily: 'var(--font-mono)' }} className="text-sm text-[#2c2117]">
              Monospace Font - Para código, variables y elementos técnicos: const variable = "value";
            </p>
          </div>
        </div>
      </GlassCard>
    </div>
  );
}
