# vibe-kanban

Visual kanban board for orchestrating parallel AI coding agents. Plan tasks, dispatch to coding agents, track progress, review results.

## Triggers

- vibe kanban
- coding board  
- parallel coding
- agent board
- kanban coding
- ai orchestration

## Description

A modern, visual kanban board designed for coordinating multiple AI coding agents (Claude Code, Cursor, Copilot). Inspired by vibekanban.com (BloopAI).

Features:
- 📝 Plan → 🤖 Coding → 👁️ Review → ✅ Done workflow
- Task cards with priority, agents, and timers
- Drag & drop between columns
- Real-time statistics and progress tracking
- Agent dispatch integration
- Local storage persistence

## Usage

```bash
# Open the kanban board
openclaw canvas present skills/vibe-kanban/index.html

# Or access via file
open /Users/bond/.openclaw/workspace/skills/vibe-kanban/index.html
```

## Files

- `index.html` - Main kanban board web app
- `scripts/dispatch.sh` - Agent dispatch script
- `SKILL.md` - This file

## Agent Integration

Supports dispatching tasks to:
- Claude Code (OpenClaw)
- Cursor CLI
- GitHub Copilot CLI
- Custom agents