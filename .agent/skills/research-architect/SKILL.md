---
name: Research Architect
description: 代行調査プロンプト作成スキル。ユーザーの「真の目的（Decision）」を深掘りし、高精度な外部検索プロンプトを生成する。
---

# Research Architect (v2.0: Split Architecture)

## 🚦 ROUTER
This file only handles the **Initial Trigger**.
Do NOT generate a prompt yet. Follow the procedure below.

### 1. Trigger
*   User says "調べて", "リサーチして", "検索したい".
*   User asks for a prompt for Perplexity/Genspark.

### 2. Immediate Action
**You MUST load the following procedure file first:**
> `view_file g:\マイドライブ\Genesis_OS\.agent\skills\research-architect\procedures\01_GOAL_CLARIFICATION.md`

**DO NOT** write the prompt immediately.
**DO NOT** assume the query is perfect.
First, load the validation file to clarify *why* this research is needed and check for bias.
