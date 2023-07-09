import time
import psutil
import win32con
import win32gui
import win32api


"""
Borderless full-screen for Supreme Commander Forged Alliance
"""

# Function to handle the window
def handle_window(hwnd):
    # Set the window style to remove borders
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
    style = style & ~(win32con.WS_CAPTION | win32con.WS_THICKFRAME)
    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)

    # Set the window position and size to cover the entire screen
    monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromWindow(hwnd))
    screen_rect = monitor_info['Monitor']
    left, top, right, bottom = screen_rect
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, left, top, right - left, bottom - top, 0)


# Main loop
while True:
    # Check if the "ForgedAlliance.exe" process is running
    if "ForgedAlliance.exe" in (p.name() for p in psutil.process_iter()):
        # Find the window titled "Forged Alliance"
        hwnd = win32gui.FindWindow(None, 'Forged Alliance')
        if hwnd != 0:
            handle_window(hwnd)  # Call the function to handle the window
    time.sleep(10)
