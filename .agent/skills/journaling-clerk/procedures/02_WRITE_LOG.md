# Procedure 02: Write Log

**Objective:**
Record the user's input into the Daily Log file with proper formatting.

## 📝 Logic Flow

### 1. File Preparation
*   **Path:** `g:\マイドライブ\Genesis_OS\20_Inventory\99_Stream\DailyLog\YYYY\MM\YYYY-MM-DD.md`
*   **Action:**
    *   If file does not exist -> Create it with `# Daily Log: YYYY-MM-DD (Day)` header.
    *   If exists -> Append to the end.

### 2. Sanitization (Input Cleaning)
*   **Input:** User's raw text or voice transcript.
*   **Action:** Remove "Filler Words" (Ah, Umm, Eto...) to improve readability.
    *   *Rule:* Do NOT summarize or change the meaning. Only clean the noise.
    *   *Style:* Use "Desu/Masu" tone (Unless instructed otherwise).

### 3. Appending
*   **Format:**
    ```markdown
    ### [HH:MM] {Topic Title}
    *   **Context:** {Brief context}
    *   **Content:** {Main content, bullet points}
    ```
*   **AI Commentary:**
    *   Attached `## 🤖 Genesis Commentary` if the user asks for advice or if there is a critical insight.

### 4. Feedback
*   **Action:** Show the result to the user.
*   **Command:** NO further file loading. The task ends here.
