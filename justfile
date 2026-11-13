# PySide6 GUI template task runner

set dotenv-load := false

# Default: show available recipes
default:
    @just --list

# Install the app, PySide6 and the development tools into .venv
setup:
    uv sync

# Launch the GUI
run:
    uv run python -m app

# Format code and apply the linter's safe fixes (changes files)
fmt:
    uv run ruff format .
    uv run ruff check --fix .

# Verify formatting without changing anything
fmt-check:
    uv run ruff format --check .

# Run the linter
lint:
    uv run ruff check .

# Type-check the package
typecheck:
    uv run pyright

# Format check, lint and type-check: changes nothing, as CI runs it
check: fmt-check lint typecheck

# Run the tests without a display
test:
    QT_QPA_PLATFORM=offscreen uv run pytest

# Serve the documentation site locally with live reload
docs:
    uv run --locked --only-group docs mkdocs serve

# Build the documentation site into site/ and fail on any warning
docs-build:
    uv run --locked --only-group docs mkdocs build --strict

# Regenerate each ui_*.py after editing a .ui file
uic:
    for form in src/app/ui/*.ui; do uv run pyside6-uic "$form" -o "${form%/*}/ui_$(basename "$form" .ui).py" || exit 1; done
