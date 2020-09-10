# holds all the config variables necesary for the app to run TODO
from locale import getdefaultlocale

LANGUAGE = getdefaultlocale()[0].split('_')[0]

# TODO: UI dimensions, debug level

# 1.5:1 aspect ratio (in grid of 200 columns x 130 rows)
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 640

# TODO: add MAX dimension variables for the widgets
SETTINGS_BOX_MIN_WIDTH = 288
SETTINGS_BOX_MIN_HEIGHT = 32

ORGANIZER_BOX_MIN_WIDTH = SETTINGS_BOX_MIN_WIDTH
ORGANIZER_BOX_MIN_HEIGHT = WINDOW_HEIGHT - SETTINGS_BOX_MIN_HEIGHT

TASK_BOX_SEARCH_BAR_MIN_WIDTH = 480
TASK_BOX_SEARCH_BAR_MIN_HEIGHT = 32

TASK_BOX_MIN_WIDTH = TASK_BOX_SEARCH_BAR_MIN_WIDTH
TASK_BOX_MIN_HEIGHT = WINDOW_HEIGHT - TASK_BOX_SEARCH_BAR_MIN_HEIGHT

DETAIL_BOX_MIN_WIDTH = 192
DETAIL_BOX_MIN_HEIGHT = WINDOW_HEIGHT

# Config directory / DB directory TODO: determine where is the best place to save the data
DB_PATH = ''