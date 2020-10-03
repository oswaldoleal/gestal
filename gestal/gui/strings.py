# TODO: this file should be a core module
import core.config as cfg

def get_string(string):
    global STRINGS
    return STRINGS[cfg.LANGUAGE][string]



# TODO this should be loaded from a file in config (?)
STRINGS = {
    'en': {
        'window_title': 'Gestal - Task Organizer',
        'task_name_label': 'Task name',
        'task_description_label': 'Task description',
        'task_due_date_label': 'Task due date',
        'task_project_label': 'Task project',
        'task_tags_label': 'Task labels',
        'task_tags_ph': '#urgent #product_owner',
        'task_save': 'Save task',
        'cancel': 'Cancel',
        'save': 'Save',
    },
    'es': {
        'window_title': 'Gestal - Organizador de Tareas',
    }
}