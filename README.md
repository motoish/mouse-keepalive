# Mouse Keepalive

**中文** | [English](README_EN.md)

跨平台 CLI 工具：按固定间隔轻微移动鼠标并立即回位，避免系统因长时间无操作而休眠或锁屏。  
支持 **macOS / Windows / Linux**。

---

## ✨ 功能亮点

- 跨平台（Python + [pyautogui](https://pypi.org/project/PyAutoGUI/)）
- 可配置移动间隔与总运行时长
- 瞬时微移（约 1–2 像素），日常使用几乎无感
- **PyPI** 与 **npm** 均可安装；命令行别名 `mka`
- 默认输出每次移动日志；`-q` 可完全静默

---

## 📋 环境要求

| 方式 | 要求 |
|------|------|
| **PyPI / pipx**（推荐） | Python **3.11+** |
| **npm** | Node.js **14+**，且本机已安装 **Python 3.11+**（npm 包为启动器，实际逻辑在 Python 中） |
| **从源码运行** | Python 3.11+；见下方「本地开发」 |

---

## 📦 安装

### PyPI（推荐）

```bash
pip install mouse-keepalive
# 或（隔离环境，推荐桌面使用）
pipx install mouse-keepalive
```

### npm

```bash
npm install -g mouse-keepalive
```

首次运行前请确保已安装 Python 3.11+；若缺少 `pyautogui`，npm 入口会尝试自动 `pip install pyautogui`。

---

## 🚀 快速开始

```bash
# 默认：每 60 秒移动一次，Ctrl+C 停止
mka

# 每 30 秒移动一次
mka -i 30

# 每 2 分钟移动一次，共运行 1 小时
mka -i 120 -d 3600

# 静默模式（无日志）
mka -q

# 帮助
mka --help
```

等效命令：

```text
mouse-keepalive
python -m mouse_keepalive
```

---

## ⚙️ 命令行参数

| 参数 | 说明 | 默认 |
|------|------|------|
| `-i, --interval` | 移动间隔（秒） | `60` |
| `-d, --duration` | 运行总时长（秒）；省略则一直运行 | 无限 |
| `-q, --quiet` | 静默模式，不输出日志 | 关闭 |
| `-h, --help` | 显示帮助 | — |

---

## 🧠 工作原理

程序按间隔获取当前光标位置，偏移 1–2 像素后**立即移回**，使系统仍检测到鼠标活动，同时尽量不打扰正常使用。

---

## 🛠 本地开发

仓库采用 **src 布局**，包路径为 `src/mouse_keepalive/`（对外导入名仍为 `mouse_keepalive`）。

```bash
git clone https://github.com/motoish/mouse-keepalive.git
cd mouse-keepalive

# 可编辑安装 + 开发依赖
pip install -e ".[dev]"

# 方式一：仓库根目录脚本（改代码后无需重装）
./move_mouse.sh
./move_mouse.sh -i 30 -q

# 方式二：Makefile
make run ARGS="-i 30"

# 方式三：安装后的 CLI
mka -i 30

# 测试与检查
make test
make lint
```

`move_mouse.sh` 会优先使用 `.venv/bin/python`，并通过 `PYTHONPATH=src` 加载源码；**不会**随 PyPI/npm 包发布。

### 目录结构（简要）

```text
mouse-keepalive/
├── src/mouse_keepalive/   # Python 包
├── bin/                   # npm CLI（转发到 python -m mouse_keepalive）
├── tests/
├── move_mouse.sh          # 仅本地开发
└── pyproject.toml
```

---

## ⚠️ 注意事项

- 使用 **Ctrl + C** 可随时退出  
- **macOS** 需在「系统设置 → 隐私与安全性 → 辅助功能」中允许终端或 Python  
- 企业安全策略可能拦截模拟鼠标；若无效请联系管理员或加入白名单  

---

## 📦 发布与版本

用户安装版本以 [PyPI](https://pypi.org/project/mouse-keepalive/) / [npm](https://www.npmjs.com/package/mouse-keepalive) 为准。  
变更记录见 [CHANGELOG.md](CHANGELOG.md)。仓库使用 [release-please](https://github.com/googleapis/release-please) 管理版本；合并 Release PR 后会发布 `v*` 标签并自动发布到 npm / PyPI。

---

## 📄 许可证

[MIT](LICENSE)
