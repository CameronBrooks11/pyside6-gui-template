"""The committed ui_*.py modules are what pyside6-uic makes of the .ui files."""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import PySide6
import pytest

import app.ui

UI_DIR = Path(app.ui.__file__).parent
FORMS = sorted(UI_DIR.glob("*.ui"))


def without_version(text: str) -> str:
    """Drop the line naming the Qt version, which differs between installs."""
    return "\n".join(line for line in text.splitlines() if "Compiler version" not in line)


def test_there_are_forms_to_check():
    assert FORMS


@pytest.mark.parametrize("form", FORMS, ids=lambda form: form.name)
def test_generated_module_is_current(form: Path):
    committed = (UI_DIR / f"ui_{form.stem}.py").read_text(encoding="utf-8")
    generated_with = re.search(r"Compiler version (\S+)", committed)
    assert generated_with, "no version line in the committed module"
    if generated_with[1] != PySide6.__version__:
        # Other versions of uic spell some lines differently, so there is
        # nothing to compare. CI installs from the lock file: a mismatch there
        # means PySide6 was upgraded without regenerating the modules.
        mismatch = f"generated with PySide6 {generated_with[1]}, not {PySide6.__version__}"
        assert not os.environ.get("CI"), f"{mismatch}: run `just uic`"
        pytest.skip(mismatch)
    uic = shutil.which("pyside6-uic", path=str(Path(sys.executable).parent))
    assert uic, "pyside6-uic is not installed beside the interpreter"
    fresh = subprocess.run([uic, str(form)], capture_output=True, text=True, check=True).stdout
    assert without_version(committed) == without_version(fresh), "run `just uic`"
