# データモデルとFirestore構造

このドキュメントでは、モノログアプリのデータモデルとFirestoreのデータ構造について詳細に説明します。

## 概要

モノログアプリは、モノ（物理的なオブジェクト）とそれに対する感情的な記録（ログ）を管理するための二層構造のデータモデルを採用しています。

## 主要データモデル

### 1. ObjectModel（モノのモデル）

**概要**: 物理的なモノの基本情報を管理するモデル

```dart
class ObjectModel {
  final String id;
  final String userId;
  final String name;
  final String imageUrl;
  final DateTime createdAt;
  final DateTime updatedAt;
  final Map<String, dynamic>? metadata;
  
  // 集計フィールド
  final int logCount;
  final DateTime? lastLoggedAt;
}
```

**Firestoreパス**: `users/{userId}/objects/{objectId}`

**フィールド説明**:
- `id`: 自動生成されるユニークID
- `userId`: 所有者のユーザーID（匿名認証ID）
- `name`: モノの名前（ユーザーが設定）
- `imageUrl`: Firebase Storageに保存された画像のURL
- `createdAt`: 作成日時
- `updatedAt`: 更新日時
- `metadata`: 追加のメタデータ（拡張用）
- `logCount`: 関連するログの数
- `lastLoggedAt`: 最後にログが記録された日時

### 2. LogModel（感情ログのモデル）

**概要**: モノに対する感情的な記録を管理するモデル

```dart
class LogModel {
  final String id;
  final String userId;
  final String objectId;
  final String objectName;
  final String objectImageUrl;
  
  // 感情ベクター
  final String emotionVector; // 'positive', 'complex', 'unknown'
  
  // 構造化された質問への回答
  final String? question1Answer;
  final String? question2Answer;
  final String? question3Answer;
  
  // 選択された感情
  final List<String> selectedEmotions;
  final String? customEmotion;
  
  // メタデータ
  final DateTime createdAt;
  final Map<String, dynamic>? additionalData;
  
  // プロンプト情報
  final String? promptId;
  final String? promptText;
}
```

**Firestoreパス**: `users/{userId}/logs/{logId}`

**フィールド説明**:
- `id`: 自動生成されるユニークID
- `userId`: 記録したユーザーのID
- `objectId`: 関連するObjectModelのID
- `objectName`: モノの名前（スナップショット）
- `objectImageUrl`: モノの画像URL（スナップショット）
- `emotionVector`: 選択された感情ベクター
- `question1Answer`〜`question3Answer`: 構造化された質問への回答
- `selectedEmotions`: 選択された感情タグのリスト
- `customEmotion`: ユーザーが入力したカスタム感情
- `createdAt`: 記録日時
- `additionalData`: 追加データ（拡張用）
- `promptId`: 使用されたプロンプトのID
- `promptText`: 使用されたプロンプトテキスト

### 3. PromptModel（プロンプトのモデル）

**概要**: 内省を促すための質問プロンプトを管理

```dart
class PromptModel {
  final String id;
  final String category; // 'positive', 'complex', 'unknown'
  final String text;
  final int order;
  final bool isActive;
  final Map<String, String>? followUpQuestions;
}
```

**Firestoreパス**: `prompts/{promptId}`

**フィールド説明**:
- `id`: プロンプトのユニークID
- `category`: 感情ベクターカテゴリ
- `text`: プロンプトのテキスト
- `order`: 表示順序
- `isActive`: アクティブ状態
- `followUpQuestions`: フォローアップ質問のマップ

### 4. DiagnosisModel（診断モデル）

**概要**: ユーザーの性格診断結果を管理

```dart
class DiagnosisModel {
  final String id;
  final String userId;
  final String diagnosisType; // 'initial' or 'deep'
  final Map<String, int> typeScores;
  final String primaryType;
  final String? secondaryType;
  final DateTime completedAt;
  final Map<String, dynamic> answers;
}
```

**Firestoreパス**: `users/{userId}/diagnoses/{diagnosisId}`

**診断タイプ（6種類）**:
1. **収集家型**: モノを集めることで安心感を得る
2. **思い出型**: モノに思い出を重ねる
3. **実用主義型**: 機能性を重視
4. **ミニマリスト型**: 必要最小限を好む
5. **感情移入型**: モノに感情を投影
6. **クリエイター型**: モノを創造的に活用

### 5. UserProfile（ユーザープロファイル）

**概要**: ユーザーの基本情報と設定

```dart
class UserProfile {
  final String userId;
  final DateTime createdAt;
  final DateTime lastActiveAt;
  final Map<String, dynamic> settings;
  final bool hasCompletedOnboarding;
  final bool hasCompletedInitialDiagnosis;
  final String? primaryDiagnosisType;
}
```

**Firestoreパス**: `users/{userId}`

### 6. InsightLog（レガシーモデル）

**概要**: 旧バージョンとの互換性のために保持

```dart
class InsightLog {
  final String id;
  final String userId;
  final String? title;
  final String content;
  final String? emotion;
  final List<String>? tags;
  final DateTime timestamp;
  final String? imagePath;
  final Map<String, dynamic>? metadata;
}
```

## Firestoreコレクション構造

```
firestore/
├── users/
│   └── {userId}/
│       ├── profile (document)
│       ├── objects/
│       │   └── {objectId} (documents)
│       ├── logs/
│       │   └── {logId} (documents)
│       ├── diagnoses/
│       │   └── {diagnosisId} (documents)
│       └── insightLogs/ (legacy)
│           └── {insightLogId} (documents)
├── prompts/
│   └── {promptId} (documents)
└── systemConfig/
    └── settings (document)
```

## インデックス設定

### 複合インデックス

1. **logs コレクション**:
   - `userId` + `createdAt` (降順) - ユーザーのログを時系列で取得
   - `userId` + `objectId` + `createdAt` (降順) - 特定のモノのログ履歴
   - `userId` + `emotionVector` + `createdAt` (降順) - 感情別のログ取得

2. **objects コレクション**:
   - `userId` + `lastLoggedAt` (降順) - 最近記録したモノの取得
   - `userId` + `createdAt` (降順) - モノの作成順

## データの関連性

### ObjectModel と LogModel の関係

```
ObjectModel (1) --- (n) LogModel
```

- 1つのObjectModelに対して複数のLogModelが存在
- LogModelは必ず1つのObjectModelに関連付けられる
- ObjectModelが削除されても、LogModelは保持される（ソフトデリート）

### データ整合性の保証

1. **トランザクション使用箇所**:
   - 新しいLogModel作成時のObjectModel.logCount更新
   - ObjectModel削除時の関連LogModel処理

2. **バッチ処理**:
   - 複数のLogModel一括作成
   - データ移行処理

## セキュリティルール

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // ユーザーは自分のデータのみアクセス可能
    match /users/{userId}/{document=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // プロンプトは全ユーザー読み取り可能
    match /prompts/{promptId} {
      allow read: if request.auth != null;
      allow write: if false; // 管理者のみ
    }
    
    // システム設定は読み取りのみ
    match /systemConfig/{document=**} {
      allow read: if request.auth != null;
      allow write: if false;
    }
  }
}
```

## ストレージ構造（Firebase Storage）

```
storage/
└── users/
    └── {userId}/
        └── objects/
            └── {objectId}/
                └── {timestamp}_{filename}.jpg
```

## データ移行とバージョニング

### スキーマバージョン管理

各ドキュメントに`schemaVersion`フィールドを持たせ、データ構造の変更を追跡：

```dart
final int currentSchemaVersion = 2;

// ドキュメント内
{
  "schemaVersion": 2,
  // その他のフィールド
}
```

### 移行戦略

1. **後方互換性**: 新しいフィールドはオプショナルとして追加
2. **レガシーサポート**: InsightLogモデルの読み取りサポート継続
3. **段階的移行**: バックグラウンドでのデータ変換処理

## オフライン対応

### MemoryStorageService

オフライン時のデータ一時保存：

```dart
class MemoryStorageService {
  // メモリ内キャッシュ
  Map<String, ObjectModel> _objectsCache;
  Map<String, LogModel> _logsCache;
  
  // 保留中の操作キュー
  Queue<PendingOperation> _pendingOperations;
}
```

### 同期戦略

1. **楽観的更新**: UIは即座に更新、バックグラウンドで同期
2. **競合解決**: タイムスタンプベースの最終更新優先
3. **再試行メカニズム**: 指数バックオフでの再試行

## パフォーマンス最適化

### データ取得の最適化

1. **ページネーション**: 
   - ログ一覧: 20件ずつ
   - オブジェクト一覧: 50件ずつ

2. **キャッシング**:
   - 頻繁にアクセスされるオブジェクトのメモリキャッシュ
   - 画像URLの有効期限管理

3. **遅延読み込み**:
   - 詳細データは必要時にのみ取得
   - 画像は表示領域に入ってから読み込み

## 今後の拡張計画

1. **共有機能**: オブジェクトやログの共有
2. **コラボレーション**: 複数ユーザーでのオブジェクト管理
3. **分析機能**: 感情パターンの可視化
4. **エクスポート機能**: データのバックアップと移行