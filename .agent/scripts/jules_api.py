"""
Jules REST API ヘルパースクリプト
================================
Jules APIを使用してセッション作成・監視を行う。
automationMode: AUTO_CREATE_PR により、手動Publish不要で自動PR作成。

使い方:
  python jules_api.py create --repo puchickey/genesis --prompt "タスク内容"
  python jules_api.py create --repo puchickey/genesis --file JULES_TASK.md
  python jules_api.py status --session SESSION_NAME
  python jules_api.py sources
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
from pathlib import Path

BASE_URL = "https://jules.googleapis.com/v1alpha"


def get_api_key():
    """環境変数からAPIキーを取得"""
    key = os.environ.get("JULES_API_KEY")
    if not key:
        print("エラー: 環境変数 JULES_API_KEY が設定されていません。")
        print("設定方法: $env:JULES_API_KEY = 'YOUR_KEY'")
        sys.exit(1)
    return key


def api_request(method, endpoint, data=None):
    """Jules APIにリクエストを送信"""
    url = f"{BASE_URL}/{endpoint}"
    headers = {
        "x-goog-api-key": get_api_key(),
        "Content-Type": "application/json",
    }

    if data:
        body = json.dumps(data).encode("utf-8")
    else:
        body = None

    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"APIエラー: {e.code}")
        print(error_body)
        sys.exit(1)


def list_sources():
    """利用可能なリポジトリ一覧を表示"""
    result = api_request("GET", "sources")
    print("=== 利用可能なリポジトリ ===")
    for source in result.get("sources", []):
        repo = source.get("githubRepo", {})
        owner = repo.get("owner", "?")
        name = repo.get("repo", "?")
        default_branch = repo.get("defaultBranch", {}).get("displayName", "?")
        private = "🔒" if repo.get("isPrivate") else "🌐"
        print(f"  {private} {owner}/{name} (branch: {default_branch})")
        print(f"     source: {source['name']}")


def create_session(repo, prompt, title=None, branch=None):
    """
    セッション作成（AUTO_CREATE_PR + requirePlanApproval: false）
    
    Args:
        repo: "owner/repo" 形式 (例: "puchickey/genesis")
        prompt: タスクの指示内容
        title: セッションのタイトル（省略可）
        branch: 開始ブランチ（省略時はデフォルトブランチ）
    """
    owner, repo_name = repo.split("/")
    source_name = f"sources/github/{owner}/{repo_name}"

    # ブランチが指定されていない場合、sourcesから取得
    if not branch:
        sources = api_request("GET", "sources")
        for s in sources.get("sources", []):
            if s["name"] == source_name:
                branch = s.get("githubRepo", {}).get("defaultBranch", {}).get("displayName", "main")
                break
        if not branch:
            branch = "main"

    payload = {
        "prompt": prompt,
        "sourceContext": {
            "source": source_name,
            "githubRepoContext": {
                "startingBranch": branch,
            },
        },
        "automationMode": "AUTO_CREATE_PR",
        "requirePlanApproval": False,
    }

    if title:
        payload["title"] = title

    print(f"セッション作成中...")
    print(f"  リポジトリ: {repo} (branch: {branch})")
    print(f"  自動PR作成: 有効")
    print(f"  プラン承認: スキップ")

    result = api_request("POST", "sessions", payload)

    session_name = result.get("name", "不明")
    status = result.get("state", "不明")

    print(f"\n✅ セッション作成完了")
    print(f"  セッション名: {session_name}")
    print(f"  ステータス: {status}")
    print(f"  タイトル: {result.get('title', 'N/A')}")

    return result


def get_session_status(session_name):
    """セッションのステータスを確認"""
    result = api_request("GET", session_name)

    state = result.get("state", "不明")
    title = result.get("title", "N/A")
    pr_url = result.get("pullRequestUrl", None)

    print(f"=== セッションステータス ===")
    print(f"  名前: {session_name}")
    print(f"  タイトル: {title}")
    print(f"  状態: {state}")

    if pr_url:
        print(f"  PR URL: {pr_url}")

    return result


def main():
    parser = argparse.ArgumentParser(description="Jules REST API ヘルパー")
    subparsers = parser.add_subparsers(dest="command", help="コマンド")

    # sources コマンド
    subparsers.add_parser("sources", help="利用可能なリポジトリ一覧")

    # create コマンド
    create_parser = subparsers.add_parser("create", help="セッション作成")
    create_parser.add_argument("--repo", required=True, help="リポジトリ (owner/repo)")
    create_parser.add_argument("--prompt", help="タスクの指示内容（テキスト）")
    create_parser.add_argument("--file", help="タスクの指示ファイル（.md）")
    create_parser.add_argument("--title", help="セッションのタイトル")
    create_parser.add_argument("--branch", help="開始ブランチ")

    # status コマンド
    status_parser = subparsers.add_parser("status", help="セッションステータス確認")
    status_parser.add_argument("--session", required=True, help="セッション名")

    args = parser.parse_args()

    if args.command == "sources":
        list_sources()
    elif args.command == "create":
        if args.file:
            prompt = Path(args.file).read_text(encoding="utf-8")
        elif args.prompt:
            prompt = args.prompt
        else:
            print("エラー: --prompt または --file を指定してください。")
            sys.exit(1)
        create_session(args.repo, prompt, title=args.title, branch=args.branch)
    elif args.command == "status":
        get_session_status(args.session)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
