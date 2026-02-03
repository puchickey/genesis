# Procedure 02: Commit Execution

**Objective:**
Stage all changes and commit them with a high-quality, standardized Japanese message.

## 📝 Logic Flow

### 1. Message Generation
Analyze the changed files from `git status` (Procedure 01) and formulate the message.
*   **Format:** `prefix(scope): Standardized Japanese Summary`
*   **Prefix Rules:**
    *   `feat`: New features/files
    *   `update`: Updates to existing logic/docs
    *   `fix`: Bug fixes
    *   `docs`: Documentation only
    *   `refactor`: Code restructuring (like this)
*   **Bulk Rule:** If multiple distinct changes exist, use multiple `-m` lines.
    *   *Example:* `git commit -m "update(log): Day 30 journal" -m "- Added offline ideas" -m "- Fixed typos"`

### 2. Execution
*   **Command:** `git add .` (Stage all)
*   **Command:** `git commit -m "..."` (Commit)
    *   *Constraint:* If error occurs (lock file), retry ONCE. If fails again, report error.

### 3. Feedback
*   Once done, verify with `git log -1 --oneline` and report success to the user.
*   **Task Complete.** No further loading.
