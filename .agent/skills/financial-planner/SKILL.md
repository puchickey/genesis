---
name: Financial Planner
description: ユーザーの財務状況（資産・収支）を分析し、J-Curve戦略に基づいた予算管理やROI試算を行うスキル。
---

# Financial Planner (v2.0: Split Architecture)

## 🚦 ROUTER
This file only handles the **Initial Trigger**.
Do NOT give financial advice yet. Follow the procedure below.

### 1. Trigger
*   User says "お金", "予算", "買う", "家賃", "節約".
*   User asks for permission to purchase something.

### 2. Immediate Action
**You MUST load the following procedure file first:**
> `view_file g:\マイドライブ\Genesis_OS\.agent\skills\financial-planner\procedures\01_STRATEGY_AUDIT.md`

**DO NOT** say "Yes/No".
**DO NOT** calculate ROI yet.
First, load the strategy file above to confirm the user's current valid strategy (J-Curve Phase 1).
