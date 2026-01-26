# monolog_analytics コレクション構造定義

## 概要
`monolog_analytics`コレクションは、モノログデータの分析用に最適化された構造を持つ、非同期で保存される分析専用コレクションです。

## データ構造

```typescript
interface MonologAnalytics {
  // 基本情報
  monologId: string;          // モノログID（monologsコレクションと連携）
  userId: string;             // ユーザーID
  objectId: string;           // オブジェクトID
  timestamp: Timestamp;       // 記録時刻
  eventType: string;          // イベントタイプ（monolog_created等）
  
  // 感情データ
  tier1Emotion: string;       // 第1階層の感情
  tier2Emotion: string;       // 第2階層の感情
  
  // メモデータ
  memoLength: number;         // メモの文字数
  hasMemo: boolean;          // メモの有無
  
  // 画像データ
  hasImage: boolean;         // 画像の有無
  
  // セッションデータ
  sessionDuration: number;    // セッション時間（ミリ秒）
  emotionSelectionDuration: number; // 感情選択にかかった時間（ミリ秒）
  
  // プラットフォーム情報
  platform: string;          // プラットフォーム（iOS/Android/Web）
  appVersion: string;        // アプリバージョン
}
```

## 特徴

1. **非同期保存**: メインのモノログ保存とは独立して非同期で保存される
2. **分析最適化**: 集計・分析に必要な情報のみを抽出した構造
3. **インデックス**: userId, timestamp, tier1Emotion, objectIdにインデックスを設定

## 使用目的

- ユーザーの感情パターン分析
- オブジェクトごとの感情傾向分析
- プラットフォーム別の利用状況分析
- セッション時間の分析
- メモの利用状況分析

## 保存タイミング

1. 新規モノログ作成時（`saveMonolog`実行時）
2. 既存のモノログデータからの移行時

## クエリ例

```dart
// ユーザーの感情傾向を分析
final query = FirebaseFirestore.instance
    .collection('monolog_analytics')
    .where('userId', isEqualTo: userId)
    .where('timestamp', isGreaterThan: startDate)
    .orderBy('timestamp', descending: true);

// 特定オブジェクトの感情履歴
final query = FirebaseFirestore.instance
    .collection('monolog_analytics')
    .where('objectId', isEqualTo: objectId)
    .orderBy('timestamp', descending: true);
```

## セキュリティルール

```javascript
match /monolog_analytics/{document} {
  // 読み取りは自分のデータのみ
  allow read: if request.auth != null && request.auth.uid == resource.data.userId;
  
  // 書き込みはサーバーサイドのみ（Cloud Functions経由）
  allow write: if false;
}