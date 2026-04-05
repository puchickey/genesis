"""
note.com 自動下書き保存スクリプト v3
Genesis OS CDP Browser Operator 拡張

+メニュー操作対応版:
  - Markdown見出し(##/###)、箇条書き、引用、区切り線をProseMirrorで正しく挿入
  - <!-- toc --> で目次挿入
  - <!-- embed: URL --> でURL埋め込み
  - <!-- paywall --> で有料エリア境界線

使用方法:
  python note_poster.py <markdownファイルパス>
  python note_poster.py <markdownファイルパス> --image <画像パス>
  python note_poster.py <markdownファイルパス> --image <画像パス> --tags "タグ1,タグ2"

Markdownファイル形式:
  ---
  tags: [タグ1, タグ2]
  image: path/to/image.png
  ---
  # タイトル
  本文...

  または単純に:
  # タイトル
  本文...
"""
import sys
import os
import time
import json
import re
import urllib.request
import websocket
import argparse

# ==============================
# CDP クライアント
# ==============================
class CDP:
    def __init__(self, port=9223):
        self.port = port
        self.ws = None
        self.msg_id = 0

    def get_tabs(self):
        with urllib.request.urlopen(f"http://127.0.0.1:{self.port}/json") as r:
            return json.loads(r.read().decode('utf-8'))

    def connect_tab(self, tab):
        if self.ws:
            try: self.ws.close()
            except: pass
        self.ws = websocket.create_connection(tab["webSocketDebuggerUrl"], timeout=10)
        self.msg_id = 0
        print(f"[CDP] 接続: {tab['url'][:100]}")

    def connect_browser(self):
        with urllib.request.urlopen(f"http://127.0.0.1:{self.port}/json/version") as r:
            info = json.loads(r.read().decode('utf-8'))
        ws_url = info["webSocketDebuggerUrl"]
        if self.ws:
            try: self.ws.close()
            except: pass
        self.ws = websocket.create_connection(ws_url, timeout=10)
        self.msg_id = 0

    def send(self, method, params=None, timeout=10):
        self.msg_id += 1
        msg_id = self.msg_id
        self.ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
        self.ws.settimeout(timeout)
        try:
            while True:
                data = json.loads(self.ws.recv())
                # CDPイベントは無視してレスポンスのみ待つ
                if "id" in data and data["id"] == msg_id:
                    if "error" in data:
                        raise Exception(f"CDPエラー: {method}: {data['error'].get('message','')}")
                    return data
        except websocket.WebSocketTimeoutException:
            return None

    def send_no_raise(self, method, params=None, timeout=10):
        """エラーでも例外を投げないsend"""
        self.msg_id += 1
        msg_id = self.msg_id
        self.ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
        self.ws.settimeout(timeout)
        try:
            while True:
                data = json.loads(self.ws.recv())
                if "id" in data and data["id"] == msg_id:
                    return data
        except websocket.WebSocketTimeoutException:
            return None

    def js(self, script, timeout=10):
        res = self.send("Runtime.evaluate", {
            "expression": script, "returnByValue": True, "awaitPromise": True
        }, timeout=timeout)
        if res and "result" in res:
            val = res["result"].get("result", {})
            if val.get("type") == "undefined":
                return None
            return val.get("value")
        return None

    def native_click(self, x, y):
        """ネイティブマウスクリック（ユーザージェスチャーが必要な操作用）"""
        self.send_no_raise("Input.dispatchMouseEvent", {
            "type": "mousePressed", "x": x, "y": y,
            "button": "left", "clickCount": 1
        }, timeout=3)
        time.sleep(0.1)
        self.send_no_raise("Input.dispatchMouseEvent", {
            "type": "mouseReleased", "x": x, "y": y,
            "button": "left", "clickCount": 1
        }, timeout=3)

# ==============================
# Markdown パーサー
# ==============================
def parse_markdown(filepath):
    """Markdownファイルからタイトル・本文・メタデータを抽出"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # フロントマター解析 (簡易YAML)
    meta = {}
    body_content = content
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            # フロントマターを解析
            for line in parts[1].strip().split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    key = key.strip()
                    val = val.strip()
                    # [item1, item2] 形式のリスト
                    if val.startswith('[') and val.endswith(']'):
                        val = [v.strip().strip('"').strip("'") for v in val[1:-1].split(',')]
                    meta[key] = val
            body_content = parts[2].strip()

    lines = body_content.strip().split('\n')

    # タイトル: 最初の # 見出し
    title = ""
    body_start = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('# ') and not stripped.startswith('## '):
            title = stripped[2:].strip()
            body_start = i + 1
            break

    if not title:
        title = lines[0].strip().lstrip('#').strip()
        body_start = 1

    body_lines = lines[body_start:]
    while body_lines and not body_lines[0].strip():
        body_lines.pop(0)

    body = '\n'.join(body_lines)
    return title, body, meta

def markdown_to_blocks(body):
    """Markdownの本文をブロックタイプ付きリストに変換
    
    Returns:
        list of dict: [{"type": "paragraph", "text": "..."}, ...]
        対応タイプ: paragraph, heading2, heading3, bullet, numbered,
                    quote, hr, toc, embed, paywall, code_block
    """
    blocks = []
    current_lines = []
    current_type = "paragraph"
    
    def flush():
        nonlocal current_lines, current_type
        if current_lines:
            text = '\n'.join(current_lines)
            # インラインMarkdownを除去
            text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
            text = re.sub(r'\*(.+?)\*', r'\1', text)
            text = re.sub(r'`(.+?)`', r'\1', text)
            if current_type == "bullet":
                blocks.append({"type": "bullet", "items": current_lines[:]})
            elif current_type == "numbered":
                blocks.append({"type": "numbered", "items": current_lines[:]})
            elif current_type == "quote":
                blocks.append({"type": "quote", "text": text})
            else:
                blocks.append({"type": current_type, "text": text})
            current_lines = []
            current_type = "paragraph"
    
    for line in body.split('\n'):
        stripped = line.strip()
        
        # 空行 → flush
        if not stripped:
            flush()
            continue
        
        # 特殊コメント記法: <!-- toc -->
        toc_match = re.match(r'^<!--\s*toc\s*-->', stripped, re.IGNORECASE)
        if toc_match:
            flush()
            blocks.append({"type": "toc"})
            continue
        
        # 特殊コメント記法: <!-- embed: URL -->
        embed_match = re.match(r'^<!--\s*embed:\s*(.+?)\s*-->', stripped, re.IGNORECASE)
        if embed_match:
            flush()
            blocks.append({"type": "embed", "url": embed_match.group(1)})
            continue
        
        # 特殊コメント記法: <!-- paywall -->
        paywall_match = re.match(r'^<!--\s*paywall\s*-->', stripped, re.IGNORECASE)
        if paywall_match:
            flush()
            blocks.append({"type": "paywall"})
            continue
        
        # 区切り線: --- or ***
        if re.match(r'^(---+|\*\*\*+)$', stripped):
            flush()
            blocks.append({"type": "hr"})
            continue
        
        # 大見出し: ##
        if stripped.startswith('## ') and not stripped.startswith('### '):
            flush()
            text = stripped[3:].strip()
            blocks.append({"type": "heading2", "text": text})
            continue
        
        # 小見出し: ###
        if stripped.startswith('### '):
            flush()
            text = stripped[4:].strip()
            blocks.append({"type": "heading3", "text": text})
            continue
        
        # 箇条書き: - or *
        bullet_match = re.match(r'^[-*]\s+(.+)', stripped)
        if bullet_match:
            if current_type != "bullet":
                flush()
                current_type = "bullet"
            # インラインMarkdown除去
            item_text = bullet_match.group(1)
            item_text = re.sub(r'\*\*(.+?)\*\*', r'\1', item_text)
            item_text = re.sub(r'\*(.+?)\*', r'\1', item_text)
            item_text = re.sub(r'`(.+?)`', r'\1', item_text)
            current_lines.append(item_text)
            continue
        
        # 番号付きリスト: 1. 2. etc
        num_match = re.match(r'^\d+\.\s+(.+)', stripped)
        if num_match:
            if current_type != "numbered":
                flush()
                current_type = "numbered"
            item_text = num_match.group(1)
            item_text = re.sub(r'\*\*(.+?)\*\*', r'\1', item_text)
            item_text = re.sub(r'\*(.+?)\*', r'\1', item_text)
            item_text = re.sub(r'`(.+?)`', r'\1', item_text)
            current_lines.append(item_text)
            continue
        
        # 引用: >
        if stripped.startswith('> '):
            if current_type != "quote":
                flush()
                current_type = "quote"
            current_lines.append(stripped[2:])
            continue
        
        # 通常段落
        if current_type != "paragraph":
            flush()
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', stripped)
        text = re.sub(r'\*(.+?)\*', r'\1', text)
        text = re.sub(r'`(.+?)`', r'\1', text)
        current_lines.append(text)
    
    flush()
    return blocks

# ==============================
# note.com 操作
# ==============================
def open_new_editor(cdp):
    """新しいタブでnoteの新規投稿ページを開く"""
    print("[1] 新規投稿ページを開く...")
    cdp.connect_browser()
    result = cdp.send("Target.createTarget", {"url": "https://note.com/notes/new"})

    if not result or "result" not in result:
        raise Exception("新しいタブの作成に失敗しました")

    target_id = result["result"].get("targetId")
    print(f"  タブ作成: {target_id}")

    for attempt in range(10):
        time.sleep(3)
        tabs = cdp.get_tabs()
        for t in tabs:
            if t["type"] == "page" and "editor.note.com" in t.get("url", "") and "/edit" in t.get("url", ""):
                cdp.connect_tab(t)
                url = cdp.js("window.location.href")
                state = cdp.js("document.readyState")
                if url and "editor.note.com" in url and state == "complete":
                    print(f"  ✅ エディタ準備完了: {url}")
                    time.sleep(2)
                    return True
        print(f"  リダイレクト待ち... ({attempt+1}/10)")

    raise Exception("エディタページへの接続に失敗しました")

def input_title(cdp, title):
    """タイトル入力"""
    label = f"\"{title[:30]}...\"" if len(title) > 30 else f"\"{title}\""
    print(f"[2] タイトル入力: {label}")

    result = cdp.js(f"""
        (() => {{
            const ta = document.querySelector('textarea');
            if (!ta) return 'textarea が見つかりません';
            ta.focus();
            const nativeSetter = Object.getOwnPropertyDescriptor(
                window.HTMLTextAreaElement.prototype, 'value'
            ).set;
            nativeSetter.call(ta, {json.dumps(title)});
            ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
            ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
            return 'OK';
        }})()
    """)

    if result != 'OK':
        raise Exception(f"タイトル入力失敗: {result}")
    print(f"  ✅ タイトル入力完了")
    time.sleep(1)

# ==============================
# +メニュー操作
# ==============================
def press_enter(cdp):
    """Enterキーを送信して新しい行を作成"""
    cdp.send("Input.dispatchKeyEvent", {
        "type": "keyDown", "key": "Enter", "code": "Enter",
        "windowsVirtualKeyCode": 13, "nativeVirtualKeyCode": 13
    })
    cdp.send("Input.dispatchKeyEvent", {
        "type": "keyUp", "key": "Enter", "code": "Enter",
        "windowsVirtualKeyCode": 13, "nativeVirtualKeyCode": 13
    })
    time.sleep(0.5)

def move_cursor_to_end(cdp):
    """Ctrl+Endでカーソルをエディタ末尾に強制移動"""
    cdp.js("(() => { const pm = document.querySelector('.ProseMirror'); if (pm) pm.focus(); })()")
    time.sleep(0.2)
    cdp.send("Input.dispatchKeyEvent", {
        "type": "keyDown", "key": "End", "code": "End",
        "windowsVirtualKeyCode": 35, "nativeVirtualKeyCode": 35, "modifiers": 2
    })
    cdp.send("Input.dispatchKeyEvent", {
        "type": "keyUp", "key": "End", "code": "End",
        "windowsVirtualKeyCode": 35, "nativeVirtualKeyCode": 35, "modifiers": 2
    })
    time.sleep(0.3)

def insert_text(cdp, text):
    """ProseMirrorにテキストを挿入"""
    escaped = text.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')
    cdp.js(f"(() => {{ const pm = document.querySelector('.ProseMirror'); if (pm) pm.focus(); document.execCommand('insertText', false, '{escaped}'); }})()")
    time.sleep(0.5)

def open_plus_menu(cdp):
    """「+」メニュー（「メニューを開く」ボタン）を開く"""
    # ProseMirrorにフォーカスして+メニューボタンを表示させる
    cdp.js("(() => { const pm = document.querySelector('.ProseMirror'); if (pm) pm.focus(); })()")
    time.sleep(0.5)
    
    coords = cdp.js("""
        (() => {
            const btn = document.querySelector('[aria-label="メニューを開く"]');
            if (!btn) return null;
            const r = btn.getBoundingClientRect();
            if (r.width <= 0) return null;
            return { x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2) };
        })()
    """)
    if not coords:
        print("  [警告] +メニューボタンが見つかりません")
        return False
    
    cdp.native_click(coords['x'], coords['y'])
    time.sleep(1.5)
    return True

def click_plus_menu_item(cdp, item_text):
    """「+」メニューから指定項目をクリック"""
    if not open_plus_menu(cdp):
        return False
    
    # メニュー項目のボタンを探してクリック
    item_coords = cdp.js(f"""
        (() => {{
            const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
            while (walker.nextNode()) {{
                const el = walker.currentNode;
                if (el.tagName !== 'BUTTON') continue;
                const directText = Array.from(el.childNodes)
                    .filter(n => n.nodeType === 3 || n.tagName === 'DIV' || n.tagName === 'SPAN')
                    .map(n => n.textContent?.trim()).join('');
                if (directText === '{item_text}' || el.textContent?.trim() === '{item_text}') {{
                    const r = el.getBoundingClientRect();
                    if (r.width > 0) return {{ x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2) }};
                }}
            }}
            return null;
        }})()
    """)
    
    if not item_coords:
        print(f"  [警告] メニュー項目「{item_text}」が見つかりません")
        return False
    
    cdp.native_click(item_coords['x'], item_coords['y'])
    time.sleep(1.5)
    return True

def insert_embed(cdp, url):
    """URL埋め込みを挿入（+メニュー経由）"""
    print(f"  → 埋め込み挿入: {url[:60]}")
    
    # 埋め込みは前のブロック（目次等）のあとカーソルが特殊位置にいることがある
    # Ctrl+End→Enterで確実に空行を作成してからメニューを開く
    cdp.js("(() => { const pm = document.querySelector('.ProseMirror'); if (pm) pm.focus(); })()")
    time.sleep(0.3)
    cdp.send("Input.dispatchKeyEvent", {
        "type": "keyDown", "key": "End", "code": "End",
        "windowsVirtualKeyCode": 35, "nativeVirtualKeyCode": 35, "modifiers": 2
    })
    cdp.send("Input.dispatchKeyEvent", {
        "type": "keyUp", "key": "End", "code": "End",
        "windowsVirtualKeyCode": 35, "nativeVirtualKeyCode": 35, "modifiers": 2
    })
    time.sleep(0.3)
    press_enter(cdp)
    time.sleep(0.5)
    
    if not click_plus_menu_item(cdp, '埋め込み'):
        print("  [警告] 埋め込みメニューの操作に失敗")
        return False
    
    # 埋め込みURL入力欄（textarea）を検出（リトライ付き）
    for attempt in range(8):
        time.sleep(1)
        result = cdp.js(f"""
            (() => {{
                // 方法1: ProseMirror内のtextarea（埋め込みウィジェット内）
                let ta = document.querySelector('.ProseMirror textarea');
                // 方法2: placeholder で検索
                if (!ta) ta = document.querySelector('textarea[placeholder="https://example.com"]');
                // 方法3: name="alt" で検索  
                if (!ta) ta = document.querySelector('textarea[name="alt"]');
                // 方法4: アクティブ要素がtextareaならそれを使う
                if (!ta && document.activeElement?.tagName === 'TEXTAREA') ta = document.activeElement;
                // 方法5: figure内のtextarea
                if (!ta) ta = document.querySelector('figure textarea');
                
                if (!ta) return 'textarea見つからず';
                
                // textareaにフォーカスしてURL入力
                ta.focus();
                ta.value = '';
                const nativeSetter = Object.getOwnPropertyDescriptor(
                    window.HTMLTextAreaElement.prototype, 'value'
                ).set;
                nativeSetter.call(ta, {json.dumps(url)});
                ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
                ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
                return 'OK';
            }})()
        """)
        if result == 'OK':
            break
        if attempt < 7:
            print(f"  リトライ ({attempt+1}/8): {result}")
    
    if result != 'OK':
        print(f"  [警告] URL入力失敗: {result}")
        return False
    
    time.sleep(0.5)
    
    # 「適用」ボタンをクリックしてURL確定（Enterではなくボタンクリック）
    apply_result = cdp.js("""
        (() => {
            // 「適用」ボタンを探す
            const btns = Array.from(document.querySelectorAll('button'));
            const apply = btns.find(b => b.textContent?.trim() === '適用');
            if (apply) {
                apply.click();
                return 'OK';
            }
            // フォールバック: ProseMirror内の小さなボタン
            const pmBtns = Array.from(document.querySelectorAll('.ProseMirror button'));
            for (const btn of pmBtns) {
                const text = btn.textContent?.trim();
                if (text === '適用' || text === 'Apply' || text === 'OK') {
                    btn.click();
                    return 'OK (PM内)';
                }
            }
            return '適用ボタンなし';
        })()
    """)
    
    if apply_result and 'OK' in apply_result:
        time.sleep(3)  # 埋め込みの読み込み待ち
        print(f"  ✅ 埋め込み完了")
        return True
    else:
        # フォールバック: Enterで確定を試みる
        print(f"  [Info] 適用ボタン: {apply_result}。Enterで確定を試行...")
        cdp.send("Input.dispatchKeyEvent", {
            "type": "keyDown", "key": "Enter", "code": "Enter",
            "windowsVirtualKeyCode": 13, "nativeVirtualKeyCode": 13
        })
        cdp.send("Input.dispatchKeyEvent", {
            "type": "keyUp", "key": "Enter", "code": "Enter",
            "windowsVirtualKeyCode": 13, "nativeVirtualKeyCode": 13
        })
        time.sleep(3)
        print(f"  ✅ 埋め込み完了（Enter確定）")
        return True

def insert_toc(cdp):
    """目次を挿入（+メニュー経由）"""
    print(f"  → 目次挿入")
    if click_plus_menu_item(cdp, '目次'):
        time.sleep(1)
        print(f"  ✅ 目次挿入完了")
        return True
    return False

def insert_paywall(cdp):
    """有料エリア境界線を挿入（+メニュー経由）"""
    print(f"  → 有料エリア挿入")
    if click_plus_menu_item(cdp, '有料エリア指定'):
        time.sleep(1)
        print(f"  ✅ 有料エリア挿入完了")
        return True
    return False

def insert_hr_via_menu(cdp):
    """区切り線を挿入（+メニュー経由）"""
    print(f"  → 区切り線挿入")
    if click_plus_menu_item(cdp, '区切り線'):
        time.sleep(0.5)
        print(f"  ✅ 区切り線挿入完了")
        return True
    return False

def insert_heading(cdp, level, text):
    """見出しを挿入（+メニュー経由）"""
    item_text = '大見出し' if level == 2 else '小見出し'
    print(f"  → {item_text}: {text[:40]}")
    if not click_plus_menu_item(cdp, item_text):
        # フォールバック: テキストとして挿入
        insert_text(cdp, text)
        return False
    
    time.sleep(0.3)
    insert_text(cdp, text)
    print(f"  ✅ {item_text}挿入完了")
    return True

def insert_quote(cdp, text):
    """引用を挿入（+メニュー経由）"""
    print(f"  → 引用: {text[:40]}")
    if not click_plus_menu_item(cdp, '引用'):
        insert_text(cdp, text)
        return False
    
    time.sleep(0.3)
    insert_text(cdp, text)
    print(f"  ✅ 引用挿入完了")
    return True

def insert_list(cdp, items, list_type='bullet'):
    """箇条書き/番号付きリストを挿入（+メニュー経由）"""
    item_text = '箇条書きリスト' if list_type == 'bullet' else '番号付きリスト'
    print(f"  → {item_text}: {len(items)}項目")
    if not click_plus_menu_item(cdp, item_text):
        # フォールバック
        for item in items:
            insert_text(cdp, item)
            press_enter(cdp)
        return False
    
    time.sleep(0.3)
    for i, item in enumerate(items):
        insert_text(cdp, item)
        if i < len(items) - 1:
            press_enter(cdp)
    
    # リストモードを抜けるためにEnter2回
    press_enter(cdp)
    press_enter(cdp)
    print(f"  ✅ {item_text}挿入完了")
    return True

# ==============================
# 本文入力（ブロックタイプ対応）
# ==============================
def input_body(cdp, blocks):
    """本文入力（ブロックタイプ対応版）"""
    print(f"[3] 本文入力: {len(blocks)}ブロック...")

    cdp.js("(() => { const pm = document.querySelector('.ProseMirror'); if (pm) pm.focus(); })()")
    time.sleep(0.5)
    cdp.js("(() => { const pm = document.querySelector('.ProseMirror'); if (!pm) return; pm.focus(); document.execCommand('selectAll'); document.execCommand('delete'); })()")
    time.sleep(0.5)

    for i, block in enumerate(blocks):
        btype = block["type"]
        
        # ★ 毎ブロック挿入前にカーソルを末尾に移動（順序崩れ防止）
        if i > 0:
            move_cursor_to_end(cdp)
        
        # ブロック間に新しい行を作成（最初のブロック以外）
        # +メニュー経由の操作（hr, toc, embed等）は自前でEnterを処理するのでスキップ
        if i > 0 and btype in ('paragraph', 'heading2', 'heading3', 'quote'):
            press_enter(cdp)
        
        if btype == "paragraph":
            insert_text(cdp, block["text"])
        
        elif btype == "heading2":
            insert_heading(cdp, 2, block["text"])
        
        elif btype == "heading3":
            insert_heading(cdp, 3, block["text"])
        
        elif btype == "bullet":
            insert_list(cdp, block["items"], 'bullet')
        
        elif btype == "numbered":
            insert_list(cdp, block["items"], 'numbered')
        
        elif btype == "quote":
            insert_quote(cdp, block["text"])
        
        elif btype == "hr":
            insert_hr_via_menu(cdp)
        
        elif btype == "toc":
            insert_toc(cdp)
        
        elif btype == "embed":
            insert_embed(cdp, block["url"])
        
        elif btype == "paywall":
            insert_paywall(cdp)
        
        else:
            print(f"  [警告] 未知のブロックタイプ: {btype}")
            if "text" in block:
                insert_text(cdp, block["text"])
        
        if (i + 1) % 5 == 0:
            print(f"  {i+1}/{len(blocks)} ブロック入力済み...")

    print(f"  ✅ 本文入力完了 ({len(blocks)}ブロック)")
    time.sleep(1)

def upload_cover_image(cdp, image_path):
    """トップ画像（見出し画像）をアップロード"""
    print(f"[4] トップ画像アップロード...")

    abs_path = os.path.abspath(image_path)
    if not os.path.exists(abs_path):
        raise Exception(f"画像ファイルが見つかりません: {abs_path}")
    print(f"  画像: {abs_path}")

    # Step A: 「画像を追加」ボタンをネイティブクリック → メニュー表示
    coords = cdp.js("""
        (() => {
            const btn = document.querySelector('[aria-label="画像を追加"]');
            if (!btn) return null;
            const r = btn.getBoundingClientRect();
            return { x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2) };
        })()
    """)
    if not coords:
        raise Exception("「画像を追加」ボタンが見つかりません")

    cdp.native_click(coords['x'], coords['y'])
    time.sleep(2)

    # Step B: メニューから「画像をアップロード」の座標を取得してクリック
    upload_coords = cdp.js("""
        (() => {
            const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
            while (walker.nextNode()) {
                const el = walker.currentNode;
                const directText = Array.from(el.childNodes)
                    .filter(n => n.nodeType === 3)
                    .map(n => n.textContent.trim()).join('');
                if (directText === '画像をアップロード') {
                    let target = el;
                    while (target && !['BUTTON','A','LI'].includes(target.tagName) && target.getAttribute?.('role') !== 'menuitem') {
                        target = target.parentElement;
                    }
                    if (!target) target = el;
                    const r = target.getBoundingClientRect();
                    if (r.width > 0) return { x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2) };
                }
            }
            return null;
        })()
    """)

    if not upload_coords:
        raise Exception("「画像をアップロード」メニュー項目が見つかりません")

    cdp.native_click(upload_coords['x'], upload_coords['y'])
    time.sleep(2)

    # Step C: input#note-editor-eyecatch-input にファイルを設定
    fi_check = cdp.js("!!document.querySelector('#note-editor-eyecatch-input, input[type=\"file\"]')")
    if not fi_check:
        # リトライ: もう一度少し待つ
        time.sleep(2)
        fi_check = cdp.js("!!document.querySelector('#note-editor-eyecatch-input, input[type=\"file\"]')")

    if not fi_check:
        raise Exception("ファイル入力要素が出現しませんでした")

    cdp.send("DOM.enable")
    doc = cdp.send("DOM.getDocument")
    root_id = doc["result"]["root"]["nodeId"]
    q = cdp.send("DOM.querySelector", {
        "nodeId": root_id,
        "selector": '#note-editor-eyecatch-input, input[type="file"]'
    })
    node_id = q["result"]["nodeId"]

    if node_id == 0:
        raise Exception("ファイル入力要素のnodeIdが取得できません")

    cdp.send("DOM.setFileInputFiles", {"nodeId": node_id, "files": [abs_path]})
    print(f"  ✅ 画像ファイル設定成功")

    # Step D: クロップダイアログの「保存」ボタンを待ってクリック
    print(f"  クロップダイアログ待ち...")
    for attempt in range(10):
        time.sleep(1)
        save_found = cdp.js("""
            (() => {
                const btns = Array.from(document.querySelectorAll('button'));
                return btns.some(b => b.textContent?.trim() === '保存' && b.offsetParent !== null);
            })()
        """)
        if save_found:
            break

    save_result = cdp.js("""
        (() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const save = btns.find(b => b.textContent?.trim() === '保存');
            if (!save) return '保存ボタンなし';
            save.click();
            return 'OK';
        })()
    """)

    if save_result != 'OK':
        raise Exception(f"クロップ保存失敗: {save_result}")

    # アップロード処理待ち
    time.sleep(5)
    print(f"  ✅ トップ画像アップロード完了")

def input_hashtags(cdp, tags):
    """ハッシュタグを入力（公開設定画面に遷移）"""
    if not tags:
        return

    print(f"[5] ハッシュタグ入力: {tags}...")

    # 「公開に進む」ボタンをクリック → /publish/ に遷移
    cdp.js("""
        (() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const pub = btns.find(b => b.textContent?.trim()?.includes('公開に進む'));
            if (pub) pub.click();
        })()
    """)
    time.sleep(3)

    # /publish/ ページの読み込み確認
    for attempt in range(10):
        url = cdp.js("window.location.href")
        if url and "/publish/" in url:
            break
        time.sleep(1)

    # ハッシュタグ入力欄にフォーカス
    for tag in tags:
        tag = tag.strip()
        if not tag:
            continue

        # input にフォーカスしてテキスト入力
        cdp.js(f"""
            (() => {{
                const input = document.querySelector('input[placeholder="ハッシュタグを追加する"]');
                if (!input) return;
                input.focus();
                const nativeSetter = Object.getOwnPropertyDescriptor(
                    window.HTMLInputElement.prototype, 'value'
                ).set;
                nativeSetter.call(input, {json.dumps(tag)});
                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                input.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }})()
        """)
        time.sleep(0.5)

        # Enterキーで確定
        cdp.send("Input.dispatchKeyEvent", {
            "type": "keyDown", "key": "Enter", "code": "Enter",
            "windowsVirtualKeyCode": 13, "nativeVirtualKeyCode": 13
        })
        cdp.send("Input.dispatchKeyEvent", {
            "type": "keyUp", "key": "Enter", "code": "Enter",
            "windowsVirtualKeyCode": 13, "nativeVirtualKeyCode": 13
        })
        time.sleep(1)
        print(f"  ✅ タグ追加: #{tag}")

    # エディタに戻る（ブラウザバック）
    cdp.js("window.history.back()")
    time.sleep(3)
    print(f"  ✅ ハッシュタグ入力完了")

def save_draft(cdp):
    """下書き保存"""
    print("[6] 下書き保存...")
    result = cdp.js("""
        (() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const draft = btns.find(b => b.textContent?.trim() === '下書き保存');
            if (!draft) return '下書き保存ボタンが見つかりません';
            draft.click();
            return 'OK';
        })()
    """)

    if result != 'OK':
        raise Exception(f"下書き保存失敗: {result}")
    time.sleep(3)
    print(f"  ✅ 下書き保存完了")

# ==============================
# メイン
# ==============================
def main():
    parser = argparse.ArgumentParser(description='note.com 自動投稿スクリプト v2')
    parser.add_argument('markdown_file', help='投稿するMarkdownファイルのパス')
    parser.add_argument('--image', help='トップ画像のファイルパス')
    parser.add_argument('--tags', help='ハッシュタグ（カンマ区切り）例: "AI,自動化,Genesis"')
    parser.add_argument('--publish', action='store_true', help='公開まで実行（未実装）')
    args = parser.parse_args()

    if not os.path.exists(args.markdown_file):
        print(f"[エラー] ファイルが見つかりません: {args.markdown_file}")
        sys.exit(1)

    # Markdown解析
    title, body, meta = parse_markdown(args.markdown_file)
    blocks = markdown_to_blocks(body)

    # メタデータとCLI引数のマージ（CLI引数優先）
    image_path = args.image or meta.get('image')
    tags = args.tags.split(',') if args.tags else meta.get('tags', [])

    # ブロックタイプの集計
    block_types = {}
    for b in blocks:
        block_types[b['type']] = block_types.get(b['type'], 0) + 1
    
    print(f"\n{'='*50}")
    print(f"📝 note.com 自動投稿 v3")
    print(f"{'='*50}")
    print(f"  ファイル: {args.markdown_file}")
    print(f"  タイトル: {title}")
    print(f"  ブロック数: {len(blocks)}")
    print(f"  ブロック内訳: {block_types}")
    print(f"  トップ画像: {image_path or 'なし'}")
    print(f"  ハッシュタグ: {tags or 'なし'}")
    print(f"  モード: {'公開' if args.publish else '下書き保存'}")
    print()

    if not title:
        print("[エラー] タイトルが空です"); sys.exit(1)
    if not blocks:
        print("[エラー] 本文が空です"); sys.exit(1)

    cdp = CDP()

    try:
        # 1. 新規投稿ページ
        open_new_editor(cdp)

        # 2. トップ画像（タイトル・本文より先に設定）
        if image_path:
            upload_cover_image(cdp, image_path)

        # 3. タイトル入力
        input_title(cdp, title)

        # 4. 本文入力
        input_body(cdp, blocks)

        # 5. 下書き保存
        save_draft(cdp)

        # 6. ハッシュタグ（公開時のみ。下書き保存では公開設定画面のタグは保持されない）
        if tags and args.publish:
            input_hashtags(cdp, tags)
            # 公開フロー（未実装：手動確認を推奨）
            print("[注意] --publish の自動公開は未実装です。手動で公開してください。")
        elif tags:
            print(f"[Info] ハッシュタグ {tags} は公開時に設定されます（下書きでは保持されないためスキップ）")

        # 結果
        url = cdp.js("window.location.href")
        print(f"\n{'='*50}")
        print(f"✅ 下書き保存が完了しました")
        print(f"  URL: {url}")
        if tags:
            print(f"  ※ タグは公開時に設定してください: {', '.join(tags)}")
        print(f"{'='*50}")

    except Exception as e:
        print(f"\n[エラー] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
