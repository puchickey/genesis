---
name: jules-coordinator
description: Antigravityから非同期作業用エージェントであるJules（GitHub経由）に重いコーディングタスクを投げるスキル
---
# Jules Coordinator Skill

## 🎯 Purpose
ローカルでの即時作業ではなく、数時間かかるような大規模リファクタリング、カオスなデータの構造化、あるいは全く新しいツールのスクラッチ開発などを、Jules (Googleの非同期Git Agent) に依頼して並列処理する。

## ⚠️ 前提条件
- **対象ファイルがGit追跡対象であること**（Git追跡外のローカルファイル操作はJulesでは不可能）
- 環境変数 `JULES_API_KEY` が設定済みであること
- ヘルパースクリプト `.agent/scripts/jules_api.py` が存在すること

## 🛠️ Execution Protocol

### 1. Lock (排他制御)
`00_SYSTEM/CORE/agent_registry.md` に以下のフォーマットでタスクを登録する。
`- [Running] Task-[ランダム3桁]: [作業内容] (Assignee: Jules) Target: [GitHub Repo名]`

### 2. Blueprint Generation (指示書作成)
目的のGitHubリポジトリの対象ブランチ内に、指示書となるMarkdownファイル（例: `JULES_TASK.md`）を作成する。
そこに以下の内容を含める:
- **Context**: 業務背景
- **Goal**: Julesが達成すべき最終ゴール
- **Output**: 完了後の成果物（PRの説明、結果レポートの出力先）
- **Constraints**: 変更禁止ファイル、作業制限

### 3. Dispatch (API経由でセッション作成)

**重要: CLIではなくREST APIを使用する。** これにより手動の「Publish PR」が不要になる。

#### 方法A: jules_api.py ヘルパーを使用（推奨）
```bash
$env:JULES_API_KEY = "YOUR_KEY"
python .agent/scripts/jules_api.py create --repo puchickey/genesis --file JULES_TASK.md --title "Task-XXX: 作業内容"
```

#### 方法B: Antigravityが直接APIを呼ぶ（run_command経由）
```powershell
$headers = @{ "x-goog-api-key" = $env:JULES_API_KEY }
$body = @{
    prompt = (Get-Content JULES_TASK.md -Raw)
    title = "Task-XXX: 作業内容"
    sourceContext = @{
        source = "sources/github/puchickey/genesis"
        githubRepoContext = @{ startingBranch = "master" }
    }
    automationMode = "AUTO_CREATE_PR"
    requirePlanApproval = $false
} | ConvertTo-Json -Depth 5
Invoke-RestMethod -Uri "https://jules.googleapis.com/v1alpha/sessions" -Headers $headers -Method Post -Body $body -ContentType "application/json"
```

### 4. 指示書のプッシュ（オプション）
指示書をGitHubにもプッシュして記録を残す場合:
```bash
git add JULES_TASK.md
git commit -m "chore: delegate task [Task-ID] to Jules"
git push origin master
```

### 5. Report (ユーザーへの連絡)
「Julesにタスク [Task-ID] をAPI経由で投入しました（AUTO_CREATE_PR有効）。PRが自動公開されるのでCoordinatorが検知します」とユーザーに報告する。

## 📋 API パラメータリファレンス

| パラメータ | 値 | 説明 |
|-----------|-----|------|
| `automationMode` | `AUTO_CREATE_PR` | 完了時に自動でPRを公開 |
| `requirePlanApproval` | `false` | プラン承認ステップをスキップ |
| `source` | `sources/github/{owner}/{repo}` | 対象リポジトリ |
| `startingBranch` | `master` / `main` | 開始ブランチ |

## 📦 利用可能リポジトリ（source名）

| リポジトリ | source | デフォルトブランチ |
|-----------|--------|------------------|
| puchickey/genesis | `sources/github/puchickey/genesis` | master |
| puchickey/mono_log | `sources/github/puchickey/mono_log` | main |
| puchickey/cos_tok | `sources/github/puchickey/cos_tok` | — |
| puchickey/kindle-screenshot-to-pdf | `sources/github/puchickey/kindle-screenshot-to-pdf` | main |
