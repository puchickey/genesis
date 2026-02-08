---
name: young-method
description: "James Webb Young's A Technique for Producing Ideas. A 5-step protocol to systematically generate ideas by combining existing elements. Use this when the user wants to brainstorm, generate ideas, or is stuck."
---

# Young Method (Idea Generator)

## 🚦 ROUTER
This file only handles the **Phase Identification**.
Ask the user (or infer from context) which phase they are in, then load the procedure.

### 1. Phase Identification

| Phase | Keyword / Context | Action |
| :--- | :--- | :--- |
| **1. Gathering** | "素材集め", "メモ", "Collect" | `procedures/01_GATHERING.md` |
| **2. Masticating** | "アイデア出し", "組み合わせ", "Thinking" | `procedures/02_MASTICATING.md` |
| **3. Incubating** | "寝る", "休憩", "Stuck", "疲れた" | `procedures/03_INCUBATING.md` |
| **4. Birth** | "わかった！", "Eureka", "ひらめいた" | `procedures/04_BIRTH.md` |
| **5. Shaping** | "検証", "これでいい？", "Criticism" | `procedures/05_SHAPING.md` |

### 2. Execution
**You MUST load the corresponding procedure file.**
Do NOT attempt to run the phase yourself. The logic is complex and separated.
