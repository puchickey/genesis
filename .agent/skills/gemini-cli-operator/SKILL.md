---
name: gemini-cli-operator
description: AntigravityからGemini CLIにバックグラウンドのローカル重処理を委譲するスキル
---

# Gemini CLI Operator Skill

## 🎯 Purpose
ローカルでの大規模なファイル集計、コードリファクタリング、複数サイトのWeb検索など、Antigravity（自身）のセッションやトークンを長く拘束する作業を裏側の「Gemini CLI」に任せて並列化するためのスキル。

## 🛠️ Execution Protocol

1. **Lock (排他制御)**
   `00_SYSTEM/CORE/agent_registry.md` を確認し、競合がないことを確かめた上で、以下のフォーマットでタスクを登録する。
   `- [Running] Task-[ランダム3桁]: [作業内容] (Assignee: Gemini CLI) Target: [影響するファイルなど]`

2. **Blueprint Generation (指示書作成)**
   `00_SYSTEM/CORE/outbox/task_[ID]_gemini.md` というMarkdownファイルを作成し、以下の内容を記載する。
   *   **Context**: 背景とタスクの目的
   *   **Task**: 具体的な作業内容（Gemini CLIが自己完結できるように詳細に記述する）
   *   **Constraints**: 触ってはいけないファイルなどの制約
   *   **Output**: 完了後、必ず `00_SYSTEM/CORE/inbox/report_[ID]_gemini.md` に結果を出力すること

3. **Dispatch (実行のトリガー)**
   Phase 3で構築するCoordinator（監視スクリプト）が稼働している場合は、指示書の投下で自動実行される。
   ※即時かつ強制的に実行させる場合は、以下のコマンドを `run_command` ツールの非同期機能（`WaitMsBeforeAsync` 指定）を用いて実行する。
   `gemini --prompt "00_SYSTEM/CORE/outbox/task_[ID]_gemini.md に記載されたタスクを熟読して実行し、指定されたフォーマットでinboxにファイルを作成して任務を完了せよ。"`

4. **Report (ユーザーへの連絡)**
   ユーザーに「Gemini CLIへタスク [Task-ID] を委譲し、裏で作業を開始させました」と報告する。
