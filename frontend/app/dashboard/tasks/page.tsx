'use client';

import { useAuth } from '@/components/auth';
import { TaskList } from '@/components/tasks/task-list';

export default function TasksPage() {
  const { user } = useAuth();

  if (!user) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <p className="text-gray-400">Please sign in to view your tasks</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-[#141b2e] p-6 rounded-lg border border-white/10">
        <h1 className="text-2xl font-bold text-white">My Tasks</h1>
        <p className="text-gray-400 mt-1">Create, manage, and track your tasks</p>
      </div>
      <TaskList userId={user.id} />
    </div>
  );
}
