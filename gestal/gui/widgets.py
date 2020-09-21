from core import config as cfg
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

    def __init__(self, backend):
        super(OrganizerBox, self).__init__(hexpand = True, vexpand = True)
        self.backend = backend

        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.set_hexpand(False)

        self.main_box = Gtk.Box(spacing = 5, orientation = Gtk.Orientation.VERTICAL)
        self.add(self.main_box)

        self.add_project_button = Gtk.Button(label="+")
        self.add_project_button.connect('clicked', self.add_project_form)
        self.main_box.pack_start(self.add_project_button, False, False, 0)
        
        # TODO: each tree view should be its own widget
        self.project_view = Gtk.TreeView()
        cell_renderer = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn("Projects", cell_renderer, text=0)
        self.project_view.append_column(col)
        self.set_projects()
        self.main_box.pack_start(self.project_view, True, True, 0)

        # TODO: add the tags and team tree views

    def add_project_form(self, button):
        # TODO: This should be in the constructor to avoid redeclaration
        self.add_project_box = AddProjectForm(self.backend, previous_widget = self.add_project_button)
        replace_widget(self.add_project_button, self.add_project_box)

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
        
        self.project_view.set_model(model)

class AddProjectForm(Gtk.Box):
    backend = None
    previous_widget = None

    def __init__(self, backend, previous_widget = None):
        super(AddProjectForm, self).__init__(spacing = 5, orientation = Gtk.Orientation.VERTICAL)
        self.backend = backend
        if (previous_widget):
            self.previous_widget = previous_widget

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
        replace_widget(self, self.previous_widget)

    def save(self, button):
        self.backend.new_project(name = self.name_entry.get_text(), description = self.description_entry.get_text())
        # TODO: update the project tree view
        replace_widget(self, self.previous_widget)

class SettingsBox(Gtk.Box):
    backend = None

    def __init__(self, backend):
        super(SettingsBox, self).__init__(spacing = 5, orientation = Gtk.Orientation.HORIZONTAL)
        self.backend = backend

        self.set_vexpand(False)
        self.set_hexpand(False)

        for _ in range(1):
            b = Gtk.Button(label="SettingsBox")
            self.pack_end(b, False, False, 0)

        # The TreeView section holds the projects as a top level (default project has no label (?))

class TaskBox(Gtk.ScrolledWindow):
    main_box = None
    backend = None

    def __init__(self, backend):
        super(TaskBox, self).__init__(hexpand = True, vexpand = True)
        self.backend = backend

        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.main_box = Gtk.Box(spacing = 5, orientation = Gtk.Orientation.VERTICAL)
        self.add(self.main_box)
        
        # TODO: missing add task button

        # TODO: filter for the current project
        tasks = backend.get_tasks()
        for task in tasks:
            task_display = TaskDisplay(task)
            self.main_box.pack_start(task_display, False, True, 0)

class TaskBoxSearchBar(Gtk.Box):
    search_entry = None
    backend = None

    def __init__(self, backend):
        super(TaskBoxSearchBar, self).__init__()
        self.backend = backend

        self.set_vexpand(False)

        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_size_request(int(float(cfg.WINDOW_WIDTH) * 0.5), 1)
        self.pack_start(self.search_entry, True, False, 0)

    # TODO: create the LoginWindow widgets

class TaskDisplay(Gtk.Box):
    task = None

    def __init__(self, task):
        super(TaskDisplay, self).__init__(spacing = 5, orientation = Gtk.Orientation.VERTICAL)
        self.task = task

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