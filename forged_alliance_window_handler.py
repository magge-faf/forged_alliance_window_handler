import time
import psutil
import win32con
import win32gui
import win32api
import logging

GAME_PROCESS_NAME = "ForgedAlliance.exe"
SEARCH_INTERVAL = 10

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

previous_borderless_state = False


def is_borderless(hwnd):
    """
    Checks if the window has minimal borders based on size difference
    """
    # Get window rect (excluding borders)
    window_rect = win32gui.GetWindowRect(hwnd)
    # Get client rect (including borders)
    client_rect = win32gui.GetClientRect(hwnd)
    # Calculate border width/height difference
    border_width = (window_rect[2] - client_rect[2]) // 2
    border_height = (window_rect[3] - client_rect[3]) // 2
    # Consider window borderless if border width/height is minimal
    min_border_size = 5
    return border_width <= min_border_size and border_height <= min_border_size


def handle_window(hwnd):
    global previous_borderless_state

    if win32gui.GetWindowPlacement(hwnd)[1] != win32con.SW_SHOWMAXIMIZED:
        # Maximize the window before removing borders, otherwise it will pixelate
        l_param = win32api.MAKELONG(0, 0)
        win32gui.PostMessage(hwnd, win32con.WM_NCLBUTTONDBLCLK, win32con.HTCAPTION, l_param)

    current_borderless_state = is_borderless(hwnd)
    if not current_borderless_state and not previous_borderless_state:
        # Remove window borders
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
        style = style & ~(win32con.WS_CAPTION | win32con.WS_THICKFRAME)
        win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)

        # Maximize window to fill the screen
        monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromWindow(hwnd))
        screen_rect = monitor_info['Monitor']
        left, top, right, bottom = screen_rect
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, left, top, right - left, bottom - top, 0)
        logging.info(f"🎉 Made your game borderless fullscreen.")

    elif current_borderless_state and not previous_borderless_state:
        logging.info(f"✅ Game is already in borderless fullscreen.")

    previous_borderless_state = current_borderless_state


logging.info("✨ Borderless Supreme Commander ✨")
logging.info("🔎 This script will check for your game and make it borderless fullscreen (if needed).")

while True:
    if "ForgedAlliance.exe" in (p.name() for p in psutil.process_iter()):
        hwnd = win32gui.FindWindow(None, 'Forged Alliance')
        if hwnd != 0:
            handle_window(hwnd)

    time.sleep(SEARCH_INTERVAL)
