from main_window import *
from config import logger

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
