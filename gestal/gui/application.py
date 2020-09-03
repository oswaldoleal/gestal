from gi.repository import Gtk
from .window import MainWindow

class Application(Gtk.Application):
    main_window = None

    def __init__(self, app_id):
        super(Application, self).__init__(application_id = app_id)

    def do_activate(self):
        if (not self.main_window):
            self.main_window = MainWindow(self)
        
        self.main_window.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)



if (__name__ == '__main__'):
    app = Application('org.gnome.gestal')
    app.run()