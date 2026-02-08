# Procedure 03: The Incubator (Forced Rest)

**Objective:**
Drop the problem completely. Let the unconscious mind work.
Enforce a **Time Lock** to prevent "fake resting".

## 🛌 Logic Flow

### 1. Check Timestamp (The Gatekeeper)
*   **Action:** Check the timestamp of the `DailyLog` or the last commit.
*   **Question:** Has enough time passed since Mastication?
    *   *Rule:* If Date == Today -> **REJECT**. (Unless manually overridden).
    *   *Rule:* If Date != Today -> **PASS**.

### 2. The Rejection (If Date == Today)
*   **AI Message:** "It is too soon. You have not slept yet. The idea will not come."
*   **Command:** "Go watch a movie. Go to sleep. I will not secure any ideas now."
*   **Action:** End Session.

### 3. The Activation (If Date != Today)
*   **AI Message:** "Welcome back. Did you have a good sleep? Did anything pop up?"
*   **Transition:** If user says "Yes, I have an idea" -> Load `04_BIRTH.md`.
