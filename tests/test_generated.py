"""The committed ui_*.py modules are what pyside6-uic makes of the .ui files."""

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

import app.ui

UI_DIR = Path(app.ui.__file__).parent
FORMS = sorted(UI_DIR.glob("*.ui"))


def without_version(text: str) -> str:
    """Drop the line naming the Qt version, which differs between installs."""
    return "\n".join(line for line in text.splitlines() if "Compiler version" not in line)


def test_there_are_forms_to_check():
    assert len(FORMS) >= 6


@pytest.mark.parametrize("form", FORMS, ids=lambda form: form.name)
def test_generated_module_is_current(form: Path):
    uic = shutil.which("pyside6-uic", path=str(Path(sys.executable).parent))
    assert uic, "pyside6-uic is not installed beside the interpreter"
    fresh = subprocess.run([uic, str(form)], capture_output=True, text=True, check=True).stdout
    committed = (UI_DIR / f"ui_{form.stem}.py").read_text(encoding="utf-8")
    assert without_version(committed) == without_version(fresh), "run `just uic`"
