import logging


class LogConfig:
    def __init__(self):
        logging.basicConfig()
        logging.getLogger().setLevel(logging.INFO)


log_config = LogConfig()
