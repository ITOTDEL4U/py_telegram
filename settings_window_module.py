# settings_window_impl.py
from PySide6.QtWidgets import QDialog,  QFileDialog, QTextEdit, QLineEdit, QCheckBox, QWidget
from settings_window import Ui_Settings
import config
from PySide6.QtCore import Qt
import os
import sys

class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Settings()  # Создайте экземпляр Ui_Settings
        self.ui.setupUi(self)    # Настройте интерфейс
        self.config = config.get_config()
        self.__fill_in_the_form()

        self.ui.checkBox2FA.stateChanged.connect(
            self.__on_check_box_state_changed)
        self.ui.phone_number.setPlaceholderText("Enter phone number")
        # Установка маски для чисел
        self.ui.phone_number.setInputMask("+000000000000")
        self.ui.push_select_path.clicked.connect(self.__open_dialog_folder)

    def __fill_in_the_form(self):
        for attr_name, attr_value in self.config.__dict__.items():
            #     setattr(self.ui, attr_name, attr_value)

            widget = getattr(self.ui, attr_name, None)
            if widget:
                if isinstance(widget, QTextEdit):
                    widget.setText(attr_value)
                elif isinstance(widget, QLineEdit):
                    widget.setText(attr_value)
                elif isinstance(widget, QCheckBox):
                    widget.setChecked(attr_value)

    def __fill_in_the_class(self):
        for attr_name, attr_value in self.ui.__dict__.items():

            widget = getattr(self.ui, attr_name, None)
            value = ''

            if widget:
                if isinstance(widget, QTextEdit):
                    value = widget.toPlainText()
                elif isinstance(widget, QLineEdit):
                    value = widget.text()
                elif isinstance(widget, QCheckBox):
                    value = widget.isChecked()

            setattr(self.config, attr_name, value)

    def __open_dialog_folder(self):
        # Открытие диалогового окна выбора папки
        folder_path = QFileDialog.getExistingDirectory(
            self, "Select Directory")

        if folder_path:
            # Установка выбранного пути в QLineEdit
            self.ui.directory_path.setText(folder_path)
            self.ui.directory_path_temp.setText(folder_path + '/temp/')
            self.ui.directory_path_staff.setText(folder_path + '/staff/')

    def accept(self):
        # Здесь можно добавить код для обработки данных, если нужно
        self.__fill_in_the_class()
        config.save_config(self.config)
        os.execv(sys.executable, ['python'] + sys.argv)
        super().accept()  # Закрывает окно с успешным завершением

    def reject(self):
        # Здесь можно добавить код для отмены, если нужно
        super().reject()  # Закрывает окно б

    def __on_check_box_state_changed(self, checked):
        # Метод для обработки изменения состояния чекбокса
        if checked:
            self.ui.password.setVisible(True)
            self.ui.label_password.setVisible(True)
        else:
            self.ui.password.setVisible(False)
            self.ui.label_password.setVisible(False)
            self.ui.password.setText('')
