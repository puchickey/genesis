---
name: Git Operator
description: Genesis OSのファイル変更履歴をGitで管理するスキル。変更の有無を確認し、標準化されたメッセージで記録する。
---

# Git Operator (v2.0: Split Architecture)

## 🚦 ROUTER
This file only handles the **Initial Trigger**.
Do NOT attempt to run commit commands yet. Follow the procedure below.

### 1. Trigger
*   User says "保存", "コミット", "Git", "更新".
*   System requires an Archive/Backup (e.g., Journey Clerk Step 1).

### 2. Immediate Action
**You MUST load the following procedure file first:**
> `view_file g:\マイドライブ\Genesis_OS\.agent\skills\git-operator\procedures\01_STATUS_CHECK.md`

**DO NOT** run `git add/commit`.
**DO NOT** assume changes exist.
Just load the status check file above. It determines the next step.
