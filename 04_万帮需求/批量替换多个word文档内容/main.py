import os
import sys

import win
from PyQt5.QtWidgets import QApplication, QMainWindow

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = win.ImgCut()
    ui.show()
    sys.exit(app.exec_())