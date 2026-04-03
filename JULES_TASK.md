# JULES_TASK: リポジトリクリーンアップ（Task-005）

## Context
前回の調査レポート（`00_SYSTEM/CORE/inbox/jules_report_repo_analysis.md`）の「設計上の懸念点・改善提案」セクションに基づき、リポジトリの整理を行う。
Genesis OS は Google Drive 上で運用されており、GitHub（`puchickey/genesis`）にはLayer A（公開可能なインフラ）のみがプッシュされる。

## Goal
以下の3つのクリーンアップを実行する。**コードの変更（ロジックの修正）は行わず、ファイルの移動・削除・.gitignore更新のみ**を行うこと。

### 1. ルートディレクトリの一時ファイル削除
以下のファイルをリポジトリのルートから**削除**する（`git rm`）:
- `find_large.py`
- `find_loose.py`
- `genesis_auto_sync.py`（※ `00_SYSTEM/Automation/genesis_auto_sync.py` に同等品があるため重複）
- `objects.txt`
- `pack.txt`
- `sync_log.txt`
- `tree.txt`（存在する場合）
- `tree_clean.txt`（存在する場合）
- `iroha_api.json`
- `iroha_articles.html`
- `iroha_page.html`
- `iroha_page2.html`

### 2. テストスクリプトの分離
`.agent/scripts/` 内のテスト用スクリプトを `.agent/scripts/tests/` ディレクトリに移動する:
- `test_antigravity_cdp.py` → `.agent/scripts/tests/`
- `test_auto_type.py` → `.agent/scripts/tests/`
- `test_daigo_click.py` → `.agent/scripts/tests/`
- `test_edge_daigo.py` → `.agent/scripts/tests/`
- `debug_cdp.py` → `.agent/scripts/tests/`

`.agent/scripts/tests/` ディレクトリが存在しない場合は新規作成すること。

### 3. .gitignore の追加整備
`.gitignore` に以下のパターンを追加する（まだ含まれていないもののみ）:
```
# Temporary output files
*.txt
!README.txt
objects.txt
pack.txt
sync_log.txt
tree.txt
tree_clean.txt

# Temporary HTML/JSON scraping files
iroha_*.html
iroha_*.json

# One-off scripts (root level)
find_large.py
find_loose.py
```

## Output
- コード修正のPull Requestを作成すること
- PRの説明に、削除したファイル一覧と移動したファイル一覧を記載すること
- 結果レポートを `00_SYSTEM/CORE/inbox/jules_task005_cleanup_report.md` に作成すること

## Constraints
- **コードのロジック変更は禁止**。ファイルの移動・削除・.gitignore更新のみ。
- `.agent/scripts/genesis_coordinator.py` と `.agent/scripts/cdp_browser.py` は絶対に変更しないこと
- `00_SYSTEM/CORE/` 配下のファイルは移動・削除しないこと
- `GEMINI.md` は変更しないこと
