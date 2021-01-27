from main_window import *
from config import logger

def main():
    logger.info("Program started")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    logger.info("Program closing")
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
