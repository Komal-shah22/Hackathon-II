'use client';

import { useState, useEffect, ChangeEvent } from 'react';
import { Task, TaskCreate, TaskPriority, TaskCategory, RecurrencePattern } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Checkbox } from '@/components/ui/checkbox';
import { cn } from '@/lib/utils';

interface TaskFormProps {
  task?: Task | null;
  onSubmit: (data: TaskCreate) => void;
  onCancel: () => void;
  loading?: boolean;
}

const PRIORITIES: { value: TaskPriority | null; label: string }[] = [
  { value: null, label: 'None' },
  { value: 'high', label: 'High' },
  { value: 'medium', label: 'Medium' },
  { value: 'low', label: 'Low' },
];

const CATEGORIES: { value: TaskCategory | null; label: string }[] = [
  { value: null, label: 'None' },
  { value: 'work', label: 'Work' },
  { value: 'personal', label: 'Personal' },
  { value: 'shopping', label: 'Shopping' },
  { value: 'health', label: 'Health' },
  { value: 'finance', label: 'Finance' },
  { value: 'other', label: 'Other' },
];

const RECURRENCE_PATTERNS: { value: RecurrencePattern | null; label: string }[] = [
  { value: null, label: 'None' },
  { value: 'daily', label: 'Daily' },
  { value: 'weekly', label: 'Weekly' },
  { value: 'monthly', label: 'Monthly' },
];

export function TaskForm({ task, onSubmit, onCancel, loading }: TaskFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<TaskPriority | null>(null);
  const [category, setCategory] = useState<TaskCategory | null>(null);
  const [dueDate, setDueDate] = useState('');
  const [dueTime, setDueTime] = useState('');
  const [reminderTime, setReminderTime] = useState('');
  const [isRecurring, setIsRecurring] = useState(false);
  const [recurrencePattern, setRecurrencePattern] = useState<RecurrencePattern | null>(null);
  const [recurrenceInterval, setRecurrenceInterval] = useState(1);
  const [recurrenceEndDate, setRecurrenceEndDate] = useState('');
  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    if (task) {
      setTitle(task.title);
      setDescription(task.description || '');
      setPriority(task.priority);
      setCategory(task.category);
      if (task.due_date) {
        const due = new Date(task.due_date);
        setDueDate(due.toISOString().split('T')[0]);
        setDueTime(due.toTimeString().slice(0, 5));
      }
      if (task.reminder_time) {
        const rem = new Date(task.reminder_time);
        setReminderTime(rem.toISOString().slice(0, 16));
      }
      setIsRecurring(task.is_recurring);
      setRecurrencePattern(task.recurrence_pattern);
      if (task.recurrence_end_date) {
        setRecurrenceEndDate(task.recurrence_end_date.split('T')[0]);
      }
    } else {
      resetForm();
    }
  }, [task]);

  const resetForm = () => {
    setTitle('');
    setDescription('');
    setPriority(null);
    setCategory(null);
    setDueDate('');
    setDueTime('');
    setReminderTime('');
    setIsRecurring(false);
    setRecurrencePattern(null);
    setRecurrenceInterval(1);
    setRecurrenceEndDate('');
    setErrors({});
  };

  const validate = () => {
    const newErrors: Record<string, string> = {};

    if (!title.trim()) {
      newErrors.title = 'Title is required';
    } else if (title.length > 200) {
      newErrors.title = 'Title must be 200 characters or less';
    }

    if (description.length > 1000) {
      newErrors.description = 'Description must be 1000 characters or less';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) return;

    // Build due_date
    let dueDateValue: string | undefined;
    if (dueDate) {
      const date = dueTime ? `${dueDate}T${dueTime}:00` : `${dueDate}T00:00:00`;
      dueDateValue = date;
    }

    // Build reminder_time
    let reminderTimeValue: string | undefined;
    if (reminderTime) {
      reminderTimeValue = reminderTime;
    }

    // Build recurrence_end_date
    let recurrenceEndDateValue: string | undefined;
    if (recurrenceEndDate) {
      recurrenceEndDateValue = `${recurrenceEndDate}T00:00:00`;
    }

    const data: TaskCreate = {
      title: title.trim(),
      description: description.trim() || undefined,
      priority: priority || undefined,
      category: category || undefined,
      due_date: dueDateValue,
      reminder_time: reminderTimeValue,
      is_recurring: isRecurring,
      recurrence_pattern: isRecurring ? recurrencePattern || undefined : undefined,
      recurrence_interval: isRecurring && recurrencePattern ? recurrenceInterval : undefined,
      recurrence_end_date: isRecurring && recurrencePattern ? recurrenceEndDateValue : undefined,
    };

    onSubmit(data);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 p-6 bg-[#141b2e] rounded-lg border border-white/10">
      <h3 className="font-medium text-lg text-white mb-4">
        {task ? 'Edit Task' : 'Create New Task'}
      </h3>

      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-300 mb-1">
          Title
        </label>
        <Input
          id="title"
          value={title}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setTitle(e.target.value)}
          placeholder="Enter task title"
          required
          maxLength={200}
          disabled={loading}
          className={errors.title ? 'border-danger focus-visible:ring-danger' : ''}
        />
        {errors.title && (
          <p className="mt-1 text-sm text-danger">{errors.title}</p>
        )}
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-300 mb-1">
          Description (optional)
        </label>
        <Textarea
          id="description"
          value={description}
          onChange={(e: ChangeEvent<HTMLTextAreaElement>) => setDescription(e.target.value)}
          placeholder="Enter task description"
          maxLength={1000}
          rows={3}
          disabled={loading}
          className={errors.description ? 'border-danger focus-visible:ring-danger' : ''}
        />
        {errors.description && (
          <p className="mt-1 text-sm text-danger">{errors.description}</p>
        )}
      </div>

      {/* Priority and Category */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label htmlFor="priority" className="block text-sm font-medium text-gray-300 mb-1">
            Priority
          </label>
          <select
            id="priority"
            value={priority || ''}
            onChange={(e: ChangeEvent<HTMLSelectElement>) => setPriority(e.target.value as TaskPriority || null)}
            className="w-full px-3 py-2 bg-[#1e2742] border border-white/10 rounded-md text-gray-300 focus:outline-none focus:ring-2 focus:ring-cyan-500 transition-all"
            disabled={loading}
          >
            {PRIORITIES.map((p) => (
              <option key={p.label} value={p.value || ''}>
                {p.label}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="category" className="block text-sm font-medium text-gray-300 mb-1">
            Category
          </label>
          <select
            id="category"
            value={category || ''}
            onChange={(e: ChangeEvent<HTMLSelectElement>) => setCategory(e.target.value as TaskCategory || null)}
            className="w-full px-3 py-2 bg-[#1e2742] border border-white/10 rounded-md text-gray-300 focus:outline-none focus:ring-2 focus:ring-cyan-500 transition-all"
            disabled={loading}
          >
            {CATEGORIES.map((c) => (
              <option key={c.label} value={c.value || ''}>
                {c.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Due Date and Time */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label htmlFor="dueDate" className="block text-sm font-medium text-gray-300 mb-1">
            Due Date (optional)
          </label>
          <Input
            id="dueDate"
            type="date"
            value={dueDate}
            onChange={(e: ChangeEvent<HTMLInputElement>) => setDueDate(e.target.value)}
            disabled={loading}
          />
        </div>

        <div>
          <label htmlFor="dueTime" className="block text-sm font-medium text-gray-300 mb-1">
            Due Time (optional)
          </label>
          <Input
            id="dueTime"
            type="time"
            value={dueTime}
            onChange={(e: ChangeEvent<HTMLInputElement>) => setDueTime(e.target.value)}
            disabled={loading}
          />
        </div>
      </div>

      {/* Reminder */}
      <div>
        <label htmlFor="reminderTime" className="block text-sm font-medium text-gray-300 mb-1">
          Reminder (optional)
        </label>
        <Input
          id="reminderTime"
          type="datetime-local"
          value={reminderTime}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setReminderTime(e.target.value)}
          disabled={loading}
        />
      </div>

      {/* Recurring Options */}
      <div className="border-t border-white/10 pt-4 mt-4">
        <div className="flex items-center space-x-2 mb-4">
          <Checkbox
            id="isRecurring"
            checked={isRecurring}
            onCheckedChange={(checked: boolean) => setIsRecurring(checked)}
            disabled={loading}
          />
          <label htmlFor="isRecurring" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 text-gray-300">
            Recurring Task
          </label>
        </div>

        {isRecurring && (
          <div className="space-y-4 pl-6">
            <div>
              <label htmlFor="recurrencePattern" className="block text-sm font-medium text-gray-300 mb-1">
                Repeat Pattern
              </label>
              <select
                id="recurrencePattern"
                value={recurrencePattern || ''}
                onChange={(e: ChangeEvent<HTMLSelectElement>) => setRecurrencePattern(e.target.value as RecurrencePattern || null)}
                className="w-full px-3 py-2 bg-[#1e2742] border border-white/10 rounded-md text-gray-300 focus:outline-none focus:ring-2 focus:ring-cyan-500 transition-all"
                disabled={loading}
              >
                {RECURRENCE_PATTERNS.map((p) => (
                  <option key={p.label} value={p.value || ''}>
                    {p.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="recurrenceInterval" className="block text-sm font-medium text-gray-300 mb-1">
                  Interval
                </label>
                <Input
                  id="recurrenceInterval"
                  type="number"
                  value={recurrenceInterval}
                  onChange={(e: ChangeEvent<HTMLInputElement>) => setRecurrenceInterval(parseInt(e.target.value) || 1)}
                  min={1}
                  disabled={loading}
                />
              </div>

              <div>
                <label htmlFor="recurrenceEndDate" className="block text-sm font-medium text-gray-300 mb-1">
                  End Date (optional)
                </label>
                <Input
                  id="recurrenceEndDate"
                  type="date"
                  value={recurrenceEndDate}
                  onChange={(e: ChangeEvent<HTMLInputElement>) => setRecurrenceEndDate(e.target.value)}
                  disabled={loading}
                />
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="flex justify-end gap-2 pt-4">
        <Button
          type="button"
          variant="outline" // Use outline variant for cancel
          onClick={onCancel}
          disabled={loading}
        >
          Cancel
        </Button>
        <Button type="submit" disabled={loading}>
          {task ? 'Save Changes' : 'Create Task'}
        </Button>
      </div>
    </form>
  );
}
