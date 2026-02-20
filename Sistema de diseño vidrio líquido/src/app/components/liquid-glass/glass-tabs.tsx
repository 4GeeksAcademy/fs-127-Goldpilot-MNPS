import React, { useState } from 'react';
import { motion } from 'motion/react';

interface Tab {
  id: string;
  label: string;
  content: React.ReactNode;
  icon?: React.ReactNode;
}

interface GlassTabsProps {
  tabs: Tab[];
  defaultTab?: string;
}

export function GlassTabs({ tabs, defaultTab }: GlassTabsProps) {
  const [activeTab, setActiveTab] = useState(defaultTab || tabs[0]?.id);
  
  const activeContent = tabs.find(tab => tab.id === activeTab)?.content;
  
  return (
    <div className="w-full">
      {/* Tab Headers */}
      <div className="
        inline-flex
        p-1
        bg-[var(--glass-white-light)]
        backdrop-blur-[var(--blur-md)]
        border border-white/30
        rounded-[var(--radius-liquid-md)]
        shadow-[var(--shadow-glass-sm)]
        gap-1
      ">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className="relative px-4 py-2 outline-none"
          >
            {activeTab === tab.id && (
              <motion.div
                layoutId="activeTab"
                className="
                  absolute inset-0
                  bg-white/80
                  backdrop-blur-sm
                  rounded-[var(--radius-liquid-sm)]
                  shadow-[var(--shadow-glass-md)]
                "
                transition={{ type: 'spring', damping: 20, stiffness: 300 }}
              />
            )}
            <span className={`
              relative z-10
              flex items-center gap-2
              text-sm font-medium
              transition-colors
              ${activeTab === tab.id ? 'text-black/90' : 'text-black/50'}
            `}>
              {tab.icon && <span>{tab.icon}</span>}
              {tab.label}
            </span>
          </button>
        ))}
      </div>
      
      {/* Tab Content */}
      <motion.div
        key={activeTab}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="mt-4"
      >
        {activeContent}
      </motion.div>
    </div>
  );
}
