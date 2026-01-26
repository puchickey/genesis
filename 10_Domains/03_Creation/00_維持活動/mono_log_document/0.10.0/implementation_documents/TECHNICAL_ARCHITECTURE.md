# モノログアプリ技術アーキテクチャ仕様書

## 概要

本ドキュメントは、モノログアプリの技術アーキテクチャと実装詳細を包括的に説明します。このアプリは、ユーザーが日常の物事に対する感情を記録し、振り返ることができるFlutterベースのモバイルアプリケーションです。

## アーキテクチャ概要

### システム構成

```
┌─────────────────────────────────────────────────────────┐
│                     Flutter App                         │
├─────────────────────────────────────────────────────────┤
│                  Presentation Layer                     │
│              (Screens & Widgets)                        │
├─────────────────────────────────────────────────────────┤
│                  Business Logic Layer                   │
│              (Services & Utilities)                     │
├─────────────────────────────────────────────────────────┤
│                    Data Layer                           │
│         ┌──────────────┬──────────────┐                │
│         │   SQLite     │  File System │                │
│         │  Database    │   (Images)   │                │
│         └──────────────┴──────────────┘                │
├─────────────────────────────────────────────────────────┤
│                  External Services                      │
│         ┌──────────────┬──────────────┐                │
│         │   Firebase   │   Firebase   │                │
│         │     Auth     │  Firestore   │                │
│         └──────────────┴──────────────┘                │
└─────────────────────────────────────────────────────────┘
```

### コアプリンシプル

1. **ローカルファースト**: すべてのユーザーデータはデバイス上に保存
2. **プライバシー重視**: 個人情報のクラウド送信を最小限に
3. **オフライン対応**: ネットワーク接続なしで完全動作
4. **段階的な機能拡張**: 基本機能から高度な機能へ

## データモデル

### 1. モノログ（Monolog）

```dart
class MonologModel {
  final String monologId;       // UUID v4
  final String userId;          // Firebase Auth UID
  final String objectId;        // 関連するオブジェクトID
  final String tier1Emotion;    // 第1階層感情（喜び、悲しみ等）
  final String tier2Emotion;    // 第2階層感情（わくわく、感動等）
  final int intensity;          // 感情の強度（1-5）
  final String? memo;           // ユーザーメモ（暗号化保存）
  final List<String> imagePaths; // ローカル画像パス
  final DateTime createdAt;     // 作成日時
  final DateTime updatedAt;     // 更新日時
  final bool isDeleted;         // 論理削除フラグ
  final bool isAnalyticsSent;   // 分析送信済みフラグ
}
```

### 2. オブジェクト（Object）

```dart
class ObjectModel {
  final String objectId;        // UUID v4
  final String userId;          // Firebase Auth UID
  final String objectName;      // オブジェクト名
  final String? customName;     // カスタム名（ユーザー定義）
  final String? imagePath;      // サムネイル画像パス
  final DateTime createdAt;     // 作成日時
  final Map<String, dynamic> metadata; // 拡張メタデータ
}
```

### 3. カスタム感情（CustomEmotion）

```dart
class CustomEmotionModel {
  final String emotionId;       // UUID v4
  final String userId;          // Firebase Auth UID
  final String category;        // 所属カテゴリ（tier1）
  final String emotionName;     // カスタム感情名
  final String? colorCode;      // 表示色（HEX）
  final int sortOrder;          // 表示順
  final bool isActive;          // 有効/無効フラグ
  final DateTime createdAt;     // 作成日時
}
```

## サービスアーキテクチャ

### 1. HybridStorageService（ハイブリッドストレージ）

**責務**: ローカルストレージとクラウドストレージの統合管理

```dart
class HybridStorageService {
  // 主要機能
  - saveMonolog()      // モノログの保存（ローカル＋分析）
  - deleteMonolog()    // モノログの削除
  - saveImages()       // 画像の最適化と保存
  - encryptMemo()      // メモの暗号化
  - syncAnalytics()    // 分析データの同期
}
```

**画像処理フロー**:
1. 画像サイズチェック（20MB制限）
2. 自動リサイズ（1920x1920以下）
3. JPEG圧縮（品質85%）
4. ローカルディレクトリに保存
5. メタデータ削除（プライバシー保護）

### 2. DatabaseHelper（データベース管理）

**責務**: SQLiteデータベースの管理とクエリ実行

```dart
class DatabaseHelper {
  // データベース操作
  - createMonolog()    // モノログ作成
  - updateMonolog()    // モノログ更新
  - deleteMonolog()    // 論理削除
  - getMonologs()      // 条件検索
  
  // トランザクション管理
  - transaction()      // ACID保証
  - batch()           // バッチ処理
  
  // マイグレーション
  - _upgradeDB()      // スキーマ更新
  - _backupDatabase() // 自動バックアップ
}
```

### 3. SecurityService（セキュリティ）

**責務**: 暗号化とセキュアストレージ管理

```dart
class SecurityService {
  // 暗号化
  - generateEncryptionKey()  // デバイス固有キー生成
  - encryptData()           // XOR暗号化
  - decryptData()           // 復号化
  
  // セキュアストレージ
  - saveSecureData()        // Keychain/KeyStore保存
  - getSecureData()         // セキュアデータ取得
  - deleteSecureData()      // セキュアデータ削除
  
  // 認証情報管理
  - saveUserId()            // ユーザーID保存
  - hashPassword()          // パスワードハッシュ化
}
```

### 4. AuthService（認証）

**責務**: Firebase認証とユーザー管理

```dart
class AuthService {
  // 認証フロー
  - signInAnonymously()     // 匿名認証
  - linkEmailPassword()     // アカウントアップグレード
  - signOut()              // サインアウト
  
  // ユーザー管理
  - getCurrentUserId()      // 現在のユーザーID
  - isEmailLinked()        // メールリンク状態
  - deleteAccount()        // アカウント削除
}
```

### 5. FirestoreService（クラウドデータ）

**責務**: Firestoreとの通信管理

```dart
class FirestoreService {
  // 分析データ
  - sendAnalyticsData()     // 匿名化データ送信
  - batchAnalytics()        // バッチ送信
  
  // プレミアム機能（将来）
  - backupUserData()        // データバックアップ
  - restoreUserData()       // データ復元
  - syncSettings()          // 設定同期
}
```

## エラーハンドリング

### UnifiedErrorHandler

統一されたエラーハンドリング機構により、一貫したエラー処理を実現：

```dart
class UnifiedErrorHandler {
  static Future<T> handle<T>({
    required Future<T> Function() operation,
    required String operationName,
    T? fallbackValue,
    Duration timeout = const Duration(seconds: 30),
    int maxRetries = 2,
  });
}
```

**エラー分類**:
- `NetworkError`: ネットワーク関連
- `AuthenticationError`: 認証関連
- `DatabaseError`: データベース関連
- `ValidationError`: 入力検証
- `StorageError`: ストレージ関連

## UI/UXアーキテクチャ

### 画面構成

1. **ホーム画面** (`HomeScreen`)
   - 最近のモノログ一覧
   - クイックアクセスボタン
   - ナビゲーション

2. **モノログ記録画面** (`RecordMonologScreen`)
   - オブジェクト選択/作成
   - 感情選択（2階層）
   - 強度選択
   - メモ入力
   - 画像添付

3. **マイログ画面** (`MyLogsScreen`)
   - タブ切り替え（すべて/フォルダ別）
   - フィルタリング
   - 検索機能

4. **振り返り画面** (`LookbackScreen`)
   - 統計表示
   - グラフ表示
   - 期間選択

### コンポーネント設計

#### DebounceButton（連打防止ボタン）

```dart
class DebounceButton extends StatefulWidget {
  final VoidCallback? onPressed;
  final Future<void> Function()? onPressedAsync;
  final Widget child;
  final Duration debounceDuration;
  
  // 統一されたボタンスタイル
  // ローディング状態の自動管理
  // エラーハンドリング
}
```

## パフォーマンス最適化

### 1. データベース最適化

- **インデックス戦略**
  - user_id, object_id, created_at にインデックス
  - 複合インデックスで検索高速化

- **クエリ最適化**
  - ページネーション実装
  - 遅延ローディング
  - キャッシュ活用

### 2. 画像処理最適化

- **プログレッシブ画像読み込み**
  - サムネイル先行表示
  - 段階的な高解像度読み込み

- **メモリ管理**
  - 画像キャッシュサイズ制限
  - 自動メモリ解放

### 3. UIレスポンス最適化

- **非同期処理**
  - Heavy処理のIsolate実行
  - StreamBuilderによる逐次更新

- **状態管理**
  - 必要最小限の再ビルド
  - ValueNotifierによる軽量通知

## セキュリティとプライバシー

### データ保護の層

1. **アプリケーション層**
   - 入力検証
   - XSS対策
   - SQLインジェクション対策

2. **データ層**
   - 暗号化（メモフィールド）
   - アクセス制御（user_id分離）
   - 論理削除

3. **ストレージ層**
   - FlutterSecureStorage
   - ファイルシステム権限
   - アプリサンドボックス

4. **ネットワーク層**
   - HTTPS通信
   - 証明書検証
   - タイムアウト設定

### プライバシー設計

- **データ最小化原則**
  - 必要最小限のデータ収集
  - 匿名化された分析データ

- **ユーザーコントロール**
  - 分析オプトアウト
  - データエクスポート
  - アカウント削除

## 拡張性とモジュール性

### プラグインアーキテクチャ

将来の機能拡張に備えた設計：

```dart
abstract class FeaturePlugin {
  String get featureId;
  bool get requiresPremium;
  Future<void> initialize();
  Widget buildUI(BuildContext context);
}
```

### 設定管理

```dart
class SettingsManager {
  // ローカル設定
  - theme, language, notifications
  
  // プレミアム設定
  - cloudBackup, advancedAnalytics
  
  // 実験的機能
  - featureFlags, betaFeatures
}
```

## テストとデバッグ

### テスト戦略

1. **単体テスト**
   - サービスクラス
   - ユーティリティ関数
   - データモデル

2. **統合テスト**
   - データベース操作
   - 認証フロー
   - 画像処理

3. **UIテスト**
   - 画面遷移
   - ユーザー操作
   - エラー表示

### デバッグツール

- **ログシステム**
  - レベル別ログ出力
  - ファイル出力オプション
  - クラッシュレポート

- **開発者モード**
  - デバッグ情報表示
  - パフォーマンスモニター
  - ネットワークインスペクター

## デプロイメントとCI/CD

### ビルド設定

- **環境別設定**
  - Development
  - Staging  
  - Production

- **機能フラグ**
  - 段階的ロールアウト
  - A/Bテスト
  - 緊急無効化

### リリースプロセス

1. 自動テスト実行
2. コード品質チェック
3. セキュリティスキャン
4. ビルド生成
5. 内部テスト配布
6. 段階的リリース

## まとめ

本アプリケーションは、ユーザープライバシーを最優先に設計された、ローカルファーストのアーキテクチャを採用しています。モジュール化された設計により、将来の機能拡張や課金機能の追加にも柔軟に対応できる構造となっています。