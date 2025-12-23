#!/bin/bash
#
# 自动移动鼠标脚本 - Shell 入口 / Auto Mouse Mover Script - Shell Entry
# 支持 macOS 和 Windows (Git Bash) / Supports macOS and Windows (Git Bash)
#

# 获取脚本所在目录 / Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 检测操作系统 / Detect operating system
detect_os() {
    case "$(uname -s)" in
        Darwin*)
            echo "macOS"
            ;;
        Linux*)
            echo "Linux"
            ;;
        MINGW*|MSYS*|CYGWIN*)
            echo "Windows"
            ;;
        *)
            echo "Unknown"
            ;;
    esac
}

# 检查 Python 是否安装 / Check if Python is installed
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        echo "错误: 未找到 Python"
        echo "Error: Python not found"
        echo "请先安装 Python 3.6 或更高版本"
        echo "Please install Python 3.6 or higher"
        exit 1
    fi
}

# 检查 pyautogui 是否安装 / Check if pyautogui is installed
check_pyautogui() {
    if ! $PYTHON_CMD -c "import pyautogui" 2>/dev/null; then
        echo "警告: pyautogui 未安装"
        echo "Warning: pyautogui not installed"
        echo "正在尝试安装..."
        echo "Attempting to install..."
        $PYTHON_CMD -m pip install pyautogui
        if [ $? -ne 0 ]; then
            echo "错误: 无法安装 pyautogui"
            echo "Error: Failed to install pyautogui"
            echo "请手动运行: pip install pyautogui"
            echo "Please run manually: pip install pyautogui"
            exit 1
        fi
    fi
}

# 主函数 / Main function
main() {
    OS=$(detect_os)
    echo "检测到操作系统: $OS"
    echo "Detected OS: $OS"

    check_python
    echo "使用 Python: $PYTHON_CMD"
    echo "Using Python: $PYTHON_CMD"

    check_pyautogui

    # 解析参数并传递给 Python 模块 / Parse arguments and pass to Python module
    $PYTHON_CMD -m auto_mouse_mover "$@"
}

# 运行主函数 / Run main function
main "$@"

