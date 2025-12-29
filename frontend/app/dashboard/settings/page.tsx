'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';

interface SettingsSection {
  id: string;
  title: string;
  description: string;
}

const settingsSections: SettingsSection[] = [
  {
    id: 'account',
    title: 'Account Settings',
    description: 'Manage your account information and preferences',
  },
  {
    id: 'notifications',
    title: 'Notifications',
    description: 'Configure how you receive alerts and updates',
  },
  {
    id: 'privacy',
    title: 'Privacy & Security',
    description: 'Control your data and security settings',
  },
  {
    id: 'appearance',
    title: 'Appearance',
    description: 'Customize the look and feel of the application',
  },
];

export default function SettingsPage() {
  const [activeSection, setActiveSection] = useState('account');

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-[#141b2e] p-6 rounded-lg border border-white/10"
      >
        <h1 className="text-2xl font-bold text-white">Settings</h1>
        <p className="text-gray-400 mt-1">Manage your preferences and configuration</p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {settingsSections.map((section, index) => (
          <motion.button
            key={section.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 + index * 0.05 }}
            onClick={() => setActiveSection(section.id)}
            className={`p-6 rounded-lg border text-left transition-all ${
              activeSection === section.id
                ? 'bg-[#141b2e] border-cyan-500/50 shadow-lg shadow-cyan-500/10'
                : 'bg-[#141b2e] border-white/10 hover:border-white/20'
            }`}
          >
            <h3 className="text-lg font-semibold text-white">{section.title}</h3>
            <p className="text-sm text-gray-400 mt-2">{section.description}</p>
          </motion.button>
        ))}
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="bg-[#141b2e] p-6 rounded-lg border border-white/10"
      >
        <h2 className="text-xl font-semibold text-white mb-4">
          {settingsSections.find((s) => s.id === activeSection)?.title || 'Settings'}
        </h2>
        <div className="text-gray-400">
          <p>This section is under development.</p>
          <p className="mt-2 text-sm">Settings options for {activeSection} will be available soon.</p>
        </div>
      </motion.div>
    </div>
  );
}
