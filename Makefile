.PHONY: help install-dev run lint lint-python lint-shell lint-markdown lint-yaml format test test-cov clean

help:
	@echo "Available targets:"
	@echo "  make install-dev    - Install editable package + dev tools (pip install -e '.[dev]')"
	@echo "  make run            - Run via move_mouse.sh (ARGS='-i 30' make run)"
	@echo "  make lint           - Run all linters"
	@echo "  make lint-python    - Run Python linters"
	@echo "  make lint-markdown  - Run Markdown linter"
	@echo "  make lint-yaml      - Run YAML linter"
	@echo "  make format         - Format Python code (black)"
	@echo "  make test           - Run tests"
	@echo "  make test-cov       - Run tests with coverage"
	@echo "  make clean          - Clean build artifacts"

install-dev:
	pip install -e ".[dev]"
	@echo "Optional: npm install -g markdownlint-cli for markdown lint"

run:
	./move_mouse.sh $(ARGS)

lint: lint-python lint-shell lint-markdown lint-yaml

lint-shell:
	@if command -v shellcheck >/dev/null 2>&1; then \
		shellcheck move_mouse.sh; \
	else \
		echo "Warning: shellcheck not found"; \
	fi

lint-python:
	flake8 src/mouse_keepalive/ || true
	black --check src/mouse_keepalive/ || true
	pylint src/mouse_keepalive/ || true
	mypy src/mouse_keepalive/ || true

lint-markdown:
	@if command -v markdownlint >/dev/null 2>&1; then \
		markdownlint "*.md" docs/*.md || true; \
	else \
		echo "Warning: markdownlint not found (npm install -g markdownlint-cli)"; \
	fi

lint-yaml:
	yamllint .github/workflows/*.yml || true

format:
	black src/mouse_keepalive/

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=mouse_keepalive --cov-report=term-missing --cov-report=html

clean:
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ htmlcov/
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
