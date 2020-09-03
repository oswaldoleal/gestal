from gi.repository import Gtk
from core import config as cfg

# Change this for a scrollable one TODO
class OrganizerBox(Gtk.ScrolledWindow):
    main_box = None

    def __init__(self):
        super(OrganizerBox, self).__init__(hexpand = True, vexpand = True)
        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.set_size_request(cfg.ORGANIZER_BOX_MIN_WIDTH, cfg.ORGANIZER_BOX_MIN_HEIGHT)

        self.main_box = Gtk.Box(spacing = 5, orientation = Gtk.Orientation.VERTICAL)
        self.add(self.main_box)

        for _ in range(5):
            b = Gtk.Button(label="OrganizerBox")
            self.main_box.pack_end(b, True, True, 0)

        # The TreeView section holds the projects as a top level (default project has no label (?))

class DetailBox(Gtk.ScrolledWindow):
    main_box = None

    def __init__(self):
        super(DetailBox, self).__init__(hexpand = True, vexpand = True)
        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.set_size_request(cfg.DETAIL_BOX_MIN_WIDTH, cfg.DETAIL_BOX_MIN_HEIGHT)

        self.main_box = Gtk.Box(spacing = 5, orientation = Gtk.Orientation.VERTICAL)
        self.add(self.main_box)

        for _ in range(30):
            b = Gtk.Button(label="DetailBox")
            self.main_box.pack_end(b, True, True, 0)

class TaskBox(Gtk.ScrolledWindow):
    main_box = None

    def __init__(self):
        super(TaskBox, self).__init__(hexpand = True, vexpand = True)
        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.set_size_request(cfg.TASK_BOX_MIN_WIDTH, cfg.TASK_BOX_MIN_HEIGHT)

        self.main_box = Gtk.Box(spacing = 5, orientation = Gtk.Orientation.VERTICAL)
        self.add(self.main_box)

        for _ in range(50):
            b = Gtk.Button(label="TaskBox")
            self.main_box.pack_end(b, True, True, 0)

class TaskBoxSearchBar(Gtk.Box):
    search_entry = None
    def __init__(self):
        super(TaskBoxSearchBar, self).__init__()
        self.set_size_request(cfg.TASK_BOX_SEARCH_BAR_MIN_WIDTH, cfg.TASK_BOX_SEARCH_BAR_MIN_HEIGHT)

        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_size_request(int(float(cfg.WINDOW_WIDTH) * 0.5), 1)
        self.pack_start(self.search_entry, True, False, 0)
