'use client';

import { useState } from 'react';
import { Task, TaskPriority, TaskCategory } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import { FiCalendar, FiBell, FiTrash2, FiEdit } from 'react-icons/fi';

interface TaskItemProps {
  task: Task;
  onToggle: (id: number) => void;
  onEdit: (task: Task) => void;
  onDelete: (id: number) => void;
}

export function TaskItem({ task, onToggle, onEdit, onDelete }: TaskItemProps) {
  const [showFullDescription, setShowFullDescription] = useState(false);

  const formatDate = (dateStr: string | null) => {
    if (!dateStr) return null;
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const isOverdue = task.due_date && !task.completed && new Date(task.due_date) < new Date();

  const getPriorityVariant = (priority: TaskPriority | null) => {
    switch (priority) {
      case 'high':
        return 'danger';
      case 'medium':
        return 'warning';
      case 'low':
        return 'info';
      default:
        return 'secondary';
    }
  };

  const getCategoryVariant = (category: TaskCategory | null) => {
    switch (category) {
      case 'work':
        return 'primary';
      case 'personal':
        return 'accent';
      case 'shopping':
        return 'info';
      case 'health':
        return 'success';
      case 'finance':
        return 'warning';
      default:
        return 'secondary';
    }
  };

  return (
    <div className={cn("relative p-4 border rounded-lg mb-2 border-white/10 transition-all duration-300 hover:border-cyan-500/50 hover:shadow-lg hover:shadow-cyan-500/10", task.completed ? 'bg-[#141b2e]/50' : 'bg-[#141b2e]', isOverdue ? 'border-l-4 border-l-danger' : 'border-l-4 border-l-transparent')}>
      <div className="flex items-start gap-3">
        <Checkbox
          id={`task-${task.id}`}
          checked={task.completed}
          onCheckedChange={() => onToggle(task.id)}
          className="mt-1"
          disabled={task.completed} // Disable checkbox if task is completed
        />

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <h3 className={cn("font-medium text-lg truncate", task.completed ? 'line-through text-gray-600' : 'text-white')}>
              {task.title}
            </h3>

            {/* Priority Badge */}
            {task.priority && (
              <Badge variant={getPriorityVariant(task.priority)}>
                {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
              </Badge>
            )}

            {/* Category Badge */}
            {task.category && (
              <Badge variant={getCategoryVariant(task.category)}>
                {task.category.charAt(0).toUpperCase() + task.category.slice(1)}
              </Badge>
            )}

            {/* Recurring Badge */}
            {task.is_recurring && (
              <Badge variant="outline">Recurring</Badge>
            )}
          </div>

{task.description && (
  <p
    onClick={() => setShowFullDescription(!showFullDescription)}
    className={cn(
      "text-sm mt-1",
      task.completed ? 'text-gray-600 line-through' : 'text-gray-300',
      showFullDescription ? '' : 'line-clamp-2 cursor-pointer'
    )}
  >
    {task.description}
  </p>
)}

          {/* Due Date */}
          {task.due_date && (
            <div className="flex items-center gap-1 mt-2 text-sm">
              <FiCalendar className="w-4 h-4 text-gray-400" />
              <span className={isOverdue ? 'text-danger font-medium' : 'text-gray-400'}>
                Due: {formatDate(task.due_date)}
              </span>
              {isOverdue && <span className="text-xs text-danger">(Overdue)</span>}
            </div>
          )}

          {/* Reminder indicator */}
          {task.reminder_time && !task.reminder_sent && (
            <div className="flex items-center gap-1 mt-1 text-sm text-cyan-400 font-medium">
              <FiBell className="w-4 h-4" />
              <span>Reminder set</span>
            </div>
          )}

          <p className="text-xs text-gray-400 mt-2">
            Created: {new Date(task.created_at).toLocaleDateString()}
          </p>
        </div>

        <div className="flex gap-2 flex-shrink-0">
          <Button variant="outline" size="sm" onClick={() => onEdit(task)} className="bg-cyan-500/10 text-cyan-400 border border-cyan-500/50 hover:bg-cyan-500/20 transition-all">
            <FiEdit className="w-4 h-4" />
          </Button>
          <Button variant="outline" size="sm" onClick={() => onDelete(task.id)} className="bg-red-500/10 text-red-400 border border-red-500/50 hover:bg-red-500/20 transition-all">
            <FiTrash2 className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}
