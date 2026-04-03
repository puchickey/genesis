# Genesis OS リポジトリ全体調査レポート

## 1. ディレクトリツリー
```text
.
├── 00_SYSTEM/                # システム管理・コア設定
│   ├── Automation/           # 自動化スクリプト（同期等）
│   ├── CORE/                 # [KERNEL] 憲法、ステータス、タスク管理
│   │   ├── inbox/            # エージェントからの報告受領
│   │   ├── memories/         # 過去のセッションサマリー
│   │   ├── outbox/           # エージェントへの指示出し
│   │   └── ...
│   └── Resource/             # プロジェクト仕様書、プロンプト等
├── 03_Creation/              # 創作プロジェクトの実体（WorryTime等）
├── 05_Resources/             # 知識ベース、ツール、プロンプト、仕様書
├── 10_Domains/               # 実行領域（Work, LifeBase, Creation）
│   ├── 01_Work/              # 仕事・キャリア戦略
│   ├── 02_LifeBase/          # 生活基盤・財務・健康
│   └── 03_Creation/          # 自己実現・副業プロジェクト
├── 20_Inventory/             # 資産・知識ベース・ログ
│   └── 99_Stream/            # 日次ログ、インタビュー記録
├── 99_Migration/             # 旧システムからの移行データ・バックアップ
├── .agent/                   # エージェント構成（scripts, skills, workflows）
│   ├── scripts/              # 実行スクリプト（ブラウザ操作等）
│   ├── skills/               # エージェントの機能定義（SKILL.md）
│   └── workflows/            # 標準化された作業フロー
└── (Root Files)              # 設定ファイル、一時スクリプト
```

## 2. ファイル一覧と概要

### System Core (`00_SYSTEM/CORE/`)
| ファイル名 | 概要 |
|:--|:--|
| `GENESIS_AI_INSTRUCTION.md` | Genesis OS の基本憲法。役割分担、ディレクトリ構造、行動指針を定義。 |
| `LIFE_PLAN_CORE.md` | 人生のコア・アイデンティティ、価値観、戦略的優先順位を記述した最上位文書。 |
| `user_profile.md` | ユーザーの客観的事実（経歴、健康、財務、性格、好み）を網羅した事実集。 |
| `current_status.md` | 現在のフェーズ、各ドメインの投資/維持ステータスを管理するダッシュボード。 |
| `active_tasks.md` | 直近のタスク一覧。カンバン形式で進行状況を管理。 |
| `agent_registry.md` | 複数エージェント（Antigravity, Jules等）間の排他制御とタスク管理。 |

### Agent Scripts (`.agent/scripts/`)
| ファイル名 | 概要 |
|:--|:--|
| `cdp_browser.py` | Edge ブラウザを CDP 経由で操作するための共通クラス。 |
| `genesis_coordinator.py` | ローカル作業の完了を Antigravity へ報告する等のコーディネートを行う。 |
| `test_antigravity_cdp.py` | Antigravity (CDPモード) への接続テスト用スクリプト。 |
| `investigate_antigravity.ps1` | ローカル環境（プロセス、ポート、パイプ）をスキャンする診断用スクリプト。 |
| `create_shortcut.ps1` | CDP 有効化状態でアプリを起動するためのショートカット作成スクリプト。 |

### Agent Skills (`.agent/skills/`)
| スキル名 | 概要 (SKILL.md より) |
|:--|:--|
| `jules-coordinator` | 非同期作業用エージェント Jules へのタスク委譲を管理する。 |
| `financial-planner` | 財務状況分析、J-Curve戦略に基づく予算管理や ROI 試算を行う。 |
| `decision-architect` | 評価マトリクスに基づき、感情を排した論理的な意思決定を支援する。 |
| `frame-discovery` | コンテンツの独自性（フレーム）を発見し、Web 検索で検証する。 |
| `young-method` | ジェームス・W・ヤングの「アイデアのつくり方」に基づく 5 段階プロトコル。 |
| `git-operator` | 変更履歴を Git で管理し、標準化されたメッセージでコミットする。 |
| `journaling-clerk` | 音声入力やログを整形し、DailyLog に適切に記録・要約する。 |

### Agent Workflows (`.agent/workflows/`)
| ファイル名 | 概要 |
|:--|:--|
| `genesis.md` | システム起動時の初期化、同期、コンテキスト読み込みの標準フロー。 |
| `clarification_interview.md` | ユーザーから潜在的な思考を抽出するためのインタビュープロトコル。 |

### Domain Files (`10_Domains/`)
| ファイル名 | 概要 |
|:--|:--|
| `01_Work/CAREER_STRATEGY_LOGIC.md` | 収入、健康、資産形成のトレードオフを分析したキャリアの論理構造。 |
| `01_Work/DOMAIN_STATUS_01_WORK.md` | 仕事ドメインの維持（本業）と投資（転職・副業）の現状。 |
| `02_LifeBase/DOMAIN_STATUS_02_LIFEBASE.md` | 健康・財務・住環境の状態と、転居プロジェクトの進捗。 |
| `02_LifeBase/INVENTORY_PHILOSOPHY.md` | 「管理という行為を消す」ための日用品管理とミニマリズムの哲学。 |
| `03_Creation/DOMAIN_STATUS_03_CREATION.md` | 創作ドメイン。過去プロジェクトの凍結と Project B への集中を定義。 |

### Inventory (`20_Inventory/`)
| ファイル名 | 概要 |
|:--|:--|
| `99_Stream/DailyLog/` | 日付ごとに整理された日次ログ。ユーザーの活動と AI の介在記録。 |
| `analyze_2025_finance.py` | 2025 年の財務データを分析するための Python スクリプト。 |
| `パレオな男_各診断結果/` | 科学的知見に基づく自己分析（適職、メタ認知等）の結果。 |
| `運の方程式_20260104.pdf` | 外部知識リソース（書籍の要約や関連資料）。 |

### Root Config
| ファイル名 | 概要 |
|:--|:--|
| `GEMINI.md` | Gemini CLI (バックグラウンドワーカー) のアイデンティティと行動規範。 |
| `JULES_TASK.md` | 今回の調査レポート作成の指示書。 |
| `genesis_auto_sync.py` | ローカルの変更を Git で自動同期（Add/Commit/Push）するスクリプト。 |

---

## 3. 設計上の懸念点・改善提案

### 重複 (Redundancy)
- **同期スクリプトの重複**: ルート直下と `00_SYSTEM/Automation/` の両方に `genesis_auto_sync.py` が存在します。環境に合わせてパスが微調整されていますが、一元管理が望ましいです。
- **ログファイルの散在**: `sync_log.txt` がルートと `00_SYSTEM/Automation/` に分散して生成されています。

### 不整合 (Inconsistency)
- **リソース配分の定義**: `00_SYSTEM/Resource/` と `05_Resources/` の役割の境界が曖昧です。前者はシステム用、後者はユーザー用などの明確な定義が必要です。
- **プロジェクトステータスの二重管理**: `00_SYSTEM/CORE/current_status.md` と各ドメインの `DOMAIN_STATUS_*.md` で情報が重なっている部分があり、更新漏れのリスクがあります。

### 不要ファイル (Unnecessary Files)
- **ルート直下の調査残骸**: `iroha_*.html`, `iroha_api.json`, `objects.txt`, `pack.txt` など、特定の調査やデバッグ時に作成されたと思われる一時ファイルがルートに残っています。これらは `99_Migration/` や適切な作業用ディレクトリへ移動、または削除すべきです。

### 命名規則の乱れ (Naming Convention)
- **ケースの混在**: `active_tasks.md` (Snake Case) と `LIFE_PLAN_CORE.md` (Upper Snake) 、`User_Profile.md` (Pascal/Snake 混在) など、Markdown ファイルの命名規則が一貫していません。
- **ディレクトリ名のプレフィックス**: `00_`, `10_`, `20_` と数字付きのものと、`.agent`, `99_Migration` のようにそうでないものが混在しています。

---
以上
