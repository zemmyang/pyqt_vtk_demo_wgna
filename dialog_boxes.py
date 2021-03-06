from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt
import config as CFG


class Settings3DView(QDialog):
    def __init__(self, parent):
        super().__init__()
        _layout = QVBoxLayout()
        self.setLayout(_layout)

        self._title = CFG.SETTINGS_3D_VIEW_TITLE
        self._left = 0
        self._top = 0
        self._width = CFG.SETTINGS_3D_VIEW_SIZE[0]
        self._height = CFG.SETTINGS_3D_VIEW_SIZE[1]
        self.setWindowTitle(self._title)
        self.setGeometry(self._left, self._top, self._width, self._height)

        # show diagram labels
        self._hide_labels = QCheckBox("Show Diagram Labels")
        self._hide_labels.setChecked(True)
        _layout.addWidget(self._hide_labels)

        # hide substrate
        self._hide_substrate = QCheckBox("Hide Substrate")
        self._hide_substrate.setChecked(True)
        _layout.addWidget(self._hide_substrate)

        # background to scale (disabling this makes the waveguide smaller)
        self._bg_to_scale = QCheckBox("Set background to scale")
        self._bg_to_scale.setChecked(True)
        _layout.addWidget(self._bg_to_scale)

        # adjust nano-antenna opacity
        _na_opacity_label = QLabel("Adjust Nano-antenna Opacity")
        _na_opacity_label.setMargin(0)
        _na_opacity_label.setAlignment(Qt.AlignBottom)
        _layout.addWidget(_na_opacity_label)
        self._na_opacity_slider = QSlider(Qt.Horizontal)
        _layout.addWidget(self._na_opacity_slider)

        # adjust isosurface opacity
        _iso_opacity_label = QLabel("Adjust Isosurface Opacity")
        _iso_opacity_label.setMargin(0)
        _iso_opacity_label.setAlignment(Qt.AlignBottom)
        _layout.addWidget(_iso_opacity_label)
        self._iso_opacity_slider = QSlider(Qt.Horizontal)
        _layout.addWidget(self._iso_opacity_slider)

        # hide x-y-z axes
        self._hide_xyz_axes = QCheckBox("Hide XYZ axes")
        _layout.addWidget(self._hide_xyz_axes)

        # place axes at origin
        self._xyz_at_origin = QCheckBox("XYZ axes at origin")
        _layout.addWidget(self._xyz_at_origin)

        # disable mouse-over
        self._disable_mouseover = QCheckBox("Disable Mouse-over")
        self._bg_to_scale.setChecked(True)
        _layout.addWidget(self._disable_mouseover)

        # save/cancel buttons
        _buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self._buttonBox = QDialogButtonBox(_buttons)
        self._buttonBox.accepted.connect(self.accept)
        self._buttonBox.rejected.connect(self.reject)

        _layout.addWidget(self._buttonBox)

class Settings2DView(QDialog):
    def __init__(self, parent):
        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)

        self.title = CFG.SETTINGS_2D_VIEW_TITLE
        self.left = 0
        self.top = 0
        self.width = CFG.SETTINGS_2D_VIEW_SIZE[0]
        self.height = CFG.SETTINGS_2D_VIEW_SIZE[1]
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # xlim min
        xlimmin_label = QLabel("x min lim")
        layout.addWidget(xlimmin_label, 0, 0)

        xlimmin_spinbox = QSpinBox()
        xlimmin_spinbox.setRange(-100, 0)
        xlimmin_spinbox.setValue(-100)
        xlimmin_spinbox.setSingleStep(5)
        xlimmin_spinbox.setSuffix(' nm')
        layout.addWidget(xlimmin_spinbox, 0, 1)

        # xlim max
        xlimmax_label = QLabel("x max lim")
        layout.addWidget(xlimmax_label, 1, 0)

        xlimmax_spinbox = QSpinBox()
        xlimmax_spinbox.setRange(0, 100)
        xlimmax_spinbox.setValue(100)
        xlimmax_spinbox.setSingleStep(5)
        xlimmax_spinbox.setSuffix(' nm')
        layout.addWidget(xlimmax_spinbox, 1, 1)

        # set ylim min
        ylimmin_label = QLabel("y min lim")
        layout.addWidget(ylimmin_label, 2, 0)

        ylimmin_spinbox = QSpinBox()
        ylimmin_spinbox.setRange(-100, 0)
        ylimmin_spinbox.setValue(-100)
        ylimmin_spinbox.setSingleStep(5)
        ylimmin_spinbox.setSuffix(' nm')
        layout.addWidget(ylimmin_spinbox, 2, 1)

        # ylim max
        ylimmax_label = QLabel("y max lim")
        layout.addWidget(ylimmax_label, 3, 0)

        ylimmax_spinbox = QSpinBox()
        ylimmax_spinbox.setRange(0, 100)
        ylimmax_spinbox.setValue(100)
        ylimmax_spinbox.setSingleStep(5)
        ylimmax_spinbox.setSuffix(' nm')
        layout.addWidget(ylimmax_spinbox, 3, 1)

        # set zlim min
        zlimmin_label = QLabel("z min lim")
        layout.addWidget(zlimmin_label, 4, 0)

        zlimmin_spinbox = QSpinBox()
        zlimmin_spinbox.setRange(0, 350)
        zlimmin_spinbox.setValue(0)
        zlimmin_spinbox.setSingleStep(5)
        zlimmin_spinbox.setSuffix(' nm')
        layout.addWidget(zlimmin_spinbox, 4, 1)

        # set zlim max
        zlimmax_label = QLabel("z max lim")
        layout.addWidget(zlimmax_label, 5, 0)

        zlimmax_spinbox = QSpinBox()
        zlimmax_spinbox.setRange(0, 350)
        zlimmax_spinbox.setValue(350)
        zlimmax_spinbox.setSingleStep(5)
        zlimmax_spinbox.setSuffix(' nm')
        layout.addWidget(zlimmax_spinbox, 5, 1)

        # set potential xy lim min
        uxymin_label = QLabel("uxy min lim")
        layout.addWidget(uxymin_label, 6, 0)

        uxymin_spinbox = QSpinBox()
        uxymin_spinbox.setRange(-18, -10)
        uxymin_spinbox.setValue(-18)
        uxymin_spinbox.setSingleStep(1)
        uxymin_spinbox.setSuffix(' mK')
        layout.addWidget(uxymin_spinbox, 6, 1)

        # set potential xy lim min
        uxymax_label = QLabel("uxy max lim")
        layout.addWidget(uxymax_label, 7, 0)

        uxymax_spinbox = QSpinBox()
        uxymax_spinbox.setRange(-18, -10)
        uxymax_spinbox.setValue(-10)
        uxymax_spinbox.setSingleStep(1)
        uxymax_spinbox.setSuffix(' mK')
        layout.addWidget(uxymax_spinbox, 7, 1)

        # set potential zlim min
        uzmin_label = QLabel("uz min lim")
        layout.addWidget(uzmin_label, 8, 0)

        uzmin_spinbox = QSpinBox()
        uzmin_spinbox.setRange(-18, 0)
        uzmin_spinbox.setValue(-18)
        uzmin_spinbox.setSingleStep(1)
        uzmin_spinbox.setSuffix(' mK')
        layout.addWidget(uzmin_spinbox, 8, 1)

        # set potential zlim min
        uzmax_label = QLabel("uz max lim")
        layout.addWidget(uzmax_label, 9, 0)

        uzmax_spinbox = QSpinBox()
        uzmax_spinbox.setRange(-18, 0)
        uzmax_spinbox.setValue(0)
        uzmax_spinbox.setSingleStep(1)
        uzmax_spinbox.setSuffix(' mK')
        layout.addWidget(uzmax_spinbox, 9, 1)

        # view legend
        viewlegend = QCheckBox("View Legend")
        layout.addWidget(viewlegend, 10, 0)

        # save/cancel buttons
        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout.addWidget(self.buttonBox, 11, 1)

    def set_xlim(self):
        xmin = self.xlimmin_spinbox.Value()
        xmax = self.xlimmax_spinbox.Value()
        return xmin, xmax