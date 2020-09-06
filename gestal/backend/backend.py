from .models import Task
from .persistence import Persistence, DefaultStorage

class Backend:
    # this persistence object should be handled as a singleton TODO
    persistence = None

    def __init__(self):
        self.persistence = Persistence()

    # TODO: new_task
    # TODO: get_task
    # TODO: new_project
    # TODO: get_project
    # TODO: get_project_progress
    # TODO: new_team
    # TODO: get_project
    # TODO: new_milestone
    # TODO: get_milestone
    # TODO: new_tag
    # TODO: get_tags