# Firestore データベース整理計画

## 現状分析（13コレクション）

### 主要コレクション（3個）
- `users` - ユーザー情報とカスタムオプション
- `objects` - モノのマスターデータ（Ver3.0）
- `logs` - 構造化ログ（Ver3.0）

### 旧データコレクション（1個）
- `insightLogs` - 廃止予定（Ver3.0で非推奨）

### モノログ関連コレクション（7個）
- `monologs` - 2タップ感情記録
- `monolog_sessions` - セッション管理
- `emotion_selections` - 感情選択履歴
- `memo_analytics` - メモ分析
- `mylog_view_sessions` - 閲覧セッション
- `user_behavior_patterns` - 行動パターン
- `analytics` - 一般アナリティクス

### その他（2個）
- `prompts` - プロンプト管理（使用中）
- `custom_emotions` - SQLiteで管理、Firestoreにバックアップ（Ver3.0で追加）

## 整理後の構成（8コレクション）

1. **users** - ユーザー情報
2. **objects** - モノのマスターデータ
3. **logs** - 構造化ログ（objects関連）
4. **monologs** - 2タップ感情記録
5. **monolog_analytics** - 統合分析データ
   - sessions
   - emotions
   - memos
   - views
   - patterns
6. **prompts** - プロンプト管理
7. **analytics** - 一般アナリティクス
8. **custom_emotions** - カスタム感情のバックアップ（オフラインファースト）

## 実装手順

### Phase 1: データバックアップ（完了）
1. ✅ 全コレクションのエクスポート
2. ✅ ローカルバックアップの作成

### Phase 2: 新構造の実装（完了）
1. ✅ `monolog_analytics`コレクションの設計
2. ✅ FirestoreServiceの更新
3. ✅ データ移行スクリプトの作成

### Phase 3: データ移行（完了）
1. ✅ 分析データの統合移行
2. ✅ `insightLogs`の削除
3. ✅ 旧コレクションの削除

### Phase 4: カスタム感情バックアップ（完了）
1. ✅ `custom_emotions`コレクションの設計と実装
2. ✅ FirestoreServiceにバックアップメソッド追加
3. ✅ EmotionServiceに同期機能追加
4. ✅ セキュリティルールの更新

### Phase 5: 検証とテスト（完了）
1. ✅ 統合テストの実施
2. ✅ パフォーマンス検証
3. ✅ カスタム感情同期機能のテスト

## 実装完了（v0.10.3+9）
すべてのフェーズが正常に完了し、本番環境で稼働中です。
- Firestoreコレクション: 13→8に削減
- InsightLog機能: 完全削除
- カスタム感情: オフラインファースト実装
- Firebase Auth保護: FirebaseAuthWrapper導入

## 写真データ保存戦略（無料枠対応）

### 1. 画像圧縮
- WebP形式（JPEG比30-50%削減）
- 最大解像度：800x800px
- 品質：80%
- 予想サイズ：50-100KB/枚

### 2. ハイブリッド保存
```dart
// ローカル優先
- 即座にローカル保存
- オフライン対応
- 無制限容量

// クラウドバックアップ（選択的）
- 重要な写真のみ
- Wi-Fi接続時
- 容量監視付き
```

### 3. 容量管理
- Firebase Storage無料枠：5GB
- 推定保存可能枚数：50,000〜100,000枚
- 80%使用時にユーザー通知
- 古い写真の自動アーカイブオプション

## セキュリティルールの更新

```javascript
// Firestore Rules
match /monolog_analytics/{document} {
  allow read, write: if request.auth != null
    && request.auth.uid == resource.data.userId;
}

// Custom Emotions Rules
match /custom_emotions/{userId} {
  allow read: if request.auth != null && request.auth.uid == userId;
  allow write: if request.auth != null
    && request.auth.uid == userId
    && request.auth.uid == resource.data.userId
    && request.resource.data.keys().hasAll(['userId', 'emotions', 'lastUpdated'])
    && request.resource.data.emotions is list
    && request.resource.data.emotions.size() <= 50
    && request.resource.size < 100 * 1024; // 100KB制限
}

// Storage Rules
match /photos/{userId}/{photoId} {
  allow read, write: if request.auth != null
    && request.auth.uid == userId
    && request.resource.size < 1 * 1024 * 1024; // 1MB制限
}
```

## 監視とアラート

1. **使用量監視**
   - Firestore読み取り/書き込み回数
   - Storage使用量
   - 帯域幅使用量

2. **アラート設定**
   - 日次上限の80%到達時
   - 異常なスパイク検知
   - エラー率上昇時

## カスタム感情の実装詳細

### オフラインファースト設計
- **ローカル（SQLite）**: プライマリストレージ
- **Firestore**: バックアップとプレミアム機能用
- **同期**: タイムスタンプベースの競合解決

### データ構造
```dart
// Firestoreドキュメント: /custom_emotions/{userId}
{
  "userId": "user123",
  "emotions": [
    {
      "id": "uuid",
      "tier1Name": "カスタム感情1",
      "tier1Emoji": "😊",
      "tier2Emotions": [
        {"name": "詳細1", "emoji": "😄"},
        {"name": "詳細2", "emoji": "😁"}
      ],
      "createdAt": "2024-01-01T00:00:00Z",
      "updatedAt": "2024-01-01T00:00:00Z"
    }
  ],
  "lastUpdated": "2024-01-01T00:00:00Z"
}
```

## コスト削減効果

- コレクション数：13→8（38%削減）
- クエリ効率：分析データ統合により最大80%改善
- ストレージ：画像圧縮により50%削減
- カスタム感情：オフラインファーストで読み取り回数最小化
- 推定月額コスト：無料枠内維持可能