from datetime import datetime
from os.path import join
import core.config as cfg
import core.info as info

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
        cls.save_to_log(cls.get_str(message, origin = origin, type = 'INFO'))

    @classmethod
    def warning(cls, message, origin = ''):
        print(cls.get_str(message, origin = origin, type = f'{ConsoleColor.yellow}WARN{ConsoleColor.end}'))
        cls.save_to_log(cls.get_str(message, origin = origin, type = '{WARN'))

    @classmethod
    def error(cls, message, origin = ''):
        print(cls.get_str(message, origin = origin, type = f'{ConsoleColor.red}ERRO{ConsoleColor.end}'))
        cls.save_to_log(cls.get_str(message, origin = origin, type = 'ERRO'))

    @classmethod
    def debug(cls, message, origin = '', level = 0):
        if (level <= cfg.VERBOSE):
            print(cls.get_str(message, origin = origin, type = f'{ConsoleColor.purple}DEBU{ConsoleColor.end}'))
            cls.save_to_log(cls.get_str(message, origin = origin, type = 'DEBU'))

    @classmethod
    def save_to_log(cls, message):
        with open(join(cfg.LOG_PATH, f'{info.NAME}.log'), 'a') as f:
            f.write(f'{message}\n')

class ConsoleColor:
    green = '\033[1;32;40m'
    yellow = '\033[1;33;40m'
    red = '\033[1;31;40m'
    purple = '\033[1;35;40m'
    end = '\033[0m'