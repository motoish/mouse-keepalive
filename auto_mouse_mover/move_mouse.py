#!/usr/bin/env python3
"""
自动移动鼠标脚本
支持 macOS、Windows 和 Linux 系统
"""

import sys
import time
import platform

try:
    import pyautogui
except ImportError:
    print("错误: 未安装 pyautogui 库")
    print("请运行: pip install pyautogui")
    sys.exit(1)

# 禁用 pyautogui 的安全功能（防止鼠标移到屏幕角落时停止）
pyautogui.FAILSAFE = False


def move_mouse(interval=60, duration=None):
    """
    自动移动鼠标

    Args:
        interval: 移动间隔（秒），默认60秒
        duration: 运行时长（秒），None表示无限运行
    """
    print("开始自动移动鼠标...")
    print(f"移动间隔: {interval} 秒")
    if duration:
        print(f"运行时长: {duration} 秒")
    else:
        print("运行时长: 无限（按 Ctrl+C 停止）")
    print(f"操作系统: {platform.system()}")
    print("-" * 50)

    start_time = time.time()
    move_count = 0

    try:
        while True:
            # 获取当前鼠标位置
            current_x, current_y = pyautogui.position()

            # 移动鼠标到稍微不同的位置（移动1-2像素）
            offset_x = 1 if move_count % 2 == 0 else -1
            offset_y = 1 if move_count % 2 == 0 else -1

            new_x = current_x + offset_x
            new_y = current_y + offset_y

            # 确保坐标在屏幕范围内
            screen_width, screen_height = pyautogui.size()
            new_x = max(1, min(new_x, screen_width - 1))
            new_y = max(1, min(new_y, screen_height - 1))

            # 移动鼠标
            pyautogui.moveTo(new_x, new_y, duration=0.1)
            move_count += 1

            # 立即移回原位置（这样用户感觉不到鼠标移动）
            pyautogui.moveTo(current_x, current_y, duration=0.1)

            elapsed = time.time() - start_time
            print(f"[{int(elapsed)}s] 已移动鼠标 {move_count} 次 (当前位置: {current_x}, {current_y})")

            # 检查是否达到运行时长
            if duration and elapsed >= duration:
                print(f"\n达到运行时长 {duration} 秒，程序退出")
                break

            # 等待指定间隔
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
        print(f"总共移动鼠标 {move_count} 次")
        print(f"运行时长: {int(time.time() - start_time)} 秒")


def main():
    """命令行入口函数"""
    import argparse

    parser = argparse.ArgumentParser(
        description="自动移动鼠标工具（防止系统进入休眠或锁定）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  auto-mouse-mover                    # 每60秒移动一次，无限运行
  auto-mouse-mover -i 30              # 每30秒移动一次
  auto-mouse-mover -i 120 -d 3600     # 每120秒移动一次，运行1小时
  python -m auto_mouse_mover         # 使用模块方式运行
        """
    )

    parser.add_argument(
        "-i", "--interval",
        type=int,
        default=60,
        help="鼠标移动间隔（秒），默认60秒"
    )

    parser.add_argument(
        "-d", "--duration",
        type=int,
        default=None,
        help="运行时长（秒），默认无限运行"
    )

    args = parser.parse_args()

    if args.interval < 1:
        print("错误: 移动间隔必须大于0")
        sys.exit(1)

    if args.duration and args.duration < 1:
        print("错误: 运行时长必须大于0")
        sys.exit(1)

    move_mouse(interval=args.interval, duration=args.duration)


if __name__ == "__main__":
    main()
