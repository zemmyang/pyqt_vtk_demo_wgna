from PyQt5.Qt import *
import config as CFG
from dialog_boxes import *

BONUS_FEATURES = CFG.DEBUG_MODE


class XSectionsView(QTabWidget):
    """
    view for the cross-section tab
    completion: 10%
    TODO: A LOT
    """
    def __init__(self, parent):
        super(QTabWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.placeholder_text = QLabel("To be Implemented")
        self.layout.addWidget(self.placeholder_text)
        self.setStatusTip(" ")

        settings_button = QPushButton("settings")
        settings_button.setEnabled(BONUS_FEATURES)
        settings_button.clicked.connect(self.open_xsection_settings)
        self.layout.addWidget(settings_button)

    def open_xsection_settings(self):
        dlg = Settings2DView(self)
        # dlg.setWindowTitle("HELLO!")
        dlg.exec_()