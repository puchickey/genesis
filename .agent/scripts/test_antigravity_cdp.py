import sys
sys.path.append(r"G:\マイドライブ\Genesis_OS\.agent\scripts")
from cdp_browser import CDPBrowser

print("Testing CDP Connection to Antigravity...")
try:
    b = CDPBrowser(port=9224)
    b.connect()
    
    html = b.evaluate("document.body.innerHTML.substring(0, 500)")
    title = b.evaluate("document.title")
    
    print("===============================")
    print(f"Connection Successful!")
    print(f"Window Title: {title}")
    print("===============================")
    
except Exception as e:
    print("===============================")
    print("Connection Failed.")
    print("Error:", e)
    print("===============================")
    print("Hint: Antigravity might not be running with the correct CDP flag.")
    print("Please completely exit the Antigravity app.")
    print("Then start it via command line or modified shortcut with:")
    print("--remote-debugging-port=9224")
    print("===============================")
