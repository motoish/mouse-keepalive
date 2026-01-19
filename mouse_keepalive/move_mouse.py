#!/usr/bin/env python3
"""
自动移动鼠标脚本 / Mouse Keepalive Script
支持 macOS、Windows 和 Linux 系统 / Supports macOS, Windows and Linux
"""

import sys
import os
import time
import platform
from typing import Optional, Callable, Tuple
from dataclasses import dataclass

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


@dataclass
class MousePosition:
    """鼠标位置数据类 / Mouse position data class"""

    x: int
    y: int


@dataclass
class ScreenSize:
    """屏幕尺寸数据类 / Screen size data class"""

    width: int
    height: int


class MouseController:
    """
    鼠标控制器接口 / Mouse controller interface
    封装鼠标操作，便于测试时替换实现
    """

    def get_position(self) -> MousePosition:
        """获取当前鼠标位置 / Get current mouse position"""
        x, y = pyautogui.position()
        return MousePosition(x, y)

    def get_screen_size(self) -> ScreenSize:
        """获取屏幕尺寸 / Get screen size"""
        width, height = pyautogui.size()
        return ScreenSize(width, height)

    def move_to(self, x: int, y: int, duration: float = 0.1) -> None:
        """移动鼠标到指定位置 / Move mouse to specified position"""
        pyautogui.moveTo(x, y, duration=duration)


class MouseMover:
    """
    核心鼠标移动逻辑类 / Core mouse movement logic class
    这个类包含所有核心逻辑，不依赖具体的 I/O 实现，便于测试
    """

    def __init__(
        self,
        controller: Optional[MouseController] = None,
        time_func: Optional[Callable[[], float]] = None,
        sleep_func: Optional[Callable[[float], None]] = None,
        print_func: Optional[Callable[[str], None]] = None,
    ):
        """
        初始化鼠标移动器 / Initialize mouse mover

        Args:
            controller: 鼠标控制器，默认使用真实实现 / Mouse controller, defaults to real implementation
            time_func: 时间函数，默认使用 time.time / Time function, defaults to time.time
            sleep_func: 睡眠函数，默认使用 time.sleep / Sleep function, defaults to time.sleep
            print_func: 打印函数，默认使用 print / Print function, defaults to print
        """
        self.controller = controller or MouseController()
        self.time_func = time_func or time.time
        self.sleep_func = sleep_func or time.sleep
        # 默认使用带刷新的 print 函数，解决 Windows 输出缓冲问题
        # Default to print with flush to solve Windows output buffering issue
        if print_func is None:
            # 创建一个自动刷新的 print 包装函数
            # Create a print wrapper function that auto-flushes
            def flushed_print(*args, **kwargs):
                kwargs.setdefault("flush", True)
                print(*args, **kwargs)

            self.print_func = flushed_print
        else:
            self.print_func = print_func

    def calculate_next_position(
        self, current_pos: MousePosition, screen_size: ScreenSize, move_count: int
    ) -> Tuple[int, int]:
        """
        计算下一个鼠标位置 / Calculate next mouse position

        Args:
            current_pos: 当前鼠标位置 / Current mouse position
            screen_size: 屏幕尺寸 / Screen size
            move_count: 移动计数（用于交替方向）/ Move count (for alternating direction)

        Returns:
            下一个位置的 (x, y) 坐标 / Next position (x, y) coordinates
        """
        # 移动鼠标到稍微不同的位置（移动1-2像素）
        # Move mouse to slightly different position (move 1-2 pixels)
        offset_x = 1 if move_count % 2 == 0 else -1
        offset_y = 1 if move_count % 2 == 0 else -1

        new_x = current_pos.x + offset_x
        new_y = current_pos.y + offset_y

        # 确保坐标在屏幕范围内 / Ensure coordinates are within screen bounds
        new_x = max(1, min(new_x, screen_size.width - 1))
        new_y = max(1, min(new_y, screen_size.height - 1))

        return new_x, new_y

    def perform_move(self, move_count: int) -> Tuple[MousePosition, int, bool]:
        """
        执行一次鼠标移动 / Perform one mouse movement

        Args:
            move_count: 当前移动计数 / Current move count

        Returns:
            (原始位置, 新的移动计数, 是否成功) / (Original position, new move count, success)
        """
        current_pos = MousePosition(0, 0)  # 默认值 / Default value
        try:
            # 获取当前鼠标位置 / Get current mouse position
            current_pos = self.controller.get_position()

            # 获取屏幕尺寸 / Get screen size
            screen_size = self.controller.get_screen_size()

            # 计算下一个位置 / Calculate next position
            new_x, new_y = self.calculate_next_position(current_pos, screen_size, move_count)

            # 移动鼠标 / Move mouse
            self.controller.move_to(new_x, new_y, duration=0.1)
            move_count += 1

            # 立即移回原位置（这样用户感觉不到鼠标移动）
            # Immediately move back to original position (user won't notice the movement)
            self.controller.move_to(current_pos.x, current_pos.y, duration=0.1)

            return current_pos, move_count, True
        except Exception as e:
            # 记录错误但不中断程序 / Log error but don't interrupt program
            self.print_func(f"警告: 鼠标移动失败 / Warning: Mouse movement failed: {e}")
            self.print_func(f"Warning: Mouse movement failed: {e}")
            return current_pos, move_count, False

    def run(
        self,
        interval: int = 60,
        duration: Optional[int] = None,
        verbose: bool = False,
        on_start: Optional[Callable[[], None]] = None,
        on_move: Optional[Callable[[int, MousePosition, float, bool], None]] = None,
        on_finish: Optional[Callable[[int, float], None]] = None,
    ) -> Tuple[int, float]:
        """
        运行鼠标移动循环 / Run mouse movement loop

        Args:
            interval: 移动间隔（秒）/ Movement interval (seconds)
            duration: 运行时长（秒），None 表示无限运行 / Duration (seconds), None means infinite
            verbose: 是否显示详细日志 / Whether to show verbose logs
            on_start: 启动回调函数 / Start callback function
            on_move: 移动回调函数，参数为 (move_count, position, elapsed, success) / Move callback function
            on_finish: 完成回调函数 / Finish callback function

        Returns:
            (移动次数, 运行时长) / (Move count, duration)
        """
        if on_start:
            on_start()

        start_time = self.time_func()
        move_count = 0
        success_count = 0

        try:
            while True:
                # 执行移动 / Perform move
                current_pos, move_count, success = self.perform_move(move_count)
                if success:
                    success_count += 1

                elapsed = self.time_func() - start_time

                if on_move:
                    on_move(move_count, current_pos, elapsed, success)

                # 检查是否达到运行时长 / Check if duration is reached
                if duration and elapsed >= duration:
                    if on_finish:
                        on_finish(move_count, elapsed)
                    break

                # 等待指定间隔 / Wait for specified interval
                self.sleep_func(interval)

        except KeyboardInterrupt:
            elapsed = self.time_func() - start_time
            if on_finish:
                on_finish(move_count, elapsed)
            raise

        elapsed = self.time_func() - start_time
        return move_count, elapsed


def move_mouse(interval: int = 60, duration: Optional[int] = None, verbose: bool = False) -> None:
    """
    自动移动鼠标 / Automatically move mouse
    这是主要的公共 API，保持向后兼容性

    Args:
        interval: 移动间隔（秒），默认60秒 / Movement interval (seconds), default 60
        duration: 运行时长（秒），None表示无限运行 / Duration (seconds), None means infinite
        verbose: 是否显示详细日志 / Whether to show verbose logs
    """
    mover = MouseMover()
    success_count = [0]  # 使用列表以便在闭包中修改 / Use list to allow modification in closure

    def on_start():
        mover.print_func("开始自动移动鼠标...")
        mover.print_func("Starting mouse keepalive...")
        mover.print_func(f"移动间隔: {interval} 秒 / Interval: {interval} seconds")
        if duration:
            mover.print_func(f"运行时长: {duration} 秒 / Duration: {duration} seconds")
        else:
            mover.print_func("运行时长: 无限（按 Ctrl+C 停止） / Duration: Infinite (Press Ctrl+C to stop)")
        mover.print_func(f"操作系统: {platform.system()} / OS: {platform.system()}")
        if verbose:
            mover.print_func("详细模式: 已启用 / Verbose mode: Enabled")
        mover.print_func("-" * 50)

    def on_move(move_count: int, current_pos: MousePosition, elapsed: float, success: bool):
        if success:
            success_count[0] += 1

        if verbose:
            status = "成功" if success else "失败"
            mover.print_func(
                f"[{int(elapsed)}s] 已移动鼠标 {move_count} 次 (当前位置: {current_pos.x}, {current_pos.y}, 状态: {status})"
            )
            status_text = "success" if success else "failed"
            mover.print_func(
                f"[{int(elapsed)}s] Moved mouse {move_count} times "
                f"(current position: {current_pos.x}, {current_pos.y}, status: {status_text})"
            )
        elif success:
            # 非详细模式下，每次成功移动都输出日志 / In non-verbose mode, output every successful moves
            mover.print_func(f"[{int(elapsed)}s] 已移动鼠标 {move_count} 次 / Moved mouse {move_count} times")
        elif not success:
            mover.print_func(
                f"[{int(elapsed)}s] 警告：移动鼠标失败 / Warning: Mouse movement failed(attempt {move_count})"
            )

    def on_finish(move_count: int, elapsed: float):
        if duration:
            mover.print_func(f"\n达到运行时长 {duration} 秒，程序退出")
            mover.print_func(f"Duration {duration} seconds reached, exiting")
        else:
            mover.print_func("\n\n程序被用户中断")
            mover.print_func("Program interrupted by user")
        mover.print_func(f"总共移动鼠标 {move_count} 次 / Total moves: {move_count}")
        mover.print_func(f"成功移动: {success_count[0]} 次 / Successful moves: {success_count[0]}")
        mover.print_func(f"运行时长: {int(elapsed)} 秒 / Duration: {int(elapsed)} seconds")

    try:
        mover.run(
            interval=interval,
            duration=duration,
            verbose=verbose,
            on_start=on_start,
            on_move=on_move,
            on_finish=on_finish,
        )
    except KeyboardInterrupt:
        # on_finish 已经在 KeyboardInterrupt 处理中调用
        pass


def main():
    """命令行入口函数 / Command line entry function"""
    import argparse

    # 在 Windows 上设置输出为行缓冲模式，解决输出延迟问题
    # Set output to line buffering on Windows to solve output delay issue
    if platform.system() == "Windows":
        try:
            # Python 3.7+ 支持 reconfigure
            # Python 3.7+ supports reconfigure
            if hasattr(sys.stdout, "reconfigure"):
                sys.stdout.reconfigure(line_buffering=True)
            else:
                # Python < 3.7 的回退方案
                # Fallback for Python < 3.7
                sys.stdout = os.fdopen(sys.stdout.fileno(), "w", buffering=1)
        except (AttributeError, OSError, ValueError):
            # 如果设置失败，继续使用默认缓冲（至少 print 函数会使用 flush=True）
            # If setting fails, continue with default buffering (at least print will use flush=True)
            pass

    parser = argparse.ArgumentParser(
        description="自动移动鼠标工具（防止系统进入休眠或锁定） / Mouse keepalive tool (prevents system sleep or lock)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例 / Examples:
  mouse-keepalive                    # 每60秒移动一次，无限运行 / Move every 60s, infinite
  mouse-keepalive -i 30              # 每30秒移动一次 / Move every 30s
  mouse-keepalive -i 120 -d 3600     # 每120秒移动一次，运行1小时 / Move every 120s, run for 1 hour
  mouse-keepalive -v                 # 显示详细日志 / Show verbose logs
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

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="显示详细日志 / Show verbose logs",
    )

    args = parser.parse_args()

    if args.interval < 1:
        print("错误: 移动间隔必须大于0")
        print("Error: Interval must be greater than 0")
        sys.exit(1)

    if args.duration is not None and args.duration < 1:
        print("错误: 运行时长必须大于0")
        print("Error: Duration must be greater than 0")
        sys.exit(1)

    move_mouse(interval=args.interval, duration=args.duration, verbose=args.verbose)


if __name__ == "__main__":
    main()
