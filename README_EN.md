# Auto Mouse Mover

[中文](README.md) | **English**

A cross-platform tool to automatically move the mouse at specified intervals to prevent system sleep or lock. Supports macOS, Windows, and Linux systems.

## Features

- ✅ Cross-platform support (macOS, Windows, and Linux)
- ✅ Customizable movement interval
- ✅ Configurable runtime duration
- ✅ Nearly imperceptible mouse movement (moves and immediately returns to original position)
- ✅ Real-time status display
- ✅ Easy installation via npm and PyPI

## Installation

### Method 1: PyPI Installation (Recommended for Python Users)

```bash
# Install using pip
pip install mouse-keepalive

# Or use pipx (recommended, isolated environment)
pipx install mouse-keepalive
```

After installation, you can use the following commands:

```bash
# Use full command name
mouse-keepalive

# Or use short alias
mka

# Or use module method
python -m mouse_keepalive
```

### Method 2: npm Installation (Recommended for Node.js Users)

```bash
# Global installation
npm install -g mouse-keepalive
```

After installation, you can use the following commands:

```bash
# Use full command name
mouse-keepalive

# Or use short alias
mka
```

### Method 3: Python Script (Development/Traditional Method)

#### System Requirements

- Python 3.11 or higher
- pyautogui library

#### Installation Steps

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

Or install directly:

```bash
pip install pyautogui
```

2. Add execute permission to the script (macOS/Linux):

```bash
chmod +x move_mouse.sh
```

## Usage

### PyPI/npm Installation Method (Recommended)

```bash
# Default: move every 60 seconds, run indefinitely
mouse-keepalive
# or
mka

# Specify movement interval as 30 seconds
mouse-keepalive -i 30
# or
mka -i 30

# Specify movement interval and runtime duration (1 hour = 3600 seconds)
mouse-keepalive -i 120 -d 3600
# or
mka -i 120 -d 3600

# View help
mouse-keepalive --help

# Run as Python module
python -m mouse_keepalive -i 30
```

### Local Python Script Method

#### macOS / Linux

Using Shell script:

```bash
# Default: move every 60 seconds, run indefinitely
./move_mouse.sh

# Specify movement interval as 30 seconds
./move_mouse.sh -i 30

# Specify movement interval and runtime duration (1 hour = 3600 seconds)
./move_mouse.sh -i 120 -d 3600
```

Or use Python module directly:

```bash
python3 -m mouse_keepalive
python3 -m mouse_keepalive -i 30
python3 -m mouse_keepalive -i 120 -d 3600
```

#### Windows

Using batch file:

```cmd
REM Default: move every 60 seconds, run indefinitely
move_mouse.bat

REM Specify movement interval as 30 seconds
move_mouse.bat -i 30

REM Specify movement interval and runtime duration
move_mouse.bat -i 120 -d 3600
```

Or use Python module directly:

```cmd
python -m mouse_keepalive
python -m mouse_keepalive -i 30
python -m mouse_keepalive -i 120 -d 3600
```

## Parameters

- `-i, --interval`: Mouse movement interval (seconds), default 60 seconds
- `-d, --duration`: Runtime duration (seconds), default infinite
- `-h, --help`: Show help information

## Usage Examples

### PyPI/npm Installation Method

```bash
# Move mouse every 30 seconds to prevent system lock
mka -i 30

# Move every 2 minutes, automatically stop after 1 hour
mka -i 120 -d 3600

# Stop program: Press Ctrl+C
```

### Local Python Script Method

```bash
# Move mouse every 30 seconds to prevent system lock
./move_mouse.sh -i 30

# Move every 2 minutes, automatically stop after 1 hour
./move_mouse.sh -i 120 -d 3600

# Stop program: Press Ctrl+C
```

## How It Works

The script periodically moves the mouse by 1-2 pixels and immediately returns it to the original position. This doesn't affect normal user operation while preventing the system from detecting mouse inactivity and entering sleep or lock state.

## Notes

1. **Program Control**: Press `Ctrl+C` to stop the program at any time
2. **Mouse Movement**: Mouse movement is very small (1-2 pixels) and almost imperceptible
3. **Screensaver**: If the system has a screensaver, this tool can help prevent it from triggering
4. **Security Software Warnings** ⚠️:
   - Some security software (antivirus, enterprise security tools) may detect and block automatic mouse movement behavior
   - If blocked, please add the program to your security software's whitelist/trust list
   - Common security software: Windows Defender, enterprise antivirus, EDR (Endpoint Detection and Response) systems, etc.
5. **Enterprise Policy Restrictions** ⚠️:
   - Some enterprise IT policies may prohibit automatic mouse movement programs from running
   - Enterprise environments may use Group Policy or MDM (Mobile Device Management) to restrict such behavior
   - If unable to run, contact your IT administrator for permissions or use alternative solutions
6. **Permission Requirements**:
   - **macOS**: May require "Accessibility" permissions (System Settings → Privacy & Security → Accessibility)
   - **Windows**: Usually no special permissions required, but enterprise environments may have additional restrictions
   - **Linux**: Usually no special permissions required

## License

MIT License

## Code Quality Checks

The project uses GitHub Actions to automatically run multiple linters to ensure code quality:

- **Python**: flake8, black, pylint, mypy
- **Shell**: ShellCheck
- **Markdown**: markdownlint
- **YAML**: yamllint
- **Batch**: Basic syntax check

GitHub Actions automatically runs these checks on every push or Pull Request.

### Running Linters Locally

Use Makefile to simplify commands:

```bash
# Install development dependencies (first time)
make install-dev
# Or use requirements-dev.txt
pip install -r requirements-dev.txt
# Or use pyproject.toml
pip install -e ".[dev]"

# Run all linters
make lint

# Run specific linter
make lint-python    # Python linters
make lint-shell     # Shell linter
make lint-markdown  # Markdown linter
make lint-yaml      # YAML linter

# Format code
make format         # Format all code
make format-python  # Format Python code only

# View all available commands
make help
```

**Note**: `shellcheck` needs to be installed separately:
- macOS: `brew install shellcheck`
- Ubuntu/Debian: `sudo apt-get install shellcheck`
- Fedora: `sudo dnf install ShellCheck`

## Dependency Management

The project uses [Renovate](https://github.com/renovatebot/renovate) to automatically maintain dependency versions:

- **Auto Update**: Automatically checks and updates dependencies before 11 AM on the first working day of each month
- **Auto Merge**: Patch version updates are automatically merged after passing tests
- **Grouped Management**: Related dependencies are grouped into the same PR
- **Security Updates**: Security-related updates are prioritized

### Renovate Configuration

Configuration file is located at `renovate.json`, main features:

- Automatically maintain Python dependencies (requirements.txt)
- Automatically maintain GitHub Actions versions
- Automatically maintain npm dependencies (such as markdownlint-cli)
- Patch versions are automatically merged
- Minor/Major versions require manual review

### Auto-approval Mechanism

When Renovate-created PRs pass all tests, GitHub Actions will automatically approve and merge (patch version updates only).

## Publishing to PyPI and npm

This project supports publishing to both PyPI and npm.

### Automatic Release (Recommended) ✨

This project uses [release-please](https://github.com/googleapis/release-please-action) to automatically manage versions and release process.

**How it works:**
1. When you commit code following [Conventional Commits](https://www.conventionalcommits.org/) specification, release-please will automatically:
   - Determine version number based on commit type (`feat:` → minor, `fix:` → patch, `BREAKING CHANGE` → major)
   - Create a Pull Request containing version updates and CHANGELOG
   - After you merge the PR, automatically create GitHub Release and tag
   - Trigger publish workflow, automatically publish to npm and PyPI

**Commit format examples:**
```bash
feat: add new feature          # 1.0.0 → 1.1.0
fix: fix bug                  # 1.0.0 → 1.0.1
feat!: breaking change        # 1.0.0 → 2.0.0
docs: update documentation    # 1.0.0 → 1.0.1
```

**Manual trigger:**
- Go to GitHub Actions → "Release Please" → "Run workflow"

### Manual Release (Fallback)

**PyPI:**
```bash
# 1. Install build tools
pip install build twine

# 2. Build package
python -m build

# 3. Publish to PyPI
twine upload dist/*
```

**npm:**
```bash
# 1. Login to npm
npm login

# 2. Publish
npm publish
```

**Note**: Before publishing, please ensure:
- Version numbers are updated (`pyproject.toml` and `package.json`)
- All features are tested
- README documentation is updated
- LICENSE file is added

## Contributing

Issues and Pull Requests are welcome!

Before submitting code, please ensure all linter checks pass.
