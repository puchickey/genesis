---
name: Decision Architect
description: 複雑な意思決定を行う際、感情や直感ではなく、定義された「評価マトリクス（Valuation Matrix）」に基づいて論理的な評決（Verdict）を下すスキル。
---

# Decision Architect (v2.0: Split Architecture)

## 🚦 ROUTER
This file only handles the **Initial Trigger**.
Do NOT give a verdict yet. Follow the procedure below.

### 1. Trigger
*   User says "迷っている", "どっちがいい？", "決めて".
*   User presents a "Side A vs Side B" dilemma.

### 2. Immediate Action
**You MUST load the following procedure file first:**
> `view_file g:\マイドライブ\Genesis_OS\.agent\skills\decision-architect\procedures\01_VARIABLE_ID.md`

**DO NOT** say "Option A is better".
**DO NOT** start scoring.
First, load the variable ID file to determine *what criteria* matter for this decision.
