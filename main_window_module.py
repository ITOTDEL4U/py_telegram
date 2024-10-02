import sys
import asyncio
from PySide6.QtWidgets import QMainWindow, QListWidgetItem, QInputDialog
from PySide6.QtCore import QTimer, Qt
from telegram import SettingsTelegram
from main_window_dkp import Ui_MainWindow  # Импортируйте сгенерированный класс
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Slot
from settings_window_module import SettingsWindow
from telethon import events
import config
import re
import excel_com


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.telegram = SettingsTelegram()
        self.loop = asyncio.get_event_loop()

        # Создаем объект QTimer
        # Периодический опрос каждые 1000 мс (1 секунда)
        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_event_loop_add)
        self.timer.start(1000)

        self.is_connected = False
        self.dialogs_with_pictures = []

        # self.loop.run_until_complete(self.start_telegram_connection())

        self.ui.comboBox.currentIndexChanged.connect(
            self.__on_combobox_selection_changed)

        self.ui.pushButton_save_chat.clicked.connect(
            self.__event_button_save_chat)
        self.ui.button_tg_send.clicked.connect(
            self.__event_button_tg_send)

        self.ui.button_exit.triggered.connect(self.__event_menu_button_exit)
        self.ui.button_settings.triggered.connect(
            self.__event_menu_button_settings)

        self.ui.button_send_files.clicked.connect(
            self.__event_button_send_files)

    # ====================================================================
    # ========== АСИНХРОННЫЕ ФУНКЦИИ ======== ============================
    # ====================================================================

    # Вызываем run_function и передаем greet с параметром
    # run_function(greet, "Алексей")

    def timer_event_loop_add(self):

        self.run_async_function(self.start_telegram_connection)

        # print('Зашли в timer_event_loop_add')
        self.run_async_function(self.get_messages_async)
        # print('Вышли из timer_event_loop_add')

    def run_async_function(self, func, *args, **kwargs):
        # print('Зашли в run_async_function')
        self.loop.run_until_complete(func(*args, **kwargs))
        # print('Вышли из run_async_function')

    async def start_telegram_connection(self):
        # Подключение к Telegram
        if not self.is_connected:
            print(f'тест start_telegram_connection ')
            try:
                await self.telegram.connect(self.callback_tg_phone,
                                            self.callback_tg_code,
                                            self.callback_tg_pass)
                self.is_connected = True

            except Exception as e:
                self.show_message(f"Error connecting: {e}")

            self.show_message(f"Connected: {self.is_connected}")
            self.telegram.client.add_event_handler(
                self.handler, events.NewMessage())
            self.dialogs_with_pictures = await self.telegram.get_dialogs_with_pictures()
            self.__populate_combo_box()
            self.__populate_listiWdget_recipient()

    async def get_messages_async(self):
        try:
            if self.is_connected:
                dialog_id = self.ui.comboBox.currentData()
                print(f"ТЕСТ get_messages_async dialog_id: {dialog_id}")
                # Замените этот пример вызова асинхронного метода на ваш собственный
                messages = await self.telegram.get_messages(dialog_id, limit=20)

                self.display_messages(messages)

        except Exception as e:
            print(f"Error in get_messages_async: {e}")

    async def stop_telegram_connection(self):
        # Отключение от Telegram
        print("stop_telegram_connection")
        if self.is_connected:
            try:
                await self.telegram.disconnect()
                self.is_connected = False
                print("Disconnected successfully")
            except Exception as e:
                print(f"Error disconnecting: {e}")

    async def send_message_to_tg(self, dialog_id, message):
        await self.telegram.send_message(dialog_id, message)

    async def send_file_to_tg(self, dialog_id, file_pah):
        await self.telegram.send_file(dialog_id, file_pah)

    async def callback_tg_phone(self):
        result, ok = QInputDialog.getText(
            self, "Input", "Пожалуйста, введите номер телефона:"
        )
        if ok:
            return result
        return None

    async def callback_tg_code(self):
        result, ok = QInputDialog.getText(
            self, "Input", "Пожалуйста, введите код, который вы получили:"
        )
        if ok:
            return result
        return None

    async def callback_tg_pass(self):
        result, ok = QInputDialog.getText(
            self, "Input", "Пожалуйста, введите ваш пароль:"
        )
        if ok:
            return result
        return None
    # ====================================================================
    # ========== ФУНКЦИИ РАБОТЫ С ИНТЕРФЕЙСОМ ============================
    # ====================================================================

    def __event_button_send_files(self):

        conf = config.get_config()
        answer = excel_com.get_soname_and_auto()
        selected_dialog_id_reserv = self.ui.comboBox.currentData()
        selected_dialog_id_for_file = ''

        current_item = self.ui.listiWdget_recipient.currentItem()
        if current_item:
            selected_dialog_id_for_file = current_item.data(Qt.UserRole)

        selected_dialog_id_reserv = self.ui.comboBox.currentData()

        if not self.is_value_filled(selected_dialog_id_for_file):
            self.show_message(f"Не удалось определить получателя {
                              selected_dialog_id_for_file}")
            return

        if not self.is_value_filled(selected_dialog_id_reserv):
            self.show_message(f"Не удалось определить резерв {
                              selected_dialog_id_reserv}")
            return

        # Нужно получить номер
        num_text = self.ui.textEdit_parsing.toPlainText()
        # Преобразуем строку в целое число
        num = int(num_text)
        next_number = num + 1

        # Если нужно, преобразуем результат обратно в строку с нулями в начале
        next_number = str(next_number).zfill(len(num_text))

        message = f"{answer} {next_number}"
        # нужно зарезервировать себе номер

        self.run_async_function(self.send_message_to_tg,
                                selected_dialog_id_reserv, message)

        excel_com.clear_directory(conf.directory_path_temp)

        path_contract = excel_com.change_contract(next_number)
        path_act = excel_com.change_act(next_number)

        # нужно отправить файлы
        self.run_async_function(self.send_file_to_tg,
                                selected_dialog_id_for_file, path_contract)
        self.run_async_function(self.send_file_to_tg,
                                selected_dialog_id_for_file, path_act)

    def __event_menu_button_exit(self, event):
        # self.close()  # Закрываем окно после выполнения асинхронной задачи

        if self.is_connected:

            # Запускаем асинхронную задачу для отключения  (ОНА УЖЕ В ОЧЕРЕДИ)
            asyncio.run(self.stop_telegram_connection())
            # Закрыть окно после выполнения задачи
            QTimer.singleShot(0, self.close)

            # QTimer.singleShot(0, self.run_disconnect_task)
            event.ignore()  # Отменяем обычное закрытие, чтобы дождаться завершения задачи
        else:
            super().closeEvent(event)  # Просто закрываем, если не подключены

    def __event_menu_button_settings(self):
        self.settings_window = SettingsWindow()  # Создаем экземпляр нового окна
        self.settings_window.exec()  # Используйте exec() для модального окна

    def __event_button_save_chat(self):
        conf = config.get_config()
        conf.main_chat_id = str(self.ui.comboBox.currentData())
        config.save_config(conf)
        self.show_message("save")

    def __event_button_tg_send(self):
        selected_dialog_id = self.ui.comboBox.currentData()
        message = self.ui.text_tg_output_message.toPlainText()

        self.run_async_function(self.send_message_to_tg,
                                selected_dialog_id, message)

    def show_message(self, text):

        self.ui.statusbar.setStyleSheet("QStatusBar { color: red; }")
        self.ui.statusbar.showMessage(text, 3000)

    def __on_combobox_selection_changed(self):

        # Очищаем текстовое поле
        self.ui.text_tg_input_message.clear()
        self.run_async_function(self.get_messages_async)

    def __populate_combo_box(self):
        conf = config.get_config()
        self.ui.comboBox.blockSignals(True)  # Отключаем сигналы
        self.ui.comboBox.clear()  # Очищаем старые элементы

        for id, username, photo_url in self.dialogs_with_pictures:
            # Загружаем изображение
            pixmap = QPixmap(photo_url)
            icon = QIcon(pixmap)

            # Добавляем элемент в QComboBox

            self.ui.comboBox.addItem(icon, username, id)

            if conf.main_chat_id == str(id):
                current_index = self.ui.comboBox.count() - 1
                self.ui.comboBox.setCurrentIndex(current_index)

        self.ui.comboBox.blockSignals(False)  # Включаем сигналы снова

    def __populate_listiWdget_recipient(self):

        # Очищаем QListWidget перед добавлением новых элементов
        self.ui.listiWdget_recipient.clear()

        for id, username, photo_url in self.dialogs_with_pictures:
            # Загружаем изображение
            pixmap = QPixmap(photo_url)
            icon = QIcon(pixmap)

            # Создаем элемент списка
            item = QListWidgetItem(icon, username)

            # Сохраняем id как пользовательские данные
            item.setData(Qt.UserRole, id)

            # Добавляем элемент в QListWidget
            self.ui.listiWdget_recipient.addItem(item)

    # ====================================================================
    # ========== другие ФУНКЦИИ ==========================================
    # ====================================================================

    def extract_number_from_end(self, text):
        # Ищем число в конце строки
        match = re.search(r'(\d+)\s*[^0-9]*$', text)

        if match:
            result = match.group(1)  # Если найдено, получаем число
        else:
            result = ''  # Если не найдено, пустая строка

        return result  # Возвращаем результат

    def display_messages(self, messages):
        # Отображаем сообщения в text_tg_input_message
        # Предполагается, что сообщения имеют атрибут 'text'
        first_message = messages[0].text

        # Пропускаем сообщения с текстом None или пустым
        if first_message:
            num_text = self.extract_number_from_end(first_message)
            text_in_textEdit_parsing = self.ui.textEdit_parsing.toPlainText()
            if num_text == text_in_textEdit_parsing:
                return

        sorted_messages = sorted(messages, key=lambda msg: msg.date)

        html_content = '<html><body style="background-color: black; color: white;">'
        for message in sorted_messages:
            text = message.text
            # Пропускаем сообщения с текстом None или пустым
            if not text:
                continue

            num_text = self.extract_number_from_end(text)
            if self.is_value_filled(num_text):
                self.ui.textEdit_parsing.clear()
                self.ui.textEdit_parsing.setPlainText(str(num_text))

            # Заменяем переносы строк на <br> для HTML
            text = text.replace('\n', '<br>')

            if message.out:
                # Исходящее сообщение: голубой фон, закругленные углы
                formatted_text = (
                    f'<div style="background-color: #87CEEB; color: black; '
                    'border-radius: 10px; padding: 10px; margin-bottom: 10px; '
                    'text-align: right; display: inline-block; max-width: 70%; '
                    'margin-left: auto; margin-right: 0; word-wrap: break-word;">'
                    f'{text}</div>'
                )
            else:
                # Входящее сообщение: белый фон, закругленные углы
                formatted_text = (
                    f'<div style="background-color: white; color: black; '
                    'border-radius: 10px; padding: 10px; margin-bottom: 10px; '
                    'text-align: left; display: inline-block; max-width: 70%; '
                    'margin-right: auto; margin-left: 0; word-wrap: break-word;">'
                    f'{text}</div>'
                )

            html_content += formatted_text

        html_content += '</body></html>'

        # Обновляем содержимое QTextEdit с HTML-контентом
        self.ui.text_tg_input_message.setHtml(html_content)
        # self.ui.text_browser_input_message.setHtml(html_content)

        # Прокручиваем QTextEdit до конца
        # Используем QTimer для отсрочки прокрутки
        QTimer.singleShot(0, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        # Прокручиваем QTextEdit до конца
        self.ui.text_tg_input_message.verticalScrollBar().setValue(
            self.ui.text_tg_input_message.verticalScrollBar().maximum())

    def is_value_filled(self, num_text):
        # Проверяем, что num_text не None и не пустая строка, и массив не пуст
        # Проверяем, что num_text не равно None
        if num_text is None:
            return False

        # Проверяем, если num_text является целым числом
        if isinstance(num_text, int):
            return True

        # Проверяем, если num_text является булевым значением
        if isinstance(num_text, bool):
            return num_text  # Возвращаем True, только если num_text == True

        # Проверяем, если num_text является строкой
        if isinstance(num_text, str):
            # Возвращаем True, если строка не пустая
            return num_text.strip() != ""

        # Проверяем, если num_text является списком
        if isinstance(num_text, list):
            # Возвращаем True, если список не пустой
            return len(num_text) > 0

        # Если num_text не подходит под ни один из предыдущих типов
        return False

    async def handler(self, event):
        if event.is_reply:
            replied = await event.get_reply_message()
            sender = replied.sender
            message_text = replied.message
            print(f'сработала  async def handler БЛОК IF Сообщение от {
                  sender.username}: "{message_text}"')
        else:
            sender = event.sender
            message_text = event.message.message
            print(f'сработала  async def handler БЛОК else Сообщение от"{
                  message_text}", отправлено пользователем: {sender.username}')

        num_text = self.extract_number_from_end(message_text)
        self.ui.textEdit_parsing.clear()
        self.ui.textEdit_parsing.setPlainText(str(num_text))
