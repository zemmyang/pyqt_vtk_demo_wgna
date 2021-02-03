# zip file with all the files
FOLDER_DATASTORE = ""
DATASTORE = "data.zip"
DATASTORE_CONFIG = "data.json"
JSON_LENGTH_UNITS_IN_NM = True

DEBUG_MODE = False  # show features in-progress

####################################
###       INTERNAL CONFIG        ###
####################################

import sys
import logging as logg
from io import StringIO

#### names and such
# for main_window.py
MAIN_WINDOW_TITLE = "Waveguide+Nano-antenna Isosurface Viewer"
MAIN_WINDOW_SIZE = (800, 600)
DEFAULT_FOOTNOTE = "Full paper by Ang A.S., et al., here: https://doi.org/10.1364/OL.394557"

# for dialog_boxes.py
SETTINGS_2D_VIEW_TITLE = "2D View settings"
SETTINGS_2D_VIEW_SIZE = (200, 500)
SETTINGS_3D_VIEW_TITLE = "3D View settings"
SETTINGS_3D_VIEW_SIZE = (300, 300)

# logging stuff
logger = logg.getLogger('wgna_viewer')
logger.setLevel(logg.DEBUG)

formatter = \
    logg.Formatter('%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s')

file_handler = logg.FileHandler('log.txt')
file_handler.setLevel(logg.WARNING)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logg.StreamHandler(sys.stdout)
stream_handler.setLevel(logg.DEBUG)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

string_stream = StringIO()
logg.basicConfig(stream=string_stream, level=logg.DEBUG)
