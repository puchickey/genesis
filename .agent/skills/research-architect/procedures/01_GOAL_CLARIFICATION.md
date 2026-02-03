# Procedure 01: Goal Clarification (Deep Dive)

**Objective:**
Before writing a search prompt, you MUST clarify the user's true intent and context.
Do not assume. Do not generalize. Ask until the "Purpose" is crystal clear.

## 🔍 Logic Flow

### 1. The Deep Dive Interview
Ask the following questions to the user (or clarify from context):
*   **Context:** Why now? What happened? (e.g., "I just saw a news article about X", "I'm thinking of quitting my job")
*   **Decision:** What decision depends on this research? (e.g., "If salaries are low, I won't move", "If it's buggy, I won't buy it")
*   **Definition of 'Good':** What kind of answer is 'satisfying'? (e.g., "I need raw CSV data", "I need 3 credible URLs", "I just want a summary")

### 2. Bias Check
*   **Self-Correction:** Are we assuming a specific result? (e.g., "Find reasons why X is bad" -> "Find pros and cons of X objectively")
*   **Correction:** If the user's request is biased ("Find why Python sucks"), suggest a balanced approach ("Compare Python's limitations vs other languages").

### 3. Transition
Once the goal is clear (and only then), load the next procedure:
> `view_file g:\マイドライブ\Genesis_OS\.agent\skills\research-architect\procedures\02_PROMPT_GENERATION.md`
