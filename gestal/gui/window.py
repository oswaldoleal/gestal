from gi.repository import Gtk
import core.config as cfg
from .strings import get_string
from .widgets import OrganizerBox, TaskBox, TaskBoxSearchBar, DetailBox

class MainWindow(Gtk.ApplicationWindow):
    # Left container that holds the project trees
    organizer_box = None
    # Right container that displays the details of an Task / Project / Team
    detail_box = None
    # Middle container that displays the task list or other items in list form
    task_box = None
    # Bar on top of the Task Box that holds the search bar and some other buttons
    task_box_search_bar = None
    # This will hold all the child widgets
    view = None

    def __init__(self, app):
        super(MainWindow, self).__init__(application = app)

        # TODO: add the app icon to the window
        # self.set_icon_from_file("icon.png")

        self.set_title(get_string("window_title"))
        self.set_default_size(cfg.WINDOW_WIDTH, cfg.WINDOW_HEIGHT)
        self.set_size_request(cfg.WINDOW_WIDTH, cfg.WINDOW_HEIGHT)

        self.view = Gtk.Grid()
        self.add(self.view)

        # TODO: change this for next_to notation
        self.organizer_box = OrganizerBox()
        self.view.attach(self.organizer_box, 0, 0, 60, 130)

        self.task_box_search_bar = TaskBoxSearchBar()
        # self.view.attach(self.task_box_search_bar, 60, 0, 100, 1)
        self.view.attach_next_to(self.task_box_search_bar,self.organizer_box, Gtk.PositionType.RIGHT, 100, 1)

        self.task_box = TaskBox()
        # self.view.attach(self.task_box, 60, 1, 100, 129)
        self.view.attach_next_to(self.task_box,self.task_box_search_bar, Gtk.PositionType.BOTTOM, 100, 129)

        self.detail_box = DetailBox()
        # self.view.attach(self.detail_box, 160, 0, 40, 130)
        self.view.attach_next_to(self.detail_box,self.task_box_search_bar, Gtk.PositionType.RIGHT, 40, 130)

        # self.connect("destroy", Gtk.main_quit)
