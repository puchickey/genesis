# モノログ。(Mono_Log) アプリ構成レポート

## 1. アプリ概要
**アプリ名**: モノログ。(Mono_Log)
**バージョン**: 0.5.3
**コンセプト**: 物（モノ）との対話を通じて感情と向き合うアプリ
**開発フレームワーク**: Flutter 3.x (Material Design 3)

## 2. アーキテクチャ概要

### 2.1 設計パターン
- **Clean Architecture**: ドメイン層、データ層、プレゼンテーション層の分離
- **Service Locator Pattern**: GetItによる依存性注入
- **BLoC Pattern**: 状態管理（主要部分のみ）
- **BaseScreen Pattern**: 画面の共通処理を基底クラスで実装

### 2.2 ディレクトリ構成
```
lib/
├── core/           # 基底クラス、インターフェース、定数
├── models/         # データモデル
├── services/       # ビジネスロジック、データアクセス
├── screens/        # 画面UI
├── widgets/        # 再利用可能なUIコンポーネント
├── config/         # 設定、定数定義
├── styles/         # スタイル定義
└── utils/          # ユーティリティ関数
```

## 3. コア機能

### 3.1 2タップ感情選択システム
- **第1階層**: 5つの感情カテゴリ
  - 心が弾む・高ぶる気持ち（楽しい、嬉しい、ワクワク）
  - 落ち着く・満たされる気持ち（安心、満足、幸せ）
  - 落ち込む・沈む気持ち（悲しい、寂しい、不安）
  - イライラ・もやもやする気持ち（怒り、嫌悪、恐怖）
  - どちらでもない・その他（興味、驚き、複雑）
- **第2階層**: 各カテゴリ6つの詳細感情

### 3.2 主要な画面フロー
1. **SimpleHomeScreen**: ホーム画面（カメラボタン）
2. **CameraCaptureScreen**: 写真撮影
3. **ObjectSelectionScreen**: モノの選択
4. **MonologFlowScreen**: 感情選択とメモ入力
5. **RegistrationCardScreen**: 記録の命名（自動生成可）
6. **LogScreen**: マイログ画面（記録の確認）

### 3.3 データモデル
- **ObjectModel**: 物の情報（ID、名前、画像パス、作成日時）
- **MonologModel**: モノログ記録（感情、メモ、タイムスタンプ）
- **UserModel**: ユーザー情報（匿名認証）

## 4. サービス層

### 4.1 データ永続化
- **FirestoreService**: Firebase Firestore（本番用、完全動作中）
- **AuthService**: Firebase匿名認証（正常動作）
- **StorageInterface**: テスト可能な抽象化層
- **MockStorageInterface**: テスト用モック実装

### 4.2 ビジネスロジック
- **AutoNamingService**: 自動命名機能
  - モノの名前: "2025/07/23のモノ"形式
  - モノログタイトル: "「嬉しい」気持ちの記録"形式
- **GuideService**: チュートリアル・ガイド機能
  - 初回起動時の連続チュートリアル
  - 各画面の操作ガイド

### 4.3 その他のサービス
- **NotificationService**: プッシュ通知（未実装）
- **AnalyticsService**: 使用状況分析（未実装）
- **BackupService**: バックアップ機能（未実装）

## 5. UI/UXデザイン

### 5.1 カラーパレット
- **Calm Green** (#6A9C89): メインカラー
- **Gentle Blue** (#87A9C4): アクセントカラー
- **Soft Beige** (#F8F7F2): 背景色
- **Ink Grey** (#333333): テキストカラー

### 5.2 タイポグラフィ
- フォント: M PLUS Rounded 1c
- Material Design 3準拠のタイプスケール

### 5.3 アニメーション
- 標準的な遷移時間:
  - Fast: 200ms
  - Medium: 300ms
  - Slow: 500ms

## 6. 技術的特徴

### 6.1 依存性注入
```dart
// GetItによるサービス登録
GetIt.I.registerLazySingleton<AuthService>(() => AuthService());
GetIt.I.registerLazySingleton<MemoryStorageService>(() => MemoryStorageService());
GetIt.I.registerLazySingleton<AutoNamingService>(() => AutoNamingService());
```

### 6.2 BaseScreen実装
```dart
abstract class BaseScreen extends StatefulWidget {
  // 共通のライフサイクル管理
  // エラーハンドリング
  // ローディング状態管理
}
```

### 6.3 レスポンシブ対応
- LayoutBuilderによる画面サイズ対応
- GridViewの動的カラム数調整
- メディアクエリによる適応的レイアウト

## 7. 開発状況

### 7.1 完了機能
- ✅ 基本的な画面フロー
- ✅ 2タップ感情選択システム
- ✅ 写真撮影・選択機能
- ✅ 自動命名機能
- ✅ チュートリアル機能
- ✅ Firebase統合（Firestore、Authentication）
- ✅ クラウドデータ永続化
- ✅ 3段階初期化プロセス
- ✅ 包括的テストスイート（43テスト）
- ✅ CI/CD自動化（GitHub Actions）

### 7.2 計画中機能
- 📋 プッシュ通知機能
- 📋 データエクスポート機能
- 📋 感情分析・可視化機能
- 📋 多言語対応（英語）
- 📋 ダークモード対応

## 8. コード品質

### 8.1 コーディング規約
- CLAUDE_WORK_GUIDELINES.mdに準拠
- エラーハンドリングの徹底
- ハードコーディングの排除
- 適切なコメント記述

### 8.2 静的解析・品質指標
- Flutter analyze: **3件の警告のみ**（146件から大幅削減）
- テスト実装: 43テスト（Unit/Widget/Integration/Smoke）
- 成功率: 100%
- CI/CD: PR自動チェック・品質ゲート完備

## 9. テスト戦略

### 9.1 テストアーキテクチャ
- **StorageInterface**: Firebase依存を排除した抽象化
- **MockStorageInterface**: mocktailベースのモック実装
- **TestHelper**: 共通テストユーティリティ

### 9.2 テストカバレッジ
```dart
// 実装済みテスト
├── unit_test/        # 13テスト
├── widget_test/      # 25テスト
├── integration_test/ # 4テスト
└── smoke_test.dart   # 1テスト
```

### 9.3 CI/CD設定
- GitHub Actions による自動実行
- PRごとの品質チェック
- テスト失敗時のマージブロック

## 10. 技術的成果

### 10.1 アーキテクチャ成熟度
- **Enterprise Level**: Service Locator + DI完備
- **テスト可能設計**: 依存性注入による分離
- **エラー処理**: 3段階初期化による堅牢性

### 10.2 開発効率
- **新機能追加**: テスト込みで品質保証
- **バグ防止**: 自動テストによる保護
- **チーム開発**: 品質ゲート設定済み

## 11. まとめ
「モノログ。」は、物との対話を通じて感情と向き合うという独自のコンセプトを持つアプリです。Ver 0.5.3では、Firebase完全統合、包括的テスト実装、CI/CD自動化により、エンタープライズレベルの品質基準を達成しました。

コード品質は146問題から3警告まで改善され、43の自動テストによる品質保証体制が確立されています。リリース準備が整い、持続可能な開発体制でユーザーに価値を提供する準備ができています。