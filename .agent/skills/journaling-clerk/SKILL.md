---
name: Journaling Clerk
description: ユーザーの日記・ログ・音声入力を受け取り、所定のフォーマットで記録・整形・要約するスキル。
---

# Journaling Clerk

## 1. Purpose
Genesis OSにおける「記憶の永続化」を担当する。ユーザーの思考の断片（Stream）を、検索可能で読みやすい資産（Stock）に変換する。

## 2. Trigger
*   ユーザーが「日記」「ログ」「メモ」と言った時。
*   長文の音声入力テキストが送られてきた時。

## 3. Storage Rule
*   **Path:** `g:\マイドライブ\Genesis_OS\20_Inventory\99_Stream\DailyLog\YYYY\MM\YYYY-MM-DD.md`
    *   *Note:* 月ごとにフォルダを自動作成すること。

## 4. Processing Workflow

### Step 1: Check & Create
対象日のファイルが存在するか確認。なければ新規作成し、H1ヘッダーを入れる。

### Step 2: Sanitization (ケバ取り)
入力テキストからノイズ（フィラー）を除去し、文体を統一する。
*   **Remove:** 「あー」「えっと」「なんか」「あのー」
*   **Format:** ユーザーの口調に合わせる（基本は「です・ます」）。
*   **Prohibition:** 意味を変える要約はしない。あくまで「読みやすくする」だけ。

### Step 3: Append
整形後のテキストを、タイムスタンプ `## HH:MM` と共に末尾に追記する。

### Step 4: Feedback
追記した内容をチャット欄にも表示し、ユーザーに確認を求める。

### Step 5: Daily Summary (Optional)
ユーザーが「今日は終わり」と言った場合、その日の内容を3行で要約し、`## 🤖 AI Summary` セクションとして末尾に追記する。
