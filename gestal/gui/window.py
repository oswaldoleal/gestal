from core import config as cfg
from gi.repository import Gdk, Gtk
from os.path import abspath, dirname, join
from .strings import get_string
from .widgets import DetailBox, OrganizerBox, SettingsBox, TaskBox, TaskBoxSearchBar

class MainWindow(Gtk.ApplicationWindow):
    # Left container that holds the project trees
    organizer_box = None
    # Lower left container that holds the project trees
    settings_box = None
    # Right container that displays the details of an Task / Project / Team
    detail_box = None
    # Middle container that displays the task list or other items in list form
    task_box = None
    # Bar on top of the Task Box that holds the search bar and some other buttons
    task_box_search_bar = None
    # This will hold all the child widgets
    view = None
    # Backend reference
    backend = None

    def __init__(self, app, backend):
        super(MainWindow, self).__init__(application = app)

        # TODO: add the app icon to the window
        # self.set_icon_from_file("icon.png")

        self.backend = backend

        self.set_title(get_string("window_title"))
        self.set_default_size(cfg.WINDOW_WIDTH, cfg.WINDOW_HEIGHT)
        self.set_size_request(cfg.WINDOW_WIDTH, cfg.WINDOW_HEIGHT)

        self.view = Gtk.Grid()
        self.add(self.view)

        # TODO: change this for next_to notation
        self.organizer_box = OrganizerBox(self.backend)
        self.view.attach(self.organizer_box, 0, 0, 60, 120)

        self.settings_box = SettingsBox(self.backend)
        self.view.attach_next_to(self.settings_box,self.organizer_box, Gtk.PositionType.BOTTOM, 60, 10)

        self.task_box_search_bar = TaskBoxSearchBar(self.backend)
        # self.view.attach(self.task_box_search_bar, 60, 0, 100, 1)
        self.view.attach_next_to(self.task_box_search_bar,self.organizer_box, Gtk.PositionType.RIGHT, 100, 1)

        self.task_box = TaskBox(self.backend)
        # self.view.attach(self.task_box, 60, 1, 100, 129)
        self.view.attach_next_to(self.task_box,self.task_box_search_bar, Gtk.PositionType.BOTTOM, 100, 129)

        self.detail_box = DetailBox(self.backend)
        # self.view.attach(self.detail_box, 160, 0, 40, 130)
        self.view.attach_next_to(self.detail_box,self.task_box_search_bar, Gtk.PositionType.RIGHT, 40, 130)

        # self.connect("destroy", Gtk.main_quit)
        self.set_style()

    # TODO: create the LoginWindow class

    def set_style(self):
        css_path = abspath(dirname(__file__))

        provider = Gtk.CssProvider()
        provider.load_from_path(join(css_path, "css/style.css"))
        screen = Gdk.Display.get_default_screen(Gdk.Display.get_default())
        # I was unable to found instrospected version of this
        GTK_STYLE_PROVIDER_PRIORITY_APPLICATION = 600
        Gtk.StyleContext.add_provider_for_screen(
            screen, provider,
            GTK_STYLE_PROVIDER_PRIORITY_APPLICATION
        )