import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Toplevel
import sys
import os
import time
import json
import threading
import pyautogui
import img2pdf
import pygetwindow as gw
import subprocess
import shutil
from PIL import Image, ImageTk
import keyboard  # Requires 'pip install keyboard'

# --- Constants & Global Setup ---
CONFIG_FILE = "kindle_config.json"
DEFAULT_OUTPUT_DIR = r"C:\Users\puchi\Desktop\antigravity\kindle_pdf\result"
pyautogui.FAILSAFE = True

# --- Logic / Helper Functions ---

def load_config():
    default_config = {
        "pages": 100,
        "delay": 0.5,
        "direction": "right",
        "output_dir": DEFAULT_OUTPUT_DIR,
        "margins": {"top": 120, "bottom": 80, "left": 50, "right": 50}
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding='utf-8') as f:
                loaded = json.load(f)
                for k, v in default_config.items():
                    if k not in loaded:
                        loaded[k] = v
                return loaded
        except:
            return default_config
    return default_config

def save_config(config):
    try:
        with open(CONFIG_FILE, "w", encoding='utf-8') as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"Config save failed: {e}")

def find_kindle_window():
    try:
        windows = gw.getWindowsWithTitle('Kindle')
        if windows:
            return windows[0]
    except:
        pass
    return None

def activate_window(win):
    try:
        if win.isMinimized:
            win.restore()
        win.activate()
        return True
    except:
        return False

# --- GUI Application ---

class KindlePdfApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kindle PDF Maker v3")
        self.geometry("520x650")
        self.resizable(False, False)
        
        self.config = load_config()
        
        # UI Variables
        self.var_title = tk.StringVar(value="")
        self.var_pages = tk.IntVar(value=self.config['pages'])
        self.var_delay = tk.DoubleVar(value=self.config['delay'])
        self.var_direction = tk.StringVar(value=self.config['direction'])
        self.var_output_dir = tk.StringVar(value=self.config.get('output_dir', DEFAULT_OUTPUT_DIR))
        
        self.var_margin_top = tk.IntVar(value=self.config['margins']['top'])
        self.var_margin_bottom = tk.IntVar(value=self.config['margins']['bottom'])
        self.var_margin_left = tk.IntVar(value=self.config['margins']['left'])
        self.var_margin_right = tk.IntVar(value=self.config['margins']['right'])
        
        self.is_running = False
        self.stop_requested = False
        
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # --- File Settings ---
        file_frame = ttk.LabelFrame(main_frame, text="ファイル設定", padding="5")
        file_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(file_frame, text="本のタイトル:").grid(row=0, column=0, sticky="w")
        ttk.Entry(file_frame, textvariable=self.var_title, width=50).grid(row=0, column=1, padx=5, sticky="w", columnspan=2)
        
        ttk.Label(file_frame, text="保存先:").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(file_frame, textvariable=self.var_output_dir, width=40).grid(row=1, column=1, padx=5, sticky="w")
        ttk.Button(file_frame, text="参照", command=self.browse_dir).grid(row=1, column=2)

        # --- Manual Settings ---
        settings_frame = ttk.LabelFrame(main_frame, text="動作設定", padding="5")
        settings_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(settings_frame, text="ページ数:").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(settings_frame, textvariable=self.var_pages, width=10).grid(row=0, column=1, sticky="w", padx=5)
        
        ttk.Label(settings_frame, text="待機(秒):").grid(row=0, column=2, sticky="w", padx=5)
        ttk.Entry(settings_frame, textvariable=self.var_delay, width=10).grid(row=0, column=3, sticky="w", padx=5)
        
        ttk.Label(settings_frame, text="めくり方向:").grid(row=1, column=0, sticky="w", pady=5)
        frame_dir = ttk.Frame(settings_frame)
        frame_dir.grid(row=1, column=1, columnspan=3, sticky="w")
        ttk.Radiobutton(frame_dir, text="右へ (→)", variable=self.var_direction, value="right").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(frame_dir, text="左へ (←)", variable=self.var_direction, value="left").pack(side=tk.LEFT)

        # --- Margin Section ---
        margin_frame = ttk.LabelFrame(main_frame, text="撮影範囲 (マージン設定)", padding="5")
        margin_frame.pack(fill=tk.X, pady=5)
        
        # Auto-set buttons
        btn_frame = ttk.Frame(margin_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="① 左上座標を取得 (3秒)", command=lambda: self.get_coords('top_left')).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        ttk.Button(btn_frame, text="② 右下座標を取得 (3秒)", command=lambda: self.get_coords('bottom_right')).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        
        # Manual entry grid
        grid_frame = ttk.Frame(margin_frame)
        grid_frame.pack(pady=5)
        
        ttk.Entry(grid_frame, textvariable=self.var_margin_top, width=6).grid(row=0, column=1, pady=2)
        ttk.Entry(grid_frame, textvariable=self.var_margin_left, width=6).grid(row=1, column=0, padx=5)
        ttk.Label(grid_frame, text="[ 本文エリア ]").grid(row=1, column=1, padx=5)
        ttk.Entry(grid_frame, textvariable=self.var_margin_right, width=6).grid(row=1, column=2, padx=5)
        ttk.Entry(grid_frame, textvariable=self.var_margin_bottom, width=6).grid(row=2, column=1, pady=2)

        # Preview Button
        ttk.Button(margin_frame, text="現在の設定でプレビュー撮影 (確認用)", command=self.preview_shot).pack(fill=tk.X, padx=20, pady=5)

        # --- Action Section ---
        self.btn_start = ttk.Button(main_frame, text="PDF作成を開始する (開始まで5秒待機)", command=self.start_process)
        self.btn_start.pack(fill=tk.X, pady=10, ipady=5)
        
        # Status
        self.status_var = tk.StringVar(value="タイトルを入力してください")
        ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN).pack(fill=tk.X)
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.pack(fill=tk.X, pady=2)
        
        ttk.Label(main_frame, text="※中断: Escキー長押し または マウスを左上へ", font=("", 8), foreground="red").pack()

    def browse_dir(self):
        d = filedialog.askdirectory(initialdir=self.var_output_dir.get())
        if d:
            self.var_output_dir.set(d)

    def save_current_config(self):
        cfg = {
            "pages": self.var_pages.get(),
            "delay": self.var_delay.get(),
            "direction": self.var_direction.get(),
            "output_dir": self.var_output_dir.get(),
            "margins": {
                "top": self.var_margin_top.get(),
                "bottom": self.var_margin_bottom.get(),
                "left": self.var_margin_left.get(),
                "right": self.var_margin_right.get()
            }
        }
        save_config(cfg)
        return cfg

    # --- Feature: Preview ---
    def preview_shot(self):
        self.iconify()
        
        def _task():
            time.sleep(1)
            win = find_kindle_window()
            if not win:
                self.after(0, lambda: messagebox.showerror("Error", "Kindleウィンドウが見つかりません"))
                self.after(0, self.deiconify)
                return
            
            activate_window(win)
            time.sleep(1)
            
            # Calculate 
            margins = {
                "top": self.var_margin_top.get(),
                "bottom": self.var_margin_bottom.get(),
                "left": self.var_margin_left.get(),
                "right": self.var_margin_right.get()
            }
            
            x = win.left + margins['left']
            y = win.top + margins['top']
            w = win.width - (margins['left'] + margins['right'])
            h = win.height - (margins['top'] + margins['bottom'])
            
            if w <= 0 or h <= 0:
                self.after(0, lambda: messagebox.showerror("Error", f"範囲が無効です。\nW={w}, H={h}"))
                self.after(0, self.deiconify)
                return
            
            # Shot
            img = pyautogui.screenshot(region=(x, y, w, h))
            
            self.after(0, self.deiconify)
            self.after(0, lambda: self.show_preview_window(img, w, h))
            
        threading.Thread(target=_task, daemon=True).start()

    def show_preview_window(self, img, w, h):
        top = Toplevel(self)
        top.title(f"プレビュー ({w}x{h})")
        top.geometry("600x600")
        
        # Resize for preview if too big
        disp_img = img.copy()
        disp_img.thumbnail((580, 580))
        tk_img = ImageTk.PhotoImage(disp_img)
        
        lbl = ttk.Label(top, image=tk_img)
        lbl.image = tk_img
        lbl.pack(expand=True)
        ttk.Label(top, text="これが正しく本文のみ切り抜かれているか確認してください。").pack(pady=5)

    # --- Feature: Coords ---
    def get_coords(self, mode):
        self.iconify()
        
        def _task():
            time.sleep(3)
            win = find_kindle_window()
            if not win:
                self.after(0, self.deiconify)
                return
            
            mx, my = pyautogui.position()
            
            if mode == 'top_left':
                ml = max(0, mx - win.left)
                mt = max(0, my - win.top)
                self.after(0, lambda: [self.var_margin_left.set(ml), self.var_margin_top.set(mt)])
                self.after(0, lambda: messagebox.showinfo("完了", f"左上取得: left={ml}, top={mt}"))
                
            elif mode == 'bottom_right':
                win_right_edge = win.left + win.width
                win_bottom_edge = win.top + win.height
                mr = max(0, win_right_edge - mx)
                mb = max(0, win_bottom_edge - my)
                self.after(0, lambda: [self.var_margin_right.set(mr), self.var_margin_bottom.set(mb)])
                self.after(0, lambda: messagebox.showinfo("完了", f"右下取得: right={mr}, bottom={mb}"))

            self.after(0, self.deiconify)

        threading.Thread(target=_task, daemon=True).start()

    # --- Process ---
    def start_process(self):
        title = self.var_title.get().strip()
        if not title:
            messagebox.showwarning("入力エラー", "本のタイトルを入力してください。")
            return

        cfg = self.save_current_config()
        self.btn_start.config(state=tk.DISABLED)
        self.is_running = True
        self.stop_requested = False
        
        threading.Thread(target=self.run_automation, args=(cfg, title), daemon=True).start()

    def run_automation(self, cfg, title):
        try:
            pages = cfg['pages']
            delay = cfg['delay']
            out_dir = cfg['output_dir']
            margins = cfg['margins']
            
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            
            timestamp = time.strftime("%Y%m%d")
            pdf_filename = f"{title}_{timestamp}.pdf"
            ts_full = time.strftime("%Y%m%d_%H%M%S")
            temp_dir = os.path.join(out_dir, f"temp_{ts_full}")
            os.makedirs(temp_dir, exist_ok=True)
            
            self.update_status(f"5秒後に開始します (Escで中止可)...")
            
            # Countdown
            for k in range(5, 0, -1):
                if keyboard.is_pressed('esc'):
                    raise Exception("ユーザーにより中止されました (Esc)")
                self.update_status(f"開始まであと {k} 秒... (Escで中止)")
                time.sleep(1)
            
            if keyboard.is_pressed('esc'): raise Exception("中止 (Esc)")

            # Activate
            win = find_kindle_window()
            if not win: raise Exception("Kindleウィンドウなし")
            activate_window(win)
            time.sleep(0.5)
            
            # Region Calc
            x = win.left + margins['left']
            y = win.top + margins['top']
            w = win.width - (margins['left'] + margins['right'])
            h = win.height - (margins['top'] + margins['bottom'])
            
            if w <= 0 or h <= 0: raise Exception("範囲無効")
            region = (x, y, w, h)
            key_to_press = 'right' if cfg['direction'] == 'right' else 'left'
            
            image_files = []
            self.after(0, lambda: self.progress.configure(maximum=pages))
            
            for i in range(pages):
                # Check Stop
                if not self.is_running: break
                if keyboard.is_pressed('esc'):
                    self.stop_requested = True
                    break

                self.update_status(f"撮影中({title}): {i+1} / {pages} (Escで停止)")
                self.after(0, lambda v=i: self.progress.configure(value=v))
                
                fname = os.path.join(temp_dir, f"p{i:04d}.png")
                pyautogui.screenshot(region=region).save(fname)
                image_files.append(fname)
                
                pyautogui.press(key_to_press)
                time.sleep(delay)
            
            if self.stop_requested:
                self.update_status("中断されました。ここまでの画像で作成します...")
                time.sleep(1)

            if image_files:
                self.update_status("PDF作成中...")
                out_pdf = os.path.join(out_dir, pdf_filename)
                if os.path.exists(out_pdf):
                     out_pdf = os.path.join(out_dir, f"{title}_{ts_full}.pdf")

                with open(out_pdf, "wb") as f:
                    f.write(img2pdf.convert(image_files))
                
                self.update_status("完了")
                messagebox.showinfo("完了", f"PDFを作成しました:\n{out_pdf}\n(ページ数: {len(image_files)})")
                subprocess.Popen(f'explorer /select,"{out_pdf}"')
            else:
                 self.update_status("画像がありません")
            
            try: shutil.rmtree(temp_dir)
            except: pass

        except pyautogui.FailSafeException:
            self.update_status("緊急停止 (マウス)")
            messagebox.showwarning("中断", "緊急停止しました。")
        except Exception as e:
            self.update_status(f"エラー: {e}")
            if "Esc" in str(e):
                pass # Just stop
            else:
                messagebox.showerror("エラー", str(e))
        finally:
            self.is_running = False
            self.after(0, lambda: self.btn_start.config(state=tk.NORMAL))

    def update_status(self, msg):
        self.after(0, lambda: self.status_var.set(msg))

if __name__ == "__main__":
    app = KindlePdfApp()
    app.mainloop()
