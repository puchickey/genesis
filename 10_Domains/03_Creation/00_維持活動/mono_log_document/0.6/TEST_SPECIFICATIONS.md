# 『モノログ。』自動テスト仕様書

**作成日**: 2025年7月28日
**更新日**: 2025年8月3日
**バージョン**: Ver 0.6.0 ハイブリッドストレージ実装版
**対象**: 開発者・AI向けテスト技術仕様

---

## 📋 テストスイート概要

### 実装完了状況
- **総テスト数**: 43テスト
- **成功率**: 100%（全テスト成功）
- **テスト種類**: 単体・ウィジェット・統合・スモークテスト
- **実行環境**: Firebase依存排除・完全分離テスト
- **Service Locator**: GetIt によるDI対応テスト環境

### テスト分類詳細

#### 1. 単体テスト（15テスト）
- **MonologFlowScreen記録ロジック**: 6テスト
- **MylogGalleryScreenフィルタリング**: 4テスト  
- **StorageExceptionハンドリング**: 5テスト

#### 2. ウィジェットテスト（5テスト）
- **MylogGalleryScreen UI動作**: 5テスト
- **タイムアウト問題**: 解決済み

#### 3. 統合テスト（22テスト）
- **モノログ記録〜一覧表示フロー**: 7テスト
- **エラーハンドリング**: 15テスト

#### 4. スモークテスト（1テスト）
- **基本アプリ起動確認**: 1テスト

---

## 🏗️ テストアーキテクチャ

### StorageInterface抽象化
```dart
abstract class StorageInterface {
  Future<void> saveMonolog(MonologModel monolog);
  Future<List<MonologModel>> getAllMonologs();
  Future<List<MonologModel>> getMonologsByEmotion(String emotion);
  Future<void> deleteMonolog(String logId);
}
```

### HybridStorageService実装
```dart
class HybridStorageService implements StorageInterface {
  // ローカルファイルシステム（写真保存）
  // Firestore（メタデータ同期）
  // 孤立データクリーンアップ機能
}
```

### MockStorageInterface実装
```dart
class MockStorageInterface extends Mock implements StorageInterface {
  // mocktailベースの完全テスト分離実装
  // Firebase依存なしの高速テスト実行
}
```

### Service Locatorテスト設定
```dart
void setupTestServiceLocator() {
  getIt.registerSingleton<StorageInterface>(MockStorageInterface());
  getIt.registerSingleton<CrisisSupportService>(MockCrisisSupportService());
  getIt.registerSingleton<EmotionPaletteService>(EmotionPaletteService());
  getIt.registerSingleton<AutoNamingService>(AutoNamingService());
}
```

---

## 🆕 Ver 0.6.0 新規テスト要件

### HybridStorageServiceテスト
- **ローカル写真保存**: ファイルシステム操作の検証
- **Firestoreメタデータ同期**: 非同期処理の検証
- **孤立データクリーンアップ**: 整合性チェックの検証
- **オフライン動作**: ネットワーク切断時の挙動検証

### 新サービステスト
#### CrisisSupportServiceテスト
- **キーワード検出**: 日本語キーワードマッチング検証
- **閾値判定**: 危機レベル判定ロジック検証
- **Analytics統合**: イベント送信の検証

#### EmotionPaletteServiceテスト
- **カラーマッピング**: 感情別色彩割当の検証
- **アイコン選択**: 感情タイプ別アイコン検証
- **グラデーション生成**: 色彩遷移の検証

#### AutoNamingServiceテスト
- **命名ロジック**: 感情ベース命名の検証
- **重複回避**: ユニーク性保証の検証
- **言語対応**: 日本語命名の検証

### BaseScreenパターンテスト
- **共通機能**: エラーハンドリング・ローディング状態の検証
- **ライフサイクル**: 画面遷移時の状態管理検証
- **依存性注入**: Service Locator統合の検証

---

## 🚀 CI/CD自動化

### GitHub Actions設定

#### flutter_test.yml
- PR時自動テスト実行
- テストカバレッジレポート生成
- 全テスト成功必須
- Service Locator初期化検証

#### quality_gate.yml
- 60%カバレッジ閾値チェック
- 静的解析自動実行
- PR品質ゲート
- 新サービス統合チェック

### カバレッジ結果
- **StorageException**: 100%
- **MylogGalleryScreen**: 90.9%
- **MonologFlowScreen**: 60.3%
- **HybridStorageService**: 実装予定
- **CrisisSupportService**: 実装予定
- **EmotionPaletteService**: 実装予定

---

## 📊 テスト実装必須化指針

### 今後の開発ルール
1. **新機能実装時**: テスト作成100%必須
2. **既存機能修正時**: 影響範囲テスト更新必須
3. **PR承認条件**: 全テスト成功・カバレッジ閾値クリア
4. **Service Locator**: 新サービス追加時のモック実装必須

### 品質保証体制
- 継続的テスト実行による品質維持
- 技術負債発生防止体制確立
- 自動品質ゲートによる客観的品質評価
- Service Locatorによるテスト容易性確保

---

## 🚀 Firebase Test Lab 統合（2025年8月1日追加）

### 環境構築完了
Firebase Test Labを使用した自動UIテスト環境を構築しました。

#### 設定ファイル
```
firebase-test-lab/
├── configs/
│   ├── android-devices-free.json  # Android無料枠デバイス設定
│   ├── ios-devices-free.json      # iOS無料枠デバイス設定
│   └── test-settings.json          # 共通テスト設定
```

#### 実行スクリプト
- **Windows**: `run-android-test.ps1`
- **Mac/Linux**: `run-android-test.sh`, `run-ios-test.sh`

### テスト対象デバイス
**Android (5デバイス)**:
- Pixel 4 (API 30)
- Pixel 6 (API 31)
- Galaxy S20 (API 30)
- Moto G Power (API 29)
- OnePlus 8 (API 30)

**iOS (4デバイス)**:
- iPhone 13 (iOS 15)
- iPhone 12 Pro (iOS 14)
- iPhone SE 2nd Gen (iOS 14)
- iPad Pro 11-inch (iOS 15)

### Robo Test機能
- 自動UIクロール
- スクリーンショット自動撮影
- クラッシュ検出
- パフォーマンス測定
- アクセシビリティチェック

### CI/CD統合
```yaml
# GitHub Actions統合例
- name: Run Firebase Test Lab
  run: |
    cd firebase-test-lab
    ./scripts/run-android-test.sh
```

---

## 🔧 Ver 0.6.0 テスト改善項目

### 実装予定テスト
1. **HybridStorageService統合テスト**
   - オフライン/オンライン切替テスト
   - データ整合性テスト
   - パフォーマンステスト

2. **危機対応機能テスト**
   - キーワード検出精度テスト
   - 緊急連絡先表示テスト
   - Analytics統合テスト

3. **Service Locatorテスト**
   - 依存性注入テスト
   - サービス登録/取得テスト
   - ライフサイクル管理テスト

### テスト環境改善
- モック生成の自動化検討
- テストデータ管理の効率化
- E2Eテストシナリオの拡充
- パフォーマンステストスイートの構築

---

**この仕様書は『モノログ。』プロジェクトVer 0.6.0の自動テスト仕様を記録し、ハイブリッドストレージとService Locatorパターンに対応した品質保証体制を示しています。**