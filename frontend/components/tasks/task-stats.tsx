'use client';

import { useEffect, useState } from 'react';
import { UserStats } from '@/lib/types';
import { api } from '@/lib/api';

interface TaskStatsProps {
  userId: string;
}

export function TaskStats({ userId }: TaskStatsProps) {
  const [stats, setStats] = useState<UserStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await api.getUserStats(userId);
        setStats(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load stats');
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, [userId]);

  if (loading) {
    return (
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="bg-white p-4 rounded-lg border border-gray-200 animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-20 mb-2"></div>
            <div className="h-8 bg-gray-200 rounded w-12"></div>
          </div>
        ))}
      </div>
    );
  }

  if (error || !stats) {
    return null;
  }

  const statCards = [
    {
      label: 'Total Tasks',
      value: stats.total_tasks,
      color: 'text-gray-900',
    },
    {
      label: 'Completed',
      value: stats.completed_tasks,
      color: 'text-green-600',
    },
    {
      label: 'Pending',
      value: stats.pending_tasks,
      color: 'text-yellow-600',
    },
    {
      label: 'Overdue',
      value: stats.overdue_count,
      color: stats.overdue_count > 0 ? 'text-red-600' : 'text-gray-600',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Main Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {statCards.map((stat) => (
          <div
            key={stat.label}
            className="bg-white p-4 rounded-lg border border-gray-200 shadow-sm"
          >
            <p className="text-sm text-gray-500">{stat.label}</p>
            <p className={`text-3xl font-bold mt-1 ${stat.color}`}>{stat.value}</p>
          </div>
        ))}
      </div>

      {/* Completion Rate */}
      <div className="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
        <div className="flex items-center justify-between mb-2">
          <p className="text-sm text-gray-500">Completion Rate</p>
          <p className="text-lg font-semibold text-gray-900">
            {(stats.completion_rate * 100).toFixed(0)}%
          </p>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-blue-500 h-2 rounded-full transition-all duration-300"
            style={{ width: `${stats.completion_rate * 100}%` }}
          ></div>
        </div>
      </div>

      {/* By Category */}
      <div className="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
        <h3 className="font-medium text-gray-900 mb-4">Tasks by Category</h3>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {Object.entries(stats.by_category).map(([category, count]) => (
            <div key={category} className="flex items-center justify-between">
              <span className="text-sm text-gray-600 capitalize">{category}</span>
              <span className="font-medium text-gray-900">{count}</span>
            </div>
          ))}
        </div>
      </div>

      {/* By Priority */}
      <div className="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
        <h3 className="font-medium text-gray-900 mb-4">Tasks by Priority</h3>
        <div className="space-y-3">
          {Object.entries(stats.by_priority).map(([priority, count]) => {
            const colors: Record<string, string> = {
              high: 'bg-red-500',
              medium: 'bg-yellow-500',
              low: 'bg-green-500',
            };
            const percentage = stats.total_tasks > 0 ? (count / stats.total_tasks) * 100 : 0;

            return (
              <div key={priority}>
                <div className="flex items-center justify-between text-sm mb-1">
                  <span className="capitalize text-gray-600">{priority}</span>
                  <span className="text-gray-900">{count}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`${colors[priority] || 'bg-gray-500'} h-2 rounded-full transition-all duration-300`}
                    style={{ width: `${percentage}%` }}
                  ></div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Due Today */}
      {stats.due_today_count > 0 && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div className="flex items-center gap-2">
            <svg className="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p className="text-yellow-800 font-medium">
              You have {stats.due_today_count} task{stats.due_today_count !== 1 ? 's' : ''} due today!
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
