import os
import time
import subprocess
import sys
import requests
import shutil

# cdp_browser.pyにパスを通す
sys.path.append(r"G:\マイドライブ\Genesis_OS\.agent\scripts")
from cdp_browser import CDPBrowser

BASE_DIR = r"G:\マイドライブ\Genesis_OS\00_SYSTEM\CORE"
OUTBOX = os.path.join(BASE_DIR, "outbox")
INBOX = os.path.join(BASE_DIR, "inbox")
REPO_ROOT = r"G:\マイドライブ\Genesis_OS"
TEMP_DIR = r"C:\tmp"
REPORTED_PRS_FILE = os.path.join(os.path.dirname(__file__), "reported_prs.txt")
ENV_FILE = os.path.join(REPO_ROOT, ".env")

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
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    for filename in os.listdir(OUTBOX):
        if filename.endswith(".md"):
            filepath = os.path.join(OUTBOX, filename)
            print(f"[Coordinator] Detected new task specification: {filename}")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                prompt_content = f.read().strip()
                
            # ASSIGNEE: Jules があるか確認
            is_jules_task = "ASSIGNEE: Jules" in prompt_content
            
            if is_jules_task:
                # Jules CLIを使って実行
                print(f"[Coordinator] Routing task {filename} to Jules CLI...")
                clean_prompt = prompt_content.replace("ASSIGNEE: Jules", "").strip()
                cmd = f"jules new \"{clean_prompt}\""
                try:
                    subprocess.Popen(["powershell", "-Command", cmd], cwd=REPO_ROOT, creationflags=subprocess.CREATE_NEW_CONSOLE)
                    print(f"[Coordinator] Task dispatched to Jules CLI in background.")
                except Exception as e:
                    print(f"[Coordinator] Error dispatching to Jules: {e}")
            else:
                # Layer A Workflow: /tmp/ にファイルをコピーしてパスを渡す
                temp_filepath = os.path.join(TEMP_DIR, filename)
                shutil.copy2(filepath, temp_filepath)
                
                report_name = filename.replace(".md", "_report.md")
                inbox_path = os.path.join(INBOX, report_name)
                
                # Gemini CLIにC:\tmp\のファイルを読ませる
                instruction = f"Read the file {temp_filepath} and execute all instructions. Write report to {inbox_path}"
                cmd = f"gemini -y -p \"{instruction}\""
                
                print(f"[Coordinator] Routing task {filename} to Gemini CLI via Layer A workflow...")
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

def check_github_prs():
    """
    puchickey/genesis repositoryのOpenなPRを確認し、
    未報告のものがあればレポートをinboxに作成する。
    """
    repo = "puchickey/genesis"
    url = f"https://api.github.com/repos/{repo}/pulls?state=open"
    
    # .envからTOKENを取得
    github_token = None
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, 'r') as f:
            for line in f:
                if line.startswith("GITHUB_TOKEN="):
                    github_token = line.split("=", 1)[1].strip()
    
    headers = {}
    if github_token:
        headers["Authorization"] = f"token {github_token}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            prs = response.json()
            
            # 既報のPR IDを読み込む
            reported_ids = set()
            if os.path.exists(REPORTED_PRS_FILE):
                with open(REPORTED_PRS_FILE, 'r') as f:
                    reported_ids = {line.strip() for line in f if line.strip()}
            
            new_prs_found = False
            for pr in prs:
                pr_id = str(pr['id'])
                if pr_id not in reported_ids:
                    # レポート作成
                    report_filename = f"jules_pr_{pr['number']}.md"
                    report_path = os.path.join(INBOX, report_filename)
                    
                    report_content = f"""# New Pull Request Detected
- **Title**: {pr['title']}
- **Number**: {pr['number']}
- **User**: {pr['user']['login']}
- **URL**: {pr['html_url']}
- **Body**:
{pr['body']}
"""
                    with open(report_path, 'w', encoding='utf-8') as f:
                        f.write(report_content)
                    
                    print(f"[Coordinator] New PR report created: {report_filename}")
                    show_toast("Genesis OS / GitHub", f"新しいPRが届きました: #{pr['number']} {pr['title']}")
                    
                    reported_ids.add(pr_id)
                    new_prs_found = True
            
            if new_prs_found:
                # 報告済みリストを更新
                with open(REPORTED_PRS_FILE, 'w') as f:
                    for rid in reported_ids:
                        f.write(rid + "\n")
        else:
            # 頻繁に出すぎるとうるさいのでエラー時は表示のみ
            if response.status_code != 403: # 403はレートリミットの可能性
                print(f"[Coordinator] GitHub API error: {response.status_code} {response.text}")
    except Exception as e:
        print(f"[Coordinator] Failed to check GitHub PRs: {e}")

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
            check_github_prs()
            time.sleep(3)
        except Exception as e:
            print(f"[Error in Event Loop] {e}")
            time.sleep(5)

if __name__ == "__main__":
    run()
