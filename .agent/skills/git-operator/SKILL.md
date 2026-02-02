---
name: Git Operator
description: Genesis OSのファイル変更履歴をGitで管理するスキル。コミットメッセージの標準化と、Google Drive特有のエラーハンドリングを行う。
---

# Git Operator

## 1. Purpose
Genesis OSの状態（State）をスナップショットとして保存し、いつでも過去の状態に戻れるようにする。

## 2. Trigger
*   **Atomic Feature (推奨):** 機能単位（スキル追加、ドキュメント改訂、設定変更）の作業が完了した時。
    *   *Reason:* 「タスク消化」ではなく「システム進化」の履歴を残すため。
*   **Session End (Backup):** セッション終了時のバックアップ。
*   **Manual:** ユーザー指示時。

## 3. Protocol

### Step 1: Command Execution
以下のコマンドを順次実行する。
```powershell
git add .
git commit -m "feat(category): Summary" -m "- Detail 1"
```

### Step 2: Commit Message Standard
**必ず「日本語 (Japanese)」で記述すること。**
「何をしたか」だけでなく「なぜしたか」がわかるように書く。

*   **Prefix:**
    *   `feat`: 新機能・新ファイル (New Skill, New Doc)
    *   `update`: 内容更新 (Log, Status Update)
    *   `fix`: 修正 (Typos, Bug fix)
    *   `docs`: ドキュメント整理
*   **Format:** `prefix(scope): 日本語の要約`
    *   *Example:* `update(finance): 2026年の予算案をJカーブ戦略に基づいて修正`

### Step 3: Bulk Commit Rule (まとめ保存時)
朝のアーカイブ処理など、複数の異なる変更をまとめてコミットする場合は、`-m` オプションを複数回使用して詳細を記録する。
*   `git commit -m "log(daily): 1月30日の活動アーカイブ" -m "- 予算案の修正 (Investment削減)" -m "- プロフィールの更新 (住居要件の追加)"`

### Step 3: Error Handling
Google Drive同期中のファイルロックにより `git commit` が失敗する場合がある。
*   **Action:** 1回だけリトライし、それでもダメなら「ロック中のため保存をスキップします」と報告して終了する（深追いしない）。

## 4. Reporting (History)
ユーザーが「更新履歴を見たい」「最近何をした？」と聞いた時の対応。

*   **Command:** `git log --oneline --graph --all -n 10 --date=short --pretty=format:"%h %cd %s"`
*   **Action:** 直近のコミットログを取得し、"What changed" を人間にわかる言葉で要約して回答する。

