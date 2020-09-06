from datetime import datetime
from .persistence import Persistence

class Base:
    id = None
    creation_date = None
    __persistence = None

    def __init__(self, persistence = None):
        self.creation_date = datetime.now().isoformat()
        if (persistence):
            self.__persistence = persistence

    def save(self):
        if (self.id):
            self.update()
        else:
            self.create()

    def create(self):
        return self.__persistence.insert(self)
   
    def update(self):
        return self.__persistence.update(self)

    def delete(self):
        return self.__persistence.delete(self)

    @staticmethod
    def get(type, id, persistence):
        return persistence.get(type, id)

    @staticmethod
    def get_all(type, persistence):
        return persistence.get_all(type)

class Task(Base):
    project_id = None
    owner_id = None
    parent_id = None
    status = None
    name = None
    description = None
    due_date = None

    def __init__(self, name = None, owner_id = None, parent_id = None, description = None, project_id = None, status = None, due_date = None, data = None, persistence = None):
        super(Task, self).__init__(persistence = persistence)
        if (data):
            for key in data.keys():
                setattr(self, key, data['key'])

            return

        if (name):
            self.name = name
        if (description):
            self.description = description
        if (owner_id):
            self.owner_id = owner_id
        if (project_id):
            self.project_id = project_id
        if (parent_id):
            self.parent_id = parent_id
        if (status):
            self.status = status
        if (due_date):
            self.due_date = due_date

class Project(Base):
    owner_id = None
    description = None

    def __init__(self, owner_id = None, description = None, data = None, persistence = None):
        super(Project, self).__init__(persistence = persistence)
        if (data):
            for key in data.keys():
                setattr(self, key, data['key'])

            return
            
        if (description):
            self.description = description
        if (owner_id):
            self.owner_id = owner_id

class Team(Base):
    owner_id = None
    name = None
    description = None

    def __init__(self, name = None, owner_id = None, description = None, data = None, persistence = None):
        super(Team, self).__init__(persistence = persistence)
        if (data):
            for key in data.keys():
                setattr(self, key, data['key'])

            return
            
        if (name):
            self.name = name
        if (description):
            self.description = description
        if (owner_id):
            self.owner_id = owner_id

class TeamPermission(Base):
    team_id = None
    user_id = None
    permissions = None # 0 (view), 1 (edit), 2 (owner)

    def __init__(self, team_id = None, user_id = None, permissions = None, data = None, persistence = None):
        super(TeamPermission, self).__init__(persistence = persistence)
        if (data):
            for key in data.keys():
                setattr(self, key, data['key'])

            return
            
        if (team_id):
            self.team_id = team_id
        if (user_id):
            self.user_id = user_id
        if (permissions):
            self.permissions = permissions

class User(Base):
    username = None
    password = None
    email = None
    first_name = None
    last_name = None

    def __init__(self, username = None, password = None, email = None, first_name = None, last_name = None, data = None, persistence = None):
        super(User, self).__init__(persistence = persistence)
        if (data):
            for key in data.keys():
                setattr(self, key, data['key'])

            return
            
        if (username):
            self.username = username
        if (password):
            self.password = password
        if (email):
            self.email = email
        if (first_name):
            self.first_name = first_name
        if (last_name):
            self.last_name = last_name