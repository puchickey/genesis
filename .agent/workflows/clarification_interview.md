# Workflow: Clarification Interview (The Mirror)

**Objective:**
Extract latent thoughts, values, and experiences from the User (Source) and record them into the `DailyLog` for future retrieval.

**Trigger:**
*   User request: "Ask me anything."
*   System initiative: "I need to clarify this part of your profile."
*   Dead wind: When idea generation stalls.

## Protocol

### 1. The Question (Input)
*   AI asks **ONE** specific, deep question.
*   **Categories:**
    *   **Past:** "Most absorbed moment in childhood?"
    *   **Emotion:** "What made you most angry recently?"
    *   **Obsession:** "What detail do you care about that nobody else does?"
    *   **Constraint:** "What would you do if money was infinite?"

### 2. The Answer (Raw Material)
*   User answers freely in the chat.

### 3. The Distillation (Output)
*   AI summarizes the answer and appends it to the **Current DailyLog**.
*   **Format:**
    ```markdown
    ### [HH:MM] Clarification Interview: {Topic} #{Tag}
    *   **Q:** {Brief Question}
    *   **A:** {User's Answer Summary}
    *   **Insight:** {Analysis of what this means for strategy}
    ```

### 4. Tagging Rules (Search Keys)
Use these tags to allow `grep_search` retrieval later:
*   `#UserProp`: Personality, history, deep values.
*   `#IdeaSeed`: Specific business or project ideas.
*   `#Obsession`: Strong emotional triggers (Love/Hate).
*   `#Asset`: New skills, connections, or resources identified.
