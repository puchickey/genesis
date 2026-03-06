---
name: Article Writer
description: チェックリスト型のnote記事をユーザーのテーマ情報から構成・生成するスキル。「記事を書いて」「ドラフトを作って」「/write」で起動。生成後はcontent-reviewerでレビュー可能。
---

# Article Writer (v1.0: Checklist Article Generator)

## 🚦 ROUTER
ユーザーが記事の作成を依頼した場合に起動。

### Trigger
*   「記事を書いて」「ドラフトを作って」「/write」
*   記事テーマ + 素材情報がユーザーから提示された場合

### Immediate Action
**以下のプロシージャファイルをロード:**
> `view_file g:\マイドライブ\Genesis_OS\.agent\skills\article-writer\procedures\01_CHECKLIST_ARTICLE.md`

### 連携スキル
*   記事生成後、**content-reviewer** でCARレビューを実行可能
*   ユーザーに「レビューしますか？」と確認してから起動
