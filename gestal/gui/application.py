from backend.backend import Backend
from gi.repository import Gtk
from os.path import abspath, dirname, join
from .window import MainWindow

class Application(Gtk.Application):
    main_window = None
    backend = None

    def __init__(self, app_id):
        super(Application, self).__init__(application_id = app_id)
        self.backend = Backend()

        # TODO: check if there is an existing user, if not create one

    def do_activate(self):
        if (not self.main_window):
            self.main_window = MainWindow(self, self.backend)
        
        self.main_window.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)



if (__name__ == '__main__'):
    app = Application('org.gnome.gestal')
    app.run()