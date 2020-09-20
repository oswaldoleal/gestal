from core import config as cfg
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

class DetailBox(Gtk.ScrolledWindow):
    main_box = None
    backend = None

    def __init__(self, backend):
        super(DetailBox, self).__init__(hexpand = True, vexpand = True)
        self.backend = backend

        # Basic setup (size and orientation)
        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.main_box = Gtk.Box(spacing = 5, orientation = Gtk.Orientation.VERTICAL)
        self.add(self.main_box)

        # Task Name section
        self.task_name_label = Gtk.Label(get_string('task_name_label'))
        self.main_box.pack_start(self.task_name_label, False, False, 0)

        self.task_name_entry = Gtk.Entry()
        self.task_name_entry.set_placeholder_text(get_string('task_name_label'))
        self.main_box.pack_start(self.task_name_entry, False, False, 0)

        # Task Description section
        self.task_description_label = Gtk.Label(get_string('task_description_label'))
        self.main_box.pack_start(self.task_description_label, False, False, 0)

        self.task_description_entry = Gtk.Entry()
        self.task_description_entry.set_placeholder_text(get_string('task_description_label'))
        self.main_box.pack_start(self.task_description_entry, False, False, 0)

        # TODO: this should be inferred from the current project selection (?) 
        # Task Project section
        self.task_project_label = Gtk.Label(get_string('task_project_label'))
        self.main_box.pack_start(self.task_project_label, False, False, 0)

        self.task_project_combobox = Gtk.ComboBox()
        renderer_text = Gtk.CellRendererText()
        self.task_project_combobox.pack_start(renderer_text, True)
        self.task_project_combobox.add_attribute(renderer_text, "text", 0)
        self.task_project_combobox.set_model(self.get_projects())
        self.main_box.pack_start(self.task_project_combobox, False, False, 0)

        # TODO: turn this calendar widget into a popover for a label
        # Task Due Date section
        self.task_due_date_label = Gtk.Label(get_string('task_due_date_label'))
        self.main_box.pack_start(self.task_due_date_label, False, False, 0)

        self.task_due_date_calendar = Gtk.Calendar()
        self.main_box.pack_start(self.task_due_date_calendar, False, False, 0)

        # Task Tag section TODO
        self.task_tags_label = Gtk.Label(get_string('task_tags_label'))
        self.main_box.pack_start(self.task_tags_label, False, False, 0)

        self.task_tags_entry = Gtk.Entry()
        self.task_tags_entry.set_placeholder_text(get_string('task_tags_ph'))
        self.main_box.pack_start(self.task_tags_entry, False, False, 0)

        # Task Color section TODO: this should be an entry widget with a popover color selector (hex? or premade)

        # Save task section
        self.task_save_button = Gtk.Button(label = get_string('task_save'))
        self.main_box.pack_start(self.task_save_button, False, False, 0)

    def get_projects(self):
        # TODO: get the projects from the backend
        project_store = Gtk.ListStore(str)
        projects = [
            "None",
            "UCAB",
            "Gestal",
        ]
        for project in projects:
            project_store.append([project])

        return project_store

class TaskBox(Gtk.ScrolledWindow):
    main_box = None
    backend = None

    def __init__(self, backend):
        super(TaskBox, self).__init__(hexpand = True, vexpand = True)
        self.backend = backend

        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.main_box = Gtk.Box(spacing = 5, orientation = Gtk.Orientation.VERTICAL)
        self.add(self.main_box)

        task_display = TaskDisplay(self.backend)
        self.main_box.pack_end(task_display, True, True, 0)

        for _ in range(50):
            b = Gtk.Button(label="TaskBox")
            self.main_box.pack_end(b, True, True, 0)

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
    backend = None

    def __init__(self, backend):
        super(TaskDisplay, self).__init__(spacing = 1, orientation = Gtk.Orientation.VERTICAL)
        self.backend = backend

        self.first_row = Gtk.Box(spacing = 5, orientation = Gtk.Orientation.HORIZONTAL)
        self.date_label = Gtk.Label('88/88/8888')
        self.name_label = Gtk.Label('Test task name')
        self.first_row.pack_start(self.date_label, False, False, 0)
        self.first_row.pack_start(self.name_label, True, True, 0)

        self.pack_start(self.first_row, True, True, 0)