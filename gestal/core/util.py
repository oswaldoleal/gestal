from gi.repository import GdkPixbuf
from os.path import abspath, dirname, join

def get_file_path(filename, folder = 'data'):
    gestal_path = abspath(dirname(__file__)).split('core')[0]
    return join(gestal_path, f'{folder}/{filename}')

def get_tinted_icon(filename, color = '#FFFFFF'):
    # TODO
    pass

def get_icon(filename):
    return GdkPixbuf.Pixbuf.new_from_file_at_scale(get_file_path(filename), -1, 18, True)