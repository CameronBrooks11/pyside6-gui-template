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

# Drive every window without a display; fail on a warning, a slot error or a missing icon
test:
    QT_QPA_PLATFORM=offscreen uv run python -W error smoke.py

# Serve the documentation site locally with live reload
docs:
    uv run --only-group docs mkdocs serve

# Build the documentation site into site/ and fail on any warning
docs-build:
    uv run --only-group docs mkdocs build --strict

# Regenerate ui_*.py and resources_rc.py after editing a .ui file, style.qss or the icons
uic:
    uv run pyside6-rcc --format-version 1 --no-compress src/app/resources/resources.qrc -o src/app/ui/resources_rc.py
    uv run pyside6-uic --from-imports src/app/ui/ui_main.ui -o src/app/ui/ui_main.py
    uv run pyside6-uic --from-imports src/app/ui/ui_dialog.ui -o src/app/ui/ui_dialog.py
    uv run pyside6-uic --from-imports src/app/ui/ui_error.ui -o src/app/ui/ui_error.py
