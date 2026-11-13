# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QListWidget,
    QListWidgetItem, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QStackedWidget, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(900, 600)
        self.action_quit = QAction(MainWindow)
        self.action_quit.setObjectName(u"action_quit")
        self.action_about = QAction(MainWindow)
        self.action_about.setObjectName(u"action_about")
        self.central = QWidget(MainWindow)
        self.central.setObjectName(u"central")
        self.central_layout = QHBoxLayout(self.central)
        self.central_layout.setSpacing(0)
        self.central_layout.setObjectName(u"central_layout")
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.navigation = QListWidget(self.central)
        self.navigation.setObjectName(u"navigation")
        self.navigation.setMinimumSize(QSize(170, 0))
        self.navigation.setMaximumSize(QSize(170, 16777215))
        self.navigation.setFrameShape(QFrame.Shape.NoFrame)
        self.navigation.setIconSize(QSize(20, 20))
        self.navigation.setSpacing(2)

        self.central_layout.addWidget(self.navigation)

        self.pages = QStackedWidget(self.central)
        self.pages.setObjectName(u"pages")

        self.central_layout.addWidget(self.pages)

        MainWindow.setCentralWidget(self.central)
        self.menu_bar = QMenuBar(MainWindow)
        self.menu_bar.setObjectName(u"menu_bar")
        self.menu_file = QMenu(self.menu_bar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu_help = QMenu(self.menu_bar)
        self.menu_help.setObjectName(u"menu_help")
        MainWindow.setMenuBar(self.menu_bar)
        self.status_bar = QStatusBar(MainWindow)
        self.status_bar.setObjectName(u"status_bar")
        MainWindow.setStatusBar(self.status_bar)

        self.menu_bar.addAction(self.menu_file.menuAction())
        self.menu_bar.addAction(self.menu_help.menuAction())
        self.menu_file.addAction(self.action_quit)
        self.menu_help.addAction(self.action_about)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        self.action_quit.setText(QCoreApplication.translate("MainWindow", u"&Quit", None))
#if QT_CONFIG(shortcut)
        self.action_quit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.action_about.setText(QCoreApplication.translate("MainWindow", u"&About", None))
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
        self.menu_help.setTitle(QCoreApplication.translate("MainWindow", u"&Help", None))
        pass
    # retranslateUi

