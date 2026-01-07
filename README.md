# Mouse Keepalive

**中文** | [English](README_EN.md)

一个跨平台的自动移动鼠标工具，用于防止系统进入休眠或锁屏。  
支持 **macOS / Windows / Linux**。

---

## ✨ 功能亮点

- 跨平台支持  
- 可配置鼠标移动间隔与运行时长  
- 鼠标几乎无感移动（移动后立即恢复原位置）  
- 支持 PyPI 和 npm 安装  
- 简洁 CLI：`mouse-keepalive` / `mka`

---

## 📦 安装指南

### PyPI（推荐）

```bash
pip install mouse-keepalive
# 或
pipx install mouse-keepalive
```

### npm

```bash
npm install -g mouse-keepalive
```

---

## 🚀 快速开始

```bash
# 默认：每 60 秒移动一次
mka

# 每 30 秒移动一次
mka -i 30

# 每 2 分钟移动一次，运行 1 小时
mka -i 120 -d 3600

# 查看帮助
mka --help
```

也可以使用：

```
mouse-keepalive
python -m mouse_keepalive
```

---

## ⚙️ 可用参数

| 参数 | 说明 | 默认 |
|------|------|------|
| `-i, --interval` | 移动间隔（秒） | 60 |
| `-d, --duration` | 运行时长（秒） | 无限 |
| `-h, --help` | 显示帮助 | — |

---

## 🧠 工作原理

程序会定期将鼠标轻微移动（1–2 像素），然后立即移回原位，  
从而避免系统检测到长时间鼠标静止而进入休眠或锁屏。

---

## ⚠️ 注意事项

- 按 **Ctrl + C** 可随时停止程序  
- **macOS** 可能需要授权「辅助功能」权限  
- 部分安全软件或企业策略可能会阻止自动鼠标移动。  
  若被拦截，请加入信任白名单或咨询管理员

---

## 📄 许可证

MIT
