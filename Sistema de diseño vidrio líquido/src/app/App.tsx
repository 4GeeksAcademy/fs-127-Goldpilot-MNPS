import { useState } from 'react';
import { 
  GlassButton, 
  GlassCard, 
  GlassInput, 
  GlassTextarea,
  GlassNavbar,
  GlassNavItem,
  GlassModal,
  GlassTabs,
  GlassBadge,
  GlassToggle
} from './components/liquid-glass';
import { DesignSystemEditor } from './components/design-system-editor';
import { TypographyShowcase } from './components/typography-showcase';
import { 
  Sparkles, 
  Crown, 
  Leaf, 
  Coffee, 
  Send, 
  Search,
  Settings,
  User,
  Bell,
  Home,
  Layout,
  Palette,
  Package,
  Type,
  Sliders
} from 'lucide-react';

export default function App() {
  const [activeNav, setActiveNav] = useState('home');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [toggleState, setToggleState] = useState({
    notifications: true,
    darkMode: false,
    autoSave: true,
  });

  const tabs = [
    {
      id: 'components',
      label: 'Componentes',
      icon: <Layout className="w-4 h-4" />,
      content: (
        <div className="space-y-6">
          {/* Buttons Section */}
          <GlassCard variant="default">
            <h3 className="text-xl font-semibold text-[#2c2117] mb-4">Botones</h3>
            <div className="flex flex-wrap gap-3">
              <GlassButton variant="primary">Primary</GlassButton>
              <GlassButton variant="gold" glow>Gold con Glow</GlassButton>
              <GlassButton variant="olive" glow>Olive</GlassButton>
              <GlassButton variant="brown" glow>Brown</GlassButton>
              <GlassButton variant="dark">Dark</GlassButton>
              <GlassButton variant="outline">Outline</GlassButton>
            </div>
            <div className="flex flex-wrap gap-3 mt-4">
              <GlassButton variant="gold" size="sm">Small</GlassButton>
              <GlassButton variant="olive" size="md">Medium</GlassButton>
              <GlassButton variant="brown" size="lg">Large</GlassButton>
            </div>
          </GlassCard>

          {/* Badges Section */}
          <GlassCard variant="gradient-2">
            <h3 className="text-xl font-semibold text-[#2c2117] mb-4">Badges</h3>
            <div className="flex flex-wrap gap-3">
              <GlassBadge variant="default">Default</GlassBadge>
              <GlassBadge variant="gold">Premium</GlassBadge>
              <GlassBadge variant="olive">Eco</GlassBadge>
              <GlassBadge variant="brown">Natural</GlassBadge>
              <GlassBadge variant="dark">Exclusivo</GlassBadge>
            </div>
          </GlassCard>

          {/* Inputs Section */}
          <GlassCard variant="gradient-3">
            <h3 className="text-xl font-semibold text-[#2c2117] mb-4">Inputs</h3>
            <div className="space-y-4 max-w-md">
              <GlassInput 
                label="Nombre"
                placeholder="Ingresa tu nombre"
              />
              <GlassInput 
                label="Buscar"
                placeholder="Buscar..."
                icon={<Search className="w-5 h-5" />}
              />
              <GlassTextarea 
                label="Mensaje"
                placeholder="Escribe tu mensaje aquí..."
                rows={4}
              />
            </div>
          </GlassCard>
        </div>
      ),
    },
    {
      id: 'typography',
      label: 'Tipografía',
      icon: <Type className="w-4 h-4" />,
      content: <TypographyShowcase />,
    },
    {
      id: 'editor',
      label: 'Editor',
      icon: <Sliders className="w-4 h-4" />,
      content: (
        <div>
          <div className="mb-6 text-center">
            <h3 className="text-2xl font-semibold text-white mb-2">Editor de Variables</h3>
            <p className="text-white/80">Edita las variables del sistema en tiempo real</p>
          </div>
          <DesignSystemEditor />
        </div>
      ),
    },
    {
      id: 'cards',
      label: 'Tarjetas',
      icon: <Palette className="w-4 h-4" />,
      content: (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <GlassCard variant="default">
            <div className="flex items-center gap-4">
              <div className="flex-shrink-0 p-3 bg-[#c38f37]/20 rounded-[var(--radius-liquid-md)]">
                <Sparkles className="w-6 h-6 text-[#c38f37]" />
              </div>
              <div className="flex-1">
                <h4 className="font-semibold text-[#2c2117] mb-1">Default Card</h4>
                <p className="text-sm text-[#564535]">Tarjeta con efecto glassmorphism básico</p>
              </div>
            </div>
          </GlassCard>

          <GlassCard variant="gradient-2">
            <div className="flex items-center gap-4">
              <div className="flex-shrink-0 p-3 bg-white/30 backdrop-blur-sm rounded-[var(--radius-liquid-md)]">
                <Crown className="w-6 h-6 text-[#2c2117]" />
              </div>
              <div className="flex-1">
                <h4 className="font-semibold text-white mb-1">Gradient Gold</h4>
                <p className="text-sm text-white/90">Tarjeta con gradiente dorado-oliva</p>
              </div>
            </div>
          </GlassCard>

          <GlassCard variant="gradient-3">
            <div className="flex items-center gap-4">
              <div className="flex-shrink-0 p-3 bg-white/30 backdrop-blur-sm rounded-[var(--radius-liquid-md)]">
                <Leaf className="w-6 h-6 text-[#2c2117]" />
              </div>
              <div className="flex-1">
                <h4 className="font-semibold text-white mb-1">Nature Card</h4>
                <p className="text-sm text-white/90">Tarjeta con gradiente verde natural</p>
              </div>
            </div>
          </GlassCard>

          <GlassCard variant="gradient-4">
            <div className="flex items-center gap-4">
              <div className="flex-shrink-0 p-3 bg-white/30 backdrop-blur-sm rounded-[var(--radius-liquid-md)]">
                <Coffee className="w-6 h-6 text-[#2c2117]" />
              </div>
              <div className="flex-1">
                <h4 className="font-semibold text-white mb-1">Earth Card</h4>
                <p className="text-sm text-white/90">Tarjeta con gradiente tierra</p>
              </div>
            </div>
          </GlassCard>
        </div>
      ),
    },
    {
      id: 'controls',
      label: 'Controles',
      icon: <Settings className="w-4 h-4" />,
      content: (
        <GlassCard>
          <h3 className="text-xl font-semibold text-[#2c2117] mb-6">Configuración</h3>
          <div className="space-y-4">
            <GlassToggle
              checked={toggleState.notifications}
              onChange={(checked) => setToggleState({ ...toggleState, notifications: checked })}
              label="Notificaciones"
              variant="gold"
            />
            <GlassToggle
              checked={toggleState.darkMode}
              onChange={(checked) => setToggleState({ ...toggleState, darkMode: checked })}
              label="Modo Premium"
              variant="olive"
            />
            <GlassToggle
              checked={toggleState.autoSave}
              onChange={(checked) => setToggleState({ ...toggleState, autoSave: checked })}
              label="Guardar Automáticamente"
              variant="brown"
            />
          </div>
        </GlassCard>
      ),
    },
    {
      id: 'tokens',
      label: 'Tokens',
      icon: <Package className="w-4 h-4" />,
      content: (
        <GlassCard variant="default" blur="xl">
          <h2 className="text-2xl font-semibold text-[#2c2117] mb-6">Tokens CSS Disponibles</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Palette Colors */}
            <div>
              <h4 className="font-semibold text-[#2c2117] mb-4 flex items-center gap-2">
                <Palette className="w-5 h-5 text-[#c38f37]" />
                Paleta de Colores
              </h4>
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-[var(--radius-liquid-sm)] bg-[#c38f37] border border-white/30 shadow-md" />
                  <div className="text-sm">
                    <div className="font-mono text-[#2c2117]">#c38f37</div>
                    <div className="text-[#564535]">Gold</div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-[var(--radius-liquid-sm)] bg-[#564535] border border-white/30 shadow-md" />
                  <div className="text-sm">
                    <div className="font-mono text-[#2c2117]">#564535</div>
                    <div className="text-[#564535]">Brown Medium</div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-[var(--radius-liquid-sm)] bg-[#2c2117] border border-white/30 shadow-md" />
                  <div className="text-sm">
                    <div className="font-mono text-[#2c2117]">#2c2117</div>
                    <div className="text-[#564535]">Brown Dark</div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-[var(--radius-liquid-sm)] bg-[#243018] border border-white/30 shadow-md" />
                  <div className="text-sm">
                    <div className="font-mono text-[#2c2117]">#243018</div>
                    <div className="text-[#564535]">Green Dark</div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-[var(--radius-liquid-sm)] bg-[#637742] border border-white/30 shadow-md" />
                  <div className="text-sm">
                    <div className="font-mono text-[#2c2117]">#637742</div>
                    <div className="text-[#564535]">Olive</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Glass Variables */}
            <div>
              <h4 className="font-semibold text-[#2c2117] mb-4">Variables de Vidrio</h4>
              <div className="space-y-2 text-sm text-[#564535] font-mono">
                <div>--glass-gold</div>
                <div>--glass-gold-light</div>
                <div>--glass-brown</div>
                <div>--glass-brown-dark</div>
                <div>--glass-olive</div>
                <div>--glass-green-dark</div>
              </div>
            </div>

            {/* Blur */}
            <div>
              <h4 className="font-semibold text-[#2c2117] mb-4">Efectos de Blur</h4>
              <div className="space-y-2 text-sm text-[#564535] font-mono">
                <div>--blur-sm: 10px</div>
                <div>--blur-md: 20px</div>
                <div>--blur-lg: 40px</div>
                <div>--blur-xl: 60px</div>
              </div>
            </div>

            {/* Radius */}
            <div>
              <h4 className="font-semibold text-[#2c2117] mb-4">Border Radius</h4>
              <div className="space-y-2 text-sm text-[#564535] font-mono">
                <div>--radius-liquid-sm: 12px</div>
                <div>--radius-liquid-md: 20px</div>
                <div>--radius-liquid-lg: 28px</div>
                <div>--radius-liquid-xl: 36px</div>
              </div>
            </div>

            {/* Shadows */}
            <div>
              <h4 className="font-semibold text-[#2c2117] mb-4">Sombras</h4>
              <div className="space-y-2 text-sm text-[#564535] font-mono">
                <div>--shadow-glass-sm</div>
                <div>--shadow-glass-md</div>
                <div>--shadow-glass-lg</div>
                <div>--shadow-glass-xl</div>
              </div>
            </div>

            {/* Glows */}
            <div>
              <h4 className="font-semibold text-[#2c2117] mb-4">Efectos Glow</h4>
              <div className="space-y-2 text-sm text-[#564535] font-mono">
                <div>--glow-gold</div>
                <div>--glow-olive</div>
                <div>--glow-brown</div>
              </div>
            </div>
          </div>
        </GlassCard>
      ),
    },
  ];

  return (
    <div 
      className="min-h-screen relative overflow-hidden"
      style={{
        background: `
          linear-gradient(135deg, 
            #637742 0%, 
            #c38f37 25%, 
            #564535 50%, 
            #243018 75%, 
            #2c2117 100%
          )`,
      }}
    >
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-20 w-96 h-96 bg-[#c38f37]/30 rounded-full blur-[100px] animate-pulse" />
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-[#637742]/30 rounded-full blur-[100px] animate-pulse" style={{ animationDelay: '1s' }} />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-[#564535]/20 rounded-full blur-[120px] animate-pulse" style={{ animationDelay: '2s' }} />
      </div>

      {/* Navbar */}
      <GlassNavbar
        logo={
          <>
            <div className="w-10 h-10 bg-gradient-to-br from-[#c38f37] to-[#637742] rounded-[var(--radius-liquid-md)] flex items-center justify-center shadow-lg">
              <Crown className="w-6 h-6 text-white" />
            </div>
            <span className="font-semibold text-lg text-[#2c2117]">Liquid Glass</span>
          </>
        }
        rightContent={
          <>
            <GlassNavItem active={activeNav === 'home'} onClick={() => setActiveNav('home')}>
              <Home className="w-4 h-4" />
            </GlassNavItem>
            <GlassNavItem active={activeNav === 'notifications'} onClick={() => setActiveNav('notifications')}>
              <Bell className="w-4 h-4" />
            </GlassNavItem>
            <GlassNavItem active={activeNav === 'settings'} onClick={() => setActiveNav('settings')}>
              <Settings className="w-4 h-4" />
            </GlassNavItem>
            <GlassButton variant="gold" size="sm" glow>
              <User className="w-4 h-4 mr-2" />
              Perfil
            </GlassButton>
          </>
        }
      />

      {/* Main Content */}
      <div className="relative z-10 pt-32 pb-16 px-4 max-w-6xl mx-auto">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 mb-4 px-4 py-2 bg-white/30 backdrop-blur-md rounded-full border border-white/40">
            <Crown className="w-5 h-5 text-[#c38f37]" />
            <span className="text-sm font-medium text-[#2c2117]">Diseño Premium</span>
          </div>
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-4 drop-shadow-[0_4px_12px_rgba(44,33,23,0.6)]">
            Liquid Glass Design System
          </h1>
          <p className="text-xl text-white/95 mb-8 drop-shadow-lg max-w-2xl mx-auto">
            Sistema de diseño inspirado en Apple Vision Pro con paleta de colores tierra, oro y naturaleza
          </p>
          <div className="flex flex-wrap gap-4 justify-center">
            <GlassButton variant="gold" size="lg" onClick={() => setIsModalOpen(true)} glow>
              <Sparkles className="w-5 h-5 mr-2" />
              Ver Demo
            </GlassButton>
            <GlassButton variant="outline" size="lg">
              <Send className="w-5 h-5 mr-2" />
              Documentación
            </GlassButton>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <GlassCard variant="gradient-2" blur="lg">
            <div className="text-center">
              <div className="inline-flex p-4 bg-white/40 rounded-[var(--radius-liquid-lg)] mb-4 shadow-lg backdrop-blur-md">
                <Crown className="w-8 h-8 text-[#2c2117]" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2 drop-shadow-lg">Glassmorphism</h3>
              <p className="text-sm text-white font-semibold drop-shadow-md">Efectos de vidrio con blur y transparencias premium</p>
            </div>
          </GlassCard>

          <GlassCard variant="gradient-3" blur="lg">
            <div className="text-center">
              <div className="inline-flex p-4 bg-white/40 rounded-[var(--radius-liquid-lg)] mb-4 shadow-lg backdrop-blur-md">
                <Leaf className="w-8 h-8 text-[#2c2117]" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2 drop-shadow-lg">Paleta Natural</h3>
              <p className="text-sm text-white font-semibold drop-shadow-md">Colores tierra inspirados en la naturaleza</p>
            </div>
          </GlassCard>

          <GlassCard variant="gradient-4" blur="lg">
            <div className="text-center">
              <div className="inline-flex p-4 bg-white/40 rounded-[var(--radius-liquid-lg)] mb-4 shadow-lg backdrop-blur-md">
                <Coffee className="w-8 h-8 text-[#2c2117]" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2 drop-shadow-lg">Tokens CSS</h3>
              <p className="text-sm text-white font-semibold drop-shadow-md">Variables personalizables y escalables</p>
            </div>
          </GlassCard>
        </div>

        {/* Tabs Section */}
        <GlassTabs tabs={tabs} defaultTab="components" />
      </div>

      {/* Modal Demo */}
      <GlassModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Ejemplo de Modal"
        footer={
          <>
            <GlassButton variant="outline" onClick={() => setIsModalOpen(false)}>
              Cancelar
            </GlassButton>
            <GlassButton variant="gold" glow onClick={() => setIsModalOpen(false)}>
              Confirmar
            </GlassButton>
          </>
        }
      >
        <p className="mb-4 text-[#2c2117]">
          Este es un modal con efecto liquid glass. Incluye backdrop blur, transparencias y animaciones fluidas con la paleta de colores personalizada.
        </p>
        <div className="space-y-3">
          <GlassInput placeholder="Tu nombre..." />
          <GlassTextarea placeholder="Tu mensaje..." rows={3} />
        </div>
      </GlassModal>
    </div>
  );
}