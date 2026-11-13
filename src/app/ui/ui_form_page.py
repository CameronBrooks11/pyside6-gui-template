# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_page.ui'
##
## Created by: Qt User Interface Compiler version 6.11.3
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QHBoxLayout,
    QLabel, QLineEdit, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_FormPage(object):
    def setupUi(self, FormPage):
        if not FormPage.objectName():
            FormPage.setObjectName(u"FormPage")
        self.page_layout = QVBoxLayout(FormPage)
        self.page_layout.setSpacing(12)
        self.page_layout.setObjectName(u"page_layout")
        self.page_layout.setContentsMargins(32, 24, 32, 24)
        self.heading = QLabel(FormPage)
        self.heading.setObjectName(u"heading")
        font = QFont()
        font.setPointSize(18)
        self.heading.setFont(font)

        self.page_layout.addWidget(self.heading)

        self.heading_gap = QSpacerItem(20, 4, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.page_layout.addItem(self.heading_gap)

        self.content = QWidget(FormPage)
        self.content.setObjectName(u"content")
        self.content.setMaximumSize(QSize(620, 16777215))
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setSpacing(12)
        self.content_layout.setObjectName(u"content_layout")
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.fields = QFormLayout()
        self.fields.setObjectName(u"fields")
        self.fields.setHorizontalSpacing(12)
        self.fields.setVerticalSpacing(10)
        self.name_label = QLabel(self.content)
        self.name_label.setObjectName(u"name_label")

        self.fields.setWidget(0, QFormLayout.ItemRole.LabelRole, self.name_label)

        self.name_edit = QLineEdit(self.content)
        self.name_edit.setObjectName(u"name_edit")
        self.name_edit.setMinimumSize(QSize(0, 28))

        self.fields.setWidget(0, QFormLayout.ItemRole.FieldRole, self.name_edit)

        self.email_label = QLabel(self.content)
        self.email_label.setObjectName(u"email_label")

        self.fields.setWidget(1, QFormLayout.ItemRole.LabelRole, self.email_label)

        self.email_edit = QLineEdit(self.content)
        self.email_edit.setObjectName(u"email_edit")
        self.email_edit.setMinimumSize(QSize(0, 28))

        self.fields.setWidget(1, QFormLayout.ItemRole.FieldRole, self.email_edit)

        self.role_label = QLabel(self.content)
        self.role_label.setObjectName(u"role_label")

        self.fields.setWidget(2, QFormLayout.ItemRole.LabelRole, self.role_label)

        self.role_combo = QComboBox(self.content)
        self.role_combo.addItem("")
        self.role_combo.addItem("")
        self.role_combo.addItem("")
        self.role_combo.addItem("")
        self.role_combo.setObjectName(u"role_combo")
        self.role_combo.setMinimumSize(QSize(180, 28))
        self.role_combo.setMaximumSize(QSize(180, 16777215))

        self.fields.setWidget(2, QFormLayout.ItemRole.FieldRole, self.role_combo)

        self.notes_label = QLabel(self.content)
        self.notes_label.setObjectName(u"notes_label")

        self.fields.setWidget(3, QFormLayout.ItemRole.LabelRole, self.notes_label)

        self.notes_edit = QPlainTextEdit(self.content)
        self.notes_edit.setObjectName(u"notes_edit")
        self.notes_edit.setMaximumSize(QSize(16777215, 130))
        self.notes_edit.setTabChangesFocus(True)

        self.fields.setWidget(3, QFormLayout.ItemRole.FieldRole, self.notes_edit)

        self.error_label = QLabel(self.content)
        self.error_label.setObjectName(u"error_label")

        self.fields.setWidget(4, QFormLayout.ItemRole.FieldRole, self.error_label)


        self.content_layout.addLayout(self.fields)

        self.buttons = QHBoxLayout()
        self.buttons.setObjectName(u"buttons")
        self.filler = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttons.addItem(self.filler)

        self.clear_button = QPushButton(self.content)
        self.clear_button.setObjectName(u"clear_button")
        self.clear_button.setMinimumSize(QSize(0, 28))

        self.buttons.addWidget(self.clear_button)

        self.save_button = QPushButton(self.content)
        self.save_button.setObjectName(u"save_button")
        self.save_button.setMinimumSize(QSize(0, 28))

        self.buttons.addWidget(self.save_button)


        self.content_layout.addLayout(self.buttons)


        self.page_layout.addWidget(self.content)

        self.bottom_filler = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.page_layout.addItem(self.bottom_filler)

#if QT_CONFIG(shortcut)
        self.name_label.setBuddy(self.name_edit)
        self.email_label.setBuddy(self.email_edit)
        self.role_label.setBuddy(self.role_combo)
        self.notes_label.setBuddy(self.notes_edit)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.name_edit, self.email_edit)
        QWidget.setTabOrder(self.email_edit, self.role_combo)
        QWidget.setTabOrder(self.role_combo, self.notes_edit)
        QWidget.setTabOrder(self.notes_edit, self.clear_button)
        QWidget.setTabOrder(self.clear_button, self.save_button)

        self.retranslateUi(FormPage)

        QMetaObject.connectSlotsByName(FormPage)
    # setupUi

    def retranslateUi(self, FormPage):
        self.heading.setText(QCoreApplication.translate("FormPage", u"New contact", None))
        self.name_label.setText(QCoreApplication.translate("FormPage", u"&Name", None))
        self.email_label.setText(QCoreApplication.translate("FormPage", u"&Email", None))
        self.email_edit.setPlaceholderText(QCoreApplication.translate("FormPage", u"name@example.com", None))
        self.role_label.setText(QCoreApplication.translate("FormPage", u"&Role", None))
        self.role_combo.setItemText(0, QCoreApplication.translate("FormPage", u"Engineer", None))
        self.role_combo.setItemText(1, QCoreApplication.translate("FormPage", u"Designer", None))
        self.role_combo.setItemText(2, QCoreApplication.translate("FormPage", u"Manager", None))
        self.role_combo.setItemText(3, QCoreApplication.translate("FormPage", u"Other", None))

        self.notes_label.setText(QCoreApplication.translate("FormPage", u"N&otes", None))
        self.error_label.setText("")
        self.clear_button.setText(QCoreApplication.translate("FormPage", u"&Clear", None))
        self.save_button.setText(QCoreApplication.translate("FormPage", u"&Save", None))
        pass
    # retranslateUi

