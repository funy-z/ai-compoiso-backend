import logging
import logging.config
import os
import json

from config import config


def setup_logging():
    if config.PRODUCTION_ENV:
        log_dir = os.path.abspath(config.LOG_DIR)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        # 读取log配置
        with open('logging_config.json', 'r') as f:
            logging_config = json.load(f)

        # 调整filename为绝对路径
        for handler in logging_config['handlers'].values():
            if 'filename' in handler:
                handler['filename'] = os.path.join(
                    log_dir, handler['filename'])
    else:
        logging_config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'standard',
                    'level': 'DEBUG',
                },
            },
            'loggers': {
                '': {
                    'handlers': ['console'],
                    'level': 'DEBUG',
                    'propagate': True
                },
            }
        }

    logging.config.dictConfig(logging_config)


appLogger = logging

setup_logging()
