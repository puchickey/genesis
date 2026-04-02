import sys
import time
sys.path.append(r"G:\マイドライブ\Genesis_OS\.agent\scripts")
from cdp_browser import CDPBrowser

print("Connecting to Edge CDP (Port 9223)...")
try:
    b = CDPBrowser(port=9223)
    b.connect()
    
    print("Navigating to https://daigovideolab.jp/ ...")
    b.navigate("https://daigovideolab.jp/")
    
    print("Waiting for page load and authentication...")
    time.sleep(5)
    
    # 最新の動画リンクを探してクリックするスクリプト
    js_find_and_click = """
    (function() {
        let links = Array.from(document.querySelectorAll('a'));
        
        // 動画ページへのパスが含まれていそうなリンクを探す（例: /videos/ /archive/ /programs/ /movies/）
        let videoLink = links.find(el => {
            let href = el.getAttribute('href') || '';
            let url = el.href || '';
            // 最も一般的な動画詳細ページのパス
            return url.includes('/video') || url.includes('/archive') || url.includes('/program') || href.includes('/video');
        });
        
        // もし見つからなければ、画像を包んでいるリンクのうち、ナビゲーションやロゴを除外したものを選ぶ
        if (!videoLink) {
            let imgLinks = links.filter(el => el.querySelector('img'));
            // ページ上部のロゴ画像などを避けるため、2番目以降の画像リンクを試す
            if (imgLinks.length > 2) {
                videoLink = imgLinks[2];
            } else if (imgLinks.length > 0) {
                videoLink = imgLinks[0];
            }
        }
        
        if (videoLink) {
            // CDP経由でネイティブなクリックを発火させるのが一番確実だが、まずはJSでclick()メソッドを呼ぶ
            videoLink.click();
            return "Clicked linking to: " + videoLink.href;
        }
        return "No suitable video link found.";
    })()
    """
    
    print("Attempting to click the latest video link...")
    res = b.evaluate(js_find_and_click)
    print('DOM Logic Result:', res)
    
    # 画面遷移を待つ
    time.sleep(4)
    final_title = b.evaluate("document.title")
    print("===============================")
    print(f"Target Page Title: {final_title}")
    print("===============================")
    
except Exception as e:
    print("Error:", e)
