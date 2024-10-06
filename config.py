import os
import logging

class Config():
  PRODUCTION_ENV = True
  UVICORN_PORT = 80
  UVICORN_RELOAD = False
  ZHIPUAI_API_KEY = ''
  LOG_DIR = '/app/logs'

  def __str__(self):
      return (f"Config(PRODUCTION_ENV: {self.PRODUCTION_ENV},"
              f"UVICORN_PORT: {self.UVICORN_PORT},"
              f"UVICORN_RELOAD: {self.UVICORN_RELOAD},"
              f"ZHIPUAI_API_KEY: {self.ZHIPUAI_API_KEY},"
              f"LOG_DIR: {self.LOG_DIR},"
              f")")

class DevelopmentConfig(Config):
  # 测试使用
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

  PRODUCTION_ENV = False
  UVICORN_PORT = 8000
  UVICORN_RELOAD = True
  LOG_DIR = './logs'

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
