'use client';

import { useState } from 'react';
import { useAuth } from '@/components/auth';
import { TaskList } from '@/components/tasks/task-list';
import { TaskStats } from '@/components/tasks/task-stats';
import { motion } from 'framer-motion';

export default function DashboardPage() {
  const { user } = useAuth();
  const [showStats, setShowStats] = useState(false);
  const [activeTab, setActiveTab] = useState<'tasks' | 'stats'>('tasks');

  if (!user) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <p className="text-gray-400">Please sign in to view your dashboard</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header with Stats Toggle */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-[#141b2e] p-6 rounded-lg border border-white/10"
      >
        <div>
          <h1 className="text-2xl font-bold text-white">My Dashboard</h1>
          <p className="text-gray-400 mt-1">Manage and track your tasks</p>
        </div>

        <div className="flex items-center gap-3">
          {/* Tab Toggle */}
          <div className="flex bg-[#1e2742] rounded-lg p-1">
            <button
              onClick={() => setActiveTab('tasks')}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${
                activeTab === 'tasks'
                  ? 'bg-cyan-500 text-white'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              Tasks
            </button>
            <button
              onClick={() => {
                setActiveTab('stats');
                setShowStats(true);
              }}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${
                activeTab === 'stats'
                  ? 'bg-cyan-500 text-white'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              Statistics
            </button>
          </div>
        </div>
      </motion.div>

      {/* Main Content */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
      >
        {activeTab === 'tasks' ? (
          <TaskList userId={user.id} />
        ) : (
          <div className="bg-[#141b2e] p-6 rounded-lg border border-white/10">
            <h2 className="text-xl font-semibold text-white mb-4">Task Statistics</h2>
            <TaskStats userId={user.id} />
          </div>
        )}
      </motion.div>

      {/* Stats Section (when enabled in tasks view) */}
      {showStats && activeTab === 'tasks' && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <div className="bg-[#141b2e] p-6 rounded-lg border border-white/10">
            <h2 className="text-xl font-semibold text-white mb-4">Task Statistics</h2>
            <TaskStats userId={user.id} />
          </div>
        </motion.div>
      )}

      {/* Feature Level Legend */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
        className="bg-[#141b2e] p-4 rounded-lg border border-white/10"
      >
        <h3 className="text-sm font-medium text-gray-400 mb-3">Feature Levels</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Basic Level */}
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-lg bg-green-500/20 flex items-center justify-center">
              <svg className="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <div>
              <p className="text-sm font-medium text-white">Basic</p>
              <p className="text-xs text-gray-400">Create, Read, Update, Delete tasks</p>
            </div>
          </div>

          {/* Intermediate Level */}
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-lg bg-yellow-500/20 flex items-center justify-center">
              <svg className="w-4 h-4 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A2 2 0 013 12V7a4 4 0 014-4z" />
              </svg>
            </div>
            <div>
              <p className="text-sm font-medium text-white">Intermediate</p>
              <p className="text-xs text-gray-400">Priority, Category, Search, Filter, Sort</p>
            </div>
          </div>

          {/* Advanced Level */}
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-lg bg-purple-500/20 flex items-center justify-center">
              <svg className="w-4 h-4 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <div>
              <p className="text-sm font-medium text-white">Advanced</p>
              <p className="text-xs text-gray-400">Due Dates, Reminders, Recurring, Stats</p>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
}

