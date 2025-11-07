from logging.config import dictConfig

LOGGING_CONFIG: dict = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            # 'datefmt': '%Y-%m-%d %H:%M:%S',
            'format': '[%(asctime)s] |%(levelname)s| (%(name)s.%(funcName)s:%(lineno)d): %(message)s',
        },
    },
    'handlers': {
        'default_console': {
            'level': 'INFO',
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default_console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


def setup_logging() -> None:
    dictConfig(LOGGING_CONFIG)
