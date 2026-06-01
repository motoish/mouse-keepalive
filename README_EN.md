# Mouse Keepalive

[中文](README.md) | **English**

A cross-platform CLI that nudges the mouse on a schedule and returns it to the original position, helping prevent sleep or lock when the system sees no pointer activity.  
Works on **macOS, Windows, and Linux**.

---

## ✨ Features

- Cross-platform (Python + [pyautogui](https://pypi.org/project/PyAutoGUI/))
- Configurable interval and total run duration
- Instant micro-movements (~1–2 px), usually unnoticeable
- Install via **PyPI** or **npm**; short alias `mka`
- Logs each move by default; use `-q` for silent mode

---

## 📋 Requirements

| Method | Requirements |
|--------|----------------|
| **PyPI / pipx** (recommended) | Python **3.11+** |
| **npm** | Node.js **14+** and **Python 3.11+** on the machine (the npm package is a launcher; logic runs in Python) |
| **From source** | Python 3.11+; see [Local development](#-local-development) |

---

## 📦 Installation

### PyPI (recommended)

```bash
pip install mouse-keepalive
# or (isolated env, good for desktop use)
pipx install mouse-keepalive
```

### npm

```bash
npm install -g mouse-keepalive
```

Ensure Python 3.11+ is available. If `pyautogui` is missing, the npm entrypoint will try `pip install pyautogui` automatically.

---

## 🚀 Quick start

```bash
# Default: move every 60s until Ctrl+C
mka

# Every 30 seconds
mka -i 30

# Every 2 minutes, stop after 1 hour
mka -i 120 -d 3600

# Silent mode (no logs)
mka -q

# Help
mka --help
```

Equivalent commands:

```text
mouse-keepalive
python -m mouse_keepalive
```

---

## ⚙️ CLI options

| Option | Description | Default |
|--------|-------------|---------|
| `-i, --interval` | Seconds between moves | `60` |
| `-d, --duration` | Total run time (seconds); omit to run until Ctrl+C | Unlimited |
| `-q, --quiet` | No log output | Off |
| `-h, --help` | Show help | — |

---

## 🧠 How it works

On each tick the tool reads the cursor position, shifts it by 1–2 pixels, then **moves back immediately** so the OS still sees activity without a visible pointer jump.

---

## 🛠 Local development

The repo uses a **src layout** (`src/mouse_keepalive/`); the import name remains `mouse_keepalive`.

```bash
git clone https://github.com/motoish/mouse-keepalive.git
cd mouse-keepalive

# Editable install + dev tools
pip install -e ".[dev]"

# Option 1: root script (pick up code changes without reinstall)
./move_mouse.sh
./move_mouse.sh -i 30 -q

# Option 2: Makefile
make run ARGS="-i 30"

# Option 3: installed CLI
mka -i 30

# Test & lint
make test
make lint
```

`move_mouse.sh` prefers `.venv/bin/python` and sets `PYTHONPATH=src`. It is **not** shipped on PyPI/npm.

### Layout (overview)

```text
mouse-keepalive/
├── src/mouse_keepalive/   # Python package
├── bin/                   # npm CLI → python -m mouse_keepalive
├── tests/
├── move_mouse.sh          # local dev only
└── pyproject.toml
```

---

## ⚠️ Notes

- Press **Ctrl + C** to stop  
- On **macOS**, grant Accessibility access to your terminal or Python  
- Corporate security tools may block synthetic mouse input; whitelist or ask your admin if it fails  

---

## 📦 Releases

Published versions: [PyPI](https://pypi.org/project/mouse-keepalive/) · [npm](https://www.npmjs.com/package/mouse-keepalive).  
See [CHANGELOG.md](CHANGELOG.md). This repo uses [release-please](https://github.com/googleapis/release-please); merging the release PR creates a `v*` tag and publishes to npm and PyPI.

---

## 📄 License

[MIT](LICENSE)
