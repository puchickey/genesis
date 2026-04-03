import os
import time
import subprocess
import sys
import shutil
import logging
from datetime import datetime, timedelta

# cdp_browser.pyにパスを通す
sys.path.append(r"G:\マイドライブ\Genesis_OS\.agent\scripts")

BASE_DIR = r"G:\マイドライブ\Genesis_OS\00_SYSTEM\CORE"
OUTBOX = os.path.join(BASE_DIR, "outbox")
INBOX = os.path.join(BASE_DIR, "inbox")
INBOX_ARCHIVE = os.path.join(INBOX, "archive")
REPO_ROOT = r"G:\マイドライブ\Genesis_OS"
TEMP_DIR = r"C:\tmp"
REPORTED_PRS_FILE = os.path.join(os.path.dirname(__file__), "reported_prs.txt")
ENV_FILE = os.path.join(REPO_ROOT, ".env")
LOG_FILE = os.path.join(os.path.dirname(__file__), "coordinator_log.txt")

# === タイミング設定 ===
OUTBOX_INTERVAL_SEC = 10       # outbox/inbox チェック間隔
PR_CHECK_INTERVAL_SEC = 1800   # GitHub PR チェック間隔（30分）

# === CDP自動入力設定 ===
ENABLE_ANTIGRAVITY_CDP_AUTO_INPUT = False
ANTIGRAVITY_CDP_PORT = 9224

# === ロギング設定 ===
logger = logging.getLogger("GenesisCoordinator")
logger.setLevel(logging.INFO)

# ファイルハンドラ
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(file_handler)

# コンソールハンドラ
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(console_handler)


def show_toast(title, message):
    try:
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
        subprocess.run(["powershell", "-Command", ps_script], creationflags=subprocess.CREATE_NO_WINDOW, timeout=10)
    except Exception as e:
        logger.warning(f"Toast通知の送信に失敗: {e}")


def process_outbox():
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    for filename in os.listdir(OUTBOX):
        if not filename.endswith(".md"):
            continue

        filepath = os.path.join(OUTBOX, filename)
        logger.info(f"新しいタスク指示書を検出: {filename}")

        with open(filepath, 'r', encoding='utf-8') as f:
            prompt_content = f.read().strip()

        # ASSIGNEE: Jules があるか確認
        is_jules_task = "ASSIGNEE: Jules" in prompt_content

        if is_jules_task:
            logger.info(f"タスク {filename} を Jules CLI にルーティング中...")
            clean_prompt = prompt_content.replace("ASSIGNEE: Jules", "").strip()
            cmd = f'jules new "{clean_prompt}"'
            try:
                subprocess.Popen(["powershell", "-Command", cmd], cwd=REPO_ROOT, creationflags=subprocess.CREATE_NEW_CONSOLE)
                logger.info(f"Jules CLI への配送完了")
            except Exception as e:
                logger.error(f"Jules への配送エラー: {e}")
        else:
            # Layer A Workflow: /tmp/ にファイルをコピーしてパスを渡す
            temp_filepath = os.path.join(TEMP_DIR, filename)
            shutil.copy2(filepath, temp_filepath)

            report_name = filename.replace(".md", "_report.md")
            inbox_path = os.path.join(INBOX, report_name)

            instruction = f"Read the file {temp_filepath} and execute all instructions. Write report to {inbox_path}"
            cmd = f'gemini -y -p "{instruction}"'

            logger.info(f"タスク {filename} を Gemini CLI にルーティング中...")
            try:
                subprocess.Popen(["powershell", "-Command", cmd], creationflags=subprocess.CREATE_NEW_CONSOLE)
                logger.info(f"Gemini CLI への配送完了")
            except Exception as e:
                logger.error(f"Gemini CLI への配送エラー: {e}")

        # 処理が終わった指示書は消す
        os.remove(filepath)


def monitor_inbox():
    if not hasattr(monitor_inbox, "processed_set"):
        monitor_inbox.processed_set = set(os.listdir(INBOX))

    current_set = set(os.listdir(INBOX))
    new_files = current_set - monitor_inbox.processed_set

    for f in new_files:
        if f.endswith(".md") or f.endswith(".json"):
            logger.info(f"新しいレポートを検知: {f}")
            show_toast("Genesis OS / Inbox", f"新しいレポートが届きました: {f}")

            if ENABLE_ANTIGRAVITY_CDP_AUTO_INPUT:
                _inject_to_antigravity(f"裏での作業が完了し、レポート `{f}` がinboxに格納されました。内容を確認後、要約して教えてください。")

            monitor_inbox.processed_set.add(f)


def _inject_to_antigravity(message):
    try:
        from cdp_browser import CDPBrowser
        b = CDPBrowser(port=ANTIGRAVITY_CDP_PORT)
        b.connect()
        js_focus = """
        (function() {
            let ta = document.querySelector('div.cursor-text[contenteditable="true"]') || document.querySelector('textarea, [contenteditable="true"]');
            if (ta) { ta.focus(); return true; }
            return false;
        })()
        """
        if b.evaluate(js_focus):
            time.sleep(0.5)
            b.send_command("Input.insertText", {"text": message})
            b.send_command("Input.dispatchKeyEvent", {"type": "keyDown", "windowsVirtualKeyCode": 13, "unmodifiedText": "\r", "text": "\r"})
            b.send_command("Input.dispatchKeyEvent", {"type": "keyUp", "windowsVirtualKeyCode": 13})
            logger.info("CDP注入に成功")
        else:
            logger.warning("CDP: 入力欄が見つからない")
    except Exception as e:
        logger.warning(f"CDP注入に失敗: {e}")


def check_github_prs():
    """puchickey/genesis の Open な PR を確認し、未報告のものを inbox に保存する。"""
    repo = "puchickey/genesis"
    url = f"https://api.github.com/repos/{repo}/pulls?state=open"

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
        import requests
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            prs = response.json()

            reported_ids = set()
            if os.path.exists(REPORTED_PRS_FILE):
                with open(REPORTED_PRS_FILE, 'r') as f:
                    reported_ids = {line.strip() for line in f if line.strip()}

            for pr in prs:
                pr_id = str(pr['id'])
                if pr_id not in reported_ids:
                    report_filename = f"jules_pr_{pr['number']}.md"
                    report_path = os.path.join(INBOX, report_filename)

                    report_content = f"""# 新しいプルリクエスト検出
- **タイトル**: {pr['title']}
- **番号**: #{pr['number']}
- **作成者**: {pr['user']['login']}
- **URL**: {pr['html_url']}
- **説明**:
{pr['body'] or '(説明なし)'}
"""
                    with open(report_path, 'w', encoding='utf-8') as f:
                        f.write(report_content)

                    logger.info(f"新規PR検出: #{pr['number']} {pr['title']}")
                    show_toast("Genesis OS / GitHub", f"新しいPR: #{pr['number']} {pr['title']}")
                    reported_ids.add(pr_id)

            with open(REPORTED_PRS_FILE, 'w') as f:
                for rid in reported_ids:
                    f.write(rid + "\n")
        elif response.status_code != 403:
            logger.warning(f"GitHub API エラー: {response.status_code}")
    except ImportError:
        logger.warning("requests モジュールが未インストール。PR監視をスキップ")
    except Exception as e:
        logger.warning(f"GitHub PR チェックに失敗: {e}")


def archive_inbox():
    """処理済みレポート（24時間以上経過）を archive/ に移動する。"""
    if not os.path.exists(INBOX_ARCHIVE):
        os.makedirs(INBOX_ARCHIVE)

    now = datetime.now()
    for filename in os.listdir(INBOX):
        filepath = os.path.join(INBOX, filename)
        if not os.path.isfile(filepath):
            continue

        # アーカイブ対象: started_*.md と task*_report.md のみ
        if not (filename.startswith("started_") or "_report.md" in filename):
            continue

        # 24時間以上経過したら移動
        mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
        if now - mtime > timedelta(hours=24):
            dest = os.path.join(INBOX_ARCHIVE, filename)
            shutil.move(filepath, dest)
            logger.info(f"アーカイブ完了: {filename}")


def run():
    logger.info("=" * 50)
    logger.info("Genesis OS Multi-Agent Coordinator v2.0 起動")
    logger.info(f"  Outbox監視 (タスクキュー): {OUTBOX}")
    logger.info(f"  Inbox監視  (結果)        : {INBOX}")
    logger.info(f"  チェック間隔: outbox/inbox={OUTBOX_INTERVAL_SEC}秒, PR={PR_CHECK_INTERVAL_SEC}秒")
    logger.info("=" * 50)

    last_pr_check = 0  # エポック秒

    while True:
        try:
            process_outbox()
            monitor_inbox()
            archive_inbox()

            # PR チェックは30分ごと
            now = time.time()
            if now - last_pr_check >= PR_CHECK_INTERVAL_SEC:
                check_github_prs()
                last_pr_check = now

            time.sleep(OUTBOX_INTERVAL_SEC)
        except Exception as e:
            logger.error(f"イベントループエラー: {e}", exc_info=True)
            time.sleep(30)


if __name__ == "__main__":
    run()
