# モノログアプリ アプリケーションフロー詳細

## 概要
このドキュメントは、モノログアプリの主要な機能フローと画面遷移について、実装の詳細を含めて説明します。

## 1. アプリケーション起動フロー

### 初期化プロセス
1. **main.dart**
   - Flutterバインディングの初期化
   - Firebaseの初期化
   - サービスロケーター（GetIt）の設定
   - BLoCプロバイダーの設定

2. **サービス初期化** (service_locator.dart)
   - DatabaseHelper（SQLite）
   - FirestoreService
   - AuthService
   - OperationGuideService
   - その他各種サービス

3. **初期画面の決定**
   - 初回起動 → OnboardingScreen
   - 2回目以降 → SimpleHomeScreen

## 2. 主要機能フロー

### A. モノログ作成フロー

#### ステップ1: ホーム画面から開始
- **画面**: SimpleHomeScreen
- **アクション**: 「モノログを始める」カードタップ
- **遷移**: Navigator.pushNamed(context, AppRoutes.cameraPreview)

#### ステップ2: 写真撮影/選択
- **画面**: CameraPreviewScreen
- **サービス**: CameraService
- **選択肢**:
  1. カメラで撮影 → _takePicture()
  2. ギャラリーから選択 → _selectFromGallery()
- **データ**: 画像パス（String）
- **遷移**: Navigator.pushReplacementNamed(context, AppRoutes.rangeSelection, arguments: {'imagePath': path})

#### ステップ3: 範囲選択
- **画面**: RangeSelectionScreen
- **実装**: 
  - GestureDetectorでドラッグ検知
  - CustomPainterで青枠描画
  - 座標変換ロジック（画面座標→実画像座標）
- **データ**: cropRect（Rect）
- **遷移**: Navigator.pushReplacementNamed(context, AppRoutes.emotionSelection)

#### ステップ4: 感情選択
- **画面**: MonologRecordingScreen
- **BLoC**: MonologRecordBloc
- **フロー**:
  1. 第1感情選択（5つの基本感情）
  2. 第2感情選択（6つの詳細感情）
  3. メモ入力（任意、最大500文字）
- **カスタム感情**: 
  - 「カスタム感情を選択」ボタン → EmotionManagementScreen
- **データ**: primaryEmotion, secondaryEmotion, memo
- **保存**: MonologBloc.add(CreateMonolog(...))

#### ステップ5: 完了画面
- **画面**: CompletionScreen
- **アニメーション**:
  - 背景グラデーション（感情に応じた色）
  - 光の粒子エフェクト
  - カード出現アニメーション（3D風）
- **遷移オプション**:
  1. カードタップ → MyLogDetailScreen
  2. 「続けてモノログする」 → CameraPreviewScreen
  3. 「ホーム画面に戻る」 → SimpleHomeScreen

### B. マイログ管理フロー

#### マイログ一覧
- **画面**: MyLogScreen
- **タブ構成**:
  1. すべてのマイログ（デフォルト）
  2. フォルダ別マイログ
- **表示モード**:
  - リストビュー（1列）
  - ギャラリービュー（2列グリッド）
- **フィルター/ソート**:
  - 感情別フィルター
  - 日付順ソート（新しい順/古い順）
- **データ取得**: MonologBloc.add(LoadMonologs())

#### マイログ詳細
- **画面**: MyLogDetailScreen
- **モード**:
  1. 閲覧モード（デフォルト）
  2. 編集モード
- **機能**:
  - タイトル編集
  - メモ編集
  - 記録削除（確認ダイアログ付き）
- **データ更新**: MonologBloc.add(UpdateMonolog(...))

### C. カスタム感情管理フロー

- **画面**: EmotionManagementScreen
- **機能**:
  1. カスタム感情一覧表示
  2. 新規作成（名前と色選択）
  3. 編集（名前と色変更）
  4. 削除（確認ダイアログ付き）
- **データ管理**: CustomOptionsService
- **最大数**: 10個まで

### D. フォルダ管理フロー

#### フォルダ作成
- **トリガー**: マイログ詳細画面でフォルダ設定
- **UI**: StorySelectionBottomSheet
- **機能**: 既存フォルダ選択 or 新規作成

#### フォルダ詳細
- **画面**: StoryDetailScreen
- **表示内容**:
  - フォルダ内のモノログ一覧
  - サマリー情報（件数、期間など）
- **編集**: フォルダ名の変更

## 3. データ管理フロー

### ローカルストレージ
```
SQLite (database_helper.dart)
├── monologs テーブル
├── stories テーブル
├── custom_emotions テーブル
└── sync_status テーブル
```

### クラウド同期
```
Firestore (firestore_service.dart)
├── users/
│   └── {userId}/
│       ├── monologs/
│       ├── stories/
│       └── settings/
```

### ハイブリッドストレージ戦略
1. **作成時**: ローカル保存 → バックグラウンド同期
2. **読み込み時**: ローカル優先 → 差分取得
3. **更新時**: ローカル更新 → 同期キュー
4. **削除時**: ソフトデリート → 同期後物理削除

## 4. 状態管理パターン

### BLoCの責務分担
- **MonologBloc**: モノログのCRUD操作
- **StoryBloc**: フォルダ管理
- **AuthBloc**: 認証状態
- **TutorialBloc**: チュートリアル進行

### イベントフロー例（モノログ作成）
```
1. UI: 保存ボタンタップ
2. Event: CreateMonolog(data)
3. Bloc: 
   - Emit: MonologCreating
   - Service呼び出し
   - Emit: MonologCreated or MonologError
4. UI: 状態に応じて画面更新
```

## 5. エラーハンドリング

### エラー種別
1. **ネットワークエラー**: オフライン時の処理継続
2. **ストレージエラー**: 容量不足の警告
3. **権限エラー**: カメラ/ギャラリーアクセス
4. **同期エラー**: リトライ機構

### エラー表示
- SnackBar: 一時的なエラー
- ダイアログ: 重要なエラー
- 画面内メッセージ: 永続的なエラー

## 6. パフォーマンス最適化

### 画像処理
- **圧縮**: 保存前に画質調整
- **キャッシュ**: メモリキャッシュ活用
- **遅延読み込み**: リスト表示時

### データベース
- **インデックス**: 日付、感情でのクエリ最適化
- **バッチ処理**: 複数レコードの一括操作
- **トランザクション**: データ整合性確保

## 7. セキュリティ実装

### データ保護
- **暗号化**: SecurityServiceによる機密データ暗号化
- **アクセス制御**: ユーザーごとのデータ分離
- **セッション管理**: 自動ログアウト機能

### プライバシー
- **ローカルファースト**: デフォルトでローカル保存
- **明示的同期**: ユーザー同意後のクラウド同期
- **データ削除**: 完全削除オプション

## 8. UI/UXパターン

### アニメーション
- **画面遷移**: FadePageRoute
- **感情選択**: 円形配置アニメーション
- **完了画面**: 3Dカード出現

### フィードバック
- **触覚**: HapticFeedback
- **視覚**: プログレスインジケーター
- **音声**: （将来実装予定）

### アクセシビリティ
- **テキストサイズ**: システム設定対応
- **コントラスト**: WCAG準拠
- **スクリーンリーダー**: Semantics対応

## 9. テスト戦略

### 単体テスト
- Service層: ビジネスロジック
- BLoC層: 状態遷移
- Model層: データ変換

### ウィジェットテスト
- 画面レイアウト
- ユーザーインタラクション
- アニメーション

### 統合テスト
- エンドツーエンドフロー
- データ永続化
- 同期処理

## 10. デバッグとモニタリング

### ログ出力
- **LoggingService**: 構造化ログ
- **レベル**: Debug, Info, Warning, Error
- **フィルタリング**: 機能別、重要度別

### 分析
- **AnalyticsService**: ユーザー行動追跡
- **イベント**: 画面遷移、機能使用
- **パフォーマンス**: 処理時間計測

このドキュメントにより、コードを直接参照できない環境でも、アプリケーションの動作フローと実装の詳細を理解することができます。