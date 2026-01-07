#!/usr/bin/env python3
"""
自动移动鼠标脚本 / Mouse Keepalive Script
支持 macOS、Windows 和 Linux 系统 / Supports macOS, Windows and Linux
"""

import sys
import time
import platform

try:
    import pyautogui
except ImportError:
    print("错误: 未安装 pyautogui 库")
    print("Error: pyautogui library not installed")
    print("请运行: pip install pyautogui")
    print("Please run: pip install pyautogui")
    sys.exit(1)

# 禁用 pyautogui 的安全功能（防止鼠标移到屏幕角落时停止）
# Disable pyautogui failsafe (prevents stopping when mouse moves to screen corner)
pyautogui.FAILSAFE = False


def move_mouse(interval=60, duration=None):
    """
    自动移动鼠标 / Automatically move mouse

    Args:
        interval: 移动间隔（秒），默认60秒 / Movement interval (seconds), default 60
        duration: 运行时长（秒），None表示无限运行 / Duration (seconds), None means infinite
    """
    print("开始自动移动鼠标...")
    print("Starting mouse keepalive...")
    print(f"移动间隔: {interval} 秒 / Interval: {interval} seconds")
    if duration:
        print(f"运行时长: {duration} 秒 / Duration: {duration} seconds")
    else:
        print("运行时长: 无限（按 Ctrl+C 停止） / Duration: Infinite (Press Ctrl+C to stop)")
    print(f"操作系统: {platform.system()} / OS: {platform.system()}")
    print("-" * 50)

    start_time = time.time()
    move_count = 0

    try:
        while True:
            # 获取当前鼠标位置 / Get current mouse position
            current_x, current_y = pyautogui.position()

            # 移动鼠标到稍微不同的位置（移动1-2像素）
            # Move mouse to slightly different position (move 1-2 pixels)
            offset_x = 1 if move_count % 2 == 0 else -1
            offset_y = 1 if move_count % 2 == 0 else -1

            new_x = current_x + offset_x
            new_y = current_y + offset_y

            # 确保坐标在屏幕范围内 / Ensure coordinates are within screen bounds
            screen_width, screen_height = pyautogui.size()
            new_x = max(1, min(new_x, screen_width - 1))
            new_y = max(1, min(new_y, screen_height - 1))

            # 移动鼠标 / Move mouse
            pyautogui.moveTo(new_x, new_y, duration=0.1)
            move_count += 1

            # 立即移回原位置（这样用户感觉不到鼠标移动）
            # Immediately move back to original position (user won't notice the movement)
            pyautogui.moveTo(current_x, current_y, duration=0.1)

            elapsed = time.time() - start_time
            print(f"[{int(elapsed)}s] 已移动鼠标 {move_count} 次 (当前位置: {current_x}, {current_y})")
            print(f"[{int(elapsed)}s] Moved mouse {move_count} times (current position: {current_x}, {current_y})")

            # 检查是否达到运行时长 / Check if duration is reached
            if duration and elapsed >= duration:
                print(f"\n达到运行时长 {duration} 秒，程序退出")
                print(f"Duration {duration} seconds reached, exiting")
                break

            # 等待指定间隔 / Wait for specified interval
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
        print("Program interrupted by user")
        print(f"总共移动鼠标 {move_count} 次 / Total moves: {move_count}")
        print(f"运行时长: {int(time.time() - start_time)} 秒 / Duration: {int(time.time() - start_time)} seconds")


def main():
    """命令行入口函数 / Command line entry function"""
    import argparse

    parser = argparse.ArgumentParser(
        description="自动移动鼠标工具（防止系统进入休眠或锁定） / Mouse keepalive tool (prevents system sleep or lock)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例 / Examples:
  mouse-keepalive                    # 每60秒移动一次，无限运行 / Move every 60s, infinite
  mouse-keepalive -i 30              # 每30秒移动一次 / Move every 30s
  mouse-keepalive -i 120 -d 3600     # 每120秒移动一次，运行1小时 / Move every 120s, run for 1 hour
  mka -i 30                          # 使用简短别名 / Use short alias
  python -m mouse_keepalive         # 使用模块方式运行 / Run as module
        """,
    )

    parser.add_argument(
        "-i",
        "--interval",
        type=int,
        default=60,
        help="鼠标移动间隔（秒），默认60秒 / Mouse movement interval (seconds), default 60",
    )

    parser.add_argument(
        "-d",
        "--duration",
        type=int,
        default=None,
        help="运行时长（秒），默认无限运行 / Duration (seconds), default infinite",
    )

    args = parser.parse_args()

    if args.interval < 1:
        print("错误: 移动间隔必须大于0")
        print("Error: Interval must be greater than 0")
        sys.exit(1)

    if args.duration and args.duration < 1:
        print("错误: 运行时长必须大于0")
        print("Error: Duration must be greater than 0")
        sys.exit(1)

    move_mouse(interval=args.interval, duration=args.duration)


if __name__ == "__main__":
    main()
