from core import config as cfg
from core.log import Log
from datetime import datetime
from gi.repository import Gtk
from .strings import get_string

def replace_widget(current, new):
    container = current.get_parent()
    assert container

    props = {}
    for pspec in container.list_child_properties():
        props[pspec.name] = container.child_get_property(current, pspec.name)

    container.remove(current)
    container.add(new)

    for name, value in props.items():
        container.child_set_property(new, name, value)

# Change this for a scrollable one TODO
class OrganizerBox(Gtk.ScrolledWindow):
    main_box = None
    backend = None
    # Main window reference to trigger other widgets backend update
    window = None

    def __init__(self, backend, window = None):
        super(OrganizerBox, self).__init__(hexpand = True, vexpand = True)
        self.backend = backend
        if (window):
            self.window = window

        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.set_hexpand(False)

        self.main_box = Gtk.Box(spacing = 5, orientation = Gtk.Orientation.VERTICAL)
        self.add(self.main_box)

        self.add_project_button = Gtk.Button(label="+")
        self.add_project_button.connect('clicked', self.add_project_form)
        self.main_box.pack_start(self.add_project_button, False, False, 0)
        
        # TODO: each tree view should be its own widget
        self.project_view = ProjectTree(self.backend)
        self.main_box.pack_start(self.project_view, True, True, 0)
        self.tags_view = TagTree(self.backend)
        self.main_box.pack_start(self.tags_view, True, True, 0)
        self.team_view = TeamTree(self.backend)
        self.main_box.pack_start(self.team_view, True, True, 0)

        # TODO: add the tags and team tree views

    def add_project_form(self, button):
        # TODO: This should be in the constructor to avoid redeclaration
        self.add_project_box = AddProjectForm(self.backend, previous_widget = self.add_project_button, window = self.window)
        replace_widget(self.add_project_button, self.add_project_box)

class ProjectTree(Gtk.TreeView):
    backend = None
    
    def __init__(self, backend):
        super(ProjectTree, self).__init__()
        self.backend = backend

        cell_renderer = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn("Projects", cell_renderer, text=0)
        self.append_column(col)
        self.set_projects()

    def set_projects(self):
        projects = self.backend.get_projects()

        model = Gtk.TreeStore(str)
        for project in projects:
            piter = model.append(None, (project.name,))

            # TODO: turn this into a recursive function
            for task in self.backend.get_tasks(filter = {'project_id': project.id}):
                titer = model.append(piter, (task.name,))

                for child_task in self.backend.get_tasks(filter = {'parent_id': task.id}):
                    model.append(titer, (child_task.name,))
        
        self.set_model(model)

class TagTree(Gtk.TreeView):
    backend = None
    
    def __init__(self, backend):
        super(TagTree, self).__init__()
        self.backend = backend

        cell_renderer = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn("Tags", cell_renderer, text=0)
        self.append_column(col)
        self.set_tags()

    def set_tags(self):
        tags = self.backend.get_tags()

        model = Gtk.TreeStore(str)
        for tag in tags:
            piter = model.append(None, (tag.name,))

            # TODO: turn this into a recursive function
            for assignment in self.backend.get_tag_assignments(filter = {'tag_id': tag.id}):
                task = self.backend.get_task(id = assignment.task_id)
                model.append(piter, (task.name,))
        
        self.set_model(model)

class TeamTree(Gtk.TreeView):
    backend = None
    
    def __init__(self, backend):
        super(TeamTree, self).__init__()
        self.backend = backend

        cell_renderer = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn("Teams", cell_renderer, text=0)
        self.append_column(col)
        self.set_teams()

    def set_teams(self):
        teams = self.backend.get_teams()

        model = Gtk.TreeStore(str)
        for team in teams:
            piter = model.append(None, (team.name,))

            # TODO: turn this into a recursive function
            for team_permission in self.backend.get_team_permissions(filter = {'team_id': team.id}):
                user = self.backend.get_user(id = team_permission.user_id)
                model.append(piter, (user.username,))
        
        self.set_model(model)

class AddProjectForm(Gtk.Box):
    backend = None
    previous_widget = None
    # Main window reference to trigger other widgets backend update
    window = None

    def __init__(self, backend, previous_widget = None, window = None):
        super(AddProjectForm, self).__init__(spacing = 5, orientation = Gtk.Orientation.VERTICAL)
        self.backend = backend
        if (previous_widget):
            self.previous_widget = previous_widget
        if (window):
            self.window = window

        name_label = Gtk.Label()
        name_label = Gtk.Label('Project Name')
        self.pack_start(name_label, False, False, 0)

        self.name_entry = Gtk.Entry()
        self.name_entry.set_placeholder_text('Project Name')
        self.pack_start(self.name_entry, False, False, 0)

        description_label = Gtk.Label()
        description_label = Gtk.Label('Project Description')
        self.pack_start(description_label, False, False, 0)

        self.description_entry = Gtk.Entry()
        self.description_entry.set_placeholder_text('Project Description')
        self.pack_start(self.description_entry, False, False, 0)

        button_holder = Gtk.Box(spacing = 5, orientation = Gtk.Orientation.HORIZONTAL)
        self.cancel_button = Gtk.Button(label = get_string('cancel'))
        self.cancel_button.connect('clicked', self.cancel)
        self.save_button = Gtk.Button(label = get_string('save'))
        self.save_button.connect('clicked', self.save)
        button_holder.pack_start(self.cancel_button, True, True, 0)
        button_holder.pack_start(self.save_button, True, True, 0)
        self.pack_start(button_holder, True, True, 0)

        self.show_all()

    def cancel(self, button):
        Log.info('Clicked cancel button', origin = 'AddProjectForm')
        replace_widget(self, self.previous_widget)

    def save(self, button):
        Log.info('Clicked save button', origin = 'AddProjectForm')
        self.backend.new_project(name = self.name_entry.get_text(), description = self.description_entry.get_text())
        # TODO: update the project tree view
        replace_widget(self, self.previous_widget)
        self.window.update_from_backend()

class SettingsBox(Gtk.Box):
    backend = None
    # Main window reference to trigger other widgets backend update
    window = None

    def __init__(self, backend, window = None):
        super(SettingsBox, self).__init__(spacing = 5, orientation = Gtk.Orientation.HORIZONTAL)
        self.backend = backend
        if (window):
            self.window = window

        self.set_vexpand(False)
        self.set_hexpand(False)

        for _ in range(1):
            b = Gtk.Button(label="SettingsBox")
            self.pack_end(b, False, False, 0)

        # The TreeView section holds the projects as a top level (default project has no label (?))

class TaskBox(Gtk.ScrolledWindow):
    main_box = None
    backend = None
    # Main window reference to trigger other widgets backend update
    window = None

    def __init__(self, backend, window = None):
        super(TaskBox, self).__init__(hexpand = True, vexpand = True)
        self.backend = backend
        if (window):
            self.window = window

        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.main_box = Gtk.Box(spacing = 5, orientation = Gtk.Orientation.VERTICAL)
        self.add(self.main_box)
        
        # TODO: missing add task button
        self.add_task_button = Gtk.Button(label="+")
        self.add_task_button.connect('clicked', self.add_task_form)
        self.main_box.pack_start(self.add_task_button, False, False, 0)

        # TODO: filter for the current project
        tasks = backend.get_tasks()
        for task in tasks:
            task_display = TaskDisplay(task, window = self.window)
            self.main_box.pack_start(task_display, False, True, 0)

    def add_task_form(self, button):
        # TODO: This should be in the constructor to avoid redeclaration
        self.add_task_box = AddTaskForm(self.backend, previous_widget = self.add_task_button, window = self.window)
        replace_widget(self.add_task_button, self.add_task_box)

class AddTaskForm(Gtk.Box):
    backend = None
    previous_widget = None
    # Main window reference to trigger other widgets backend update
    window = None

    def __init__(self, backend, previous_widget = None, window = None):
        super(AddTaskForm, self).__init__(spacing = 5, orientation = Gtk.Orientation.VERTICAL)
        self.backend = backend
        if (previous_widget):
            self.previous_widget = previous_widget
        if (window):
            self.window = window

        name_label = Gtk.Label()
        name_label = Gtk.Label('Task Name')
        self.pack_start(name_label, False, False, 0)

        self.name_entry = Gtk.Entry()
        self.name_entry.set_placeholder_text('Task Name')
        self.pack_start(self.name_entry, False, False, 0)

        description_label = Gtk.Label()
        description_label = Gtk.Label('Task Description')
        self.pack_start(description_label, False, False, 0)

        self.description_entry = Gtk.Entry()
        self.description_entry.set_placeholder_text('Task Description')
        self.pack_start(self.description_entry, False, False, 0)

        # TODO: add calendar popover (due_date)

        tags_label = Gtk.Label()
        tags_label = Gtk.Label('Task Tags')
        self.pack_start(tags_label, False, False, 0)

        self.tags_entry = Gtk.Entry()
        self.tags_entry.set_placeholder_text('Task Tags')
        self.pack_start(self.tags_entry, False, False, 0)

        button_holder = Gtk.Box(spacing = 5, orientation = Gtk.Orientation.HORIZONTAL)
        self.cancel_button = Gtk.Button(label = get_string('cancel'))
        self.cancel_button.connect('clicked', self.cancel)
        self.save_button = Gtk.Button(label = get_string('save'))
        self.save_button.connect('clicked', self.save)
        button_holder.pack_start(self.cancel_button, True, True, 0)
        button_holder.pack_start(self.save_button, True, True, 0)
        self.pack_start(button_holder, True, True, 0)

        self.show_all()

    def cancel(self, button):
        Log.info('Clicked cancel button', origin = 'AddTaskForm')
        replace_widget(self, self.previous_widget)

    def save(self, button):
        Log.info('Clicked save button', origin = 'AddTaskForm')
        self.backend.new_task(name = self.name_entry.get_text(), description = self.description_entry.get_text(), tags = self.tags_entry.get_text())
        # TODO: update the project tree view
        replace_widget(self, self.previous_widget)
        self.window.update_from_backend()

class TaskBoxSearchBar(Gtk.Box):
    search_entry = None
    backend = None
    # Main window reference to trigger other widgets backend update
    window = None

    def __init__(self, backend, window = None):
        super(TaskBoxSearchBar, self).__init__()
        self.backend = backend
        if (window):
            self.window = window

        self.set_vexpand(False)

        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_size_request(int(float(cfg.WINDOW_WIDTH) * 0.5), 1)
        self.pack_start(self.search_entry, True, False, 0)

    # TODO: create the LoginWindow widgets

class TaskDisplay(Gtk.Box):
    task = None
    # Main window reference to trigger other widgets backend update
    window = None

    def __init__(self, task, window = None):
        super(TaskDisplay, self).__init__(spacing = 5, orientation = Gtk.Orientation.VERTICAL)
        self.task = task
        if (window):
            self.window = window

        self.first_row = Gtk.Box(spacing = 5, orientation = Gtk.Orientation.HORIZONTAL)
        date = datetime.strptime(task.creation_date, "%Y-%m-%dT%H:%M:%S.%f")
        self.date_label = Gtk.Label(str(date.date()))
        self.name_label = Gtk.Label(task.name)
        self.first_row.pack_start(self.date_label, False, False, 0)
        self.first_row.pack_start(self.name_label, True, True, 0)

        self.description_label = Gtk.Label(task.description)
        self.description_label.set_line_wrap(True)
        self.tag_label = Gtk.Label('#urgent #PO' * 4)
        self.tag_label.set_line_wrap(True)

        self.pack_start(self.first_row, True, True, 0)
        self.pack_start(self.description_label, True, True, 0)
        self.pack_start(self.tag_label, True, True, 0)

        # TODO: link to parent task

    def calendar_popover(self, widget):
        print('pop')