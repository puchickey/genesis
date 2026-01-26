# モノログ。- 身の回りのモノとの対話を通じた内省アプリ

## 概要

「モノログ。」は、身の回りのモノとの関係性を通じて自己理解を深める内省アプリです。カメラでモノを撮影し、そのモノに対する感情や記憶を記録することで、自分自身の価値観や感情パターンを発見できます。

## 主な特徴

- 📸 **簡単な撮影フロー**: カメラでモノを撮影して内省を開始
- 💭 **感情ベースの内省**: 3つの感情ベクター（ポジティブ、複雑、不明）から選択
- 📝 **構造化された記録**: 段階的な質問で深い内省をサポート
- 🏷️ **モノの戸籍管理**: モノごとに複数の記録を時系列で管理
- 📊 **診断機能**: 6つのタイプから自分の特性を発見
- 🔐 **プライバシー重視**: Firebase匿名認証でアカウント作成不要

## ドキュメント構成

| ドキュメント | 内容 |
|------------|------|
| [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) | プロジェクト全体の詳細な概要 |
| [TECHNICAL_ARCHITECTURE.md](TECHNICAL_ARCHITECTURE.md) | 技術的なアーキテクチャと実装詳細 |
| [SCREENS_AND_FEATURES.md](SCREENS_AND_FEATURES.md) | 全画面と機能の詳細説明 |
| [DATA_MODELS.md](DATA_MODELS.md) | データモデルとFirestore構造 |
| [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md) | 開発環境のセットアップと開発ガイド |

## クイックスタート

### 前提条件
- Flutter 3.24.5以上
- Dart SDK >=3.5.0
- Firebase プロジェクトの設定

### セットアップ
```bash
# 依存関係のインストール
flutter pub get

# ビルドランナーの実行（モックファイル生成）
flutter pub run build_runner build --delete-conflicting-outputs

# アプリの実行
flutter run
```

## アプリの基本フロー

1. **初回起動**: オンボーディング → 診断 → ホーム画面
2. **モノログ作成**: カメラ撮影 → 感情選択 → 内省記録 → カード登録
3. **振り返り**: マイログ画面でこれまでの記録を確認

## 技術スタック

- **フレームワーク**: Flutter 3.24.5
- **状態管理**: flutter_bloc (v8.1.6)
- **バックエンド**: Firebase (Authentication, Firestore, Storage)
- **依存性注入**: get_it (v8.0.2)
- **テスト**: mockito (v5.4.4)

## 開発状況

現在のバージョン: v0.9.0

最新の更新内容や開発状況については、[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)を参照してください。

## ライセンス

このプロジェクトはプライベートプロジェクトです。無断での複製・配布は禁止されています。