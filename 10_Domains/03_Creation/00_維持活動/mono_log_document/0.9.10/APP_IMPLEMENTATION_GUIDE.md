# モノログ。 - 実装ガイド

## プロジェクト情報
- **プロジェクト名**: モノログ。(mono_log_app)
- **バージョン**: 1.0.0
- **更新日**: 2025年8月12日
- **対応プラットフォーム**: iOS, Android

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

# Firebase設定 (Firebaseプロジェクトに接続する場合)
# flutterfire configure
```
*注: このプロジェクトはすでにFirebaseに接続済みです。新規でセットアップする場合のみ上記コマンドが必要です。*

## プロジェクト構造

`lib`ディレクトリは、機能と役割に基づいて以下のように構成されています。

```
lib/
├── blocs/              # BLoC (状態管理)
├── config/             # アプリ全体の設定 (色、タイポグラフィ等)
├── core/               # アプリのコア機能 (ナビゲーション、サービスロケーター等)
├── models/             # データモデル (Monolog, Objectなど)
├── screens/            # 各画面のUIを構成するWidget
├── services/           # ビジネスロジック (ストレージ、認証、画像処理等)
├── styles/             # アプリ固有のスタイル定義
├── utils/              # 汎用的なユーティリティやヘルパー
├── widgets/            # 画面間で共有される再利用可能なUIコンポーネント
└── main.dart           # アプリケーションのエントリーポイント
```

## 主要機能の実装ガイド

### 1. 新しい画面の追加

1.  **Screen作成**: `lib/screens`に新しい`your_screen.dart`を作成します。`Scaffold`を持つ`StatelessWidget`または`StatefulWidget`を基本とします。
2.  **Route定義**: `lib/core/navigation/app_routes.dart`に新しいルートを追加します。
    ```dart
    // app_routes.dart
    static const String yourScreen = '/your_screen';

    static Route<dynamic> generateRoute(RouteSettings settings) {
      switch (settings.name) {
        // ...
        case yourScreen:
          return MaterialPageRoute(builder: (_) => const YourScreen());
        // ...
      }
    }
    ```
3.  **画面遷移**: 他の画面から`Navigator`を使って遷移します。
    ```dart
    Navigator.of(context).pushNamed(AppRoutes.yourScreen, arguments: ...);
    ```

### 2. 状態管理 (BLoC)

BLoC (Business Logic Component) パターンを使用して、UIとビジネスロジックを分離しています。新しいBLoCを追加する手順は以下の通りです。

1.  **Event定義**: `lib/blocs/your_feature/your_feature_event.dart` を作成し、ユーザーアクションやUIイベントを定義します。
2.  **State定義**: `lib/blocs/your_feature/your_feature_state.dart` を作成し、UIの状態（初期状態、ロード中、成功、失敗など）を定義します。
3.  **BLoC実装**: `lib/blocs/your_feature/your_feature_bloc.dart` を作成し、イベントに応じてビジネスロジックを実行し、新しいStateを`emit`します。
    ```dart
    class YourFeatureBloc extends Bloc<YourFeatureEvent, YourFeatureState> {
      YourFeatureBloc() : super(YourFeatureInitial()) {
        on<YourFeatureRequested>((event, emit) {
          // ビジネスロジックを実行
          emit(YourFeatureLoadSuccess(...));
        });
      }
    }
    ```
4.  **UIでの使用**: `BlocProvider`でBLoCを注入し、`BlocBuilder`や`BlocListener`でUIを構築・更新します。
    ```dart
    BlocProvider(
      create: (context) => getIt<YourFeatureBloc>(), // ServiceLocator経由で取得
      child: BlocBuilder<YourFeatureBloc, YourFeatureState>(
        builder: (context, state) {
          // stateに基づいてUIを構築
        },
      ),
    )
    ```

### 3. 依存性注入 (GetIt)

`get_it`をサービスロケーターとして使用し、サービスのインスタンスを管理しています。新しいサービスを追加する際は、`lib/core/services/service_locator.dart`に登録します。

```dart
// lib/core/services/service_locator.dart
final getIt = GetIt.instance;

Future<void> initialize() async {
  // Service (Singleton)
  getIt.registerLazySingleton<AuthService>(() => AuthService());
  getIt.registerLazySingleton<HybridStorageService>(() => HybridStorageService());

  // BLoC (Factory)
  getIt.registerFactory<MonologBloc>(() => MonologBloc(
    storageService: getIt<HybridStorageService>(),
  ));
  // ... 他のサービスの登録
}
```
- **Singleton**: アプリケーションのライフサイクル中に常に単一のインスタンスを保持します。
- **Factory**: 要求されるたびに新しいインスタンスを生成します。BLoCはこちらを使用することが多いです。

## テスト戦略

- **ユニットテスト**: `test/`ディレクトリに配置します。`bloc_test`パッケージを利用して、BLoCのロジック（イベント→ステートの遷移）をテストします。サービスの単体テストもここに含まれます。
- **ウィジェットテスト**: `test/widget_test/`ディレクトリに配置します。`flutter_test`フレームワークを使い、個別のWidgetが正しくレンダリングされ、ユーザーの操作に反応することをテストします。
- **統合テスト**: `integration_test/`ディレクトリに配置します。複数の画面やサービスをまたがるユーザーフロー全体をテストします。（例：モノログ作成フロー）

## ベストプラクティス

- **Effective Dart**: 公式のスタイルガイドに従い、コードの可読性と一貫性を保ちます。
- **SOLID原則**: 保守性・拡張性の高いコードを目指し、クラスの責務を単一に保ちます。
- **エラーハンドリング**: `lib/core/utils/error_handler.dart` に定義されたグローバルエラーハンドリング機構を利用します。サービス層では`Result`型（`Success`/`Failure`）を返し、UI層に明確なエラー情報を伝達することを推奨します。
- **不変性 (Immutability)**: BLoCのStateやModelクラスは、`copyWith`メソッドを持つ不変クラスとして定義することが推奨されます。これにより、状態の変更が予測可能になります。
