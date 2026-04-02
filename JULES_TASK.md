# JULES_TASK: Genesis OS リポジトリ全体調査レポートの作成

## Context (背景)
Genesis OS は個人の生活・仕事・創作活動を一元管理するファイルベースのOSである。
最近、マルチエージェント統合環境（Antigravity / Gemini CLI / Jules の連携基盤）を追加した。
現在、リポジトリ全体の構造や各ファイルの役割が体系的にまとまっていないため、全体像を把握するための調査レポートが必要である。

## Goal (ゴール)
リポジトリ内の**全てのディレクトリとファイル**を走査し、以下の情報を網羅した**調査レポート（Markdown）**を作成せよ。

## Output Requirements (出力要件)

### 1. ディレクトリツリー
- リポジトリ全体のディレクトリ構造を `tree` 形式で出力すること。
- `.git` ディレクトリは除外すること。

### 2. ファイル一覧と概要
以下のカテゴリに分けて、各ファイルの**目的・内容の要約（1〜2行）**を記載すること。

| カテゴリ | 対象 |
|:--|:--|
| System Core | `00_SYSTEM/CORE/` 配下の全ファイル |
| Agent Scripts | `.agent/scripts/` 配下の全ファイル |
| Agent Skills | `.agent/skills/` 配下の全SKILL.md |
| Agent Workflows | `.agent/workflows/` 配下の全ファイル |
| Domain Files | `10_Domains/` 配下の主要ファイル |
| Inventory | `20_Inventory/` 配下の主要ファイル |
| Root Config | ルート直下の設定ファイル（GEMINI.md 等） |

### 3. 設計上の懸念点・改善提案
ファイルを読んだ上で気づいた以下の点を列挙すること。
- **重複**: 同じ内容が複数ファイルに書かれている箇所
- **不整合**: ファイル間で矛盾する記述
- **不要ファイル**: 明らかにテスト用・一時的で削除すべきファイル
- **命名規則の乱れ**: ファイル名やディレクトリ名の一貫性の欠如

## Output Format (出力形式)
- ファイル名: `00_SYSTEM/CORE/inbox/jules_report_repo_analysis.md`
- 形式: Markdown
- 言語: 日本語

## Constraints (制約)
- **コードの変更は一切行わないこと。** 今回のタスクは調査・レポートのみ。
- レポートファイルの作成のみをPull Requestとして提出すること。
