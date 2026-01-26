# モノログ。 - アプリケーションアーキテクチャレポート

## プロジェクト概要
- **プロジェクト名**: モノログ。(mono_log_app)
- **バージョン**: 0.6.0
- **更新日**: 2025年8月3日
- **プラットフォーム**: Flutter (クロスプラットフォーム対応)
- **対応OS**: iOS、Android、Web、Windows、macOS、Linux

## アーキテクチャ概要

### レイヤード・アーキテクチャ

本アプリケーションは、クリーンアーキテクチャの原則に基づいた4層構造を採用しています：

```
┌─────────────────────────────────────────────────┐
│             Presentation Layer                  │
│    (Screens, Widgets, Controllers)              │
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

1. **ハイブリッドストレージアーキテクチャ**
   - ローカルファイルストレージ（写真）
   - クラウドストレージ（メタデータ）
   - オフライン対応とオンライン同期

2. **サービスロケーターパターン**
   - GetItによる依存性注入
   - サービスの疎結合化
   - テスタビリティの向上

3. **基底クラスパターン**
   - BaseScreenによる共通機能の抽象化
   - 一貫性のある画面実装
   - エラーハンドリングの統一

## 主要コンポーネント

### 1. プレゼンテーション層

#### 画面構成
- **SimpleHomeScreen**: シンプルなホーム画面
  - 大きなカメラボタン
  - マイログへのアクセス
  - 設定とガイドへのリンク

- **CameraCaptureScreen**: カメラ撮影画面
  - 写真撮影機能
  - ギャラリーからの選択
  - 撮影後の確認

- **SpotlightSelectionScreen**: スポットライト選択画面
  - AI提案による切り抜き候補
  - 手動範囲選択
  - 選択領域のプレビュー

- **MonologFlowScreen**: モノログフロー画面
  - 2タップ感情選択
  - 任意メモ入力
  - 自動保存機能

- **LogScreen**: ログ一覧画面
  - モノログの一覧表示
  - 検索・フィルタリング
  - 詳細画面への遷移

#### ウィジェット
- **TwoTapEmotionSelector**: 2タップ感情選択ウィジェット
  - 第1階層: 5つの感情カテゴリ
  - 第2階層: 各6つの詳細感情
  - アニメーション付きUI

- **TutorialGuideOverlay**: チュートリアルガイドオーバーレイ
  - 統合された状態管理
  - エラー回復機能
  - 画面別ガイド表示

- **TutorialNavigationGuard**: ナビゲーション制御
  - チュートリアル中の画面遷移制限
  - 状態に応じた制御

### 2. アプリケーション層

#### コアサービス

- **HybridStorageService**: ハイブリッドストレージサービス
  ```dart
  - savePhoto(): ローカルに写真を保存
  - saveMetadata(): Firestoreにメタデータを保存
  - cleanupOrphaned(): 孤立したデータのクリーンアップ
  ```

- **TutorialController**: チュートリアル制御
  ```dart
  - 6段階のチュートリアルフロー
  - 進行状況の追跡
  - スキップ機能
  ```

- **CrisisSupportService**: 危機対応サービス
  ```dart
  - detectCrisisKeywords(): 危機キーワード検出
  - showSupportDialog(): サポートダイアログ表示
  - 緊急連絡先情報
  ```

- **EmotionPaletteService**: 感情パレットサービス
  ```dart
  - getEmotionColor(): 感情に応じた色取得
  - getEmotionIcon(): 感情アイコン取得
  - generateGradient(): グラデーション生成
  ```

- **AutoNamingService**: 自動命名サービス
  ```dart
  - generateObjectName(): モノの名前生成
  - generateMonologTitle(): モノログタイトル生成
  - 日時ベースの命名規則
  ```

### 3. ドメイン層

#### データモデル

- **MonologModel**: モノログデータモデル
  ```dart
  - logId: 一意識別子
  - userId: ユーザーID
  - objectId: オブジェクトID
  - tier1Emotion: 第1階層感情
  - tier2Emotion: 第2階層感情
  - memo: 任意メモ
  - createdAt: 作成日時
  ```

- **ObjectModel**: オブジェクトデータモデル
  ```dart
  - objectId: 一意識別子
  - userId: ユーザーID
  - physicalName: 物理名
  - mainImageUrl: メイン画像URL
  - createdAt: 作成日時
  ```

- **EmotionTier**: 感情階層モデル
  ```dart
  - id: 感情ID
  - label: 表示ラベル
  - emoji: 絵文字
  - color: テーマカラー
  - tier2Emotions: 第2階層感情リスト
  ```

### 4. インフラストラクチャ層

#### ストレージ
- **LocalFileHandler**: ローカルファイル管理
- **FirestoreService**: Firestore連携
- **StorageInterface**: ストレージ抽象インターフェース

#### 外部サービス連携
- **Firebase Authentication**: 認証
- **Firebase Firestore**: データベース
- **Firebase Analytics**: 分析
- **Firebase Crashlytics**: クラッシュレポート
- **Firebase Remote Config**: リモート設定

## データフロー

### モノログ作成フロー
```
1. カメラ撮影/ギャラリー選択
   ↓
2. スポットライト選択（オプション）
   ↓
3. 2タップ感情選択
   ↓
4. メモ入力（任意）
   ↓
5. 自動保存
   ├─ 写真: ローカルストレージ
   └─ メタデータ: Firestore
```

### チュートリアルフロー
```
1. 初回起動検出
   ↓
2. オンボーディング
   ↓
3. 診断
   ↓
4. カメラ操作
   ↓
5. 感情選択
   ↓
6. モノログフロー
   ↓
7. 命名
   ↓
8. 完了
```

## セキュリティとプライバシー

### データ保護
- 写真データのローカル保存
- Firebase Authenticationによる認証
- ユーザー別データ分離
- HTTPS通信の強制

### プライバシー配慮
- 位置情報の非収集
- 最小限のパーミッション要求
- オプトインベースの分析

## パフォーマンス最適化

### 画像処理
- 効率的な画像圧縮
- サムネイル生成
- 遅延読み込み

### メモリ管理
- 画像キャッシュの適切な管理
- ウィジェットの効率的な再利用
- メモリリークの防止

### ネットワーク最適化
- オフライン対応
- バッチ同期処理
- 再試行メカニズム

## 開発ガイドライン

### コーディング規約
- Effective Dartガイドラインの遵守
- 明確な命名規則
- 適切なコメントとドキュメント

### アーキテクチャ原則
- 単一責任の原則（SRP）
- 依存性逆転の原則（DIP）
- インターフェース分離の原則（ISP）

### テスト戦略
- ユニットテスト: ビジネスロジック
- ウィジェットテスト: UI コンポーネント
- 統合テスト: エンドツーエンドフロー

## 今後の拡張計画

### 短期計画（〜3ヶ月）
- [ ] AIスポットライト機能の本格実装
- [ ] 感情分析の高度化
- [ ] 共有機能の追加

### 中期計画（3〜6ヶ月）
- [ ] マルチユーザー対応
- [ ] データエクスポート機能
- [ ] 高度な検索・フィルタリング

### 長期計画（6ヶ月〜）
- [ ] 機械学習による感情予測
- [ ] ソーシャル機能の追加
- [ ] プレミアムプランの導入

## 技術スタック

### フロントエンド
- Flutter 3.x
- Dart 3.x
- Material Design 3

### バックエンド
- Firebase (BaaS)
- Cloud Functions（予定）

### 状態管理
- Provider Pattern
- GetIt (Service Locator)

### 主要パッケージ
- camera: カメラ機能
- image_picker: 画像選択
- path_provider: ファイルパス管理
- shared_preferences: ローカル設定
- firebase_core: Firebase基盤
- firebase_auth: 認証
- cloud_firestore: データベース
- crypto: 暗号化
- get_it: 依存性注入
- uuid: UUID生成
- intl: 国際化

## まとめ

モノログ。アプリは、モノとの対話を通じて自己理解を深めるという独自のコンセプトを、洗練されたアーキテクチャで実現しています。ハイブリッドストレージによるオフライン対応、2タップ感情選択による使いやすさ、包括的なチュートリアルシステムなど、ユーザー体験を最優先に設計されています。

今後も継続的な改善と新機能の追加により、より多くのユーザーの心の健康と自己理解をサポートしていきます。