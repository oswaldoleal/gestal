# all the logging constant configuration and wrappers should be placed here TODO
from datetime import datetime
from core.config import VERBOSE

class Log():
    pattern = '[{}] [{}] [{}] - {}'
    # INFO - WARNING - ERROR - DEBUG

    # TODO: move the console colors to their own class
    @classmethod
    def get_str(cls, message, origin = '', type = ''):
        date_str = datetime.now().strftime('%Y%m%d %H:%M:%S')
        return cls.pattern.format(date_str, type, origin, message)

    @classmethod
    def info(cls, message, origin = ''):
        print(cls.get_str(message, origin = origin, type = '\033[1;32;40mINFO\033[0m'))

    @classmethod
    def warning(cls, message, origin = ''):
        print(cls.get_str(message, origin = origin, type = '\033[1;33;40mWARN\033[0m'))

    @classmethod
    def error(cls, message, origin = ''):
        print(cls.get_str(message, origin = origin, type = '\033[1;31;40mERRO\033[0m'))

    @classmethod
    def debug(cls, message, origin = '', level = 0):
        if (level <= VERBOSE):
            print(cls.get_str(message, origin = origin, type = '\033[1;35;40mDEBU\033[0m'))

    # TODO: add support to save log to file