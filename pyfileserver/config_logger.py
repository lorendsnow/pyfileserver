from logging import getLogger
from logging.config import dictConfig


def make_logger(name: str, log_path: str):

    CONFIG_DICT = {
        "version": 1.0,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
        "handlers": {
            "file": {
                "class": "logging.FileHandler",
                "filename": log_path,
                "level": "DEBUG",
                "formatter": "simple",
            },
        },
        "root": {"level": "DEBUG", "handlers": ["file"]},
    }

    dictConfig(CONFIG_DICT)

    return getLogger(name)
