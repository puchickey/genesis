# 技術アーキテクチャ仕様書

このドキュメントでは、モノログアプリの技術的なアーキテクチャ、設計パターン、および実装の詳細について説明します。

## 目次

1. [アーキテクチャ概要](#アーキテクチャ概要)
2. [技術スタック](#技術スタック)
3. [アプリケーション構造](#アプリケーション構造)
4. [状態管理](#状態管理)
5. [データ層](#データ層)
6. [プレゼンテーション層](#プレゼンテーション層)
7. [ビジネスロジック層](#ビジネスロジック層)
8. [外部サービス連携](#外部サービス連携)
9. [セキュリティ](#セキュリティ)
10. [パフォーマンス最適化](#パフォーマンス最適化)

## アーキテクチャ概要

モノログアプリは、クリーンアーキテクチャの原則に基づいた層構造を採用しています。

```
┌─────────────────────────────────────────────┐
│          Presentation Layer                  │
│         (Screens & Widgets)                  │
├─────────────────────────────────────────────┤
│         State Management Layer               │
│            (BLoC Pattern)                    │
├─────────────────────────────────────────────┤
│        Business Logic Layer                  │
│       (ViewModels & Services)                │
├─────────────────────────────────────────────┤
│            Data Layer                        │
│   (Repositories & Data Sources)              │
├─────────────────────────────────────────────┤
│         External Services                    │
│    (Firebase, Camera, Storage)               │
└─────────────────────────────────────────────┘
```

## 技術スタック

### コア技術

| 技術 | バージョン | 用途 |
|-----|-----------|------|
| Flutter | 3.24.5 | UIフレームワーク |
| Dart | >=3.5.0 | プログラミング言語 |
| flutter_bloc | ^8.1.6 | 状態管理 |
| get_it | ^8.0.2 | 依存性注入 |

### Firebase関連

| パッケージ | バージョン | 用途 |
|-----------|-----------|------|
| firebase_core | ^3.8.1 | Firebase初期化 |
| firebase_auth | ^5.3.4 | 認証 |
| cloud_firestore | ^5.5.1 | データベース |
| firebase_storage | ^12.3.7 | ファイルストレージ |
| firebase_crashlytics | ^4.2.0 | クラッシュレポート |

### UI/UX関連

| パッケージ | バージョン | 用途 |
|-----------|-----------|------|
| google_fonts | ^6.2.1 | カスタムフォント |
| flutter_svg | ^2.0.10+1 | SVG画像表示 |
| photo_view | ^0.15.0 | 画像ズーム |
| introduction_screen | ^3.1.14 | オンボーディング |

### その他の主要パッケージ

| パッケージ | バージョン | 用途 |
|-----------|-----------|------|
| camera | ^0.11.0+2 | カメラ機能 |
| image_picker | ^1.1.2 | 画像選択 |
| path_provider | ^2.1.5 | ファイルパス管理 |
| shared_preferences | ^2.3.3 | ローカル設定保存 |
| intl | ^0.19.0 | 国際化 |

## アプリケーション構造

### ディレクトリ構造

```
lib/
├── main.dart                    # エントリーポイント
├── models/                      # データモデル
│   ├── object_models.dart       # ObjectModel, LogModel
│   ├── diagnosis_models.dart    # DiagnosisModel
│   ├── insight_log.dart         # InsightLog (レガシー)
│   └── prompt_models.dart       # PromptModel
├── screens/                     # 画面コンポーネント（23画面）
│   ├── auth/                    # 認証関連画面
│   ├── home/                    # ホーム画面
│   ├── camera/                  # カメラ関連画面
│   ├── journaling/              # 内省記録画面
│   ├── logs/                    # ログ管理画面
│   └── settings/                # 設定画面
├── services/                    # ビジネスロジック
│   ├── auth_service.dart        # 認証サービス
│   ├── firestore_service.dart   # Firestoreサービス
│   ├── storage_service.dart     # ストレージサービス
│   └── memory_storage_service.dart # オフライン対応
├── viewmodels/                  # ViewModels (BLoC)
│   ├── monolog_flow_viewmodel.dart
│   ├── object_viewmodel.dart
│   └── diagnosis_viewmodel.dart
├── widgets/                     # 再利用可能なウィジェット
│   ├── common/                  # 共通ウィジェット
│   ├── buttons/                 # ボタンコンポーネント
│   └── cards/                   # カードコンポーネント
├── utils/                       # ユーティリティ
│   ├── constants.dart           # 定数定義
│   ├── validators.dart          # バリデーション
│   └── extensions.dart          # 拡張メソッド
└── config/                      # 設定ファイル
    ├── firebase_options.dart    # Firebase設定
    └── app_config.dart          # アプリ設定
```

## 状態管理

### BLoCパターンの実装

```dart
// ViewModelの例: MonologFlowViewModel
class MonologFlowViewModel extends Cubit<MonologFlowState> {
  final FirestoreService _firestoreService;
  final AuthService _authService;
  
  MonologFlowViewModel({
    required FirestoreService firestoreService,
    required AuthService authService,
  }) : _firestoreService = firestoreService,
       _authService = authService,
       super(MonologFlowInitial());
  
  // 感情ベクター選択
  void selectEmotionVector(String vector) {
    emit(MonologFlowVectorSelected(vector));
  }
  
  // ログ保存
  Future<void> saveLog(LogModel log) async {
    emit(MonologFlowLoading());
    try {
      await _firestoreService.saveLog(log);
      emit(MonologFlowSuccess());
    } catch (e) {
      emit(MonologFlowError(e.toString()));
    }
  }
}
```

### 状態クラスの定義

```dart
abstract class MonologFlowState {}

class MonologFlowInitial extends MonologFlowState {}

class MonologFlowVectorSelected extends MonologFlowState {
  final String vector;
  MonologFlowVectorSelected(this.vector);
}

class MonologFlowLoading extends MonologFlowState {}

class MonologFlowSuccess extends MonologFlowState {}

class MonologFlowError extends MonologFlowState {
  final String message;
  MonologFlowError(this.message);
}
```

## データ層

### Firestoreサービス実装

```dart
class FirestoreService {
  final FirebaseFirestore _firestore = FirebaseFirestore.instance;
  
  // コレクション参照
  CollectionReference<Map<String, dynamic>> _usersCollection() =>
      _firestore.collection('users');
  
  // ObjectModelの保存
  Future<String> saveObject(ObjectModel object) async {
    final doc = _usersCollection()
        .doc(object.userId)
        .collection('objects')
        .doc();
    
    await doc.set(object.copyWith(id: doc.id).toJson());
    return doc.id;
  }
  
  // LogModelの保存（トランザクション使用）
  Future<void> saveLog(LogModel log) async {
    await _firestore.runTransaction((transaction) async {
      // ObjectModelのlogCountを更新
      final objectRef = _usersCollection()
          .doc(log.userId)
          .collection('objects')
          .doc(log.objectId);
      
      final objectSnapshot = await transaction.get(objectRef);
      final currentLogCount = objectSnapshot.data()?['logCount'] ?? 0;
      
      // ログを保存
      final logRef = _usersCollection()
          .doc(log.userId)
          .collection('logs')
          .doc();
      
      transaction.set(logRef, log.copyWith(id: logRef.id).toJson());
      
      // ObjectModelを更新
      transaction.update(objectRef, {
        'logCount': currentLogCount + 1,
        'lastLoggedAt': FieldValue.serverTimestamp(),
      });
    });
  }
}
```

### オフライン対応

```dart
class MemoryStorageService {
  final Map<String, ObjectModel> _objectsCache = {};
  final Map<String, LogModel> _logsCache = {};
  final Queue<PendingOperation> _pendingOperations = Queue();
  
  // オフライン時の保存
  Future<void> saveOffline(LogModel log) async {
    _logsCache[log.id] = log;
    _pendingOperations.add(
      PendingOperation(
        type: OperationType.create,
        collection: 'logs',
        data: log.toJson(),
      ),
    );
  }
  
  // オンライン復帰時の同期
  Future<void> syncPendingOperations() async {
    while (_pendingOperations.isNotEmpty) {
      final operation = _pendingOperations.removeFirst();
      try {
        await _executePendingOperation(operation);
      } catch (e) {
        // 再試行キューに戻す
        _pendingOperations.add(operation);
        break;
      }
    }
  }
}
```

## プレゼンテーション層

### 画面の基本構造

```dart
class MicroJournalingScreen extends StatefulWidget {
  final String objectId;
  final String imageUrl;
  
  const MicroJournalingScreen({
    Key? key,
    required this.objectId,
    required this.imageUrl,
  }) : super(key: key);
  
  @override
  State<MicroJournalingScreen> createState() => _MicroJournalingScreenState();
}

class _MicroJournalingScreenState extends State<MicroJournalingScreen> {
  late final MonologFlowViewModel _viewModel;
  
  @override
  void initState() {
    super.initState();
    _viewModel = GetIt.I<MonologFlowViewModel>();
  }
  
  @override
  Widget build(BuildContext context) {
    return BlocProvider.value(
      value: _viewModel,
      child: BlocConsumer<MonologFlowViewModel, MonologFlowState>(
        listener: (context, state) {
          if (state is MonologFlowError) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text(state.message)),
            );
          }
        },
        builder: (context, state) {
          return Scaffold(
            body: _buildBody(state),
          );
        },
      ),
    );
  }
}
```

### カスタムウィジェット

```dart
// カメラボタンのアニメーション
class AnimatedCameraButton extends StatefulWidget {
  final VoidCallback onPressed;
  
  const AnimatedCameraButton({
    Key? key,
    required this.onPressed,
  }) : super(key: key);
  
  @override
  State<AnimatedCameraButton> createState() => _AnimatedCameraButtonState();
}

class _AnimatedCameraButtonState extends State<AnimatedCameraButton>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scaleAnimation;
  
  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(seconds: 2),
      vsync: this,
    )..repeat(reverse: true);
    
    _scaleAnimation = Tween<double>(
      begin: 1.0,
      end: 1.1,
    ).animate(CurvedAnimation(
      parent: _controller,
      curve: Curves.easeInOut,
    ));
  }
}
```

## ビジネスロジック層

### 認証サービス

```dart
class AuthService {
  final FirebaseAuth _auth = FirebaseAuth.instance;
  
  // 匿名認証
  Future<User?> signInAnonymously() async {
    try {
      final credential = await _auth.signInAnonymously();
      return credential.user;
    } catch (e) {
      throw AuthException('認証に失敗しました: $e');
    }
  }
  
  // ユーザー状態の監視
  Stream<User?> get authStateChanges => _auth.authStateChanges();
  
  // 現在のユーザー
  User? get currentUser => _auth.currentUser;
}
```

### 画像処理サービス

```dart
class ImageService {
  // 画像の圧縮
  Future<Uint8List> compressImage(String imagePath) async {
    final file = File(imagePath);
    final bytes = await file.readAsBytes();
    
    final image = img.decodeImage(bytes);
    if (image == null) throw Exception('画像のデコードに失敗');
    
    // 最大幅1080pxにリサイズ
    final resized = img.copyResize(
      image,
      width: image.width > 1080 ? 1080 : image.width,
    );
    
    // JPEG品質80%で圧縮
    return Uint8List.fromList(
      img.encodeJpg(resized, quality: 80),
    );
  }
  
  // Firebase Storageへのアップロード
  Future<String> uploadImage(String userId, String objectId, Uint8List imageData) async {
    final storage = FirebaseStorage.instance;
    final timestamp = DateTime.now().millisecondsSinceEpoch;
    final ref = storage.ref().child('users/$userId/objects/$objectId/${timestamp}_image.jpg');
    
    final uploadTask = ref.putData(imageData);
    final snapshot = await uploadTask;
    return await snapshot.ref.getDownloadURL();
  }
}
```

## 外部サービス連携

### Firebase初期化

```dart
// main.dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Firebase初期化
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  
  // 依存性注入の設定
  await setupDependencies();
  
  // Crashlyticsの設定
  FlutterError.onError = FirebaseCrashlytics.instance.recordFlutterFatalError;
  
  runApp(const MonologApp());
}
```

### 依存性注入の設定

```dart
Future<void> setupDependencies() async {
  final getIt = GetIt.instance;
  
  // Services
  getIt.registerLazySingleton(() => AuthService());
  getIt.registerLazySingleton(() => FirestoreService());
  getIt.registerLazySingleton(() => ImageService());
  getIt.registerLazySingleton(() => MemoryStorageService());
  
  // ViewModels
  getIt.registerFactory(() => MonologFlowViewModel(
    firestoreService: getIt<FirestoreService>(),
    authService: getIt<AuthService>(),
  ));
  
  getIt.registerFactory(() => ObjectViewModel(
    firestoreService: getIt<FirestoreService>(),
  ));
}
```

## セキュリティ

### Firestoreセキュリティルール

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // ユーザーは自分のデータのみアクセス可能
    match /users/{userId}/{document=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // プロンプトは認証済みユーザーなら誰でも読み取り可能
    match /prompts/{promptId} {
      allow read: if request.auth != null;
      allow write: if false; // 管理者のみ（Cloud Functions経由）
    }
  }
}
```

### Storageセキュリティルール

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /users/{userId}/{allPaths=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

### アプリ内セキュリティ

```dart
// 入力値のサニタイズ
class Validators {
  static String? validateObjectName(String? value) {
    if (value == null || value.isEmpty) {
      return 'モノの名前を入力してください';
    }
    if (value.length > 50) {
      return '50文字以内で入力してください';
    }
    // XSS対策
    final sanitized = value.replaceAll(RegExp(r'<[^>]*>'), '');
    if (sanitized != value) {
      return '使用できない文字が含まれています';
    }
    return null;
  }
}
```

## パフォーマンス最適化

### 画像の遅延読み込み

```dart
class LazyImageWidget extends StatelessWidget {
  final String imageUrl;
  
  const LazyImageWidget({
    Key? key,
    required this.imageUrl,
  }) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return CachedNetworkImage(
      imageUrl: imageUrl,
      placeholder: (context, url) => const CircularProgressIndicator(),
      errorWidget: (context, url, error) => const Icon(Icons.error),
      fadeInDuration: const Duration(milliseconds: 300),
      memCacheHeight: 300, // メモリキャッシュサイズ制限
    );
  }
}
```

### リストのページネーション

```dart
class PaginatedLogsList extends StatefulWidget {
  @override
  State<PaginatedLogsList> createState() => _PaginatedLogsListState();
}

class _PaginatedLogsListState extends State<PaginatedLogsList> {
  static const _pageSize = 20;
  DocumentSnapshot? _lastDocument;
  bool _hasMore = true;
  
  Future<void> _loadMore() async {
    if (!_hasMore) return;
    
    Query query = FirebaseFirestore.instance
        .collection('users')
        .doc(userId)
        .collection('logs')
        .orderBy('createdAt', descending: true)
        .limit(_pageSize);
    
    if (_lastDocument != null) {
      query = query.startAfterDocument(_lastDocument!);
    }
    
    final snapshot = await query.get();
    
    if (snapshot.docs.length < _pageSize) {
      _hasMore = false;
    }
    
    if (snapshot.docs.isNotEmpty) {
      _lastDocument = snapshot.docs.last;
    }
  }
}
```

### メモリ管理

```dart
// 画面破棄時のリソース解放
@override
void dispose() {
  _animationController?.dispose();
  _streamSubscription?.cancel();
  _scrollController?.dispose();
  super.dispose();
}
```

## エラーハンドリング

### グローバルエラーハンドラー

```dart
void main() {
  // Flutter エラーハンドリング
  FlutterError.onError = (FlutterErrorDetails details) {
    FirebaseCrashlytics.instance.recordFlutterFatalError(details);
  };
  
  // Dart エラーハンドリング
  PlatformDispatcher.instance.onError = (error, stack) {
    FirebaseCrashlytics.instance.recordError(error, stack, fatal: true);
    return true;
  };
  
  runApp(const MonologApp());
}
```

### サービス層のエラーハンドリング

```dart
class FirestoreService {
  Future<T> _handleFirestoreOperation<T>(Future<T> Function() operation) async {
    try {
      return await operation();
    } on FirebaseException catch (e) {
      throw DataException('データ操作エラー: ${e.message}');
    } on TimeoutException catch (_) {
      throw DataException('タイムアウトエラー');
    } catch (e) {
      throw DataException('予期しないエラー: $e');
    }
  }
}
```

## テスト戦略

### ユニットテスト

```dart
// ViewModelのテスト
test('MonologFlowViewModel saves log successfully', () async {
  final mockFirestoreService = MockFirestoreService();
  final mockAuthService = MockAuthService();
  
  when(mockAuthService.currentUser).thenReturn(mockUser);
  when(mockFirestoreService.saveLog(any)).thenAnswer((_) async => {});
  
  final viewModel = MonologFlowViewModel(
    firestoreService: mockFirestoreService,
    authService: mockAuthService,
  );
  
  await viewModel.saveLog(testLog);
  
  expect(viewModel.state, isA<MonologFlowSuccess>());
  verify(mockFirestoreService.saveLog(testLog)).called(1);
});
```

## まとめ

このアーキテクチャは、以下の原則に基づいて設計されています：

1. **関心の分離**: 各層が明確な責任を持つ
2. **テスタビリティ**: 依存性注入によるテスト容易性
3. **スケーラビリティ**: 機能追加が容易な構造
4. **保守性**: コードの理解と変更が容易
5. **パフォーマンス**: 最適化された実装

詳細な実装については、各ソースコードファイルを参照してください。