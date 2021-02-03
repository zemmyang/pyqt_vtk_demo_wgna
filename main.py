from main_window import *
from config import logger

import sys
import vtk
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt import *

import zipfile
import json
import h5py
import scipy.constants as const
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtk.util import numpy_support


def main():
    logger.info("Program started")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    logger.info("Program loaded")
    sys.exit(app.exec_())

# a.     Selection of specific nanoantenna geometry

# b.     Visualization of the 3D optical potential field for a given nanoantenna geometry

# c.     Allow interactive measurements of the 3D optical potential at different 3D points selected by the user mouse.


if __name__ == "__main__":
    main()
