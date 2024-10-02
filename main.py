import sys
from PySide6.QtWidgets import QApplication
from main_window_module import MainWindow
import asyncio
from telethon import TelegramClient, events
import config
from telethon.errors.rpcerrorlist import SessionPasswordNeededError



   
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
