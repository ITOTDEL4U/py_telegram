# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window_dkp.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QListWidget,
    QListWidgetItem, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QTextEdit,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1035, 321)
        self.button_exit = QAction(MainWindow)
        self.button_exit.setObjectName(u"button_exit")
        self.button_settings = QAction(MainWindow)
        self.button_settings.setObjectName(u"button_settings")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 10, 581, 251))
        self.groupBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_tg_input_message = QTextEdit(self.groupBox)
        self.text_tg_input_message.setObjectName(u"text_tg_input_message")
        self.text_tg_input_message.setGeometry(QRect(20, 60, 371, 111))
        self.text_tg_input_message.setReadOnly(True)
        self.button_tg_send = QPushButton(self.groupBox)
        self.button_tg_send.setObjectName(u"button_tg_send")
        self.button_tg_send.setGeometry(QRect(310, 180, 81, 31))
        self.text_tg_output_message = QTextEdit(self.groupBox)
        self.text_tg_output_message.setObjectName(u"text_tg_output_message")
        self.text_tg_output_message.setGeometry(QRect(20, 180, 281, 31))
        self.comboBox = QComboBox(self.groupBox)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(20, 30, 371, 22))
        self.pushButton_save_chat = QPushButton(self.groupBox)
        self.pushButton_save_chat.setObjectName(u"pushButton_save_chat")
        self.pushButton_save_chat.setGeometry(QRect(400, 30, 75, 24))
        self.textEdit_parsing = QTextEdit(self.groupBox)
        self.textEdit_parsing.setObjectName(u"textEdit_parsing")
        self.textEdit_parsing.setGeometry(QRect(400, 60, 171, 111))
        self.pushButton_test_extract = QPushButton(self.groupBox)
        self.pushButton_test_extract.setObjectName(u"pushButton_test_extract")
        self.pushButton_test_extract.setGeometry(QRect(430, 190, 75, 24))
        self.button_send_files = QPushButton(self.centralwidget)
        self.button_send_files.setObjectName(u"button_send_files")
        self.button_send_files.setGeometry(QRect(860, 90, 161, 61))
        self.listiWdget_recipient = QListWidget(self.centralwidget)
        self.listiWdget_recipient.setObjectName(u"listiWdget_recipient")
        self.listiWdget_recipient.setGeometry(QRect(590, 20, 256, 241))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1035, 22))
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu_settings = QMenu(self.menubar)
        self.menu_settings.setObjectName(u"menu_settings")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_settings.menuAction())
        self.menu_file.addAction(self.button_exit)
        self.menu_settings.addAction(self.button_settings)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.button_exit.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0445\u043e\u0434", None))
        self.button_settings.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u043b\u0430\u0448\u0442\u0443\u0432\u0430\u043d\u043d\u044f", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Telegram \u0447\u0442\u0435\u043d\u0438\u0435/ \u043e\u043f\u0442\u0430\u0432\u043a\u0430 \u043d\u043e\u043c\u0435\u0440\u043e\u0432", None))
        self.button_tg_send.setText(QCoreApplication.translate("MainWindow", u"send", None))
        self.pushButton_save_chat.setText(QCoreApplication.translate("MainWindow", u"save", None))
        self.pushButton_test_extract.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.button_send_files.setText(QCoreApplication.translate("MainWindow", u"\u0441\u0444\u043e\u0440\u043c\u0443\u0432\u0430\u0442\u0438 \u0456 \u0432\u0456\u0434\u043f\u0440\u0430\u0432\u0438\u0442\u0438", None))
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u0439\u043b", None))
        self.menu_settings.setTitle(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u043b\u0430\u0448\u0442\u0443\u0432\u0430\u043d\u043d\u044f", None))
    # retranslateUi

