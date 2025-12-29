'use client';

import { useAuth } from '@/components/auth';
import { TaskStats } from '@/components/tasks/task-stats';
import { motion } from 'framer-motion';

export default function StatisticsPage() {
  const { user } = useAuth();

  if (!user) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <p className="text-gray-400">Please sign in to view statistics</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-[#141b2e] p-6 rounded-lg border border-white/10"
      >
        <h1 className="text-2xl font-bold text-white">Task Statistics</h1>
        <p className="text-gray-400 mt-1">Analyze your productivity and task completion</p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-[#141b2e] p-6 rounded-lg border border-white/10"
      >
        <TaskStats userId={user.id} />
      </motion.div>
    </div>
  );
}
