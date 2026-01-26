# 旧Firestoreコレクション削除ガイド

## 概要

本ドキュメントは、Firestoreコレクション統合プロジェクトの一環として、不要になった旧コレクションを安全に削除する手順を説明します。

## 削除対象コレクション

以下の6つのコレクションが削除対象です：

1. **insightLogs** - 旧アナリティクスコレクション（削除済みコードで使用）
2. **monolog_sessions** - monolog_analyticsに統合済み
3. **emotion_selections** - monolog_analyticsに統合済み
4. **memo_analytics** - monolog_analyticsに統合済み
5. **mylog_view_sessions** - monolog_analyticsに統合済み
6. **user_behavior_patterns** - monolog_analyticsに統合済み

## 実行前の確認事項

### 1. バックアップ
- 重要なデータがないか最終確認
- 必要に応じてFirestoreエクスポートを実行

### 2. アプリケーションの確認
- 最新のアプリバージョンが新しいコレクション構造を使用していることを確認
- 旧バージョンのアプリがまだ使用されていないことを確認

### 3. Firebase コンソールでの確認
```
1. Firebase Console > Firestore Database
2. 各コレクションのドキュメント数を確認
3. サンプルドキュメントを確認して内容を把握
```

## 削除スクリプトの実行

### 1. 依存関係のインストール
```bash
# プロジェクトルートで実行
flutter pub get
```

### 2. Firebase設定の確認
```bash
# Firebase CLIでログイン状態を確認
firebase login
```

### 3. スクリプトの実行
```bash
# プロジェクトルートから実行
dart run scripts/delete_old_collections.dart
```

### 4. 実行時の流れ
1. 削除対象コレクションの一覧が表示されます
2. 確認プロンプトで `yes` を入力
3. 各コレクションが順次削除されます
4. エラーが発生した場合、続行するか選択できます

## スクリプトの特徴

### バッチ処理
- 500件ずつバッチ削除を実行（Firestoreの制限）
- 大量のドキュメントも効率的に削除

### 安全機能
- 実行前の確認プロンプト
- 空のコレクションはスキップ
- エラー時の続行/中止選択

### 進捗表示
- 削除中のドキュメント数をリアルタイム表示
- 各コレクションの削除完了時に総数表示

## 削除後の確認

### 1. Firebase Consoleで確認
```
1. Firestore Databaseを開く
2. 削除対象コレクションが表示されないことを確認
```

### 2. 現在のコレクション構成（削除後）
```
- users/                    # ユーザー基本情報
- objects/                 # モノのマスターデータ
- logs/                    # 構造化ログ（objects関連）
- monologs/                # モノログデータ
- monolog_analytics/       # 統合アナリティクス
- prompts/                 # プロンプト管理
- analytics/               # 一般アナリティクス
- custom_emotions/        # カスタム感情バックアップ（オフラインファースト）
```

## トラブルシューティング

### 権限エラーが発生する場合
```bash
# Firebase CLIで再ログイン
firebase logout
firebase login
```

### スクリプトが途中で止まる場合
- ネットワーク接続を確認
- Firebase Consoleでクォータを確認
- 少し時間を置いてから再実行

### 削除が完了しない場合
- Firebase Consoleから手動で削除
- または、Firebase CLIを使用：
```bash
firebase firestore:delete [collection-name] --recursive
```

## 注意事項

⚠️ **この操作は取り消せません**
- 削除したデータは復元できません
- 本番環境での実行は慎重に行ってください

## 関連ドキュメント

- [Firestoreコレクション整理計画](./firestore_cleanup_plan.md)
- [カスタム感情Firestore構造](./custom_emotions_firestore_structure.md)