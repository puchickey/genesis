# モノログ。 - 技術仕様書

## プロジェクト概要
- **プロジェクト名**: モノログ。(mono_log_app)
- **バージョン**: 1.0.0
- **更新日**: 2025年8月3日
- **プラットフォーム**: Flutter（クロスプラットフォーム）
- **対応OS**: iOS 12.0+、Android 5.0+（API 21+）、Web、Windows 10+、macOS 10.14+、Linux

## 技術スタック

### フロントエンド
- **フレームワーク**: Flutter 3.x
- **言語**: Dart 3.x
- **状態管理**: flutter_bloc, bloc, equatable
- **UIフレームワーク**: Material Design 3

### バックエンド
- **BaaS**: Firebase
  - Authentication: ユーザー認証
  - Firestore: NoSQLデータベース
  - Analytics: 利用分析
  - Crashlytics: クラッシュレポート
  - Remote Config: リモート設定

### ストレージ
- **ローカル**: デバイスファイルシステム（写真、SQLite）
- **クラウド**: Firebase Firestore（メタデータ）
- **ハイブリッド**: オフライン優先アーキテクチャ

## 主要な依存関係

```yaml
dependencies:
  flutter:
    sdk: flutter
  
  # Core
  camera: ^0.11.0
  tflite_flutter: ^0.11.0
  image: ^4.0.17
  flutter_bloc: ^8.1.3
  bloc: ^8.1.3
  equatable: ^2.0.5
  path_provider: ^2.1.1
  path: ^1.8.3
  image_picker: ^1.0.7
  intl: ^0.19.0
  uuid: ^4.3.3
  bloc_concurrency: ^0.2.5
  shared_preferences: ^2.2.2
  sqflite: ^2.3.0
  
  # Firebase
  firebase_core: ^2.24.2
  firebase_auth: ^4.15.3
  cloud_firestore: ^4.13.6
  firebase_analytics: ^10.7.4
  firebase_crashlytics: ^3.4.8
  firebase_remote_config: ^4.3.8
  
  # UI & Sharing
  cupertino_icons: ^1.0.8
  flutter_animate: ^4.3.0
  share_plus: ^7.2.2
  url_launcher: ^6.2.2
  google_fonts: ^6.1.0
  get_it: ^8.0.0  # Service Locator
  crypto: ^3.0.3  # Security & Hashing
```

## データモデル

### 1. MonologModel
```dart
class MonologModel {
  final String logId;           // UUID v4
  final String userId;          // Firebase UID
  final String objectId;        // Object UUID
  final String tier1Emotion;    // 第1階層感情ID
  final String tier2Emotion;    // 第2階層感情ID
  final String? memo;           // 任意メモ（最大500文字）
  final DateTime createdAt;     // 作成日時
  final DateTime? updatedAt;    // 更新日時
  final bool isDeleted;         // 論理削除フラグ
}
```

### 2. ObjectModel
```dart
class ObjectModel {
  final String objectId;        // UUID v4
  final String userId;          // Firebase UID
  final String physicalName;    // 物理名（自動生成）
  final String? customName;     // カスタム名（ユーザー定義）
  final String mainImageUrl;    // メイン画像パス
  final String? thumbnailUrl;   // サムネイル画像パス
  final List<String> tags;      // タグリスト
  final DateTime createdAt;     // 作成日時
  final DateTime? updatedAt;    // 更新日時
  final bool isArchived;        // アーカイブフラグ
}
```

### 3. EmotionTier
```dart
class EmotionTier {
  final String id;              // 感情ID
  final String label;           // 表示ラベル
  final String emoji;           // 絵文字
  final Color primaryColor;     // プライマリカラー
  final Color secondaryColor;   // セカンダリカラー
  final List<EmotionTier>? tier2Emotions; // 第2階層感情
}
```

### 4. TutorialProgress
```dart
class TutorialProgress {
  final String userId;          // Firebase UID
  final TutorialStage currentStage; // 現在のステージ
  final int completedSteps;     // 完了ステップ数
  final DateTime startedAt;     // 開始日時
  final DateTime? completedAt;  // 完了日時
  final bool isSkipped;         // スキップフラグ
}
```

## API仕様

### Firestore コレクション構造

```
firestore/
├── users/
│   └── {userId}/
│       ├── profile
│       ├── settings
│       └── tutorial_progress
├── objects/
│   └── {userId}/
│       └── items/
│           └── {objectId}
├── monologs/
│   └── {userId}/
│       └── logs/
│           └── {logId}
└── system/
    ├── emotions
    ├── crisis_keywords
    └── app_config
```

### データ操作API

#### 1. モノログ作成
```dart
Future<MonologModel> createMonolog({
  required String userId,
  required String objectId,
  required String tier1Emotion,
  required String tier2Emotion,
  String? memo,
}) async {
  final logId = Uuid().v4();
  final monolog = MonologModel(
    logId: logId,
    userId: userId,
    objectId: objectId,
    tier1Emotion: tier1Emotion,
    tier2Emotion: tier2Emotion,
    memo: memo,
    createdAt: DateTime.now(),
    isDeleted: false,
  );
  
  await firestore
    .collection('monologs')
    .doc(userId)
    .collection('logs')
    .doc(logId)
    .set(monolog.toJson());
    
  return monolog;
}
```

#### 2. オブジェクト検索
```dart
Stream<List<ObjectModel>> searchObjects({
  required String userId,
  String? searchQuery,
  List<String>? tags,
  bool includeArchived = false,
}) {
  Query query = firestore
    .collection('objects')
    .doc(userId)
    .collection('items');
    
  if (!includeArchived) {
    query = query.where('isArchived', isEqualTo: false);
  }
  
  if (tags != null && tags.isNotEmpty) {
    query = query.where('tags', arrayContainsAny: tags);
  }
  
  return query
    .orderBy('createdAt', descending: true)
    .snapshots()
    .map((snapshot) => 
      snapshot.docs.map((doc) => 
        ObjectModel.fromJson(doc.data() as Map<String, dynamic>)
      ).toList()
    );
}
```

## セキュリティ要件

### 1. 認証・認可
- Firebase Authentication による認証
- ユーザーは自分のデータのみアクセス可能
- Firestore Security Rules による厳格なアクセス制御

### 2. データ保護
```javascript
// Firestore Security Rules
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // ユーザーは自分のデータのみアクセス可能
    match /users/{userId}/{document=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    match /objects/{userId}/{document=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    match /monologs/{userId}/{document=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // システムデータは読み取りのみ
    match /system/{document=**} {
      allow read: if request.auth != null;
      allow write: if false;
    }
  }
}
```

### 3. データ暗号化
- 写真のローカル保存時の暗号化（オプション）
- HTTPS通信の強制
- 機密情報のハッシュ化

```dart
// 暗号化ユーティリティ
import 'package:crypto/crypto.dart';

class CryptoUtil {
  static String hashText(String text) {
    final bytes = utf8.encode(text);
    final digest = sha256.convert(bytes);
    return digest.toString();
  }
  
  static String generateSecureFileName() {
    final timestamp = DateTime.now().millisecondsSinceEpoch;
    final random = Random.secure().nextInt(999999);
    return hashText('$timestamp-$random');
  }
}
```

### 4. プライバシー保護
- 位置情報の非収集
- 最小限のパーミッション要求
- ユーザーデータの完全削除機能
- GDPR/CCPA準拠

## パフォーマンス仕様

### 1. レスポンス時間要件
- 画面遷移: < 300ms
- 画像読み込み: < 1s
- データ保存: < 2s
- 検索結果表示: < 500ms

### 2. キャッシュ戦略
```dart
class CacheManager {
  static const Duration imageCacheDuration = Duration(days: 7);
  static const int maxCacheSize = 100 * 1024 * 1024; // 100MB
  
  // 画像キャッシュ
  final Map<String, CachedImage> _imageCache = {};
  
  // メモリ管理
  void cleanupCache() {
    final now = DateTime.now();
    _imageCache.removeWhere((key, value) => 
      now.difference(value.cachedAt) > imageCacheDuration
    );
  }
}
```

### 3. 最適化手法
- 画像の遅延読み込み
- リストの仮想スクロール
- データのページネーション
- 不要な再ビルドの防止

## エラーハンドリング

### 1. エラーコード体系
```dart
enum ErrorCode {
  // ネットワークエラー (1xxx)
  NETWORK_UNAVAILABLE(1001, 'ネットワーク接続がありません'),
  TIMEOUT(1002, 'タイムアウトしました'),
  
  // ストレージエラー (2xxx)
  STORAGE_FULL(2001, 'ストレージ容量が不足しています'),
  FILE_NOT_FOUND(2002, 'ファイルが見つかりません'),
  
  // 認証エラー (3xxx)
  UNAUTHORIZED(3001, '認証が必要です'),
  TOKEN_EXPIRED(3002, 'セッションの有効期限が切れました'),
  
  // アプリケーションエラー (4xxx)
  INVALID_INPUT(4001, '入力値が不正です'),
  OPERATION_FAILED(4002, '操作に失敗しました');
  
  final int code;
  final String message;
  
  const ErrorCode(this.code, this.message);
}
```

### 2. エラー通知
```dart
class ErrorNotifier {
  static void notifyError(BuildContext context, ErrorCode error) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(error.message),
        backgroundColor: Colors.red,
        action: SnackBarAction(
          label: '詳細',
          onPressed: () => _showErrorDetails(context, error),
        ),
      ),
    );
  }
}
```

## テスト仕様

### 1. テストカバレッジ要件
- ユニットテスト: 80%以上
- ウィジェットテスト: 70%以上
- 統合テスト: 主要フロー100%

### 2. テスト環境
```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^5.0.0
  
  # Testing frameworks
  bloc_test: ^9.1.5
  mockito: ^5.4.4
  mocktail: ^1.0.3
  build_runner: ^2.4.9
  json_annotation: ^4.9.0
  fake_cloud_firestore: ^2.4.6
  
  # Integration testing
  integration_test:
    sdk: flutter
```

### 3. テストデータ
```dart
class TestData {
  static final testUser = UserModel(
    userId: 'test_user_001',
    email: 'test@example.com',
    createdAt: DateTime(2024, 1, 1),
  );
  
  static final testObject = ObjectModel(
    objectId: 'test_object_001',
    userId: testUser.userId,
    physicalName: 'テストオブジェクト',
    mainImageUrl: 'test/path/image.jpg',
    createdAt: DateTime(2024, 1, 1),
  );
  
  static final testMonolog = MonologModel(
    logId: 'test_log_001',
    userId: testUser.userId,
    objectId: testObject.objectId,
    tier1Emotion: 'happy',
    tier2Emotion: 'excited',
    memo: 'テストメモ',
    createdAt: DateTime(2024, 1, 1),
  );
}
```

## 監視・ロギング

### 1. Analytics イベント
```dart
class AnalyticsEvents {
  // ユーザーアクション
  static const String PHOTO_CAPTURED = 'photo_captured';
  static const String EMOTION_SELECTED = 'emotion_selected';
  static const String MONOLOG_CREATED = 'monolog_created';
  static const String TUTORIAL_COMPLETED = 'tutorial_completed';
  
  // エラーイベント
  static const String ERROR_OCCURRED = 'error_occurred';
  static const String CRASH_REPORTED = 'crash_reported';
  
  // パフォーマンス
  static const String SCREEN_LOAD_TIME = 'screen_load_time';
  static const String API_RESPONSE_TIME = 'api_response_time';
}
```

### 2. ログレベル
```dart
enum LogLevel {
  DEBUG,    // 開発時のみ
  INFO,     // 一般情報
  WARNING,  // 警告
  ERROR,    // エラー
  CRITICAL  // 致命的エラー
}

class Logger {
  static void log(LogLevel level, String message, [dynamic data]) {
    if (kDebugMode || level.index >= LogLevel.WARNING.index) {
      print('[${level.name}] $message');
      if (data != null) print('Data: $data');
    }
    
    // Crashlyticsへの送信
    if (level.index >= LogLevel.ERROR.index) {
      FirebaseCrashlytics.instance.log('[$level] $message');
    }
  }
}
```

## デプロイメント要件

### 1. ビルド設定
- 最小SDKバージョン
  - Android: API 21 (Android 5.0)
  - iOS: 12.0
- コード圧縮・難読化の有効化
- ProGuardルールの設定

### 2. 署名設定
```gradle
// android/app/build.gradle
android {
    signingConfigs {
        release {
            keyAlias keystoreProperties['keyAlias']
            keyPassword keystoreProperties['keyPassword']
            storeFile keystoreProperties['storeFile'] ? file(keystoreProperties['storeFile']) : null
            storePassword keystoreProperties['storePassword']
        }
    }
    
    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
}
```

### 3. 環境変数
```dart
// 環境別設定
class Config {
  static const Map<String, dynamic> development = {
    'apiUrl': 'https://dev-api.monolog.app',
    'enableLogging': true,
    'enableCrashlytics': false,
  };
  
  static const Map<String, dynamic> staging = {
    'apiUrl': 'https://staging-api.monolog.app',
    'enableLogging': true,
    'enableCrashlytics': true,
  };
  
  static const Map<String, dynamic> production = {
    'apiUrl': 'https://api.monolog.app',
    'enableLogging': false,
    'enableCrashlytics': true,
  };
}
```

## 互換性マトリックス

| プラットフォーム | 最小バージョン | 推奨バージョン | 備考 |
|---|---|---|---|
| iOS | 12.0 | 16.0+ | カメラ機能はiOS 13.0以上推奨 |
| Android | API 21 (5.0) | API 30+ (11.0+) | カメラ2 API対応 |
| Web | Chrome 84+ | 最新版 | WebRTC対応ブラウザ必須 |
| Windows | Windows 10 1803+ | Windows 11 | .NET Framework 4.7.2以上 |
| macOS | 10.14 (Mojave) | 13.0+ (Ventura) | Metal対応GPU推奨 |
| Linux | Ubuntu 18.04+ | Ubuntu 22.04+ | GTK 3.0以上 |

## まとめ

本技術仕様書では、モノログ。アプリの技術的な詳細について定義しました。これらの仕様に準拠することで、安定性、セキュリティ、パフォーマンスを確保しながら、優れたユーザー体験を提供できます。

仕様は継続的に見直し、技術の進歩やユーザーニーズの変化に応じて更新していく必要があります。
