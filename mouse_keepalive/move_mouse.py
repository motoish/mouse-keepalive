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


def get_system_idle_seconds() -> Optional[float]:
    """
    获取系统空闲时间（秒）/ Get system idle time (seconds)

    - Windows: 使用 GetLastInputInfo 读取系统最后一次“输入事件”到当前的时间差
      Use GetLastInputInfo to get time since last input event.
    - 其他系统: 返回 None / Other OS: returns None
    """
    if platform.system() != "Windows":
        return None

    try:
        import ctypes
        from ctypes import wintypes

        class LASTINPUTINFO(ctypes.Structure):
            _fields_ = [("cbSize", wintypes.UINT), ("dwTime", wintypes.DWORD)]

        last_input_info = LASTINPUTINFO()
        last_input_info.cbSize = ctypes.sizeof(LASTINPUTINFO)

        # BOOL GetLastInputInfo(PLASTINPUTINFO plii);
        if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(last_input_info)) == 0:
            return None

        # DWORD GetTickCount(void);  (millis since system start)
        tick_count_ms = ctypes.windll.kernel32.GetTickCount()
        idle_ms = tick_count_ms - last_input_info.dwTime
        return float(idle_ms) / 1000.0
    except Exception:
        return None


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

    def press_key(self, key: str = "shift") -> None:
        """模拟按键按下和释放 / Simulate key press and release"""
        pyautogui.press(key)


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
        # 移动鼠标到稍微不同的位置（移动20-30像素，确保被系统识别为有效输入）
        # Move mouse to slightly different position (move 20-30 pixels to ensure recognized as valid input)
        # 使用更大的移动距离，以便 Teams 等应用能够识别为用户活动
        # Use larger movement distance so apps like Teams can recognize it as user activity
        base_offset = 25  # 基础偏移量 / Base offset
        offset_x = base_offset if move_count % 2 == 0 else -base_offset
        offset_y = base_offset if move_count % 2 == 0 else -base_offset

        new_x = current_pos.x + offset_x
        new_y = current_pos.y + offset_y

        # 确保坐标在屏幕范围内 / Ensure coordinates are within screen bounds
        new_x = max(1, min(new_x, screen_size.width - 1))
        new_y = max(1, min(new_y, screen_size.height - 1))

        return new_x, new_y

    def perform_key_press(self, move_count: int) -> Tuple[MousePosition, int, bool]:
        """
        执行一次键盘按键 / Perform one key press

        Args:
            move_count: 当前移动计数 / Current move count

        Returns:
            (当前位置, 新的移动计数, 是否成功) / (Current position, new move count, success)
        """
        current_pos = MousePosition(0, 0)  # 默认值 / Default value
        try:
            # 获取当前鼠标位置（用于日志显示）/ Get current mouse position (for logging)
            current_pos = self.controller.get_position()

            # 模拟按下 Shift 键（不会影响当前输入，但会被系统识别为活动）
            # Simulate pressing Shift key (won't affect current input, but recognized as activity)
            self.controller.press_key("shift")
            move_count += 1

            return current_pos, move_count, True
        except Exception as e:
            # 记录错误但不中断程序 / Log error but don't interrupt program
            self.print_func(f"警告: 键盘输入失败 / Warning: Key press failed: {e}")
            self.print_func(f"Warning: Key press failed: {e}")
            return current_pos, move_count, False

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
        method: str = "mouse",
        diagnose: bool = False,
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
            method: 活动方式，"mouse" 或 "keyboard" / Activity method, "mouse" or "keyboard"
            diagnose: 是否输出系统空闲时间诊断信息（Windows）/ Whether to print idle-time diagnostics (Windows)
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
                idle_before = get_system_idle_seconds() if diagnose else None

                # 执行移动或按键 / Perform move or key press
                if method == "keyboard":
                    current_pos, move_count, success = self.perform_key_press(move_count)
                else:
                    current_pos, move_count, success = self.perform_move(move_count)
                if success:
                    success_count += 1

                elapsed = self.time_func() - start_time

                if diagnose:
                    idle_after = get_system_idle_seconds()
                    # Windows 下：如果 idle_before/after 没变化，说明系统未把这次操作计入“真实输入”
                    # On Windows: if idle doesn't change, system likely didn't count this as real input
                    self.print_func(
                        f"[{int(elapsed)}s] diagnose: idle_before={idle_before}, idle_after={idle_after} (seconds)"
                    )

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


def move_mouse(
    interval: int = 60,
    duration: Optional[int] = None,
    verbose: bool = False,
    method: str = "mouse",
) -> None:
    """
    自动移动鼠标 / Automatically move mouse
    这是主要的公共 API，保持向后兼容性

    Args:
        interval: 移动间隔（秒），默认60秒 / Movement interval (seconds), default 60
        duration: 运行时长（秒），None表示无限运行 / Duration (seconds), None means infinite
        verbose: 是否显示详细日志 / Whether to show verbose logs
        method: 活动方式，"mouse"（鼠标移动）或 "keyboard"（键盘按键），默认 "mouse" /
            Activity method, "mouse" or "keyboard", default "mouse"
    """
    mover = MouseMover()
    success_count = [0]  # 使用列表以便在闭包中修改 / Use list to allow modification in closure

    def on_start():
        if method == "keyboard":
            mover.print_func("开始自动按键保持活动...")
            mover.print_func("Starting keyboard keepalive...")
        else:
            mover.print_func("开始自动移动鼠标...")
            mover.print_func("Starting mouse keepalive...")
        mover.print_func(f"活动方式: {method} / Method: {method}")
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

        if method == "keyboard":
            if verbose:
                status = "成功" if success else "失败"
                mover.print_func(
                    f"[{int(elapsed)}s] 已按键 {move_count} 次 (状态: {status}) / "
                    f"Pressed key {move_count} times (status: {status})"
                )
            elif success:
                mover.print_func(f"[{int(elapsed)}s] 已按键 {move_count} 次 / Pressed key {move_count} times")
            elif not success:
                mover.print_func(f"[{int(elapsed)}s] 警告: 按键失败 / Warning: Key press failed (attempt {move_count})")
        else:
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
                # 非详细模式下，每次成功移动都输出日志（包含坐标） / In non-verbose mode, output every successful move (with coordinates)
                mover.print_func(
                    f"[{int(elapsed)}s] 已移动鼠标 {move_count} 次 "
                    f"(位置: {current_pos.x}, {current_pos.y}) / "
                    f"Moved mouse {move_count} times "
                    f"(position: {current_pos.x}, {current_pos.y})"
                )
            elif not success:
                # 移动失败时也输出警告 / Output warning when move fails
                mover.print_func(
                    f"[{int(elapsed)}s] 警告: 鼠标移动失败 / Warning: Mouse movement failed (attempt {move_count})"
                )

    def on_finish(move_count: int, elapsed: float):
        if duration:
            mover.print_func(f"\n达到运行时长 {duration} 秒，程序退出")
            mover.print_func(f"Duration {duration} seconds reached, exiting")
        else:
            mover.print_func("\n\n程序被用户中断")
            mover.print_func("Program interrupted by user")
        if method == "keyboard":
            mover.print_func(f"总共按键 {move_count} 次 / Total key presses: {move_count}")
        else:
            mover.print_func(f"总共移动鼠标 {move_count} 次 / Total moves: {move_count}")
        if method == "keyboard":
            mover.print_func(f"成功按键: {success_count[0]} 次 / Successful key presses: {success_count[0]}")
        else:
            mover.print_func(f"成功移动: {success_count[0]} 次 / Successful moves: {success_count[0]}")
        mover.print_func(f"运行时长: {int(elapsed)} 秒 / Duration: {int(elapsed)} seconds")

    try:
        mover.run(
            interval=interval,
            duration=duration,
            verbose=verbose,
            method=method,
            diagnose=False,
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
  mouse-keepalive -m keyboard         # 使用键盘按键方式（推荐用于 Teams） / Use keyboard method (recommended for Teams)
  mouse-keepalive -m mouse            # 使用鼠标移动方式（默认） / Use mouse method (default)
  mouse-keepalive --diagnose          # 输出 Windows 系统 idle 秒数（诊断 Teams 为何不认） / Print Windows idle seconds (diagnose)
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

    parser.add_argument(
        "-m",
        "--method",
        type=str,
        choices=["mouse", "keyboard"],
        default="mouse",
        help=(
            "活动方式：mouse（鼠标移动）或 keyboard（键盘按键）。键盘方式对 Teams 等应用更有效 / "
            "Activity method: mouse or keyboard. Keyboard method is more effective for Teams"
        ),
    )

    parser.add_argument(
        "--diagnose",
        action="store_true",
        help=(
            "输出 Windows 系统 idle 秒数（用于诊断 Teams 为何不把模拟输入算作活动） / "
            "Print Windows idle seconds to diagnose why Teams may not count simulated input"
        ),
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

    # 直接走 MouseMover.run，这样可以透传 diagnose 参数，同时保持 move_mouse() API 的向后兼容
    # Call MouseMover.run directly to pass diagnose, while keeping move_mouse() API backward compatible
    mover = MouseMover()

    def on_start():
        if args.method == "keyboard":
            mover.print_func("开始自动按键保持活动...")
            mover.print_func("Starting keyboard keepalive...")
        else:
            mover.print_func("开始自动移动鼠标...")
            mover.print_func("Starting mouse keepalive...")
        mover.print_func(f"活动方式: {args.method} / Method: {args.method}")
        mover.print_func(f"移动间隔: {args.interval} 秒 / Interval: {args.interval} seconds")
        if args.duration:
            mover.print_func(f"运行时长: {args.duration} 秒 / Duration: {args.duration} seconds")
        else:
            mover.print_func("运行时长: 无限（按 Ctrl+C 停止） / Duration: Infinite (Press Ctrl+C to stop)")
        mover.print_func(f"操作系统: {platform.system()} / OS: {platform.system()}")
        if args.verbose:
            mover.print_func("详细模式: 已启用 / Verbose mode: Enabled")
        if args.diagnose:
            mover.print_func(
                "诊断模式: 已启用（将输出 Windows idle 秒数） / Diagnose: Enabled (prints Windows idle seconds)"
            )
        mover.print_func("-" * 50)

    def on_move(move_count: int, current_pos: MousePosition, elapsed: float, success: bool):
        # 复用 move_mouse() 的输出逻辑（保持一致）
        # Reuse the same output behavior as move_mouse()
        status = "成功" if success else "失败"
        if args.method == "keyboard":
            if args.verbose:
                mover.print_func(
                    f"[{int(elapsed)}s] 已按键 {move_count} 次 (状态: {status}) / "
                    f"Pressed key {move_count} times (status: {status})"
                )
            elif success:
                mover.print_func(f"[{int(elapsed)}s] 已按键 {move_count} 次 / Pressed key {move_count} times")
            else:
                mover.print_func(f"[{int(elapsed)}s] 警告: 按键失败 / Warning: Key press failed (attempt {move_count})")
        else:
            if args.verbose:
                mover.print_func(
                    f"[{int(elapsed)}s] 已移动鼠标 {move_count} 次 (当前位置: {current_pos.x}, {current_pos.y}, 状态: {status})"
                )
                status_text = "success" if success else "failed"
                mover.print_func(
                    f"[{int(elapsed)}s] Moved mouse {move_count} times "
                    f"(current position: {current_pos.x}, {current_pos.y}, status: {status_text})"
                )
            elif success:
                mover.print_func(
                    f"[{int(elapsed)}s] 已移动鼠标 {move_count} 次 "
                    f"(位置: {current_pos.x}, {current_pos.y}) / "
                    f"Moved mouse {move_count} times "
                    f"(position: {current_pos.x}, {current_pos.y})"
                )
            else:
                mover.print_func(
                    f"[{int(elapsed)}s] 警告: 鼠标移动失败 / Warning: Mouse movement failed (attempt {move_count})"
                )

    def on_finish(move_count: int, elapsed: float):
        if args.duration:
            mover.print_func(f"\n达到运行时长 {args.duration} 秒，程序退出")
            mover.print_func(f"Duration {args.duration} seconds reached, exiting")
        else:
            mover.print_func("\n\n程序被用户中断")
            mover.print_func("Program interrupted by user")
        if args.method == "keyboard":
            mover.print_func(f"总共按键 {move_count} 次 / Total key presses: {move_count}")
        else:
            mover.print_func(f"总共移动鼠标 {move_count} 次 / Total moves: {move_count}")
        mover.print_func(f"运行时长: {int(elapsed)} 秒 / Duration: {int(elapsed)} seconds")

    try:
        mover.run(
            interval=args.interval,
            duration=args.duration,
            verbose=args.verbose,
            method=args.method,
            diagnose=args.diagnose,
            on_start=on_start,
            on_move=on_move,
            on_finish=on_finish,
        )
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
