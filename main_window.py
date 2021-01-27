import sys
import vtk
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt import *
from dialog_boxes import *
import json
import config as CFG

from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class Tab3DModel(QAbstractTableModel):
    """
    usage: initialize with argument of the model name
    returns a dict with all the info of the model like the file location, etc.
    also handles the vtk stuff
    """
    def __init__(self):
        super().__init__()
        self.datafile_3d_dict = self.load()
        self._update_paths()
        self.header_labels = list(self.datafile_3d_dict[0].keys())

    def rowCount(self, parent=None):
        return len(self.datafile_3d_dict)

    def columnCount(self, parent=None):
        return len(self.datafile_3d_dict[0])

    def index(self, row: int, column: int, parent=None):
        return self.datafile_3d_dict[row][self.header_labels[column]]

    def named_index(self, row: int, column, parent=None):
        return self.datafile_3d_dict[row][column]

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.header_labels[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)

    def _update_paths(self):
        for i in range(self.rowCount()):
            self.datafile_3d_dict[i]["nageom_path"] = os.path.join(CFG.FULLDIR_NAGEOM,
                                                                   self.datafile_3d_dict[i]["filename"])
            self.datafile_3d_dict[i]["iso_path"] = os.path.join(CFG.FULLDIR_ISOSURF,
                                                                self.datafile_3d_dict[i]["filename"])

    @staticmethod
    def load():
        try:
            with open(CFG.FULLDIR_DATASTORE, 'r') as f:
                _full_datafile = json.load(f)
        except Exception as err:
            print(err)
            sys.exit(0)
        else:
            CFG.logger.info("Loaded file: " + str(CFG.FULLDIR_DATASTORE))
            return json.loads(json.dumps(_full_datafile["model3d"]))


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


class Tab3DView(QTabWidget):
    """
    view for the 3D tab
    completion: 70%
    TODO: make buttons show isosurfaces
    """
    def __init__(self, parent):
        super(QTabWidget, self).__init__(parent)
        self.layout = QVBoxLayout()
        self._tab_3d_model = Tab3DModel()

        self.setLayout(self.layout)

        self._nageomradio_groupbox = QGroupBox("Nano-antenna Geometry")
        self.layout.addWidget(self._nageomradio_groupbox)

        self._frame = QFrame()
        self._vl = QVBoxLayout()
        self._vtkWidget = QVTKRenderWindowInteractor(self._frame)
        self._vl.addWidget(self._vtkWidget)

        self._labels = [str(self._tab_3d_model.named_index(i, "display"))
                        for i in range(self._tab_3d_model.rowCount())]

        self._colors = vtk.vtkNamedColors()
        self._set_vtk()
        self._set_groupbox_buttons()


    def _set_groupbox_buttons(self):
        _grouphbox = QHBoxLayout()
        self._nageomradio_groupbox.setLayout(_grouphbox)

        for i in range(self._tab_3d_model.rowCount()):
            _display_text = self._tab_3d_model.named_index(i, "display")
            _iso_path = self._tab_3d_model.named_index(i, "iso_path")
            _na_path = self._tab_3d_model.named_index(i, "nageom_path")
            _button = QRadioButton(_display_text)
            _button.clicked.connect(lambda checked, a=_na_path: self.activate_button(a))

            # _button.stateChanged.connect(self.remove_previous_display)
            CFG.logg.debug("Connecting " + self._tab_3d_model.named_index(i, "display") + " button to actions.")
            _grouphbox.addWidget(_button)

        _test_labels = [QLabel(self._tab_3d_model.named_index(i, "iso_path"))
                        for i in range(self._tab_3d_model.rowCount())]

        self.placeholder = QLabel()
        self.layout.addWidget(self.placeholder)

    def _set_vtk(self):
        self._ren = vtk.vtkRenderer()
        self._vtkWidget.GetRenderWindow().AddRenderer(self._ren)
        self._iren = self._vtkWidget.GetRenderWindow().GetInteractor()

        self._ren.AddActor(self._set_axes_vtk())
        self._ren.AddActor(self._set_wg_vtk())
        self._ren.SetActiveCamera(self._set_camera_vtk())

        self._frame.setLayout(self._vl)
        self.layout.addWidget(self._frame)

        self.show()
        self._iren.Initialize()
        self._iren.Start()

        _dummy_actor = vtk.vtkActor()
        self._ren.AddActor(_dummy_actor)

    @staticmethod
    def _set_axes_vtk():
        _axes_transform = vtk.vtkTransform()
        _axes_transform.Translate(-0.5, -0.5, 0.0)

        _axes_actor = vtk.vtkAxesActor()
        _axes_actor.SetUserTransform(_axes_transform)
        return _axes_actor

    @staticmethod
    def _set_camera_vtk():
        _camera = vtk.vtkCamera()
        _camera.SetViewUp(1, 1, 1)
        _camera.SetPosition(5, 5, 2)
        _camera.SetFocalPoint(0, 0, 0)
        return _camera

    @staticmethod
    def _set_wg_vtk():
        # create a source
        _wg_source = vtk.vtkCubeSource()
        _wg_source.SetCenter(0, 0, -0.534 / 2)

        _wg_source.SetXLength(4.000)
        _wg_source.SetYLength(1.560)
        _wg_source.SetZLength(0.534)
        _wg_source.Update()

        # Create a mapper
        _wg_mapper = vtk.vtkPolyDataMapper()
        _wg_mapper.SetInputConnection(_wg_source.GetOutputPort())

        _wg_actor = vtk.vtkActor()
        _wg_actor.SetMapper(_wg_mapper)
        CFG.logg.debug("setting up waveguide in 3D View.")
        return _wg_actor

    def _set_iso_vtk(self, filename):
        _iso_stlreader = vtk.vtkSTLReader()
        _iso_stlreader.SetFileName(filename)

        _iso_mapper = vtk.vtkPolyDataMapper()
        _iso_mapper.SetInputConnection(_iso_stlreader.GetOutputPort())

        _iso_actor = vtk.vtkActor()
        _iso_actor.SetMapper(_iso_mapper)
        _iso_actor.GetProperty().SetDiffuseColor(self._colors.GetColor3d('Blue'))

        _iso_transform = vtk.vtkTransform()
        _iso_transform.RotateZ(90)
        _iso_transform.Translate(0, 0, 0.35)
        _iso_actor.SetUserTransform(_iso_transform)

        return _iso_actor

    def _set_na_vtk(self, filename):
        _na_stlreader = vtk.vtkSTLReader()
        _na_stlreader.SetFileName(filename)

        _na_mapper = vtk.vtkPolyDataMapper()
        _na_mapper.SetInputConnection(_na_stlreader.GetOutputPort())

        _na_actor = vtk.vtkActor()
        _na_actor.SetMapper(_na_mapper)
        _na_actor.GetProperty().SetDiffuseColor(self._colors.GetColor3d('Blue'))

        return _na_actor

    @pyqtSlot(str)
    def on_button(self, b):
        self.placeholder.setText(b)

    @pyqtSlot(str)
    def activate_button(self, filename):
        self._ren.RemoveActor(self._ren.GetActors().GetLastActor())
        self._iren.ReInitialize()

        # self._ren.AddActor(self._set_iso_vtk(filename))
        self._ren.AddActor(self._set_na_vtk(filename))
        CFG.logg.info("Showing " + filename + " in 3D View.")
        self._iren.ReInitialize()


class XSectionsView(QTabWidget):
    """
    view for the cross-section tab
    completion: 10%
    TODO: A LOT
    """
    def __init__(self, parent):
        super(QTabWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.placeholder_text = QLabel("placeholder text tab 2")
        self.layout.addWidget(self.placeholder_text)
        self.setStatusTip("aaaaaaaa")

        settings_button = QPushButton("settings")
        settings_button.clicked.connect(self.open_xsection_settings)
        self.layout.addWidget(settings_button)

    def open_xsection_settings(self):
        dlg = Settings2DView(self)
        # dlg.setWindowTitle("HELLO!")
        dlg.exec_()