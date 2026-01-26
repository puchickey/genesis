# モノログ。 - アプリケーションアーキテクチャレポート

## プロジェクト概要
- **プロジェクト名**: モノログ。(mono_log_app)
- **バージョン**: 1.0.0
- **更新日**: 2025年8月3日
- **プラットフォーム**: Flutter (クロスプラットフォーム対応)
- **対応OS**: iOS、Android、Web、Windows、macOS、Linux

## アーキテクチャ概要

### レイヤード・アーキテクチャ

本アプリケーションは、クリーンアーキテクチャの原則に基づいた4層構造を採用しています：

```
┌─────────────────────────────────────────────────┐
│             Presentation Layer                  │
│    (Screens, Widgets, Blocs)                    │
├─────────────────────────────────────────────────┤
│             Application Layer                   │
│    (Services, Business Logic)                   │
├─────────────────────────────────────────────────┤
│               Domain Layer                      │
│    (Models, Interfaces, Entities)               │
├─────────────────────────────────────────────────┤
│           Infrastructure Layer                  │
│    (Storage, Network, External Services)        │
└─────────────────────────────────────────────────┘
```

### コアコンセプト

1. **BLoC (Business Logic Component)**
   - UIとビジネスロジックの分離
   - Streamを用いたリアクティブな状態管理
   - テスタビリティの向上

2. **サービスロケーターパターン**
   - GetItによる依存性注入
   - サービスの疎結合化

3. **ハイブリッドストレージアーキテクチャ**
   - ローカルファイルストレージ（写真）とSQLiteデータベース
   - クラウドストレージ（メタデータ）
   - オフライン対応とオンライン同期

## 主要コンポーネント

### 1. プレゼンテーション層 (lib/features, lib/screens, lib/widgets)

- **BLoC**: 各フィーチャーに対応するBlocがビジネスロジックを管理します。
- **Screens**: 各画面のUIを構築します。
- **Widgets**: 再利用可能なUIコンポーネントです。

#### 画面構成
- **OnboardingScreen**: アプリの初回利用時に表示されるオンボーディング画面です。
- **DiagnosisScreen**: ユーザーのタイプを診断する画面です。
- **SimpleHomeScreen**: アプリのメイン画面です。
- **CameraCaptureScreen**: 写真を撮影する画面です。
- **MonologFlowScreen**: 感情を選択し、モノログを作成する画面です。
- **LogScreen**: 過去のモノログを一覧表示する画面です。

### 2. アプリケーション層 (lib/services, lib/blocs)

- **Services**: アプリケーション全体で利用されるサービスを提供します。
  - `AuthService`: 認証関連の処理を担当します。
  - `GuideService`: チュートリアルの進捗管理を担当します。
  - `RemoteConfigService`: Firebase Remote Configとの連携を担当します。
- **Blocs**: プレゼンテーション層からのイベントを受け取り、状態を更新します。

### 3. ドメイン層 (lib/models)

- **Models**: アプリケーションのデータ構造を定義します。
  - `MonologModel`: モノログのデータモデルです。
  - `ObjectModel`: モノのデータモデルです。
  - `EmotionTier`: 感情の階層モデルです。

### 4. インフラストラクチャ層 (lib/core/storage, lib/services)

- **Storage**: データの永続化を担当します。
  - `LocalFileHandler`: ローカルファイル（主に画像）を扱います。
  - `FirestoreService`: Firestoreとの連携を担当します。
  - `SQFlite`: ローカルデータベースを扱います。
- **Firebase**: バックエンドサービスとして利用します。

## データフロー

### モノログ作成フロー
```
1. CameraCaptureScreenで写真を撮影またはギャラリーから選択
   ↓
2. MonologFlowScreenで感情を選択し、メモを入力
   ↓
3. 対応するBlocがイベントを処理
   ↓
4. HybridStorageServiceを介してデータを保存
   ├─ 写真: ローカルストレージ
   └─ メタデータ: Firestore & ローカルDB (SQLite)
```

## セキュリティとプライバシー

- **データ保護**: Firebase Authenticationによる認証、Firestoreのセキュリティルールによるアクセス制御、ローカルデータの暗号化（検討中）
- **プライバシー配慮**: 位置情報の非収集、最小限のパーミッション要求

## パフォーマンス最適化

- **画像処理**: 効率的な画像圧縮、サムネイル生成、遅延読み込み
- **メモリ管理**: BLoCの適切な破棄、キャッシュ管理
- **ネットワーク最適化**: オフライン対応、データのバッチ処理

## 開発ガイドライン

- **コーディング規約**: Effective Dart
- **アーキテクチャ原則**: SOLID原則
- **テスト戦略**: ユニットテスト、ウィジェットテスト、統合テスト

## 技術スタック

### フロントエンド
- Flutter 3.x
- Dart 3.x
- Material Design 3

### バックエンド
- Firebase (BaaS)

### 状態管理
- flutter_bloc / bloc
- GetIt (Service Locator)

### 主要パッケージ
- `camera`: カメラ機能
- `image_picker`: 画像選択
- `tflite_flutter`: 機械学習モデルの実行
- `path_provider`: ファイルパス管理
- `shared_preferences`: ローカル設定
- `sqflite`: ローカルデータベース
- `firebase_core`: Firebase基盤
- `firebase_auth`: 認証
- `cloud_firestore`: データベース
- `crypto`: 暗号化
- `get_it`: 依存性注入
- `uuid`: UUID生成
- `intl`: 国際化
