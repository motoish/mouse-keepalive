# Auto Mouse Mover

一个可以指定时间间隔自动移动鼠标的工具，支持 macOS 和 Windows 系统。

## 功能特性

- ✅ 支持 macOS 和 Windows
- ✅ 可自定义移动间隔时间
- ✅ 最小化移动距离（仅移动1像素，几乎不可见）
- ✅ 多种实现方式（Shell脚本和Python脚本）

## 使用方法

### macOS

#### 方式1: 使用 Bash 脚本

```bash
# 给脚本添加执行权限
chmod +x move-mouse.sh

# 使用默认间隔（60秒）
./move-mouse.sh

# 指定间隔时间（例如：每30秒移动一次）
./move-mouse.sh 30
```

#### 方式2: 使用 Python 脚本（推荐，跨平台）

```bash
# 安装依赖
pip install pyautogui

# 使用默认间隔（60秒）
python3 move-mouse.py

# 指定间隔时间（例如：每30秒移动一次）
python3 move-mouse.py 30
```

### Windows

#### 方式1: 使用 PowerShell 脚本

```powershell
# 使用默认间隔（60秒）
.\move-mouse.ps1

# 指定间隔时间（例如：每30秒移动一次）
.\move-mouse.ps1 30
```

**注意**: 如果遇到执行策略限制，需要先运行：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 方式2: 使用 Python 脚本（推荐，跨平台）

```cmd
# 安装依赖
pip install pyautogui

# 使用默认间隔（60秒）
python move-mouse.py

# 指定间隔时间（例如：每30秒移动一次）
python move-mouse.py 30
```

## 停止脚本

按 `Ctrl+C` 停止脚本运行。

## 文件说明

- `move-mouse.sh` - macOS/Linux 的 Bash 脚本
- `move-mouse.ps1` - Windows 的 PowerShell 脚本
- `move-mouse.py` - 跨平台的 Python 脚本（推荐使用）

## 依赖要求

### Python 版本
- Python 3.6+
- pyautogui 库

安装方法：
```bash
pip install pyautogui
```

### macOS Bash 版本
- macOS 系统
- 需要授予终端"辅助功能"权限（系统偏好设置 > 安全性与隐私 > 辅助功能）

### Windows PowerShell 版本
- Windows 系统
- PowerShell 5.1+ 或 PowerShell Core

## 工作原理

脚本会定期（根据指定的时间间隔）将鼠标移动1像素，然后立即移回原位置。这个移动非常微小，几乎不可见，但足以防止系统进入睡眠模式或触发屏幕保护程序。

## 注意事项

1. **macOS 权限**: 首次运行时，macOS 可能会要求授予终端"辅助功能"权限
2. **Windows 执行策略**: PowerShell 脚本可能需要调整执行策略
3. **Python 版本**: 推荐使用 Python 脚本，因为它跨平台且更易维护
4. **使用场景**: 适用于需要保持系统活跃状态的场景，如长时间下载、编译等

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

