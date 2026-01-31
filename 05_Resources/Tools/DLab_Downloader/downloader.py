import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from getpass import getpass

# Settings
BASE_DIR = r"g:\マイドライブ\Genesis_OS\05_Resources"
INBOX_DIR = os.path.join(BASE_DIR, "Inbox")
LOG_FILE = "download_log.txt"

# Fix PermissionError: Force webdriver_manager to use local directory
os.environ['WDM_LOCAL'] = '1'
os.environ['WDM_SSL_VERIFY'] = '0' # Sometimes SSL fails in corporate networks

def setup_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Comment out for visual debugging
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,720")
    # Output logs to suppress console noise
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    
    # Suppress SSL Warnings
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def login(driver):
    print("🔑 Login Process Initiated...")
    # Corrected URL based on search
    target_url = "https://daigovideolab.jp/login" 
    # Fallback to general top page if specific login page differs, 
    # but search suggests daigovideolab.jp
    driver.get(target_url)
    
    # Check if already logged in (cookies) or wait for user
    print("👉 Please login manually in the browser window if needed.")
    print("   (Reason: Handling CAPTCHA/MFA automatically is risky)")
    input("Press Enter here AFTER you have successfully logged in...")
    print("✅ Login confirmed (by user).")

def download_video(driver, url):
    print(f"🔍 Accessing: {url}")
    driver.get(url)
    time.sleep(3) # Wait for load

    # Try to find video tag (Recursive for Iframes)
    video_src = find_video_recursive(driver)
    
    if not video_src:
        print(f"⚠️ No <video> tag found on {url}")
        # Debug: Save page source
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("   (Saved page source to debug_page.html for analysis)")
        return False

    print(f"🎬 Found Video Source: {video_src[:50]}...")
    
    # Generate Filename
    title = driver.title.replace("|", "").replace(":", "").strip() or "video"
    filename = f"{title}.mp4"
    save_path = os.path.join(INBOX_DIR, filename)
    
    # Download Strategy
    if ".m3u8" in video_src:
        print("🌊 HLS Stream detected. Using FFMPEG...")
        download_hls(video_src, save_path)
    else:
        print("📦 Direct File detected. Using Requests...")
        download_direct(video_src, save_path)
    
    return True

def find_video_recursive(driver):
    # 1. Check current context
    try:
        vid = driver.find_element(By.TAG_NAME, "video")
        src = vid.get_attribute("src")
        if src: return src
    except:
        pass
        
    # 2. Check Iframes
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    for i, frame in enumerate(iframes):
        try:
            driver.switch_to.frame(frame)
            # Recursively check
            src = find_video_recursive(driver)
            if src: return src
            driver.switch_to.parent_frame()
        except:
            driver.switch_to.default_content()
    return None

def download_hls(url, save_path):
    import subprocess
    # ffmpeg -i "url" -c copy -bsf:a aac_adtstoasc "out.mp4"
    cmd = f'ffmpeg -y -i "{url}" -c copy -bsf:a aac_adtstoasc "{save_path}"'
    print(f"Exec: {cmd}")
    subprocess.call(cmd, shell=True)
    print(f"✅ Download Complete: {save_path}")

def download_direct(url, save_path):
    print(f"⬇️ Downloading to: {save_path}")
    response = requests.get(url, stream=True)
    with open(save_path, 'wb') as file:
        for data in response.iter_content(chunk_size=1024):
            file.write(data)
    print(f"✅ Download Complete: {save_path}")

def usage_video(tags):
    return len(tags) > 0

def main():
    print("🤖 Genesis D-Lab Downloader v1.0")
    
    # Ensure Inbox exists
    os.makedirs(INBOX_DIR, exist_ok=True)

    driver = setup_driver()
    
    try:
        login(driver)
        
        while True:
            print("\n--- Menu ---")
            print("1. Download Single Video (Paste URL)")
            print("2. Navigate browser manually & Download current page")
            print("q. Quit")
            choice = input("Select > ")
            
            if choice == '1':
                url = input("URL: ")
                download_video(driver, url)
            elif choice == '2':
                print("👉 Use the browser to navigate to the video page.")
                input("Press Enter when the video page is ready...")
                download_video(driver, driver.current_url)
            elif choice == 'q':
                break
            
    except Exception as e:
        print(f"❌ Fatal Error: {e}")
    finally:
        driver.quit()
        print("👋 Driver closed.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\n❌ Critical Error: {e}")
    finally:
        input("\nPress Enter to exit...")
