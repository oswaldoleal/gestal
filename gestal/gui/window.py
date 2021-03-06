from core import config as cfg
from gi.repository import Gdk, Gtk
from os.path import abspath, dirname, join
from .strings import get_string
from .widgets import OrganizerBox, SettingsBox, TaskBox, TaskBoxSearchBar

class MainWindow(Gtk.ApplicationWindow):
    # Main view containers
    main_view = None
    left_view = None
    right_view = None
    
    # Left view content
    organizer_box = None
    settings_box = None

    # Right view content
    task_box_search_bar = None
    task_box = None
    
    # Backend reference
    backend = None

    def __init__(self, app, backend):
        super(MainWindow, self).__init__(application = app)

        self.backend = backend

        # TODO: add the app icon to the window
        gestal_path = abspath(dirname(__file__)).split('gui')[0]
        self.set_icon_from_file(join(gestal_path, "data/icon.png"))
        self.set_title(get_string("window_title"))
        self.set_default_size(cfg.WINDOW_WIDTH, cfg.WINDOW_HEIGHT)
        self.set_size_request(cfg.WINDOW_WIDTH, cfg.WINDOW_HEIGHT)

        # Main View content holder
        self.main_view = Gtk.Box(spacing = 0, orientation = Gtk.Orientation.HORIZONTAL)
        self.add(self.main_view)
        # Left pane container box
        self.left_view = Gtk.Box(spacing = 5, orientation = Gtk.Orientation.VERTICAL)
        self.left_view.set_hexpand(False)
        self.left_view.set_size_request(cfg.LEFT_PANE_WIDTH, cfg.LEFT_PANE_HEIGHT)
        self.main_view.pack_start(self.left_view, False, False, 0)
        # Right pane main content box
        self.right_view = Gtk.Box(spacing = 5, orientation = Gtk.Orientation.VERTICAL)
        self.main_view.pack_start(self.right_view, True, True, 0)


        # Organizer Box (left pane)
        self.organizer_box = OrganizerBox(backend, window = self)
        self.left_view.pack_start(self.organizer_box, True, True, 0)
        # Settings Bar (left pane)
        self.settings_box = SettingsBox(backend, window = self)
        self.left_view.pack_start(self.settings_box, False, True, 0)

        # Search Bar (right pane)
        self.task_box_search_bar = TaskBoxSearchBar(backend, window = self)
        self.right_view.pack_start(self.task_box_search_bar, False, True, 0)
        # Task Box (right pane)
        self.task_box = TaskBox(backend, window = self)
        self.right_view.pack_start(self.task_box, True, True, 0)

    # TODO: create the LoginWindow class

    def set_style(self):
        gui_path = abspath(dirname(__file__))

        provider = Gtk.CssProvider()
        provider.load_from_path(join(gui_path, "css/style.css"))
        screen = Gdk.Display.get_default_screen(Gdk.Display.get_default())
        # I was unable to found instrospected version of this
        GTK_STYLE_PROVIDER_PRIORITY_APPLICATION = 600
        Gtk.StyleContext.add_provider_for_screen(
            screen, provider,
            GTK_STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def update_from_backend(self):
        # TODO: implement update functions on every widget and call the necesary ones from here
        # This is supposed to be a callback function for every creation / deletion action
        self.organizer_box.project_view.set_projects()
        self.organizer_box.tags_view.set_tags()