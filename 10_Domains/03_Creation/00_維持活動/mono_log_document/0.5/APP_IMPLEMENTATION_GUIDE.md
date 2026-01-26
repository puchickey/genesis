# 『モノログ。』アプリ実装ガイド（完全版）

**更新日**: 2025年7月21日  
**バージョン**: v3.2 感情日記風UI統合・チュートリアルシステム完成版  
**対象**: 開発者・他AI向けアプリ詳細仕様

---

## 📱 アプリケーション概要

### アプリ名
**『モノログ。』(mono_log_app)**

### コンセプト
身の回りの「モノ」を通じて内省を促進するマイクロジャーナリングアプリ。撮影したモノに対する感情や記憶を段階的に掘り下げることで、ユーザーの自己理解を深める。

### 主要機能
1. **カメラ撮影**: モノの撮影と基本的な画像処理
2. **マイクロジャーナリング**: 4段階の内省フロー
3. **感情記録**: 2段階感情選択システム
4. **データ管理**: 構造化ログによるFirestore保存
5. **オブジェクト管理**: モノの戸籍システム

---

## 🏗️ アーキテクチャ概要

### フレームワーク
- **Flutter**: クロスプラットフォーム開発
- **Dart**: プログラミング言語
- **Firebase**: バックエンドサービス（Firestore, Auth, Analytics）

### 設計パターン
- **BLoC Pattern**: 状態管理（カメラ機能）
- **Repository Pattern**: データアクセス層
- **Service Layer**: ビジネスロジック層

### ディレクトリ構造
```
lib/
├── main.dart                    # アプリエントリーポイント
├── blocs/                       # BLoC状態管理
├── models/                      # データモデル
├── screens/                     # UI画面
├── services/                    # ビジネスロジック
├── widgets/                     # 再利用可能コンポーネント
└── config/                      # 設定・定数
```

---

## 📱 画面構成・UI詳細

### 1. メイン画面 (main.dart)

#### 表示内容
```dart
// 初回起動チェック
final prefs = await SharedPreferences.getInstance();
final hasCompletedOnboarding = prefs.getBool('onboarding_completed') ?? false;

MaterialApp(
  title: 'モノログ。',
  theme: カスタムテーマ,
  home: hasCompletedOnboarding ? SimpleHomeScreen() : OnboardingScreen(),
)
```

#### 機能
- アプリの初期化とルーティング設定
- Firebase初期化
- テーマ設定（M PLUS Rounded 1cフォント）
- 初回起動判定（SharedPreferences使用）
- 適切な画面への振り分け
  - 初回起動: OnboardingScreen
  - 2回目以降: SimpleHomeScreen

### 1.1. オンボーディング画面 (OnboardingScreen)

#### 機能
初回起動時のアプリ説明と診断への誘導を行う5ページ構成の画面。

#### ページ構成
1. **ウェルカムページ**
   - タイトル: 「ようこそ、モノログ。へ」
   - モノとの新しい関係性の紹介
   - 浮遊するモノのアニメーション表示

2. **スポットライト戦略説明**
   - AIの役割説明（黒子として控えめにサポート）
   - スポットライト効果のビジュアル表現

3. **診断案内**
   - 2分で分かるモノとの関係性診断の紹介
   - 6つの診断タイプのアイコン表示

4. **法的事項**
   - プライバシーポリシーとデータ保護
   - セキュリティアニメーション表示

5. **機能紹介**
   - 感情記録の簡便さをアピール
   - 医療機器ではない旨の警告表示

#### UI実装
```dart
// アニメーション設定
AnimationController _logoAnimation;    // elasticOut、1.5秒
AnimationController _floatAnimation;   // 3秒周期の浮遊効果
AnimationController _fadeAnimation;    // フェードイン効果

// ナビゲーション要素
PageIndicator: 上部中央（現在のページ表示）
SkipButton: 右上（診断画面へスキップ）
NextButton: 下部（次へ/診断を始める）

// 完了処理
await prefs.setBool('onboarding_completed', true);
Navigator.pushReplacement(
  context,
  MaterialPageRoute(builder: (_) => DiagnosisScreen()),
);
```

### 1.2. 診断画面 (DiagnosisScreen)

#### 機能
ユーザーのモノとの関係性を6つのタイプに分類する診断機能。

#### 診断タイプ
```dart
enum PersonalityType {
  minimalist,      // ミニマリスト - 最小限のモノで生きる
  collector,       // コレクター - モノを集めることが好き
  storyteller,     // ストーリーテラー - モノの物語を大切にする
  practical,       // 実用主義者 - 機能性を重視
  emotional,       // 感情派 - モノとの感情的つながりを重視
  balanced        // バランス型 - 状況に応じて柔軟に対応
}
```

#### 質問システム（5問詳細）

1. **大掃除で昔の恋人からもらったマグカップが出てきました。どう思う？**
   - まだ使えるし、モノに罪はない → 実用主義型 +2
   - あの頃の思い出が蘇ってくる → ストーリーテラー型 +2
   - 複雑だけど、大切にしてきた時間もある → 感情派 +2
   - 美しいデザインだから観賞用に残そう → コレクター型 +2
   - もう必要ない、手放そう → ミニマリスト型 +2

2. **友人が趣味の違う雑貨をくれようとしています。どうする？**
   - 気持ちだけ受け取り、丁重にお断り → ミニマリスト型 +2
   - 友情の証として、大切に受け取る → 感情派 +2
   - デザインが気に入れば喜んで受け取る → コレクター型 +2
   - 何かに使えるかもしれない、とりあえず受け取る → 実用主義型 +2
   - 申し訳ないけど、断りづらい → バランス型 +1

3. **あなたのクローゼットは、どんな状態に近い？**
   - 厳選したお気に入りだけが整然と → ミニマリスト型 +2
   - 好きなモノがたくさん、見ているだけで幸せ → コレクター型 +2
   - それぞれに思い出があって、なかなか手放せない → ストーリーテラー型 +2
   - よく使うモノから順番に整理されている → 実用主義型 +2
   - なんとなく愛着があって、全部大切 → 感情派 +2

4. **新しい趣味の道具を一式揃えたけど、3ヶ月で飽きちゃった。どうする？**
   - すぐに売るか誰かに譲る → ミニマリスト型 +2
   - また興味が湧くかもしれないから保管 → 実用主義型 +2
   - 頑張った時間の証として取っておく → ストーリーテラー型 +2
   - デザインが素敵なら飾り物として活用 → コレクター型 +2
   - せっかく買ったのに、手放すのは心が痛む → 感情派 +2

5. **「あなたの人生を象徴するモノを一点選んで」と言われたら？**
   - シンプルで飽きのこない、長年愛用しているモノ → ミニマリスト型 +2
   - 美しくて、見ているだけで心が満たされるモノ → コレクター型 +2
   - 大切な人との思い出が詰まったモノ → ストーリーテラー型 +2
   - 日々の生活で一番役立っているモノ → 実用主義型 +2
   - 理由はうまく言えないけど、なんとなく大切なモノ → 感情派 +2

#### スコアリング判定
- 各選択肢のスコアを加算
- 最高スコアと2番目のスコアの差が2点未満の場合 → バランス型
- それ以外 → 最高スコアのタイプを診断結果とする

#### 診断結果画面 (DiagnosisResultScreen)
```dart
// 結果表示内容
- タイプ名とアイコン
- 詳細な性格説明
- 3つの主要な特徴
- アプリ活用のアドバイス
- ホーム画面への遷移ボタン

// 完了処理
Navigator.pushAndRemoveUntil(
  context,
  MaterialPageRoute(builder: (_) => SimpleHomeScreen()),
  (route) => false, // 全画面履歴をクリア
);
```

### 1.3. シンプルホーム画面 (SimpleHomeScreen)

#### 表示内容
- **中央**: 大型円形カメラボタン（120x120）
- **アプリタイトル**: 「モノログ。」+ サブタイトル「内省支援ツール」
- **背景**: Paper White (0xFFF8F7F2)
- **操作ガイド**: オンボーディング後の連続ガイドモード対応

#### メインボタン実装
```dart
GestureDetector(
  key: _cameraButtonKey, // ガイドモード用
  onTap: _startCamera,
  child: Container(
    width: 120,
    height: 120,
    decoration: BoxDecoration(
      color: const Color(0xFF6A9C89), // Calm Green
      shape: BoxShape.circle,
      boxShadow: [
        BoxShadow(
          color: Colors.black.withValues(alpha: 0.2),
          blurRadius: 10,
          offset: const Offset(0, 4),
        ),
      ],
    ),
    child: const Icon(
      Icons.camera_alt,
      size: 50,
      color: Colors.white,
    ),
  ),
```

#### 操作ガイド機能
SimpleHomeScreenには、オンボーディング完了後の連続ガイドモード機能が統合されています：

```dart
// ガイドモードチェック
Future<void> _checkGuideMode() async {
  final shouldShowContinuous = await GuideService.shouldShowContinuousGuide();
  if (shouldShowContinuous) {
    setState(() {
      _showGuideMode = true;
      _isContinuousMode = true;
      _guideSteps = GuideService.getSimpleHomeScreenGuideSteps(
        cameraButtonKey: _cameraButtonKey,
      );
    });
  }
```

#### アニメーション
- **パルス効果**: 1.0 ↔ 1.05のスケール変化
- **継続時間**: 2秒周期で無限リピート
- **タップ時**: カメラ画面に遷移

### 4. カメラ画面 (CameraCaptureScreen)

#### 表示内容
- **上部**: カメラプレビュー（クリーンなUI）
- **下部**: 撮影ボタン
- **削除済み要素**: 
  - ❌ 診断結果表示（2025年7月19日削除）
  - ❌ デバッグ情報表示（本番では非表示）

#### 遷移フロー（2025年7月19日修正）
```
CameraCaptureScreen（撮影）
        ↓
ObjectSelectionScreen（手動範囲選択）
        ↓
MicroJournalingScreen（内省フロー）
```

#### 主要なテキスト表示
```dart
// デバッグ情報例
'📱 初期化開始...'
'🔧 AI推論エンジンを初期化中...'
'✅ カメラ機能初期化完了'
'📷 カメラをチェック中...'
'🎥 カメラを初期化中...'
'✅ カメラプレビュー準備完了'
```

#### カメラ状態管理 (CameraBloc)
```dart
enum CameraStatus {
  initial,     // 初期状態
  loading,     // 初期化中
  ready,       // 準備完了
  capturing,   // 撮影中
  processing,  // 処理中
  paused,      // 一時停止
  failure,     // エラー
}
```

#### 撮影処理フロー
1. `CameraPhotoCaptureStarted` イベント発火
2. `CameraStatus.capturing` に状態変更
3. 画像ファイル保存
4. マイクロジャーナリング画面に遷移

### 4.1. オブジェクト選択画面 (ObjectSelectionScreen) - 2025年7月19日重要実装

#### 概要
手動で範囲を選択し、選択した範囲のみをクロップして内省画面に正確に反映する機能。

#### 画像クロップシステム実装
```dart
/// 選択範囲の画像をクロップして新しいファイルを作成
Future<String> _cropImageToSelection(Rect cropRegion) async {
  // 元画像読み込み・デコード
  final originalImage = img.decodeImage(imageBytes);
  
  // 境界チェック付きクロップ範囲計算
  final cropX = cropRegion.left.round().clamp(0, originalImage.width);
  final cropY = cropRegion.top.round().clamp(0, originalImage.height);
  
  // 高品質クロップ処理
  final croppedImage = img.copyCrop(originalImage, ...);
  
  // 一時ファイル保存（JPEG 90%品質）
  final jpegBytes = img.encodeJpg(croppedImage, quality: 90);
  return croppedFile.path;
}
```

#### UI座標→画像座標変換
```dart
Future<Rect> _convertUICoordinatesToImageCoordinates(Rect uiRect) async {
  // スケール比率計算
  final scaleX = originalWidth / displayWidth;
  final scaleY = originalHeight / displayHeight;
  
  // UI座標を元画像座標に変換
  return Rect.fromLTWH(
    uiRect.left * scaleX,
    uiRect.top * scaleY,
    uiRect.width * scaleX,
    uiRect.height * scaleY,
  );
}
```

### 5. マイクロジャーナリング画面 (MicroJournalingScreen)

#### 画面構造（2025年7月19日レスポンシブ対応）
```dart
Scaffold(
  body: SafeArea(
    child: SingleChildScrollView(
      child: ConstrainedBox(
        constraints: BoxConstraints(minHeight: screenHeight),
        child: IntrinsicHeight(
          child: Column([
            // 画像表示エリア（20%に縮小）
            Container(
              height: MediaQuery.of(context).size.height * 0.20,
              child: クロップ済み画像表示,
            ),
            
            // コンテンツエリア（自動調整）
            Expanded(child: _buildCurrentStep()),
          ]),
        ),
      ),
    ),
  ),
)
```

#### レスポンシブ対応（2025年7月19日）
- **SafeArea + SingleChildScrollView**: bottom overflow完全解決
- **画像エリア縮小**: 30% → 20%
- **パディング調整**: 24px → 20px、16px → 12px

#### ステップ管理
```dart
String _currentStep = 'trigger'; // フロー状態管理
```

**フロー段階**:
1. `trigger` - 感情ベクター選択
2. `step2` - 現在の関係性質問
3. `step3` - 過去の記憶質問
4. `step4` - 自己との繋がり質問
5. `feeling` - 感情選択
6. `name` - オブジェクト名入力（新規時のみ）
7. `complete` - 完了

#### 4段階フローの質問強調表示（2025年7月19日実装）

**全質問共通デザイン**:
```dart
Container(
  decoration: BoxDecoration(
    gradient: LinearGradient(
      colors: [Color(0xFF6A9C89), Color(0xFF87A9C4)], // アプリ色調統一
    ),
    borderRadius: BorderRadius.circular(16),
    boxShadow: [BoxShadow(...)],
  ),
  child: Row([
    Container(width: 4, color: Colors.white), // 白いアクセントライン
    Expanded(
      child: Text(
        question,
        style: TextStyle(
          color: Colors.white,
          fontSize: 18,
          fontWeight: FontWeight.w600,
          height: 1.5, // デバイス対応の自動改行
        ),
      ),
    ),
  ]),
)
```

#### タイトル入力フィールド（2025年7月19日追加）

**新規実装**: 画像表示後にタイトル入力フィールドを追加
```dart
TextField(
  controller: _titleController,
  decoration: InputDecoration(
    hintText: 'このモノは、あなたにとってどんな存在ですか？',
    hintStyle: TextStyle(
      color: Colors.grey[500],
      fontFamily: 'M PLUS Rounded 1c',
      fontSize: 14,
    ),
    filled: true,
    fillColor: Colors.white.withValues(alpha: 0.9),
    border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
  ),
)
```

#### 入力順序の改善（2025年7月19日変更）

**変更内容**: ユーザビリティ向上のため入力順序を調整
```
変更前: テキスト入力 → タグ選択
変更後: タグ選択 → テキスト入力（より直感的）
```

#### Step 1: 感情ベクター選択

**表示テキスト**（強調表示適用）:
```
「このモノを見て、まずどう感じる？」
```

**選択肢ボタン**:
```dart
'😊 あたたかい・ポジティブな気持ち'  // positive
'🤔 複雑・ネガティブな気持ち'        // complex  
'❓ 今は、よくわからない'           // unknown
```

**ボタンスタイル**:
- 背景色: `Color(0xFF6A9C89)` (ポジティブ)
- 背景色: `Color(0xFF87A9C4)` (複雑)
- 背景色: `Colors.grey[600]` (わからない)
- フォント: M PLUS Rounded 1c

#### Step 2: 現在の関係性質問

**ポジティブベクター選択時**:
```
質問: 「このモノがくれた、一番の宝物は？」
選択肢: [楽しい時間, 自信, 安心感, 新しい発見, 人との縁]
```

**複雑・ネガティブベクター選択時**:
```
質問: 「このモノを手放すとしたら、何が気になる？」
選択肢: [値段, 思い出, 人目, 後悔, 面倒]
```

**わからないベクター選択時**:
```
質問: 「このモノが、最後に活躍したのはいつ？」
選択肢: [1週間以内, 1ヶ月以内, 1年以内, 1年以上前, 覚えてない]
```

#### Step 3: 過去の記憶質問

**ポジティブベクター選択時**:
```
質問: 「その気持ちは、いつの記憶と繋がっていますか？」
選択肢: [手に入れた瞬間, 誰かと過ごした時間, 最近の出来事, 子供の頃]
```

**複雑・ネガティブベクター選択時**:
```
質問: 「その気持ちは、いつの記憶と繋がっていますか？」
選択肢: [手に入れた瞬間, 使わなくなった頃, 過去の失敗, 未来への不安]
```

**わからないベクター選択時**:
```
質問: 「このモノに関する出来事を、何か一つ思い出せますか？」
選択肢: [手に入れた時のこと, 使っていた時のこと, 誰かとのこと, 特にない]
```

#### Step 4: 自己との繋がり質問

**ポジティブベクター選択時**:
```
質問: 「このモノは、あなたのどんな一面を映していますか？」
選択肢: [理想の自分, 努力の証, 好きなもの, 大切な価値観]
```

**複雑・ネガティブベクター選択時**:
```
質問: 「このモノは、あなたのどんな一面を映していますか？」
選択肢: [過去の自分, 手放せない弱さ, 忘れたい記憶, なりたくない自分]
```

**わからないベクター選択時**:
```
質問: 「このモノを持っていることは、今のあなたにとってどんな意味がありますか？」
選択肢: [お守りのようなもの, ただそこにあるだけ, 過去の自分の一部, よくわからない]
```

#### 入力UI詳細

**ハイブリッド入力システム**:
```dart
// テキスト入力フィールド
TextField(
  maxLines: 4,
  maxLength: 500,
  hintText: '自由に書いてみてください…',
  decoration: InputDecoration(
    filled: true,
    fillColor: Colors.white.withValues(alpha: 0.8),
    border: OutlineInputBorder(borderRadius: 12),
  ),
)

// 選択肢チップ
Wrap(
  children: chips.map((chip) => _buildChipForStep(chip, step)),
)
```

**チップスタイル**:
- 未選択: 白背景、グレー枠線
- 選択済み: `Color(0xFF6A9C89)` 背景、同色枠線
- フォントサイズ: 14px
- パディング: 12px水平、8px垂直

**次へボタン**:
```dart
ElevatedButton(
  onPressed: hasInput ? onPressed : null,
  style: ElevatedButton.styleFrom(
    backgroundColor: hasInput ? Color(0xFF6A9C89) : Colors.grey[400],
    padding: EdgeInsets.symmetric(vertical: 16),
  ),
  child: Text('次へ'),
)
```

**入力状態管理**:
```dart
// 各ステップの状態管理
Map<String, String> _stepResponses = {};           // テキスト回答
Map<String, List<String>> _stepTappedChips = {};   // 選択チップ
Map<String, TextEditingController> _stepControllers = {}; // コントローラー
```

#### Step 5: 感情選択（2段階UI）

**表示方法（2025年7月19日変更）**: 底部シート（ボトムシート）で感情選択
```dart
// 「その他...」ボタンタップ時
showModalBottomSheet(
  context: context,
  isScrollControlled: true,
  backgroundColor: Colors.transparent,
  builder: (context) => EmotionSelectionBottomSheet(
    feelingsByVector: _feelingsByVector,
    selectedVector: _selectedVector!,
    onEmotionSelected: (emotionId) {
      setState(() => _selectedFeeling = emotionId);
      Navigator.pop(context);
    },
  ),
);
```

**1st Tier表示テキスト**:
```
「今の気持ちは？」
```

**ポジティブベクター時の1st Tier候補**:
```
感謝 🙏, 愛着 🥰, 懐かしさ 😌, 喜び ✨, 誇り 🏆
```

**複雑・ネガティブベクター時の1st Tier候補**:
```
考えさせられる 🤔, ほろ苦さ 😢, 罪悪感 😥, モヤモヤ 🌫️, 後悔 😔
```

**わからないベクター時の1st Tier候補**:
```
愛着 🥰, ほろ苦さ 😢, なるほど 💡, スッキリ 🍃
```

**2nd Tier（全感情パレット）**:
```dart
// ポジティブな気持ち（9種）
感謝🙏, 愛着🥰, 懐かしさ😌, 喜び✨, 誇り🏆, 
スッキリ🍃, ワクワク🎉, ほっ😌, 面白い😂

// 複雑・ネガティブな気持ち（8種）
考えさせられる🤔, ほろ苦さ😢, 罪悪感😥, モヤモヤ🌫️, 
後悔😔, 悲しい😭, 寂しい💔, 怒り😠

// ニュートラルな気持ち（4種）  
なるほど💡, まあまあ🙂, 普通😐, 無心😑
```

**感情ボタンスタイル**:
```dart
Container(
  padding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
  decoration: BoxDecoration(
    color: isSelected ? Color(0xFF6A9C89).withValues(alpha: 0.2) : Colors.white,
    border: Border.all(
      color: isSelected ? Color(0xFF6A9C89) : Colors.grey[300],
      width: 2,
    ),
    borderRadius: BorderRadius.circular(25),
  ),
  child: Row(
    children: [
      Text(emoji, style: TextStyle(fontSize: 20)),
      SizedBox(width: 8),
      Text(name, style: TextStyle(fontSize: 16)),
    ],
  ),
)
```

#### Step 6: オブジェクト名入力（新規作成時のみ）

**表示テキスト**:
```
「このモノの名前は何ですか？」
```

**入力フィールド**:
```dart
TextField(
  decoration: InputDecoration(
    hintText: '例：お気に入りのマグカップ',
    filled: true,
    fillColor: Colors.white.withValues(alpha: 0.8),
  ),
)
```

**完了ボタン**:
```
「記録する」
```

### 4. カスタムチップ追加機能

#### マイタグ追加ダイアログ
```dart
AlertDialog(
  title: Text('マイタグを追加'),
  content: Column(
    children: [
      TextField(
        maxLength: 20,
        hintText: '例: よく使う、お気に入り',
      ),
      Text('${usage}/10個使用中'), // 制限表示
    ],
  ),
  actions: [
    TextButton('キャンセル'),
    TextButton('追加'),
  ],
)
```

#### 制限管理
- **上限**: 各ステップごとに10個
- **カテゴリキー**: `spark_step2`, `spark_step3`, `spark_step4`
- **状態管理**: `CustomOptionsService`

---

## 🗄️ データモデル詳細

### 1. ObjectModel（モノの戸籍）

```dart
class ObjectModel {
  final String objectId;       // UUID
  final String userId;         // Firebase Auth UID
  final String physicalName;   // 例: "腕時計"
  final String mainImageUrl;   // メイン画像URL
  final DateTime createdAt;    // 作成日時
  final DateTime? updatedAt;   // 更新日時
  
  // 追加メタデータ
  final String? description;           // 説明
  final List<String>? tags;           // タグ
  final Map<String, dynamic>? metadata; // その他データ
}
```

**Firestore保存場所**: `objects/{objectId}`

### 2. LogModel（構造化ログ）- 2025年7月19日更新

```dart
class LogModel {
  final String logId;                              // UUID
  final String userId;                             // Firebase Auth UID  
  final String objectId;                           // ObjectModelへの参照
  final String emotionalTitle;                     // 自動生成タイトル
  final String imageUrl;                           // 撮影画像URL（クロップ済み）
  final DateTime createdAt;                        // 作成日時
  
  // 2025年7月19日追加: タイトルフィールド
  final String? title;                             // ユーザー入力タイトル
  
  // 仕様書準拠: 構造化ログフィールド
  final String initialFeelingVector;              // positive/complex/unknown
  final List<Map<String, dynamic>> responses;     // 各ステップの構造化回答
  final String selectedFeeling;                   // 最終選択感情
  
  final Map<String, dynamic>? additionalData;     // 追加データ
}
```

**responses配列の構造**:
```dart
{
  'prompt_id': 'prompt_positive_step2_v1',     // プロンプトID
  'prompt_version': 1,                          // バージョン
  'prompt_theme': 'このモノがくれた、一番の宝物は？', // 質問テーマ
  'user_response_text': 'テキスト回答内容',       // ユーザー回答
  'tapped_chips': ['楽しい時間', '自信'],        // 選択チップ
}
```

**Firestore保存場所**: `logs/{logId}`

---

## 🔧 主要サービス詳細

### 1. FirestoreService

#### 主要メソッド
```dart
// オブジェクト管理
Future<bool> saveObject(ObjectModel object)
Future<List<ObjectModel>> getUserObjects()
Future<ObjectModel?> getObject(String objectId)

// ログ管理  
Future<bool> saveLog(LogModel log)
Future<List<LogModel>> getObjectLogs(String objectId)
Future<List<LogModel>> getUserLogs()

// カスタムオプション管理
Future<bool> saveCustomOptions(String category, List<String> options)
Future<List<String>> getCustomOptions(String category)
```

#### データ保存処理
```dart
Future<bool> saveLog(LogModel logModel) async {
  try {
    await _firestore.collection('logs').doc(logModel.logId).set({
      'logId': logModel.logId,
      'userId': logModel.userId,
      'objectId': logModel.objectId,
      'emotionalTitle': logModel.emotionalTitle,
      'imageUrl': logModel.imageUrl,
      'createdAt': Timestamp.fromDate(logModel.createdAt),
      'initialFeelingVector': logModel.initialFeelingVector,
      'responses': logModel.responses,  // 構造化ログ
      'selectedFeeling': logModel.selectedFeeling,
    });
    return true;
  } catch (e) {
    return false;
  }
}
```

### 2. CustomOptionsService

#### 機能
- ユーザー個別のカスタムタグ管理
- カテゴリ別制限（10個まで）
- ローカルキャッシュとFirestore同期

#### 主要メソッド
```dart
Future<bool> addCustomOption(String category, String option)
Future<List<String>> getCustomOptions(String category)
bool isLimitReached(String category)
int getCategoryUsage(String category)
```

### 3. AuthService

#### 機能
- Firebase Authentication連携
- ユーザー状態管理
- 自動ログイン

#### 主要プロパティ
```dart
User? get currentUser           // 現在のユーザー
String? get currentUserId       // ユーザーID
bool get isLoggedIn            // ログイン状態
```

### 4. GuideService（操作ガイド）

#### 概要
オンボーディング完了後の連続ガイドモードと、設定画面からの個別ガイドモードを管理するサービス。

#### 主要メソッド
```dart
class GuideService {
  // 連続ガイドモード判定（オンボーディング後の初回完全ガイド）
  static Future<bool> shouldShowContinuousGuide()
  
  // 個別ガイドモード判定（設定画面からの再実行）
  static Future<bool> shouldShowIndividualGuide()
  
  // SimpleHomeScreen用ガイドステップ取得
  static List<GuideStep> getSimpleHomeScreenGuideSteps({
    required GlobalKey? cameraButtonKey,
  })
  
  // 連続ガイド完了マーク
  static Future<void> completeContinuousGuide()
  
  // 個別ガイド完了マーク
  static Future<void> completeIndividualGuide()
}
```

#### ガイドステップ例
```dart
GuideStep(
  title: 'モノログを始める',
  description: '中央のカメラボタンをタップして、新しいモノとの対話を始めましょう。\n写真を撮影して、そのモノとの関係を深く見つめ直すことができます。',
  targetKey: cameraButtonKey,
)
```

### 5. CameraBloc（状態管理）

#### 状態定義
```dart
class CameraState {
  final CameraStatus status;              // カメラ状態
  final CameraController? controller;     // カメラコントローラー
  final Size? imageSize;                  // 画像サイズ
  final String? lastCapturedImagePath;    // 最後の撮影画像
  final String? errorMessage;             // エラーメッセージ
  final String? debugInfo;                // デバッグ情報
}
```

#### 主要イベント
```dart
abstract class CameraEvent {}

class CameraInitialized extends CameraEvent {}
class CameraPhotoCaptureStarted extends CameraEvent {}
class CameraImageCaptureRequested extends CameraEvent {}
class CameraPaused extends CameraEvent {}
class CameraResumed extends CameraEvent {}
```

---

## 🎨 デザイン・UI詳細

### カラーパレット
```dart
// メインカラー
Color(0xFF6A9C89)  // Calm Green - メインアクション
Color(0xFF87A9C4)  // Gentle Blue - サブアクション  
Color(0xFFF8F7F2)  // Paper White - 背景

// テキストカラー
Color(0xFF333333)  // ダークグレー - メインテキスト
Color(0xFF666666)  // ミディアムグレー - サブテキスト
Colors.grey[500]   // ライトグレー - プレースホルダー
```

### フォント
```dart
// メインフォント
fontFamily: 'M PLUS Rounded 1c'

// フォントサイズ
fontSize: 20  // 質問タイトル
fontSize: 16  // ボタンテキスト、入力テキスト
fontSize: 14  // チップテキスト、補助テキスト
fontSize: 12  // キャプション
```

### アニメーション
```dart
// フェードイン
AnimationController(duration: Duration(milliseconds: 800))
Tween<double>(begin: 0.0, end: 1.0)

// スライドイン
AnimationController(duration: Duration(milliseconds: 600))
Tween<Offset>(begin: Offset(0, 0.3), end: Offset.zero)
```

### レイアウト指標
```dart
// 画面分割比率
撮影画像エリア: MediaQuery.height * 0.3  // 30%
コンテンツエリア: Expanded              // 70%

// マージン・パディング
EdgeInsets.all(24)           // メインコンテンツ
EdgeInsets.all(16)           // サブコンテンツ
EdgeInsets.symmetric(horizontal: 12, vertical: 8)  // チップ

// 角丸
BorderRadius.circular(12)    // ボタン、入力フィールド
BorderRadius.circular(20)    // チップ
BorderRadius.circular(25)    // 感情ボタン
```

---

## 🔄 データフロー詳細

### 1. 撮影からログ保存まで

```
1. CameraScreen
   ↓ 撮影ボタンタップ
2. CameraBloc → CameraPhotoCaptureStarted
   ↓ 画像保存
3. Navigator.push(MicroJournalingScreen)
   ↓ ユーザー入力
4. 4段階フロー実行
   ↓ 全ステップ完了
5. _completeJournaling()
   ↓ 構造化ログ作成
6. FirestoreService.saveLog()
   ↓ Firestore保存
7. 完了通知・画面遷移
```

### 2. 構造化ログ作成処理

```dart
// 各ステップの回答を構造化
final responses = <Map<String, dynamic>>[];

for (String step in ['step2', 'step3', 'step4']) {
  final questionsData = _getQuestionsForVector(_selectedVector!, step);
  responses.add({
    'prompt_id': 'prompt_${_selectedVector}_${step}_v1',
    'prompt_version': 1,
    'prompt_theme': questionsData['question'] ?? '',
    'user_response_text': _stepResponses[step] ?? '',
    'tapped_chips': _stepTappedChips[step] ?? [],
  });
}

// LogModel作成
final logModel = LogModel(
  logId: uuid.v4(),
  userId: user.uid,
  objectId: objectId,
  emotionalTitle: _generateEmotionalTitle(),
  imageUrl: widget.imagePath,
  createdAt: DateTime.now(),
  initialFeelingVector: _selectedVector!,
  responses: responses,
  selectedFeeling: _selectedFeeling!,
);
```

### 3. タイトル自動生成

```dart
String _generateEmotionalTitle() {
  // 選択された感情名を取得
  final feeling = _feelingsByVector[_selectedVector!]!
      .firstWhere((f) => f['id'] == _selectedFeeling, 
                 orElse: () => {'name': '気持ち'})['name'];
  
  // step2の回答を使用（最も重要な回答）
  final step2Response = _stepResponses['step2'] ?? '';
  final shortResponse = step2Response.length > 20 
      ? '${step2Response.substring(0, 20)}...' 
      : step2Response;
  
  return '$feeling - $shortResponse';
  // 例: "感謝 - 毎朝使っている時間"
}
```

---

## 🔧 設定・環境詳細

### pubspec.yaml主要依存関係
```yaml
dependencies:
  # Core
  flutter: sdk: flutter
  camera: ^0.11.0              # カメラ機能
  image: ^4.0.17               # 画像処理
  
  # 状態管理
  flutter_bloc: ^8.1.3         # BLoC
  bloc: ^8.1.3
  bloc_concurrency: ^0.2.5
  
  # Firebase
  firebase_core: ^2.24.2       # Firebase基盤
  firebase_auth: ^4.15.3       # 認証
  cloud_firestore: ^4.13.6     # データベース
  firebase_analytics: ^10.7.4  # 分析
  
  # ユーティリティ
  path_provider: ^2.1.1        # ファイルパス
  path: ^1.8.3                 # パス操作
  uuid: ^4.3.3                 # UUID生成
  intl: ^0.19.0                # 国際化
  
  # UI
  google_fonts: ^6.1.0         # フォント
  share_plus: ^7.2.2           # 共有機能
```

### Firebase設定
```
- プロジェクト: mono-log-app
- 認証: Firebase Authentication（匿名ログイン）
- データベース: Cloud Firestore
- ストレージ: Firebase Storage（画像保存）
- 分析: Firebase Analytics
```

---

## 🚀 技術的制約・パフォーマンス

### 技術的制約
- **画像サイズ**: ResolutionPreset.high（デバイス依存）
- **テキスト制限**: 500文字（各ステップ）
- **カスタムタグ**: ステップあたり10個まで
- **オフライン対応**: 限定的（Firebase依存）

### メモリ管理
- 画像ファイルの適切な破棄
- コントローラーのライフサイクル管理
- BLoCの適切なdispose

### セキュリティ
- Firebase Security Rules
- ユーザーデータの分離
- 画像URLの適切な管理

---

## 📝 v3.2 最新実装内容（2025年7月21日）

### 🎨 感情日記風UI統合システム

#### EmotionPaletteService
```dart
class EmotionPaletteService {
  // 感情IDから色彩を取得
  static Color getEmotionColor(String? emotion)
  
  // 感情に応じたグラデーション背景
  static LinearGradient getEmotionGradient(String? emotion)
  
  // 感情アイコンマッピング
  static IconData getEmotionIcon(String? emotion)
  
  // テキスト色の自動調整
  static Color getTextColor(Color backgroundColor)
  
  // 感情説明の日本語化
  static String getEmotionDescription(String? emotion)
}
```

#### EmotionDiaryCard
```dart
class EmotionDiaryCard extends StatelessWidget {
  // 感情ベース背景グラデーション
  // 額縁風画像表示（120x120）
  // TextExtractUtilによる重要フレーズ抽出
  // ジェントルな日付表現
  // スポットライト演出対応
}
```

#### ログ詳細画面
```dart
class LogDetailScreen extends StatelessWidget {
  // メインカード：感情グラデーション + 大画像（200x200）
  // サブカード：ユーザー気持ち記録
  // ハイライト領域の切り抜き表示
  // 感情統一カラーテーマ
}
```

### 🎯 連続チュートリアルシステム

#### TutorialController
```dart
class TutorialController {
  // 画面遷移制御
  static Future<void> handleScreenNavigation(context, screenName)
  
  // アクセス権限チェック
  static Future<bool> canNavigateToScreen(String screenName)
  
  // 進行状況管理
  static Future<void> markTutorialStepCompleted(String step)
}
```

#### TutorialNavigationGuard
```dart
class TutorialNavigationGuard extends StatelessWidget {
  // 制限中のナビゲーション防止
  // 進行状況プログレスバー表示
  // アクセス拒否ダイアログ
}
```

#### GuideService拡張
```dart
// 連続ガイド判定
static Future<bool> shouldShowContinuousGuide()

// チュートリアル進行管理
static Future<void> setTutorialProgress(String progress)
static Future<String?> getTutorialProgress()

// ガイド全体タップ機能
Widget GuideOverlay with GestureDetector全面タップ対応
```

### 🧹 データクリーンアップ

#### 削除された要素
```dart
// ❌ 削除：最終決定フィールド（英語表示問題）
// LogDetailScreen から除去
Text('最終決定: ${log.finalDecision}')

// ❌ 削除：Q&A履歴セクション（未使用機能）
// qaPairs表示ロジック完全除去

// ❌ 削除：ハイライト領域座標表示
// デバッグ用表示の除去
```

#### 保持された要素
```dart
// ✅ 保持：感情ベース視覚要素
// EmotionPaletteServiceによる色彩・アイコン

// ✅ 保持：構造化ログ基盤
// 将来拡張のためのデータ構造維持

// ✅ 保持：画像処理パイプライン
// ハイライト領域切り抜き機能
```

### 🔧 技術改善点

#### 座標補正システム
```dart
// ボタン特定による座標微調整
if (widget is ElevatedButton && step.title.contains('選択を確定')) {
  adjustedPosition = Offset(position.dx, position.dy - 10);
}
```

#### 非同期画像処理
```dart
// 詳細画面での切り抜き画像表示
Future<Widget> _buildCroppedImage() async {
  // 非同期での画像処理
  // エラー時の適切なフォールバック
}
```

#### メモリ最適化
```dart
// ガイド状態のライフサイクル管理
@override
void dispose() {
  if (_showGuide) {
    _showGuide = false;  // 状態クリーンアップ
  }
  super.dispose();
}
```

---

**このドキュメントは『モノログ。』アプリの2025年7月19日時点での完全な実装仕様を記録しています。他のAIや開発者がこの情報を基に、アプリの理解・改善・拡張を行うことができます。**