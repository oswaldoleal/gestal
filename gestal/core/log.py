from datetime import datetime
import core.config as cfg

class Log:
    pattern = '[{}] [{}] [{}] - {}'
    # INFO - WARNING - ERROR - DEBUG

    # TODO: move the console colors to their own class
    @classmethod
    def get_str(cls, message, origin = '', type = ''):
        date_str = datetime.now().strftime('%Y%m%d %H:%M:%S')
        return cls.pattern.format(date_str, type, origin, message)

    @classmethod
    def info(cls, message, origin = ''):
        print(cls.get_str(message, origin = origin, type = f'{ConsoleColor.green}INFO{ConsoleColor.end}'))

    @classmethod
    def warning(cls, message, origin = ''):
        print(cls.get_str(message, origin = origin, type = f'{ConsoleColor.yellow}WARN{ConsoleColor.end}'))

    @classmethod
    def error(cls, message, origin = ''):
        print(cls.get_str(message, origin = origin, type = f'{ConsoleColor.red}ERRO{ConsoleColor.end}'))

    @classmethod
    def debug(cls, message, origin = '', level = 0):
        if (level <= cfg.VERBOSE):
            print(cls.get_str(message, origin = origin, type = f'{ConsoleColor.purple}DEBU{ConsoleColor.end}'))

    # TODO: add support to save log to file

class ConsoleColor:
    green = '\033[1;32;40m'
    yellow = '\033[1;33;40m'
    red = '\033[1;31;40m'
    purple = '\033[1;35;40m'
    end = '\033[0m'