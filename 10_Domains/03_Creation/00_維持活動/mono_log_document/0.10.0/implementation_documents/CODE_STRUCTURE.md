# モノログアプリ コード構成ドキュメント

## 概要
このドキュメントは、モノログアプリ（バージョン0.10.0+6）のコード構成について、コードを直接参照できない環境でも理解できるよう体系的にまとめたものです。

## プロジェクト構造

### ルートディレクトリ
```
mono_log_app/
├── lib/                    # Flutterアプリケーションのソースコード
├── test/                   # テストコード
├── assets/                 # 画像、フォントなどのリソース
├── android/                # Android固有の設定
├── ios/                    # iOS固有の設定
├── docs/                   # ドキュメント
└── pubspec.yaml           # プロジェクト設定と依存関係
```

## lib/ ディレクトリ構造

### 1. エントリーポイント
- **main.dart**: アプリケーションのエントリーポイント
- **mono_log_app.dart**: アプリケーションのルートウィジェット定義

### 2. blocs/ - 状態管理（BLoCパターン）
アプリケーションの状態管理にBLoC（Business Logic Component）パターンを採用。

#### 主要なBLoC
- **auth/**: 認証関連
  - auth_bloc.dart: 認証ロジック
  - auth_event.dart: 認証イベント定義
  - auth_state.dart: 認証状態定義

- **monolog/**: モノログ機能
  - monolog_bloc.dart: モノログの作成、読み込み、更新、削除
  - monolog_event.dart: CRUD操作イベント
  - monolog_state.dart: モノログリストや操作状態

- **object/**: オブジェクト（フォルダ）管理
  - object_bloc.dart: フォルダの管理ロジック
  - object_event.dart: フォルダ操作イベント
  - object_state.dart: フォルダ状態

- **tutorial/**: チュートリアル制御
  - tutorial_bloc.dart: チュートリアル進行管理
  - tutorial_event.dart: チュートリアルイベント
  - tutorial_state.dart: チュートリアル状態

- **その他**:
  - camera_bloc.dart: カメラ制御
  - story_bloc.dart: ストーリー（フォルダ）関連
  - monolog_record_bloc.dart: モノログ記録プロセス管理

### 3. models/ - データモデル
アプリケーションで使用される全てのデータ構造を定義。

#### 主要モデル
- **monolog_model.dart**: モノログデータ構造
  - logId: 一意識別子
  - imagePath: 画像パス
  - cropRect: 切り抜き範囲
  - primaryEmotion: 第1感情
  - secondaryEmotion: 第2感情
  - memo: メモ
  - title: タイトル
  - createdAt: 作成日時

- **custom_emotion_model.dart**: カスタム感情
- **emotion_data.dart**: 感情マスターデータ
- **object_models.dart**: フォルダモデル
- **sync_status.dart**: 同期状態管理
- **analytics_data_models.dart**: 分析データ
- **diagnosis_models.dart**: 診断機能モデル
- **prompt_model.dart**: プロンプトモデル

### 4. screens/ - 画面コンポーネント
各画面の実装。1画面1ファイルの原則。

#### モノログフロー画面
1. **simple_home_screen.dart**: ホーム画面
2. **camera_preview_screen.dart**: カメラプレビュー画面
3. **range_selection_screen.dart**: 範囲選択画面
4. **monolog_recording_screen.dart**: 感情選択画面
5. **completion_screen.dart**: 完了画面

#### マイログ機能画面
- **mylog_screen.dart**: マイログ一覧（タブ付き）
- **mylog_detail_screen.dart**: マイログ詳細

#### その他の画面
- **settings_screen.dart**: 設定画面
- **emotion_management_screen.dart**: カスタム感情管理
- **story_detail_screen.dart**: フォルダ詳細
- **onboarding_screen.dart**: オンボーディング
- **diagnosis_screen.dart**: 診断画面
- **diagnosis_result_screen.dart**: 診断結果
- **image_crop_screen.dart**: 画像クロップ
- **monolog_memo_screen.dart**: メモ編集

### 5. services/ - ビジネスロジックとサービス
アプリケーションのコア機能を提供するサービス層。

#### データ管理サービス
- **hybrid_storage_service.dart**: ハイブリッドストレージ（ローカル+クラウド）
- **database_helper.dart**: SQLiteデータベース管理
- **firestore_service.dart**: Firestore連携
- **memory_storage_service.dart**: メモリストレージ

#### 機能サービス
- **auth_service.dart**: 認証サービス
- **camera_service.dart**: カメラ制御
- **emotion_service.dart**: 感情データ管理
- **story_service.dart**: フォルダ管理
- **operation_guide_service.dart**: 操作ガイド
- **analytics_service.dart**: アナリティクス
- **log_service.dart**: ログ管理
- **image_processing_service.dart**: 画像処理

#### サポートサービス
- **crisis_support_service.dart**: 危機サポート
- **support_service.dart**: ユーザーサポート
- **guide_service.dart**: ガイド機能
- **tutorial_controller.dart**: チュートリアル制御

### 6. widgets/ - 再利用可能なUIコンポーネント

#### 感情選択UI
- **circular_emotion_selector.dart**: 円形感情セレクター
- **emotion_button_flat.dart**: フラット感情ボタン
- **emotion_button_stadium.dart**: スタジアム型感情ボタン
- **emotion_grid_selector.dart**: グリッド感情セレクター
- **secondary_emotion_grid.dart**: 第2感情グリッド
- **custom_emotion_creator.dart**: カスタム感情作成

#### ガイド・チュートリアル
- **operation_guide_overlay.dart**: 操作ガイドオーバーレイ
- **guide_overlay.dart**: ガイドオーバーレイ
- **tutorial_spotlight.dart**: チュートリアルスポットライト
- **tutorial_progress_bar.dart**: チュートリアル進捗バー

#### その他のウィジェット
- **app_button.dart**: 共通ボタン
- **help_button.dart**: ヘルプボタン
- **emotion_diary_card.dart**: 感情日記カード
- **story_selection_bottom_sheet.dart**: フォルダ選択シート
- **cropped_image_widget.dart**: クロップ済み画像表示

### 7. core/ - コア機能とユーティリティ

#### 基底クラス
- **base_classes/base_screen.dart**: 画面の基底クラス

#### 設定
- **config/app_config.dart**: アプリケーション設定

#### 定数
- **constants/app_constants.dart**: アプリ定数
- **constants/error_codes.dart**: エラーコード定義

#### インターフェース
- **interfaces/base_service.dart**: サービス基底インターフェース
- **interfaces/storage_interface.dart**: ストレージインターフェース

#### ナビゲーション
- **navigation/app_routes.dart**: ルート定義

#### サービスロケーター
- **services/service_locator.dart**: 依存性注入（GetIt使用）

### 8. config/ - アプリケーション設定
- **app_colors.dart**: カラーパレット定義
- **app_strings.dart**: 文字列定数
- **app_typography.dart**: タイポグラフィ定義
- **feature_flags.dart**: 機能フラグ

### 9. styles/ - スタイル定義
- **guide_styles.dart**: ガイド関連のスタイル

### 10. utils/ - ユーティリティ
- **database_backup.dart**: データベースバックアップ
- **fade_page_route.dart**: ページ遷移アニメーション
- **haptic_feedback.dart**: 触覚フィードバック
- **navigation_helper.dart**: ナビゲーションヘルパー
- **text_extract_util.dart**: テキスト抽出ユーティリティ

## アーキテクチャパターン

### 1. BLoCパターン
- **責務分離**: UI、ビジネスロジック、データ層の明確な分離
- **イベント駆動**: ユーザーアクションをイベントとして処理
- **状態管理**: アプリケーション状態の一元管理

### 2. レイヤードアーキテクチャ
```
UI層 (screens, widgets)
  ↓
BLoC層 (blocs)
  ↓
サービス層 (services)
  ↓
データ層 (models, database)
```

### 3. 依存性注入
- GetItを使用したサービスロケーターパターン
- サービスの疎結合化

## データフロー

### モノログ作成フロー
1. **画像撮影/選択** → CameraService
2. **範囲選択** → 画面内で処理
3. **感情選択** → EmotionService
4. **データ保存** → MonologBloc → HybridStorageService
5. **完了通知** → CompletionScreen

### データ同期フロー
1. **ローカル保存** → SQLite (database_helper.dart)
2. **バックグラウンド同期** → FirestoreService
3. **同期状態管理** → SyncStatus

## 主要な依存関係

### 外部パッケージ（pubspec.yaml）
- **flutter_bloc**: 状態管理
- **get_it**: 依存性注入
- **sqflite**: ローカルデータベース
- **cloud_firestore**: クラウドストレージ
- **firebase_auth**: 認証
- **camera**: カメラ機能
- **image_picker**: 画像選択
- **image_cropper**: 画像クロップ

### 内部依存関係
- Screens → BLoCs → Services → Models
- Widgets は独立したコンポーネント
- Core は全体で共有される基盤機能

## セキュリティとプライバシー
- **SecurityService**: データ暗号化
- **AuthService**: ユーザー認証
- ローカルファーストアプローチ
- オプショナルなクラウド同期

## テスト構造
```
test/
├── unit/           # 単体テスト
├── widget/         # ウィジェットテスト
└── integration/    # 統合テスト
```

## ビルドと配布
- **Android**: Google Play Store
- **iOS**: App Store
- **バージョン管理**: pubspec.yaml で管理
- **環境設定**: dev, staging, production

このドキュメントは、コードを直接参照せずともアプリケーションの構造と設計を理解できるよう作成されています。各コンポーネントの詳細な実装については、実際のソースコードを参照してください。