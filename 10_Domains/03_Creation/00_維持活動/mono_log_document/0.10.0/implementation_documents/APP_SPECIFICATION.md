# モノログ。アプリケーション仕様書

## 概要

**アプリ名**: モノログ。  
**バージョン**: 0.10.0+6  
**プラットフォーム**: Flutter (iOS/Android/Web/Windows/macOS/Linux)  
**更新日**: 2025年8月17日

モノログ。は、身の回りのモノとの対話を通じて自己理解を深める内省支援アプリケーションです。

## 主要機能

### 1. モノログ記録機能

日常のモノを撮影し、感情を記録する5ステップのフローです。

#### フロー詳細

1. **ホーム画面 (HomeScreen)**
   - 画面中央に「モノログを始める」カードボタンを配置
   - タップでカメラプレビュー画面へ遷移

2. **写真撮影/選択 (CameraPreviewScreen)**
   - カメラプレビューが全画面表示
   - 撮影ボタン、カメラ切り替え、ギャラリー選択ボタンを配置
   - 撮影または選択後、範囲選択画面へ遷移

3. **範囲選択 (RangeSelectionScreen)**
   - 選択した画像を表示
   - ドラッグで矩形範囲を選択
   - 「次へ」ボタンで感情選択画面へ遷移

4. **感情選択 (EmotionSelectionScreen)**
   - 切り出した画像を画面上部に表示
   - 2段階の感情選択：
     - 第1段階: 5つの基本感情（喜び、落ち着き、モヤモヤ、悲しみ、驚き）
     - 第2段階: 選択した感情に関連する6つの詳細感情
   - カスタム感情の選択も可能（カスタム感情管理画面へ遷移）
   - メモ入力欄（最大500文字）と「記録する」ボタン

5. **記録完了 (CompletionScreen)**
   - 選択した感情に応じたグラデーション背景
   - 光や粒子のアニメーション効果
   - 作成したモノログカードを3Dアニメーションで表示
   - 「続けてモノログする」「ホーム画面に戻る」ボタン

### 2. マイログ機能

過去の記録を閲覧・管理する機能です。

- **一覧表示**: ギャラリー/リスト形式で切り替え可能
- **タブ表示**: 「すべてのマイログ」と「フォルダ」タブ
- **詳細表示**: 各記録の詳細情報とタイトル/メモの編集
- **削除機能**: 不要な記録の削除

### 3. フォルダ機能

モノログをグループ化して管理する機能です。

- フォルダの作成/編集/削除
- フォルダへのモノログ追加
- フォルダ内のモノログ一覧表示

### 4. 設定機能

- プロフィール管理
- プライバシーポリシー/利用規約の表示
- アプリバージョン情報

### 5. 操作ガイド機能

各画面に操作ガイドボタンを配置し、使い方を説明します。

## 技術仕様

### アーキテクチャ

- **状態管理**: BLoC (Business Logic Component)
- **依存性注入**: GetIt (Service Locator)
- **ストレージ**: ハイブリッド (ローカルファイル + SQLite + Firestore)
- **UIフレームワーク**: Material Design 3

### データモデル

#### MonologModel
```dart
class MonologModel {
  final String logId;           // UUID v4
  final String userId;          // Firebase UID
  final String? objectId;       // フォルダID (nullable)
  final String tier1Emotion;    // 第1階層感情ID
  final String tier2Emotion;    // 第2階層感情ID
  final String? customEmotion;  // カスタム感情 (nullable)
  final String? memo;           // メモ（最大500文字）
  final String? title;          // タイトル
  final DateTime createdAt;     // 作成日時
  final DateTime? updatedAt;    // 更新日時
  final bool isDeleted;         // 論理削除フラグ
}
```

#### ObjectModel (フォルダ)
```dart
class ObjectModel {
  final String objectId;        // UUID v4
  final String userId;          // Firebase UID
  final String physicalName;    // 物理名（自動生成）
  final String? customName;     // カスタム名（ユーザー定義）
  final String mainImageUrl;    // メイン画像パス
  final String? thumbnailUrl;   // サムネイル画像パス
  final List<String> tags;      // タグリスト
  final DateTime createdAt;     // 作成日時
  final DateTime? updatedAt;    // 更新日時
  final bool isArchived;        // アーカイブフラグ
}
```

### 主要パッケージ

- `camera`: カメラ機能
- `image_picker`: 画像選択
- `flutter_bloc`: 状態管理
- `get_it`: 依存性注入
- `shared_preferences`: ローカル設定保存
- `firebase_core`, `firebase_auth`, `cloud_firestore`: Firebase統合

## API仕様

### データ操作

#### モノログ作成
```dart
Future<MonologModel> createMonolog({
  required String userId,
  required String? objectId,
  required String tier1Emotion,
  required String tier2Emotion,
  String? customEmotion,
  String? memo,
  String? title,
})
```

#### フォルダ作成
```dart
Future<ObjectModel> createObject({
  required String userId,
  required String physicalName,
  String? customName,
  required String mainImageUrl,
  String? thumbnailUrl,
  List<String> tags = const [],
})
```

### エラーハンドリング

標準的なエラーコード体系:
- 1xxx: 認証関連エラー
- 2xxx: データベース関連エラー
- 3xxx: ネットワーク関連エラー
- 4xxx: ビジネスロジック関連エラー
- 5xxx: UI関連エラー

## セキュリティ

- Firebase Authentication による認証
- Firestore Security Rules によるアクセス制御
- HTTPS通信の強制
- 位置情報の非収集
- 最小限のパーミッション要求

## 今後の開発方針

現在のバージョン（0.10.0+6）では、基本的な機能が実装されています。今後は以下の改善を検討：

1. パフォーマンスの最適化
2. オフライン対応の強化
3. UIの洗練
4. 新機能の追加（統計・分析機能など）