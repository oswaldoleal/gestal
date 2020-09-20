from .models import Project, Task
from .persistence import DefaultStorage, Persistence

class Backend:
    # this persistence object should be handled as a singleton TODO
    persistence = None

    def __init__(self):
        self.persistence = Persistence()

    # TODO: new_task

    # TODO: get_task

    # TODO: get_tasks

    # TODO: new_project
    def new_project(self, name = None, description = None):
        project = Project(owner_id = 'oswaldo', name = name, description = description, persistence = self.persistence)
        project.save()
    # TODO: get_project

    # TODO: get_projects

    # TODO: get_project_progress

    # TODO: new_team

    # TODO: get_team

    # TODO: get_teams

    # TODO: new_milestone

    # TODO: get_milestone

    # TODO: get_milestones

    # TODO: new_tag

    # TODO: get_tag

    # TODO: get_tags


    def get_tasks(self, filter = None):
        return Task.get_all(Task, self.persistence, filter = filter)

    def get_projects(self, filter = None):
        return Project.get_all(Project, self.persistence, filter = filter)