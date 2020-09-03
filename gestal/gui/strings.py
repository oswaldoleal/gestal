from core import config as cfg

def get_string(string):
    global STRINGS
    return STRINGS[cfg.LANGUAGE][string]



# TODO this should be loaded from a file in config (?)
STRINGS = {
    'en_US': {
        'window_title': 'Gestal - Task Organizer',
    },
    'es': {
        'window_title': 'Gestal - Organizador de Tareas',
    }
}