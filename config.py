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
    # ZHIPUAI_API_KEY = ''
    LOG_DIR = '/app/logs'
    SQLITE3_DB = '/app/sqlite3_db/'
    API_KEY_DIR = '/app/environ'

    def __str__(self):
        return (f"Config(PRODUCTION_ENV: {self.PRODUCTION_ENV},"
                f"UVICORN_PORT: {self.UVICORN_PORT},"
                f"UVICORN_RELOAD: {self.UVICORN_RELOAD},"
                f"LOG_DIR: {self.LOG_DIR},"
                f")")


class DevelopmentConfig(Config):
    # 测试使用
    # PRODUCTION_ENV = True

    PRODUCTION_ENV = False
    UVICORN_PORT = 8000
    UVICORN_RELOAD = True
    LOG_DIR = './logs'
    SQLITE3_DB = './db/'
    API_KEY_DIR = './.env'

    def __init__(self) -> None:
        super().__init__()
        self.SQLITE3_DB = get_dir_base_root(self.SQLITE3_DB)
        self.API_KEY_DIR = get_dir_base_root(self.API_KEY_DIR)


class ProductionConfig(Config):
    def __init__(self) -> None:
        super().__init__()
        self.SQLITE3_DB = get_dir_base_root(self.SQLITE3_DB)
        self.API_KEY_DIR = get_dir_base_root(self.API_KEY_DIR)


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
