---
name: Frame Discovery
description: コンテンツのフレーム（切り口・ポジション）の独自性を発見・検証するスキル。user_profile.mdから「自分にしかできない」フレーム候補を生成し、調査AIによるWeb検索で類似コンテンツの有無を検証する。「フレームを考えたい」「切り口を探したい」「ポジションを見つけたい」「被りを調べたい」「/frame」で起動。
---

# Frame Discovery Skill

## Purpose
Web上に存在しない、ユーザーにしか主張できない独自のフレーム（切り口・ポジション）を発見するための探索プロセス。

## Design Principles
*   「自分の中身」から発散し、「市場の不在」で収束する
*   調査プロンプトには「被りがないことを確認したい」という目的を**含めない**（アンチバイアス）
*   「狂気」を直接定義しない。「自分にできる × Webに存在しない」制約の交差が自然に新規性を担保する

## 📂 Key References
*   **ユーザーの属性:** `G:\マイドライブ\Genesis_OS\00_SYSTEM\CORE\user_profile.md`
*   **既存のコンテンツ方針:** `G:\マイドライブ\Genesis_OS\10_Domains\03_Creation\01_投資活動\note\Note_Project_Setup.md`

---

## 🚦 Execution Workflow

### Phase 1: Frame Generation（発散）
**Load:** `procedures/01_FRAME_GENERATION.md`

user_profile.md の属性を掛け合わせ、フレーム候補を複数生成する。

### Phase 2: Research Prompt（調査準備）
**Load:** `procedures/02_RESEARCH_PROMPT.md`

Phase 1の候補をもとに、調査AI用のプロンプトを生成する。目的を秘匿したニュートラルな設計。

### Phase 3: Evaluation（収束）
**Load:** `procedures/03_EVALUATION.md`

調査結果を受け取り、ユーザーと共に判定する。不合格ならPhase 1へループ。
