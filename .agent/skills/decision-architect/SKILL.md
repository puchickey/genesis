---
name: Decision Architect
description: 複雑な意思決定を行う際、感情や直感ではなく、定義された「評価マトリクス（Valuation Matrix）」に基づいて論理的な評決（Verdict）を下すスキル。
---

# Decision Architect

## 1. Purpose
ユーザーが「AかBか」の岐路に立たされた際、Ad-hoc（その場しのぎ）な助言を防ぎ、常にGenesisの憲法（L1 Strategy）と評価基準（7 Virtues / 8 Nightmares）に基づいた一貫性のある意思決定を支援する。

## 2. Trigger
ユーザーが以下のような相談をした時に発動する。
*   「どっちがいいと思う？」 (Comparative Question)
*   「これでいいかな？」 (Validation Question)
*   「迷っている」 (Dilemma)

## 3. Decision Protocol
回答を作成する前に、必ず以下のステップで思考せよ（思考プロセスは出力しても良い）。

### Step 1: Variable Identification (軸の特定)
その決断において重要な変数は何か？ `VALUATION_MATRIX.md` から該当する項目をピックアップする。
*   *例: 転職相談なら -> Money, Freedom, Risk*
*   *例: 物件相談なら -> Comfort, Cost, Commute*

### Step 2: Scoring (採点)
選択肢（Option A / Option B）を、Step 1で定めた変数ごとに採点する。
*   **◎ Winner:** 明らかに優れている (+1pt)
*   **◯ Good:** 十分な水準 (0pt)
*   **△ Risk:** 懸念がある (-1pt)
*   **× Critical:** 致命的な欠点 (-100pt -> 即却下)

### Step 3: Synthesis & Verdict (評決)
総合点だけでなく、「Scenario C（現在の戦略）」との適合性を加味して結論を出す。
*   **Verdict:** [Option A / Option B / Both Reject]
*   **Reason:** なぜそちらを選ぶのか、ロジックを一言で。

## 4. Reference
*   `10_Domains/01_Work/02_Career_Design/01_VALUATION_MATRIX.md` (詳細な評価基準辞書)
