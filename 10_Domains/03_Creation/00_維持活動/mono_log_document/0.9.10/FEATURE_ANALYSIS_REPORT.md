### **モノログ・マイログ機能 詳細分析レポート（最終版）**

本資料は、アプリケーションのコア機能である「モノログ」および「マイログ」について、ソースコードを詳細に分析し、現在の動作、目的、画面構成、およびそれを実現するコードを網羅的にまとめたものです。

### 1. モノログ機能（詳細分析）

モノログ機能は、ユーザーが日常のオブジェクトと向き合い、内省を記録するための一連の体験を提供します。このフローは、ホーム画面から始まり、5つの主要な画面を経て記録が完了します。

---

#### **ステップ1: フローの開始 (`HomeScreen`)**

*   **目的**:
    アプリケーションのメインハブとして機能し、ここからモノログ作成フローを開始します。

*   **UIレイアウト**:
    画面中央に「モノログを始める」というタイトルの付いた大きなカード型ボタンが配置されています。

*   **機能とコード**:
    このカードをタップすると、モノログ作成の最初の画面であるカメラプレビュー画面に遷移します。この動作は `HomeScreen` の `_buildFeatureCard` ウィジェットの `onTap` コールバックで定義されています。

    ```dart
    // lib/screens/home_screen.dart

    _buildFeatureCard(
      context,
      icon: Icons.psychology_rounded,
      title: 'モノログを始める',
      // ...
      onTap: () {
        // ... analytics calls
        // カメラプレビュー画面へ遷移
        Navigator.pushNamed(context, AppRoutes.cameraPreview);
      },
      // ...
    ),
    ```
    `AppRoutes.cameraPreview` は `CameraPreviewScreen` に対応付けられています。

---

#### **ステップ2: 写真の撮影または選択 (`CameraPreviewScreen`)**

*   **目的**:
    モノログの対象となるモノの写真を、カメラで新たに撮影するか、デバイスのギャラリーから選択します。

*   **UIレイアウト**:
    *   **メインエリア**: カメラからの映像が全画面でプレビュー表示されます。
    *   **ヘッダー**: 画面上部には「閉じる」ボタンと「フラッシュ」の切り替えボタンがあります。
    *   **フッター**: 画面下部には、「カメラ切り替え」（内側/外側）ボタン、中央に大きな「撮影ボタン」、そして「ギャラリー」ボタンが配置されています。

*   **機能とコード**:
    1.  **撮影**: 中央の「撮影ボタン」をタップすると、`_takePicture()` メソッドが呼ばれます。撮影が成功すると、画像へのパスを引数として次の「範囲選択画面」に遷移します。
    2.  **ギャラリーから選択**: 「ギャラリー」ボタンをタップすると、`_selectFromGallery()` メソッドが呼ばれ、デバイスの画像ピッカーが起動します。画像が選択されると、同様にそのパスを引数として「範囲選択画面」に遷移します。

    どちらのケースでも、画面遷移には `Navigator.pushReplacementNamed` が使用され、現在のカメラ画面を置き換える形で次の画面に進みます。

    ```dart
    // lib/screens/camera_preview_screen.dart

    // _takePicture() 内
    Navigator.pushReplacementNamed(
      context,
      AppRoutes.rangeSelection,
      arguments: {
        'imagePath': picture.path,
      },
    );

    // _selectFromGallery() 内
    Navigator.pushReplacementNamed(
      context,
      AppRoutes.rangeSelection,
      arguments: {
        'imagePath': image.path,
      },
    );
    ```
    `AppRoutes.rangeSelection` は `RangeSelectionScreen` に対応します。

---

#### **ステップ3: 記録範囲の選択 (`RangeSelectionScreen`)**

*   **目的**:
    撮影・選択した写真の中から、ユーザーが特に注目したい「モノ」の部分を矩形で切り出すための画面です。

*   **UIレイアウト**:
    *   画面中央に選択された画像が大きく表示されます。
    *   ユーザーは画面をドラッグすることで、青い枠線の矩形（選択範囲）を描画できます。
    *   画面下部には「次へ」ボタンがあり、範囲が選択されるとアクティブになります。

*   **機能とコード**:
    ユーザーが指でドラッグして範囲を選択すると、その座標が `_startPoint` と `_endPoint` に保存されます。

    「次へ」ボタンをタップすると、`_handleNext()` メソッドが呼ばれます。このメソッドは、画面上の選択範囲の座標を、実際の画像の解像度に合わせた座標（`cropRect`）に変換し、次の「感情選択画面」に渡します。

    ```dart
    // lib/screens/range_selection_screen.dart

    void _handleNext() {
      // ... 座標変換ロジック ...
      final actualRect = Rect.fromLTWH(/* ... */);

      // 感情選択画面へ遷移（現在の画面を置き換える）
      Navigator.pushReplacementNamed(
        context,
        AppRoutes.emotionSelection,
        arguments: {
          'imagePath': widget.imagePath,
          'cropRect': actualRect,
        },
      );
    }
    ```
    `AppRoutes.emotionSelection` は `EmotionSelectionScreen` に対応します。

---

#### **ステップ4: 感情の選択とメモ入力 (`EmotionSelectionScreen`)**

*   **目的**:
    切り出した「モノ」の画像を見ながら、自身の感情を2段階で選択し、任意で内省メモを記録します。この画面がモノログ機能の中核です。

*   **UIレイアウト**:
    *   **画像表示**: 画面上部に、切り出されたモノの写真が小さく表示されます。
    *   **プログレス表示**: ヘッダー部分に、2段階の感情選択の進捗を示すインジケーターがあります。
    *   **感情選択エリア**:
        1.  **第1段階**: 「モノから感じる、一番近い気持ちは何ですか？」という問いかけと共に、5つの主要な感情（喜び、落ち着き、モヤモヤ、悲しみ、驚き）が円形のボタンとして表示されます。
        2.  **第2段階**: 第1段階の感情を選択すると、その感情に関連する6つの具体的な感情が、選択した親感情を中央にして、その周りを衛星のように回る形でアニメーション付きで表示されます。
    *   **メモ入力エリア**: 2段階目の感情を選択すると、画面下部にメモ入力欄（最大500文字）と「記録する」ボタンが表示されます。

*   **機能とコード**:
    この画面は `_currentStep` という内部状態でUIを制御しています。

    1.  **第1感情選択**: `_buildPrimaryEmotionView` で5つの感情ボタンが生成されます。ボタンをタップすると `_handlePrimaryEmotionSelect` が呼ばれ、`_currentStep` が `1` に更新され、第2段階のUIに切り替わります。
    2.  **第2感情選択**: `_buildSecondaryEmotionView` で6つの感情ボタンが円形に配置されます。ボタンをタップすると `_handleSecondaryEmotionSelect` が呼ばれ、`_selectedSecondaryEmotion` がセットされます。
    3.  **保存**: 2段階の感情選択が完了すると、「記録する」ボタンがアクティブになります。タップすると `_handleSave()` が呼ばれます。このメソッドは `MonologBloc` に `CreateMonolog` イベントを発行し、非同期で保存処理を行います。

    保存処理が成功すると、次の「完了画面」に遷移します。

    ```dart
    // lib/screens/emotion_selection_screen.dart

    void _handleSave() async {
      // ... 保存処理 ...

      // BLoCのストリームを監視して状態変化を待つ
      await for (final state in monologBloc.stream) {
        if (state is MonologCreated) {
          // ...
          // 成功：完了画面へ遷移
          if (mounted) {
            Navigator.pushReplacementNamed(
              context,
              AppRoutes.completion,
              arguments: { /* ...記録データ... */ },
            );
          }
          break;
        }
        // ... エラー処理 ...
      }
    }
    ```
    `AppRoutes.completion` は `CompletionScreen` に対応します。

---

#### **ステップ5: 記録の完了 (`CompletionScreen`)**

*   **目的**:
    記録が正常に完了したことをユーザーに伝え、達成感を演出し、次の行動を促します。

*   **UIレイアウト**:
    *   **背景**: 選択した感情に応じたグラデーションと、光や粒子が舞うアニメーションが表示されます。
    *   **完了メッセージ**: 「記録が完了しました」というテキストが表示されます。
    *   **モノログカード**: 作成されたばかりのモノログが、画像、感情、日時などを含むカード形式で中央に表示されます。このカードは3Dのようなアニメーションで出現します。
    *   **行動喚起テキスト**: カードの下に「カードをタップして名前をつけよう」と表示されます。
    *   **ボタン**: 画面下部に「続けてモノログする」と「ホーム画面に戻る」の2つのボタンが配置されます。

*   **機能とコード**:
    この画面は複数の `AnimationController` を駆使して、仕様書に定義された複雑な出現アニメーションを実現しています。

    *   **カードのタップ**: 表示されたモノログカード全体が `GestureDetector` で囲まれており、タップすると `_navigateToMyLogDetail()` が呼ばれ、今作成したモノログの詳細画面（マイログ機能の一部）に直接遷移できます。
    *   **ボタンのタップ**:
        *   「続けてモノログする」: `_continueMonolog()` が呼ばれ、カメラ画面 (`AppRoutes.cameraPreview`) に戻り、すぐに次のモノログを作成できます。
        *   「ホーム画面に戻る」: `_returnToHome()` が呼ばれ、ホーム画面に遷移します。

    ```dart
    // lib/screens/completion_screen.dart

    void _navigateToMyLogDetail() {
      // ... BLoCから保存されたモノログを取得するロジック ...
      if (savedMonolog != null) {
        // マイログ一覧を経由して詳細画面へ
        Navigator.of(context).pushNamedAndRemoveUntil(
          AppRoutes.mylog, (route) => route.isFirst,
        );
        Navigator.of(context).push(
          MaterialPageRoute(
            builder: (context) => MyLogDetailScreen(monolog: savedMonolog!),
            // ...
          ),
        );
      }
    }
    ```
---

### 2. マイログ機能（詳細分析）

マイログ機能は、ユーザーが過去に作成した全てのモノログを閲覧、管理、編集するための機能群です。この機能は主に「一覧画面」と「詳細画面」の2つの画面で構成されています。

---

#### **画面1: マイログ一覧 (`MyLogListScreen`)**

*   **目的**:
    保存されている全てのモノログをリストまたはギャラリー形式で表示し、個々の記録へのアクセスポイントを提供します。

*   **UIレイアウトとBLoC連携**:
    この画面は `MonologBloc` と密に連携しており、現在の状態 (`MonologState`) に応じて表示内容が動的に変化します。

    *   **データ読み込み**: 画面初期化時 (`initState`) に `LoadMonologs` イベントが発行されます。
        ```dart
        // lib/screens/mylog_list_screen.dart
        @override
        void initState() {
          super.initState();
          // ...
          context.read<MonologBloc>().add(const LoadMonologs());
        }
        ```
    *   **UIの構築**: `BlocBuilder` が `MonologBloc` の状態を監視し、UIを構築します。
        ```dart
        // lib/screens/mylog_list_screen.dart
        BlocBuilder<MonologBloc, MonologState>(
          builder: (context, state) {
            if (state is MonologLoading) {
              return const Center(child: CircularProgressIndicator(...));
            }
            if (state is MonologError) {
              return Center(child: Text('エラーが発生しました...'));
            }
            if (state is MonologLoaded) {
              // ログリストを表示
              final monologs = state.monologs;
              if (monologs.isEmpty) {
                return _buildEmptyState(); // 「まだ記録がありません」
              }
              return _isGalleryView
                  ? _buildGalleryView(monologs)
                  : _buildListView(monologs);
            }
            return _buildEmptyState();
          },
        )
        ```
    *   **表示モード**: `_isGalleryView` というbool値の状態で、2列のグリッド表示 (`_buildGalleryView`) と1列のリスト表示 (`_buildListView`) を切り替えます。この切り替えは `AppBar` の `IconButton` で行われます。

*   **機能とコード**:
    *   **フィルターとソート**: `AppBar` のフィルターアイコンをタップすると `_showFilterOptions` が呼ばれ、モーダルボトムシートが表示されます。ここで選択された条件（感情、日付順）は `_filterAndSortMonologs` メソッドで使用され、表示されるログのリストが更新されます。
    *   **詳細画面への遷移**: ギャラリーまたはリストの各アイテムは `GestureDetector` でラップされており、タップすると `MyLogDetailScreen` へ遷移します。この際、`Hero` ウィジェットが画像のトランジションアニメーションを実現します。
        ```dart
        // lib/screens/mylog_list_screen.dart -> _buildGalleryItem 内
        GestureDetector(
          onTap: () {
            Navigator.pushNamed(
              context,
              AppRoutes.mylogDetail,
              arguments: monolog, // タップされたMonologModelオブジェクトを渡す
            );
          },
          child: Hero(
            tag: 'monolog-image-${monolog.logId}', // 一意のタグ
            child: // ...画像ウィジェット
          ),
        )
        ```

---

#### **画面2: マイログ詳細 (`MyLogDetailScreen`)**

*   **目的**:
    単一のモノログの詳細情報を表示し、タイトルやメモの編集、および記録自体の削除機能を提供します。

*   **UIレイアウトと状態管理**:
    この画面は `_isEditing` というbool値の状態で「閲覧モード」と「編集モード」を切り替えます。

    *   **閲覧モード (`_isEditing == false`)**:
        *   `AppBar` には「マイログ詳細」というタイトルと「編集」アイコンが表示されます。
        *   ボディには、`Hero` アニメーションで表示される画像、日時、編集不可のタイトルとメモが表示されます。
        *   メモが長い場合は `_shouldShowExpandButton()` が `true` を返し、「...もっと読む」ボタンが表示されます。
        *   画面下部には「この記録を削除」ボタンが表示されます。
    *   **編集モード (`_isEditing == true`)**:
        *   `AppBar` のタイトルは「編集」に、アクションボタンは「保存」に変わります。
        *   タイトルとメモが `TextField` になり、編集可能になります。
        *   画面下部には「キャンセル」と「保存」ボタンを持つボトムバーが表示されます。

*   **機能とコード**:
    *   **編集機能**:
        1.  「編集」アイコンタップで `_toggleEdit()` が呼ばれ、`setState` で `_isEditing` が `true` になります。
        2.  ユーザーが `TextField` でタイトルやメモを編集します。
        3.  「保存」ボタンをタップすると `_saveChanges()` が呼ばれます。このメソッドは `MonologBloc` に `UpdateMonolog` イベントを発行し、変更をデータベースに保存します。
            ```dart
            // lib/screens/mylog_detail_screen.dart
            void _saveChanges() {
              context.read<MonologBloc>().add(
                UpdateMonolog(
                  logId: widget.monolog.logId,
                  title: _titleController.text,
                  memo: _memoController.text,
                ),
              );
              setState(() { _isEditing = false; }); // 閲覧モードに戻る
            }
            ```
    *   **削除機能**:
        1.  「この記録を削除」ボタンをタップすると `_showDeleteConfirmation()` が呼ばれ、確認ダイアログが表示されます。
        2.  ダイアログで「削除」を選択すると、`MonologBloc` に `DeleteMonolog` イベントが発行され、記録が削除されます。その後、`Navigator.pop(context)` で一覧画面に戻ります。
            ```dart
            // lib/screens/mylog_detail_screen.dart -> _showDeleteConfirmation 内
            TextButton(
              onPressed: () {
                context.read<MonologBloc>().add(
                  DeleteMonolog(logId: widget.monolog.logId),
                );
                Navigator.pop(context); // ダイアログを閉じる
                Navigator.pop(context); // 詳細画面を閉じる
              },
              child: const Text('削除', ...),
            ),
            ```
---

### 3. 結論

当初の分析ではモノログ作成フローに実装の不備があるとの結論に至りましたが、ユーザー様からのご指摘を受け、ホーム画面からの遷移を再調査した結果、その結論は誤りであったことが判明しました。以下に、最終的な結論を記します。

*   **モノログ機能とマイログ機能は、両方とも仕様書に忠実に、かつ高い完成度で実装されている。**
    *   **モノログ作成フロー**: ホーム画面から始まり、カメラ、範囲選択、2段階の感情選択、そしてアニメーションを伴う完了画面へと続く、一貫した5ステップの体験が完全に実装されています。これは `emotion_selection_screen.dart` を中心とする、洗練された実装です。
    *   **マイログ閲覧・管理フロー**: 記録の一覧表示（ギャラリー/リスト）、フィルター、ソート、詳細表示、編集、削除といった全ての機能が、仕様書通りに堅牢に実装されています。

*   **`simple_micro_journaling_screen.dart` は、現在使用されていないコードである。**
    *   分析の初期段階で混乱の原因となったこのファイルは、3つの感情ボタンを持つ簡易的なUIであり、実際のアプリケーションフローからは呼び出されていません。これは、開発過程で作成された古いバージョン、あるいはデバッグ目的の画面である可能性が極めて高いと結論付けられます。

総じて、本アプリケーションのモノログおよびマイログ機能は、ユーザーに一貫性のある豊かな内省体験を提供するための主要機能が、設計通りにほぼ完全に実装されている状態にあると評価できます。
