# PySide6 GUI template task runner

set dotenv-load := false

# Default: show available recipes
default:
    @just --list

# Install dependencies into .venv
setup:
    uv sync

# Launch the GUI
run:
    uv run python main.py

# Build every window without a display and fail on any Qt warning
check:
    QT_QPA_PLATFORM=offscreen uv run python -W error smoke.py

# Regenerate the ui_*.py files after editing a .ui file in Qt Designer
uic:
    uv run pyside6-uic ui_main.ui -o ui_main.py
    uv run pyside6-uic ui_dialog.ui -o ui_dialog.py
    uv run pyside6-uic ui_error.ui -o ui_error.py
