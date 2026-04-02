import os
import time
import subprocess
import sys

# cdp_browser.pyにパスを通す
sys.path.append(r"G:\マイドライブ\Genesis_OS\.agent\scripts")
from cdp_browser import CDPBrowser

BASE_DIR = r"G:\マイドライブ\Genesis_OS\00_SYSTEM\CORE"
OUTBOX = os.path.join(BASE_DIR, "outbox")
INBOX = os.path.join(BASE_DIR, "inbox")

# === CONFIGURATION (Phase 5) ===
# Antigravityのチャット画面へ自動で完了報告を打ち込む機能のオンオフ
ENABLE_ANTIGRAVITY_CDP_AUTO_INPUT = False 
ANTIGRAVITY_CDP_PORT = 9224
# ===============================

def show_toast(title, message):
    ps_script = f"""
    [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
    $template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
    $textNodes = $template.GetElementsByTagName('text')
    $textNodes.Item(0).AppendChild($template.CreateTextNode("{title}")) | Out-Null
    $textNodes.Item(1).AppendChild($template.CreateTextNode("{message}")) | Out-Null
    $toast = [Windows.UI.Notifications.ToastNotification]::new($template)
    $notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('Genesis OS')
    $notifier.Show($toast)
    """
    subprocess.run(["powershell", "-Command", ps_script], creationflags=subprocess.CREATE_NO_WINDOW)

def process_outbox():
    for filename in os.listdir(OUTBOX):
        if filename.endswith(".md"):
            filepath = os.path.join(OUTBOX, filename)
            print(f"[Coordinator] Detected new task specification: {filename}")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                prompt_content = f.read().strip()
                
            # Gemini CLIに全ての判断と実行を委ねる（ズルを廃止）
            # プロンプト内で「必要に応じて自律的にターミナルコマンドを実行すること」を強調
            system_instruction = (
                f"あなたはGenesis OSのバックグラウンドワーカーです。以下の指示を熟読し、ReActループを用いて自律的に作業を完遂せよ。\\n"
                f"必要であればターミナル（シェル）組み込みツールを用いて指定されたPythonスクリプト等（例：G:\\マイドライブ\\Genesis_OS\\.agent\\scripts\\ 内のファイル）を実行せよ。\\n"
                f"実行の際は、OSのデフォルトPython環境を利用し、仮想環境の差異に注意せよ。\\n"
                f"最終結果は必ず {INBOX} 内にMarkdownファイルとして出力して終了せよ。\\n\\n"
            )
            
            # Yoloモード相当のフラグがあれば付与（コマンドライン引数の詳細は要調整だが、まずは標準のプロンプトで実行機能を引き出す）
            # もし npm の @google/gemini-cli で実行機能がプロンプトから呼べるならこれで起動する
            # ※注：もし実際のコマンドに --yolo オプションがあるなら追加する
            cmd = f"gemini --prompt '{system_instruction}{prompt_content}'"
            
            print(f"[Coordinator] Routing task {filename} to Gemini CLI...")
            try:
                subprocess.Popen(["powershell", "-Command", cmd], creationflags=subprocess.CREATE_NEW_CONSOLE)
                print(f"[Coordinator] Task dispatched to Gemini CLI in background.")
            except Exception as e:
                print(f"[Coordinator] Error dispatching to Gemini: {e}")
                
            # 処理が終わった指示書は消す
            os.remove(filepath)

def inject_to_antigravity(message):
    try:
        b = CDPBrowser(port=ANTIGRAVITY_CDP_PORT)
        b.connect()
        # 確実に入力欄にフォーカスを当てる
        js_focus = """
        (function() {
            let ta = document.querySelector('div.cursor-text[contenteditable="true"]') || document.querySelector('textarea, [contenteditable="true"]');
            if (ta) {
                ta.focus();
                return true;
            }
            return false;
        })()
        """
        if b.evaluate(js_focus):
            time.sleep(0.5)
            # ネイティブAPI経由での確実な入力
            b.send_command("Input.insertText", {"text": message})
            
            # Enterキーのネイティブ発火
            b.send_command("Input.dispatchKeyEvent", {
                "type": "keyDown",
                "windowsVirtualKeyCode": 13, 
                "unmodifiedText": "\r", 
                "text": "\r"
            })
            b.send_command("Input.dispatchKeyEvent", {
                "type": "keyUp",
                "windowsVirtualKeyCode": 13
            })
            
            print("[CDP Injector] Injected successfully via native API.")
        else:
            print("[CDP Injector] Input area not found.")
    except Exception as e:
        print(f"[CDP Injector] Failed to inject: {e}")
        print(f"** Antigravityが --remote-debugging-port={ANTIGRAVITY_CDP_PORT} で起動されているか確認してください。")

def monitor_inbox():
    if not hasattr(monitor_inbox, "processed_set"):
        monitor_inbox.processed_set = set(os.listdir(INBOX))
        
    current_set = set(os.listdir(INBOX))
    new_files = current_set - monitor_inbox.processed_set
    
    for f in new_files:
        if f.endswith(".md") or f.endswith(".json"):
            print(f"[Coordinator] New report logic triggered: {f}")
            show_toast("Genesis OS / Inbox", f"作業部隊から新しいレポートが届きました: {f}")
            
            # Phase 5: Antigravityへの自動入力がONなら実行
            if ENABLE_ANTIGRAVITY_CDP_AUTO_INPUT:
                inject_to_antigravity(f"裏での作業が完了し、レポート `{f}` がinboxに格納されました。内容を確認後、要約して教えてください。")
            
            monitor_inbox.processed_set.add(f)

def run():
    print("=======================================")
    print("Genesis OS Multi-Agent Coordinator v1.0")
    print(f"Monitoring Outbox (Task Queue): {OUTBOX}")
    print(f"Monitoring Inbox  (Results)   : {INBOX}")
    print("=======================================")
    
    while True:
        try:
            process_outbox()
            monitor_inbox()
            time.sleep(3)
        except Exception as e:
            print(f"[Error in Event Loop] {e}")
            time.sleep(5)

if __name__ == "__main__":
    run()
