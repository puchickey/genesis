"""
Nano Banana Pro サムネイル生成スクリプト
Gemini API のネイティブ画像生成機能を使用して、note.com記事のサムネイルを生成する。
"""
import sys
import base64
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image
import io

# --- 設定 ---
MODEL = "gemini-3-pro-image-preview"  # Nano Banana Pro
THUMBNAIL_DIR = Path(r"g:\マイドライブ\Genesis_OS\10_Domains\03_Creation\01_投資活動\note\thumnail")
BACKGROUND = THUMBNAIL_DIR / "thumnail_background.jpg"
ICON_DIR = THUMBNAIL_DIR / "icon_note"
ARTICLE_DIR = THUMBNAIL_DIR / "article"
OUTPUT_DIR = Path(r"g:\マイドライブ\Genesis_OS\10_Domains\03_Creation\01_投資活動\note\thumbnails")

def load_image(path: Path) -> Image.Image:
    """画像を読み込む"""
    return Image.open(path)

def generate_thumbnail(
    top_text: str,
    main_text: str, 
    bottom_text: str,
    icon_name: str,
    reference_article: str,
    output_name: str
):
    """サムネイルを生成する"""
    
    # クライアント初期化（ADC使用）
    client = genai.Client()
    
    # 参照画像を読み込む
    background = load_image(BACKGROUND)
    icon = load_image(ICON_DIR / icon_name)
    reference = load_image(ARTICLE_DIR / reference_article)
    
    prompt = f"""あなたはプロのサムネイルデザイナーです。

以下の3つの参照画像を使って、note.com記事のサムネイル画像を1枚生成してください。

【参照画像の役割】
- 1枚目: 背景画像（そのまま背景として使用）
- 2枚目: 人物キャラクター（右側に配置。このキャラクターの見た目を正確に再現してください）
- 3枚目: レイアウト・スタイルの参考（この画像と全く同じレイアウト・フォント処理・構図で作ってください）

【出力要件】
- サイズ: 横1280px × 縦670px（16:9に近い横長バナー）。絶対に正方形にしないでください。
- 背景: 1枚目の基板パターン背景を全面に使用
- 白枠: 四辺に細い白い枠線（内側マージン付き）

【テキスト配置（左側60%のみ）】
- 上段: 白い帯（角丸長方形）の上に太い黒文字で「{top_text}」
- 中段: 超大サイズのメタリックシルバー文字（グラデーション＋光沢効果）で「{main_text}」← これが一番大きいテキスト
- 下段: 白い太字で「{bottom_text}」
- 特別ルール: テキストに「Google」という単語が含まれる場合、その部分だけ本物のGoogleロゴと同じカラフルな配色（青・赤・黄・青・緑・赤の順の各文字色）で表示すること

【人物キャラクター配置（右側40%）】
- 2枚目のキャラクターを右半分に配置
- 腰から下はトリミング（画面外）
- キャラクターの背後にキラキラのパーティクル効果（白〜水色の光の粒子）
- テキストとキャラクターは重ならないようにする
- 重要: キャラクターの肌色は参照画像の元の色（自然な肌色）を正確に保ってください。青白くしたり、背景色に染めたりしないでください

【厳守事項】
- 指定した3行のテキスト以外は絶対に追加しないでください
- テキストの文字は1文字も省略しないでください。「{main_text}」は全文字を含めてください
- 横長バナー形式を厳守（正方形は不可）
- キャラクターの肌色を自然に保つこと（青白くしない）
"""
    
    response = client.models.generate_content(
        model=MODEL,
        contents=[prompt, background, icon, reference],
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
        )
    )
    
    # レスポンスから画像を保存
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / output_name
    
    for part in response.parts:
        if part.inline_data is not None:
            img = part.as_image()
            img.save(str(output_path))
            print(f"✅ サムネイル保存完了: {output_path}")
            return output_path
    
    print("❌ 画像が生成されませんでした")
    return None


# --- 生成定義 ---
THUMBNAILS = [
    {
        "top_text": "課金してる僕が言う",
        "main_text": "無料でいい",
        "bottom_text": "Antigravityの本音",
        "icon_name": "icon_笑顔で指を立てる.png",
        "reference_article": "note_023.png",
        "output_name": "thumb_v2_001_muryou.png",
    },
    {
        "top_text": "AIが「怖い」なら",
        "main_text": "画面を見て",
        "bottom_text": "Antigravityは見える",
        "icon_name": "icon_頭を抱えて驚く.png",
        "reference_article": "note_021.png",
        "output_name": "thumb_v2_002_kowai.png",
    },
    {
        "top_text": "ChatGPTの先へ",
        "main_text": "Google Antigravity",
        "bottom_text": "パソコンが動く体験",
        "icon_name": "icon_右手を差し出す.png",
        "reference_article": "note_022.png",
        "output_name": "thumb_v2_003_chatgpt.png",
    },
]

if __name__ == "__main__":
    import sys
    # 引数で番号指定（1,2,3）。なければ全部生成
    targets = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [1, 2, 3]
    
    for i in targets:
        t = THUMBNAILS[i - 1]
        print(f"\n--- 記事{i} 生成中 ---")
        result = generate_thumbnail(**t)
        if result:
            print(f"✅ 完了: {result}")
