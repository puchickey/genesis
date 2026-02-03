# Procedure 01: Archive Trigger

**Objective:**
Ensure that the "Previous Session" is archived (Committed) before starting a new Daily Log.
This prevents the new log from being mixed with yesterday's changes in a single commit.

## 🔍 Logic Flow

### 1. Check Date
*   Target File: `g:\マイドライブ\Genesis_OS\20_Inventory\99_Stream\DailyLog\YYYY\MM\YYYY-MM-DD.md`
*   **Question:** Does this file ALREADY exist?
    *   **YES:** -> Skip to **[Loading Procedure 02]**. (Do not commit, just append).
    *   **NO:** -> Proceed to **Step 2 (Archive Check)**.

### 2. Archive Check (Git)
*   **Action:** execution `git status`
*   **Question:** Are there uncommitted changes?
    *   **NO:** -> Skip to **[Loading Procedure 02]**.
    *   **YES:** -> **STOP.** You must commit them now.

### 3. Execution (The Archive Commit)
*   **Action:** Call `Git Operator` (or run git command).
    *   *Message:* "log: archive previous session (YYYY-MM-DD)"
    *   *Constraint:* Do NOT include today's new log file in this commit. Only commit the *existing* changes.

---

## 🏁 Transition
After the commit is done (or if skipped), you MUST load the next file:
> `view_file g:\マイドライブ\Genesis_OS\.agent\skills\journaling-clerk\procedures\02_WRITE_LOG.md`
