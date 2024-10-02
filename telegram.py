import json
import getpass  # Для безопасного ввода пароля
from telethon import TelegramClient, sync, events
from telethon.errors.rpcerrorlist import SessionPasswordNeededError
from telethon.tl.types import User, Chat
import os
import asyncio
# from config import Config
import config

# client = TelegramClient(
#     'automat_session', self.api_id, self.api_hash,)
# @client.on(events.NewMessage)
# async def my_event_handler(event):
#     if 'hello' in event.raw_text:
#         await event.reply('hi!')


   

# async def code_callback():
#     return await get_input("Пожалуйста, введите код, который вы получили:")


# async def password_callback():
#     return await get_input("Пожалуйста, введите ваш пароль:")
    
    
class SettingsTelegram:
    client = None
    def __init__(self):
        # Чтение конфигурации из config_telegram.json
      

            self.api_id = ''
            self.api_hash = ''
            self.phone_number = ''
            self.pwd = ''
            self.__fill_in_the_class()

            client = TelegramClient(
                'automat_session', self.api_id, self.api_hash,)
            self.client = client

            # Подписка на новые сообщения
            self.client.on(events.NewMessage)(self.handle_new_message)
           
            self.message_callback = None  # Ссылка на колбэк

    

    def set_message_callback(self, callback):
        self.message_callback = callback

    async def handle_new_message(self, event):
        
        message_text = event.message.message
        sender_id = event.sender_id
        print(f"ТЕСТ МОДУЛЬ ТЕЛЕГРАМ  handle_new_message {
              sender_id}: {message_text}")
        # Вызываем колбэк, если он установлен
        if self.message_callback:
            await self.message_callback(sender_id, message_text)


    async def send_file(self, chat_id, file_path):
        async with self.client:
            await self.client.send_file(chat_id, file_path)
    
    def __fill_in_the_class(self):

        conf = config.get_config()
        for attr_name, attr_value in conf.__dict__.items():
            attr = getattr(self, attr_name, None)

            if hasattr(self, attr_name):
                setattr(self, attr_name, attr_value)

    async def connect(self, callback_tg_phone, callback_tg_code, callback_tg_pass):
        settings = config.get_config()
        if not settings.api_id:
            return

        try:
            await self.client.start(
                phone= callback_tg_phone,  # Колбек для телефона
                code_callback=callback_tg_code,          # Колбек для кода
                password=callback_tg_pass)
            
        except SessionPasswordNeededError:
                print("Авторизация не прошла успешно")
                return  # Выходим из функции, если авторизация не прошла
        
        
        # if settings.checkBox2FA:
        #     try:
        #         await self.client.start(password=self.pwd)
        #     except SessionPasswordNeededError:
        #         print("Авторизация не прошла успешно")
        #         return
        # else:
        #     try:
        #        await self.client.start(phone=settings.phone_number,code_callback= code_callback)
        #     except SessionPasswordNeededError:
        #         print("Авторизация не прошла успешно")
        #         return  # Выходим из функции, если авторизация не прошла

        #     # Если не возникло ошибки, но требуется ввод телефона
        #     try:
        #         await self.client.start(phone=settings.phone_number)
        #     except SessionPasswordNeededError:
        #         print("Авторизация не прошла успешно")
        #         return
        
        
        
        
        
        
        
        # Ваш основной код тут
        # Например, получение информации о себе:
        # me = await self.client.get_me()
        # print(f'Привет, {me.first_name}!')

        # # # Получаем список чатов
        # async for dialog in self.client.iter_dialogs():
        #     # Проверяем наличие атрибутов перед их использованием
        #     name = dialog.name
        #     id = dialog.id
        #     username = getattr(dialog, 'username', 'Нет username')
        #     print(f'Название: {name}, ID: {id}, Username: {username}')

        # Получаем последние 5 сообщений из указанного чата
        # chat_id = 1353211874
        # messages = await self.client.get_messages(chat_id, limit=15)

        # # Выводим сообщения
        # for message in messages:
        #     print(f'ID: {message.id}, Дата: {message.date}, Текст: {message.text}')

        # Пример отправки сообщения
        # chat_id = -1001260324106  # Хранителі зради🇺🇦
        # await self.send_message(chat_id, "Привет! Это тестовое сообщение сформированное на python библиотеке телеграм от моего имени. Возможно даже ботом")

        # await self.client.disconnect()





    async def get_messages(self, dialog_id, limit=20):

        messages = await self.client.get_messages(dialog_id, limit)
        return messages
       
    async def get_dialogs_with_pictures(self):

        dialogs_with_pictures = []
        config_unit = config.get_config()
        directory_path_staff = config_unit.directory_path_staff

        async for dialog in self.client.iter_dialogs():

            id = dialog.id
            username = getattr(dialog.entity, 'username', None)
            dialogname = dialog.name

            # Используем username, если он есть, иначе используем dialogname
            # Если оба отсутствуют, используем "Нет username"
            display_name = username if username else (
                dialogname if dialogname else 'Нет username')

            photo_file_name = f"photo_{dialog.id}.jpg"
            photo_file_path = os.path.join(
                directory_path_staff, photo_file_name)

            if os.path.exists(photo_file_path):
                # Файл существует, используем его
                photo_url = photo_file_path
            else:
                photo_url = photo_file_path  # Локальный путь к файлу
                await self.client.download_profile_photo(dialog.id, file=photo_file_path, download_big=False)

            dialogs_with_pictures.append((id, display_name, photo_url))

        return dialogs_with_pictures


    async def disconnect(self):
        try:
            await self.client.disconnect()
        except SessionPasswordNeededError:
            print("disconnect не прошла успешно")
            return

        print("disconnect  успешно")

    async def send_message(self, chat_id, message):
        try:
            await self.client.send_message(chat_id, message)

        except Exception as e:
            print(f'Ошибка при отправке сообщения: {e}')

    def run(self):
        import asyncio
        asyncio.run(self.connect())  # Запускаем асинхронный метод
