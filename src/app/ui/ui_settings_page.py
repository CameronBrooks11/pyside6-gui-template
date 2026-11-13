# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_page.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QLabel,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_SettingsPage(object):
    def setupUi(self, SettingsPage):
        if not SettingsPage.objectName():
            SettingsPage.setObjectName(u"SettingsPage")
        self.page_layout = QVBoxLayout(SettingsPage)
        self.page_layout.setSpacing(12)
        self.page_layout.setObjectName(u"page_layout")
        self.page_layout.setContentsMargins(32, 24, 32, 24)
        self.heading = QLabel(SettingsPage)
        self.heading.setObjectName(u"heading")
        font = QFont()
        font.setPointSize(18)
        self.heading.setFont(font)

        self.page_layout.addWidget(self.heading)

        self.heading_gap = QSpacerItem(20, 4, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.page_layout.addItem(self.heading_gap)

        self.fields = QFormLayout()
        self.fields.setObjectName(u"fields")
        self.fields.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.FieldsStayAtSizeHint)
        self.fields.setHorizontalSpacing(12)
        self.theme_label = QLabel(SettingsPage)
        self.theme_label.setObjectName(u"theme_label")

        self.fields.setWidget(0, QFormLayout.ItemRole.LabelRole, self.theme_label)

        self.theme_combo = QComboBox(SettingsPage)
        self.theme_combo.setObjectName(u"theme_combo")
        self.theme_combo.setMinimumSize(QSize(180, 28))

        self.fields.setWidget(0, QFormLayout.ItemRole.FieldRole, self.theme_combo)


        self.page_layout.addLayout(self.fields)

        self.filler = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.page_layout.addItem(self.filler)

#if QT_CONFIG(shortcut)
        self.theme_label.setBuddy(self.theme_combo)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(SettingsPage)

        QMetaObject.connectSlotsByName(SettingsPage)
    # setupUi

    def retranslateUi(self, SettingsPage):
        self.heading.setText(QCoreApplication.translate("SettingsPage", u"Settings", None))
        self.theme_label.setText(QCoreApplication.translate("SettingsPage", u"&Theme", None))
        pass
    # retranslateUi

