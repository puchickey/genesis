# Project B Design Doc: "The Janitor" (経理データ洗浄の達人)

**Status:** Draft
**Last Updated:** 2025-12-28
**Purpose:** 転職市場における「経理実務 x エンジニアリング」の証明（Proof of Competence）。

---

## 1. Vision & Strategy
### 1.1 The Concept
一般のエンジニアが見落としがちな、経理現場特有の「汚いデータ（Dirty Data）」を、エンジニアリングで「美しいデータ（Clean Data）」に変換する。
華やかなAI分析の前段階にある**「泥臭い前処理（Pre-processing）」**に特化した、職人芸的スクリプト集。

### 1.2 The "Bridge" Narrative
*   **Target:** Unicorn / Tech企業のCFO, CTO, バックオフィス責任者。
*   **Message:** 「私はAIをただ使うだけの人間ではありません。AIが最も嫌う『現場データの汚れ』を、あなたの会社のエンジニアに代わって掃除できる人間です」
*   **Outcome:** 「この人は現場（Accounting）と技術（Engineering）の共通言語を持っている」と評価させる。

---

## 2. Product Architecture
Webアプリとして公開するのではなく、**GitHubリポジトリ（Library/Tool）** として構成する。

### 2.1 Core Modules (The Toolkit)
*   **`cleaner.py` (浄化装置)**
    *   **Normalizer:** 全角半角統一（`unicodedata.normalize('NFKC')`）、環境依存文字の排除。
    *   **AddressParser:** 住所分割（都道府県、市区町村、番地）。
    *   **NumberParser:** 「金壱萬圓」「1,000円」「1000」等の混在を `int/float` に統一。
*   **`merger.py` (結合解除)**
    *   Excelの「結合セル（Merged Cells）」を検知し、値を展開（Unmerge & Fill）してCSV化する。
*   **`linker.py` (名寄せ)**
    *   `RapidFuzz` を使用したあいまい一致マッチング（振込名義 vs 請求先マスタ）。
    *   スコア判定（Score > 90 で自動突合）。

### 2.2 Simulation Environment (The Trap)
会社で使えないなら、自宅で「架空の最悪な現場」を再現する。
*   **`generate_dirty_data.py` (汚染物質生成)**
    *   Fakerライブラリを使用し、意図的に「表記ゆれ」「結合セル」「欠損」を含むダミーCSVを生成する。
    *   *Purpose:* 自作自演のマッチポンプだが、GitHub上のDemoとして「処理前(Before) / 処理後(After)」を見せるために必須。

---

## 3. Implementation Roadmap (年末年始プラン)

### Phase 1: Preparation (骨格作り)
*   [ ] GitHubリポジトリ作成（`accounting-janitor`）。
*   [ ] README.md の執筆（技術力ではなく「解決する課題」を熱く語る）。
*   [ ] 環境構築（Poetry / venv）。

### Phase 2: Core Logic (武器作り)
*   [ ] `generate_dirty_data.py` の実装（まずは敵を作る）。
*   [ ] `cleaner.py` の実装（敵を倒す）。
*   [ ] **Jupyter Notebook作成**: 「汚いデータ」が「綺麗になる」過程を可視化する（これがポートフォリオの本体）。

### Phase 3: The "Business Impact" (翻訳)
*   [ ] 職務経歴書の「備考・特記事項」用テキスト作成。
*   [ ] 仮想事例スライド（1枚）: 「月20時間の削減効果シミュレーション」。

---

## 4. Why This Wins?
*   **Uniqueness:** 多くのエンジニア候補は「モデル作成（TensorFlow/PyTorch）」をアピールするが、「前処理（Pandas/Re）」を極めている人は少ない。
*   **Empathy:** 経理担当者にしか分からない「Excelの苦しみ」への深い理解が、コードの端々（コメントや README）に滲み出る。

---
*Created by Genesis OS Planning Module*
