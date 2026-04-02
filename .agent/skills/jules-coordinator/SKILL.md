---
name: jules-coordinator
description: Antigravityから非同期作業用エージェントであるJules（GitHub経由）に重いコーディングタスクを投げるスキル
---
# Jules Coordinator Skill

## 🎯 Purpose
ローカルでの即時作業ではなく、数時間かかるような大規模リファクタリング、カオスなデータの構造化、あるいは全く新しいツールのスクラッチ開発などを、Jules (Googleの非同期Git Agent) に依頼して並列処理する。

## 🛠️ Execution Protocol
1. **Lock (排他制御)**
   `00_SYSTEM/CORE/agent_registry.md` に以下のフォーマットでタスクを登録する。
   `- [Running] Task-[ランダム3桁]: [作業内容] (Assignee: Jules) Target: [GitHub Repo名]`

2. **Blueprint Generation (指示書作成)**
   目的のGitHubリポジトリ（Jules連携が設定されているリポジトリ）の対象ブランチ内に、指示書となるMarkdownファイル（例: `JULES_TASK.md` や `ProjectB_data/README.md` など）を直接作成するか、追記する。
   そこに以下の内容を含める。
    - **Context**: 業務背景
    - **Goal**: Julesが達成すべき最終ゴール
    - **Output**: 完了後、必ず結果レポートをIssue等にまとめ、コード修正はPull Requestとして提出すること
    
3. **Dispatch (Githubプッシュ)**
   `run_command` ツールの同期機能を利用して、以下のGitコマンドを実行し、Julesを自動的に目覚めさせる。
   `git add .`
   `git commit -m "chore: delegate task [Task-ID] to Jules"`
   `git push origin main`
   
4. **Report (ユーザーへの連絡)**
   「Julesにタスク [Task-ID] を投げ、GitHubにプッシュしました。数時間後にPRが上がってくるまで、ローカルで別のタスクを進められます」とユーザーに報告する。
