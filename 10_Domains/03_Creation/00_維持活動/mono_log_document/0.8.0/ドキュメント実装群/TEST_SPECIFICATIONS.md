# 『モノログ。』自動テスト仕様書

**作成日**: 2025年7月28日
**更新日**: 2025年8月3日
**バージョン**: Ver 1.0.0
**対象**: 開発者・AI向けテスト技術仕様

---

## 📋 テストスイート概要

- **テストフレームワーク**: `flutter_test`, `bloc_test`, `mockito`, `integration_test`
- **テスト対象**: BLoC, Services, Widgets, 統合フロー

### テスト分類

- **単体テスト (`/test/blocs`, `/test/services`)**: 
  - 各BLoCのロジックを`bloc_test`を用いてテストします。
  - 各Serviceのロジックを`mockito`を用いてテストします。

- **ウィジェットテスト (`/test/screens`, `/test/widgets`)**: 
  - 各画面（Screen）や再利用可能なウィジェットのUIとインタラクションをテストします。

- **統合テスト (`/test/integration`)**: 
  - 複数のコンポーネント（画面、BLoC、サービス）を連携させたエンドツーエンドのフローをテストします。

- **その他 (`/test`)**:
  - `firebase_initialization_test.dart`: Firebaseの初期化に関するテストです。
  - `security_test.dart`: セキュリティ関連のテストです。
  - `widget_test.dart`: デフォルトで生成されるウィジェットテストです。

---

## 🏗️ テストアーキテクチャ

- **依存性の注入 (DI)**: `get_it` を使用してテスト対象のクラスにモックを注入しやすくしています。
- **モック**: `mockito` や `mocktail` を使用して、外部依存（Firebase, APIクライアントなど）をモック化し、テストの分離性と速度を確保します。
- **テストヘルパー (`/test/test_helpers`)**: テストで繰り返し利用するセットアップコードやモックの生成コードなどを共通化しています。

---

## 🚀 CI/CD自動化

### GitHub Actions設定

- **`flutter_test.yml`**: プルリクエストやマージ時に、全てのテスト（単体、ウィジェット、統合）を自動実行します。
- **`quality_gate.yml`**: テストカバレッジの閾値チェックや静的解析を自動実行し、コードの品質を担保します。

---

## 🔧 テスト実行方法

```bash
# 全てのテストを実行
flutter test

# 特定のテストファイルを指定して実行
flutter test test/blocs/your_bloc_test.dart

# テストカバレッジを生成
flutter test --coverage
```

---

**この仕様書は『モノログ。』プロジェクトVer 1.0.0の自動テスト仕様を記録し、品質保証体制を示しています。**
