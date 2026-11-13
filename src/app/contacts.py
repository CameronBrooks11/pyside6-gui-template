"""The example data: a list of contacts as a Qt table model."""

from dataclasses import astuple, dataclass

from PySide6.QtCore import QAbstractTableModel, QModelIndex, QPersistentModelIndex, Qt

_ROOT = QModelIndex()


@dataclass
class Contact:
    name: str
    email: str
    role: str
    notes: str = ""


EXAMPLES = (
    Contact("Ada Lovelace", "ada@example.com", "Engineer", "Wrote the first program"),
    Contact("Grace Hopper", "grace@example.com", "Engineer"),
    Contact("Dieter Rams", "dieter@example.com", "Designer", "Less, but better"),
    Contact("Peter Drucker", "peter@example.com", "Manager"),
)


class ContactsModel(QAbstractTableModel):
    HEADERS = ("Name", "Email", "Role", "Notes")

    def __init__(self, contacts: tuple[Contact, ...] = (), parent=None) -> None:
        super().__init__(parent)
        self._contacts = list(contacts)

    def rowCount(self, parent: QModelIndex | QPersistentModelIndex = _ROOT) -> int:
        return 0 if parent.isValid() else len(self._contacts)

    def columnCount(self, parent: QModelIndex | QPersistentModelIndex = _ROOT) -> int:
        return 0 if parent.isValid() else len(self.HEADERS)

    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ):
        if index.isValid() and role == Qt.ItemDataRole.DisplayRole:
            return astuple(self._contacts[index.row()])[index.column()]
        return None

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.HEADERS[section]
        return None

    def add(self, contact: Contact) -> None:
        row = len(self._contacts)
        self.beginInsertRows(_ROOT, row, row)
        self._contacts.append(contact)
        self.endInsertRows()

    def remove(self, rows: list[int]) -> None:
        # From the bottom up, so removing one row does not renumber the rest.
        for row in sorted(set(rows), reverse=True):
            self.beginRemoveRows(_ROOT, row, row)
            del self._contacts[row]
            self.endRemoveRows()
