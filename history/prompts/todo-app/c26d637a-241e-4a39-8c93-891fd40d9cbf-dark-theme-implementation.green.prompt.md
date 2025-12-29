---
id: c26d637a-241e-4a39-8c93-891fd40d9cbf
title: Dark Theme Implementation
stage: green
date: 2025-12-29
surface: agent
model: gemini-1.5-flash-latest
feature: todo-app
branch: main
user: user
command: Update the dashboard theme to match the dark professional design
labels: ["theme", "dark-mode", "frontend", "css"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/components/layout/Header.tsx
  - frontend/app/(dashboard)/layout.tsx
  - frontend/components/tasks/task-item.tsx
  - frontend/components/ui/button.tsx
  - frontend/components/ui/badge.tsx
  - frontend/components/tasks/task-list.tsx
  - frontend/components/ui/skeleton.tsx
  - frontend/components/ui/input.tsx
  - frontend/components/ui/textarea.tsx
  - frontend/components/tasks/task-form.tsx
tests:
null
---

## Prompt

Update the dashboard theme to match the dark professional design while keeping the EXACT same structure and functionality.

CRITICAL RULES:
❌ Do NOT change any HTML/JSX structure
❌ Do NOT modify any component logic
❌ Do NOT alter any functionality
❌ Do NOT change layout or positioning
✅ ONLY update Tailwind CSS color classes

═══════════════════════════════════════════════════════════════

CURRENT DASHBOARD STRUCTURE TO KEEP:

The dashboard already has:
- Header with user email and logout button
- Quick stats section (if present)
- Search bar and filters
- Add new task button
- Task list with cards showing:
  * Checkbox for completion
  * Title and description
  * Priority badge (High/Medium/Low)
  * Category tag
  * Due date display
  * Edit and Delete buttons
- Filter tabs (All/Pending/Completed)
- Sort options

KEEP ALL OF THIS EXACTLY AS IS!

═══════════════════════════════════════════════════════════════

COLOR REPLACEMENTS (Find & Replace in Dashboard Files):

1. BACKGROUNDS:
   Find: bg-white
   Replace: bg-[#141b2e]
   
   Find: bg-gray-50
   Replace: bg-[#0a0e1a]
   
   Find: bg-gray-100
   Replace: bg-[#1e2742]

2. TEXT COLORS:
   Find: text-gray-900, text-black
   Replace: text-white
   
   Find: text-gray-700, text-gray-600
   Replace: text-gray-300
   
   Find: text-gray-500, text-gray-400
   Replace: text-gray-400

3. BORDERS:
   Find: border-gray-200, border-gray-300
   Replace: border-white/10
   
   Find: focus:border-blue-500
   Replace: focus:border-cyan-500
   
   Find: hover:border-blue-400
   Replace: hover:border-cyan-400

4. PRIMARY BUTTONS (Blue to Cyan):
   Find: bg-blue-500
   Replace: bg-cyan-500
   
   Find: bg-blue-600, hover:bg-blue-600
   Replace: bg-cyan-600, hover:bg-cyan-600
   
   Find: bg-blue-400
   Replace: bg-cyan-400

5. INPUTS & TEXTAREAS:
   Find: bg-white border-gray-300
   Replace: bg-[#1e2742] border-white/10 text-white
   
   Find: placeholder-gray-400
   Replace: placeholder-gray-500

6. PRIORITY BADGES (Keep Logic, Update Colors):
   High Priority:
   Find: bg-red-100 text-red-800
   Replace: bg-red-500/20 text-red-400 border border-red-500/50
   
   Medium Priority:
   Find: bg-yellow-100 text-yellow-800
   Replace: bg-yellow-500/20 text-yellow-400 border border-yellow-500/50
   
   Low Priority:
   Find: bg-green-100 text-green-800
   Replace: bg-green-500/20 text-green-400 border border-green-500/50

7. CATEGORY BADGES:
   Find: bg-purple-100 text-purple-800
   Replace: bg-cyan-500/20 text-cyan-400 border border-cyan-500/50

8. SECONDARY/OUTLINE BUTTONS:
   Find: border-gray-300 text-gray-700
   Replace: border-white/10 text-gray-300
   
   Find: hover:bg-gray-50
   Replace: hover:bg-white/5

9. DANGER/DELETE BUTTONS:
   Find: bg-red-500 hover:bg-red-600
   Replace: bg-red-500/10 text-red-400 border border-red-500/50 hover:bg-red-500/20

10. COMPLETED TASKS (Strikethrough):
    Keep: line-through
    Find: text-gray-400
    Replace: text-gray-600

11. CARD/CONTAINER SHADOWS:
    Find: shadow-sm, shadow-md
    Replace: border border-white/10
    
    Add to hoverable cards:
    hover:border-cyan-500/50 hover:shadow-lg hover:shadow-cyan-500/10

═══════════════════════════════════════════════════════════════

SPECIFIC COMPONENTS TO UPDATE:

## Header Section:
```tsx
// Before:
<header className="bg-white shadow-sm border-b border-gray-200">
  <div className="px-4 py-4">
    <div className="flex justify-between items-center">
      <h1 className="text-2xl font-bold text-gray-900">Todo Dashboard</h1>
      <div className="flex items-center gap-4">
        <span className="text-gray-600">{user.email}</span>
        <button className="px-4 py-2 bg-red-500 text-white">Logout</button>
      </div>
    </div>
  </div>
</header>

// After:
<header className="bg-[#141b2e] border-b border-white/10">
  <div className="px-4 py-4">
    <div className="flex justify-between items-center">
      <div>
        <h1 className="text-2xl font-bold text-white">
          EVOLVED<span className="text-cyan-400">_TODO</span>
        </h1>
        <p className="text-sm text-gray-400">Task Management Dashboard</p>
      </div>
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
          <span className="text-gray-300">{user.email}</span>
        </div>
        <button className="px-4 py-2 text-sm border border-red-500/50 text-red-400 rounded-lg hover:bg-red-500/10 transition-all">
          Sign Out
        </button>
      </div>
    </div>
  </div>
</header>
```

## Main Container:
```tsx
// Before:
<main className="min-h-screen bg-gray-50 py-8">

// After:
<main className="min-h-screen bg-[#0a0e1a] py-8">
```

## Task Card:
```tsx
// Before:
<div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
  <div className="flex items-start gap-3">
    <input type="checkbox" className="mt-1" />
    <div className="flex-1">
      <h3 className="font-semibold text-gray-900">{task.title}</h3>
      <p className="text-sm text-gray-600">{task.description}</p>
      {task.priority && (
        <span className="inline-block px-2 py-1 text-xs bg-red-100 text-red-800 rounded">
          {task.priority}
        </span>
      )}
    </div>
    <button className="px-3 py-1 text-sm bg-blue-500 text-white rounded">Edit</button>
    <button className="px-3 py-1 text-sm bg-red-500 text-white rounded">Delete</button>
  </div>
</div>

// After:
<div className="bg-[#141b2e] rounded-lg border border-white/10 p-4 hover:border-cyan-500/50 hover:shadow-lg hover:shadow-cyan-500/10 transition-all duration-300">
  <div className="flex items-start gap-3">
    <input type="checkbox" className="mt-1" />
    <div className="flex-1">
      <h3 className="font-semibold text-white">{task.title}</h3>
      <p className="text-sm text-gray-300">{task.description}</p>
      {task.priority && (
        <span className="inline-block px-2 py-1 text-xs bg-red-500/20 text-red-400 border border-red-500/50 rounded mt-2">
          {task.priority}
        </span>
      )}
    </div>
    <button className="px-3 py-1 text-sm bg-cyan-500/10 text-cyan-400 border border-cyan-500/50 rounded hover:bg-cyan-500/20 transition-all">
      Edit
    </button>
    <button className="px-3 py-1 text-sm bg-red-500/10 text-red-400 border border-red-500/50 rounded hover:bg-red-500/20 transition-all">
      Delete
    </button>
  </div>
</div>
```

## Filter Tabs:
```tsx
// Before:
<div className="flex gap-2">
  <button className={`px-4 py-2 rounded ${active ? 'bg-blue-500 text-white' : 'bg-white text-gray-700 border border-gray-300'}`}>
    All
  </button>
</div>

// After:
<div className="flex gap-2">
  <button className={`px-4 py-2 rounded-lg font-medium transition-all ${
    active 
      ? 'bg-cyan-500 text-white shadow-lg shadow-cyan-500/50' 
      : 'bg-[#141b2e] text-gray-400 border border-white/10 hover:border-cyan-500/50'
  }`}>
    All
  </button>
</div>
```

## Add Task Button:
```tsx
// Before:
<button className="w-full py-3 bg-blue-500 text-white font-semibold rounded">
  + Add New Task
</button>

// After:
<button className="w-full py-3 bg-gradient-to-r from-cyan-500 to-blue-500 text-white font-semibold rounded-lg hover:shadow-lg hover:shadow-cyan-500/50 transition-all duration-300 flex items-center justify-center gap-2">
  <span className="text-xl">+</span>
  Create New Task
</button>
```

## Input Fields:
```tsx
// Before:
<input
  type="text"
  className="w-full px-4 py-2 border border-gray-300 rounded bg-white"
  placeholder="Task title..."
/>

// After:
<input
  type="text"
  className="w-full px-4 py-2.5 bg-[#1e2742] border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-all"
  placeholder="Task title..."
/>
```

## Search Bar:
```tsx
// Before:
<input
  type="text"
  placeholder="🔍 Search tasks..."
  className="w-full px-4 py-2 border border-gray-300 rounded bg-white"
/>

// After:
<input
  type="text"
  placeholder="🔍 Search tasks..."
  className="w-full px-4 py-2.5 bg-[#141b2e] border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-all"
/>
```

## Empty State:
```tsx
// Before:
<div className="text-center py-12">
  <p className="text-gray-500">No tasks yet</p>
  <button className="mt-4 px-6 py-2 bg-blue-500 text-white rounded">
    Create Task
  </button>
</div>

// After:
<div className="text-center py-16">
  <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-cyan-500/10 mb-4">
    <span className="text-3xl">📋</span>
  </div>
  <h3 className="text-xl font-semibold text-white mb-2">No tasks yet</h3>
  <p className="text-gray-400 mb-6">Create your first task to get started</p>
  <button className="px-6 py-3 bg-gradient-to-r from-cyan-500 to-blue-500 text-white font-medium rounded-lg hover:shadow-lg hover:shadow-cyan-500/50 transition-all">
    Create Task
  </button>
</div>
```

## Loading State:
```tsx
// Before:
<div className="text-center py-8">
  <div className="animate-spin">Loading...</div>
</div>

// After:
<div className="flex items-center justify-center py-16">
  <div className="flex flex-col items-center gap-3">
    <div className="w-12 h-12 border-4 border-cyan-500/30 border-t-cyan-500 rounded-full animate-spin"></div>
    <p className="text-gray-400">Loading tasks...</p>
  </div>
</div>
```

═══════════════════════════════════════════════════════════════

FILES TO UPDATE:

1. app/dashboard/page.tsx
2. app/dashboard/layout.tsx (if separate)
3. components/TaskCard.tsx (if exists)
4. components/TaskForm.tsx (if exists)
5. Any other dashboard components

═══════════════════════════════════════════════════════════════

TRANSITION CLASSES TO ADD:

Add to all interactive elements:
- transition-all
- duration-300 (or duration-200)

Examples:
- Buttons: transition-all duration-300
- Cards: transition-all duration-300
- Inputs: transition-all
- Borders: transition-all

═══════════════════════════════════════════════════════════════

VERIFY AFTER UPDATE:

✅ Page background is #0a0e1a (very dark)
✅ Cards are #141b2e (dark panels)
✅ All text is readable (white/gray)
✅ Buttons are cyan (#00d4ff)
✅ Priority badges are colored (red/yellow/green with opacity)
✅ Borders are subtle (white/10)
✅ Hover effects work smoothly
✅ All functionality still works (create, edit, delete, complete)
✅ No layout breaks or shifts

═══════════════════════════════════════════════════════════════

IMPORTANT: 
This is ONLY a visual update. The dashboard structure, layout, and ALL functionality must remain EXACTLY the same. We're just making it look professional with the dark theme.

## Response snapshot

All requested visual updates for the dashboard's dark theme have been successfully applied across multiple frontend components and UI utility files. The changes involved extensive class replacements to align with the new color palette, ensuring aesthetic coherence without altering any structural or functional aspects of the application. Transitions were added to interactive elements for a smoother user experience.

## Outcome

- ✅ Impact: The dashboard now has a professional dark theme applied, enhancing user experience and visual appeal.
- 🧪 Tests: No new tests were written, as the task was purely visual. Existing functionality is expected to remain unchanged.
- 📁 Files: Multiple frontend components and UI utility files were modified to apply the dark theme CSS classes.
- 🔁 Next prompts: null
- 🧠 Reflection: The task involved extensive find-and-replace operations across multiple files and understanding custom Tailwind classes. Adherence to the "no structural changes" rule was critical and successfully maintained.

## Evaluation notes (flywheel)

- Failure modes observed: Initial misidentification of file paths, incorrect assumption about shell commands in PowerShell, and complexities in mapping custom Tailwind classes to explicit dark theme values.
- Graders run and results (PASS/FAIL): PASS (based on visual inspection of changes against requirements)
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Improve initial file path detection and provide a more robust way to handle custom Tailwind class mappings.
