import sys
import vtk
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt import *

from dialog_boxes import *
from model3d import Tab3DView
from xsections import XSectionsView
import config as CFG


class MainWindow(QMainWindow):
    """
    view for the main window
    completion: mostly done
    """
    def __init__(self):
        super().__init__()
        self.title = CFG.MAIN_WINDOW_TITLE
        self.left = 0
        self.top = 0
        self.width = CFG.MAIN_WINDOW_SIZE[0]
        self.height = CFG.MAIN_WINDOW_SIZE[1]
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # tabs
        self.tab_widget = TabWidget(self)
        self.setCentralWidget(self.tab_widget)

        # default footnote status bar
        self.statusBar = QStatusBar()
        self.default_footnote = QLabel(CFG.DEFAULT_FOOTNOTE)
        self.statusBar.addWidget(self.default_footnote)
        self.setStatusBar(self.statusBar)
        CFG.logger.debug("Main Window view done.")


class TabWidget(QWidget):
    """
    view for the tab widget
    completion: mostly done
    """
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()

        # Add tabs
        # self.tabs.addTab(ViewExperimentalVTKTab(self), "FOR TESTING")
        self.tabs.addTab(Tab3DView(self), "3D View")
        self.tabs.addTab(XSectionsView(self), "2D cross-sections")
        self.tabs.addTab(LoggerView(self), "Log")
        self.tabs.setStatusTip("Select between 2D and 3D view.")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        CFG.logger.debug("Tab Widget view done.")


class LoggerView(QTabWidget):
    def __init__(self, parent):
        super(QTabWidget, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.textbox = QTextEdit()
        self.setLayout(self.layout)
        self.layout.addWidget(self.textbox)

        self.textbox.insertPlainText(CFG.string_stream.getvalue())
        self.textbox.setReadOnly(True)


########################################################################################################################
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtk.util import numpy_support
from scipy.io import loadmat

class ViewExperimentalVTKTab(QTabWidget):
    """
    for debugging VTK stuff
    TODO: REMOVE THIS
    """
    def __init__(self, parent):
        super(QTabWidget, self).__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)

        test_gb = QGroupBox("test groupbox")
        layout.addWidget(test_gb)

        hbox = QHBoxLayout()
        test_gb.setLayout(hbox)

        button_test = QRadioButton("test button")
        hbox.addWidget(button_test)
        button_test.toggled.connect(self.button_test)

        button_test2 = QRadioButton("test button2")
        hbox.addWidget(button_test2)
        button_test2.toggled.connect(self.button_test2)

        self.frame = QFrame()
        self.vl = QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        # Create wg_source
        wg_source = vtk.vtkCubeSource()
        wg_source.SetCenter(0, 0, -0.534*100/2)

        wg_source.SetXLength(4.000*100)
        wg_source.SetYLength(1.560*100)
        wg_source.SetZLength(0.534*100)
        wg_source.Update()

        # Create a mapper
        wg_mapper = vtk.vtkPolyDataMapper()
        wg_mapper.SetInputConnection(wg_source.GetOutputPort())

        wg_actor = vtk.vtkActor()
        wg_actor.SetMapper(wg_mapper)

        self.colors = vtk.vtkNamedColors()

        self.ren = vtk.vtkRenderer()
        self.ren.SetBackground(0, 0, 0)
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        frommat = loadmat("toroid_isosurf_data.mat")
        export = frommat["export"].T # transpose the data
        gs_export = frommat["gs_export"]

        vtk_data_array = numpy_support.numpy_to_vtk(num_array=export.ravel(), deep=True, array_type=vtk.VTK_FLOAT)

        img_vtk = vtk.vtkStructuredPoints()
        img_vtk.SetOrigin(0, 0, 0)
        img_vtk.SetDimensions(export.shape[::-1])
        img_vtk.GetPointData().SetScalars(vtk_data_array)

        contours = vtk.vtkContourFilter()
        contours.SetInputData(img_vtk)
        contours.SetValue(0, gs_export)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(contours.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        _axes_actor = vtk.vtkAxesActor()
        # self.ren.AddActor(_axes_actor)
        self.ren.AddActor(actor)
        self.ren.AddActor(wg_actor)

        # set camera
        camera = vtk.vtkCamera()
        camera.SetViewUp(1, 1, 1)
        camera.SetPosition(500, 500, 200)
        camera.SetFocalPoint(0, 0, 0)

        self.ren.SetActiveCamera(camera)

        self.frame.setLayout(self.vl)
        layout.addWidget(self.frame)

        self.show()
        self.iren.Initialize()
        self.iren.Start()

    def button_test(self, enabled):
        if enabled:
            iso_stlreader = vtk.vtkSTLReader()
            iso_stlreader.SetFileName("stl/iso/toroid.stl")

            iso_mapper = vtk.vtkPolyDataMapper()
            iso_mapper.SetInputConnection(iso_stlreader.GetOutputPort())

            self.iso_actor = vtk.vtkActor()
            self.iso_actor.SetMapper(iso_mapper)
            self.iso_actor.GetProperty().SetDiffuseColor(self.colors.GetColor3d('Blue'))

            iso_transform = vtk.vtkTransform()
            iso_transform.RotateZ(90)
            iso_transform.Translate(0, 0, 0.35)
            self.iso_actor.SetUserTransform(iso_transform)

            self.ren.AddActor(self.iso_actor)

            self.iren.ReInitialize()

    def button_test2(self, enabled):
        if enabled:
            self.ren.RemoveActor(self.iso_actor)

            self.iren.ReInitialize()