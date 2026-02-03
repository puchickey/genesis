---
name: Journaling Clerk
description: ユーザーの日記・ログ・音声入力を受け取り、所定のフォーマットで記録・整形・要約するスキル。
---

# Journaling Clerk (v2.0: Split Architecture)

## 🚦 ROUTER
This file only handles the **Initial Trigger**.
Do NOT attempt to write the log yet. Follow the procedure below.

### 1. Trigger
*   User says "日記", "ログ", "メモ".
*   User inputs long text/voice transcript for recording.

### 2. Immediate Action
**You MUST load the following procedure file first:**
> `view_file g:\マイドライブ\Genesis_OS\.agent\skills\journaling-clerk\procedures\01_ARCHIVE_TRIGGER.md`

**DO NOT** write the log, **DO NOT** check the date, **DO NOT** summarize.
Just load the file above. It contains the instructions for Step 1.
