# モノログアプリ 主要コンポーネント詳細

## 概要
このドキュメントは、モノログアプリの主要なコンポーネントとサービスの実装詳細を説明します。

## 1. BLoCコンポーネント詳細

### MonologBloc
**責務**: モノログのCRUD操作と状態管理

**イベント** (monolog_event.dart):
- `LoadMonologs`: 全モノログの読み込み
- `CreateMonolog`: 新規モノログ作成
- `UpdateMonolog`: 既存モノログ更新
- `DeleteMonolog`: モノログ削除
- `FilterMonologs`: フィルタリング

**状態** (monolog_state.dart):
- `MonologInitial`: 初期状態
- `MonologLoading`: 読み込み中
- `MonologLoaded`: データ読み込み完了
- `MonologCreated`: 作成完了
- `MonologUpdated`: 更新完了
- `MonologDeleted`: 削除完了
- `MonologError`: エラー状態

**主要メソッド**:
```dart
// 作成処理の流れ
on<CreateMonolog>((event, emit) async {
  emit(MonologCreating());
  try {
    // 1. ローカル保存
    final monolog = await _storageService.createMonolog(event.data);
    // 2. 状態更新
    emit(MonologCreated(monolog));
    // 3. バックグラウンド同期
    _syncService.queueSync(monolog);
  } catch (e) {
    emit(MonologError(e.toString()));
  }
});
```

### MonologRecordBloc
**責務**: モノログ記録プロセスの状態管理

**フロー管理**:
1. 画像パス設定
2. 切り抜き範囲設定
3. 第1感情選択
4. 第2感情選択
5. メモ入力
6. 保存処理

**状態遷移**:
- `RecordingInitial` → `ImageSelected` → `RangeSelected` → `PrimaryEmotionSelected` → `SecondaryEmotionSelected` → `RecordingComplete`

## 2. サービスコンポーネント詳細

### HybridStorageService
**責務**: ローカルとクラウドのハイブリッドストレージ管理

**主要メソッド**:
- `saveMonolog()`: ローカル保存 → 同期キュー追加
- `loadMonologs()`: ローカル読み込み → 差分同期
- `syncPendingData()`: 保留中データの同期
- `resolveConflicts()`: 競合解決

**同期戦略**:
1. **オフラインファースト**: 常にローカル優先
2. **差分同期**: タイムスタンプベース
3. **競合解決**: 最終更新時刻優先
4. **バッチ処理**: 複数変更をまとめて同期

### OperationGuideService
**責務**: 各画面の操作ガイド管理

**ガイドデータ構造**:
```dart
Map<String, GuideData> guides = {
  'home': GuideData(
    title: 'ホーム画面',
    description: '主要機能へのアクセスポイント',
    steps: [
      '「モノログを始める」をタップして記録開始',
      '「マイログ」で過去の記録を確認',
      '「設定」でアプリをカスタマイズ'
    ]
  ),
  // 他の画面のガイド...
};
```

**表示制御**:
- 初回表示の記録
- スキップ設定の管理
- コンテキストに応じた表示

### EmotionService
**責務**: 感情データの管理とカスタム感情

**基本感情構造**:
```dart
final emotions = {
  'joy': {
    'name': '喜び',
    'color': Color(0xFFFFD93D),
    'subEmotions': ['嬉しい', '楽しい', 'わくわく', '満足', '幸せ', '誇らしい']
  },
  'calm': {
    'name': '落ち着き',
    'color': Color(0xFF6BB6FF),
    'subEmotions': ['安心', 'リラックス', '穏やか', '平和', 'のんびり', 'ゆったり']
  },
  // 他の感情...
};
```

**カスタム感情管理**:
- 最大10個まで作成可能
- 色と名前をカスタマイズ
- ローカル保存

### CameraService
**責務**: カメラ制御と画像処理

**機能**:
- カメラ初期化
- プレビュー表示
- 撮影処理
- フラッシュ制御
- カメラ切り替え（前面/背面）

**エラーハンドリング**:
- 権限エラー
- デバイス非対応
- カメラ使用中エラー

## 3. ウィジェットコンポーネント詳細

### CircularEmotionSelector
**用途**: 第2感情選択時の円形配置UI

**実装詳細**:
- CustomPainterで円形配置計算
- AnimationControllerで出現アニメーション
- 中央に選択した第1感情を配置
- 周囲に6つの第2感情を均等配置

### OperationGuideOverlay
**用途**: 操作ガイドのオーバーレイ表示

**構成要素**:
- 半透明背景
- ガイドカード（タイトル、説明、ステップ）
- 閉じるボタン
- 「今後表示しない」チェックボックス

### StorySelectionBottomSheet
**用途**: フォルダ選択のボトムシート

**機能**:
- 既存フォルダ一覧
- 新規フォルダ作成
- 検索機能（将来実装）
- 選択後の即時反映

## 4. データモデル詳細

### MonologModel
```dart
class MonologModel {
  final String logId;          // UUID
  final String imagePath;      // ローカルファイルパス
  final Rect cropRect;         // 切り抜き範囲
  final String primaryEmotion; // 第1感情
  final String secondaryEmotion; // 第2感情
  final String? memo;          // メモ（任意）
  final String? title;         // タイトル（任意）
  final String? storyId;       // フォルダID（任意）
  final DateTime createdAt;    // 作成日時
  final DateTime updatedAt;    // 更新日時
  final bool isSynced;         // 同期状態
}
```

### CustomEmotionModel
```dart
class CustomEmotionModel {
  final String id;
  final String name;      // 感情名
  final Color color;      // 表示色
  final int order;        // 表示順序
  final DateTime createdAt;
}
```

## 5. 画面実装詳細

### MonologRecordingScreen
**実装のポイント**:
- ステップ管理（_currentStep変数）
- アニメーション制御（複数のAnimationController）
- 状態に応じたUI切り替え
- プログレスインジケーター表示

**ウィジェット構成**:
```
Column
├── AppBar（プログレス表示付き）
├── 画像表示エリア
├── 質問テキスト
├── 感情選択エリア（動的切り替え）
│   ├── 第1感情グリッド or
│   └── 第2感情円形配置
└── アクションエリア（メモ入力・保存ボタン）
```

### CompletionScreen
**アニメーション構成**:
1. 背景グラデーション（0-500ms）
2. 光の粒子出現（200-1000ms）
3. カード出現（800-1500ms）
4. テキスト表示（1500ms-）

**実装技術**:
- AnimatedBuilder
- Transform（3D効果）
- CustomPainter（粒子描画）
- Hero（画面遷移アニメーション）

## 6. ナビゲーション実装

### AppRoutes定義
```dart
class AppRoutes {
  static const String home = '/';
  static const String onboarding = '/onboarding';
  static const String cameraPreview = '/camera-preview';
  static const String rangeSelection = '/range-selection';
  static const String emotionSelection = '/emotion-selection';
  static const String completion = '/completion';
  static const String mylog = '/mylog';
  static const String mylogDetail = '/mylog-detail';
  static const String settings = '/settings';
  static const String emotionManagement = '/emotion-management';
  static const String storyDetail = '/story-detail';
}
```

### ルート設定
- MaterialApp.onGenerateRouteで動的ルート生成
- 引数の受け渡し（arguments）
- トランジションアニメーション（FadePageRoute）

## 7. エラーハンドリング実装

### ErrorHandler
**エラー分類**:
1. **回復可能エラー**: リトライ可能
2. **部分的エラー**: 機能制限で継続
3. **致命的エラー**: アプリ再起動必要

**エラー通知方法**:
```dart
// SnackBar（軽微なエラー）
ScaffoldMessenger.of(context).showSnackBar(
  SnackBar(content: Text('一時的なエラーが発生しました'))
);

// Dialog（重要なエラー）
showDialog(
  context: context,
  builder: (_) => AlertDialog(
    title: Text('エラー'),
    content: Text('データの保存に失敗しました'),
    actions: [/*...*/]
  )
);
```

## 8. パフォーマンス最適化実装

### 画像最適化
- 保存時: 最大1920x1920に圧縮
- 表示時: サムネイル生成（リスト用）
- メモリ管理: LRUキャッシュ

### リスト最適化
- ListView.builderで遅延生成
- AutomaticKeepAliveClientMixinでスクロール位置保持
- ページネーション（将来実装）

## 9. テスト実装例

### BLoCテスト
```dart
test('モノログ作成テスト', () async {
  final bloc = MonologBloc(mockService);
  
  bloc.add(CreateMonolog(/*...*/));
  
  await expectLater(
    bloc.stream,
    emitsInOrder([
      MonologCreating(),
      MonologCreated(/*...*/),
    ]),
  );
});
```

### ウィジェットテスト
```dart
testWidgets('感情選択UIテスト', (tester) async {
  await tester.pumpWidget(
    MaterialApp(home: EmotionSelector())
  );
  
  // 感情ボタンをタップ
  await tester.tap(find.text('喜び'));
  await tester.pump();
  
  // 第2感情が表示されることを確認
  expect(find.text('嬉しい'), findsOneWidget);
});
```

このドキュメントにより、各コンポーネントの実装詳細と相互作用を理解することができます。