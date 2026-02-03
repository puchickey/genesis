# Procedure 01: Git Status Check

**Objective:**
Identify pending changes in the Genesis OS repository to determine if a commit is necessary.

## 🔍 Logic Flow

### 1. Execute Command
*   **Action:** Run `git status`
*   **Wait:** 2 seconds for output.

### 2. Analyze Output
*   **Case A: "nothing to commit, working tree clean"**
    *   **Decision:** STOP. No further action needed.
    *   **Response:** "変更はありません (Clean)."
*   **Case B: "Changes not staged" or "Untracked files"**
    *   **Decision:** Proceed to **[Loading Procedure 02]**.
    *   **Context:** Note the filenames. (e.g., `SKILL.md` modified, `new_file.md` untracked).

### 3. Transition
If Case B (Changes exist), you MUST load the next file:
> `view_file g:\マイドライブ\Genesis_OS\.agent\skills\git-operator\procedures\02_COMMIT_EXECUTION.md`
