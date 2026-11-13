# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'task_page.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QHBoxLayout, QLabel,
    QProgressBar, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_TaskPage(object):
    def setupUi(self, TaskPage):
        if not TaskPage.objectName():
            TaskPage.setObjectName(u"TaskPage")
        self.page_layout = QVBoxLayout(TaskPage)
        self.page_layout.setSpacing(12)
        self.page_layout.setObjectName(u"page_layout")
        self.page_layout.setContentsMargins(32, 24, 32, 24)
        self.heading = QLabel(TaskPage)
        self.heading.setObjectName(u"heading")
        font = QFont()
        font.setPointSize(18)
        self.heading.setFont(font)

        self.page_layout.addWidget(self.heading)

        self.heading_gap = QSpacerItem(20, 4, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.page_layout.addItem(self.heading_gap)

        self.content = QWidget(TaskPage)
        self.content.setObjectName(u"content")
        self.content.setMaximumSize(QSize(620, 16777215))
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setSpacing(12)
        self.content_layout.setObjectName(u"content_layout")
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.description = QLabel(self.content)
        self.description.setObjectName(u"description")
        self.description.setWordWrap(True)

        self.content_layout.addWidget(self.description)

        self.fields = QFormLayout()
        self.fields.setObjectName(u"fields")
        self.fields.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.FieldsStayAtSizeHint)
        self.fields.setHorizontalSpacing(12)
        self.steps_label = QLabel(self.content)
        self.steps_label.setObjectName(u"steps_label")

        self.fields.setWidget(0, QFormLayout.ItemRole.LabelRole, self.steps_label)

        self.steps_spin = QSpinBox(self.content)
        self.steps_spin.setObjectName(u"steps_spin")
        self.steps_spin.setMinimumSize(QSize(100, 28))
        self.steps_spin.setMinimum(1)
        self.steps_spin.setMaximum(1000)
        self.steps_spin.setValue(100)

        self.fields.setWidget(0, QFormLayout.ItemRole.FieldRole, self.steps_spin)


        self.content_layout.addLayout(self.fields)

        self.progress_bar = QProgressBar(self.content)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setMaximumSize(QSize(16777215, 8))
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)

        self.content_layout.addWidget(self.progress_bar)

        self.status_label = QLabel(self.content)
        self.status_label.setObjectName(u"status_label")

        self.content_layout.addWidget(self.status_label)

        self.buttons = QHBoxLayout()
        self.buttons.setObjectName(u"buttons")
        self.filler = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttons.addItem(self.filler)

        self.cancel_button = QPushButton(self.content)
        self.cancel_button.setObjectName(u"cancel_button")
        self.cancel_button.setMinimumSize(QSize(0, 28))
        self.cancel_button.setEnabled(False)

        self.buttons.addWidget(self.cancel_button)

        self.start_button = QPushButton(self.content)
        self.start_button.setObjectName(u"start_button")
        self.start_button.setMinimumSize(QSize(0, 28))

        self.buttons.addWidget(self.start_button)


        self.content_layout.addLayout(self.buttons)


        self.page_layout.addWidget(self.content)

        self.bottom_filler = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.page_layout.addItem(self.bottom_filler)

#if QT_CONFIG(shortcut)
        self.steps_label.setBuddy(self.steps_spin)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(TaskPage)

        QMetaObject.connectSlotsByName(TaskPage)
    # setupUi

    def retranslateUi(self, TaskPage):
        self.heading.setText(QCoreApplication.translate("TaskPage", u"Background task", None))
        self.description.setText(QCoreApplication.translate("TaskPage", u"The work runs on a second thread, so the window stays responsive while it does.", None))
        self.steps_label.setText(QCoreApplication.translate("TaskPage", u"S&teps", None))
        self.status_label.setText(QCoreApplication.translate("TaskPage", u"Not started", None))
        self.cancel_button.setText(QCoreApplication.translate("TaskPage", u"&Cancel", None))
        self.start_button.setText(QCoreApplication.translate("TaskPage", u"&Start", None))
        pass
    # retranslateUi

