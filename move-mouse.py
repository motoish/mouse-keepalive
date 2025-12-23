#!/usr/bin/env python3
"""
Auto Mouse Mover - Cross-platform Python version
Usage: python move-mouse.py [interval_seconds]
Example: python move-mouse.py 60  (moves mouse every 60 seconds)
"""

import sys
import time
import platform
from datetime import datetime

try:
    import pyautogui
except ImportError:
    print("Error: pyautogui is not installed.")
    print("Please install it using: pip install pyautogui")
    sys.exit(1)

# Disable pyautogui failsafe (optional, comment out if you want failsafe)
# pyautogui.FAILSAFE = False

def move_mouse():
    """Move mouse slightly and return to original position"""
    current_x, current_y = pyautogui.position()
    
    # Move mouse slightly (1 pixel) and back
    pyautogui.moveRel(1, 0, duration=0.1)
    pyautogui.moveRel(-1, 0, duration=0.1)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - Mouse moved")

def main():
    # Get interval from command line argument or use default
    try:
        interval = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    except ValueError:
        print("Error: Interval must be a number")
        print("Usage: python move-mouse.py [interval_seconds]")
        sys.exit(1)
    
    print("Auto Mouse Mover started")
    print(f"Platform: {platform.system()}")
    print(f"Interval: {interval} seconds")
    print("Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        while True:
            move_mouse()
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nAuto Mouse Mover stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main()

