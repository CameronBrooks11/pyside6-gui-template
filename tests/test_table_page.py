import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox

from app.contacts import Contact, ContactsModel
from app.pages.table import TablePage

CONTACTS = (
    Contact("Cy", "cy@example.com", "Engineer"),
    Contact("bea", "bea@example.com", "Designer", "likes tables"),
    Contact("Abe", "abe@example.com", "Engineer"),
)


@pytest.fixture
def model():
    return ContactsModel(CONTACTS)


@pytest.fixture
def page(qtbot, model):
    page = TablePage(model)
    qtbot.addWidget(page)
    return page


def names(page):
    shown = page.ui.table_view.model()
    return [shown.index(row, 0).data() for row in range(shown.rowCount())]


def test_rows_are_sorted_by_name_ignoring_case(page):
    assert names(page) == ["Abe", "bea", "Cy"]
    assert page.ui.count_label.text() == "3 contacts"


def test_clicking_a_header_sorts_by_that_column(page):
    page.ui.table_view.sortByColumn(1, Qt.SortOrder.DescendingOrder)
    assert names(page) == ["Cy", "bea", "Abe"]


def test_the_header_names_the_columns(page):
    shown = page.ui.table_view.model()
    headers = [shown.headerData(c, Qt.Orientation.Horizontal) for c in range(shown.columnCount())]
    assert headers == ["Name", "Email", "Role", "Notes"]


def test_the_filter_matches_any_column_ignoring_case(page):
    page.ui.filter_edit.setText("ENGINEER")
    assert names(page) == ["Abe", "Cy"]
    assert page.ui.count_label.text() == "2 of 3 contacts"
    page.ui.filter_edit.setText("tables")
    assert names(page) == ["bea"]
    page.ui.filter_edit.clear()
    assert page.ui.count_label.text() == "3 contacts"


def test_delete_is_only_enabled_with_a_selection(page):
    assert not page.ui.delete_button.isEnabled()
    page.ui.table_view.selectRow(0)
    assert page.ui.delete_button.isEnabled()
    page.ui.table_view.clearSelection()
    assert not page.ui.delete_button.isEnabled()


def test_delete_removes_the_selected_row_not_the_row_at_that_position(page, model, answer):
    asked = answer(QMessageBox.StandardButton.Yes)
    page.ui.table_view.selectRow(0)  # Abe, who is last in the model
    page.ui.delete_button.click()
    assert asked == ["Delete the selected contact?"]
    assert names(page) == ["bea", "Cy"]
    assert model.rowCount() == 2
    assert page.ui.count_label.text() == "2 contacts"


def test_delete_removes_several_rows(page, model, answer):
    asked = answer(QMessageBox.StandardButton.Yes)
    page.ui.table_view.selectAll()
    page.ui.delete_button.click()
    assert asked == ["Delete the 3 selected contacts?"]
    assert model.rowCount() == 0
    assert not page.ui.delete_button.isEnabled()


def test_delete_keeps_the_rows_on_no(page, model, answer):
    answer(QMessageBox.StandardButton.No)
    page.ui.table_view.selectRow(0)
    page.ui.delete_button.click()
    assert model.rowCount() == 3


def test_an_added_contact_appears(page, model):
    model.add(Contact("Aaron", "aaron@example.com", "Other"))
    assert names(page) == ["Aaron", "Abe", "bea", "Cy"]
    assert page.ui.count_label.text() == "4 contacts"


def test_the_count_includes_an_added_contact_the_filter_hides(page, model):
    page.ui.filter_edit.setText("designer")
    model.add(Contact("Aaron", "aaron@example.com", "Other"))
    assert names(page) == ["bea"]
    assert page.ui.count_label.text() == "1 of 4 contacts"


def test_the_count_is_singular_for_one_contact(page, model):
    model.remove([0, 1])
    assert page.ui.count_label.text() == "1 contact"


def test_delete_without_a_selection_asks_nothing(page, model, answer):
    asked = answer(QMessageBox.StandardButton.Yes)
    page.delete_selected()
    assert asked == []
    assert model.rowCount() == 3
