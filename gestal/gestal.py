# Main / Top level executable TODO

import gi
gi.require_version('Gdk', '3.0')
from gui.application import Application


app = Application('org.gnome.gestal')
app.run()