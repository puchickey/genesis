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
Read the active tasks, current status, and multi-agent registry to identify priorities and background processes.

- Load context from: `G:\マイドライブ\Genesis_OS\00_SYSTEM\CORE\current_status.md`
- Load context from: `G:\マイドライブ\Genesis_OS\00_SYSTEM\CORE\active_tasks.md`
- Load context from: `G:\マイドライブ\Genesis_OS\00_SYSTEM\CORE\agent_registry.md`

## 5. Check Agent Inbox (最優先)
Check if there are any unread reports from external agents (Jules, Gemini CLI).
If reports exist, **summarize and report them to the user BEFORE anything else.**

// turbo-all
Get-ChildItem -Path "G:\マイドライブ\Genesis_OS\00_SYSTEM\CORE\inbox" -Filter "*.md" | Select-Object -First 5

## 6. Report Ready State
Summarize the loaded context, report any completed background tasks found in the inbox, and ask for the next directive based on `active_tasks.md`.

---

## Mid-Session Rule: タスク完了時の inbox 確認
**Trigger:** 会話中に何かひとつの話題・タスクが完了し、「次は何をしますか？」と聞く直前。
**Action:** `inbox/` を確認し、新着レポートがあれば「そういえば、裏で走らせていた作業が完了していました」と自然に報告する。
**目的:** ユーザーに確認の手間をかけず、会話のテンポも崩さない。
