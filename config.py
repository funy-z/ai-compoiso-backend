import os
import logging


def get_dir_base_root(_path):
    if os.path.isabs(_path):
        _dir = _path
    else:
        current_dir = os.path.dirname(__file__)
        _dir = os.path.abspath(os.path.join(current_dir, _path))
    if not os.path.exists(_dir):
        os.makedirs(_dir)
        logging.info(f"Created directory: {_dir} !")
    else:
        logging.info(f"Directory already exists: {_dir}!")
    return _dir


class Config():
    PRODUCTION_ENV = True
    UVICORN_PORT = 80
    UVICORN_RELOAD = False
    ZHIPUAI_API_KEY = ''
    LOG_DIR = '/app/logs'
    SQLITE3_DB = '/app/sqlite3_db/'

    def __str__(self):
        return (f"Config(PRODUCTION_ENV: {self.PRODUCTION_ENV},"
                f"UVICORN_PORT: {self.UVICORN_PORT},"
                f"UVICORN_RELOAD: {self.UVICORN_RELOAD},"
                f"ZHIPUAI_API_KEY: {self.ZHIPUAI_API_KEY},"
                f"LOG_DIR: {self.LOG_DIR},"
                f")")


class DevelopmentConfig(Config):
    # # 测试使用
    # @staticmethod
    # def load_api_key():
    #       try:
    #           with open('.env/ZHIPUAI_API_KEY', "r") as file:
    #               result = file.read().strip()
    #               logging.info(f"open .env/ZHIPUAI_API_KEY, result: {result}")
    #               return result
    #       except FileNotFoundError:
    #           return None

    # ZHIPUAI_API_KEY = load_api_key()
    # PRODUCTION_ENV = True

    PRODUCTION_ENV = False
    UVICORN_PORT = 8000
    UVICORN_RELOAD = True
    LOG_DIR = './logs'
    SQLITE3_DB = './db/'

    def __init__(self) -> None:
        super().__init__()
        self.SQLITE3_DB = get_dir_base_root(self.SQLITE3_DB)


api_key_file = '/app/ZHIPUAI_API_KEY'


class ProductionConfig(Config):
    @staticmethod
    def load_api_key():
        try:
            with open(api_key_file, "r") as file:
                result = file.read().strip()
                logging.info(f"open {api_key_file}, result: {result}")
                return result
        except FileNotFoundError:
            return None

    ZHIPUAI_API_KEY = load_api_key()

    def __init__(self) -> None:
        super().__init__()
        self.SQLITE3_DB = get_dir_base_root(self.SQLITE3_DB)


def get_config():
    environment = os.getenv("ENVIRONMENT", "development")
    if environment == "production":
        logging.info('loaded ProductionConfig')
        return ProductionConfig()
    else:
        logging.info('loaded DevelopmentConfig')
        return DevelopmentConfig()


config = get_config()
logging.info(f'config: {config}')
