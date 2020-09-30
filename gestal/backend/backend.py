from .models import Project, Task, Tag, TagAssignment, Team, TeamPermission, User
from .persistence import DefaultStorage, Persistence

class Backend:
    # this persistence object should be handled as a singleton TODO
    persistence = None

    def __init__(self):
        self.persistence = Persistence()

    ## TASK
    def new_task(self, name = None, description = None, due_date = None, tags = None):
        # TODO: properly handle the owner id application wide
        # TODO: handle the parent_id
        # TODO: handle the project_id from the currently selected
        # TODO: handle the tags
        task = Task(name = name, owner_id = 'oswaldo', parent_id = None, project_id = '1', description = description, status = False, due_date = due_date, persistence = self.persistence)
        task.save()

    # TODO: get_task

    def get_tasks(self, filter = None):
        return Task.get_all(Task, self.persistence, filter = filter)

    ## PROJECT
    def new_project(self, name = None, description = None):
        # TODO: properly handle the owner id application wide
        project = Project(owner_id = 'oswaldo', name = name, description = description, persistence = self.persistence)
        project.save()

    # TODO: get_project

    def get_projects(self, filter = None):
        return Project.get_all(Project, self.persistence, filter = filter)

    # TODO: get_project_progress

    ## TEAM
    # TODO: new_team

    # TODO: get_team

    def get_teams(self, filter = None):
        return Team.get_all(Team, self.persistence, filter = filter)

    ## TEAM PERMISSIONS
    # TODO: new_team_permission

    # TODO: get_team_permission

    def get_team_permissions(self, filter = None):
        return TeamPermission.get_all(TeamPermission, self.persistence, filter = filter)

    ## MILESTONE
    # TODO: new_milestone

    # TODO: get_milestone

    # TODO: get_milestones

    ## TAG
    # TODO: new_tag

    # TODO: get_tag

    def get_tags(self, filter = None):
        return Tag.get_all(Tag, self.persistence, filter = filter)

    ## TAG ASSIGNMENT
    # TODO: new_tag_assignment

    # TODO: get_tag_assignment

    def get_tag_assignments(self, filter = None):
        return TagAssignment.get_all(TagAssignment, self.persistence, filter = filter)

    ## USER
    # TODO: new_user

    def get_user(self, id = None):
        return User.get(User, id, self.persistence)

    # TODO: get_users