---
name: Git Operator
description: Genesis OSのファイル変更履歴をGitで管理するスキル。コミットメッセージの標準化と、Google Drive特有のエラーハンドリングを行う。
---

# Git Operator

## 1. Purpose
Genesis OSの状態（State）をスナップショットとして保存し、いつでも過去の状態に戻れるようにする。

## 2. Trigger
*   セッション終了時（「今日は終わり」）。
*   重要なマイルストーン達成時（スキル作成完了、プロジェクト定義完了など）。
*   ユーザーが `/git` や `/save` コマンドを実行した時。

## 3. Protocol

### Step 1: Command Execution
以下のコマンドを順次実行する。
```powershell
git add .
git commit -m "feat(category): Summary" -m "- Detail 1"
```

### Step 2: Commit Message Standard
「何をしたか」だけでなく「なぜしたか」がわかるように書く。
*   **Prefix:**
    *   `feat`: 新機能・新ファイル (New Skill, New Doc)
    *   `update`: 内容更新 (Log, Status Update)
    *   `fix`: 修正 (Typos, Bug fix)
    *   `docs`: ドキュメント整理
*   **Format:** `prefix(scope): Subject`

### Step 3: Error Handling
Google Drive同期中のファイルロックにより `git commit` が失敗する場合がある。
*   **Action:** 1回だけリトライし、それでもダメなら「ロック中のため保存をスキップします」と報告して終了する（深追いしない）。
