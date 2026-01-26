# モノログ。 - アプリケーションアーキテクチャレポート

## プロジェクト概要
- **プロジェクト名**: モノログ。(mono_log_app)
- **バージョン**: 1.0.0
- **更新日**: 2025年8月12日
- **プラットフォーム**: Flutter (クロスプラットフォーム対応)
- **対応OS**: iOS、Android (Web、Windows、macOS、Linuxは現状サポート対象外)

## アーキテクチャ概要

### 改良版レイヤード・アーキテクチャ

本アプリケーションは、クリーンアーキテクチャの原則を参考にしつつ、Flutterプロジェクトの実情に合わせて最適化した、実用的なレイヤード・アーキテクチャを採用しています。

```
┌─────────────────────────────────────────────────┐
│             Presentation Layer                  │
│    (Screens, Widgets, Blocs)                    │
├─────────────────────────────────────────────────┤
│             Application Layer                   │
│    (Services)                                   │
├─────────────────────────────────────────────────┤
│               Domain Layer                      │
│    (Models)                                     │
├─────────────────────────────────────────────────┤
│           Infrastructure Layer                  │
│    (Firebase, Local DB, Device APIs)            │
└─────────────────────────────────────────────────┘
```

- **Supporting Directories**: `config`, `core`, `styles`, `utils` が各レイヤーを横断的にサポートします。

### コアコンセプト

1. **BLoC (Business Logic Component)**
   - UIとビジネスロジックを明確に分離し、UIの関心を状態の描画のみに限定します。
   - `flutter_bloc` を利用し、Streamを用いたリアクティブな状態管理を実現します。
   - コンポーネントの独立性が高まり、機能ごとのテストが容易になります。

2. **サービスロケーター (GetIt)**
   - `get_it` パッケージによる依存性注入（DI）パターンを採用し、サービスのライフサイクル管理と疎結合を実現します。
   - BLoCやUIコンポーネントが必要とするサービスへのアクセスを一元管理します。

3. **ハイブリッドストレージ**
   - `HybridStorageService` を中心に、データの永続化戦略を抽象化します。
   - モノログのメタデータはローカルDB（SQLite）とクラウド（Firestore）に同期的に保存され、オフライン対応とデータ保護を両立します。
   - 画像データはデバイスのローカルストレージに保存されます。

## 主要コンポーネント (`lib` ディレクトリ構成)

### 1. プレゼンテーション層 (`lib/screens`, `lib/widgets`, `lib/blocs`)

- **Screens**: 各画面のUIを構築するWidgetです。ユーザーのアクションを受け付け、BLoCにイベントを通知します。
- **Widgets**: 画面間で再利用される汎用的なUIコンポーネントです。
- **BLoCs**: プレゼンテーション層からのイベントを受け取り、アプリケーション層のサービスと連携してビジネスロジックを実行し、UIの状態（State）を更新します。

#### 主要画面構成
- **OnboardingScreen**: アプリの初回利用時に表示されるオンボーディング画面です。
- **DiagnosisScreen**: ユーザーのタイプを診断する画面です。
- **SimpleHomeScreen**: アプリのメイン画面。ここからモノログ作成フローを開始します。
- **CameraScreen / CameraPreviewScreen**: 写真の撮影とプレビューを行います。
- **RangeSelectionScreen**: 撮影した写真の中から、対象となる「モノ」の範囲を選択します。
- **EmotionSelectionScreen**: モノに対する感情を選択します。
- **CompletionScreen**: モノの名前、メモを入力し、モノログを完成させます。
- **MyLogListScreen / MyLogDetailScreen**: 過去のモノログを一覧表示し、詳細を確認します。
- **SettingsScreen**: アプリケーションの設定を行う画面です。

### 2. アプリケーション層 (`lib/services`)

アプリケーションのビジネスロジックの中核を担うサービス群です。UIには依存せず、純粋なDartコードで記述されます。

- **`HybridStorageService`**: データの保存、読み込み、更新、削除（CRUD）を担当する中心的なサービス。FirestoreとローカルDBへのアクセスを抽象化します。
- **`AuthService`**: Firebase Authenticationを利用した匿名認証の管理を担当します。
- **`ImageAnalysisService`**: `tflite_flutter` を利用し、画像内のオブジェクト検出など、機械学習モデルの推論を実行します。
- **`ImageProcessingService`**: 画像の切り抜き、圧縮、フォーマット変換などの処理を担当します。
- **`GuideService`**: オンボーディングやチュートリアルの進捗状況を管理します。

### 3. ドメイン層 (`lib/models`)

アプリケーション全体で利用されるデータ構造（エンティティ）を定義します。

- **`MonologModel`**: 一つのモノログ全体を表すデータモデルです。
- **`ObjectModel`**: モノログの対象となる「モノ」のデータモデルです。
- **`EmotionData`**: 感情のデータモデルです。

### 4. インフラストラクチャ層 (`lib/core`, `lib/services`の一部)

外部システムやプラットフォームの機能との連携を担当します。

- **`FirestoreService`**: Google Firestoreとのデータ送受信を担当します。
- **`DatabaseHelper`**: `sqflite` を用いてローカルのSQLiteデータベースを操作します。
- **`camera` / `image_picker`**: デバイスのカメラ機能やギャラリーへのアクセスを提供します。

## データフロー

### モノログ作成フロー
```
1. SimpleHomeScreenからカメラを起動
   ↓
2. CameraScreenで写真を撮影し、CameraPreviewScreenで確認
   ↓
3. RangeSelectionScreenでモノの範囲を指定
   ↓
4. EmotionSelectionScreenで感情を選択
   ↓
5. CompletionScreenでモノの名前やメモを入力し、保存をトリガー
   ↓
6. MonologBloc / ObjectBlocがイベントを受け取り、状態を更新
   ↓
7. HybridStorageServiceが呼び出され、以下の処理を実行
   ├─ 画像データ: ローカルストレージに保存
   └─ メタデータ: ローカルDB (SQLite) と Firestore に保存
   ↓
8. MyLogListScreenにリダイレクトされ、新しいモノログが表示される
```

## 技術スタック

### フロントエンド
- Flutter 3.x
- Dart 3.x
- Material Design 3

### 状態管理
- **flutter_bloc / bloc**: リアクティブな状態管理
- **GetIt**: サービスロケーター (依存性注入)

### バックエンド
- **Firebase (BaaS)**
  - **Authentication**: 匿名認証
  - **Cloud Firestore**: クラウドデータベース
  - **Remote Config**: フィーチャーフラグ管理
  - **Analytics**: 利用状況分析
  - **Crashlytics**: クラッシュレポート

### 主要パッケージ
- `camera`: カメラ機能
- `image_picker`: 画像選択
- `tflite_flutter`: 機械学習モデルの実行
- `sqflite`: ローカルリレーショナルデータベース
- `path_provider`: ファイルシステムパス管理
- `shared_preferences`: 軽量なKey-Valueストレージ
- `get_it`: サービスロケーター
- `equatable`: オブジェクトの比較を簡略化
- `firebase_core`, `firebase_auth`, `cloud_firestore` など
