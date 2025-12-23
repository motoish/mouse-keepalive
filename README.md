# 自动移动鼠标工具

**中文** | [English](README_EN.md)

一个跨平台的自动移动鼠标工具，可以防止系统进入休眠或锁定状态。支持 macOS、Windows 和 Linux 系统。

## 功能特点

- ✅ 跨平台支持（macOS、Windows 和 Linux）
- ✅ 可自定义移动间隔时间
- ✅ 可设置运行时长
- ✅ 鼠标移动几乎无感知（移动后立即返回原位置）
- ✅ 实时显示运行状态
- ✅ 支持 npm 和 PyPI 安装，使用简单

## 安装方式

### 方式一：PyPI 安装（Python 用户推荐）

```bash
# 使用 pip 安装
pip install auto-mouse-mover

# 或使用 pipx（推荐，隔离环境）
pipx install auto-mouse-mover
```

安装后可以使用以下命令：

```bash
# 使用完整命令名
auto-mouse-mover

# 或使用简短别名
amm

# 或使用模块方式
python -m auto_mouse_mover
```

### 方式二：npm 安装（Node.js 用户推荐）

```bash
# 全局安装
npm install -g auto-mouse-mover
```

安装后可以使用以下命令：

```bash
# 使用完整命令名
auto-mouse-mover

# 或使用简短别名
amm
```

### 方式三：Python 脚本（开发/传统方式）

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
```

## 使用方法

### PyPI/npm 安装方式（推荐）

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

# Python 模块方式运行
python -m auto_mouse_mover -i 30
```

### 本地 Python 脚本方式

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

或直接使用 Python 模块：

```bash
python3 -m auto_mouse_mover
python3 -m auto_mouse_mover -i 30
python3 -m auto_mouse_mover -i 120 -d 3600
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

或直接使用 Python 模块：

```cmd
python -m auto_mouse_mover
python -m auto_mouse_mover -i 30
python -m auto_mouse_mover -i 120 -d 3600
```

## 参数说明

- `-i, --interval`: 鼠标移动间隔（秒），默认60秒
- `-d, --duration`: 运行时长（秒），默认无限运行
- `-h, --help`: 显示帮助信息

## 使用示例

### PyPI/npm 安装方式

```bash
# 每30秒移动一次鼠标，防止系统锁定
amm -i 30

# 每2分钟移动一次，运行1小时后自动停止
amm -i 120 -d 3600

# 停止程序：按 Ctrl+C
```

### 本地 Python 脚本方式

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

使用 Makefile 简化命令：

```bash
# 安装开发依赖（首次使用）
make install-dev

# 运行所有 linter
make lint

# 运行特定 linter
make lint-python    # Python linters
make lint-shell     # Shell linter
make lint-markdown  # Markdown linter
make lint-yaml      # YAML linter

# 格式化代码
make format         # 格式化所有代码
make format-python  # 仅格式化 Python 代码

# 查看所有可用命令
make help
```

**注意**: `shellcheck` 需要单独安装：
- macOS: `brew install shellcheck`
- Ubuntu/Debian: `sudo apt-get install shellcheck`
- Fedora: `sudo dnf install ShellCheck`

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

## 发布到 PyPI 和 npm

本项目同时支持发布到 PyPI 和 npm。

### 自动发布（推荐）✨

本项目使用 [release-please](https://github.com/googleapis/release-please-action) 自动管理版本和发布流程。

**工作原理：**
1. 当你提交符合 [Conventional Commits](https://www.conventionalcommits.org/) 规范的代码时，release-please 会自动：
   - 根据提交类型决定版本号（`feat:` → minor, `fix:` → patch, `BREAKING CHANGE` → major）
   - 创建包含版本更新和 CHANGELOG 的 Pull Request
   - 当你合并 PR 后，自动创建 GitHub Release 和 tag
   - 触发发布工作流，自动发布到 npm 和 PyPI

**提交规范示例：**
```bash
feat: add new feature          # 1.0.0 → 1.1.0
fix: fix bug                  # 1.0.0 → 1.0.1
feat!: breaking change        # 1.0.0 → 2.0.0
docs: update documentation    # 1.0.0 → 1.0.1
```

**手动触发发布：**
- 前往 GitHub Actions → "Release Please" → "Run workflow"

### 手动发布（备用）

**PyPI:**
```bash
# 1. 安装构建工具
pip install build twine

# 2. 构建包
python -m build

# 3. 发布到 PyPI
twine upload dist/*
```

**npm:**
```bash
# 1. 登录 npm
npm login

# 2. 发布
npm publish
```

**注意**: 发布前请确保：
- 已更新版本号（`pyproject.toml` 和 `package.json`）
- 已测试所有功能
- 已更新 README 文档
- 已添加 LICENSE 文件

## 贡献

欢迎提交 Issue 和 Pull Request！

在提交代码前，请确保所有 linter 检查通过。
