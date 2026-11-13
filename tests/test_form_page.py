import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox

from app.contacts import Contact
from app.pages.form import FormPage


@pytest.fixture
def page(qtbot):
    page = FormPage()
    qtbot.addWidget(page)
    return page


def fill(page, name="Linus", email="linus@example.com"):
    page.ui.name_edit.setText(name)
    page.ui.email_edit.setText(email)


def test_save_emits_the_contact_and_empties_the_form(page, qtbot):
    fill(page)
    page.ui.role_combo.setCurrentText("Manager")
    page.ui.notes_edit.setPlainText("  kernel  ")
    with qtbot.waitSignal(page.submitted) as signal:
        page.ui.save_button.click()
    assert signal.args == [Contact("Linus", "linus@example.com", "Manager", "kernel")]
    assert page.ui.name_edit.text() == ""
    assert page.ui.email_edit.text() == ""
    assert page.ui.notes_edit.toPlainText() == ""
    assert page.ui.role_combo.currentIndex() == 0


def test_a_missing_name_is_refused(page, qtbot):
    fill(page, name="   ")
    with qtbot.assertNotEmitted(page.submitted):
        page.ui.save_button.click()
    assert "name" in page.ui.error_label.text()
    assert page.ui.email_edit.text() == "linus@example.com"


@pytest.mark.parametrize("email", ["", "linus", "linus@", "@example.com", "a b@example.com"])
def test_a_bad_email_is_refused(page, qtbot, email):
    fill(page, email=email)
    with qtbot.assertNotEmitted(page.submitted):
        page.ui.save_button.click()
    assert "email" in page.ui.error_label.text()


def test_the_error_goes_away_after_a_good_save(page):
    fill(page, email="nope")
    page.ui.save_button.click()
    fill(page)
    page.ui.save_button.click()
    assert page.ui.error_label.text() == ""


def test_clear_asks_first_and_keeps_the_text_on_no(page, answer):
    asked = answer(QMessageBox.StandardButton.No)
    fill(page)
    page.ui.clear_button.click()
    assert len(asked) == 1
    assert page.ui.name_edit.text() == "Linus"


def test_clear_empties_the_form_on_yes(page, answer):
    answer(QMessageBox.StandardButton.Yes)
    fill(page)
    page.ui.clear_button.click()
    assert page.ui.name_edit.text() == ""
    assert page.ui.email_edit.text() == ""


def test_clear_does_not_ask_about_an_empty_form(page, answer):
    asked = answer(QMessageBox.StandardButton.No)
    page.ui.clear_button.click()
    assert asked == []


def test_a_saved_contact_reaches_the_table_and_the_status_bar(window):
    before = window.contacts.rowCount()
    fill(window.form_page)
    window.form_page.ui.save_button.click()
    assert window.contacts.rowCount() == before + 1
    assert "Linus" in window.ui.status_bar.currentMessage()


def test_return_in_a_field_saves(page, qtbot):
    fill(page)
    with qtbot.waitSignal(page.submitted):
        qtbot.keyClick(page.ui.email_edit, Qt.Key.Key_Return)
    fill(page)
    with qtbot.waitSignal(page.submitted):
        qtbot.keyClick(page.ui.name_edit, Qt.Key.Key_Return)
