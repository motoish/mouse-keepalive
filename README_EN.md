# Mouse Keepalive

[中文](README.md) | **English**

A cross-platform tool that periodically moves the mouse to prevent system sleep or lock.  
Supports **macOS, Windows, and Linux**.

---

## ✨ Features

- Cross-platform
- Configurable movement interval and duration
- Nearly imperceptible mouse movement
- Install via PyPI or npm
- Simple CLI: `mouse-keepalive` / `mka`

---

## 📦 Installation

### PyPI (Recommended)

```bash
pip install mouse-keepalive
# or
pipx install mouse-keepalive
```

### npm

```bash
npm install -g mouse-keepalive
```

---

## 🚀 Quick Start

```bash
# Default: move every 60 seconds
mka

# Every 30 seconds
mka -i 30

# Every 2 minutes, stops after 1 hour
mka -i 120 -d 3600

# Show help
mka --help
```

You can also run:

```bash
mouse-keepalive
python -m mouse_keepalive
```

---

## ⚙️ Options

| Option | Description | Default |
|--------|-------------|---------|
| `-i, --interval` | Movement interval (seconds) | 60 |
| `-d, --duration` | Run duration (seconds) | Infinite |
| `-h, --help` | Show help | — |

---

## 🧠 How It Works

The program periodically moves the mouse a tiny amount (1–2 pixels)  
and immediately returns it, preventing the system from detecting inactivity.

---

## ⚠️ Notes

- Stop anytime with **Ctrl + C**  
- **macOS** may require Accessibility permission  
- Some security software or enterprise policies may block automatic mouse movement.  
  If blocked, add to whitelist or contact your administrator

---

## 📄 License

MIT
