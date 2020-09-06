from core import config as cfg

def get_string(string):
    global STRINGS
    return STRINGS[cfg.LANGUAGE][string]



# TODO this should be loaded from a file in config (?)
STRINGS = {
    'en_US': {
        'window_title': 'Gestal - Task Organizer',
        'task_name_label': 'Task name',
        'task_description_label': 'Task description',
        'task_due_date_label': 'Task due date',
        'task_project_label': 'Task project',
    },
    'es': {
        'window_title': 'Gestal - Organizador de Tareas',
    }
}