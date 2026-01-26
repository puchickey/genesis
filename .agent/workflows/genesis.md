---
description: Genesis OS Initialization & Synchronization Routine
---

# Genesis OS Bootstrap

This workflow standardizes the initialization process for Genesis OS. It ensures that the AI is fully synchronized with the user's context and system state.

## 1. System Synchronization
Run the auto-sync script to ensure local changes are pushed to the remote repository.

// turbo
python genesis_auto_sync.py

## 2. Load System Identity
Read the core instruction file to establish the AI's role and behavior protocols.

- Load context from: `G:\マイドライブ\Genesis_OS\00_SYSTEM\CORE\GENESIS_AI_INSTRUCTION.md`

## 3. Load User Context
Read the user profile and life plan to understand current constraints and long-term goals.

- Load context from: `G:\マイドライブ\Genesis_OS\00_SYSTEM\CORE\user_profile.md`
- Load context from: `G:\マイドライブ\Genesis_OS\00_SYSTEM\CORE\LIFE_PLAN_CORE.md`

## 4. Check Current Status
Read the active tasks and current status to identify immediate priorities.

- Load context from: `G:\マイドライブ\Genesis_OS\00_SYSTEM\CORE\current_status.md`
- Load context from: `G:\マイドライブ\Genesis_OS\00_SYSTEM\CORE\active_tasks.md`

## 5. Report Ready State
Summarize the loaded context and ask for the next directive based on `active_tasks.md`.
