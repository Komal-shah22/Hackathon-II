'use client';

import { useState, useCallback, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Task, TaskFilters, TaskCreate, TaskUpdate } from '@/lib/types';
import { api } from '@/lib/api';
import { TaskItem } from './task-item';
import { TaskForm } from './task-form';
import { Button } from '@/components/ui/button';
import { TaskListSkeleton } from '@/components/ui/skeleton';
import { useTaskToast } from '@/lib/toast';

interface TaskListProps {
  userId: string;
  initialTasks?: Task[];
  initialTotal?: number;
}

const defaultFilters: TaskFilters = {
  status: 'all',
  priority: 'all',
  category: 'all',
  search: '',
  sort_by: 'created_at',
  sort_order: 'desc',
};

// Debounce hook
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

export function TaskList({ userId, initialTasks = [], initialTotal = 0 }: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>(initialTasks);
  const [total, setTotal] = useState(initialTotal);
  const [filters, setFilters] = useState<TaskFilters>(defaultFilters);
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searchValue, setSearchValue] = useState('');
  const debouncedSearch = useDebounce(searchValue, 300);

  const taskToast = useTaskToast();

  // Update filters when debounced search changes
  useEffect(() => {
    setFilters((prev) => ({ ...prev, search: debouncedSearch }));
  }, [debouncedSearch]);

  // Fetch tasks with filters
  const fetchTasks = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await api.getTasks(userId, {
        status: filters.status,
        priority: filters.priority,
        category: filters.category === 'all' ? undefined : filters.category,
        search: filters.search || undefined,
        sort_by: filters.sort_by,
        sort_order: filters.sort_order,
      });
      setTasks(response.tasks);
      setTotal(response.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  }, [userId, filters]);

  // Fetch on filter change
  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const handleCreateTask = async (data: TaskCreate) => {
    setLoading(true);
    setError(null);

    try {
      const newTask = await api.createTask(userId, data);
      setTasks((prev) => [newTask, ...prev]);
      setTotal((prev) => prev + 1);
      setShowForm(false);
      taskToast.created();
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to create task';
      setError(message);
      taskToast.error(message);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateTask = async (data: TaskUpdate) => {
    if (!editingTask) return;

    setLoading(true);
    setError(null);

    try {
      const updatedTask = await api.updateTask(userId, editingTask.id, data);
      setTasks((prev) =>
        prev.map((t) => (t.id === editingTask.id ? updatedTask : t))
      );
      setEditingTask(null);
      taskToast.updated();
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to update task';
      setError(message);
      taskToast.error(message);
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = async (taskId: number) => {
    setError(null);

    try {
      const task = tasks.find((t) => t.id === taskId);
      if (task) {
        const updated = await api.toggleComplete(userId, taskId, !task.completed);
        setTasks((prev) =>
          prev.map((t) => (t.id === taskId ? updated : t))
        );
        if (updated.completed) {
          taskToast.completed();
        }
      }
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to toggle task';
      taskToast.error(message);
    }
  };

  const handleEdit = (task: Task) => {
    setEditingTask(task);
    setShowForm(false);
  };

  const handleDelete = async (taskId: number) => {
    if (!confirm('Are you sure you want to delete this task?')) return;

    setError(null);

    try {
      await api.deleteTask(userId, taskId);
      setTasks((prev) => prev.filter((t) => t.id !== taskId));
      setTotal((prev) => prev - 1);
      taskToast.deleted();
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to delete task';
      setError(message);
      taskToast.error(message);
    }
  };

  const handleCancelForm = () => {
    setShowForm(false);
    setEditingTask(null);
  };

  const handleSearchChange = (value: string) => {
    setSearchValue(value);
  };

  const clearFilters = () => {
    setSearchValue('');
    setFilters(defaultFilters);
  };

  const hasActiveFilters =
    filters.status !== 'all' ||
    filters.priority !== 'all' ||
    filters.category !== 'all' ||
    filters.search !== '';

  return (
    <div className="space-y-4">
      {/* Search Bar - Prominent Position */}
      <div className="mb-4">
        <div className="relative max-w-2xl">
          <div className="absolute inset-y-0 left-0 flex items-center pl-4 pointer-events-none">
            <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <input
            type="text"
            placeholder="Search tasks by title or description..."
            value={searchValue}
            onChange={(e) => handleSearchChange(e.target.value)}
            className="w-full pl-12 pr-12 py-3 bg-[#141b2e] border border-white/10 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20 transition-all"
          />
          {searchValue && (
            <button
              onClick={() => handleSearchChange('')}
              className="absolute inset-y-0 right-0 flex items-center pr-4 text-gray-400 hover:text-cyan-400 transition-colors"
              aria-label="Clear search"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>
        {searchValue && (
          <p className="mt-2 text-sm text-gray-400">
            Showing {tasks.length} of {total} tasks
          </p>
        )}
      </div>

      {/* Filters */}
      <div className="bg-[#141b2e] p-4 rounded-lg border border-white/10">
        <div className="flex flex-wrap gap-4">
          {/* Status Filter */}
          <label className="flex items-center gap-2">
            <span className="text-sm text-gray-400">Status:</span>
            <select
              value={filters.status}
              onChange={(e) => setFilters({ ...filters, status: e.target.value as TaskFilters['status'] })}
              className="px-3 py-2 bg-[#1e2742] border border-white/10 rounded-md text-gray-300 focus:outline-none focus:ring-2 focus:ring-cyan-500 transition-all"
              aria-label="Filter by status"
            >
              <option value="all">All</option>
              <option value="pending">Pending</option>
              <option value="completed">Completed</option>
            </select>
          </label>

          {/* Priority Filter */}
          <label className="flex items-center gap-2">
            <span className="text-sm text-gray-400">Priority:</span>
            <select
              value={filters.priority}
              onChange={(e) => setFilters({ ...filters, priority: e.target.value as TaskFilters['priority'] })}
              className="px-3 py-2 bg-[#1e2742] border border-white/10 rounded-md text-gray-300 focus:outline-none focus:ring-2 focus:ring-cyan-500 transition-all"
              aria-label="Filter by priority"
            >
              <option value="all">All</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
              <option value="none">None</option>
            </select>
          </label>

          {/* Category Filter */}
          <label className="flex items-center gap-2">
            <span className="text-sm text-gray-400">Category:</span>
            <select
              value={filters.category}
              onChange={(e) => setFilters({ ...filters, category: e.target.value })}
              className="px-3 py-2 bg-[#1e2742] border border-white/10 rounded-md text-gray-300 focus:outline-none focus:ring-2 focus:ring-cyan-500 transition-all"
              aria-label="Filter by category"
            >
              <option value="all">All</option>
              <option value="work">Work</option>
              <option value="personal">Personal</option>
              <option value="shopping">Shopping</option>
              <option value="health">Health</option>
              <option value="finance">Finance</option>
              <option value="other">Other</option>
            </select>
          </label>

          {/* Sort By */}
          <label className="flex items-center gap-2">
            <span className="text-sm text-gray-400">Sort:</span>
            <select
              value={filters.sort_by}
              onChange={(e) => setFilters({ ...filters, sort_by: e.target.value as TaskFilters['sort_by'] })}
              className="px-3 py-2 bg-[#1e2742] border border-white/10 rounded-md text-gray-300 focus:outline-none focus:ring-2 focus:ring-cyan-500 transition-all"
              aria-label="Sort by"
            >
              <option value="created_at">Created Date</option>
              <option value="due_date">Due Date</option>
              <option value="priority">Priority</option>
              <option value="title">Title</option>
            </select>
          </label>

          {/* Sort Order */}
          <select
            value={filters.sort_order}
            onChange={(e) => setFilters({ ...filters, sort_order: e.target.value as TaskFilters['sort_order'] })}
            className="px-3 py-2 bg-[#1e2742] border border-white/10 rounded-md text-gray-300 focus:outline-none focus:ring-2 focus:ring-cyan-500 transition-all"
            aria-label="Sort order"
          >
            <option value="desc">Newest First</option>
            <option value="asc">Oldest First</option>
          </select>

          {hasActiveFilters && (
            <Button variant="secondary" onClick={clearFilters} aria-label="Clear all filters">
              Clear Filters
            </Button>
          )}
        </div>
      </div>

      {/* Header */}
      <div className="flex justify-between items-center">
        <div className="text-sm text-gray-300" role="status" aria-live="polite">
          {!searchValue && `Showing ${tasks.length} of ${total} tasks`}
        </div>

        <Button onClick={() => setShowForm(true)} aria-label="Create new task">
          + Add Task
        </Button>
      </div>

      {/* Task Form */}
      <AnimatePresence>
        {(showForm || editingTask) && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.2 }}
          >
            <TaskForm
              task={editingTask}
              onSubmit={editingTask ? handleUpdateTask : handleCreateTask}
              onCancel={handleCancelForm}
              loading={loading}
            />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Loading State with Skeleton */}
      {loading && tasks.length === 0 && (
        <TaskListSkeleton count={5} />
      )}

      {/* Empty State with Illustration */}
      {!loading && tasks.length === 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-center py-12 bg-[#0a0e1a] rounded-lg border border-white/10"
        >
          <svg
            className="mx-auto h-12 w-12 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
            />
          </svg>
          <h3 className="mt-2 text-lg font-medium text-white">No tasks found</h3>
          <p className="mt-1 text-gray-400">
            {hasActiveFilters
              ? 'Try adjusting your filters'
              : 'Get started by creating your first task'}
          </p>
          {!hasActiveFilters && (
            <div className="mt-4">
              <Button onClick={() => setShowForm(true)}>Create Your First Task</Button>
            </div>
          )}
        </motion.div>
      )}

      {/* Task List with Animations */}
      {!loading && tasks.length > 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3 }}
        >
          <AnimatePresence mode="popLayout">
            {tasks.map((task, index) => (
              <motion.div
                key={task.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.95 }}
                transition={{ duration: 0.2, delay: index * 0.05 }}
                layout
              >
                <TaskItem
                  task={task}
                  onToggle={handleToggle}
                  onEdit={handleEdit}
                  onDelete={handleDelete}
                />
              </motion.div>
            ))}
          </AnimatePresence>
        </motion.div>
      )}
    </div>
  );
}
