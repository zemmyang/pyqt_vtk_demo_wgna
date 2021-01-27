# folder of the 3D files
FOLDER_3D_FILES = "stl"

# subfolder of the nano-antenna geometry
SUBFOLDER_NAGEOM = "na"

# subfolder of the isosurfaces
SUBFOLDER_ISOSURF = "iso"

# data for the files
DATA_STORE = "data.json"
FOLDER_DATASTORE = ""

####################################
###       INTERNAL CONFIG        ###
####################################

import logging as logg
import os
import sys
from io import StringIO

#### filenames
# putting filenames together from config
FULLDIR_NAGEOM = os.path.join(FOLDER_3D_FILES, SUBFOLDER_NAGEOM)
FULLDIR_ISOSURF = os.path.join(FOLDER_3D_FILES, SUBFOLDER_ISOSURF)
FULLDIR_DATASTORE = os.path.join(FOLDER_DATASTORE, DATA_STORE)

#### names and such
# for main_window.py
MAIN_WINDOW_TITLE = "change me"
MAIN_WINDOW_SIZE = (800, 600)
DEFAULT_FOOTNOTE = "wheeeeeeeeeee"

# for dialog_boxes.py
SETTINGS_2D_VIEW_TITLE = "2d settings title"
SETTINGS_2D_VIEW_SIZE = (200, 500)

# logging stuff
logger = logg.getLogger('wgna_viewer')
logger.setLevel(logg.DEBUG)

formatter = \
    logg.Formatter('%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s')

file_handler = logg.FileHandler('log.txt')
file_handler.setLevel(logg.WARNING)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# stream_handler = logg.StreamHandler(sys.stdout)
# stream_handler.setLevel(logg.WARNING)
# stream_handler.setFormatter(formatter)
# logger.addHandler(stream_handler)

string_stream = StringIO()
logg.basicConfig(stream=string_stream, level=logg.DEBUG)
