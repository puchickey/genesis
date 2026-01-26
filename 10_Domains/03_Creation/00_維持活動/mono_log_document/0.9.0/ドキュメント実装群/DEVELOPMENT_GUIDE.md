# 開発ガイド

このドキュメントでは、モノログアプリの開発環境セットアップから、開発フロー、テスト、デプロイまでの開発者向けガイドを提供します。

## 目次

1. [開発環境のセットアップ](#開発環境のセットアップ)
2. [プロジェクト構造](#プロジェクト構造)
3. [開発フロー](#開発フロー)
4. [コーディング規約](#コーディング規約)
5. [テスト](#テスト)
6. [デバッグ](#デバッグ)
7. [ビルドとデプロイ](#ビルドとデプロイ)
8. [トラブルシューティング](#トラブルシューティング)

## 開発環境のセットアップ

### 必要なツール

1. **Flutter SDK** (3.24.5以上)
   ```bash
   flutter --version
   # Flutter 3.24.5 • channel stable
   ```

2. **Dart SDK** (>=3.5.0)
   - Flutterに含まれています

3. **IDE**
   - VSCode (推奨) + Flutter/Dart拡張機能
   - Android Studio + Flutter/Dartプラグイン

4. **Firebase CLI**
   ```bash
   npm install -g firebase-tools
   firebase login
   ```

### プロジェクトのセットアップ

1. **リポジトリのクローン**
   ```bash
   git clone [repository-url]
   cd mono_log_app
   ```

2. **依存関係のインストール**
   ```bash
   flutter pub get
   ```

3. **Firebaseの設定**
   ```bash
   # Firebase プロジェクトの作成と設定
   flutterfire configure
   
   # 必要な場合は環境ごとに設定
   flutterfire configure --project=mono-log-dev  # 開発環境
   flutterfire configure --project=mono-log-prod # 本番環境
   ```

4. **ビルドランナーの実行**
   ```bash
   flutter pub run build_runner build --delete-conflicting-outputs
   ```

5. **環境変数の設定**
   `.env`ファイルを作成（`.env.example`を参考に）
   ```
   FIREBASE_API_KEY=your_api_key
   FIREBASE_PROJECT_ID=your_project_id
   ```

## プロジェクト構造

```
mono_log_app/
├── lib/
│   ├── main.dart                # アプリのエントリーポイント
│   ├── models/                  # データモデル
│   │   ├── object_models.dart
│   │   ├── diagnosis_models.dart
│   │   └── insight_log.dart
│   ├── screens/                 # 画面コンポーネント
│   │   ├── simple_home_screen.dart
│   │   ├── micro_journaling_screen.dart
│   │   └── ... (23画面)
│   ├── services/                # ビジネスロジック
│   │   ├── auth_service.dart
│   │   ├── firestore_service.dart
│   │   └── memory_storage_service.dart
│   ├── viewmodels/              # ViewModels (BLoC/Provider)
│   │   ├── monolog_flow_viewmodel.dart
│   │   └── object_viewmodel.dart
│   ├── widgets/                 # 再利用可能なウィジェット
│   │   ├── camera_button.dart
│   │   └── emotion_selector.dart
│   └── utils/                   # ユーティリティ関数
│       ├── constants.dart
│       └── helpers.dart
├── test/                        # テストファイル
│   ├── unit/
│   ├── widget/
│   └── integration/
├── assets/                      # 静的アセット
│   ├── images/
│   └── fonts/
└── pubspec.yaml                 # 依存関係定義
```

## 開発フロー

### 1. ブランチ戦略

```bash
# 機能開発
git checkout -b feature/新機能名

# バグ修正
git checkout -b fix/バグ説明

# ホットフィックス
git checkout -b hotfix/緊急修正
```

### 2. コミットメッセージ規約

```
<type>(<scope>): <subject>

<body>

<footer>
```

例:
```
feat(camera): カメラ撮影時のプレビュー機能を追加

- 撮影前にプレビューを表示
- 再撮影オプションを追加
- 画像圧縮処理を最適化

Closes #123
```

タイプ:
- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメント
- `style`: コードスタイル
- `refactor`: リファクタリング
- `test`: テスト
- `chore`: その他

### 3. プルリクエスト

1. 機能ブランチで開発
2. テストを実行して合格を確認
3. コードレビューを依頼
4. CI/CDパイプラインの通過を確認
5. マージ

## コーディング規約

### Dartコーディングスタイル

1. **命名規則**
   ```dart
   // クラス名: PascalCase
   class ObjectModel {}
   
   // 変数・メソッド名: camelCase
   String objectName;
   void saveObject() {}
   
   // 定数: camelCase (ALL_CAPSは使わない)
   const defaultTimeout = 30;
   ```

2. **インポート順序**
   ```dart
   // 1. Dart SDK
   import 'dart:async';
   
   // 2. パッケージ
   import 'package:flutter/material.dart';
   import 'package:firebase_auth/firebase_auth.dart';
   
   // 3. プロジェクト内
   import 'models/object_models.dart';
   import 'services/auth_service.dart';
   ```

3. **コードフォーマット**
   ```bash
   # 自動フォーマット
   dart format lib/
   ```

### アーキテクチャルール

1. **状態管理**: BLoCパターンを使用
2. **依存性注入**: get_itを使用
3. **非同期処理**: async/awaitを優先
4. **エラーハンドリング**: 適切な例外処理

## テスト

### テストの種類

1. **単体テスト**
   ```dart
   // test/unit/object_model_test.dart
   test('ObjectModel should create from JSON', () {
     final json = {'id': '123', 'name': 'テストオブジェクト'};
     final object = ObjectModel.fromJson(json);
     
     expect(object.id, '123');
     expect(object.name, 'テストオブジェクト');
   });
   ```

2. **ウィジェットテスト**
   ```dart
   // test/widget/camera_button_test.dart
   testWidgets('CameraButton shows pulse animation', (tester) async {
     await tester.pumpWidget(MaterialApp(
       home: Scaffold(body: CameraButton()),
     ));
     
     expect(find.byType(AnimatedContainer), findsOneWidget);
   });
   ```

3. **統合テスト**
   ```dart
   // test/integration/auth_flow_test.dart
   testWidgets('Anonymous auth flow completes', (tester) async {
     // 実際のFirebase接続を使用したテスト
   });
   ```

### テストの実行

```bash
# 全テストを実行
flutter test

# カバレッジ付きで実行
flutter test --coverage

# 特定のテストファイルを実行
flutter test test/unit/object_model_test.dart

# ウォッチモードで実行
flutter test --watch
```

### モックの生成

```bash
# mockitoを使用したモック生成
flutter pub run build_runner build --delete-conflicting-outputs
```

## デバッグ

### 1. デバッグツール

- **Flutter Inspector**: UIの階層を視覚的に確認
- **DevTools**: パフォーマンス分析とデバッグ
- **VSCode デバッガー**: ブレークポイントとステップ実行

### 2. ログ出力

```dart
// 開発時のログ
import 'package:flutter/foundation.dart';

if (kDebugMode) {
  print('デバッグ: オブジェクトID = ${object.id}');
}

// より詳細なログ
debugPrint('詳細ログ: ${object.toJson()}');
```

### 3. エラーハンドリング

```dart
try {
  await firestoreService.saveObject(object);
} catch (e, stackTrace) {
  // エラーログ
  debugPrint('エラー: $e');
  debugPrintStack(stackTrace: stackTrace);
  
  // Crashlyticsへの送信
  FirebaseCrashlytics.instance.recordError(e, stackTrace);
}
```

## ビルドとデプロイ

### 開発ビルド

```bash
# iOS
flutter build ios --debug

# Android
flutter build apk --debug
```

### リリースビルド

```bash
# iOS
flutter build ios --release

# Android
flutter build appbundle --release
```

### 環境別ビルド

```bash
# 開発環境
flutter run --dart-define=ENVIRONMENT=dev

# ステージング環境
flutter run --dart-define=ENVIRONMENT=staging

# 本番環境
flutter run --dart-define=ENVIRONMENT=prod
```

### CI/CD設定例 (GitHub Actions)

```yaml
name: Build and Test

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
          flutter-version: '3.24.5'
      - run: flutter pub get
      - run: flutter test
      - run: flutter build apk
```

## トラブルシューティング

### よくある問題と解決方法

1. **ビルドエラー: "Gradle build failed"**
   ```bash
   cd android
   ./gradlew clean
   cd ..
   flutter clean
   flutter pub get
   ```

2. **iOS: "No valid code signing identity found"**
   - Xcodeでプロジェクトを開く
   - Signing & Capabilitiesで適切な証明書を選択

3. **Firebaseエラー: "No Firebase App"**
   ```dart
   // main.dartで初期化を確認
   await Firebase.initializeApp(
     options: DefaultFirebaseOptions.currentPlatform,
   );
   ```

4. **状態管理エラー**
   ```dart
   // BLoCが見つからない場合
   BlocProvider.of<ObjectBloc>(context)
   // ↓
   context.read<ObjectBloc>() // 推奨
   ```

### デバッグTips

1. **パフォーマンス問題**
   - Flutter DevToolsのPerformanceタブを使用
   - `flutter run --profile`でプロファイルモード実行

2. **メモリリーク**
   - DevToolsのMemoryタブで確認
   - StreamSubscriptionのdisposeを確認

3. **レイアウト問題**
   - Debug Paint (`debugPaintSizeEnabled = true`)
   - Layout Explorerの使用

## リソース

- [Flutter公式ドキュメント](https://flutter.dev/docs)
- [Firebase Flutter Setup](https://firebase.google.com/docs/flutter/setup)
- [BLoC Library](https://bloclibrary.dev/)
- [Effective Dart](https://dart.dev/guides/language/effective-dart)

## サポート

問題が解決しない場合は、以下の方法でサポートを受けてください：

1. プロジェクトのIssueトラッカーに報告
2. 開発チームのSlackチャンネルで質問
3. ドキュメントの更新提案をPRで送信