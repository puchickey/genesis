# モノログ。 - 実装ガイド

## プロジェクト情報
- **プロジェクト名**: モノログ。(mono_log_app)
- **バージョン**: 1.0.0
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

# Firebase設定 (未設定の場合)
flutterfire configure
```

## プロジェクト構造

```
lib/
├── blocs/              # BLoC関連
├── config/             # 設定ファイル
├── controllers/        # コントローラー
├── core/               # コア機能
├── features/           # 機能ごと
├── helpers/            # ヘルパー
├── models/             # データモデル
├── screens/            # 画面
├── services/           # サービス層
├── shared/             # 共有ウィジェットなど
├── styles/             # スタイル定義
├── utils/              # ユーティリティ
├── widgets/            # 再利用可能なウィジェット
└── main.dart           # エントリーポイント
```

## 主要機能の実装

### 1. アプリケーションの初期化と画面遷移

アプリケーションの起動時、`main.dart`の`AppInitializer`ウィジェットがユーザーの状態（オンボーディング完了済みか、チュートリアルの進捗はどうか）を判断し、適切な画面に遷移させます。

```dart
// lib/main.dart抜粋

class AppInitializerState extends State<AppInitializer> {
  // ...
  Future<void> _checkTutorialStatus() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final hasCompletedOnboarding = prefs.getBool('onboarding_completed') ?? false;
      
      final tutorialProgress = await GuideService.getTutorialProgress();
      
      String targetScreen = 'home';
      
      if (!hasCompletedOnboarding) {
        targetScreen = 'onboarding';
      } else if (tutorialProgress == GuideService.tutorialOnboardingCompleted) {
        targetScreen = 'diagnosis';
      } else {
        targetScreen = 'home';
      }
      
      setState(() {
        _targetScreen = targetScreen;
        _isLoading = false;
      });
    } catch (e) {
      // エラーハンドリング
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Scaffold(
        body: const Center(child: CircularProgressIndicator()),
      );
    }

    switch (_targetScreen) {
      case 'onboarding':
        return const OnboardingScreen();
      case 'diagnosis':
        return const DiagnosisScreen();
      case 'home':
      default:
        return const SimpleHomeScreen();
    }
  }
}
```

### 2. 状態管理 (BLoC)

BLoC (Business Logic Component) パターンを使用して、UIとビジネスロジックを分離しています。以下は簡単なカウンターの例です。

**イベント定義 (`counter_event.dart`)**
```dart
abstract class CounterEvent extends Equatable {
  const CounterEvent();

  @override
  List<Object> get props => [];
}

class Increment extends CounterEvent {}

class Decrement extends CounterEvent {}
```

**状態定義 (`counter_state.dart`)**
```dart
class CounterState extends Equatable {
  final int count;

  const CounterState(this.count);

  @override
  List<Object> get props => [count];
}
```

**BLoC実装 (`counter_bloc.dart`)**
```dart
class CounterBloc extends Bloc<CounterEvent, CounterState> {
  CounterBloc() : super(const CounterState(0)) {
    on<Increment>((event, emit) => emit(CounterState(state.count + 1)));
    on<Decrement>((event, emit) => emit(CounterState(state.count - 1)));
  }
}
```

**UIでの使用**
```dart
BlocProvider(
  create: (context) => CounterBloc(),
  child: BlocBuilder<CounterBloc, CounterState>(
    builder: (context, state) {
      return Text('Count: ${state.count}');
    },
  ),
)
```

### 3. 依存性注入 (GetIt)

`get_it`パッケージをサービスロケーターとして使用し、アプリケーション全体で共有するサービスのインスタンスを管理しています。

```dart
// lib/core/services/service_locator.dart
final getIt = GetIt.instance;

Future<void> initialize() async {
  getIt.registerLazySingleton<AuthService>(() => AuthService());
  getIt.registerLazySingleton<GuideService>(() => GuideService());
  // ... 他のサービスの登録
}
```

## テスト戦略

- **ユニットテスト**: `bloc_test`を使い、Blocのロジックをテストします。
- **ウィジェットテスト**: `flutter_test`を使い、ウィジェットの振る舞いをテストします。
- **統合テスト**: `integration_test`を使い、複数の画面やサービスをまたがるフローをテストします。

## CI/CD設定

`.github/workflows/`配下にあるYAMLファイルで、GitHub ActionsによるCI/CDパイプラインを定義しています。
- `ci.yml`: プルリクエスト時にテストや静的解析を実行します。
- `release.yml`: mainブランチへのマージ時にリリースビルドを作成します。

## ベストプラクティス

- **Effective Dart**: 公式のスタイルガイドに従います。
- **SOLID原則**: 保守性・拡張性の高いコードを目指します。
- **エラーハンドリング**: `try-catch`ブロックと、必要に応じて`Result`型のようなものを導入し、堅牢なエラー処理を行います。