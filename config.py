import logging
import sys
import json
import os
import shutil

# Получаем путь к директории исполняемого файла
if getattr(sys, 'frozen', False):  # Если запущено как .exe
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

log_file_path = os.path.join(base_path, "app.log")

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        # Логирование в файл в той же директории
        logging.FileHandler(log_file_path),
        logging.StreamHandler()  # Логирование в консоль
    ]
)


class Config:
    def __init__(self):
        # Чтение конфигурации из config.json

        self.directory_path = ''
        self.directory_path_temp = ''
        self.directory_path_staff = ''
        self.file_extension = ''
        self.prefix_number = ''
        self.name_pattern_contract = ''
        self.name_pattern_act = ''
        self.main_chat_id = ''

        self.api_id = ''
        self.api_hash = ''
        self.phone_number = ''
        self.checkBox2FA = 0
        self.password = ''

        self.__check_structure()

    def __check_structure(self):
        # Чтение конфигурации из config_telegram.json
        # Определение пути к файлу JSON в папке с программой
        # script_dir = os.path.dirname(os.path.abspath(__file__))
        script_dir = base_path

        json_path_config_tg = os.path.join(script_dir, 'config_telegram.json')
        json_path_config = os.path.join(script_dir, 'config.json')

        logging.info(f'__check_structure')
        logging.info(f'script_dir {script_dir}')
        logging.info(f'json_path_config_tg {json_path_config_tg}')
        logging.info(f'json_path_config {json_path_config}')

        if not os.path.exists(json_path_config):
            self.__create_config()
            with open(json_path_config, 'r', encoding='utf-8') as config_file:
                config = json.load(config_file)
                   
            directory_path_temp = (config['directory_path_temp'])
            directory_path_staff = (config['directory_path_staff'])
            
            self.__check_folder('temp', True, directory_path_temp)
            self.__check_folder('staff', True, directory_path_staff)

        else:
            with open(json_path_config, 'r', encoding='utf-8') as config_file:
                config = json.load(config_file)

                directory_path_temp = (config['directory_path_temp'])
                directory_path_staff = (config['directory_path_staff'])

                self.__check_folder('temp', False, directory_path_temp)
                self.__check_folder('staff', False, directory_path_staff)

        if not os.path.exists(json_path_config_tg):
            self.__create_config_tg()

    def __check_folder(self, name: str, remove: bool, path):

        folder_path_temp = path

        # Проверьте, существует ли папка
        if not os.path.isdir(folder_path_temp):
            os.makedirs(folder_path_temp)

        if remove:
            for item in os.listdir(folder_path_temp):
                item_path = os.path.join(folder_path_temp, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)

    def __create_config(self):

        logging.info(f'__create_config')

        # script_dir = os.path.dirname(os.path.abspath(__file__))
        script_dir = base_path

        json_path_config = os.path.join(script_dir, 'config.json')

        data = {
            'directory_path': script_dir,
            'directory_path_temp': script_dir + '/temp/',
            'directory_path_staff': script_dir + '/staff/',
            'file_extension': '',
            'prefix_number': '',
            'name_pattern_contract': '',
            'name_pattern_act': '',
            'main_chat_id': ''
        }

        with open(json_path_config, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

        logging.info(f'json_file {json_file}')
        logging.info(f'config.json')

    def __create_config_tg(self):
        logging.info(f'__create_config_tg')

        # script_dir = os.path.dirname(os.path.abspath(__file__))
        script_dir = base_path

        json_path_config_tg = os.path.join(script_dir, 'config_telegram.json')

        data = {
            'api_id': '',
            'api_hash': '',
            'phone_number': '',
            '2FA': 0,
            'pass': ''
        }

        with open(json_path_config_tg, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

        logging.info(f'json_path_config_tg {json_path_config_tg}')
        logging.info(f'config_telegram.json')


def get_config():

    logging.info(f'get_config')
    conf_class = Config()

    # Чтение конфигурации из config_telegram.json
    # Определение пути к файлу JSON в папке с программой
    # script_dir = os.path.dirname(os.path.abspath(__file__))
    script_dir = base_path

    logging.info(f'script_dir {script_dir}')

    json_path_config = os.path.join(script_dir, 'config.json')
    logging.info(f'json_path_config {json_path_config}')

    if os.path.exists(json_path_config):
        with open(json_path_config, 'r', encoding='utf-8') as config_file:
            config = json.load(config_file)

            conf_class.directory_path = (config['directory_path'])
            conf_class.directory_path_temp = (config['directory_path_temp'])
            conf_class.directory_path_staff = (config['directory_path_staff'])
            conf_class.file_extension = (config['file_extension'])
            conf_class.prefix_number = (config['prefix_number'])
            conf_class.name_pattern_contract = (
                config['name_pattern_contract'])
            conf_class.name_pattern_act = (config['name_pattern_act'])
            conf_class.main_chat_id = (config['main_chat_id'])

    json_path_config_tg = os.path.join(script_dir, 'config_telegram.json')

    if os.path.exists(json_path_config_tg):
        with open(json_path_config_tg, 'r', encoding='utf-8') as config_file_tg:
            config = json.load(config_file_tg)

            conf_class.api_id = (config['api_id'])
            conf_class.api_hash = (config['api_hash'])
            conf_class.phone_number = (config['phone_number'])
            conf_class.password = config['pass']
            conf_class.checkBox2FA = config['2FA']

    return conf_class


def save_config(conf_class: Config):

    script_dir = base_path

    data = {
        'directory_path': conf_class.directory_path,
        'directory_path_temp': conf_class.directory_path_temp,
        'directory_path_staff': conf_class.directory_path_staff,
        'file_extension': conf_class.file_extension,
        'prefix_number': conf_class.prefix_number,
        'name_pattern_contract': conf_class.name_pattern_contract,
        'name_pattern_act': conf_class.name_pattern_contract,
        'main_chat_id': conf_class.main_chat_id
    }

    # Определение пути к файлу JSON в папке с программой
    # script_dir = os.path.dirname(os.path.abspath(__file__))

    json_path = os.path.join(script_dir, 'config.json')

    # Сохранение данных в JSON файл
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    data_tg = {
        'api_id': conf_class.api_id,
        'api_hash': conf_class.api_hash,
        'phone_number': conf_class.phone_number,
        '2FA': conf_class.checkBox2FA,
        'pass': conf_class.password
    }

    # Определение пути к файлу JSON в папке с программой
    # script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'config_telegram.json')

    # Сохранение данных в JSON файл
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(data_tg, json_file, indent=4, ensure_ascii=False)
