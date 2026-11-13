"""A table: a model shown in a view, with sorting, filtering and deleting."""

from PySide6.QtCore import QSortFilterProxyModel, Qt
from PySide6.QtWidgets import QMessageBox, QWidget

from app.contacts import ContactsModel
from app.ui.ui_table_page import Ui_TablePage


class TablePage(QWidget):
    def __init__(self, contacts: ContactsModel, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_TablePage()
        self.ui.setupUi(self)

        self._contacts = contacts
        # The proxy sorts and filters what the view shows; the model is untouched.
        self._proxy = QSortFilterProxyModel(self)
        self._proxy.setSourceModel(contacts)
        self._proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self._proxy.setSortCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self._proxy.setFilterKeyColumn(-1)  # match against every column
        self.ui.table_view.setModel(self._proxy)
        self.ui.table_view.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        self.ui.table_view.resizeColumnsToContents()

        self.ui.filter_edit.textChanged.connect(self._proxy.setFilterFixedString)
        self.ui.delete_button.clicked.connect(self.delete_selected)
        self.ui.table_view.selectionModel().selectionChanged.connect(self._update_delete_button)
        for signal in (
            contacts.rowsInserted,
            contacts.rowsRemoved,
            self._proxy.rowsInserted,
            self._proxy.rowsRemoved,
            self._proxy.modelReset,
            self._proxy.layoutChanged,
        ):
            signal.connect(self._update_count)
        self._update_count()
        self._update_delete_button()

    def delete_selected(self) -> None:
        selected = self.ui.table_view.selectionModel().selectedRows()
        if not selected:
            return
        count = len(selected)
        what = "the selected contact" if count == 1 else f"the {count} selected contacts"
        answer = QMessageBox.question(self, "Delete contacts", f"Delete {what}?")
        if answer == QMessageBox.StandardButton.Yes:
            self._contacts.remove([self._proxy.mapToSource(index).row() for index in selected])

    def _update_count(self) -> None:
        shown, total = self._proxy.rowCount(), self._contacts.rowCount()
        if shown == total:
            self.ui.count_label.setText(f"{total} contacts")
        else:
            self.ui.count_label.setText(f"{shown} of {total} contacts")

    def _update_delete_button(self) -> None:
        self.ui.delete_button.setEnabled(self.ui.table_view.selectionModel().hasSelection())
