# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_window.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QGridLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QTabWidget, QTextEdit,
    QWidget)

class Ui_Settings(object):
    def setupUi(self, Settings):
        if not Settings.objectName():
            Settings.setObjectName(u"Settings")
        Settings.resize(753, 420)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Settings.sizePolicy().hasHeightForWidth())
        Settings.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(Settings)
        self.gridLayout.setObjectName(u"gridLayout")
        self.buttonBox = QDialogButtonBox(Settings)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.tabWidget = QTabWidget(Settings)
        self.tabWidget.setObjectName(u"tabWidget")
        self.Telegram = QWidget()
        self.Telegram.setObjectName(u"Telegram")
        self.label_api_hash = QLabel(self.Telegram)
        self.label_api_hash.setObjectName(u"label_api_hash")
        self.label_api_hash.setGeometry(QRect(10, 50, 100, 22))
        self.label_password = QLabel(self.Telegram)
        self.label_password.setObjectName(u"label_password")
        self.label_password.setGeometry(QRect(10, 160, 100, 22))
        self.api_id = QTextEdit(self.Telegram)
        self.api_id.setObjectName(u"api_id")
        self.api_id.setGeometry(QRect(120, 10, 400, 26))
        self.label_2FA = QLabel(self.Telegram)
        self.label_2FA.setObjectName(u"label_2FA")
        self.label_2FA.setGeometry(QRect(10, 130, 100, 22))
        self.checkBox2FA = QCheckBox(self.Telegram)
        self.checkBox2FA.setObjectName(u"checkBox2FA")
        self.checkBox2FA.setGeometry(QRect(120, 130, 400, 22))
        self.label_api_id = QLabel(self.Telegram)
        self.label_api_id.setObjectName(u"label_api_id")
        self.label_api_id.setGeometry(QRect(10, 10, 100, 22))
        self.api_hash = QTextEdit(self.Telegram)
        self.api_hash.setObjectName(u"api_hash")
        self.api_hash.setGeometry(QRect(120, 50, 400, 26))
        self.label_phone_number = QLabel(self.Telegram)
        self.label_phone_number.setObjectName(u"label_phone_number")
        self.label_phone_number.setGeometry(QRect(10, 90, 100, 22))
        self.password = QLineEdit(self.Telegram)
        self.password.setObjectName(u"password")
        self.password.setGeometry(QRect(120, 160, 400, 22))
        self.password.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)
        self.phone_number = QLineEdit(self.Telegram)
        self.phone_number.setObjectName(u"phone_number")
        self.phone_number.setGeometry(QRect(120, 90, 400, 22))
        self.main_chat_id = QTextEdit(self.Telegram)
        self.main_chat_id.setObjectName(u"main_chat_id")
        self.main_chat_id.setGeometry(QRect(120, 210, 400, 26))
        self.label_main_chat_id = QLabel(self.Telegram)
        self.label_main_chat_id.setObjectName(u"label_main_chat_id")
        self.label_main_chat_id.setGeometry(QRect(10, 210, 100, 22))
        self.tabWidget.addTab(self.Telegram, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.label_2 = QLabel(self.tab_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 10, 101, 50))
        self.directory_path = QLineEdit(self.tab_2)
        self.directory_path.setObjectName(u"directory_path")
        self.directory_path.setGeometry(QRect(200, 20, 400, 22))
        self.directory_path_temp = QLineEdit(self.tab_2)
        self.directory_path_temp.setObjectName(u"directory_path_temp")
        self.directory_path_temp.setGeometry(QRect(200, 100, 400, 22))
        self.directory_path_temp.setReadOnly(True)
        self.label_7 = QLabel(self.tab_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(10, 90, 101, 50))
        self.label_file_extension = QLabel(self.tab_2)
        self.label_file_extension.setObjectName(u"label_file_extension")
        self.label_file_extension.setGeometry(QRect(10, 130, 101, 50))
        self.file_extension = QLineEdit(self.tab_2)
        self.file_extension.setObjectName(u"file_extension")
        self.file_extension.setGeometry(QRect(200, 140, 400, 22))
        self.prefix_number = QLineEdit(self.tab_2)
        self.prefix_number.setObjectName(u"prefix_number")
        self.prefix_number.setGeometry(QRect(200, 180, 400, 22))
        self.label_prefix_number = QLabel(self.tab_2)
        self.label_prefix_number.setObjectName(u"label_prefix_number")
        self.label_prefix_number.setGeometry(QRect(10, 170, 81, 50))
        self.name_pattern_contract = QLineEdit(self.tab_2)
        self.name_pattern_contract.setObjectName(u"name_pattern_contract")
        self.name_pattern_contract.setGeometry(QRect(200, 220, 400, 22))
        self.label_name_pattern_contract = QLabel(self.tab_2)
        self.label_name_pattern_contract.setObjectName(u"label_name_pattern_contract")
        self.label_name_pattern_contract.setGeometry(QRect(10, 220, 171, 21))
        self.name_pattern_act = QLineEdit(self.tab_2)
        self.name_pattern_act.setObjectName(u"name_pattern_act")
        self.name_pattern_act.setGeometry(QRect(200, 260, 400, 22))
        self.label_name_pattern_act = QLabel(self.tab_2)
        self.label_name_pattern_act.setObjectName(u"label_name_pattern_act")
        self.label_name_pattern_act.setGeometry(QRect(10, 260, 151, 20))
        self.push_select_path = QPushButton(self.tab_2)
        self.push_select_path.setObjectName(u"push_select_path")
        self.push_select_path.setGeometry(QRect(610, 20, 22, 22))
        self.label_8 = QLabel(self.tab_2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(10, 50, 101, 50))
        self.directory_path_staff = QLineEdit(self.tab_2)
        self.directory_path_staff.setObjectName(u"directory_path_staff")
        self.directory_path_staff.setGeometry(QRect(200, 60, 400, 22))
        self.directory_path_staff.setReadOnly(True)
        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)


        self.retranslateUi(Settings)
        self.buttonBox.accepted.connect(Settings.accept)
        self.buttonBox.rejected.connect(Settings.reject)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Settings)
    # setupUi

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QCoreApplication.translate("Settings", u"Settings", None))
        self.label_api_hash.setText(QCoreApplication.translate("Settings", u"<html><head/><body><p align=\"right\">API Hash</p></body></html>", None))
        self.label_password.setText(QCoreApplication.translate("Settings", u"<html><head/><body><p align=\"right\">Password</p></body></html>", None))
        self.label_2FA.setText(QCoreApplication.translate("Settings", u"<html><head/><body><p align=\"right\">2FA</p></body></html>", None))
        self.checkBox2FA.setText("")
        self.label_api_id.setText(QCoreApplication.translate("Settings", u"<html><head/><body><p align=\"right\">API ID</p></body></html>", None))
        self.label_phone_number.setText(QCoreApplication.translate("Settings", u"<html><head/><body><p align=\"right\">Phone numer</p></body></html>", None))
        self.label_main_chat_id.setText(QCoreApplication.translate("Settings", u"<html><head/><body><pre align=\"right\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"tw-target\"/><span style=\" font-family:'Courier New';\">m</span><span style=\" font-family:'Courier New';\">ain chat id</span></pre></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Telegram), QCoreApplication.translate("Settings", u"Telegram", None))
        self.label_2.setText(QCoreApplication.translate("Settings", u"<html><head/><body><p align=\"center\">\u041f\u0443\u0442\u044c \u043a \u043f\u0430\u043f\u043a\u0435</p></body></html>", None))
        self.label_7.setText(QCoreApplication.translate("Settings", u"<html><head/><body><p align=\"center\">\u041f\u0443\u0442\u044c \u043a  temp</p></body></html>", None))
        self.label_file_extension.setText(QCoreApplication.translate("Settings", u"<html><head/><body><p align=\"center\">\u0420\u0430\u0441\u0448\u0438\u0440\u0435\u043d\u0438\u0435</p></body></html>", None))
        self.file_extension.setText(QCoreApplication.translate("Settings", u".xls", None))
        self.prefix_number.setText(QCoreApplication.translate("Settings", u"8632/24/", None))
        self.label_prefix_number.setText(QCoreApplication.translate("Settings", u"<html><head/><body><p align=\"center\">\u041f\u0440\u0435\u0444\u0438\u043a\u0441</p></body></html>", None))
        self.name_pattern_contract.setText(QCoreApplication.translate("Settings", u"\u0414\u043e\u0433\u043e\u0432\u0456\u0440 \u043a\u0443\u043f\u0456\u0432\u043b\u0456-\u043f\u0440\u043e\u0434\u0430\u0436\u0443", None))
        self.label_name_pattern_contract.setText(QCoreApplication.translate("Settings", u"<html><head/><body><p align=\"center\">\u041f\u0430\u0442\u0442\u0435\u0440\u043d \u043f\u043e\u0438\u0441\u043a\u0430 \u0434\u043e\u0433\u043e\u0432\u043e\u0440\u0430</p></body></html>", None))
        self.name_pattern_act.setText(QCoreApplication.translate("Settings", u"ActInspectSale", None))
        self.label_name_pattern_act.setText(QCoreApplication.translate("Settings", u"<html><head/><body><p align=\"center\">\u041f\u0430\u0442\u0442\u0435\u0440\u043d\u043e \u043f\u043e\u0438\u0441\u043a\u0430 \u0430\u043a\u0442\u0430</p></body></html>", None))
        self.push_select_path.setText(QCoreApplication.translate("Settings", u"...", None))
        self.label_8.setText(QCoreApplication.translate("Settings", u"<html><head/><body><p align=\"center\">\u041f\u0443\u0442\u044c \u043a staff</p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Settings", u"Files Excel", None))
    # retranslateUi

