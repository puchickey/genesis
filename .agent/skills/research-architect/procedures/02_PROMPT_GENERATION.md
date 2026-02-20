# Procedure 02: Prompt Generation

**Objective:**
Construct a high-precision prompt for an External Research AI (Perplexity/Genspark) based on the clarified goal.

## 📝 Logic Flow

### 1. Variables
Use the variables identified in Procedure 01:
*   `{Context}`: The user's situation.
*   `{Decision}`: What needs to be decided.
*   `{Target_Data}`: The specific form of answer needed (Stats, case studies, etc.).

### 2. The Verification Template
Use this template to generate the output:
```markdown
You are a Data Analyst. Investigation required.

## Objective
The user needs to decide: **"{Decision}"**.
To support this, please research the following topic objectively.

## Context
*   Situation: {Context}
*   Constraint: No generalities. Provide specific data/sources.

## Investigation Points
1.  **Fact Check:** Validate the premise. Is it true?
2.  **Data Extraction:** Find statistics/updates regarding {Target_Data}.
3.  **Counter-Evidence:** Find data that *contradicts* the user's initial assumption (Bias Check).

## Output Format
*   Verdict: [Go / No Go / Unclear]
*   Evidence Table: [Source URL | Main/Finding | Date]
*   **Language: Output the entire report in Japanese (日本語).**
```

### 3. Execution
*   Output the completed prompt in a code block.
*   Instruct the user to copy-paste it to Perplexity/Genspark.
