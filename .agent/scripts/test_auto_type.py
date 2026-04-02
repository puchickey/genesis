import sys
import time
sys.path.append(r"G:\マイドライブ\Genesis_OS\.agent\scripts")
from cdp_browser import CDPBrowser

print("Retrying Antigravity injection test using native CDP Input...")

try:
    b = CDPBrowser(port=9224)
    b.connect()
    
    # 確実に入力欄にフォーカスを当てる
    js_focus = """
    (function() {
        let ta = document.querySelector('div.cursor-text[contenteditable="true"]') || document.querySelector('textarea, [contenteditable="true"]');
        if (ta) {
            ta.focus();
            return "Focused";
        }
        return "Not found";
    })()
    """
    res1 = b.evaluate(js_focus)
    print("Focus result:", res1)
    
    if res1 == "Focused":
        time.sleep(0.5) # フォーカスが当たるのを少し待つ
        
        message = "【最終テスト完了】ネイティブ入力APIを使いました。これでいかがですか！？"
        # ブラウザレベルで「実際に文字が打ち込まれた」という信号を直接送る
        b.send_command("Input.insertText", {"text": message})
        print("Text inserted natively via CDP.")
        print("Please check the input area.")
    
except Exception as e:
    print("Injection Error:", e)
