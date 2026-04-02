---
name: cdp-browser-operator
description: Edgeブラウザを直接操作し、ログイン済みのSaaSやWeb画面の全自動処理（スクレイピング・入力）を行うスキル
---
# CDP Browser Operator Skill

## 🎯 Purpose
ローカルのEdgeブラウザ内ですでにログイン済みのセッション（Cookieパス等）を活用し、データの自動抽出や入力などのブラウザ作業をGenesis OS (Antigravity) から全自動化する。

## 🛠️ Setup & Requirements
このスキルを利用する前に、ユーザーが必ず事前に以下のPowerShellスクリプトを実行し、Edgeをデバッグモード（port 9223）で起動している必要がある。
`G:\マイドライブ\Genesis_OS\.agent\scripts\edge_cdp_start.ps1`

## 📝 Execution Protocol
当スキルを利用する場合、Antigravity（貴方）は以下の役割を果たす。

1. **スクリプトの動的生成**: 目的のWebサイト操作専用のPython操作スクリプト( 例: `auto_fetch.py` )を自動生成する。
   * ルール: `import sys`, `sys.path.append(r"G:\マイドライブ\Genesis_OS\.agent\scripts")` を行い、`from cdp_browser import CDPBrowser` を利用すること。
   * ルール: `b = CDPBrowser()`, `b.connect()` を行い、`b.evaluate()` (JavaScriptの実行) を多用してDOMからテキストを抽出またはクリック操作を行うこと。
   
2. **スクリプトの実行**: ターミナルから `run_command` を用いて、作成したPythonスクリプトを実行する。

3. **結果のパースと報告**: 取得したJSONデータやCSVデータを読み取り、要約してユーザーに報告する。
