# 画面と機能の詳細

このドキュメントでは、モノログアプリの全23画面の詳細と、それぞれの機能について説明します。

## 画面一覧

### 1. 初期フロー画面

#### 1.1 スプラッシュ画面 (splash_screen.dart)
- **概要**: アプリ起動時のスプラッシュ画面
- **機能**: 
  - Firebase初期化の待機
  - 認証状態の確認
  - 次画面への自動遷移

#### 1.2 オンボーディング画面 (onboarding_screen.dart)
- **概要**: 初回起動時のアプリ紹介
- **機能**:
  - アプリコンセプトの説明
  - 主要機能の紹介
  - 診断画面への誘導

#### 1.3 初期診断画面 (initial_diagnosis_screen.dart)
- **概要**: ユーザーの特性を診断する初期設定
- **機能**:
  - 6つのタイプから診断
  - 診断結果の保存
  - ホーム画面への遷移

### 2. メイン画面

#### 2.1 シンプルホーム画面 (simple_home_screen.dart)
- **概要**: アプリのメインハブ
- **機能**:
  - 中央のカメラボタンで撮影開始
  - ナビゲーションメニュー
  - 最近の記録の表示
- **主要コンポーネント**:
  ```dart
  - AnimatedCameraButton: パルスアニメーション付きカメラボタン
  - NavigationDrawer: サイドメニュー
  - RecentLogsWidget: 最近の記録表示
  ```

#### 2.2 マイログ画面 (my_log_screen.dart)
- **概要**: ユーザーの全記録を管理
- **機能**:
  - モノごとの記録一覧
  - フィルタリング機能
  - 詳細画面への遷移
- **データ表示**:
  - ObjectModelとLogModelの統合表示
  - タイムライン形式での表示

### 3. カメラ・撮影フロー

#### 3.1 カメラキャプチャ画面 (camera_capture_screen.dart)
- **概要**: モノの撮影インターフェース
- **機能**:
  - カメラプレビュー
  - 撮影ガイド表示
  - 画像の一時保存
- **技術詳細**:
  - CameraControllerの管理
  - 画像圧縮処理
  - Firebase Storageへのアップロード準備

#### 3.2 画像確認画面 (image_confirmation_screen.dart)
- **概要**: 撮影した画像の確認
- **機能**:
  - 画像のプレビュー
  - 再撮影オプション
  - 次ステップへの確認

### 4. 内省・記録フロー

#### 4.1 マイクロジャーナリング画面 (micro_journaling_screen.dart) - 1860行
- **概要**: アプリの中核となる内省記録画面
- **機能**:
  - 3つの感情ベクター選択（ポジティブ、複雑、不明）
  - 段階的な質問フロー
  - 感情の詳細記録
- **画面構成**:
  ```dart
  1. VectorSelectionView: 感情ベクター選択
  2. QuestionFlowView: 構造化された質問
  3. EmotionSelectionView: 詳細な感情選択
  4. SummaryView: 記録内容の確認
  ```

#### 4.2 ログ保存画面 (save_log_screen.dart)
- **概要**: 記録の保存と確認
- **機能**:
  - 記録内容のプレビュー
  - タグ付け機能
  - Firestoreへの保存

#### 4.3 登録カード画面 (registration_card_screen.dart)
- **概要**: モノの「戸籍」登録
- **機能**:
  - ObjectModelの作成
  - LogModelとの関連付け
  - カード形式での表示

### 5. 詳細・振り返り画面

#### 5.1 ログ詳細画面 (log_detail_screen.dart)
- **概要**: 個別記録の詳細表示
- **機能**:
  - 記録内容の完全表示
  - 編集・削除機能
  - 関連するモノの情報表示

#### 5.2 振り返りカード画面 (reflection_card_screen.dart)
- **概要**: 過去の記録を振り返る
- **機能**:
  - カード形式での表示
  - スワイプナビゲーション
  - インサイトの発見支援

### 6. 診断・分析画面

#### 6.1 診断結果画面 (diagnosis_result_screen.dart)
- **概要**: 6つのタイプ診断の結果表示
- **機能**:
  - タイプの詳細説明
  - 特性の可視化
  - アドバイスの提供

#### 6.2 深掘り診断画面 (deep_diagnosis_screen.dart)
- **概要**: より詳細な自己分析
- **機能**:
  - 追加の質問セット
  - 詳細な分析結果
  - 成長のヒント提供

### 7. 設定・管理画面

#### 7.1 設定画面 (settings_screen.dart)
- **概要**: アプリの各種設定
- **機能**:
  - プロフィール管理
  - 通知設定
  - データ管理オプション
  - ログアウト機能

#### 7.2 利用規約画面 (terms_of_service_screen.dart)
- **概要**: 利用規約の表示
- **機能**:
  - 規約内容の表示
  - 同意状態の管理

#### 7.3 プライバシーポリシー画面 (privacy_policy_screen.dart)
- **概要**: プライバシーポリシーの表示
- **機能**:
  - ポリシー内容の表示
  - データ取り扱いの説明

### 8. ヘルプ・ガイド画面

#### 8.1 チュートリアル画面 (tutorial_screen.dart)
- **概要**: アプリの使い方ガイド
- **機能**:
  - ステップバイステップの説明
  - インタラクティブなデモ
  - スキップ機能

#### 8.2 アプリガイド画面 (app_guide_screen.dart)
- **概要**: 機能別の詳細ガイド
- **機能**:
  - 各機能の説明
  - FAQ
  - トラブルシューティング

### 9. その他の画面

#### 9.1 オブジェクト詳細画面 (object_detail_screen.dart)
- **概要**: モノの詳細情報表示
- **機能**:
  - モノの基本情報
  - 関連する全ログの表示
  - タイムライン表示

#### 9.2 感情選択画面 (emotion_selection_screen.dart)
- **概要**: 詳細な感情選択インターフェース
- **機能**:
  - 感情カテゴリの選択
  - 感情の強度設定
  - カスタム感情の入力

## 画面遷移フロー

### 初回起動フロー
```
SplashScreen → OnboardingScreen → InitialDiagnosisScreen → SimpleHomeScreen
```

### モノログ作成フロー
```
SimpleHomeScreen → CameraCaptureScreen → ImageConfirmationScreen 
→ MicroJournalingScreen → SaveLogScreen → RegistrationCardScreen
```

### 振り返りフロー
```
SimpleHomeScreen → MyLogScreen → LogDetailScreen/ReflectionCardScreen
```

## 主要な機能コンポーネント

### 1. カメラ機能
- **CameraController**: カメラの制御
- **ImagePicker**: ギャラリーからの選択
- **画像圧縮**: アップロード前の最適化

### 2. 感情分析システム
- **3つのベクター**: ポジティブ、複雑、不明
- **構造化された質問**: 段階的な内省サポート
- **感情タグ**: 詳細な感情の分類

### 3. データ同期
- **オフライン対応**: MemoryStorageService
- **リアルタイム同期**: Firestore listeners
- **画像管理**: Firebase Storage

### 4. ナビゲーション
- **TutorialController**: 初回ユーザーのガイド
- **NavigationGuard**: 画面遷移の制御
- **DeepLink対応**: 特定画面への直接遷移

## UI/UXの特徴

### 1. ミニマルデザイン
- シンプルで直感的なインターフェース
- 余白を活かしたレイアウト
- 集中を促すデザイン

### 2. アニメーション
- スムーズな画面遷移
- マイクロインタラクション
- フィードバックアニメーション

### 3. アクセシビリティ
- 大きなタップ領域
- 明確なビジュアルフィードバック
- テキストサイズの調整可能

## 技術的な実装詳細

各画面の詳細な実装については、[TECHNICAL_ARCHITECTURE.md](TECHNICAL_ARCHITECTURE.md)を参照してください。