import urllib.request
import json
import websocket
# Requires: pip install websocket-client

class CDPBrowser:
    def __init__(self, port=9223):
        self.port = port
        self.ws = None
        self.message_id = 0

    def connect(self):
        url = f"http://127.0.0.1:{self.port}/json"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                tabs = json.loads(response.read().decode('utf-8'))
        except urllib.error.URLError:
            raise Exception(f"Cannot connect to Edge on port {self.port}. Ensure Edge is running with --remote-debugging-port={self.port}")
            
        page_tab = next((t for t in tabs if t["type"] == "page" and not t["url"].startswith("devtools://")), None)
        if not page_tab:
            raise Exception("No active web page tab found in Edge.")
            
        ws_url = page_tab["webSocketDebuggerUrl"]
        self.ws = websocket.create_connection(ws_url)
        print(f"[CDP] Successfully connected to Edge -> {page_tab['url']}")

    def send_command(self, method, params=None):
        self.message_id += 1
        payload = {
            "id": self.message_id,
            "method": method,
            "params": params or {}
        }
        self.ws.send(json.dumps(payload))
        while True:
            res = json.loads(self.ws.recv())
            # Usually receives events too, ignore them, wait for corresponding id
            if "id" in res and res["id"] == self.message_id:
                if "error" in res:
                    print(f"[CDP Error] Command {method} failed: {res['error']}")
                return res

    def navigate(self, url):
        return self.send_command("Page.navigate", {"url": url})
        
    def evaluate(self, script):
        """Executes JavaScript on the page and returns the result."""
        res = self.send_command("Runtime.evaluate", {
            "expression": script, 
            "returnByValue": True,
            "awaitPromise": True
        })
        if "result" in res:
            return res["result"].get("result", {}).get("value")
        return None

if __name__ == "__main__":
    print("CDPBrowser Library Context Loaded.")
