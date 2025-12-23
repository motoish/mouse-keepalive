@echo off
REM 自动移动鼠标脚本 - Windows 批处理入口 / Auto Mouse Mover Script - Windows Batch Entry
REM 适用于 Windows 命令提示符和 PowerShell / For Windows Command Prompt and PowerShell

setlocal

set SCRIPT_DIR=%~dp0

REM 检查 Python 是否安装 / Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    where python3 >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo 错误: 未找到 Python
        echo Error: Python not found
        echo 请先安装 Python 3.6 或更高版本
        echo Please install Python 3.6 or higher
        exit /b 1
    ) else (
        set PYTHON_CMD=python3
    )
) else (
    set PYTHON_CMD=python
)

echo 使用 Python: %PYTHON_CMD%
echo Using Python: %PYTHON_CMD%

REM 检查 pyautogui 是否安装 / Check if pyautogui is installed
%PYTHON_CMD% -c "import pyautogui" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo 警告: pyautogui 未安装
    echo Warning: pyautogui not installed
    echo 正在尝试安装...
    echo Attempting to install...
    %PYTHON_CMD% -m pip install pyautogui
    if %ERRORLEVEL% NEQ 0 (
        echo 错误: 无法安装 pyautogui
        echo Error: Failed to install pyautogui
        echo 请手动运行: pip install pyautogui
        echo Please run manually: pip install pyautogui
        exit /b 1
    )
)

REM 运行 Python 模块并传递所有参数 / Run Python module and pass all arguments
%PYTHON_CMD% -m auto_mouse_mover %*

endlocal

