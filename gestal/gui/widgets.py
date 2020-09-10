from core import config as cfg
from gi.repository import Gtk
from .strings import get_string

# Change this for a scrollable one TODO
class OrganizerBox(Gtk.ScrolledWindow):
    main_box = None
    backend = None

    def __init__(self, backend):
        super(OrganizerBox, self).__init__(hexpand = True, vexpand = True)
        self.backend = backend

        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.set_size_request(cfg.ORGANIZER_BOX_MIN_WIDTH, cfg.ORGANIZER_BOX_MIN_HEIGHT)

        self.main_box = Gtk.Box(spacing = 5, orientation = Gtk.Orientation.VERTICAL)
        self.add(self.main_box)

        # TODO: add new project button
        self.add_project_button = Gtk.Button(label="+")
        self.main_box.pack_start(self.add_project_button, False, False, 0)
        
        self.project_view = Gtk.TreeView()
        cell_renderer = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn(None, cell_renderer, text=0)
        self.project_view.append_column(col)
        self.set_projects()
        self.main_box.pack_start(self.project_view, True, True, 0)

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

class SettingsBox(Gtk.Box):
    backend = None

    def __init__(self, backend):
        super(SettingsBox, self).__init__(spacing = 5, orientation = Gtk.Orientation.HORIZONTAL)
        self.backend = backend

        self.set_size_request(cfg.SETTINGS_BOX_MIN_WIDTH, cfg.SETTINGS_BOX_MIN_HEIGHT)

        for _ in range(5):
            b = Gtk.Button(label="SettingsBox")
            self.pack_end(b, True, True, 0)

        # The TreeView section holds the projects as a top level (default project has no label (?))

class DetailBox(Gtk.ScrolledWindow):
    main_box = None
    backend = None

    def __init__(self, backend):
        super(DetailBox, self).__init__(hexpand = True, vexpand = True)
        self.backend = backend

        # Basic setup (size and orientation)
        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.set_size_request(cfg.DETAIL_BOX_MIN_WIDTH, cfg.DETAIL_BOX_MIN_HEIGHT)
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
        self.set_size_request(cfg.TASK_BOX_MIN_WIDTH, cfg.TASK_BOX_MIN_HEIGHT)

        self.main_box = Gtk.Box(spacing = 5, orientation = Gtk.Orientation.VERTICAL)
        self.add(self.main_box)

        for _ in range(50):
            b = Gtk.Button(label="TaskBox")
            self.main_box.pack_end(b, True, True, 0)

class TaskBoxSearchBar(Gtk.Box):
    search_entry = None
    backend = None

    def __init__(self, backend):
        super(TaskBoxSearchBar, self).__init__()
        self.backend = backend

        self.set_size_request(cfg.TASK_BOX_SEARCH_BAR_MIN_WIDTH, cfg.TASK_BOX_SEARCH_BAR_MIN_HEIGHT)

        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_size_request(int(float(cfg.WINDOW_WIDTH) * 0.5), 1)
        self.pack_start(self.search_entry, True, False, 0)

    # TODO: create the LoginWindow widgets