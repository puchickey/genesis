# データベース管理とセキュリティ詳細仕様書

## 1. データベース管理の詳細

### 1.1 SQLiteデータベース構成

#### データベースファイル
- **ファイル名**: `monolog.db`
- **保存場所**: アプリケーション専用ディレクトリ
- **アクセス権限**: アプリケーションのみ読み書き可能

#### バージョン管理
```dart
// 現在のバージョン: 3
// DatabaseHelper._initDB()
return await openDatabase(
  path,
  version: 3,
  onCreate: _createDB,
  onUpgrade: _upgradeDB,
);
```

### 1.2 データ保護メカニズム

#### 1.2.1 ローカルデータの暗号化

**メモフィールドの暗号化プロセス**
```dart
// HybridStorageService._encryptSensitiveData()
1. デバイス固有キーの取得（SecurityService経由）
2. UTF-8エンコード
3. XOR暗号化（キーとのXOR演算）
4. Base64エンコード
5. データベースに保存
```

**暗号化対象フィールド**
- `monologs.memo` - ユーザーが入力したメモ
- 将来的な拡張: `objects.custom_name`（検討中）

#### 1.2.2 暗号化キー管理

**デバイス暗号化キー生成**
```dart
// SecurityService._generateEncryptionKey()
- タイムスタンプ（ミリ秒）
- マイクロ秒単位のランダム値
- アプリケーション固有のソルト
- SHA256ハッシュ化
```

**キーの保存**
- FlutterSecureStorage使用
- Android: EncryptedSharedPreferences（AES-256）
- iOS: Keychain Services（ハードウェア暗号化）

### 1.3 データアクセス制御

#### 1.3.1 ユーザーIDベースの分離
```dart
// すべてのクエリでuser_idフィルタリング
WHERE user_id = ? AND is_deleted = 0
```

#### 1.3.2 論理削除の実装
- 物理削除ではなく`is_deleted`フラグで管理
- 削除データの復元可能性を維持
- 完全削除は別途バッチ処理で実行（未実装）

### 1.4 トランザクション管理

#### 1.4.1 整合性保証
```dart
// DatabaseHelper.deleteObject()
await db.transaction((txn) async {
  // 1. 関連するモノログを論理削除
  await txn.update('monologs', {
    'is_deleted': 1,
    'updated_at': DateTime.now().millisecondsSinceEpoch,
  }, where: 'object_id = ?', whereArgs: [objectId]);
  
  // 2. オブジェクトを物理削除
  await txn.delete('objects', where: 'object_id = ?', whereArgs: [objectId]);
});
```

### 1.5 バックアップとリカバリ

#### 1.5.1 自動バックアップ
- データベースマイグレーション時
- バックアップファイル命名: `monolog_backup_${timestamp}.db`
- 保存期間: 7日間（設定可能）

#### 1.5.2 マイグレーション分析
```dart
// MigrationAnalyzer
- 総レコード数の確認
- NULL値の検出
- データ整合性チェック
- マイグレーションレポート生成
```

## 2. セキュリティ実装の詳細

### 2.1 認証フロー

#### 2.1.1 初回起動時の匿名認証
```dart
// AuthService.signInAnonymously()
1. Firebase匿名認証の実行
2. ユーザーUID取得
3. SecureStorageに保存
4. タイムアウト: 30秒
5. リトライ: 最大2回（ネットワークエラー時）
```

#### 2.1.2 アカウントアップグレード
```dart
// AuthService.linkEmailPassword()
1. 現在の匿名ユーザー確認
2. メールアドレス検証
3. パスワード強度チェック
4. Firebase認証情報のリンク
5. ハッシュ化パスワードの保存
```

### 2.2 データ送信時のプライバシー保護

#### 2.2.1 匿名化プロセス
```dart
// 分析データ送信時の匿名化
{
  'event_type': 'monolog_created',
  'tier1_emotion': '喜び',        // OK: 感情カテゴリ
  'tier2_emotion': 'わくわく',     // OK: 詳細感情
  'has_memo': true,              // OK: 存在フラグのみ
  'timestamp': '2024-01-20T...',  // OK: タイムスタンプ
  // NG: user_id, memo内容, 画像データ
}
```

#### 2.2.2 オプトアウト機能
```dart
// DatabaseHelper
- isAnalyticsEnabled() // 現在の設定確認
- setAnalyticsEnabled(bool) // 設定変更
- デフォルト: false（オプトイン）
```

### 2.3 ネットワークセキュリティ

#### 2.3.1 通信の保護
- すべてのFirestore通信はHTTPS
- 証明書ピニング（将来実装予定）
- 中間者攻撃（MITM）対策

#### 2.3.2 タイムアウト設定
```dart
// 各操作のタイムアウト値
- 認証操作: 30秒
- データ取得: 15秒
- データ送信: 10秒
- ファイル操作: 30秒
```

### 2.4 エラーハンドリングとログ

#### 2.4.1 エラー情報の制御
```dart
// ユーザー向けエラーメッセージ
- 具体的な技術詳細を含めない
- 一般的なエラーメッセージを表示
- 詳細はログに記録（デバッグ時のみ）
```

#### 2.4.2 ログレベル管理
```dart
// 本番環境でのログ制御
- DEBUG: 無効化
- INFO: 重要な操作のみ
- WARNING: 記録
- ERROR: 記録とクラッシュレポート
```

## 3. 課金機能実装時のセキュリティ考慮事項

### 3.1 決済情報の取り扱い

#### 3.1.1 決済情報の非保存原則
```dart
// 推奨実装
class PaymentService {
  // NG: クレジットカード情報の保存
  // void saveCreditCard(String number, String cvv) 
  
  // OK: 決済トークンの保存
  Future<void> savePaymentToken(String token) async {
    await _securityService.saveSensitiveData('payment_token', token);
  }
}
```

#### 3.1.2 レシート検証フロー
```dart
// 推奨実装フロー
1. アプリ内購入の実行
2. レシートデータの取得
3. サーバーへの送信（HTTPS必須）
4. サーバー側でApple/Googleへの検証
5. 検証結果の受信
6. ローカルでのプレミアムフラグ更新
```

### 3.2 プレミアム機能のアクセス制御

#### 3.2.1 多層防御の実装
```dart
// レイヤー1: UIレベル
if (await isPremiumEnabled()) {
  // プレミアム機能のUI表示
}

// レイヤー2: ビジネスロジック
Future<void> executePremiumFeature() async {
  if (!await isPremiumEnabled()) {
    throw UnauthorizedException();
  }
  // 機能実行
}

// レイヤー3: データアクセス
Future<void> savePremiumData() async {
  // サーバー側での最終検証
  final isValid = await verifyPremiumStatus();
  if (!isValid) throw UnauthorizedException();
}
```

### 3.3 データベーススキーマの拡張案

#### 3.3.1 サブスクリプション管理テーブル
```sql
CREATE TABLE subscriptions (
  subscription_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  product_id TEXT NOT NULL,
  platform TEXT NOT NULL, -- 'ios' or 'android'
  status TEXT NOT NULL, -- 'active', 'expired', 'cancelled'
  expires_at INTEGER,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (user_id)
);

CREATE TABLE purchase_history (
  purchase_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  product_id TEXT NOT NULL,
  transaction_id TEXT NOT NULL,
  amount INTEGER NOT NULL,
  currency TEXT NOT NULL,
  purchased_at INTEGER NOT NULL,
  receipt_data TEXT, -- 暗号化して保存
  FOREIGN KEY (user_id) REFERENCES users (user_id)
);
```

## 4. パフォーマンスとスケーラビリティ

### 4.1 インデックス戦略
```sql
-- 現在のインデックス
CREATE INDEX idx_monologs_user_id ON monologs(user_id);
CREATE INDEX idx_monologs_object_id ON monologs(object_id);
CREATE INDEX idx_monologs_created_at ON monologs(created_at);
CREATE INDEX idx_monologs_is_analytics_sent ON monologs(is_analytics_sent);

-- 課金機能追加時の推奨インデックス
CREATE INDEX idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);
CREATE INDEX idx_subscriptions_expires_at ON subscriptions(expires_at);
```

### 4.2 クエリ最適化
```dart
// ページネーション実装
Future<List<MonologModel>> getMonologsPaginated({
  required String userId,
  required int page,
  int pageSize = 20,
}) async {
  final offset = (page - 1) * pageSize;
  return await getMonologs(
    userId: userId,
    limit: pageSize,
    offset: offset,
  );
}
```

## 5. 監査とコンプライアンス

### 5.1 アクセスログ
```dart
// 重要操作のログ記録
class AuditLogger {
  static Future<void> logDataAccess({
    required String userId,
    required String action,
    required String resourceType,
    required String resourceId,
  }) async {
    await _databaseHelper.addAnalyticsEvent(
      eventType: 'audit_log',
      eventData: {
        'action': action,
        'resource_type': resourceType,
        'timestamp': DateTime.now().toIso8601String(),
        // user_idとresource_idは含めない（プライバシー）
      },
    );
  }
}
```

### 5.2 データ保持ポリシー
- アクティブデータ: 無期限
- 削除済みデータ: 30日後に物理削除
- バックアップ: 7日間
- 分析ログ: 90日間

## 6. 災害復旧計画

### 6.1 ローカルデータの復旧
1. 自動バックアップからの復元
2. Firestoreからの部分復元（プレミアム機能）
3. エクスポート/インポート機能（計画中）

### 6.2 認証情報の復旧
1. Firebase Auth の復旧メカニズム
2. SecureStorage のバックアップ（iCloud/Google Drive）
3. アカウントリカバリーフロー

## まとめ

本アプリケーションは、ローカルファーストの設計により高いプライバシー保護を実現しています。課金機能の実装にあたっては、既存のセキュリティ基盤を活用しつつ、決済情報の適切な管理と多層防御によるアクセス制御が重要となります。

特に注意すべき点：
1. 決済情報は一切保存しない
2. レシート検証は必ずサーバー側で実行
3. プレミアム機能へのアクセスは多層防御で保護
4. すべての機密データは暗号化して保存
5. 監査ログによるコンプライアンス対応