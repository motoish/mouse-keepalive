# 自动移动鼠标工具

一个跨平台的自动移动鼠标工具，可以防止系统进入休眠或锁定状态。支持 macOS、Windows 和 Linux 系统。

## 功能特点

- ✅ 跨平台支持（macOS、Windows 和 Linux）
- ✅ 可自定义移动间隔时间
- ✅ 可设置运行时长
- ✅ 鼠标移动几乎无感知（移动后立即返回原位置）
- ✅ 实时显示运行状态
- ✅ 支持 npm 安装，使用简单

## 安装方式

### 方式一：npm 安装（推荐）

```bash
# 全局安装
npm install -g auto-mouse-mover

# 或使用简短别名
npm install -g auto-mouse-mover
```

安装后可以使用以下命令：

```bash
# 使用完整命令名
auto-mouse-mover

# 或使用简短别名
amm
```

### 方式二：Python 脚本（传统方式）

#### 系统要求

- Python 3.11 或更高版本
- pyautogui 库

#### 安装步骤

1. 安装 Python 依赖：

```bash
pip install -r requirements.txt
```

或者直接安装：

```bash
pip install pyautogui
```

2. 给脚本添加执行权限（macOS/Linux）：

```bash
chmod +x move_mouse.sh
chmod +x move_mouse.py
```

## 使用方法

### npm 安装方式（推荐）

```bash
# 默认：每60秒移动一次，无限运行
auto-mouse-mover
# 或
amm

# 指定移动间隔为30秒
auto-mouse-mover -i 30
# 或
amm -i 30

# 指定移动间隔和运行时长（1小时 = 3600秒）
auto-mouse-mover -i 120 -d 3600
# 或
amm -i 120 -d 3600

# 查看帮助
auto-mouse-mover --help
```

### Python 脚本方式

#### macOS / Linux

使用 Shell 脚本：

```bash
# 默认：每60秒移动一次，无限运行
./move_mouse.sh

# 指定移动间隔为30秒
./move_mouse.sh -i 30

# 指定移动间隔和运行时长（1小时 = 3600秒）
./move_mouse.sh -i 120 -d 3600
```

或直接使用 Python 脚本：

```bash
python3 move_mouse.py
python3 move_mouse.py -i 30
python3 move_mouse.py -i 120 -d 3600
```

#### Windows

使用批处理文件：

```cmd
REM 默认：每60秒移动一次，无限运行
move_mouse.bat

REM 指定移动间隔为30秒
move_mouse.bat -i 30

REM 指定移动间隔和运行时长
move_mouse.bat -i 120 -d 3600
```

或直接使用 Python 脚本：

```cmd
python move_mouse.py
python move_mouse.py -i 30
python move_mouse.py -i 120 -d 3600
```

## 参数说明

- `-i, --interval`: 鼠标移动间隔（秒），默认60秒
- `-d, --duration`: 运行时长（秒），默认无限运行
- `-h, --help`: 显示帮助信息

## 使用示例

### npm 方式

```bash
# 每30秒移动一次鼠标，防止系统锁定
amm -i 30

# 每2分钟移动一次，运行1小时后自动停止
amm -i 120 -d 3600

# 停止程序：按 Ctrl+C
```

### Python 方式

```bash
# 每30秒移动一次鼠标，防止系统锁定
./move_mouse.sh -i 30

# 每2分钟移动一次，运行1小时后自动停止
./move_mouse.sh -i 120 -d 3600

# 停止程序：按 Ctrl+C
```

## 工作原理

脚本会定期将鼠标移动1-2像素，然后立即移回原位置。这样既不会影响用户的正常使用，又能防止系统检测到鼠标静止而进入休眠或锁定状态。

## 注意事项

1. 程序运行时，按 `Ctrl+C` 可以随时停止
2. 鼠标移动幅度很小，几乎不会被察觉
3. 如果系统有屏幕保护程序，此工具可以帮助防止触发
4. 在某些安全软件可能会检测到自动鼠标移动行为

## 许可证

MIT License

## 代码质量检查

项目使用 GitHub Actions 自动运行多种 linter 来确保代码质量：

- **Python**: flake8, black, pylint, mypy
- **Shell**: ShellCheck
- **Markdown**: markdownlint
- **YAML**: yamllint
- **Batch**: 基础语法检查

每次推送代码或创建 Pull Request 时，GitHub Actions 会自动运行这些检查。

### 本地运行 Linter

如果你想在本地运行这些检查：

```bash
# Python linting
pip install flake8 black pylint mypy
flake8 move_mouse.py
black --check move_mouse.py
pylint move_mouse.py
mypy move_mouse.py

# Shell linting (需要安装 shellcheck)
shellcheck move_mouse.sh

# Markdown linting (需要安装 markdownlint-cli)
npm install -g markdownlint-cli
markdownlint "*.md"

# YAML linting
pip install yamllint
yamllint .github/workflows/*.yml
```

## 依赖管理

项目使用 [Renovate](https://github.com/renovatebot/renovate) 自动维护依赖版本：

- **自动更新**: 每月第一个工作日上午 11 点前自动检查并更新依赖
- **自动合并**: Patch 版本更新会自动通过测试后合并
- **分组管理**: 相关依赖会被分组到同一个 PR 中
- **安全更新**: 安全相关的更新会优先处理

### Renovate 配置

配置文件位于 `renovate.json`，主要特性：

- 自动维护 Python 依赖（requirements.txt）
- 自动维护 GitHub Actions 版本
- 自动维护 npm 依赖（如 markdownlint-cli）
- Patch 版本自动合并
- Minor/Major 版本需要手动审查

### 自动批准机制

当 Renovate 创建的 PR 通过所有测试后，GitHub Actions 会自动批准并合并（仅限 patch 版本更新）。

## 发布到 npm

如果你想将本项目发布到 npm：

```bash
# 1. 登录 npm（如果还没有登录）
npm login

# 2. 检查包名是否可用（可选）
npm view auto-mouse-mover

# 3. 发布
npm publish

# 4. 验证发布
npm view auto-mouse-mover
```

**注意**: 发布前请确保：
- 已更新 `package.json` 中的版本号
- 已测试所有功能
- 已更新 README 文档
- 已添加 LICENSE 文件

## 贡献

欢迎提交 Issue 和 Pull Request！

在提交代码前，请确保所有 linter 检查通过。

