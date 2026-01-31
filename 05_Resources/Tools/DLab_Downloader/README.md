# D-Lab Automated Downloader

**Purpose:** D-Lab (daigovideo.jp) の動画を自動/半自動で収集するツール。

---

## 🛠️ Setup

1.  **Chromeのインストール**: Google Chromeが必要です。
2.  **依存ライブラリのインストール**:
    *   同封の `setup.bat` をダブルクリックして実行してください。
    *   (または `pip install selenium webdriver-manager requests` を実行)

## 📖 Usage

1.  `downloader.py` を実行します。
    ```powershell
    python downloader.py
    ```
2.  Chromeブラウザが自動で立ち上がります。
3.  **初回ログイン**:
    *   ログイン画面が表示されます。
    *   **手動で** メールアドレスとパスワードを入力してログインしてください。
    *   ログインできたら、コンソール画面で `Enter` キーを押します。
4.  **ダウンロード**:
    *   メニューから 「1. URL指定」 または 「2. 手動移動」 を選べます。
    *   **Option 2 (推奨):** ブラウザ上で好きな動画ページを開き、コンソールでEnterを押すと、その場の動画を `Inbox` にダウンロードします。

## 📂 Output
ダウンロードされた動画は以下に保存されます:
`g:\マイドライブ\Genesis_OS\05_Resources\Inbox`
