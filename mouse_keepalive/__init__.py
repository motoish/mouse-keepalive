"""
自动移动鼠标工具 / Mouse Keepalive Tool
支持 macOS、Windows 和 Linux 系统 / Supports macOS, Windows and Linux

模块化架构：
- 核心逻辑在 move_mouse 模块中实现
- 所有入口点（CLI、模块调用）都使用相同的核心逻辑
- 支持依赖注入，便于测试
"""

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    # Python < 3.8
    from importlib_metadata import version, PackageNotFoundError  # type: ignore[no-redef]

try:
    __version__ = version("mouse-keepalive")
except PackageNotFoundError:
    # 如果包未安装，使用硬编码版本 / Fallback if package not installed
    __version__ = "1.2.1"

__author__ = "motoish"

from .move_mouse import move_mouse, main, MouseMover, MouseController, MousePosition, ScreenSize

__all__ = ["move_mouse", "main", "MouseMover", "MouseController", "MousePosition", "ScreenSize"]
