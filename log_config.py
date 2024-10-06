import logging
import logging.config
from config import config
import os

def setup_logging():
    if config.PRODUCTION_ENV:
        log_dir = os.path.abspath(config.LOG_DIR)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        logging_config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                },
            },
            'handlers': {
                'app_handler': {
                    'class': 'logging.FileHandler',
                    'filename': os.path.join(log_dir, 'app.log'),
                    'formatter': 'standard',
                    'level': 'INFO',
                },
                'ai_docs_handler': {
                    'class': 'logging.FileHandler',
                    'filename': os.path.join(log_dir, 'ai_docs.log'),
                    'formatter': 'standard',
                    'level': 'INFO',
                }
            },
            'loggers': {
                '': {
                    'handlers': ['app_handler'],
                    'level': 'INFO',
                    'propagate': True
                },
                'ai_docs': {
                    'handlers': ['ai_docs_handler'],
                    'level': 'INFO',
                    'propagate': False
                }
            }
        }
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
