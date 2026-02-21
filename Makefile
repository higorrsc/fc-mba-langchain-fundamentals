.PHONY: help check-python venv install-pip export-req install-uv install-uv-prd lint lint-fix type-check test test-cov

# === Variables ===

# Virtual environment directory (default: .venv)
VENV_DIR ?= .venv

# UV wrapper commands
UV = @uv
RUN_PY = $(UV) run python
RUN_TOOL = $(UV) run

# Detect Operating System for manual paths (fallback)
ifdef ComSpec
	PYTHON_EXEC = $(VENV_DIR)/Scripts/python.exe
else
	PYTHON_EXEC = $(VENV_DIR)/bin/python
endif

# === Environment Setup ===

# Verify if python executable exists in venv
check-python:
	@if [ ! -f "$(PYTHON_EXEC)" ]; then \
		echo "❌ Virtual environment not found at $(PYTHON_EXEC)"; \
		echo "👉 Run 'make venv' to create the virtual environment."; \
		exit 1; \
	fi

# Create virtual environment
venv:
	$(UV) venv $(VENV_DIR)

# Export dependencies to requirements.txt
export-req:
	$(UV) export --no-dev --no-hashes --no-annotate --output-file requirements.txt --format requirements.txt

# Install dependencies from requirements.txt using uv (faster)
install-pip: check-python
	$(UV) pip install -r requirements.txt

# Install dependencies from pyproject.toml using uv (faster)
install-uv:
	$(UV) sync

# Install dependencies from pyproject.toml using uv (faster)
install-uv-prd:
	$(UV) sync --no-dev

# === Linting / Typing / Tests ===

# Lint and Format Check (Ruff)
lint:
	$(RUN_TOOL) ruff check .
	$(RUN_TOOL) ruff format --check .

# Fix Linting and Format (Ruff)
lint-fix:
	$(RUN_TOOL) ruff check . --fix
	$(RUN_TOOL) ruff format .

# Type Checking (Mypy)
type-check:
	$(RUN_TOOL) mypy .

# Tests (PyTest)
test:
	$(RUN_TOOL) pytest -q

test-cov:
	$(RUN_TOOL) pytest --cov=src --cov-report=term-missing --cov-report=html

# === Help ===

help:
	@echo "Available commands:"
	@echo ""
