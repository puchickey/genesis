# Flutter App 状態管理分析レポート

## 概要
このドキュメントは、アプリ内の状態管理パターン、BLoC構成、データ永続化戦略について詳細な分析結果をまとめたものです。

**更新日**: 2025年8月23日
**バージョン**: 0.10.3+9対応

## 1. BLoC アーキテクチャ

### 1.1 グローバルBLoC構成
アプリは6つのグローバルBLoCを使用し、`MultiBlocProvider`経由で提供されています：

| BLoC | 責任範囲 | 使用サービス |
|------|----------|-------------|
| **AuthBloc** | Firebase認証の管理 | FirebaseAuth（StreamSubscription） |
| **MonologBloc** | モノログのCRUD操作 | HybridStorageService |
| **ObjectBloc** | オブジェクト管理 | FirestoreService（直接） |
| **StoryBloc** | フォルダ組織化 | StoryService |
| **TutorialBloc** | チュートリアル進行 | SharedPreferences |
| **CameraBloc** | カメラ撮影制御 | Camera API |

### 1.2 状態アクセスパターン
```dart
// ワンタイムアクセス（コマンド送信）
context.read<MonologBloc>().add(SaveMonolog(monolog));

// リアクティブUI更新
BlocBuilder<MonologBloc, MonologState>(
  builder: (context, state) => // UI構築
)
```

## 2. データ永続化戦略

### 2.1 3層ストレージアーキテクチャ

```
┌─────────────────┐
│  画面 (Screen)  │
└────────┬────────┘
         │
┌────────▼────────┐
│   BLoC層        │
└────────┬────────┘
         │
┌────────▼─────────────────────────┐
│         サービス層                │
├──────────────┬───────────────────┤
│HybridStorage │  FirestoreService │
│  Service     │                   │
├──────────────┴───────────────────┤
│  ・Monolog用  │  ・Object用      │
│  ・ローカル   │  ・クラウド      │
│    ファースト │    ファースト    │
└──────────────────────────────────┘
```

### 2.2 データタイプ別永続化パターン

#### Monolog（モノログ）
- **保存先**: 統合コレクション`monologs`
- **実装**: `HybridStorageService.saveMonolog()`
  - ローカルファースト戦略
  - 非同期でFirestoreへバックアップ
  - 写真はローカルファイルシステムのみ
- **分析データ**: `monolog_analytics`コレクションに非同期保存

#### Object（オブジェクト）
- **保存先**: Firestore `objects`コレクション
- **実装**:
  - `ObjectBloc` → `FirestoreService`
  - 統一されたデータフロー
- **用途**: フォルダ（ストーリー）として機能

#### Custom Emotions（カスタム感情）
- **保存先**: ローカルDB（プライマリ）+ Firestore（バックアップ）
- **実装**: `EmotionService`
  - オフラインファースト設計
  - Firestoreバックアップは`custom_emotions`コレクション

## 3. 発見された問題点

### 3.1 データ重複
- ObjectモデルがFirestoreServiceとHybridStorageServiceの両方で保存可能
- StoryServiceが両方のサービスを使用（`_firestoreService.saveObject`と`_db.getObjects`）

### 3.2 不整合なデータフロー
```
ObjectBloc → FirestoreService → Firestore
    ↓
StoryService → HybridStorageService → ローカルDB
```

### 3.3 同期の複雑性
- Monolog: ローカル → Firestore（単方向）
- Object: Firestore ↔ ローカル（双方向、異なるパス）

## 4. 画面間の状態共有

### 4.1 共有メカニズム
- **グローバル状態**: MultiBlocProviderによる全画面アクセス
- **ナビゲーション**: Named routesによる画面遷移
- **データ受け渡し**: RouteSettingsのarguments

### 4.2 実装例
```dart
// SimpleHomeScreen → MonologRecordingScreen
Navigator.pushNamed(
  context,
  AppRoutes.monologRecording,
  arguments: {'objectId': selectedObject.objectId}
);

// MonologRecordingScreenでの受け取り
final args = ModalRoute.of(context)!.settings.arguments as Map;
final objectId = args['objectId'];
```

## 5. 最新のアーキテクチャ改善（実装済み）

### 5.1 Firestoreコレクション統合
- **旧構造**: 13コレクション（monolog_sessions, emotion_selections等が分散）
- **新構造**: 8コレクション（`monolog_analytics`に統合）
- **削除済み**: `insightLogs`および関連コード

### 5.2 Firebase Auth保護
- **FirebaseAuthWrapper**: PigeonUserDetailsエラー対策
- **MigrationService**: バージョン間のデータ移行
- **ユーザーIDキャッシュ**: オフライン対応強化

## 6. 改善提案（今後の課題）

### 6.1 ストレージサービスの完全統一
```dart
// 統一されたストレージインターフェース
abstract class StorageService {
  Future<void> saveObject(ObjectModel object);
  Future<List<ObjectModel>> getObjects({required String userId});
  Future<void> saveMonolog(MonologModel monolog);
  Future<List<MonologModel>> getMonologs({required String userId});
}
```

### 6.2 BLoC依存関係の整理
- 各BLoCの責任範囲をより明確に定義
- サービス層への依存を最小限に

### 6.3 パフォーマンス最適化
- 画像の遅延読み込み
- リスト表示のページネーション
- キャッシュ戦略の改善

## 7. まとめ

現在のアーキテクチャは以下の改善を経て、より堅牢になりました：

1. **Firestoreコレクション統合**: 13→8コレクションに削減、効率的なクエリ実現
2. **Firebase Auth保護**: アップグレード時のエラーに対する防御的実装
3. **オフラインファースト強化**: カスタム感情のローカル管理とバックアップ戦略

今後の課題：
- ストレージサービスの完全な統一
- パフォーマンスの継続的改善
- テストカバレッジの向上