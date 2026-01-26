import os
import subprocess
import datetime
import sys

# Genesis OS Location - Lightweight Sync
TARGET_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(TARGET_DIR, "sync_log.txt")

def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding='utf-8') as f:
        f.write(f"[{timestamp}] {message}\n")

def run_command(command):
    try:
        # Run silently (no window)
        subprocess.run(
            command, 
            cwd=TARGET_DIR, 
            check=True, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
        )
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    # 1. Check for Git
    if not os.path.exists(os.path.join(TARGET_DIR, ".git")):
        log("Error: Not a git repository. Run 'git init' first.")
        return

    # 2. Add & Check Status
    run_command(["git", "add", "."])
    
    # Check if there are changes
    status = subprocess.run(
        ["git", "status", "--porcelain"], 
        cwd=TARGET_DIR, 
        capture_output=True, 
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
    )
    
    if not status.stdout.strip():
        # No changes, exit silently
        return

    # 3. Commit
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"Auto-Sync: {timestamp}"
    if run_command(["git", "commit", "-m", commit_msg]):
        # 4. Push
        if run_command(["git", "push", "origin", "main"]):
            log("Sync Successful")
        else:
            log("Push Failed (Check Network/Auth)")
    else:
        log("Commit Failed")

if __name__ == "__main__":
    main()
