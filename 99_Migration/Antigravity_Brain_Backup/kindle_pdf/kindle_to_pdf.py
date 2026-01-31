import sys
import time
import os
import json
import shutil
import subprocess

# Try to import required packages
try:
    import pyautogui
    import img2pdf
    import pygetwindow as gw
    from PIL import Image
except ImportError as e:
    print("必要なライブラリが見つかりません。")
    print("pip install pyautogui img2pdf pygetwindow pillow")
    sys.exit(1)

CONFIG_FILE = "kindle_config.json"

# Mouse to top-left corner will trigger FailSafeException
pyautogui.FAILSAFE = True

def load_config():
    default_config = {
        "pages": 100,
        "margins": {
            "top": 120,    
            "bottom": 80,  
            "left": 50,    
            "right": 50    
        },
        "delay": 0.5,
        "direction": "right" # 'right' or 'left'
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                cf = json.load(f)
                # Migration for old config
                if "direction" not in cf:
                    cf["direction"] = "right"
                return cf
        except:
            return default_config
    return default_config

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
    print("設定を保存しました。")

def find_kindle_window():
    try:
        windows = gw.getWindowsWithTitle('Kindle')
        if windows:
            return windows[0]
    except:
        pass
    return None

def get_capture_region(window, margins):
    x = window.left + margins['left']
    y = window.top + margins['top']
    w = window.width - (margins['left'] + margins['right'])
    # Sanity check
    if w < 0: w = 100
    h = window.height - (margins['top'] + margins['bottom'])
    if h < 0: h = 100
    return (x, y, w, h)

def coordinate_checker(win):
    print("\n=== 座標・マージン計測モード ===")
    print("1. マウスを測りたい場所に置いてください。")
    print("2. その状態で 'Enter' キーを押すと、現在の座標とマージンを表示します。")
    print("3. 'q' を入力して Enter で終了します。")
    print("-------------------------------------------------------")
    
    # Activate Kindle window just for context, but keep terminal focused for input?
    # Actually user needs to click on Kindle to measure, but then alt-tab back to terminal?
    # No, pyautogui.position() works globally.
    
    while True:
        try:
            cmd = input("\n[Enter]で計測 / [q]終了 > ")
            if cmd.strip().lower() == 'q':
                break
                
            mx, my = pyautogui.position()
            
            # Relative coords
            rel_x = mx - win.left
            rel_y = my - win.top
            
            right_margin = win.width - rel_x
            bottom_margin = win.height - rel_y

            print(f"  Mouse: ({mx}, {my})")
            print(f"  >> もしここが左上(Top-Left)なら : left={rel_x}, top={rel_y}")
            print(f"  >> もしここが右下(Btm-Right)なら: right={right_margin}, bottom={bottom_margin}")
            
        except KeyboardInterrupt:
            break
    print("計測モードを終了します。")

def main():
    print("=== Kindle for PC 専用 PDF化ツール v3 ===")
    
    # 1. Init
    config = load_config()
    
    # 2. Find Window
    print("Kindleのウィンドウを探しています...")
    win = find_kindle_window()
    if not win:
        print("エラー: 'Kindle' という名前のウィンドウが見つかりません。")
        print("アプリを起動してください。")
        input("Enterキーで終了...")
        return

    print(f"発見: '{win.title}'")
    
    # Attempt activation
    try:
        if win.isMinimized:
            win.restore()
        win.activate()
    except:
        pass
    
    time.sleep(1)

    while True:
        pages = config['pages']
        margins = config['margins']
        delay = config['delay']
        direction = config.get('direction', 'right')
        
        region = get_capture_region(win, margins)
        
        print("\n--- メインメニュー ---")
        print(f"1. ページ数     : {pages}")
        print(f"2. マージン設定 : 上{margins['top']} 下{margins['bottom']} 左{margins['left']} 右{margins['right']}")
        print(f"   -> 撮影サイズ: W={region[2]}, H={region[3]}")
        print(f"3. 待機時間     : {delay}秒")
        print(f"4. めくり方向   : {'進む(→)' if direction == 'right' else '戻る(←)'} (現在: {direction})")
        print("------------------")
        print("[Enter] 撮影開始")
        print("[c]     設定変更")
        print("[m]     座標・マージン計測ツール")
        print("[q]     終了")
        
        choice = input("選択: ").strip().lower()
        
        if choice == 'q':
            return
            
        elif choice == 'm':
            coordinate_checker(win)
            
        elif choice == 'c':
            print("\n変更したい項目:")
            print("p: ページ数")
            print("m: マージン数値を入力")
            print("d: 待機時間")
            print("k: めくり方向 (← / →)")
            sub = input("> ").strip().lower()
            
            if sub == 'p':
                try:
                    p = int(input(f"ページ数 (現在 {pages}): "))
                    config['pages'] = p
                except ValueError: pass
                
            elif sub == 'd':
                try:
                    d = float(input(f"待機時間 (現在 {delay}): "))
                    config['delay'] = d
                except ValueError: pass
            
            elif sub == 'k':
                print("めくり方向を選択してください:")
                print("1: 右へ進む (→) [通常]")
                print("2: 左へ進む (←) [縦書き本などで逆の場合]")
                k_sel = input("> ").strip()
                if k_sel == '1': config['direction'] = 'right'
                elif k_sel == '2': config['direction'] = 'left'
                
            elif sub == 'm':
                print("値を入力してください (Enterで変更なし)")
                for key in ['top', 'bottom', 'left', 'right']:
                    val = input(f"{key} (現在 {margins[key]}): ")
                    if val.strip():
                        try:
                            config['margins'][key] = int(val)
                        except ValueError: pass
            
            save_config(config)
            
        else:
            # START
            break

    # Start Capture
    print("\n3秒後に開始します。")
    print("【重要】動作を緊急停止するには、マウスカーソルを画面の『左上隅』にぶつけてください。")
    print("マウス操作厳禁！...")
    time.sleep(3)
    
    # Re-activate just in case
    try:
        if win.isMinimized:
            win.restore()
        win.activate()
        # Ensure focus by clicking safely in the margin (top-left margin area)
        # This prevents clicking a link but gives focus
        safe_x = win.left + 10
        safe_y = win.top + 10
        pyautogui.click(safe_x, safe_y)
    except: 
        print("ウィンドウのアクティブ化に失敗した可能性があります。")
        pass
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    temp_dir = f"temp_kindle_{timestamp}"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    image_files = []
    
    # Key mapping
    key_to_press = 'right' if config.get('direction', 'right') == 'right' else 'left'

    try:
        for i in range(pages):
            filename = os.path.join(temp_dir, f"page_{i:04d}.png")
            
            # Recalculate region just in case window moved slightly
            current_region = get_capture_region(win, config['margins'])
            
            screenshot = pyautogui.screenshot(region=current_region)
            screenshot.save(filename)
            image_files.append(filename)
            
            print(f"保存: {i+1}/{pages} -> {filename}", end='\r')
            
            pyautogui.press(key_to_press)
            time.sleep(delay)
            
    except pyautogui.FailSafeException:
        print("\n\n!!! 緊急停止（フェイルセーフ）が発動しました !!!")
        print("マウスが画面左上に移動されました。")
    except KeyboardInterrupt:
        print("\n中断されました。")
    except Exception as e:
        print(f"\nエラー: {e}")
    
    print("\n\nこれまでの画像からPDFを作成します...")
    
    if not image_files:
        print("画像が保存されませんでした。")
        return
        
    output_pdf = f"kindle_book_{timestamp}.pdf"
    abs_pdf_path = os.path.abspath(output_pdf)
    
    try:
        with open(output_pdf, "wb") as f:
            f.write(img2pdf.convert(image_files))
        print(f"完了！: {abs_pdf_path}")
        
        # Cleanup
        shutil.rmtree(temp_dir)
        
        # Open Folder
        print("保存先フォルダを開きます...")
        subprocess.Popen(f'explorer /select,"{abs_pdf_path}"') 
        
    except Exception as e:
        print(f"エラー発生: {e}")

if __name__ == "__main__":
    main()
