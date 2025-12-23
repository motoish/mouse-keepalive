.PHONY: help lint lint-python lint-shell lint-markdown lint-yaml format format-python install-dev test test-cov clean

# Default target
help:
	@echo "Available targets:"
	@echo "  make install-dev    - Install all development dependencies"
	@echo "  make lint           - Run all linters"
	@echo "  make lint-python    - Run Python linters (flake8, black, pylint, mypy)"
	@echo "  make lint-shell     - Run Shell linter (shellcheck)"
	@echo "  make lint-markdown  - Run Markdown linter (markdownlint)"
	@echo "  make lint-yaml      - Run YAML linter (yamllint)"
	@echo "  make format         - Format code (black)"
	@echo "  make format-python  - Format Python code (black)"
	@echo "  make test           - Run tests"
	@echo "  make test-cov       - Run tests with coverage"
	@echo "  make clean          - Clean build artifacts"

# Install development dependencies
install-dev:
	@echo "Installing Python development dependencies..."
	pip install flake8 black pylint mypy yamllint pytest pytest-cov
	@echo "Installing Node.js development dependencies..."
	npm install -g markdownlint-cli
	@echo "Note: shellcheck needs to be installed separately:"
	@echo "  macOS: brew install shellcheck"
	@echo "  Ubuntu/Debian: sudo apt-get install shellcheck"
	@echo "  Fedora: sudo dnf install ShellCheck"

# Run all linters
lint: lint-python lint-shell lint-markdown lint-yaml

# Python linting
lint-python:
	@echo "Running Python linters..."
	@echo "  - flake8..."
	flake8 auto_mouse_mover/ || true
	@echo "  - black (check)..."
	black --check auto_mouse_mover/ || true
	@echo "  - pylint..."
	pylint auto_mouse_mover/ || true
	@echo "  - mypy..."
	mypy auto_mouse_mover/ || true

# Shell linting
lint-shell:
	@echo "Running Shell linter..."
	@if command -v shellcheck >/dev/null 2>&1; then \
		shellcheck move_mouse.sh; \
	else \
		echo "Warning: shellcheck not found. Install it first:"; \
		echo "  macOS: brew install shellcheck"; \
		echo "  Ubuntu/Debian: sudo apt-get install shellcheck"; \
		echo "  Fedora: sudo dnf install ShellCheck"; \
	fi

# Markdown linting
lint-markdown:
	@echo "Running Markdown linter..."
	@if command -v markdownlint >/dev/null 2>&1; then \
		markdownlint "*.md" || true; \
	else \
		echo "Warning: markdownlint not found. Install it first:"; \
		echo "  npm install -g markdownlint-cli"; \
	fi

# YAML linting
lint-yaml:
	@echo "Running YAML linter..."
	yamllint .github/workflows/*.yml || true

# Format code
format: format-python

# Format Python code
format-python:
	@echo "Formatting Python code with black..."
	black auto_mouse_mover/

# Run tests
test:
	@echo "Running tests..."
	pytest tests/ -v

# Run tests with coverage
test-cov:
	@echo "Running tests with coverage..."
	pytest tests/ -v --cov=auto_mouse_mover --cov-report=term-missing --cov-report=html

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	@echo "Clean complete!"

