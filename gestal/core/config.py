# holds all the config variables necesary for the app to run TODO
from locale import getdefaultlocale

LANGUAGE = getdefaultlocale()[0].split('_')[0]

# TODO: UI dimensions, debug level

# 1.5:1 aspect ratio (in grid of 200 columns x 130 rows)
# ratio
WIDTH_RATIO = 1.61803398875
HEIGHT_RATIO = 1.0

WINDOW_WIDTH = 960
WINDOW_HEIGHT = int(round(float(WINDOW_WIDTH) / WIDTH_RATIO))

LEFT_PANE_WIDTH = int(round(float(WINDOW_HEIGHT) / WIDTH_RATIO))
LEFT_PANE_HEIGHT = WINDOW_HEIGHT

# Config directory / DB directory TODO: determine where is the best place to save the data
DB_PATH = ''