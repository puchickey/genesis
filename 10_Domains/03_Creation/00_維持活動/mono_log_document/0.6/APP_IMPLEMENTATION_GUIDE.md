# モノログ。 - 実装ガイド

## プロジェクト情報
- **プロジェクト名**: モノログ。(mono_log_app)
- **バージョン**: 0.6.0
- **更新日**: 2025年8月3日
- **対応プラットフォーム**: iOS、Android、Web、Windows、macOS、Linux

## 開発環境のセットアップ

### 必要なツール
- Flutter SDK 3.x以上
- Dart SDK 3.x以上
- Android Studio / VS Code
- Xcode（iOS開発用）

### プロジェクトのセットアップ
```bash
# 依存関係のインストール
flutter pub get

# Firebase設定
flutterfire configure
```

## プロジェクト構造

```
lib/
├── core/              # コア機能
│   ├── base/         # 基底クラス
│   ├── constants/    # 定数定義
│   ├── routes/       # ルーティング
│   ├── storage/      # ストレージ
│   ├── theme/        # テーマ設定
│   └── utils/        # ユーティリティ
├── models/           # データモデル
├── screens/          # 画面
├── services/         # サービス層
├── widgets/          # 再利用可能なウィジェット
└── main.dart         # エントリーポイント
```

## 主要機能の実装

### 1. 依存性注入（Service Locator）

```dart
// lib/service_locator.dart
import 'package:get_it/get_it.dart';

final GetIt getIt = GetIt.instance;

void setupServiceLocator() {
  // サービスの登録
  getIt.registerLazySingleton<StorageService>(
    () => HybridStorageService()
  );
  
  getIt.registerLazySingleton<TutorialController>(
    () => TutorialController()
  );
  
  getIt.registerLazySingleton<CrisisSupportService>(
    () => CrisisSupportService()
  );
  
  getIt.registerLazySingleton<EmotionPaletteService>(
    () => EmotionPaletteService()
  );
  
  getIt.registerLazySingleton<AutoNamingService>(
    () => AutoNamingService()
  );
}
```

### 2. ハイブリッドストレージ実装

```dart
// lib/core/storage/hybrid_storage_service.dart
class HybridStorageService implements StorageService {
  final LocalFileHandler _localHandler;
  final FirestoreService _firestoreService;
  
  Future<void> saveMonolog(MonologData data) async {
    // 写真をローカルに保存
    final localPath = await _localHandler.savePhoto(data.photo);
    
    // メタデータをFirestoreに保存
    final metadata = MonologMetadata(
      photoPath: localPath,
      emotion: data.emotion,
      memo: data.memo,
      createdAt: DateTime.now(),
    );
    
    await _firestoreService.saveMetadata(metadata);
  }
  
  Future<void> cleanupOrphanedData() async {
    // 孤立したデータのクリーンアップ
    final localFiles = await _localHandler.getAllFiles();
    final remoteRefs = await _firestoreService.getAllReferences();
    
    // 参照のないローカルファイルを削除
    for (final file in localFiles) {
      if (!remoteRefs.contains(file.path)) {
        await file.delete();
      }
    }
  }
}
```

### 3. 2タップ感情選択システム

```dart
// lib/widgets/two_tap_emotion_selector.dart
class TwoTapEmotionSelector extends StatefulWidget {
  final Function(String tier1, String tier2) onEmotionSelected;
  
  @override
  _TwoTapEmotionSelectorState createState() => _TwoTapEmotionSelectorState();
}

class _TwoTapEmotionSelectorState extends State<TwoTapEmotionSelector> {
  String? selectedTier1;
  
  // 第1階層の感情カテゴリ
  final tier1Emotions = [
    EmotionTier(id: 'happy', label: 'うれしい', emoji: '😊'),
    EmotionTier(id: 'fun', label: 'たのしい', emoji: '🎉'),
    EmotionTier(id: 'calm', label: 'おだやか', emoji: '😌'),
    EmotionTier(id: 'anxious', label: 'ふあん', emoji: '😰'),
    EmotionTier(id: 'sad', label: 'かなしい', emoji: '😢'),
  ];
  
  Widget buildTier1Grid() {
    return GridView.builder(
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        childAspectRatio: 1.5,
      ),
      itemCount: tier1Emotions.length,
      itemBuilder: (context, index) {
        final emotion = tier1Emotions[index];
        return EmotionCard(
          emotion: emotion,
          onTap: () => setState(() => selectedTier1 = emotion.id),
        );
      },
    );
  }
}
```

## サービスの実装

### 1. チュートリアルコントローラー

```dart
// lib/services/tutorial_controller.dart
class TutorialController extends ChangeNotifier {
  TutorialStage _currentStage = TutorialStage.notStarted;
  int _currentStep = 0;
  
  static const tutorialStages = [
    TutorialStage.onboarding,
    TutorialStage.diagnosis,
    TutorialStage.cameraIntro,
    TutorialStage.emotionSelection,
    TutorialStage.monologFlow,
    TutorialStage.naming,
    TutorialStage.completion,
  ];
  
  void startTutorial() {
    _currentStage = TutorialStage.onboarding;
    _currentStep = 0;
    notifyListeners();
  }
  
  void nextStep() {
    if (_currentStep < tutorialStages.length - 1) {
      _currentStep++;
      _currentStage = tutorialStages[_currentStep];
      notifyListeners();
    } else {
      completeTutorial();
    }
  }
  
  void skipTutorial() async {
    final shouldSkip = await _showSkipConfirmation();
    if (shouldSkip) {
      completeTutorial();
    }
  }
}
```

### 2. 危機対応サービス

```dart
// lib/services/crisis_support_service.dart
class CrisisSupportService {
  // 危機関連キーワード（日本語）
  static const crisisKeywords = [
    '死にたい', '消えたい', '生きるのが辛い',
    '自殺', '自傷', 'リストカット',
    '助けて', 'つらい', '苦しい',
  ];
  
  bool detectCrisisKeywords(String text) {
    final lowerText = text.toLowerCase();
    return crisisKeywords.any((keyword) => 
      lowerText.contains(keyword.toLowerCase())
    );
  }
  
  void showSupportDialog(BuildContext context) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => CrisisSupportDialog(),
    );
  }
  
  List<EmergencyContact> getEmergencyContacts() {
    return [
      EmergencyContact(
        name: 'いのちの電話',
        number: '0120-783-556',
        hours: '毎日16:00-21:00',
      ),
      EmergencyContact(
        name: 'よりそいホットライン',
        number: '0120-279-338',
        hours: '24時間',
      ),
    ];
  }
}
```

### 3. 感情パレットサービス

```dart
// lib/services/emotion_palette_service.dart
class EmotionPaletteService {
  final Map<String, EmotionStyle> emotionStyles = {
    'happy': EmotionStyle(
      primaryColor: Color(0xFFFFD700),
      secondaryColor: Color(0xFFFFA500),
      icon: Icons.sentiment_very_satisfied,
    ),
    'sad': EmotionStyle(
      primaryColor: Color(0xFF4169E1),
      secondaryColor: Color(0xFF6495ED),
      icon: Icons.sentiment_dissatisfied,
    ),
    // その他の感情スタイル...
  };
  
  Color getEmotionColor(String emotionId) {
    return emotionStyles[emotionId]?.primaryColor ?? Colors.grey;
  }
  
  IconData getEmotionIcon(String emotionId) {
    return emotionStyles[emotionId]?.icon ?? Icons.sentiment_neutral;
  }
  
  Gradient generateEmotionGradient(String emotionId) {
    final style = emotionStyles[emotionId];
    if (style == null) {
      return LinearGradient(colors: [Colors.grey, Colors.grey.shade300]);
    }
    
    return LinearGradient(
      colors: [style.primaryColor, style.secondaryColor],
      begin: Alignment.topLeft,
      end: Alignment.bottomRight,
    );
  }
}
```

## 画面の実装

### 1. BaseScreen パターン

```dart
// lib/core/base/base_screen.dart
abstract class BaseScreen extends StatelessWidget {
  final String screenName;
  
  const BaseScreen({required this.screenName});
  
  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      onWillPop: () => handleBackPress(context),
      child: Scaffold(
        body: SafeArea(
          child: buildContent(context),
        ),
      ),
    );
  }
  
  Widget buildContent(BuildContext context);
  
  Future<bool> handleBackPress(BuildContext context) async {
    // 共通のバックプレス処理
    return true;
  }
  
  void showError(BuildContext context, String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message)),
    );
  }
}
```

### 2. モノログフロー画面

```dart
// lib/screens/monolog_flow_screen.dart
class MonologFlowScreen extends BaseScreen {
  final File imageFile;
  final String? objectId;
  
  MonologFlowScreen({
    required this.imageFile,
    this.objectId,
  }) : super(screenName: 'MonologFlow');
  
  @override
  Widget buildContent(BuildContext context) {
    return Column(
      children: [
        // プログレスインジケーター
        LinearProgressIndicator(value: 0.6),
        
        // 画像プレビュー
        Expanded(
          flex: 2,
          child: Image.file(imageFile),
        ),
        
        // 2タップ感情選択
        Expanded(
          flex: 3,
          child: TwoTapEmotionSelector(
            onEmotionSelected: (tier1, tier2) {
              _navigateToMemoInput(context, tier1, tier2);
            },
          ),
        ),
      ],
    );
  }
}
```

## チュートリアルシステム

### チュートリアルガイドオーバーレイ

```dart
// lib/widgets/tutorial_guide_overlay.dart
class TutorialGuideOverlay extends StatelessWidget {
  final TutorialStage stage;
  final Widget child;
  
  @override
  Widget build(BuildContext context) {
    final controller = getIt<TutorialController>();
    
    return Stack(
      children: [
        child,
        if (controller.isActive)
          Positioned.fill(
            child: TutorialOverlayContent(
              stage: stage,
              onNext: controller.nextStep,
              onSkip: controller.skipTutorial,
            ),
          ),
      ],
    );
  }
}
```

### ナビゲーションガード

```dart
// lib/widgets/tutorial_navigation_guard.dart
class TutorialNavigationGuard {
  static bool canNavigate(String route) {
    final controller = getIt<TutorialController>();
    
    if (!controller.isActive) return true;
    
    // チュートリアル中は特定のルートのみ許可
    final allowedRoutes = getAllowedRoutesForStage(controller.currentStage);
    return allowedRoutes.contains(route);
  }
}
```

## データ永続化

### ローカルストレージ

```dart
// lib/core/storage/local_file_handler.dart
class LocalFileHandler {
  Future<String> savePhoto(File photo) async {
    final appDir = await getApplicationDocumentsDirectory();
    final fileName = '${DateTime.now().millisecondsSinceEpoch}.jpg';
    final filePath = '${appDir.path}/photos/$fileName';
    
    // ディレクトリの作成
    final photoDir = Directory('${appDir.path}/photos');
    if (!await photoDir.exists()) {
      await photoDir.create(recursive: true);
    }
    
    // ファイルのコピー
    await photo.copy(filePath);
    
    return filePath;
  }
}
```

### Firestore連携

```dart
// lib/services/firestore_service.dart
class FirestoreService {
  final FirebaseFirestore _firestore = FirebaseFirestore.instance;
  
  Future<void> saveMonolog(MonologModel monolog) async {
    await _firestore
      .collection('users')
      .doc(monolog.userId)
      .collection('monologs')
      .doc(monolog.logId)
      .set(monolog.toJson());
  }
  
  Stream<List<MonologModel>> getUserMonologs(String userId) {
    return _firestore
      .collection('users')
      .doc(userId)
      .collection('monologs')
      .orderBy('createdAt', descending: true)
      .snapshots()
      .map((snapshot) => 
        snapshot.docs.map((doc) => 
          MonologModel.fromJson(doc.data())
        ).toList()
      );
  }
}
```

## エラーハンドリング

### グローバルエラーハンドラー

```dart
// lib/core/utils/error_handler.dart
class ErrorHandler {
  static void handleError(dynamic error, StackTrace? stack) {
    // エラーログの記録
    debugPrint('Error: $error');
    debugPrint('Stack: $stack');
    
    // Crashlyticsへの送信
    if (!kDebugMode) {
      FirebaseCrashlytics.instance.recordError(error, stack);
    }
  }
  
  static String getUserFriendlyMessage(dynamic error) {
    if (error is NetworkException) {
      return 'ネットワーク接続を確認してください';
    } else if (error is StorageException) {
      return 'ストレージへのアクセスに失敗しました';
    } else if (error is AuthException) {
      return '認証エラーが発生しました';
    }
    
    return 'エラーが発生しました。しばらくしてからお試しください。';
  }
}
```

## テスト戦略

### ユニットテスト

```dart
// test/services/emotion_palette_service_test.dart
void main() {
  late EmotionPaletteService service;
  
  setUp(() {
    service = EmotionPaletteService();
  });
  
  group('EmotionPaletteService', () {
    test('should return correct color for emotion', () {
      final color = service.getEmotionColor('happy');
      expect(color, equals(Color(0xFFFFD700)));
    });
    
    test('should return grey for unknown emotion', () {
      final color = service.getEmotionColor('unknown');
      expect(color, equals(Colors.grey));
    });
  });
}
```

### ウィジェットテスト

```dart
// test/widgets/two_tap_emotion_selector_test.dart
void main() {
  testWidgets('shows tier 1 emotions initially', (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: TwoTapEmotionSelector(
          onEmotionSelected: (_, __) {},
        ),
      ),
    );
    
    expect(find.text('うれしい'), findsOneWidget);
    expect(find.text('かなしい'), findsOneWidget);
  });
}
```

## デプロイメント

### ビルド設定

1. **Android**
   ```bash
   # リリースビルド
   flutter build apk --release
   
   # App Bundle
   flutter build appbundle --release
   ```

2. **iOS**
   ```bash
   # リリースビルド
   flutter build ios --release
   
   # Xcodeでアーカイブ作成
   open ios/Runner.xcworkspace
   ```

### 環境別設定

```dart
// lib/config/environment.dart
class Environment {
  static const String dev = 'development';
  static const String staging = 'staging';
  static const String prod = 'production';
  
  static String get current => 
    const String.fromEnvironment('ENV', defaultValue: dev);
  
  static String get apiUrl {
    switch (current) {
      case dev:
        return 'https://dev-api.monolog.app';
      case staging:
        return 'https://staging-api.monolog.app';
      case prod:
        return 'https://api.monolog.app';
      default:
        return 'https://dev-api.monolog.app';
    }
  }
}
```

### CI/CD設定

```yaml
# .github/workflows/flutter.yml
name: Flutter CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: subosito/flutter-action@v2
      with:
        flutter-version: '3.x'
    - run: flutter pub get
    - run: flutter test
    - run: flutter analyze
    
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: subosito/flutter-action@v2
      with:
        flutter-version: '3.x'
    - run: flutter pub get
    - run: flutter build apk --release
    - uses: actions/upload-artifact@v3
      with:
        name: release-apk
        path: build/app/outputs/flutter-apk/app-release.apk
```

## ベストプラクティス

### コーディング規約

1. **命名規則**
   - クラス名: UpperCamelCase
   - 変数・関数名: lowerCamelCase
   - 定数: UPPER_SNAKE_CASE
   - ファイル名: snake_case

2. **ディレクトリ構造**
   - 機能ごとにフォルダを分割
   - 共通コンポーネントは別フォルダ
   - テストは対応するファイル構造を維持

3. **状態管理**
   - Providerパターンの活用
   - 不要な再ビルドの回避
   - 適切なスコープでの状態管理

### パフォーマンス最適化

1. **画像処理**
   - 効率的な画像圧縮
   - サムネイル生成
   - 遅延読み込み

2. **リスト最適化**
   - ListView.builderの使用
   - アイテムの再利用
   - 適切なキーの設定

3. **メモリ管理**
   - リソースの適切な解放
   - StreamSubscriptionのキャンセル
   - Controllerのdispose

## トラブルシューティング

### よくある問題

1. **ビルドエラー**
   ```bash
   # キャッシュクリア
   flutter clean
   flutter pub get
   
   # iOS固有の問題
   cd ios
   pod install
   pod update
   ```

2. **パフォーマンス問題**
   - Flutter DevToolsの活用
   - プロファイルモードでの実行
   - 不要な再ビルドの特定

3. **Firebase接続エラー**
   - google-services.json / GoogleService-Info.plistの確認
   - Firebase Consoleでの設定確認
   - ネットワーク接続の確認

## まとめ

本実装ガイドでは、モノログ。アプリの主要な実装パターンと手法について説明しました。このガイドに従うことで、一貫性のある保守しやすいコードベースを維持できます。

継続的な改善とリファクタリングを心がけ、ユーザー体験の向上に努めてください。
