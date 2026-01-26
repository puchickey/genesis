# カスタム感情Firestoreコレクション構造

## 概要

カスタム感情は主にローカル（SQLite）で管理され、Firestoreはバックアップとして機能します。
ユーザーごとの感情カスタマイズ設定を保存し、デバイス間での同期や復元に使用されます。

## コレクション構造

### `custom_emotions` コレクション

```
custom_emotions/
├── {userId}/
│   └── emotions/
│       └── data
```

#### ドキュメント構造

```typescript
interface CustomEmotionsDocument {
  // ユーザーのカスタム感情配列
  emotions: CustomEmotion[];
  
  // 最終更新日時
  lastUpdated: Timestamp;
  
  // バックアップバージョン（将来の拡張用）
  version: number;
}

interface CustomEmotion {
  // カスタム感情の一意識別子
  id: string;
  
  // 第1階層感情（例："喜び"、"悲しみ"など）
  tier1Emotion: string;
  
  // 第2階層感情の配列（最大6個）
  tier2Emotions: string[];
  
  // 作成日時
  createdAt: string; // ISO 8601形式
  
  // 更新日時（オプション）
  updatedAt?: string; // ISO 8601形式
}
```

## データ例

```json
{
  "emotions": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "tier1Emotion": "喜び",
      "tier2Emotions": ["幸福", "満足", "ワクワク", "達成感", "安心", "感謝"],
      "createdAt": "2024-01-15T09:30:00.000Z",
      "updatedAt": "2024-01-20T14:45:00.000Z"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "tier1Emotion": "怒り",
      "tier2Emotions": ["イライラ", "憤り", "不満", "悔しさ"],
      "createdAt": "2024-01-16T10:00:00.000Z",
      "updatedAt": null
    }
  ],
  "lastUpdated": "2024-01-20T14:45:00.000Z",
  "version": 1
}
```

## アクセスパターン

### 1. バックアップ（書き込み）
- **頻度**: 低（カスタム感情変更時のみ）
- **パス**: `/custom_emotions/{userId}/emotions/data`
- **操作**: SET（全体を上書き）
- **バッチ処理**: 不要（単一ドキュメント）

### 2. 復元（読み取り）
- **頻度**: 極低（アプリ初回起動、デバイス変更時など）
- **パス**: `/custom_emotions/{userId}/emotions/data`
- **操作**: GET
- **キャッシュ**: 不要（一度きりの読み取り）

### 3. 同期チェック
- **頻度**: 低（アプリ起動時など）
- **パス**: `/custom_emotions/{userId}/emotions/data`
- **操作**: GET（lastUpdatedフィールドのみ）

## セキュリティルール

```javascript
match /custom_emotions/{userId}/emotions/{document} {
  // ユーザーは自分のカスタム感情のみ読み書き可能
  allow read, write: if request.auth != null && request.auth.uid == userId;
  
  // データ検証
  allow write: if request.auth != null && request.auth.uid == userId
    && request.resource.data.emotions is list
    && request.resource.data.emotions.size() <= 20  // 最大20カテゴリ
    && request.resource.data.lastUpdated is timestamp
    && request.resource.data.version is number;
}
```

## 設計方針

1. **オフラインファースト**
   - 主要なデータはローカルSQLiteで管理
   - Firestoreはバックアップとしてのみ使用

2. **シンプルな構造**
   - ユーザーごとに1つのドキュメント
   - 全カスタム感情を配列として保存

3. **効率的な同期**
   - 更新日時による簡易的な同期判定
   - 全体を一括で保存/復元

4. **将来の拡張性**
   - versionフィールドによる互換性管理
   - プレミアム機能での拡張を考慮

## 制限事項

- カスタム感情カテゴリは最大20個まで
- 各カテゴリの第2階層感情は最大6個まで
- ドキュメントサイズは1MBまで（Firestore制限）

## 関連ファイル

- `/lib/services/firestore_service.dart` - Firestore操作の実装
- `/lib/services/emotion_service.dart` - カスタム感情管理ロジック
- `/lib/models/custom_emotion_model.dart` - データモデル定義