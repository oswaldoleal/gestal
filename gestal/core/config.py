# holds all the config variables necesary for the app to run TODO

LANGUAGE = 'en_US'

# TODO: UI dimensions, debug level

# 1.5:1 aspect ratio (in grid of 200 columns x 130 rows)
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 640

ORGANIZER_BOX_MIN_WIDTH = 288
ORGANIZER_BOX_MIN_HEIGHT = WINDOW_HEIGHT

TASK_BOX_SEARCH_BAR_MIN_WIDTH = 480
TASK_BOX_SEARCH_BAR_MIN_HEIGHT = 32

TASK_BOX_MIN_WIDTH = TASK_BOX_SEARCH_BAR_MIN_WIDTH
TASK_BOX_MIN_HEIGHT = WINDOW_HEIGHT - TASK_BOX_SEARCH_BAR_MIN_HEIGHT

DETAIL_BOX_MIN_WIDTH = 192
DETAIL_BOX_MIN_HEIGHT = WINDOW_HEIGHT

# Config directory / DB directory TODO: determine where is the best place to save the data
DB_PATH = ''