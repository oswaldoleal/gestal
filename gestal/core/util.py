from os.path import abspath, dirname, join

def get_file_path(filename, folder = 'data'):
    gestal_path = abspath(dirname(__file__)).split('core')[0]
    return join(gestal_path, f'{folder}/{filename}')

def get_tinted_icon(filename, color = '#FFFFFF'):
    # TODO
    pass