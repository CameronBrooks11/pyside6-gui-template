# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'home_page.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_HomePage(object):
    def setupUi(self, HomePage):
        if not HomePage.objectName():
            HomePage.setObjectName(u"HomePage")
        self.page_layout = QVBoxLayout(HomePage)
        self.page_layout.setSpacing(12)
        self.page_layout.setObjectName(u"page_layout")
        self.page_layout.setContentsMargins(32, 24, 32, 24)
        self.heading = QLabel(HomePage)
        self.heading.setObjectName(u"heading")
        font = QFont()
        font.setPointSize(18)
        self.heading.setFont(font)

        self.page_layout.addWidget(self.heading)

        self.body = QLabel(HomePage)
        self.body.setObjectName(u"body")
        self.body.setTextFormat(Qt.TextFormat.RichText)
        self.body.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.body.setWordWrap(True)

        self.page_layout.addWidget(self.body)

        self.filler = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.page_layout.addItem(self.filler)


        self.retranslateUi(HomePage)

        QMetaObject.connectSlotsByName(HomePage)
    # setupUi

    def retranslateUi(self, HomePage):
        self.heading.setText(QCoreApplication.translate("HomePage", u"Home", None))
        self.body.setText(QCoreApplication.translate("HomePage", u"<p>This is a starting point for a desktop application: a window with a sidebar, a few pages, and the patterns most applications need.</p><ul><li><b>Form</b>: input, validation and a confirmation before discarding.</li><li><b>Table</b>: a model shown in a view, with sorting, filtering and deleting.</li><li><b>Task</b>: long work on a second thread, with progress and cancel.</li><li><b>Settings</b>: a light and a dark theme, remembered between runs.</li></ul><p>Replace these pages with your own.</p>", None))
        pass
    # retranslateUi

