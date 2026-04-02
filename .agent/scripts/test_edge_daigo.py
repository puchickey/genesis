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
    
    print("Waiting for page load...")
    time.sleep(5)
    
    title = b.evaluate("document.title")
    
    # ログイン状態の簡単なチェック
    # 例えば動画一覧などの要素があるかなど
    body_html = b.evaluate("document.body.innerHTML.substring(0, 300)")
    
    print("===============================")
    print("Edge Automation: Success!")
    print(f"Page Title: {title}")
    print("===============================")
    
except Exception as e:
    print("Error:", e)
