# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'table_page.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTableView, QVBoxLayout, QWidget)

class Ui_TablePage(object):
    def setupUi(self, TablePage):
        if not TablePage.objectName():
            TablePage.setObjectName(u"TablePage")
        self.page_layout = QVBoxLayout(TablePage)
        self.page_layout.setObjectName(u"page_layout")
        self.page_layout.setContentsMargins(24, 24, 24, 24)
        self.heading = QLabel(TablePage)
        self.heading.setObjectName(u"heading")
        font = QFont()
        font.setPointSize(18)
        self.heading.setFont(font)

        self.page_layout.addWidget(self.heading)

        self.filter_edit = QLineEdit(TablePage)
        self.filter_edit.setObjectName(u"filter_edit")
        self.filter_edit.setClearButtonEnabled(True)

        self.page_layout.addWidget(self.filter_edit)

        self.table_view = QTableView(TablePage)
        self.table_view.setObjectName(u"table_view")
        self.table_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSortingEnabled(True)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.verticalHeader().setVisible(False)

        self.page_layout.addWidget(self.table_view)

        self.buttons = QHBoxLayout()
        self.buttons.setObjectName(u"buttons")
        self.count_label = QLabel(TablePage)
        self.count_label.setObjectName(u"count_label")

        self.buttons.addWidget(self.count_label)

        self.filler = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttons.addItem(self.filler)

        self.delete_button = QPushButton(TablePage)
        self.delete_button.setObjectName(u"delete_button")

        self.buttons.addWidget(self.delete_button)


        self.page_layout.addLayout(self.buttons)


        self.retranslateUi(TablePage)

        QMetaObject.connectSlotsByName(TablePage)
    # setupUi

    def retranslateUi(self, TablePage):
        self.heading.setText(QCoreApplication.translate("TablePage", u"Contacts", None))
        self.filter_edit.setPlaceholderText(QCoreApplication.translate("TablePage", u"Filter", None))
        self.count_label.setText("")
        self.delete_button.setText(QCoreApplication.translate("TablePage", u"&Delete selected", None))
        pass
    # retranslateUi

